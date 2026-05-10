#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compatibility wrapper for the Qdrant-based RAG pipeline.

Prefer using build_nodes.py, index_qdrant.py, and query.py directly. This file is
kept so older commands still work without silently using the former simple FAISS
pipeline.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = SCRIPT_DIR / "config.yaml"


def run(args: list[str | Path]) -> int:
    print("Running:", " ".join(str(a) for a in args))
    return subprocess.run([sys.executable, *map(str, args)]).returncode


def build(args: argparse.Namespace) -> int:
    code = run([SCRIPT_DIR / "build_nodes.py", "--config", args.config])
    if code != 0:
        return code
    return run([SCRIPT_DIR / "index_qdrant.py", "--config", args.config])


def query(args: argparse.Namespace) -> int:
    query_args: list[str | Path] = [SCRIPT_DIR / "query.py", "--config", args.config, "--query", args.question]
    if args.top_k:
        query_args.extend(["--top-k", str(args.top_k)])
    if args.answer:
        query_args.append("--answer")
    return run(query_args)


def stats(args: argparse.Namespace) -> int:
    return run([SCRIPT_DIR / "build_nodes.py", "--config", args.config, "--dry-run"])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compatibility wrapper for the Qdrant RAG pipeline.")
    sub = parser.add_subparsers(dest="command", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--config", default=str(DEFAULT_CONFIG))

    build_cmd = sub.add_parser("build", parents=[common])
    build_cmd.set_defaults(func=build)

    query_cmd = sub.add_parser("query", parents=[common])
    query_cmd.add_argument("question")
    query_cmd.add_argument("--top-k", type=int, default=0)
    query_cmd.add_argument("--answer", action="store_true")
    query_cmd.set_defaults(func=query)

    stats_cmd = sub.add_parser("stats", parents=[common])
    stats_cmd.set_defaults(func=stats)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
