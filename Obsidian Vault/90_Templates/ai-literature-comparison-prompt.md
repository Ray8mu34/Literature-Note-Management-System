# AI Literature Comparison Prompt

你将比较多篇论文。请不要只做逐篇摘要，而要找出它们之间的关系。

## Input

我会提供多篇文献笔记或 AI context packs。

## Tasks

### 1. Comparison table

请生成表格，列包括：

- Paper
- Problem
- Method
- Dataset
- Metric
- Main claim
- Limitation
- Relevance to my question

### 2. Research landscape

这些论文构成了什么研究脉络？

### 3. Main disagreements

它们在哪些问题上观点不同？

### 4. Method evolution

方法如何演化？

### 5. Dataset / evaluation issues

它们是否使用了不同数据集或指标？这些差异会不会影响结论？

### 6. Gap

现有工作没有解决什么？

### 7. Possible research directions

基于这些论文，提出可能的研究切入点。

## Rules

- 区分论文原文信息和你的推断。
- 不要编造没有出现过的实验结果。
- 不要把所有论文强行归为同一类。
- 如果比较依据不足，请指出缺失信息。
