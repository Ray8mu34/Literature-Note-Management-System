# AI Context Automation Scripts

这套脚本把 Zotero PDF、MinerU Markdown、结构化检索节点、Qdrant dense retrieval、本地 BM25 keyword retrieval、hybrid retrieval 和可选 reranker 串成一条可重复运行的工作流。

默认设计是 retrieval-only：脚本只负责返回高质量证据 chunks，最终回答由外部 AI/agent 基于证据完成。这样不需要在 vault 里维护 API key，也避免重复实现平台已经优化过的回答层。

## 当前目录约定

当前项目根目录建议保持为：

```text
D:/Users/Learning/CV/
  Obsidian Vault/
    60_AI_Context/
    95_Scripts/
  rag_runtime/
    qdrant_storage/
    cache/
    logs/
    snapshots/
```

Obsidian vault 内只放人类可读、可复现、适合版本管理的内容：

```text
60_AI_Context/fulltext_md/
60_AI_Context/manifests/pdf_conversion_manifest.json
60_AI_Context/rag_nodes/nodes.jsonl
60_AI_Context/rag_nodes/manifest.json
95_Scripts/
```

Qdrant storage、embedding cache、logs、snapshots 默认放在 vault 外的 `../rag_runtime/`。

## Canonical Paper ID

现在脚本把 Better BibTeX citekey 作为唯一优先的 `paper_id`。

原因：

- 你的 Obsidian 文献笔记使用 `loweDistinctiveImageFeatures2004` 这类 Better BibTeX citekey 命名。
- Zotero 自动重命名 PDF 可能是 `Lowe 等 - 2004 - ...pdf`，和笔记名不一致。
- 如果 RAG 的 Markdown 文件夹也使用 PDF 文件名，后续检索来源、文献笔记链接、Zotero Integration 笔记会出现两套 ID。
- 使用 citekey 后，笔记、fulltext Markdown、nodes、Qdrant payload 都能共享同一个稳定 ID。

解析链路：

```text
Zotero/storage/ABCDEFGH/paper.pdf
  -> ABCDEFGH 是 attachment item key
  -> 只读 zotero.sqlite，找到 parent item key
  -> 调 Better BibTeX JSON-RPC item.citationkey
  -> 得到 citekey
  -> fulltext_md/<citekey>/<citekey>.md
```

默认接口：

```text
Zotero DB: C:/Users/30674/Zotero/zotero.sqlite
Better BibTeX JSON-RPC: http://localhost:23119/better-bibtex/json-rpc
```

使用前请确保 Zotero 已打开，Better BibTeX 插件已启用。

## 主要脚本

- `zotero_citekey_resolver.py`：从 Zotero storage PDF 解析 Better BibTeX citekey。
- `convert_pdf_to_md.py`：用户友好的 PDF 转 Markdown CLI。
- `mineru_pdf_converter.py`：扫描 Zotero storage、调用 MinerU、清理中间产物、写 manifest。
- `migrate_fulltext_to_citekeys.py`：把旧的 PDF 文件名文件夹迁移为 citekey 文件夹。
- `build_nodes.py`：从 Markdown 构建 header-aware retrieval nodes。
- `index_qdrant.py`：增量写入 Qdrant dense vectors。
- `query.py`：Qdrant dense + 本地 BM25 hybrid query，默认只返回证据 chunks。

## 安装依赖

建议先激活环境：

```powershell
conda activate mineru_env
pip install -r "Obsidian Vault\95_Scripts\requirements.txt"
```

Windows 上 `conda run` 在打印 OCR 文本时偶尔会触发 GBK 编码问题。更稳的方式是直接用环境里的 Python：

```powershell
D:\Env\Conda\envs\mineru_env\python.exe "Obsidian Vault\95_Scripts\query.py" --config "Obsidian Vault\95_Scripts\config.yaml" --query "What is YOLO?"
```

## 测试 Citekey 解析

先拿一个 Zotero storage 里的 PDF 测试：

```powershell
python "Obsidian Vault\95_Scripts\zotero_citekey_resolver.py" --pdf "C:\Users\30674\Zotero\storage\ABCDEFGH\paper.pdf"
```

如果成功，会输出：

```text
attachment_key: ABCDEFGH
parent_key: ...
library_id: ...
citation_key: loweDistinctiveImageFeatures2004
```

如果失败，通常是 Zotero 没打开、Better BibTeX 没启用、或者这个 PDF 不是标准 stored attachment。

## PDF 转 Markdown

Dry-run：

```powershell
python "Obsidian Vault\95_Scripts\convert_pdf_to_md.py" --input C:\Users\30674\Zotero\storage --output "Obsidian Vault\60_AI_Context\fulltext_md" --dry-run
```

正式转换：

```powershell
python "Obsidian Vault\95_Scripts\convert_pdf_to_md.py" --input C:\Users\30674\Zotero\storage --output "Obsidian Vault\60_AI_Context\fulltext_md"
```

默认行为：

- 优先使用 Better BibTeX citekey 命名文件夹和 Markdown。
- 如果 citekey 解析失败，回退到 PDF 文件名。
- PDF 用 `sha256` 去重，已转换且 hash 命中时跳过。
- MinerU 中间输出放到 `60_AI_Context/_mineru_tmp/`，成功后只保留 `md + images + metadata.json`。
- 如果同一个 citekey 目标文件夹已存在但 PDF hash 不同，脚本会追加短 hash，避免误覆盖。

如果你临时不想使用 citekey：

```powershell
python "Obsidian Vault\95_Scripts\convert_pdf_to_md.py" --no-citekey --dry-run
```

## 迁移旧 Fulltext 文件夹

已有的旧文件夹如果是 PDF 文件名，可以迁移成 citekey：

```powershell
python "Obsidian Vault\95_Scripts\migrate_fulltext_to_citekeys.py" --dry-run
```

确认无冲突后正式迁移，建议带备份：

```powershell
python "Obsidian Vault\95_Scripts\migrate_fulltext_to_citekeys.py" --backup "Obsidian Vault\60_AI_Context\fulltext_md_backup_before_citekey_migration"
```

迁移会做这些事：

- 重命名 `fulltext_md/<old_id>/` 为 `fulltext_md/<citekey>/`。
- 重命名 `<old_id>.md` 为 `<citekey>.md`。
- 更新 `metadata.json` 中的 `paper_id`、`citation_key`、Zotero item keys、路径。
- 更新 `pdf_conversion_manifest.json`。

迁移后请重建 nodes 和 Qdrant index：

```powershell
python "Obsidian Vault\95_Scripts\build_nodes.py" --config "Obsidian Vault\95_Scripts\config.yaml"
python "Obsidian Vault\95_Scripts\index_qdrant.py" --config "Obsidian Vault\95_Scripts\config.yaml"
```

## 构建 Nodes

```powershell
python "Obsidian Vault\95_Scripts\build_nodes.py" --config "Obsidian Vault\95_Scripts\config.yaml"
```

输出：

```text
Obsidian Vault/60_AI_Context/rag_nodes/nodes.jsonl
Obsidian Vault/60_AI_Context/rag_nodes/manifest.json
```

每个 node 保留：

- `paper_id`
- `title`
- `authors`
- `year`
- `doi`
- `arxiv_id`
- `section_path`
- `section_path_text`
- `heading`
- `source_file`
- `pdf_path`
- `md_sha256`
- `citation_key`
- `zotero_attachment_key`
- `zotero_parent_key`

增量逻辑：

- 每个 Markdown 计算 bytes hash。
- 文件未变化时不重复清洗、不重复切块。
- 文件变化时只重建对应 paper 的 nodes。

## 写入 Qdrant

```powershell
python "Obsidian Vault\95_Scripts\index_qdrant.py" --config "Obsidian Vault\95_Scripts\config.yaml"
```

增量逻辑：

- 根据 node manifest 判断哪些 paper 变化。
- 文件未变化时不重复 embedding。
- 文件变化时删除对应 `paper_id` 的旧 Qdrant points，再写入新 points。
- 如果没有变化，会跳过 embedding 和 Qdrant 写入。

默认 dense model 是 `BAAI/bge-m3`。它质量较好，但首次下载约 GB 级，冷启动也较慢。只是调试链路时，可以临时换成更小的 sentence-transformers 模型。

## 查询

```powershell
python "Obsidian Vault\95_Scripts\query.py" --config "Obsidian Vault\95_Scripts\config.yaml" --query "What problem does SIFT solve?" --top-k 8
```

可加 metadata filter：

```powershell
python "Obsidian Vault\95_Scripts\query.py" --config "Obsidian Vault\95_Scripts\config.yaml" --query "What is the method?" --paper-id "loweDistinctiveImageFeatures2004"
python "Obsidian Vault\95_Scripts\query.py" --config "Obsidian Vault\95_Scripts\config.yaml" --query "ablation" --section-contains "Experiments"
python "Obsidian Vault\95_Scripts\query.py" --config "Obsidian Vault\95_Scripts\config.yaml" --query "dataset" --title-contains "SIFT"
```

每个 chunk 会显示：

- score
- paper title
- source_file
- section_path
- heading
- text snippet

检索策略：

- Dense semantic retrieval：Qdrant + `BAAI/bge-m3`
- Sparse / keyword retrieval：本地 BM25
- Hybrid retrieval：dense 和 BM25 分数归一化后加权合并
- Reranking：可选，配置 `reranker.enabled: true`
- Answer layer：默认不启用。推荐由外部 AI/agent 读取检索结果后回答。

如果你确实要测试本地回答层，必须显式传 `--answer`，否则即使配置里有 LLM 参数也不会自动调用 API：

```powershell
python "Obsidian Vault\95_Scripts\query.py" --config "Obsidian Vault\95_Scripts\config.yaml" --query "What problem does SIFT solve?" --answer
```

回答层只允许基于检索证据回答，并要求用 `[1]`、`[2]` 形式引用来源。如果证据不足，应输出“当前语料没有足够证据”。

## 为什么暂时没有使用 LlamaIndex

LlamaIndex 的 `MarkdownNodeParser`、Qdrant integration、query engine 都很有价值，但当前基础版本暂时没有直接使用它，主要是工程取舍：

- 首要目标是先把 Windows + Zotero + MinerU + Better BibTeX + Qdrant + 增量更新这条链路跑稳。
- 我们需要完全控制 `paper_id`、`source_file`、`section_path`、`md_sha256`、Qdrant point 删除和更新逻辑。
- LlamaIndex 的版本、Qdrant adapter、hybrid search 参数和 embedding/reranker 组合会引入额外耦合，初期排错成本更高。
- 目前本地 Markdown header parser 已经能保留论文结构路径，足够支撑基础论文检索。

不用 LlamaIndex 的不方便：

- 对复杂 Markdown 的处理不如成熟 parser，例如表格、代码块、脚注、跨 section 内容。
- 没有 LlamaIndex 内置的 node relationship、parent-child retrieval、auto-merging retrieval。
- 没有直接使用 LlamaIndex QueryEngine、ResponseSynthesizer、postprocessor、evaluation 工具。
- Qdrant sparse vectors / hybrid search 目前用本地 BM25 fallback，而不是 LlamaIndex + Qdrant 的完整 hybrid integration。
- 后续如果要做多跳检索、层级检索、citation-aware synthesis，自己维护会更费工。

未来扩展建议：

- 第一阶段：只把 `build_nodes.py` 的 Markdown 解析部分替换为 LlamaIndex `MarkdownNodeParser`，继续沿用现有 metadata schema 和 Qdrant 写入逻辑。
- 第二阶段：增加 `nodes.parser: llamaindex_markdown` 配置，让本地 parser 和 LlamaIndex parser 可切换。
- 第三阶段：如果依赖稳定，再迁移到 LlamaIndex + Qdrant hybrid search，或者保留直接 `qdrant_client` 写入、只用 LlamaIndex 做 query/rerank/synthesis。
- 第四阶段：加入 parent-child retrieval、section-level filtering、reranker evaluation、answer citation checker。

换句话说，现在不是否定 LlamaIndex，而是先把可控、可调试、可增量更新的底座搭稳；后续再把 LlamaIndex 作为 parser/query layer 增强，而不是一开始让它接管整个 pipeline。

## 安全注意

- 不要提交 `.env`。
- 不要把 `rag_runtime/` 放进 Obsidian vault。
- 不要提交 Qdrant storage、embedding cache、logs、snapshots。
- 删除或重建 Qdrant collection 前先 dry-run 或备份确认。
