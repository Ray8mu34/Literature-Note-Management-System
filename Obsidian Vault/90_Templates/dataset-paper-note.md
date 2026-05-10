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
