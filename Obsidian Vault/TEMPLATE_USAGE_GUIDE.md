# 模板使用说明

这个文件说明 `90_Templates/` 中哪些模板适合 Zotero Integration 半自动导入，哪些模板适合人工新建。原则是：凡是对应 Zotero 条目的模板，都尽量让插件自动填入元数据、摘要、参考文献和标注；凡是地图、方法、项目和维护类笔记，则由人工维护。

## Zotero Integration 半自动模板

这些模板用于从 Zotero 条目生成 Obsidian 文献笔记。它们包含 `{{citekey}}`、`{{title}}`、`{{authors}}`、`{{bibliography}}`、`{{abstractNote}}`、`annotations` 等 Zotero Integration 变量。

- `zotero-integration-import-template.md`：通用 Zotero 导入模板，适合普通论文的默认导入。
- `literature-note-L2.md`：泛读 / 筛选文献模板，适合快速判断是否保留。
- `literature-note-L3.md`：精读文献模板，适合理解方法、实验和可引用价值。
- `literature-note-L4.md`：核心文献模板，适合深读、复现、批判和 related work 写作。
- `book-note.md`：书籍、教材、长篇报告模板，适合 Zotero 中的 book 条目。
- `dataset-paper-note.md`：数据集或 benchmark 论文模板，适合从 Zotero 导入数据集论文。

使用建议：

1. 在 Zotero 中确保条目元数据完整，尤其是 title、authors、year、venue、DOI、URL。
2. 在 Obsidian 的 Zotero Integration 设置中，为不同文献类型选择对应模板。
3. 导入后手动维护 `domain`、`task`、`method_family`、`dataset`、`relevance`、`projects`、`question_maps`。
4. Zotero 自动导入的摘要和标注只能作为材料，最终判断仍然写在正文分析部分。


## 重复导入与覆盖保护

Zotero Integration 重新导入同一个条目时，可能会覆盖已有 Markdown 文件。为避免 Obsidian frontmatter 解析失败，模板的 YAML 区域保持纯净结构，不放 `{% persist %}`、`{% for %}`、`{% if %}` 这类控制结构。正文中的人工笔记区域使用 `{% persist "..." %}` 和 `{% endpersist %}` 做覆盖保护。

会随 Zotero 重导入刷新的区域：

- `citekey`
- `title`
- `year`
- `authors`
- `venue`
- `doi`
- `url`
- `zotero`
- `Bibliography`
- `Abstract`
- `Zotero annotations / excerpts`

会被 `persist` 保护的区域：

- 正文中的所有人工分析、批判、勾选项、复现记录、项目关联和个人判断

使用时需要注意：

1. 第一次导入后，可以放心在正文的 `persist` 区域内写笔记。
2. YAML 中的 `domain`、`task`、`method_family`、`dataset`、`status`、`reading_level`、`relevance`、`projects`、`question_maps` 需要手动维护。
3. 不建议对已经手动维护过 YAML 的同一篇笔记反复执行完整导入。
4. 如果需要更新 annotations，优先使用只更新正文 annotations 区域的方式，不要覆盖整篇笔记。
5. 如果你修改模板中的 `persist` 名称，旧笔记中对应区域可能无法被正确识别。
6. 不建议在自动导入区域写长期笔记，尤其是 `Abstract` 和 `Zotero annotations / excerpts` 下方。

## 人工模板

这些模板不对应单个 Zotero 条目，主要用于组织知识、推进研究问题和管理项目，适合在 Obsidian 中手动新建。

- `00-inbox-note.md`：临时记录、灵感、未整理材料。
- `literature-note.md`：通用手工文献模板，适合没有从 Zotero 导入的材料。
- `survey-note.md`：综述笔记模板；如果综述已在 Zotero 中，也可以改用通用导入模板后手工调整。
- `method-paper-note.md`：方法论文的手工强化模板；如果要从 Zotero 导入，可先用 `literature-note-L3.md`。
- `field-map.md`：领域地图。
- `question-map.md`：问题地图。
- `method-note.md`：方法概念笔记。
- `dataset-note.md`：数据集 / benchmark 本体笔记。
- `dataset-index.md`：数据集总表。
- `candidate-topic.md`：候选选题。
- `project-overview.md`：项目总览。
- `project-00-problem.md`：项目问题定义。
- `project-01-related-work.md`：项目相关工作。
- `project-02-baselines.md`：项目 baseline 管理。
- `project-03-datasets.md`：项目数据集管理。
- `project-04-experiments.md`：项目实验记录。
- `project-05-results.md`：项目结果整理。
- `project-06-writing.md`：项目写作草稿。
- `project-reviewer-attacks.md`：审稿风险与防御。
- `ai-context-pack.md`：给 AI 的上下文包。
- `ai-paper-review-prompt.md`：AI 论文阅读提示词。
- `ai-literature-comparison-prompt.md`：AI 多文献对比提示词。
- `controlled-vocabulary.md`：YAML 受控词表。
- `dataview-literature-dashboard.md`：文献数据库面板模板。

## 判断规则

- 如果笔记对应 Zotero 中的一条文献对象，优先使用 Zotero Integration 半自动模板。
- 如果笔记是在组织多个文献、多个方法或一个研究问题，使用人工模板。
- 如果一篇文献只是临时材料，还没有进入 Zotero，先放入 `00_Inbox/`。
- 如果 AI 输出需要进入系统，先放入 `60_AI_Context/`，人工核查后再整理到正式笔记。

## 推荐工作流

1. 文献先进入 Zotero。
2. 在 Zotero 中补齐元数据、citekey、PDF 和标注。
3. 通过 Zotero Integration 导入到 `10_Literature/`。
4. 用 L2、L3、L4 模板决定阅读深度。
5. 从多篇文献中抽象出 `question-map`、`method-note`、`dataset-note`。
6. 当问题成熟后，再进入 `candidate-topic` 或 `50_Projects/`。
