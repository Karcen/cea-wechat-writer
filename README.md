### README.md（中文）

# CEA_Skill 项目说明与使用教程

**文档语言：中文（默认）｜[English documentation](README_EN.md)**

## 快速开始（Quick Start）

本项目支持基于 AI 的论文深度解读与 CEA 公众号内容生成工作流。

### 1. 准备论文材料

对于论文深度解读任务，建议准备以下三个输入：

```text
paper/
├── paper.pdf              # 原始论文 PDF（最高优先级参考）
├── paper.md               # PDF 转换后的 Markdown（用于快速检索和理解）
└── figures/               # 论文图片、图表和插图
```

推荐流程：

1. 下载论文 PDF；
2. 使用 PDF 转 Markdown 工具（例如 MarkItDown Online）生成 Markdown 文件；
3. 单独下载或提取论文中的 figures；
4. 将三个文件/目录路径同时提供给 AI。

### 2. 为什么同时提供 PDF、Markdown 和图片？

三类材料承担不同任务：

| 文件       | 用途                            | 优先级 |
| -------- | ----------------------------- | --- |
| PDF      | 最终事实依据，包括公式、表格、脚注、排版和精确定位     | 最高  |
| Markdown | 快速阅读、关键词检索、结构理解，减少模型 token 消耗 | 辅助  |
| figures  | 精确分析论文图表、机制图和实验结果             | 辅助  |

默认阅读逻辑：

1. 首先读取 Markdown，快速建立论文结构；
2. 当 Markdown 出现公式错误、表格丢失、符号异常或格式无法识别时；
3. 回到 PDF 进行核验；
4. 涉及图表解释时读取 figures 或 PDF 原图。

这样可以在降低 token 消耗的同时，提高复杂论文（尤其包含大量公式、表格和图形）的解析准确率。

### 3. 启动论文解读

向 AI 输入：

```text
使用 $cea-wechat-writer 启动论文深度解读工作流。

我的论文材料如下：

1. Skill 路径：
[填写路径]

2. 论文 PDF：
[填写路径]

3. 论文 Markdown：
[填写路径]

4. 论文 figures：
[填写路径]

5. 输出目录：
[填写路径]

请先执行阶段 1：
- 检查所有输入文件；
- 确认 PDF、Markdown 和 figures 是否对应同一篇论文；
- 说明三类材料分别如何使用；
- 不开始正式论文解读。

只有我明确回复“开始阶段 2”后，再生成最终论文解读。
```

### 4. 推荐工作原则

* Markdown 用于快速理解，不作为最终证据来源；
* PDF 是公式、数字、引用和关键结论的最终依据；
* figures 用于辅助解释论文中的视觉信息；
* AI 不应直接相信 Markdown 转换结果，需要在关键位置回查 PDF；
* 对公式、模型、识别策略和定量结果必须优先核验原 PDF。

### 5. 下一步

完成 Quick Start 后，可继续阅读：

* 两阶段论文解读教程；
* CEA 公众号 Markdown 初稿教程；
* Skill 安装与配置说明。

---

### README_EN.md（English）

# CEA_Skill Project Guide

**Documentation language: Chinese (default) | [English documentation](README_EN.md)**

## Quick Start

This project provides AI-assisted workflows for deep research paper analysis and CEA WeChat article generation.

## 1. Prepare Paper Materials

For deep paper analysis, prepare the following three inputs:

```text
paper/
├── paper.pdf              # Original paper PDF (primary source)
├── paper.md               # Markdown converted from PDF (fast reading/search)
└── figures/               # Paper figures, tables, and illustrations
```

Recommended workflow:

1. Download the original paper PDF;
2. Convert the PDF into Markdown using a PDF-to-Markdown tool (e.g., MarkItDown Online);
3. Download or extract paper figures separately;
4. Provide all three paths to the AI system.

## 2. Why Provide PDF, Markdown, and Figures Together?

Each material serves a different purpose:

| File     | Purpose                                                                           | Priority  |
| -------- | --------------------------------------------------------------------------------- | --------- |
| PDF      | Final source for equations, tables, footnotes, formatting, and precise references | Highest   |
| Markdown | Fast reading, keyword search, and structural understanding with fewer tokens      | Auxiliary |
| figures  | Detailed analysis of charts, diagrams, and visual evidence                        | Auxiliary |

Default reading strategy:

1. Read Markdown first to quickly understand the paper structure;
2. If formulas, tables, symbols, or formatting are incorrectly converted;
3. Return to the original PDF for verification;
4. Use figures or PDF images when analyzing visual evidence.

This workflow reduces token consumption while improving accuracy for papers with complex equations, tables, and figures.

## 3. Start Paper Analysis

Provide the following instruction to AI:

```text
Use $cea-wechat-writer to start the deep paper analysis workflow.

My paper materials:

1. Skill path:
[insert path]

2. Paper PDF:
[insert path]

3. Paper Markdown:
[insert path]

4. Paper figures:
[insert path]

5. Output directory:
[insert path]

First execute Stage 1:
- Check all input files;
- Confirm that PDF, Markdown, and figures belong to the same paper;
- Explain how each material will be used;
- Do not start the final analysis.

Only begin Stage 2 after I explicitly reply:
"Start Stage 2".
```

## 4. Recommended Principles

* Markdown is for fast understanding, not the final evidence source;
* PDF is the authoritative source for equations, numbers, citations, and conclusions;
* Figures provide additional evidence for visual interpretation;
* AI should verify important information against the PDF instead of relying on conversion output;
* Equations, models, identification strategies, and quantitative results require PDF-level verification.

## 5. Next Steps

After completing Quick Start, continue with:

* Two-stage paper analysis workflow;
* CEA WeChat Markdown generation workflow;
* Skill installation and configuration guide.
