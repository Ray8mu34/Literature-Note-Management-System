# Literature Note Management System

一个基于Obsidian的文献笔记管理系统，用于学术研究和知识管理。

## 项目结构

```
文献笔记管理/
├── AI_KNOWLEDGE_BASE_GUIDE.md    # AI知识库使用指南
├── README.md                     # 项目说明
├── Obsidian Vault/              # Obsidian笔记库
│   ├── 00_Inbox/                # 收件箱
│   ├── 10_Literature/           # 文献笔记
│   ├── 20_Field_Maps/           # 领域地图
│   ├── 21_Question_Maps/        # 问题地图
│   ├── 30_Methods/              # 方法笔记
│   ├── 35_Datasets_Benchmarks/  # 数据集和基准
│   ├── 40_Candidate_Topics/     # 候选主题
│   ├── 50_Projects/             # 项目笔记
│   ├── 60_AI_Context/           # AI上下文
│   ├── 90_Templates/            # 笔记模板
│   ├── 95_Scripts/              # Python脚本
│   └── 99_Attachments/          # 附件
└── rag_runtime/                 # RAG运行时环境
```

## 主要功能

### 1. 文献管理
- 多层级文献笔记系统（L2-L4）
- 文献分类和标签管理
- Zotero集成支持

### 2. 知识组织
- 领域地图和问题地图
- 方法论笔记
- 数据集和基准记录

### 3. AI辅助
- AI知识库构建
- RAG（检索增强生成）支持
- 智能上下文管理

### 4. 项目管理
- 研究项目跟踪
- 候选主题管理
- 实验记录

## 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/Ray8mu34/Literature-Note-Management-System.git
```

### 2. 打开Obsidian
1. 安装[Obsidian](https://obsidian.md/)
2. 打开Obsidian，选择"打开另一个库"
3. 选择克隆的`Obsidian Vault`文件夹

### 3. 安装依赖（可选）
如果需要使用Python脚本：
```bash
cd "Obsidian Vault/95_Scripts"
pip install -r requirements.txt
```

## 模板系统

系统包含多种笔记模板：
- 文献笔记模板（L2-L4）
- 项目笔记模板
- 数据集记录模板
- 方法论笔记模板
- AI上下文模板

## 脚本工具

`95_Scripts`目录包含以下工具：
- `convert_pdf_to_md.py` - PDF转Markdown
- `build_kb.py` - 知识库构建
- `ai_context_pipeline.py` - AI上下文处理
- `query.py` - 知识库查询
- `zotero_citekey_resolver.py` - Zotero引用键解析

## 配置说明

### Obsidian配置
`.obsidian`目录已忽略，不包含在版本控制中。每个用户需要根据自己的Obsidian设置进行配置。

### 环境变量
脚本需要配置环境变量，参考`.env.example`文件。

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License

## 联系方式

- GitHub: [Ray8mu34](https://github.com/Ray8mu34)
- 邮箱: 3067482506@qq.com