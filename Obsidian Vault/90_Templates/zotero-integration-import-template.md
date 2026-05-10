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
