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
