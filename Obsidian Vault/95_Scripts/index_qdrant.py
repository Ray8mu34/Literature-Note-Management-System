#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Index retrieval nodes into a local Qdrant collection."""

from __future__ import annotations

import argparse
import uuid
from pathlib import Path
from typing import Any

from rag_utils import DEFAULT_CONFIG, RagConfig, ensure_runtime_dirs, iter_jsonl, load_config, read_json, write_json


INDEX_MANIFEST_NAME = "qdrant_index_manifest.json"


def load_deps():
    try:
        import numpy as np  # type: ignore
        from qdrant_client import QdrantClient  # type: ignore
        from qdrant_client.http import models  # type: ignore
        from sentence_transformers import SentenceTransformer  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "Missing indexing dependencies. Install 95_Scripts/requirements.txt in the RAG environment."
        ) from exc
    return np, QdrantClient, models, SentenceTransformer


def point_id_for(node_id: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, node_id))


def get_collection_names(client: Any) -> set[str]:
    return {collection.name for collection in client.get_collections().collections}


def ensure_collection(client: Any, models: Any, collection: str, vector_name: str, dim: int, recreate: bool) -> None:
    exists = collection in get_collection_names(client)
    if exists and recreate:
        client.delete_collection(collection)
        exists = False
    if exists:
        return
    client.create_collection(
        collection_name=collection,
        vectors_config={
            vector_name: models.VectorParams(size=dim, distance=models.Distance.COSINE)
        },
    )


def close_client(client: Any) -> None:
    close = getattr(client, "close", None)
    if callable(close):
        close()


def delete_paper_points(client: Any, models: Any, collection: str, paper_ids: set[str]) -> None:
    for paper_id in sorted(paper_ids):
        client.delete(
            collection_name=collection,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="paper_id",
                            match=models.MatchValue(value=paper_id),
                        )
                    ]
                )
            ),
            wait=True,
        )


def payload_for_node(node: dict[str, Any]) -> dict[str, Any]:
    metadata = dict(node["metadata"])
    metadata["text"] = node["text"]
    return metadata


def index_nodes(config: RagConfig, force: bool = False, dry_run: bool = False) -> int:
    ensure_runtime_dirs(config)
    nodes = iter_jsonl(config.nodes_path)
    if not nodes:
        print(f"No nodes found: {config.nodes_path}")
        return 1

    manifest_path = config.cache_dir / INDEX_MANIFEST_NAME
    old_manifest = read_json(manifest_path, {"nodes": {}, "papers": {}})
    old_nodes = old_manifest.get("nodes", {})
    old_papers = old_manifest.get("papers", {})

    changed_nodes = [
        node for node in nodes
        if force or old_nodes.get(node["id"]) != node["metadata"].get("md_sha256")
    ]
    changed_papers = {node["metadata"]["paper_id"] for node in changed_nodes}
    current_papers = {node["metadata"]["paper_id"] for node in nodes}
    removed_papers = set(old_papers) - current_papers

    print(f"Nodes: {len(nodes)}")
    print(f"Changed nodes: {len(changed_nodes)}")
    print(f"Changed papers: {len(changed_papers)}")
    print(f"Removed papers: {len(removed_papers)}")
    if dry_run:
        return 0
    if not force and not changed_papers and not removed_papers:
        print("No indexing changes; skipped embedding and Qdrant write.")
        return 0

    np, QdrantClient, models, SentenceTransformer = load_deps()

    model = SentenceTransformer(config.dense_model, cache_folder=str(config.cache_dir / "sentence_transformers"))
    sample_vec = model.encode(["dimension probe"], normalize_embeddings=True)
    dim = int(np.asarray(sample_vec).shape[1])

    client = QdrantClient(path=str(config.qdrant_storage))
    try:
        ensure_collection(
            client=client,
            models=models,
            collection=config.collection,
            vector_name=config.dense_vector_name,
            dim=dim,
            recreate=bool(config.raw.get("qdrant", {}).get("recreate_collection", False)),
        )

        if changed_papers or removed_papers:
            delete_paper_points(client, models, config.collection, changed_papers | removed_papers)

        nodes_to_upsert = [node for node in nodes if node["metadata"]["paper_id"] in changed_papers]
        batch_size = int(config.raw.get("embedding", {}).get("batch_size", 16))
        for start in range(0, len(nodes_to_upsert), batch_size):
            batch = nodes_to_upsert[start:start + batch_size]
            texts = [node["text"] for node in batch]
            vectors = model.encode(texts, normalize_embeddings=True)
            vectors = np.asarray(vectors, dtype="float32")
            points = [
                models.PointStruct(
                    id=point_id_for(node["id"]),
                    vector={config.dense_vector_name: vector.tolist()},
                    payload=payload_for_node(node),
                )
                for node, vector in zip(batch, vectors)
            ]
            client.upsert(collection_name=config.collection, points=points, wait=True)
            print(f"Upserted {min(start + batch_size, len(nodes_to_upsert))}/{len(nodes_to_upsert)}")
    finally:
        close_client(client)

    new_manifest = {
        "nodes": {node["id"]: node["metadata"].get("md_sha256") for node in nodes},
        "papers": {paper_id: True for paper_id in current_papers},
        "collection": config.collection,
        "dense_model": config.dense_model,
        "dense_vector_name": config.dense_vector_name,
    }
    write_json(manifest_path, new_manifest)
    print(f"Indexed collection: {config.collection}")
    print(f"Qdrant storage: {config.qdrant_storage}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Index nodes into Qdrant.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = load_config(args.config)
    return index_nodes(config, force=args.force, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
