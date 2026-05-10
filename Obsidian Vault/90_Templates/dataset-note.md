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
