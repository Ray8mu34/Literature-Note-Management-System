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
