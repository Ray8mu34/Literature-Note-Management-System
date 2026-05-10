---
type: maintenance
subtype: controlled_vocabulary
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# Controlled Vocabulary

规则：

```text
1. 字段值使用英文
2. 小写
3. 使用 snake_case
4. 不使用空格
5. 不在 YAML 分类字段中使用中文
6. 新增字段值前，先检查是否已有同义词
```

## type

- inbox
- literature
- field_map
- question_map
- method
- dataset
- dataset_index
- candidate_topic
- project
- project_note
- ai_context_pack
- maintenance

## literature subtype

- paper
- survey
- book
- method_paper
- dataset_paper
- benchmark_paper
- thesis
- report
- webpage

## domain

- computer_vision
- remote_sensing
- nlp
- multimodal_learning
- geospatial_ai
- machine_learning
- deep_learning

## task

- foundation_model
- representation_learning
- semantic_segmentation
- object_detection
- oriented_object_detection
- image_retrieval
- change_detection
- classification
- visual_question_answering
- image_captioning
- grounding
- detection
- domain_adaptation
- transfer_learning
- few_shot_learning

## modality

- optical
- rgb
- multispectral
- hyperspectral
- sar
- lidar
- text
- image
- video
- time_series

## method_family

- cnn
- vision_transformer
- masked_image_modeling
- contrastive_learning
- self_supervised_learning
- supervised_learning
- weakly_supervised_learning
- semi_supervised_learning
- adapter_tuning
- prompt_tuning
- vision_language_model
- diffusion_model
- domain_adaptation
- retrieval_augmented_generation

## dataset

- dota
- xview
- spacenet
- loveda
- bigearthnet
- fair1m
- nwpu_vhr10
- aid
- eurosat
- unknown

## status

### literature status

- inbox
- to_check
- to_read
- skimmed
- read
- annotated
- note_done
- cited
- x_irrelevant

### project status

- exploring
- active
- paused
- finished
- abandoned

## reading_level

- L0
- L1
- L2
- L3
- L4

## relevance

- unknown
- weak
- medium
- strong
- high

## priority

- low
- medium
- high

## replication_status

- not_started
- code_found
- environment_ready
- demo_ran
- partially_reproduced
- reproduced
- failed
- abandoned
