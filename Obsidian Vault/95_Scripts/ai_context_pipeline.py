#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Small orchestration wrapper for the AI Context PDF -> Markdown -> RAG flow."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
CONVERTER = SCRIPT_DIR / "mineru_pdf_converter.py"
BUILD_NODES = SCRIPT_DIR / "build_nodes.py"
INDEX_QDRANT = SCRIPT_DIR / "index_qdrant.py"
QUERY = SCRIPT_DIR / "query.py"
CONFIG = SCRIPT_DIR / "config.yaml"


def run_step(args: list[str | Path]) -> int:
    print("Running:", " ".join(str(a) for a in args))
    result = subprocess.run([sys.executable, *map(str, args)])
    return result.returncode


def command_all(args: argparse.Namespace) -> int:
    convert_args: list[str | Path] = [CONVERTER, "convert"]
    if args.limit:
        convert_args.extend(["--limit", str(args.limit)])
    if args.dry_run:
        convert_args.append("--dry-run")
    if args.no_citekey:
        convert_args.append("--no-citekey")
    code = run_step(convert_args)
    if code != 0 or args.dry_run:
        return code
    code = run_step([BUILD_NODES, "--config", CONFIG])
    if code != 0:
        return code
    return run_step([INDEX_QDRANT, "--config", CONFIG])


def command_convert(args: argparse.Namespace) -> int:
    convert_args: list[str | Path] = [CONVERTER, "convert"]
    if args.limit:
        convert_args.extend(["--limit", str(args.limit)])
    if args.dry_run:
        convert_args.append("--dry-run")
    if args.force:
        convert_args.append("--force")
    if args.no_citekey:
        convert_args.append("--no-citekey")
    return run_step(convert_args)


def command_build(args: argparse.Namespace) -> int:
    build_args: list[str | Path] = [BUILD_NODES, "--config", CONFIG]
    if args.force:
        build_args.append("--force")
    code = run_step(build_args)
    if code != 0:
        return code
    index_args: list[str | Path] = [INDEX_QDRANT, "--config", CONFIG]
    if args.force:
        index_args.append("--force")
    return run_step(index_args)


def command_query(args: argparse.Namespace) -> int:
    query_args: list[str | Path] = [QUERY, "--config", CONFIG, "--query", args.question, "--top-k", str(args.top_k)]
    if args.answer:
        query_args.append("--answer")
    return run_step(query_args)


def command_stats(_: argparse.Namespace) -> int:
    return run_step([BUILD_NODES, "--config", CONFIG, "--dry-run"])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the AI Context automation pipeline.")
    sub = parser.add_subparsers(dest="command", required=True)

    all_cmd = sub.add_parser("all", help="Convert new PDFs, then build the RAG index.")
    all_cmd.add_argument("--limit", type=int, default=0)
    all_cmd.add_argument("--dry-run", action="store_true")
    all_cmd.add_argument("--no-citekey", action="store_true")
    all_cmd.set_defaults(func=command_all)

    convert_cmd = sub.add_parser("convert", help="Run only PDF conversion.")
    convert_cmd.add_argument("--limit", type=int, default=0)
    convert_cmd.add_argument("--dry-run", action="store_true")
    convert_cmd.add_argument("--force", action="store_true")
    convert_cmd.add_argument("--no-citekey", action="store_true")
    convert_cmd.set_defaults(func=command_convert)

    build_cmd = sub.add_parser("build-kb", help="Build nodes and index Qdrant.")
    build_cmd.add_argument("--force", action="store_true")
    build_cmd.set_defaults(func=command_build)

    query_cmd = sub.add_parser("query", help="Query the RAG index.")
    query_cmd.add_argument("question")
    query_cmd.add_argument("--top-k", type=int, default=5)
    query_cmd.add_argument("--answer", action="store_true")
    query_cmd.set_defaults(func=command_query)

    stats_cmd = sub.add_parser("stats", help="Show node-build stats.")
    stats_cmd.set_defaults(func=command_stats)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
