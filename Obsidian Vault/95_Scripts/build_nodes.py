#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build citation-aware retrieval nodes from MinerU markdown files."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any

from rag_utils import (
    DEFAULT_CONFIG,
    RagConfig,
    ensure_runtime_dirs,
    iter_jsonl,
    load_config,
    read_json,
    repo_relative,
    sha256_bytes,
    sha256_file,
    write_json,
    write_jsonl,
)


NODE_MANIFEST_VERSION = 1


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def clean_markdown_text(text: str) -> str:
    text = re.sub(r"!\[.*?\]\(.*?\)", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.DOTALL)
    text = re.sub(r"\$[^$]+\$", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("# "):
            title = line.lstrip("# ").strip()
            if title:
                return title
    return fallback


def read_sidecar_metadata(md_path: Path) -> dict[str, Any]:
    sidecar = md_path.parent / "metadata.json"
    if not sidecar.exists():
        return {}
    try:
        return json.loads(sidecar.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def parse_year_from_text(text: str) -> str | None:
    match = re.search(r"\b(19|20)\d{2}\b", text)
    return match.group(0) if match else None


def extract_arxiv_id(text: str) -> str | None:
    match = re.search(r"arXiv[:\s]+(\d{4}\.\d{4,5}(?:v\d+)?)", text, re.IGNORECASE)
    return match.group(1) if match else None


def extract_doi(text: str) -> str | None:
    match = re.search(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", text, re.IGNORECASE)
    return match.group(0).rstrip(".,)") if match else None


def markdown_blocks(text: str) -> list[dict[str, Any]]:
    """Parse markdown into sections with header paths."""
    lines = text.splitlines()
    stack: list[tuple[int, str]] = []
    blocks: list[dict[str, Any]] = []
    current_heading = "Document"
    current_level = 0
    current_path: list[str] = []
    current_lines: list[str] = []

    def flush() -> None:
        if not current_lines:
            return
        content = "\n".join(current_lines).strip()
        if content:
            blocks.append(
                {
                    "heading": current_heading,
                    "level": current_level,
                    "section_path": current_path.copy() if current_path else [current_heading],
                    "content": content,
                }
            )

    for line in lines:
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            flush()
            level = len(match.group(1))
            heading = match.group(2).strip()
            stack = [(lvl, text_) for lvl, text_ in stack if lvl < level]
            stack.append((level, heading))
            current_heading = heading
            current_level = level
            current_path = [text_ for _, text_ in stack]
            current_lines = []
        else:
            current_lines.append(line)
    flush()

    if not blocks:
        blocks.append({"heading": "Document", "level": 0, "section_path": ["Document"], "content": text})
    return blocks


def split_long_text(text: str, max_chars: int, overlap_chars: int) -> list[str]:
    paragraphs = re.split(r"\n\s*\n", text)
    chunks: list[str] = []
    current = ""
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if current and len(current) + len(para) > max_chars:
            chunks.append(current.strip())
            current = (current[-overlap_chars:] + "\n\n" + para) if overlap_chars else para
        else:
            current = f"{current}\n\n{para}" if current else para
    if current.strip():
        chunks.append(current.strip())
    return chunks


def build_nodes_for_markdown(md_path: Path, config: RagConfig) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    md_hash = sha256_file(md_path)
    raw = md_path.read_text(encoding="utf-8", errors="replace")
    paper_id = md_path.parent.name
    title = extract_title(raw, paper_id)
    sidecar = read_sidecar_metadata(md_path)

    nodes_cfg = config.raw.get("nodes", {})
    min_chars = int(nodes_cfg.get("min_chars", 120))
    max_chars = int(nodes_cfg.get("max_chars", 1800))
    overlap_chars = int(nodes_cfg.get("overlap_chars", 180))

    rel_source = md_path.relative_to(config.fulltext_dir).as_posix()
    source_file = repo_relative(md_path, config.vault_root)
    metadata_base = {
        "paper_id": paper_id,
        "title": title,
        "authors": sidecar.get("authors"),
        "year": sidecar.get("year") or parse_year_from_text(md_path.name),
        "doi": sidecar.get("doi") or extract_doi(raw[:4000]),
        "arxiv_id": sidecar.get("arxiv_id") or extract_arxiv_id(raw[:4000]),
        "source_file": source_file,
        "source_rel": rel_source,
        "pdf_path": sidecar.get("pdf_path"),
        "pdf_sha256": sidecar.get("pdf_sha256"),
        "citation_key": sidecar.get("citation_key"),
        "zotero_attachment_key": sidecar.get("zotero_attachment_key"),
        "zotero_parent_key": sidecar.get("zotero_parent_key"),
        "zotero_library_id": sidecar.get("zotero_library_id"),
        "md_sha256": md_hash,
    }

    nodes: list[dict[str, Any]] = []
    for block in markdown_blocks(raw):
        cleaned = clean_markdown_text(block["content"])
        if len(cleaned) < min_chars:
            continue
        pieces = [cleaned] if len(cleaned) <= max_chars else split_long_text(cleaned, max_chars, overlap_chars)
        for idx, piece in enumerate(pieces, 1):
            heading = block["heading"]
            section_path = block["section_path"]
            chunk_label = heading if len(pieces) == 1 else f"{heading} (part {idx})"
            text = f"[{title}] {' > '.join(section_path)}\n\n{piece}"
            node_id = sha256_bytes(f"{rel_source}\n{'/'.join(section_path)}\n{idx}\n{text}".encode("utf-8"))
            metadata = dict(metadata_base)
            metadata.update(
                {
                    "node_id": node_id,
                    "heading": heading,
                    "section_path": section_path,
                    "section_path_text": " > ".join(section_path),
                    "chunk_label": chunk_label,
                    "chunk_index": idx,
                }
            )
            nodes.append({"id": node_id, "text": text, "metadata": metadata})

    doc = {
        "paper_id": paper_id,
        "title": title,
        "source_file": source_file,
        "source_rel": rel_source,
        "md_sha256": md_hash,
        "node_count": len(nodes),
        "updated_at": utc_now(),
    }
    return doc, nodes


def find_markdown_files(fulltext_dir: Path) -> list[Path]:
    if not fulltext_dir.exists():
        return []
    files: list[Path] = []
    for md in fulltext_dir.rglob("*.md"):
        rel_parts = md.relative_to(fulltext_dir).parts
        if "images" in rel_parts or any(part.startswith("_") for part in rel_parts):
            continue
        files.append(md)
    return sorted(files, key=lambda p: str(p).lower())


def build_nodes(config: RagConfig, force: bool = False, dry_run: bool = False) -> int:
    ensure_runtime_dirs(config)
    old_manifest = read_json(config.node_manifest_path, {"version": NODE_MANIFEST_VERSION, "documents": {}})
    old_docs = old_manifest.get("documents", {})
    old_nodes = iter_jsonl(config.nodes_path)
    md_files = find_markdown_files(config.fulltext_dir)

    new_docs: dict[str, dict[str, Any]] = {}
    new_nodes: list[dict[str, Any]] = []
    unchanged_sources: set[str] = set()
    changed_sources: set[str] = set()

    print(f"Found {len(md_files)} markdown files")
    for md_path in md_files:
        rel = md_path.relative_to(config.fulltext_dir).as_posix()
        current_hash = sha256_file(md_path)
        if not force and rel in old_docs and old_docs[rel].get("md_sha256") == current_hash:
            unchanged_sources.add(rel)
            new_docs[rel] = old_docs[rel]
            continue
        doc, nodes = build_nodes_for_markdown(md_path, config)
        changed_sources.add(rel)
        new_docs[rel] = doc
        new_nodes.extend(nodes)

    kept_nodes = [
        node for node in old_nodes
        if node.get("metadata", {}).get("source_rel") in unchanged_sources and not force
    ]
    all_nodes = kept_nodes + new_nodes
    deduped = {node["id"]: node for node in all_nodes}
    all_nodes = list(deduped.values())

    print(f"Changed documents: {len(changed_sources)}")
    print(f"Total nodes: {len(all_nodes)}")
    if dry_run:
        return 0

    write_jsonl(config.nodes_path, all_nodes)
    write_json(
        config.node_manifest_path,
        {
            "version": NODE_MANIFEST_VERSION,
            "documents": new_docs,
            "updated_at": utc_now(),
        },
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build retrieval nodes from MinerU markdown.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = load_config(args.config)
    return build_nodes(config, force=args.force, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
