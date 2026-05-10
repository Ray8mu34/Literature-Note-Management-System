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
