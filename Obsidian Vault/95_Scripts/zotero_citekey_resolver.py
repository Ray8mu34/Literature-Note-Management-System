#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Resolve Zotero attachment PDFs to Better BibTeX citation keys.

The PDF path usually looks like ``Zotero/storage/ABCDEFGH/file.pdf`` where
``ABCDEFGH`` is the Zotero attachment item key. We read zotero.sqlite in
read-only mode to find the parent bibliographic item, then ask Better BibTeX's
local JSON-RPC API for the citation key.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import re
import sqlite3
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_ZOTERO_DB = Path(r"C:\Users\30674\Zotero\zotero.sqlite")
DEFAULT_BBT_JSON_RPC = "http://localhost:23119/better-bibtex/json-rpc"


@dataclasses.dataclass(frozen=True)
class ZoteroItemRef:
    attachment_key: str
    parent_key: str | None
    library_id: int | None
    item_id: int | None
    parent_item_id: int | None

    @property
    def citation_item_key(self) -> str:
        return self.parent_key or self.attachment_key

    @property
    def better_bibtex_key(self) -> str:
        if self.library_id is None:
            return self.citation_item_key
        return f"{self.library_id}:{self.citation_item_key}"


@dataclasses.dataclass(frozen=True)
class CitekeyResolution:
    pdf_path: Path
    attachment_key: str
    parent_key: str | None
    library_id: int | None
    citation_key: str | None
    error: str | None = None


def attachment_key_from_pdf(pdf_path: Path) -> str:
    return pdf_path.resolve().parent.name


def sqlite_uri(path: Path) -> str:
    return f"{path.resolve().as_uri()}?mode=ro"


def sqlite_immutable_uri(path: Path) -> str:
    return f"{path.resolve().as_uri()}?mode=ro&immutable=1"


def execute_parent_lookup(zotero_db_uri: str, attachment_key: str) -> tuple[Any, ...] | None:
    query = """
        SELECT
            child.itemID AS attachmentItemID,
            child.key AS attachmentKey,
            child.libraryID AS attachmentLibraryID,
            parent.itemID AS parentItemID,
            parent.key AS parentKey,
            parent.libraryID AS parentLibraryID
        FROM items AS child
        LEFT JOIN itemAttachments AS attachment
            ON attachment.itemID = child.itemID
        LEFT JOIN items AS parent
            ON parent.itemID = attachment.parentItemID
        WHERE child.key = ?
        LIMIT 1
    """
    with sqlite3.connect(zotero_db_uri, uri=True, timeout=10.0) as conn:
        conn.execute("PRAGMA query_only = ON")
        conn.execute("PRAGMA busy_timeout = 10000")
        row = conn.execute(query, (attachment_key,)).fetchone()
    return row


def lookup_parent_item(zotero_db: Path, attachment_key: str) -> ZoteroItemRef | None:
    if not zotero_db.exists():
        raise FileNotFoundError(f"Zotero database not found: {zotero_db}")
    try:
        row = execute_parent_lookup(sqlite_uri(zotero_db), attachment_key)
    except sqlite3.OperationalError as exc:
        if "locked" not in str(exc).lower():
            raise
        row = execute_parent_lookup(sqlite_immutable_uri(zotero_db), attachment_key)
    if row is None:
        return None
    attachment_item_id, attachment_key, attachment_library_id, parent_item_id, parent_key, parent_library_id = row
    library_id = parent_library_id if parent_library_id is not None else attachment_library_id
    return ZoteroItemRef(
        attachment_key=str(attachment_key),
        parent_key=str(parent_key) if parent_key else None,
        library_id=int(library_id) if library_id is not None else None,
        item_id=int(attachment_item_id) if attachment_item_id is not None else None,
        parent_item_id=int(parent_item_id) if parent_item_id is not None else None,
    )


class BetterBibTeXClient:
    def __init__(self, url: str = DEFAULT_BBT_JSON_RPC, timeout: float = 5.0):
        self.url = url
        self.timeout = timeout
        self._request_id = 0

    def call(self, method: str, params: list[Any] | None = None) -> Any:
        self._request_id += 1
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
            "id": self._request_id,
        }
        request = urllib.request.Request(
            self.url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=self.timeout) as response:  # noqa: S310 - local trusted endpoint.
            data = json.loads(response.read().decode("utf-8"))
        if "error" in data:
            raise RuntimeError(data["error"])
        return data.get("result")

    def ready(self) -> bool:
        try:
            return bool(self.call("api.ready", []))
        except (OSError, RuntimeError, urllib.error.URLError):
            return False

    def citationkey(self, item_ref: ZoteroItemRef) -> str | None:
        candidates = [item_ref.better_bibtex_key]
        if item_ref.citation_item_key not in candidates:
            candidates.append(item_ref.citation_item_key)

        last_error: Exception | None = None
        for candidate in candidates:
            try:
                result = self.call("item.citationkey", [[candidate]])
            except Exception as exc:  # noqa: BLE001 - try alternate key form.
                last_error = exc
                continue
            key = extract_citation_key(result, candidate)
            if key:
                return key
        if last_error:
            raise last_error
        return None


def extract_citation_key(result: Any, requested_key: str) -> str | None:
    if isinstance(result, str):
        return result or None
    if isinstance(result, list):
        if not result:
            return None
        first = result[0]
        if isinstance(first, str):
            return first or None
        if isinstance(first, dict):
            return first.get("citationKey") or first.get("citekey") or first.get("citationkey")
    if isinstance(result, dict):
        direct = result.get(requested_key)
        if isinstance(direct, str):
            return direct or None
        for key in ("citationKey", "citekey", "citationkey"):
            value = result.get(key)
            if isinstance(value, str):
                return value or None
        for value in result.values():
            if isinstance(value, str):
                return value or None
    return None


def safe_paper_id(identifier: str, max_len: int = 120) -> str:
    value = identifier.strip()
    value = re.sub(r"\s+", "_", value)
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", value)
    value = re.sub(r"_+", "_", value).strip("._ ")
    return value[:max_len].strip("._ ") or "paper"


def resolve_pdf_citekey(
    pdf_path: Path,
    zotero_db: Path = DEFAULT_ZOTERO_DB,
    bbt_url: str = DEFAULT_BBT_JSON_RPC,
    timeout: float = 5.0,
) -> CitekeyResolution:
    attachment_key = attachment_key_from_pdf(pdf_path)
    try:
        item_ref = lookup_parent_item(zotero_db, attachment_key)
    except Exception as exc:  # noqa: BLE001 - surface as resolution error.
        return CitekeyResolution(pdf_path, attachment_key, None, None, None, str(exc))
    if item_ref is None:
        return CitekeyResolution(pdf_path, attachment_key, None, None, None, "attachment item key not found")

    client = BetterBibTeXClient(bbt_url, timeout=timeout)
    if not client.ready():
        return CitekeyResolution(
            pdf_path,
            attachment_key,
            item_ref.parent_key,
            item_ref.library_id,
            None,
            "Better BibTeX JSON-RPC is not ready; open Zotero and enable Better BibTeX",
        )
    try:
        citation_key = client.citationkey(item_ref)
    except Exception as exc:  # noqa: BLE001 - keep converter non-fatal.
        return CitekeyResolution(pdf_path, attachment_key, item_ref.parent_key, item_ref.library_id, None, str(exc))
    return CitekeyResolution(pdf_path, attachment_key, item_ref.parent_key, item_ref.library_id, citation_key)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Resolve a Zotero storage PDF to a Better BibTeX citekey.")
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--zotero-db", type=Path, default=DEFAULT_ZOTERO_DB)
    parser.add_argument("--bbt-url", default=DEFAULT_BBT_JSON_RPC)
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = resolve_pdf_citekey(args.pdf, args.zotero_db, args.bbt_url, args.timeout)
    if args.json:
        print(json.dumps(dataclasses.asdict(result), ensure_ascii=False, indent=2, default=str))
    else:
        print(f"pdf: {result.pdf_path}")
        print(f"attachment_key: {result.attachment_key}")
        print(f"parent_key: {result.parent_key or ''}")
        print(f"library_id: {result.library_id if result.library_id is not None else ''}")
        print(f"citation_key: {result.citation_key or ''}")
        if result.error:
            print(f"error: {result.error}")
    return 0 if result.citation_key else 1


if __name__ == "__main__":
    raise SystemExit(main())
