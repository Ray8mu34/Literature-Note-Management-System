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

status: skimmed
reading_level: L2
relevance: unknown

projects: []
field_maps: []
question_maps: []

questions: []

created: "{{importDate | format('YYYY-MM-DD')}}"
updated: "{{importDate | format('YYYY-MM-DD')}}"
---

# {{title}}

## Bibliography

{{bibliography}}

## Abstract

{{abstractNote}}

## Quick screening

{% persist "quick-screening" %}

- Problem:
- Method:
- Relevance: strong / medium / weak
- Keep because:

{% endpersist %}

## Possible use

{% persist "possible-use" %}

- [ ] Related work
- [ ] Background
- [ ] Baseline
- [ ] Dataset / benchmark reference
- [ ] Method reference
- [ ] Not useful now, maybe later

{% endpersist %}

## Notes

{% persist "notes" %}

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
