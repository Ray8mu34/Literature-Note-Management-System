#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""User-friendly wrapper around mineru_pdf_converter.py."""

from __future__ import annotations

import argparse
from pathlib import Path

import mineru_pdf_converter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert Zotero PDFs to normalized Markdown with MinerU.")
    parser.add_argument("--input", type=Path, default=mineru_pdf_converter.DEFAULT_ZOTERO_STORAGE)
    parser.add_argument("--output", type=Path, default=mineru_pdf_converter.DEFAULT_FULLTEXT_DIR)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--env", default="mineru_env")
    parser.add_argument("--timeout", type=int, default=1200)
    parser.add_argument("--zotero-db", type=Path, default=mineru_pdf_converter.DEFAULT_ZOTERO_DB)
    parser.add_argument("--bbt-url", default=mineru_pdf_converter.DEFAULT_BBT_JSON_RPC)
    parser.add_argument("--no-citekey", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    argv = [
        "convert",
        "--zotero-storage",
        str(args.input),
        "--fulltext-dir",
        str(args.output),
        "--env",
        args.env,
        "--timeout",
        str(args.timeout),
        "--zotero-db",
        str(args.zotero_db),
        "--bbt-url",
        args.bbt_url,
    ]
    if args.dry_run:
        argv.append("--dry-run")
    if args.limit:
        argv.extend(["--limit", str(args.limit)])
    if args.force:
        argv.append("--force")
    if args.keep_temp:
        argv.append("--keep-temp")
    if args.no_citekey:
        argv.append("--no-citekey")
    return mineru_pdf_converter.main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
