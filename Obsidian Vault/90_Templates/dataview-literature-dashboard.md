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
