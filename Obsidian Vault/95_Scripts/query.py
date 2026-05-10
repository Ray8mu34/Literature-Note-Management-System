#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hybrid query over Qdrant dense retrieval plus local BM25.

By default this script is retrieval-only. It prints evidence chunks for an
external AI/agent to read and answer from. LLM calls are never started unless
the caller explicitly passes --answer.
"""

from __future__ import annotations

import argparse
import dataclasses
import os
import re
import sys
from pathlib import Path
from typing import Any

from rag_utils import (
    BM25Index,
    DEFAULT_CONFIG,
    RagConfig,
    iter_jsonl,
    load_config,
    merge_hybrid,
)


INSUFFICIENT_EVIDENCE = "当前语料没有足够证据"


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


@dataclasses.dataclass(frozen=True)
class MetadataFilters:
    paper_id: str | None = None
    source_file: str | None = None
    title_contains: str | None = None
    section_contains: str | None = None

    @property
    def active(self) -> bool:
        return any(dataclasses.astuple(self))


def load_dense_deps():
    try:
        import numpy as np  # type: ignore
        from qdrant_client import QdrantClient  # type: ignore
        from qdrant_client.http import models  # type: ignore
        from sentence_transformers import SentenceTransformer  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "Missing query dependencies. Install 95_Scripts/requirements.txt in the RAG environment."
        ) from exc
    return np, QdrantClient, models, SentenceTransformer


def contains_text(value: Any, needle: str | None) -> bool:
    if not needle:
        return True
    if isinstance(value, list):
        haystack = " > ".join(str(item) for item in value)
    else:
        haystack = str(value or "")
    return needle.lower() in haystack.lower()


def payload_matches(payload: dict[str, Any], filters: MetadataFilters) -> bool:
    if filters.paper_id and payload.get("paper_id") != filters.paper_id:
        return False
    if filters.source_file and payload.get("source_file") != filters.source_file:
        return False
    if not contains_text(payload.get("title"), filters.title_contains):
        return False
    section_value = payload.get("section_path_text") or payload.get("section_path")
    if not contains_text(section_value, filters.section_contains):
        return False
    return True


def build_qdrant_filter(models: Any, filters: MetadataFilters) -> Any | None:
    must = []
    if filters.paper_id:
        must.append(models.FieldCondition(key="paper_id", match=models.MatchValue(value=filters.paper_id)))
    if filters.source_file:
        must.append(models.FieldCondition(key="source_file", match=models.MatchValue(value=filters.source_file)))
    return models.Filter(must=must) if must else None


def close_client(client: Any) -> None:
    close = getattr(client, "close", None)
    if callable(close):
        close()


def dense_search(
    config: RagConfig,
    question: str,
    top_k: int,
    filters: MetadataFilters,
) -> list[dict[str, Any]]:
    np, QdrantClient, models, SentenceTransformer = load_dense_deps()
    model = SentenceTransformer(config.dense_model, cache_folder=str(config.cache_dir / "sentence_transformers"))
    q_vec = model.encode([question], normalize_embeddings=True)
    q_vec = np.asarray(q_vec, dtype="float32")[0].tolist()
    client = QdrantClient(path=str(config.qdrant_storage))
    qdrant_filter = build_qdrant_filter(models, filters)
    limit = max(top_k, top_k * 5 if filters.active else top_k)

    try:
        try:
            if hasattr(client, "query_points"):
                response = client.query_points(
                    collection_name=config.collection,
                    query=q_vec,
                    using=config.dense_vector_name,
                    query_filter=qdrant_filter,
                    limit=limit,
                    with_payload=True,
                )
                hits = getattr(response, "points", response)
            else:
                hits = client.search(
                    collection_name=config.collection,
                    query_vector=(config.dense_vector_name, q_vec),
                    query_filter=qdrant_filter,
                    limit=limit,
                    with_payload=True,
                )
        except Exception as exc:  # noqa: BLE001 - provide BM25 fallback.
            print(f"Dense search unavailable: {exc}")
            return []

        results: list[dict[str, Any]] = []
        for hit in hits:
            payload = hit.payload or {}
            node_id = payload.get("node_id")
            if not node_id or not payload_matches(payload, filters):
                continue
            results.append({"node_id": node_id, "score": float(hit.score), "payload": payload})
            if len(results) >= top_k:
                break
        return results
    finally:
        close_client(client)


def bm25_search(
    nodes: list[dict[str, Any]],
    question: str,
    top_k: int,
    filters: MetadataFilters,
) -> list[dict[str, Any]]:
    filtered_nodes: list[dict[str, Any]] = []
    for node in nodes:
        metadata = dict(node.get("metadata", {}))
        metadata["text"] = node.get("text", "")
        if payload_matches(metadata, filters):
            filtered_nodes.append(node)

    index = BM25Index(filtered_nodes)
    results: list[dict[str, Any]] = []
    for node_index, score in index.search(question, top_k):
        node = filtered_nodes[node_index]
        metadata = dict(node.get("metadata", {}))
        metadata["text"] = node.get("text", "")
        results.append({"node_id": node["id"], "score": float(score), "payload": metadata})
    return results


def by_node_id(results: list[dict[str, Any]]) -> list[tuple[str, float]]:
    return [(result["node_id"], result["score"]) for result in results]


def merge_payloads(*groups: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    payloads: dict[str, dict[str, Any]] = {}
    for group in groups:
        for result in group:
            payloads[result["node_id"]] = result["payload"]
    return payloads


def rerank_if_enabled(config: RagConfig, question: str, results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not config.reranker_enabled or not results:
        return results
    try:
        from sentence_transformers import CrossEncoder  # type: ignore
    except ImportError:
        print("Reranker unavailable: sentence-transformers CrossEncoder not installed.")
        return results
    model = CrossEncoder(config.reranker_model, max_length=512)
    pairs = [(question, result["payload"].get("text", "")) for result in results]
    scores = model.predict(pairs)
    reranked = []
    for result, score in zip(results, scores):
        updated = dict(result)
        updated["rerank_score"] = float(score)
        reranked.append(updated)
    return sorted(reranked, key=lambda item: item["rerank_score"], reverse=True)


def snippet(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


def format_result(index: int, result: dict[str, Any], snippet_chars: int) -> str:
    payload = result["payload"]
    section_path = payload.get("section_path_text")
    if not section_path and isinstance(payload.get("section_path"), list):
        section_path = " > ".join(payload["section_path"])
    score_bits = [f"score={result['score']:.4f}"]
    if "rerank_score" in result:
        score_bits.append(f"rerank={result['rerank_score']:.4f}")
    return "\n".join(
        [
            f"[{index}] {'; '.join(score_bits)}",
            f"title: {payload.get('title', 'Unknown')}",
            f"source_file: {payload.get('source_file', payload.get('source_path', 'Unknown'))}",
            f"section_path: {section_path or 'Unknown'}",
            f"heading: {payload.get('heading', 'Unknown')}",
            f"snippet: {snippet(payload.get('text', ''), snippet_chars)}",
        ]
    )


def build_evidence(results: list[dict[str, Any]], snippet_chars: int) -> str:
    lines: list[str] = []
    for idx, result in enumerate(results, 1):
        payload = result["payload"]
        section_path = payload.get("section_path_text")
        if not section_path and isinstance(payload.get("section_path"), list):
            section_path = " > ".join(payload["section_path"])
        lines.append(
            "\n".join(
                [
                    f"[{idx}] {payload.get('title', 'Unknown')}",
                    f"source_file: {payload.get('source_file', payload.get('source_path', 'Unknown'))}",
                    f"section_path: {section_path or 'Unknown'}",
                    f"heading: {payload.get('heading', 'Unknown')}",
                    f"text: {snippet(payload.get('text', ''), snippet_chars)}",
                ]
            )
        )
    return "\n\n".join(lines)


def answer_with_llm(
    config: RagConfig,
    question: str,
    results: list[dict[str, Any]],
    force: bool = False,
) -> str | None:
    if not config.llm_enabled and not force:
        return None
    if not results:
        return INSUFFICIENT_EVIDENCE
    if config.llm_provider != "openai":
        return f"LLM provider not supported yet: {config.llm_provider}"
    try:
        from openai import OpenAI  # type: ignore
    except ImportError:
        return "OpenAI package is not installed; cannot generate answer."
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "OPENAI_API_KEY is not configured; cannot generate answer."
    base_url = config.llm_base_url or os.environ.get("OPENAI_BASE_URL") or None
    client = OpenAI(api_key=api_key, base_url=base_url)
    evidence = build_evidence(results, int(config.raw.get("retrieval", {}).get("snippet_chars", 700)))
    prompt = f"""You must answer only from the evidence below.
If the evidence is insufficient, say exactly: {INSUFFICIENT_EVIDENCE}
Every factual claim must cite sources using [1], [2], etc.

Question:
{question}

Evidence:
{evidence}
"""
    response = client.chat.completions.create(
        model=config.llm_model,
        messages=[
            {"role": "system", "content": "You are a careful research assistant. Do not invent citations."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""


def query(
    config: RagConfig,
    question: str,
    top_k: int | None = None,
    answer: bool = False,
    filters: MetadataFilters | None = None,
) -> int:
    nodes = iter_jsonl(config.nodes_path)
    if not nodes:
        print(f"No nodes found: {config.nodes_path}. Run build_nodes.py first.")
        return 1

    filters = filters or MetadataFilters()
    retrieval_cfg = config.raw.get("retrieval", {})
    dense_top_k = int(retrieval_cfg.get("dense_top_k", 30))
    sparse_top_k = int(retrieval_cfg.get("sparse_top_k", 30))
    final_top_k = top_k or int(retrieval_cfg.get("final_top_k", 8))
    dense_weight = float(retrieval_cfg.get("dense_weight", 0.65))
    sparse_weight = float(retrieval_cfg.get("sparse_weight", 0.35))
    snippet_chars = int(retrieval_cfg.get("snippet_chars", 700))

    dense = dense_search(config, question, dense_top_k, filters)
    sparse = bm25_search(nodes, question, sparse_top_k, filters)
    payloads = merge_payloads(dense, sparse)
    merged_scores = merge_hybrid(by_node_id(dense), by_node_id(sparse), dense_weight, sparse_weight, final_top_k * 2)
    merged = [
        {"node_id": node_id, "score": score, "payload": payloads[node_id]}
        for node_id, score in merged_scores
        if node_id in payloads
    ]
    merged = rerank_if_enabled(config, question, merged)[:final_top_k]

    if not merged:
        print(INSUFFICIENT_EVIDENCE)
        return 0

    for idx, result in enumerate(merged, 1):
        print(format_result(idx, result, snippet_chars))
        print()

    if answer:
        generated = answer_with_llm(config, question, merged, force=answer)
        if generated:
            print("Answer")
            print("=" * 72)
            print(generated)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Hybrid query over AI Context nodes.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--query", required=True)
    parser.add_argument("--top-k", type=int, default=None)
    parser.add_argument("--answer", action="store_true", help="Explicitly call the optional local LLM answer layer.")
    parser.add_argument("--paper-id", help="Exact paper_id filter.")
    parser.add_argument("--source-file", help="Exact source_file filter, e.g. 60_AI_Context/fulltext_md/foo/foo.md.")
    parser.add_argument("--title-contains", help="Case-insensitive title substring filter.")
    parser.add_argument("--section-contains", help="Case-insensitive section path substring filter.")
    return parser


def main() -> int:
    configure_stdio()
    args = build_parser().parse_args()
    config = load_config(args.config)
    filters = MetadataFilters(
        paper_id=args.paper_id,
        source_file=args.source_file,
        title_contains=args.title_contains,
        section_contains=args.section_contains,
    )
    return query(config, args.query, top_k=args.top_k, answer=args.answer, filters=filters)


if __name__ == "__main__":
    raise SystemExit(main())
