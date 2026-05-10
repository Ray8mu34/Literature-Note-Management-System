#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scan Zotero storage, convert new PDFs with MinerU, and normalize outputs into
60_AI_Context/fulltext_md.

Zotero storage is intentionally an absolute path. Vault paths are derived from
this repository so moving the vault only requires editing repository-local paths.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from zotero_citekey_resolver import (
    DEFAULT_BBT_JSON_RPC,
    DEFAULT_ZOTERO_DB,
    CitekeyResolution,
    resolve_pdf_citekey,
    safe_paper_id as safe_identifier,
)


VAULT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ZOTERO_STORAGE = Path(r"C:\Users\30674\Zotero\storage")
DEFAULT_FULLTEXT_DIR = VAULT_ROOT / "60_AI_Context" / "fulltext_md"
DEFAULT_MANIFEST_PATH = VAULT_ROOT / "60_AI_Context" / "manifests" / "pdf_conversion_manifest.json"
DEFAULT_TEMP_DIR = VAULT_ROOT / "60_AI_Context" / "_mineru_tmp"

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
MANIFEST_VERSION = 1


@dataclass(frozen=True)
class PdfItem:
    path: Path
    size: int
    mtime: float
    sha256: str


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(VAULT_ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(chunk_size), b""):
            h.update(block)
    return h.hexdigest()


def safe_paper_id(pdf_path: Path, max_prefix_len: int = 96) -> str:
    return safe_identifier(pdf_path.stem, max_prefix_len)


def choose_paper_id(
    pdf: PdfItem,
    fulltext_dir: Path,
    existing: dict[str, Any] | None,
    citekey: CitekeyResolution | None = None,
) -> str:
    if citekey and citekey.citation_key:
        base = safe_identifier(citekey.citation_key)
    elif existing and existing.get("paper_id"):
        return str(existing["paper_id"])
    else:
        base = safe_paper_id(pdf.path)
    metadata_path = metadata_path_for(fulltext_dir, base)
    if not metadata_path.exists():
        return base
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return f"{base}_{pdf.sha256[:8]}"
    if metadata.get("pdf_sha256") in {None, pdf.sha256}:
        return base
    return f"{base}_{pdf.sha256[:8]}"


def normalized_tokens(text: str) -> set[str]:
    tokens = re.findall(r"[a-z0-9\u4e00-\u9fff]+", text.lower())
    return {token for token in tokens if len(token) >= 3}


def load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"version": MANIFEST_VERSION, "items_by_hash": {}, "items_by_path": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("version", MANIFEST_VERSION)
    data.setdefault("items_by_hash", {})
    data.setdefault("items_by_path", {})
    return data


def save_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def scan_pdfs(storage_dir: Path, max_depth: int | None = 3) -> list[Path]:
    storage_dir = storage_dir.resolve()
    pdfs: list[Path] = []
    for root, dirs, files in os.walk(storage_dir):
        root_path = Path(root)
        if max_depth is not None:
            depth = len(root_path.relative_to(storage_dir).parts)
            if depth > max_depth:
                dirs[:] = []
                continue
        for name in files:
            if name.lower().endswith(".pdf"):
                pdfs.append(root_path / name)
    return sorted(pdfs, key=lambda p: str(p).lower())


def build_pdf_item(path: Path) -> PdfItem:
    stat = path.stat()
    return PdfItem(path=path.resolve(), size=stat.st_size, mtime=stat.st_mtime, sha256=sha256_file(path))


def metadata_path_for(fulltext_dir: Path, paper_id: str) -> Path:
    return fulltext_dir / paper_id / "metadata.json"


def md_path_for(fulltext_dir: Path, paper_id: str) -> Path:
    return fulltext_dir / paper_id / f"{paper_id}.md"


def build_metadata(
    pdf: PdfItem,
    paper_id: str,
    md_path: Path,
    status: str,
    error: str | None = None,
    citekey: CitekeyResolution | None = None,
) -> dict[str, Any]:
    item = {
        "paper_id": paper_id,
        "pdf_path": str(pdf.path),
        "pdf_sha256": pdf.sha256,
        "pdf_size": pdf.size,
        "pdf_mtime": pdf.mtime,
        "md_path": repo_relative(md_path),
        "output_dir": repo_relative(md_path.parent),
        "mineru_status": status,
        "updated_at": utc_now(),
    }
    if citekey:
        item.update(
            {
                "paper_id_source": "better_bibtex_citekey" if citekey.citation_key else "pdf_filename_fallback",
                "citation_key": citekey.citation_key,
                "zotero_attachment_key": citekey.attachment_key,
                "zotero_parent_key": citekey.parent_key,
                "zotero_library_id": citekey.library_id,
                "citekey_error": citekey.error,
            }
        )
    else:
        item["paper_id_source"] = "pdf_filename_fallback"
    if error:
        item["error"] = error
    return item


def existing_item_for_hash(manifest: dict[str, Any], pdf_hash: str, fulltext_dir: Path) -> dict[str, Any] | None:
    item = manifest.get("items_by_hash", {}).get(pdf_hash)
    if not item:
        return None
    md_rel = item.get("md_path")
    if md_rel and (VAULT_ROOT / md_rel).exists():
        return item
    paper_id = item.get("paper_id")
    if paper_id and md_path_for(fulltext_dir, paper_id).exists():
        return item
    return None


def load_existing_metadata(fulltext_dir: Path, manifest: dict[str, Any]) -> None:
    if not fulltext_dir.exists():
        return
    for metadata_file in fulltext_dir.glob("*/metadata.json"):
        try:
            item = json.loads(metadata_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        pdf_hash = item.get("pdf_sha256")
        pdf_path = item.get("pdf_path")
        if not pdf_hash:
            continue
        manifest["items_by_hash"][pdf_hash] = item
        if pdf_path:
            manifest["items_by_path"][pdf_path] = pdf_hash


def adopt_existing_output(pdf: PdfItem, fulltext_dir: Path, manifest: dict[str, Any]) -> dict[str, Any] | None:
    """Best-effort adoption for legacy folders created before metadata existed."""
    if not fulltext_dir.exists():
        return None
    pdf_tokens = normalized_tokens(pdf.path.stem)
    if len(pdf_tokens) < 3:
        return None

    best: tuple[int, Path, Path] | None = None
    for md_file in fulltext_dir.glob("*/*.md"):
        folder = md_file.parent
        if (folder / "metadata.json").exists():
            continue
        candidate_tokens = normalized_tokens(folder.name) | normalized_tokens(md_file.stem)
        score = len(pdf_tokens & candidate_tokens)
        if score >= 3 and (best is None or score > best[0]):
            best = (score, folder, md_file)

    if best is None:
        return None

    _, folder, md_file = best
    paper_id = folder.name
    target_md = md_path_for(fulltext_dir, paper_id)
    if md_file.name != target_md.name:
        target_md.write_text(md_file.read_text(encoding="utf-8"), encoding="utf-8")
    item = build_metadata(pdf, paper_id, target_md, "adopted_existing")
    metadata_path_for(fulltext_dir, paper_id).write_text(json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest["items_by_hash"][pdf.sha256] = item
    manifest["items_by_path"][str(pdf.path)] = pdf.sha256
    return item


def run_mineru(pdf_path: Path, output_dir: Path, env_name: str, timeout: int) -> subprocess.CompletedProcess[str]:
    cmd = [
        "conda",
        "run",
        "-n",
        env_name,
        "mineru",
        "-p",
        str(pdf_path),
        "-o",
        str(output_dir),
        "--format",
        "md",
        "-b",
        "pipeline",
    ]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def find_primary_markdown(root: Path) -> Path:
    md_files = [p for p in root.rglob("*.md") if p.is_file()]
    if not md_files:
        raise FileNotFoundError(f"No markdown file produced under {root}")
    return max(md_files, key=lambda p: p.stat().st_size)


def copy_images(converted_root: Path, final_dir: Path) -> None:
    image_files = [p for p in converted_root.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS]
    if not image_files:
        return
    image_dir = final_dir / "images"
    image_dir.mkdir(parents=True, exist_ok=True)
    seen: set[str] = set()
    for src in image_files:
        name = src.name
        if name in seen:
            name = f"{src.stem}_{sha256_file(src)[:8]}{src.suffix.lower()}"
        seen.add(name)
        shutil.copy2(src, image_dir / name)


def normalize_mineru_output(converted_root: Path, final_dir: Path, paper_id: str) -> Path:
    primary_md = find_primary_markdown(converted_root)
    final_dir.mkdir(parents=True, exist_ok=True)
    final_md = final_dir / f"{paper_id}.md"
    final_md.write_text(primary_md.read_text(encoding="utf-8"), encoding="utf-8")
    copy_images(converted_root, final_dir)
    return final_md


def convert_one(
    pdf: PdfItem,
    fulltext_dir: Path,
    temp_dir: Path,
    manifest: dict[str, Any],
    env_name: str,
    timeout: int,
    force: bool,
    keep_temp: bool,
    use_citekey: bool,
    zotero_db: Path,
    bbt_url: str,
) -> tuple[str, str]:
    existing = existing_item_for_hash(manifest, pdf.sha256, fulltext_dir)
    if existing and not force:
        return "skipped", existing["paper_id"]

    citekey = resolve_pdf_citekey(pdf.path, zotero_db=zotero_db, bbt_url=bbt_url) if use_citekey else None
    adopted = adopt_existing_output(pdf, fulltext_dir, manifest)
    if adopted and not force:
        return "adopted", adopted["paper_id"]

    paper_id = choose_paper_id(pdf, fulltext_dir, existing, citekey)
    temp_parent = temp_dir / paper_id
    if temp_parent.exists():
        shutil.rmtree(temp_parent)
    temp_parent.mkdir(parents=True, exist_ok=True)

    try:
        result = run_mineru(pdf.path, temp_parent, env_name, timeout)
        if result.returncode != 0:
            item = build_metadata(
                pdf,
                paper_id,
                md_path_for(fulltext_dir, paper_id),
                "failed",
                result.stderr.strip(),
                citekey,
            )
            manifest["items_by_hash"][pdf.sha256] = item
            manifest["items_by_path"][str(pdf.path)] = pdf.sha256
            return "failed", paper_id

        final_md = normalize_mineru_output(temp_parent, fulltext_dir / paper_id, paper_id)
        item = build_metadata(pdf, paper_id, final_md, "success", citekey=citekey)
        metadata_path_for(fulltext_dir, paper_id).write_text(json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8")
        manifest["items_by_hash"][pdf.sha256] = item
        manifest["items_by_path"][str(pdf.path)] = pdf.sha256
        return "converted", paper_id
    except Exception as exc:  # noqa: BLE001 - record conversion failures and continue.
        item = build_metadata(pdf, paper_id, md_path_for(fulltext_dir, paper_id), "failed", str(exc), citekey)
        manifest["items_by_hash"][pdf.sha256] = item
        manifest["items_by_path"][str(pdf.path)] = pdf.sha256
        return "failed", paper_id
    finally:
        if not keep_temp and temp_parent.exists():
            shutil.rmtree(temp_parent, ignore_errors=True)


def command_scan(args: argparse.Namespace) -> int:
    pdf_paths = scan_pdfs(args.zotero_storage, args.max_depth)
    print(f"Found {len(pdf_paths)} PDF files under {args.zotero_storage}")
    for pdf in pdf_paths[: args.limit or len(pdf_paths)]:
        print(pdf)
    if args.limit and len(pdf_paths) > args.limit:
        print(f"... {len(pdf_paths) - args.limit} more")
    return 0


def command_convert(args: argparse.Namespace) -> int:
    args.fulltext_dir.mkdir(parents=True, exist_ok=True)
    args.temp_dir.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest(args.manifest)
    load_existing_metadata(args.fulltext_dir, manifest)

    pdf_paths = scan_pdfs(args.zotero_storage, args.max_depth)
    if args.limit:
        pdf_paths = pdf_paths[: args.limit]

    print(f"Found {len(pdf_paths)} PDF files to inspect")
    counts = {"converted": 0, "skipped": 0, "adopted": 0, "failed": 0}

    for index, pdf_path in enumerate(pdf_paths, 1):
        pdf = build_pdf_item(pdf_path)
        existing = existing_item_for_hash(manifest, pdf.sha256, args.fulltext_dir)
        if args.dry_run:
            status = "would-skip" if existing and not args.force else "would-convert"
            if existing and not args.force:
                paper_id = existing.get("paper_id", pdf.path.stem)
            else:
                citekey = (
                    resolve_pdf_citekey(pdf.path, zotero_db=args.zotero_db, bbt_url=args.bbt_url)
                    if not args.no_citekey
                    else None
                )
                paper_id = choose_paper_id(pdf, args.fulltext_dir, existing, citekey)
            print(f"[{index}/{len(pdf_paths)}] {status}: {paper_id} <- {pdf.path}")
            continue

        status, paper_id = convert_one(
            pdf=pdf,
            fulltext_dir=args.fulltext_dir,
            temp_dir=args.temp_dir,
            manifest=manifest,
            env_name=args.env,
            timeout=args.timeout,
            force=args.force,
            keep_temp=args.keep_temp,
            use_citekey=not args.no_citekey,
            zotero_db=args.zotero_db,
            bbt_url=args.bbt_url,
        )
        counts[status] += 1
        save_manifest(args.manifest, manifest)
        print(f"[{index}/{len(pdf_paths)}] {status}: {paper_id}")

    if not args.dry_run:
        save_manifest(args.manifest, manifest)
    print(json.dumps(counts, ensure_ascii=False, indent=2))
    return 1 if counts["failed"] else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert Zotero PDFs to normalized MinerU markdown outputs.")
    sub = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--zotero-storage", type=Path, default=DEFAULT_ZOTERO_STORAGE)
    common.add_argument("--fulltext-dir", type=Path, default=DEFAULT_FULLTEXT_DIR)
    common.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH)
    common.add_argument("--max-depth", type=int, default=3)
    common.add_argument("--limit", type=int, default=0)
    common.add_argument("--zotero-db", type=Path, default=DEFAULT_ZOTERO_DB)
    common.add_argument("--bbt-url", default=DEFAULT_BBT_JSON_RPC)

    scan = sub.add_parser("scan", parents=[common], help="List discovered PDFs.")
    scan.set_defaults(func=command_scan)

    convert = sub.add_parser("convert", parents=[common], help="Convert new PDFs and skip existing outputs.")
    convert.add_argument("--env", default="mineru_env")
    convert.add_argument("--temp-dir", type=Path, default=DEFAULT_TEMP_DIR)
    convert.add_argument("--timeout", type=int, default=1200)
    convert.add_argument("--force", action="store_true")
    convert.add_argument("--dry-run", action="store_true")
    convert.add_argument("--keep-temp", action="store_true")
    convert.add_argument("--no-citekey", action="store_true", help="Disable Better BibTeX citekey resolution.")
    convert.set_defaults(func=command_convert)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
