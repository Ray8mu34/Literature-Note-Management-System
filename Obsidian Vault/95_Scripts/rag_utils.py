#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared helpers for the AI Context RAG scripts."""

from __future__ import annotations

import dataclasses
import hashlib
import json
import math
import os
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parent
DEFAULT_CONFIG = SCRIPT_DIR / "config.yaml"


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise SystemExit("Missing dependency: PyYAML. Install requirements.txt in your RAG environment.") from exc
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def resolve_path(value: str | Path, base_dir: Path = VAULT_ROOT) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return (base_dir / path).resolve()


@dataclasses.dataclass(frozen=True)
class RagConfig:
    raw: dict[str, Any]
    config_path: Path
    vault_root: Path
    fulltext_dir: Path
    nodes_dir: Path
    nodes_path: Path
    node_manifest_path: Path
    runtime_dir: Path
    qdrant_storage: Path
    cache_dir: Path
    logs_dir: Path
    snapshots_dir: Path
    collection: str
    dense_model: str
    dense_vector_name: str
    sparse_vector_name: str
    reranker_model: str
    reranker_enabled: bool
    llm_enabled: bool
    llm_provider: str
    llm_model: str
    llm_base_url: str | None


def load_config(config_path: str | Path = DEFAULT_CONFIG) -> RagConfig:
    config_path = Path(config_path).resolve()
    raw = load_yaml(config_path)
    env_file = raw.get("env_file", ".env")
    load_dotenv(resolve_path(env_file, config_path.parent))

    paths = raw.get("paths", {})
    vault_root = resolve_path(paths.get("vault_root", ".."), config_path.parent)
    fulltext_dir = resolve_path(paths.get("fulltext_dir", "60_AI_Context/fulltext_md"), vault_root)
    nodes_dir = resolve_path(paths.get("nodes_dir", "60_AI_Context/rag_nodes"), vault_root)
    runtime_dir = resolve_path(paths.get("runtime_dir", "../rag_runtime"), vault_root)

    qdrant = raw.get("qdrant", {})
    embedding = raw.get("embedding", {})
    reranker = raw.get("reranker", {})
    llm = raw.get("llm", {})

    return RagConfig(
        raw=raw,
        config_path=config_path,
        vault_root=vault_root,
        fulltext_dir=fulltext_dir,
        nodes_dir=nodes_dir,
        nodes_path=nodes_dir / "nodes.jsonl",
        node_manifest_path=nodes_dir / "manifest.json",
        runtime_dir=runtime_dir,
        qdrant_storage=resolve_path(paths.get("qdrant_storage", "qdrant_storage"), runtime_dir),
        cache_dir=resolve_path(paths.get("cache_dir", "cache"), runtime_dir),
        logs_dir=resolve_path(paths.get("logs_dir", "logs"), runtime_dir),
        snapshots_dir=resolve_path(paths.get("snapshots_dir", "snapshots"), runtime_dir),
        collection=qdrant.get("collection", "cv_papers"),
        dense_model=embedding.get("dense_model", "BAAI/bge-m3"),
        dense_vector_name=qdrant.get("dense_vector_name", "dense"),
        sparse_vector_name=qdrant.get("sparse_vector_name", "sparse"),
        reranker_model=reranker.get("model", "BAAI/bge-reranker-base"),
        reranker_enabled=bool(reranker.get("enabled", False)),
        llm_enabled=bool(llm.get("enabled", False)),
        llm_provider=llm.get("provider", "openai"),
        llm_model=llm.get("model", "gpt-4.1-mini"),
        llm_base_url=llm.get("base_url"),
    )


def ensure_runtime_dirs(config: RagConfig) -> None:
    for path in [config.nodes_dir, config.runtime_dir, config.qdrant_storage, config.cache_dir, config.logs_dir, config.snapshots_dir]:
        path.mkdir(parents=True, exist_ok=True)


def repo_relative(path: Path, vault_root: Path = VAULT_ROOT) -> str:
    try:
        return path.resolve().relative_to(vault_root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def iter_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_+\-]+|[\u4e00-\u9fff]", text.lower())


class BM25Index:
    def __init__(self, docs: list[dict[str, Any]], k1: float = 1.5, b: float = 0.75):
        self.docs = docs
        self.k1 = k1
        self.b = b
        self.doc_tokens = [tokenize(doc.get("text", "")) for doc in docs]
        self.doc_lens = [len(tokens) for tokens in self.doc_tokens]
        self.avgdl = sum(self.doc_lens) / max(len(self.doc_lens), 1)
        self.df: Counter[str] = Counter()
        self.tf: list[Counter[str]] = []
        for tokens in self.doc_tokens:
            counts = Counter(tokens)
            self.tf.append(counts)
            self.df.update(counts.keys())
        self.n = len(docs)

    def search(self, query: str, top_k: int) -> list[tuple[int, float]]:
        q_terms = tokenize(query)
        scores: dict[int, float] = defaultdict(float)
        for term in q_terms:
            df = self.df.get(term, 0)
            if df == 0:
                continue
            idf = math.log(1 + (self.n - df + 0.5) / (df + 0.5))
            for idx, counts in enumerate(self.tf):
                freq = counts.get(term, 0)
                if freq == 0:
                    continue
                denom = freq + self.k1 * (1 - self.b + self.b * self.doc_lens[idx] / max(self.avgdl, 1))
                scores[idx] += idf * freq * (self.k1 + 1) / denom
        return sorted(scores.items(), key=lambda item: item[1], reverse=True)[:top_k]


def normalize_scores(results: list[tuple[str, float]]) -> dict[str, float]:
    if not results:
        return {}
    values = [score for _, score in results]
    lo, hi = min(values), max(values)
    if hi == lo:
        return {key: 1.0 for key, _ in results}
    return {key: (score - lo) / (hi - lo) for key, score in results}


def merge_hybrid(
    dense: list[tuple[str, float]],
    sparse: list[tuple[str, float]],
    dense_weight: float,
    sparse_weight: float,
    top_k: int,
) -> list[tuple[str, float]]:
    dense_norm = normalize_scores(dense)
    sparse_norm = normalize_scores(sparse)
    keys = set(dense_norm) | set(sparse_norm)
    merged = [
        (key, dense_weight * dense_norm.get(key, 0.0) + sparse_weight * sparse_norm.get(key, 0.0))
        for key in keys
    ]
    return sorted(merged, key=lambda item: item[1], reverse=True)[:top_k]
