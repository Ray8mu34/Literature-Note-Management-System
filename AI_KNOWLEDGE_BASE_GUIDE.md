# AI Knowledge Base Guide

This repository is a local literature knowledge base. It is designed for external AI agents to query evidence first, then answer from that evidence.

## Directory Layout

```text
D:/Users/Learning/CV/
  Obsidian Vault/
    60_AI_Context/
      fulltext_md/        # MinerU-converted paper Markdown and images
      rag_nodes/          # retrieval nodes.jsonl and manifest
      manifests/          # PDF conversion manifest
    95_Scripts/           # conversion, indexing, query scripts
  rag_runtime/
    qdrant_storage/       # local Qdrant database state
    cache/                # embedding/model/cache files
    logs/
    snapshots/
```

Do not treat `rag_runtime/` as note content. It is database/runtime state.

## Primary Agent Workflow

Use the local retrieval script to get evidence chunks:

```powershell
D:\Env\Conda\envs\mineru_env\python.exe "Obsidian Vault\95_Scripts\query.py" --config "Obsidian Vault\95_Scripts\config.yaml" --query "YOUR QUESTION" --top-k 8
```

Then answer using only the returned evidence. Each result includes:

- `score`
- `title`
- `source_file`
- `section_path`
- `heading`
- `snippet`

When answering, cite sources using the returned result numbers and include the paper/source context. If the retrieved evidence is insufficient, say:

```text
当前语料没有足够证据
```

Do not invent citations or rely on unstated paper content.

## Useful Query Filters

Filter by canonical paper id:

```powershell
D:\Env\Conda\envs\mineru_env\python.exe "Obsidian Vault\95_Scripts\query.py" --config "Obsidian Vault\95_Scripts\config.yaml" --query "method" --paper-id "loweDistinctiveImageFeatures2004"
```

Filter by section path:

```powershell
D:\Env\Conda\envs\mineru_env\python.exe "Obsidian Vault\95_Scripts\query.py" --config "Obsidian Vault\95_Scripts\config.yaml" --query "ablation" --section-contains "Experiments"
```

Filter by title substring:

```powershell
D:\Env\Conda\envs\mineru_env\python.exe "Obsidian Vault\95_Scripts\query.py" --config "Obsidian Vault\95_Scripts\config.yaml" --query "object detection" --title-contains "YOLO"
```

## Important Policy For Agents

- Prefer calling `query.py` instead of reading all Markdown files directly.
- The query script is retrieval-only by default. Do not pass `--answer` unless explicitly asked.
- Do not write API keys into this repository.
- Do not modify or delete `rag_runtime/` unless explicitly asked to rebuild or repair the index.
- Do not rebuild Qdrant unless Markdown content or node files changed.
- Do not rename `fulltext_md` paper folders casually. They should use Better BibTeX citekeys as canonical `paper_id`.

## Updating The Knowledge Base

Convert new Zotero PDFs to Markdown:

```powershell
D:\Env\Conda\envs\mineru_env\python.exe "Obsidian Vault\95_Scripts\convert_pdf_to_md.py" --input C:\Users\30674\Zotero\storage --output "Obsidian Vault\60_AI_Context\fulltext_md"
```

Build retrieval nodes:

```powershell
D:\Env\Conda\envs\mineru_env\python.exe "Obsidian Vault\95_Scripts\build_nodes.py" --config "Obsidian Vault\95_Scripts\config.yaml"
```

Index into Qdrant:

```powershell
D:\Env\Conda\envs\mineru_env\python.exe "Obsidian Vault\95_Scripts\index_qdrant.py" --config "Obsidian Vault\95_Scripts\config.yaml"
```

The scripts are incremental:

- unchanged PDFs are skipped by hash;
- unchanged Markdown files are not re-chunked;
- unchanged nodes are not re-embedded;
- changed papers update only their own Qdrant points.

## Paper IDs

Canonical `paper_id` should be the Better BibTeX citekey, for example:

```text
loweDistinctiveImageFeatures2004
redmonYouOnlyLook2016
```

The converter resolves this by:

```text
Zotero/storage/<attachment item key>/paper.pdf
  -> read zotero.sqlite parent item key
  -> call Better BibTeX JSON-RPC
  -> use citation key as paper_id
```

If Better BibTeX is unavailable, the converter falls back to a safe PDF filename. Prefer fixing citekey resolution and migrating later rather than building long-term notes around fallback names.

## LLM/API Layer

This repository intentionally does not depend on an embedded answer API. Platform agents are expected to:

1. call `query.py`;
2. inspect returned chunks;
3. produce a grounded answer with citations.

This keeps secrets out of the vault and avoids maintaining a weaker duplicate answer layer.
