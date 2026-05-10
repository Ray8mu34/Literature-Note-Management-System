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
