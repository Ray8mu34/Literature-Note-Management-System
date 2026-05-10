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
