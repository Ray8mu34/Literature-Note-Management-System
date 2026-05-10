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
