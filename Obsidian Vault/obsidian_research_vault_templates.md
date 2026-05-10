# Obsidian Research Vault 标准模板包

适用目录：

```text
Research Vault/
├── 00_Inbox/
├── 10_Literature/
├── 20_Field_Maps/
├── 21_Question_Maps/
├── 30_Methods/
├── 35_Datasets_Benchmarks/
├── 40_Candidate_Topics/
├── 50_Projects/
├── 60_AI_Context/
└── 90_Templates/
```

核心原则：

```text
Zotero：文献对象、PDF、元数据、标注、引用
Obsidian：理解、分类、问题、项目推进
YAML：稳定、可检索、可筛选的信息
正文：复杂理解、批判、推理、写作素材
Dataview / Bases：动态视图，不是主知识本体
```

---

# 0. 模板文件清单

建议在 `90_Templates/` 下维护：

```text
90_Templates/
├── 00-inbox-note.md
├── literature-note.md
├── literature-note-L2.md
├── literature-note-L3.md
├── literature-note-L4.md
├── survey-note.md
├── book-note.md
├── method-paper-note.md
├── dataset-paper-note.md
├── field-map.md
├── question-map.md
├── method-note.md
├── dataset-note.md
├── dataset-index.md
├── candidate-topic.md
├── project-overview.md
├── project-00-problem.md
├── project-01-related-work.md
├── project-02-baselines.md
├── project-03-datasets.md
├── project-04-experiments.md
├── project-05-results.md
├── project-06-writing.md
├── project-reviewer-attacks.md
├── ai-context-pack.md
├── ai-paper-review-prompt.md
├── ai-literature-comparison-prompt.md
├── controlled-vocabulary.md
└── dataview-literature-dashboard.md
```

---

# 1. `00-inbox-note.md`

用于 `00_Inbox/` 中的临时想法、会议摘录、未整理材料。

```markdown
---
type: inbox
subtype: note
status: inbox
source:
related_area: []
related_questions: []
related_projects: []
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# {{title}}

## 原始记录


## 这是什么？

- [ ] 文献
- [ ] 方法
- [ ] 数据集 / benchmark
- [ ] 研究问题
- [ ] 候选选题
- [ ] 项目任务
- [ ] AI 输出
- [ ] 其他

## 为什么值得保留？


## 应该移动到哪里？

- Target folder:
- Target note:

## 下一步

- [ ] 删除
- [ ] 移动到正式笔记
- [ ] 转成 question map
- [ ] 转成 candidate topic
- [ ] 加入 Zotero
- [ ] 需要进一步搜索文献
```

---

# 2. `literature-note.md`

通用文献笔记模板。适合从 Zotero 导入后再人工补充。

```markdown
---
type: literature
subtype: paper

citekey:
title:
year:
authors: []
venue:
doi:
url:
zotero:

# 知识分类：人工维护
domain: []
task: []
modality: []
method_family: []
dataset: []

# 阅读状态：人工维护
status: inbox
reading_level: L0
relevance: unknown

# 研究连接：人工维护
projects: []
field_maps: []
question_maps: []
related_methods: []
related_datasets: []

questions: []

created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# {{title}}

## TL;DR

一句话说明这篇论文做了什么，以及它为什么可能重要。

## Problem

这篇论文试图解决什么问题？

## Method

它的方法是什么？核心假设是什么？

## Experiments

- Datasets:
- Metrics:
- Baselines:
- Main results:

## Relevance to my research

它和我的研究方向有什么关系？

## Keep because

为什么值得保留？

## Limitations / concerns

这篇论文有什么局限、风险或不可信之处？

## Useful citations

可以在 related work / method / motivation 中引用的点：

-

## Connections

相关文献：
-

相关方法：
-

相关问题：
-

相关数据集：
-

## My thoughts

自己的想法、批判、可能延伸。

## Zotero annotations / excerpts

从 Zotero 导入的标注、摘录、页码放这里。
```

---

# 3. `literature-note-L2.md`

用于泛读、筛选文献。只写极简信息。

```markdown
---
type: literature
subtype: paper

citekey: "{{citekey}}"
title: "{{title}}"
year: "{{date | format('YYYY')}}"
authors: "{{authors}}"
venue: "{{publicationTitle}}"
doi: "{{DOI}}"
url: "{{url}}"
zotero: "{{select}}"

domain: []
task: []
modality: []
method_family: []
dataset: []

status: skimmed
reading_level: L2
relevance: unknown

projects: []
field_maps: []
question_maps: []

questions: []

created: "{{importDate | format('YYYY-MM-DD')}}"
updated: "{{importDate | format('YYYY-MM-DD')}}"
---

# {{title}}

## Bibliography

{{bibliography}}

## Abstract

{{abstractNote}}

## Quick screening

{% persist "quick-screening" %}

- Problem:
- Method:
- Relevance: strong / medium / weak
- Keep because:

{% endpersist %}

## Possible use

{% persist "possible-use" %}

- [ ] Related work
- [ ] Background
- [ ] Baseline
- [ ] Dataset / benchmark reference
- [ ] Method reference
- [ ] Not useful now, maybe later

{% endpersist %}

## Notes

{% persist "notes" %}

{% endpersist %}

## Zotero annotations / excerpts

{% for annotation in annotations %}
{% if annotation.annotatedText %}
> Page {{annotation.page}}: {{annotation.annotatedText}}
{% endif %}
{% if annotation.comment %}
>
> Comment: {{annotation.comment}}
{% endif %}

{% endfor %}
```

---

# 4. `literature-note-L3.md`

用于精读文献，目标是理解方法、实验和可引用价值。

```markdown
---
type: literature
subtype: paper

citekey: "{{citekey}}"
title: "{{title}}"
year: "{{date | format('YYYY')}}"
authors: "{{authors}}"
venue: "{{publicationTitle}}"
doi: "{{DOI}}"
url: "{{url}}"
zotero: "{{select}}"

domain: []
task: []
modality: []
method_family: []
dataset: []

status: read
reading_level: L3
relevance: unknown

projects: []
field_maps: []
question_maps: []
related_methods: []
related_datasets: []

questions: []

created: "{{importDate | format('YYYY-MM-DD')}}"
updated: "{{importDate | format('YYYY-MM-DD')}}"
---

# {{title}}

## Bibliography

{{bibliography}}

## Abstract

{{abstractNote}}

## 1. One-sentence summary

{% persist "one-sentence-summary" %}

{% endpersist %}

## 2. Research problem

{% persist "research-problem" %}

### 2.1 论文声称要解决什么问题？


### 2.2 这个问题为什么重要？


### 2.3 这个问题在我的研究中对应什么？

{% endpersist %}

## 3. Core method

{% persist "core-method" %}

### 3.1 方法结构


### 3.2 核心假设


### 3.3 关键技术点


### 3.4 和已有方法相比的差异

{% endpersist %}

## 4. Experiments

{% persist "experiments" %}

### 4.1 Datasets


### 4.2 Metrics


### 4.3 Baselines


### 4.4 Main results


### 4.5 Ablations


### 4.6 实验是否可信？

{% endpersist %}

## 5. What can I use?

{% persist "what-can-i-use" %}

### 5.1 Motivation 可用点


### 5.2 Related work 可用点


### 5.3 Method 可借鉴点


### 5.4 Experiment design 可借鉴点

{% endpersist %}

## 6. Limitations

{% persist "limitations" %}

{% endpersist %}

## 7. Questions after reading

{% persist "questions-after-reading" %}

-

{% endpersist %}

## 8. Connections

{% persist "connections" %}

### Related papers

-

### Related methods

-

### Related datasets

-

### Related question maps

-

{% endpersist %}

## 9. Zotero annotations / excerpts

{% for annotation in annotations %}
{% if annotation.annotatedText %}
> Page {{annotation.page}}: {{annotation.annotatedText}}
{% endif %}
{% if annotation.comment %}
>
> Comment: {{annotation.comment}}
{% endif %}

{% endfor %}
```

---

# 5. `literature-note-L4.md`

用于深读、复现、批判、写入 related work 的核心文献。

```markdown
---
type: literature
subtype: paper

citekey: "{{citekey}}"
title: "{{title}}"
year: "{{date | format('YYYY')}}"
authors: "{{authors}}"
venue: "{{publicationTitle}}"
doi: "{{DOI}}"
url: "{{url}}"
zotero: "{{select}}"

domain: []
task: []
modality: []
method_family: []
dataset: []

status: annotated
reading_level: L4
relevance: high

projects: []
field_maps: []
question_maps: []
related_methods: []
related_datasets: []

questions: []

replication_status: not_started
code_available: unknown
code_url:

created: "{{importDate | format('YYYY-MM-DD')}}"
updated: "{{importDate | format('YYYY-MM-DD')}}"
---

# {{title}}

## Bibliography

{{bibliography}}

## Abstract

{{abstractNote}}

## 1. Why this paper matters

{% persist "why-this-paper-matters" %}

这篇论文为什么是核心文献？它在领域中的位置是什么？

{% endpersist %}

## 2. Paper claim

{% persist "paper-claim" %}

作者最核心的 claim 是什么？

{% endpersist %}

## 3. Problem formulation

{% persist "problem-formulation" %}

### 3.1 Input / output


### 3.2 Task definition


### 3.3 Assumptions


### 3.4 What is excluded?

{% endpersist %}

## 4. Method reconstruction

{% persist "method-reconstruction" %}

### 4.1 Pipeline


### 4.2 Model architecture


### 4.3 Objective / loss


### 4.4 Training data


### 4.5 Inference procedure


### 4.6 Implementation details

{% endpersist %}

## 5. Experiment reconstruction

{% persist "experiment-reconstruction" %}

### 5.1 Datasets


### 5.2 Splits


### 5.3 Metrics


### 5.4 Baselines


### 5.5 Hyperparameters


### 5.6 Main table interpretation


### 5.7 Ablations


### 5.8 Error analysis

{% endpersist %}

## 6. Critical evaluation

{% persist "critical-evaluation" %}

### 6.1 What is convincing?


### 6.2 What is weak?


### 6.3 What might reviewers attack?


### 6.4 Hidden assumptions


### 6.5 Possible confounders

{% endpersist %}

## 7. Relation to my work

{% persist "relation-to-my-work" %}

### 7.1 我会如何引用它？


### 7.2 我的工作和它的区别是什么？


### 7.3 我的工作可以继承它什么？


### 7.4 我的工作可以批判它什么？

{% endpersist %}

## 8. Replication notes

{% persist "replication-notes" %}

### 8.1 Code


### 8.2 Data


### 8.3 Environment


### 8.4 Reproduction checklist

- [ ] 找到代码
- [ ] 找到数据
- [ ] 跑通 demo
- [ ] 复现主结果
- [ ] 复现关键消融
- [ ] 记录失败原因

{% endpersist %}

## 9. Related work paragraph draft

{% persist "related-work-paragraph-draft" %}

可以直接写进论文 related work 的草稿：

{% endpersist %}

## 10. Open questions

{% persist "open-questions" %}

-

{% endpersist %}

## 11. Zotero annotations / excerpts

{% for annotation in annotations %}
{% if annotation.annotatedText %}
> Page {{annotation.page}}: {{annotation.annotatedText}}
{% endif %}
{% if annotation.comment %}
>
> Comment: {{annotation.comment}}
{% endif %}

{% endfor %}
```

---

# 6. `survey-note.md`

用于综述文章。

```markdown
---
type: literature
subtype: survey

citekey:
title:
year:
authors: []
venue:
doi:
url:
zotero:

domain: []
task: []
method_family: []
dataset: []

status: skimmed
reading_level: L2
relevance: unknown

field_maps: []
question_maps: []
projects: []

created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# {{title}}

## Survey scope

这篇综述覆盖哪些问题、方法、任务、数据集？

## Taxonomy

作者如何划分领域？

### Category 1


### Category 2


### Category 3


## Important papers mentioned

-

## Useful tables / figures

-

## What this survey helps me understand


## What this survey misses


## Related field maps

-

## Related question maps

-

## Follow-up reading list

- [ ]
```

---

# 7. `book-note.md`

用于书、教材、长篇报告。

```markdown
---
type: literature
subtype: book

citekey: "{{citekey}}"
title: "{{title}}"
year: "{{date | format('YYYY')}}"
authors: "{{authors}}"
publisher: "{{publisher}}"
isbn: "{{ISBN}}"
url: "{{url}}"
zotero: "{{select}}"

domain: []
method_family: []

status: reading
reading_level: L2
relevance: unknown

projects: []
field_maps: []
question_maps: []

created: "{{importDate | format('YYYY-MM-DD')}}"
updated: "{{importDate | format('YYYY-MM-DD')}}"
---

# {{title}}

## Bibliography

{{bibliography}}

## Abstract / summary

{{abstractNote}}

## Why read this?

{% persist "why-read-this" %}

{% endpersist %}

## Core ideas

{% persist "core-ideas" %}

{% endpersist %}

## Chapter notes

{% persist "chapter-notes" %}

### Chapter 1


### Chapter 2


### Chapter 3

{% endpersist %}

## Concepts to extract

{% persist "concepts-to-extract" %}

-

{% endpersist %}

## Methods to extract

{% persist "methods-to-extract" %}

-

{% endpersist %}

## Useful quotes

{% persist "useful-quotes" %}

-

{% endpersist %}

## Relation to my research

{% persist "relation-to-my-research" %}

{% endpersist %}

## Zotero annotations / excerpts

{% for annotation in annotations %}
{% if annotation.annotatedText %}
> Page {{annotation.page}}: {{annotation.annotatedText}}
{% endif %}
{% if annotation.comment %}
>
> Comment: {{annotation.comment}}
{% endif %}

{% endfor %}
```

---

# 8. `method-paper-note.md`

用于重点记录一篇“方法论文”。

```markdown
---
type: literature
subtype: method_paper

citekey:
title:
year:
authors: []
venue:
doi:
url:
zotero:

domain: []
task: []
method_family: []
related_methods: []
dataset: []

status: read
reading_level: L3
relevance: unknown

projects: []
question_maps: []

created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# {{title}}

## Method in one sentence


## What problem does this method solve?


## Core mechanism


## Assumptions


## Where it works well


## Where it may fail


## Required data / supervision


## Computational cost


## Compared with previous methods


## Potential use in my research


## Should create / update method note?

- [ ] [[方法名]]

## Zotero annotations / excerpts


```

---

# 9. `dataset-paper-note.md`

用于提出数据集或 benchmark 的论文。

```markdown
---
type: literature
subtype: dataset_paper

citekey: "{{citekey}}"
title: "{{title}}"
year: "{{date | format('YYYY')}}"
authors: "{{authors}}"
venue: "{{publicationTitle}}"
doi: "{{DOI}}"
url: "{{url}}"
zotero: "{{select}}"

domain: []
task: []
modality: []
dataset: []

status: read
reading_level: L3
relevance: unknown

projects: []
question_maps: []
related_datasets: []

created: "{{importDate | format('YYYY-MM-DD')}}"
updated: "{{importDate | format('YYYY-MM-DD')}}"
---

# {{title}}

## Bibliography

{{bibliography}}

## Abstract

{{abstractNote}}

## Dataset / benchmark introduced

{% persist "dataset-benchmark-introduced" %}

{% endpersist %}

## Task

{% persist "task" %}

{% endpersist %}

## Data source

{% persist "data-source" %}

{% endpersist %}

## Annotation type

{% persist "annotation-type" %}

{% endpersist %}

## Scale

{% persist "scale" %}

- Number of images:
- Number of instances:
- Number of classes:
- Spatial resolution:
- Modality:

{% endpersist %}

## Splits

{% persist "splits" %}

{% endpersist %}

## Metrics

{% persist "metrics" %}

{% endpersist %}

## Baselines reported

{% persist "baselines-reported" %}

{% endpersist %}

## Biases / limitations

{% persist "biases-limitations" %}

{% endpersist %}

## What question does this benchmark actually answer?

{% persist "benchmark-answers" %}

{% endpersist %}

## What question does it fail to answer?

{% persist "benchmark-fails-to-answer" %}

{% endpersist %}

## Should create / update dataset note?

{% persist "should-create-update-dataset-note" %}

- [ ] [[数据集名]]

{% endpersist %}

## Zotero annotations / excerpts

{% for annotation in annotations %}
{% if annotation.annotatedText %}
> Page {{annotation.page}}: {{annotation.annotatedText}}
{% endif %}
{% if annotation.comment %}
>
> Comment: {{annotation.comment}}
{% endif %}

{% endfor %}
```

---

# 10. `field-map.md`

用于 `20_Field_Maps/`。

```markdown
---
type: field_map
field:
domain: []
status: active
related_methods: []
related_datasets: []
related_questions: []
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# {{title}}

## 我当前的理解

这个领域大概研究什么？核心对象是什么？为什么重要？

## 主要任务

### Task 1

- 代表问题：
- 相关方法：
- 相关数据集：
- 相关问题地图：

### Task 2

- 代表问题：
- 相关方法：
- 相关数据集：
- 相关问题地图：

## 主要方法族

- [[方法 A]]
- [[方法 B]]

## 重要数据集 / benchmark

- [[数据集 A]]
- [[数据集 B]]

## 代表性综述

-

## 核心文献

```dataview
TABLE citekey, year, status, reading_level, relevance, task, method_family
FROM "10_Literature"
WHERE type = "literature"
WHERE contains(domain, "在这里填写领域词")
SORT year DESC
```

## 我感兴趣的方向

-

## 当前不清楚的问题

-

## 下一步阅读

- [ ]
```

---

# 11. `question-map.md`

用于 `21_Question_Maps/`。

```markdown
---
type: question_map
question:
status: active
priority: medium

domain: []
task: []
method_family: []
dataset: []

related_field_maps: []
related_methods: []
related_datasets: []
related_projects: []

created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# {{title}}

## 这个问题是什么？

用自己的话定义问题。避免只写一个大领域名。

## 为什么重要？

这个问题对领域、方法、数据集、应用或我的研究有什么意义？

## 当前我看到的主要观点

### 观点 A：

支持文献：
- [[@paperA]] — 原因：
- [[@paperB]] — 原因：

### 观点 B：

支持文献：
- [[@paperC]] — 原因：

### 观点 C：

支持文献：
-

## 关键证据

-

## 关键反证 / 冲突

-

## 我的当前判断


## 可能的研究切入点

1.
2.
3.

## 相关文献表

```dataview
TABLE citekey, year, status, reading_level, relevance, method_family, dataset
FROM "10_Literature"
WHERE type = "literature"
WHERE contains(question_maps, this.file.name)
SORT year DESC
```

## 待读文献

- [ ]

## 下一步

- [ ]
```

---

# 12. `method-note.md`

用于 `30_Methods/`。

```markdown
---
type: method
method:
method_family: []
domain: []
task: []
status: active
related_questions: []
related_datasets: []
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# {{title}}

## 一句话理解


## 它解决什么问题？


## 核心假设


## 基本形式 / pipeline


## 常见变体

### Variant 1


### Variant 2


## 在普通 CV / NLP / ML 中怎么用？


## 迁移到我的领域时有什么变化？


## 优点

-

## 局限

-

## 相关文献

```dataview
TABLE citekey, year, status, reading_level, relevance, task, dataset
FROM "10_Literature"
WHERE type = "literature"
WHERE contains(method_family, "在这里填写方法词")
SORT year DESC
```

## 相关问题

-

## 我的问题

-
```

---

# 13. `dataset-note.md`

用于 `35_Datasets_Benchmarks/`。

```markdown
---
type: dataset
dataset:
benchmark: true

domain: []
task: []
modality: []
annotation_type: []
metrics: []

status: active
homepage:
paper:
license:

created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# {{title}}

## 基本信息

- Task:
- Data type:
- Modality:
- Annotation:
- Common metrics:
- Homepage:
- Paper:

## 数据规模

- Images:
- Instances:
- Classes:
- Spatial resolution:
- Geographic coverage:
- Temporal coverage:

## Splits


## Labels / classes


## 它适合回答什么问题？


## 它不适合回答什么问题？


## 常见使用方式


## 已知偏差 / 风险


## 相关问题

-

## 使用它的文献

```dataview
TABLE citekey, year, status, reading_level, relevance, method_family
FROM "10_Literature"
WHERE type = "literature"
WHERE contains(dataset, this.file.name) OR contains(dataset, "在这里填写数据集词")
SORT year DESC
```

## Notes


```

---

# 14. `dataset-index.md`

用于维护数据集总表，例如 `35_Datasets_Benchmarks/遥感数据集总表.md`。

```markdown
---
type: dataset_index
domain: []
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# {{title}}

## 数据集总表

```dataview
TABLE task, modality, annotation_type, metrics, status, homepage
FROM "35_Datasets_Benchmarks"
WHERE type = "dataset"
SORT file.name ASC
```

## 按任务分组

### Object detection

```dataview
TABLE modality, annotation_type, metrics, homepage
FROM "35_Datasets_Benchmarks"
WHERE type = "dataset"
WHERE contains(task, "object_detection")
SORT file.name ASC
```

### Semantic segmentation

```dataview
TABLE modality, annotation_type, metrics, homepage
FROM "35_Datasets_Benchmarks"
WHERE type = "dataset"
WHERE contains(task, "semantic_segmentation")
SORT file.name ASC
```

### Change detection

```dataview
TABLE modality, annotation_type, metrics, homepage
FROM "35_Datasets_Benchmarks"
WHERE type = "dataset"
WHERE contains(task, "change_detection")
SORT file.name ASC
```

## 我对 benchmark 的整体判断


```

---

# 15. `candidate-topic.md`

用于 `40_Candidate_Topics/`。

```markdown
---
type: candidate_topic
topic:
status: exploring
priority: medium

domain: []
task: []
method_family: []
dataset: []

related_questions: []
related_methods: []
related_datasets: []
related_literature: []

created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# {{title}}

## 研究问题

我想研究的具体问题是什么？

## 为什么重要？

这个问题为什么值得做？

## 当前已有文献

```dataview
TABLE citekey, year, status, reading_level, relevance, method_family, dataset
FROM "10_Literature"
WHERE type = "literature"
WHERE contains(projects, this.file.name) OR contains(question_maps, this.file.name)
SORT relevance DESC
```

手动补充：
- [[@paperA]] —
- [[@paperB]] —

## Gap

现有工作缺什么？

## 可能的创新点

1.
2.
3.

## 可用数据集

-

## 可能 baseline

-

## 可能方法


## 初步实验设计


## 风险

### 技术风险


### 数据风险


### 评价风险


### 投稿风险


## 最小可行验证

- [ ]

## 下一步

- [ ]
```

---

# 16. `project-overview.md`

用于 `50_Projects/<ProjectName>/README.md` 或 `overview.md`。

```markdown
---
type: project
project:
status: active
stage: problem_formulation
priority: high

domain: []
task: []
method_family: []
dataset: []

target_venue:
deadline:

created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# {{title}}

## Project in one sentence


## Research question


## Hypothesis


## Claimed contribution

1.
2.
3.

## Why now?


## Related notes

- [[00_problem]]
- [[01_related_work]]
- [[02_baselines]]
- [[03_datasets]]
- [[04_experiments]]
- [[05_results]]
- [[06_writing]]
- [[reviewer_attacks]]

## Current status


## Next actions

- [ ]
```

---

# 17. `project-00-problem.md`

```markdown
---
type: project_note
subtype: problem
project:
status: active
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# 00 Problem

## Problem statement


## Why this problem matters


## Who cares?


## Why existing solutions are insufficient


## Hypothesis


## Contribution claim draft

This paper shows that ...

## Scope

### In scope

-

### Out of scope

-

## Reviewer will ask

-
```

---

# 18. `project-01-related-work.md`

```markdown
---
type: project_note
subtype: related_work
project:
status: active
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# 01 Related Work

## Literature groups

### Group 1:

Core papers:
-

Claim:


Limitation:


### Group 2:

Core papers:
-

Claim:


Limitation:


### Group 3:

Core papers:
-

Claim:


Limitation:


## Project literature table

```dataview
TABLE citekey, year, reading_level, relevance, task, method_family, dataset
FROM "10_Literature"
WHERE type = "literature"
WHERE contains(projects, "在这里填写项目名")
SORT relevance DESC
```

## Related work paragraph draft


## How we differ


```

---

# 19. `project-02-baselines.md`

```markdown
---
type: project_note
subtype: baselines
project:
status: active
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# 02 Baselines

## Baseline selection criteria


## Required baselines

| Baseline | Paper | Code | Dataset support | Why included | Status |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Strong baselines


## Weak / optional baselines


## Baselines reviewers will expect


## Implementation notes


## Risks


```

---

# 20. `project-03-datasets.md`

```markdown
---
type: project_note
subtype: datasets
project:
status: active
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# 03 Datasets

## Dataset selection criteria


## Candidate datasets

| Dataset | Task | Modality | Metric | Pros | Cons | Status |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

## Final datasets


## Splits


## Metrics


## Preprocessing


## Dataset risks


```

---

# 21. `project-04-experiments.md`

```markdown
---
type: project_note
subtype: experiments
project:
status: active
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# 04 Experiments

## Main experiment

### Goal


### Setup


### Expected result


### What would falsify the hypothesis?


## Ablation studies

| Ablation | Purpose | Expected finding | Status |
|---|---|---|---|
|  |  |  |  |

## Sensitivity analysis


## Error analysis


## Experiment log

### {{date:YYYY-MM-DD}}

- Goal:
- Setup:
- Result:
- Interpretation:
- Next:

## Open issues

- [ ]
```

---

# 22. `project-05-results.md`

```markdown
---
type: project_note
subtype: results
project:
status: active
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# 05 Results

## Main result table

| Method | Dataset | Metric | Result | Notes |
|---|---|---|---|---|
|  |  |  |  |  |

## Key findings

1.
2.
3.

## Figures


## Interpretation


## Negative results


## What results support the claim?


## What results weaken the claim?


```

---

# 23. `project-06-writing.md`

```markdown
---
type: project_note
subtype: writing
project:
status: active
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# 06 Writing

## Title candidates

-

## Abstract draft


## Introduction outline

1. Broad problem:
2. Gap:
3. Our idea:
4. Contributions:

## Contributions

1.
2.
3.

## Method section outline


## Experiment section outline


## Related work draft


## Limitations


## Checklist

- [ ] Problem is clear
- [ ] Contributions are explicit
- [ ] Baselines are fair
- [ ] Datasets are justified
- [ ] Results support claims
- [ ] Limitations are acknowledged
```

---

# 24. `project-reviewer-attacks.md`

```markdown
---
type: project_note
subtype: reviewer_attacks
project:
status: active
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# Reviewer Attacks

## Attack 1: Novelty is weak

### Why reviewer might say this


### Evidence against this attack


### What to add to paper


## Attack 2: Baselines are insufficient

### Why reviewer might say this


### Evidence against this attack


### What to add to paper


## Attack 3: Dataset choice is biased

### Why reviewer might say this


### Evidence against this attack


### What to add to paper


## Attack 4: Claims are too broad

### Why reviewer might say this


### Evidence against this attack


### What to add to paper


## Attack 5: Evaluation does not prove the claim

### Why reviewer might say this


### Evidence against this attack


### What to add to paper


## Final defense checklist

- [ ] Novelty is clear
- [ ] Baselines are strong
- [ ] Dataset choice is justified
- [ ] Evaluation matches claims
- [ ] Limitations are explicit
```

---

# 25. `ai-context-pack.md`

用于 `60_AI_Context/ai_packs/<paper_or_project>/metadata.md` 或 `task.md`。

```markdown
---
type: ai_context_pack
source:
source_type: paper / project / question_map
created: "{{date:YYYY-MM-DD}}"
---

# AI Context Pack - {{title}}

## Purpose

这次给 AI 的任务是什么？

## Source materials

- Paper full text:
- My note:
- Related notes:
- Project note:

## Background

给 AI 的必要背景，不要假设 AI 知道你的研究系统。

## What I want AI to do

- [ ] Summarize
- [ ] Compare papers
- [ ] Extract method details
- [ ] Extract datasets / metrics
- [ ] Draft related work
- [ ] Critique limitations
- [ ] Generate experiment ideas

## Constraints

- 不要把 AI 输出当事实源
- 必须区分原文信息和推断
- 不要编造 citation
- 不确定时标注 uncertainty

## Output format


```

---

# 26. `ai-paper-review-prompt.md`

```markdown
# AI Paper Review Prompt

你将阅读一篇学术论文的 Markdown 全文，以及我的文献笔记。请完成以下任务。

## Role

你是我的研究助手。你的任务不是替我得出最终结论，而是帮助我抽取、对比、检查和组织信息。

## Input

我会提供：

1. Paper metadata
2. Paper full text converted from PDF
3. My literature note, if available
4. Specific research context

## Tasks

请按以下结构输出：

### 1. One-sentence summary

用一句话说明这篇论文做了什么。

### 2. Problem

- 论文试图解决什么问题？
- 这个问题为什么重要？
- 作者如何定义这个问题？

### 3. Method

- 方法 pipeline 是什么？
- 核心模块是什么？
- 训练目标 / loss 是什么？
- 它和已有方法的区别是什么？

### 4. Experiments

请抽取：

- Datasets
- Metrics
- Baselines
- Main results
- Ablations
- Implementation details

### 5. Claims vs evidence

列出作者的主要 claims，并判断实验是否支持这些 claims。

### 6. Limitations

区分：

- 作者自己承认的 limitation
- 你推断出的 limitation
- 我作为研究者应该警惕的 limitation

### 7. Relevance to my research

结合我提供的研究背景，判断这篇论文可能有什么用：

- motivation
- related work
- baseline
- method component
- dataset / benchmark
- negative example

### 8. Questions for me

提出 5 个我应该继续思考的问题。

## Rules

- 不要编造论文中没有的信息。
- 如果信息来自论文原文，请说明位置或章节。
- 如果是你的推断，请明确标注“推断”。
- 如果不确定，请说不确定。
- 不要生成不存在的引用。
```

---

# 27. `ai-literature-comparison-prompt.md`

```markdown
# AI Literature Comparison Prompt

你将比较多篇论文。请不要只做逐篇摘要，而要找出它们之间的关系。

## Input

我会提供多篇文献笔记或 AI context packs。

## Tasks

### 1. Comparison table

请生成表格，列包括：

- Paper
- Problem
- Method
- Dataset
- Metric
- Main claim
- Limitation
- Relevance to my question

### 2. Research landscape

这些论文构成了什么研究脉络？

### 3. Main disagreements

它们在哪些问题上观点不同？

### 4. Method evolution

方法如何演化？

### 5. Dataset / evaluation issues

它们是否使用了不同数据集或指标？这些差异会不会影响结论？

### 6. Gap

现有工作没有解决什么？

### 7. Possible research directions

基于这些论文，提出可能的研究切入点。

## Rules

- 区分论文原文信息和你的推断。
- 不要编造没有出现过的实验结果。
- 不要把所有论文强行归为同一类。
- 如果比较依据不足，请指出缺失信息。
```

---

# 28. `controlled-vocabulary.md`

用于统一 YAML 字段值，防止同义词混乱。

```markdown
---
type: maintenance
subtype: controlled_vocabulary
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# Controlled Vocabulary

规则：

```text
1. 字段值使用英文
2. 小写
3. 使用 snake_case
4. 不使用空格
5. 不在 YAML 分类字段中使用中文
6. 新增字段值前，先检查是否已有同义词
```

## type

- inbox
- literature
- field_map
- question_map
- method
- dataset
- dataset_index
- candidate_topic
- project
- project_note
- ai_context_pack
- maintenance

## literature subtype

- paper
- survey
- book
- method_paper
- dataset_paper
- benchmark_paper
- thesis
- report
- webpage

## domain

- computer_vision
- remote_sensing
- nlp
- multimodal_learning
- geospatial_ai
- machine_learning
- deep_learning

## task

- foundation_model
- representation_learning
- semantic_segmentation
- object_detection
- oriented_object_detection
- image_retrieval
- change_detection
- classification
- visual_question_answering
- image_captioning
- grounding
- detection
- domain_adaptation
- transfer_learning
- few_shot_learning

## modality

- optical
- rgb
- multispectral
- hyperspectral
- sar
- lidar
- text
- image
- video
- time_series

## method_family

- cnn
- vision_transformer
- masked_image_modeling
- contrastive_learning
- self_supervised_learning
- supervised_learning
- weakly_supervised_learning
- semi_supervised_learning
- adapter_tuning
- prompt_tuning
- vision_language_model
- diffusion_model
- domain_adaptation
- retrieval_augmented_generation

## dataset

- dota
- xview
- spacenet
- loveda
- bigearthnet
- fair1m
- nwpu_vhr10
- aid
- eurosat
- unknown

## status

### literature status

- inbox
- to_check
- to_read
- skimmed
- read
- annotated
- note_done
- cited
- x_irrelevant

### project status

- exploring
- active
- paused
- finished
- abandoned

## reading_level

- L0
- L1
- L2
- L3
- L4

## relevance

- unknown
- weak
- medium
- strong
- high

## priority

- low
- medium
- high

## replication_status

- not_started
- code_found
- environment_ready
- demo_ran
- partially_reproduced
- reproduced
- failed
- abandoned
```

---

# 29. `dataview-literature-dashboard.md`

建议放在 `20_Field_Maps/文献数据库.md` 或 `21_Question_Maps/文献处理面板.md`。

```markdown
---
type: dashboard
subtype: literature_dashboard
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# 文献数据库

## 全部文献

```dataview
TABLE citekey, year, status, reading_level, relevance, domain, task, method_family
FROM "10_Literature"
WHERE type = "literature"
SORT year DESC
```

## 待读文献

```dataview
TABLE citekey, title, year, relevance, domain, task
FROM "10_Literature"
WHERE type = "literature"
WHERE status = "to_read" OR status = "to_check"
SORT year DESC
```

## 已泛读文献 L2

```dataview
TABLE citekey, title, year, relevance, domain, task, method_family
FROM "10_Literature"
WHERE type = "literature"
WHERE reading_level = "L2"
SORT year DESC
```

## 精读及以上文献 L3/L4

```dataview
TABLE citekey, title, year, reading_level, relevance, domain, task, method_family
FROM "10_Literature"
WHERE type = "literature"
WHERE reading_level = "L3" OR reading_level = "L4"
SORT relevance DESC
```

## 高相关文献

```dataview
TABLE citekey, title, year, status, reading_level, domain, task, method_family
FROM "10_Literature"
WHERE type = "literature"
WHERE relevance = "high" OR relevance = "strong"
SORT year DESC
```

## 缺少关键字段的文献

```dataview
TABLE citekey, title, status, reading_level, domain, task, method_family, relevance
FROM "10_Literature"
WHERE type = "literature"
WHERE !citekey OR !title OR !domain OR !task OR !method_family OR relevance = "unknown"
SORT file.name ASC
```

## 已有 Zotero 标注但未整理成 note_done

```dataview
TABLE citekey, title, year, status, reading_level, relevance
FROM "10_Literature"
WHERE type = "literature"
WHERE status = "annotated"
SORT year DESC
```

## 按项目筛选：示例

```dataview
TABLE citekey, title, year, status, reading_level, relevance, method_family, dataset
FROM "10_Literature"
WHERE type = "literature"
WHERE contains(projects, "project_name_here")
SORT relevance DESC
```

## 按问题地图筛选：示例

```dataview
TABLE citekey, title, year, status, reading_level, relevance, method_family, dataset
FROM "10_Literature"
WHERE type = "literature"
WHERE contains(question_maps, "question_map_name_here")
SORT relevance DESC
```
```

---

# 30. Zotero Integration 导入模板示意

这个模板不是给 Obsidian Core Templates 直接用的，而是给 Zotero Integration / ZotLit 这类插件用的。具体变量名称需要根据插件的数据浏览器微调。

```markdown
---
type: literature
subtype: paper

citekey: "{{citekey}}"
title: "{{title}}"
year: "{{date | format('YYYY')}}"
authors: "{{authors}}"
venue: "{{publicationTitle}}"
doi: "{{DOI}}"
url: "{{url}}"
zotero: "{{select}}"

domain: []
task: []
modality: []
method_family: []
dataset: []

status: read
reading_level: L3
relevance: high

projects: []
field_maps: []
question_maps: []
related_methods: []
related_datasets: []

questions: []

created: "{{importDate | format('YYYY-MM-DD')}}"
updated: "{{importDate | format('YYYY-MM-DD')}}"
---

# {{title}}

## Bibliography

{{bibliography}}

## Abstract

{{abstractNote}}

## Core claim

{% persist "core-claim" %}

{% endpersist %}

## Research question

{% persist "research-question" %}

{% endpersist %}

## Background

{% persist "background" %}

{% endpersist %}

## Method details

{% persist "method-details" %}

### Key idea


### Assumptions


### Pipeline / architecture


### Objective / loss / algorithm

{% endpersist %}

## Experiments

{% persist "experiments" %}

### Datasets


### Baselines


### Metrics


### Main results


### Ablations

{% endpersist %}

## What this paper contributes

{% persist "contributions" %}

{% endpersist %}

## What this paper does not solve

{% persist "unsolved" %}

{% endpersist %}

## Limitations / concerns

{% persist "limitations-concerns" %}

{% endpersist %}

## Relationship to other work

{% persist "relationship-to-other-work" %}

### Earlier work


### Similar work


### Follow-up work


### Contradicting work

{% endpersist %}

## Relevance to my research

{% persist "relevance-to-my-research" %}

{% endpersist %}

## Reusable concepts

{% persist "reusable-concepts" %}

{% endpersist %}

## Possible project use

{% persist "possible-project-use" %}

{% endpersist %}

## Open questions

{% persist "open-questions" %}

{% endpersist %}

## My critique

{% persist "my-critique" %}

{% endpersist %}

## Zotero annotations / excerpts

{% for annotation in annotations %}
{% if annotation.annotatedText %}
> Page {{annotation.page}}: {{annotation.annotatedText}}
{% endif %}
{% if annotation.comment %}
>
> Comment: {{annotation.comment}}
{% endif %}

{% endfor %}
```

---

# 31. 推荐使用规则

## L0 / L1 不一定进入 Obsidian

```text
L0：丢弃文献，只在 Zotero 标注 x_irrelevant，不进入 Obsidian
L1：收藏但不读，只在 Zotero 标注 to_check，通常不进入 Obsidian
L2：进入 Obsidian，使用 literature-note-L2.md
L3：进入 Obsidian，使用 literature-note-L3.md
L4：进入 Obsidian，使用 literature-note-L4.md
```

## YAML 字段只放稳定信息

适合放 YAML：

```text
citekey
title
year
domain
task
method_family
dataset
status
reading_level
relevance
projects
question_maps
```

不适合放 YAML：

```text
长篇批判
复杂推理
论文段落草稿
详细实验解释
对作者观点的长篇评论
```

## 文献笔记不要太长

普通 L2 文献只写 4 行即可。L3 / L4 才值得长笔记。

## 地图笔记必须有人工总结

Dataview 表格只能自动收集，不等于理解。每个 field map / question map 都必须有“我当前的判断”。

## AI 输出必须隔离

AI context pack 和 AI outputs 放在 `60_AI_Context/`。不要让 AI 输出直接覆盖你的 literature note。可以把有价值的部分人工整理进正式笔记。

