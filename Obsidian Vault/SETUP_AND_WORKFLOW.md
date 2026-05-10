# Obsidian 配置与使用流程

这份说明把这个 vault 的初始化配置、插件建议、模板使用方法和日常工作流整理成一套可直接执行的步骤。

## 1. 初始化配置

### 1.1 打开仓库

1. 在 Obsidian 中选择 `Open folder as vault`。
2. 打开当前目录 `D:\Users\Learning\CV`。

### 1.2 检查目录是否完整

第一次打开后，确认这些目录已经存在：

- `00_Inbox/`
- `10_Literature/`
- `20_Field_Maps/`
- `21_Question_Maps/`
- `30_Methods/`
- `35_Datasets_Benchmarks/`
- `40_Candidate_Topics/`
- `50_Projects/`
- `60_AI_Context/`
- `90_Templates/`
- `99_Attachments/`

## 2. 插件配置

这套系统建议至少使用 2 个插件：

- `Dataview`
- `Zotero Integration`

### 2.1 Dataview

用途：

- 让 `field map`、`question map`、`dataset index`、`文献数据库` 自动生成表格
- 基于 YAML 字段筛选文献、项目、数据集

建议设置：

1. 打开 `Settings -> Community plugins`
2. 安装并启用 `Dataview`
3. 保持默认设置即可

验证方法：

1. 打开 [文献数据库.md]
2. 如果 Dataview 已启用，代码块会被渲染为表格
3. 现在库里还没有正式文献，表格为空是正常的


### 2.2 Zotero Integration

用途：

- 从 Zotero 导入 metadata、bibliography、abstract、annotations
- 配合 Better BibTeX 使用 `citekey`

建议设置：

1. 安装并启用 `Zotero Integration`
2. 在 Zotero 里安装并启用 `Better BibTeX`
3. 确保 Zotero 能稳定生成 citation key
4. 在 Obsidian 里将导入模板指向：
   `90_Templates/zotero-integration-import-template.md`

说明：

- 这个模板是给 Zotero Integration 用的，不是普通新建笔记模板
- 文献导入后，仍然需要你手动维护 `domain`、`task`、`method_family`、`relevance` 等字段


## 4. 命名与存放规则

### 4.1 文献笔记

统一放在：

- `10_Literature/Papers/`
- `10_Literature/Surveys/`
- `10_Literature/Books/`

命名建议：

- 普通论文：`@citekey.md`
- 综述：`@citekey.md`
- 书籍：可以用 `书名.md` 或 `@citekey.md`

例如：

- `10_Literature/Papers/@wangRemoteSensingFoundation2024.md`
- `10_Literature/Surveys/@liRemoteSensingSurvey2025.md`

### 4.2 问题与地图笔记

统一使用自然语言问题或概念命名：

- `20_Field_Maps/CV × Remote Sensing 地图.md`
- `21_Question_Maps/遥感基础模型是否需要专门预训练.md`
- `30_Methods/Masked Image Modeling.md`
- `35_Datasets_Benchmarks/DOTA.md`

### 4.3 项目目录

正式项目放在：

- `50_Projects/<ProjectName>/`

建议项目名短一些、稳定一些，例如：

- `50_Projects/RS_Foundation_Model_Transfer/`
- `50_Projects/GeoVLM_Eval/`


## 5. 日常使用流程

下面这套流程是最推荐的。

### 5.1 新材料进入系统

当你刚看到一篇论文、一个想法、一段 AI 输出、一个数据集链接时：

1. 先不要纠结放哪里
2. 先放进 `00_Inbox/`
3. 用 [00-inbox-note.md] 建一条临时记录

适合丢进 Inbox 的内容：

- 刚发现但还没读的论文
- 会议时记录的灵感
- 一个还没验证的研究问题
- AI 帮你生成但还没核实的摘要
- 别人推荐给你的 benchmark

原则：

- 先记录
- 后整理
- 不让输入阶段卡住

### 5.2 文献进入正式笔记

当一篇文献值得进入 Obsidian 时：

1. 在 Zotero 中保存条目并阅读、标注
2. 判断这篇文献属于 L2、L3 还是 L4
3. 在 `10_Literature/Papers/` 新建笔记
4. 选择对应模板

模板选择建议：

- 快速筛选：`literature-note-L2.md`
- 精读理解：`literature-note-L3.md`
- 核心文献 / 复现 / 批判：`literature-note-L4.md`
- 不确定时可先用：`literature-note.md`

最关键的维护项不是正文，而是 YAML：

- `domain`
- `task`
- `method_family`
- `dataset`
- `status`
- `reading_level`
- `relevance`
- `projects`
- `question_maps`

### 5.3 从文献走向问题

当你发现多篇文献围绕同一个争议或问题时：

1. 在 `21_Question_Maps/` 新建一个问题地图
2. 使用 [question-map.md](D:/Users/Learning/CV/90_Templates/question-map.md)
3. 把相关文献链过去
4. 手动写“我的当前判断”

这个步骤非常重要，因为：

- Dataview 只能聚合
- 真正的研究判断需要你手写

### 5.4 从问题走向方法与数据集

如果同一个方法或数据集反复出现，就不要只在文献笔记里零散记录。

应该拆出独立笔记：

- 方法写入 `30_Methods/`
- 数据集写入 `35_Datasets_Benchmarks/`

使用模板：

- [method-note.md](D:/Users/Learning/CV/90_Templates/method-note.md)
- [dataset-note.md](D:/Users/Learning/CV/90_Templates/dataset-note.md)

好处：

- 同类知识不会散落在几十篇论文里
- 后面写综述、写 related work、选 baseline 会更快

### 5.5 从问题走向候选选题

当你对某个问题不只是“理解”，而是开始思考“我能做什么”时：

1. 在 `40_Candidate_Topics/` 新建候选选题
2. 使用 [candidate-topic.md](D:/Users/Learning/CV/90_Templates/candidate-topic.md)
3. 明确：
   - 研究问题
   - gap
   - 可用数据集
   - baseline
   - 风险

候选选题和问题地图的区别：

- `question map`：别人怎么想
- `candidate topic`：我准备做什么

### 5.6 从候选选题进入正式项目

满足下面这些条件时，就可以进入 `50_Projects/`：

- 研究问题比较清楚
- baseline 大致明确
- 数据集候选明确
- 初步实验能设计出来
- 你能说清楚潜在贡献

建立项目后，建议创建一个项目文件夹，并放入这些文件：

- `overview.md` 或 `README.md`
- `00_problem.md`
- `01_related_work.md`
- `02_baselines.md`
- `03_datasets.md`
- `04_experiments.md`
- `05_results.md`
- `06_writing.md`
- `reviewer_attacks.md`

对应模板都已在 `90_Templates/` 中准备好。



## 6. AI 材料如何使用

`60_AI_Context/` 是故意隔离出来的区域，不要把 AI 输出直接当正式笔记。

推荐方式：

1. 把 PDF 转成 markdown，放到 `60_AI_Context/fulltext_md/`
2. 为某篇论文或项目建立一个 `ai_pack`
3. 用 AI 做抽取、比较、草稿辅助
4. 人工把有价值内容整理回正式笔记

记住：

- AI 输出不是事实源
- 正式判断写回 literature note / question map / project note
- AI 区只做“加工区”，不做最终知识库


## 8. 使用时最容易出错的地方

### 8.1 YAML 分类字段写中文

不要在这些字段里写中文：

- `domain`
- `task`
- `method_family`
- `dataset`
- `status`

请统一参考 [controlled-vocabulary.md](D:/Users/Learning/CV/90_Templates/controlled-vocabulary.md)。

### 8.2 文献笔记写得太长

建议：

- `L2` 保持极简
- `L3` 关注方法和实验
- `L4` 只留给真正核心的文献

不是每篇论文都值得写成长文。

### 8.3 只建 Dataview 表，不写人工判断

自动表格只能帮你收集，不能替你思考。

这些文件里一定要手写结论：

- `20_Field_Maps/*.md`
- `21_Question_Maps/*.md`
- `40_Candidate_Topics/*.md`
- `50_Projects/*`

### 8.4 把 AI 输出直接覆盖正式笔记

不要这么做。

正确方式是：

1. AI 输出先进入 `60_AI_Context/`
2. 你人工核查
3. 再把确认有价值的内容整理进正式笔记



