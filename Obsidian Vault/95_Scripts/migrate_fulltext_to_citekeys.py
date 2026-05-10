#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rename existing MinerU fulltext folders to Better BibTeX citekeys."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from mineru_pdf_converter import (
    DEFAULT_BBT_JSON_RPC,
    DEFAULT_FULLTEXT_DIR,
    DEFAULT_MANIFEST_PATH,
    DEFAULT_ZOTERO_DB,
    metadata_path_for,
    repo_relative,
)
from zotero_citekey_resolver import resolve_pdf_citekey, safe_paper_id


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def rename_markdown_file(folder: Path, old_id: str, new_id: str) -> Path:
    old_md = folder / f"{old_id}.md"
    new_md = folder / f"{new_id}.md"
    if old_md.exists() and old_md != new_md:
        old_md.rename(new_md)
        return new_md
    md_files = sorted(folder.glob("*.md"))
    if md_files and md_files[0] != new_md:
        md_files[0].rename(new_md)
    return new_md


def migrate_one(metadata_path: Path, args: argparse.Namespace) -> tuple[str, str, str]:
    item = read_json(metadata_path, {})
    old_id = str(item.get("paper_id") or metadata_path.parent.name)
    pdf_path_raw = item.get("pdf_path")
    if not pdf_path_raw:
        return "skipped", old_id, "metadata has no pdf_path"

    resolution = resolve_pdf_citekey(Path(pdf_path_raw), args.zotero_db, args.bbt_url)
    if not resolution.citation_key:
        return "skipped", old_id, f"no citekey: {resolution.error or 'unknown error'}"

    new_id = safe_paper_id(resolution.citation_key)
    if old_id == new_id:
        return "unchanged", old_id, "already canonical"

    old_folder = metadata_path.parent
    new_folder = args.fulltext_dir / new_id
    if new_folder.exists() and new_folder.resolve() != old_folder.resolve():
        target_metadata = read_json(metadata_path_for(args.fulltext_dir, new_id), {})
        if target_metadata.get("pdf_sha256") != item.get("pdf_sha256"):
            return "conflict", old_id, f"target exists with different pdf hash: {new_folder}"

    if args.dry_run:
        return "would-migrate", old_id, new_id

    if new_folder.exists() and new_folder.resolve() != old_folder.resolve():
        raise FileExistsError(f"Target folder already exists: {new_folder}")

    old_folder.rename(new_folder)
    new_md = rename_markdown_file(new_folder, old_id, new_id)
    metadata = read_json(new_folder / "metadata.json", {})
    metadata.update(
        {
            "paper_id": new_id,
            "paper_id_source": "better_bibtex_citekey",
            "citation_key": resolution.citation_key,
            "zotero_attachment_key": resolution.attachment_key,
            "zotero_parent_key": resolution.parent_key,
            "zotero_library_id": resolution.library_id,
            "md_path": repo_relative(new_md),
            "output_dir": repo_relative(new_folder),
        }
    )
    metadata.pop("citekey_error", None)
    write_json(new_folder / "metadata.json", metadata)
    update_manifest(args.manifest, item.get("pdf_sha256"), metadata)
    return "migrated", old_id, new_id


def update_manifest(manifest_path: Path, pdf_sha256: str | None, item: dict[str, Any]) -> None:
    if not pdf_sha256:
        return
    manifest = read_json(manifest_path, {"version": 1, "items_by_hash": {}, "items_by_path": {}})
    manifest.setdefault("items_by_hash", {})[pdf_sha256] = item
    if item.get("pdf_path"):
        manifest.setdefault("items_by_path", {})[item["pdf_path"]] = pdf_sha256
    write_json(manifest_path, manifest)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Migrate fulltext_md folders from PDF names to Better BibTeX citekeys.")
    parser.add_argument("--fulltext-dir", type=Path, default=DEFAULT_FULLTEXT_DIR)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--zotero-db", type=Path, default=DEFAULT_ZOTERO_DB)
    parser.add_argument("--bbt-url", default=DEFAULT_BBT_JSON_RPC)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--backup", type=Path, help="Optional backup directory before renaming.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.backup and not args.dry_run:
        shutil.copytree(args.fulltext_dir, args.backup, dirs_exist_ok=True)
        print(f"Backup written: {args.backup}")

    metadata_files = sorted(args.fulltext_dir.glob("*/metadata.json"))
    counts: dict[str, int] = {}
    for metadata_path in metadata_files:
        status, old_id, detail = migrate_one(metadata_path, args)
        counts[status] = counts.get(status, 0) + 1
        print(f"{status}: {old_id} -> {detail}")
    print(json.dumps(counts, ensure_ascii=False, indent=2))
    return 1 if counts.get("conflict") else 0


if __name__ == "__main__":
    raise SystemExit(main())
