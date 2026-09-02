# CEA_Skill 项目指南与教程

**文档语言：[中文（默认）](README.md) | English**

> 
> 中文仅作为项目文档默认入口。任何写作任务均不可跳过语言确认环节；生成内容仍需确认使用中文、英文、严格中英双语或其他语言。

本目录包含全欧/全英中国经济学会（CEA）的公众号写作与深度论文分析工作流，含可安装的 Codex Skill、历史训练素材、参考格式 Skill、品牌素材图片以及完整示例。

可调用 Skill 位于 [`cea-wechat-writer/`](cea-wechat-writer/)。

## 目录

- [1. 项目功能](#1-%E9%A1%B9%E7%9B%AE%E5%8A%9F%E8%83%BD)
- [2. 项目目录结构](#2-%E9%A1%B9%E7%9B%AE%E7%9B%AE%E5%BD%95%E7%BB%93%E6%9E%84)
- [3. 安装或更新 Skill](#3-%E5%AE%89%E8%A3%85%E6%88%96%E6%9B%B4%E6%96%B0-skill)
- [4. 五分钟快速上手](#4-%E4%BA%94%E5%88%86%E9%92%9F%E5%BF%AB%E9%80%9F%E4%B8%8A%E6%89%8B)
- [5. 教程一：双阶段论文分析](#5-%E6%95%99%E7%A8%8B%E4%B8%80%E5%8F%8C%E9%98%B6%E6%AE%B5%E8%AE%BA%E6%96%87%E5%88%86%E6%9E%90)
- [6. 教程二：CEA公众号Markdown稿件撰写](#6-%E6%95%99%E7%A8%8B%E4%BA%8Ccea%E5%85%AC%E4%BC%97%E5%8F%B7markdown%E7%A8%BF%E4%BB%B6%E6%92%B0%E5%86%99)
- [7. CEA强制写作与排版规范](#7-cea%E5%BC%BA%E5%88%B6%E5%86%99%E4%BD%9C%E4%B8%8E%E6%8E%92%E7%89%88%E8%A7%84%E8%8C%83)
- [8. 七大内容分类与五类模板](#8-%E4%B8%83%E5%A4%A7%E5%86%85%E5%AE%B9%E5%88%86%E7%B1%BB%E4%B8%8E%E4%BA%94%E7%B1%BB%E6%A8%A1%E6%9D%BF)
- [9. 训练数据与历史语料库](#9-%E8%AE%AD%E7%BB%83%E6%95%B0%E6%8D%AE%E4%B8%8E%E5%8E%86%E5%8F%B2%E8%AF%AD%E6%96%99%E5%BA%93)
- [10. 脚本、示例与校验](#10-%E8%84%9A%E6%9C%AC%E7%A4%BA%E4%BE%8B%E4%B8%8E%E6%A0%A1%E9%AA%8C)
- [11. 输出文件与发布边界](#11-%E8%BE%93%E5%87%BA%E6%96%87%E4%BB%B6%E4%B8%8E%E5%8F%91%E5%B8%83%E8%BE%B9%E7%95%8C)
- [12. 故障排查](#12-%E6%95%85%E9%9A%9C%E6%8E%92%E6%9F%A5)
- [13. 资料来源与版权说明](#13-%E8%B5%84%E6%96%99%E6%9D%A5%E6%BA%90%E4%B8%8E%E7%89%88%E6%9D%83%E8%AF%B4%E6%98%8E)

## 1. 项目功能

本项目支持两套独立工作模式：

| 模式 | 主要用途 | 默认输出结果 |
| --- | --- | --- |
| CEA公众号写作 | 论文解读、方法介绍、会议资讯、新闻、历史专题、特刊、招聘推文 | 本地公众号Markdown稿件、来源台账、QA核查报告、发布前指引、配套图片 |
| 深度论文分析 | 阅读笔记、文献综述素材、研究设计分析、理论与证据评估 | 一份面向读者的完整分析文稿 + 一份编辑审核记录 |

若用户仅提出“论文分析”需求，Skill 会先确认输出是公众号推文，还是论文阅读笔记。默认不会混合两套输出结构。

### 1.1 公众号写作模式

公众号模式重点要求：

- 遵循CEA行文风格，使用五套固定模板；
- 事实内容必须有原始或官方来源支撑；
- 生成`sources.md`来源台账；
- 本地图片资源、隐藏来源注释、每张图的图注确认；
- 严格质量核查，附带双语发布前指引；
- 最终仍需在公众号编辑器内完成人工调整。

### 1.2 论文分析模式

研究分析模式重点要求：

- 同时使用论文PDF、转换后的Markdown、论文图表；
- 必须先完成第一阶段对齐校验，再执行第二阶段分析；
- 文稿内部区分作者观点、论文证据、作者解读、编辑判断；面向读者输出时做自然转述；
- 只选取服务核心论点的理论、方法、结果、图表、创新点与局限，不逐章节复述全文；
- 关键判断需标注对应原文章节、图表、表格、公式、附录或PDF页码；
- 分析文稿一般设置4‑6个二级标题，保证篇幅适中、逻辑连贯；
- 工作流状态、判断映射关系、待核实问题全部存放在独立的编辑审核记录中。

## 2. 项目目录结构

```
CEA_Skill/
├── README.md                       默认中文项目教程
├── README_EN.md                    英文项目指南
├── cea-wechat-writer/              可安装调用的Skill
│   ├── SKILL.md                    执行规则入口文件
│   ├── README.md                   Skill完整中文教程
│   ├── README_EN.md                Skill完整英文教程
│   ├── agents/openai.yaml          Codex接口元数据与默认提示词
│   ├── assets/                     模板提示词与品牌资源
│   ├── references/                 证据、行文、图片、质量核查完整规则
│   ├── sample/                     七大类内容示例
│   └── scripts/                    生成、检索、质检、归档脚本
├── training_data/                  历史HTML与世经Word/PDF素材
├── ref-duyi-wechat-skill-suite-main/  参考格式Skill
└── QR_code-png/                    CEA二维码与联合传播素材图片
```

关键入口文件：

- [Skill执行规则](cea-wechat-writer/SKILL.md)
- [Skill完整中文教程](cea-wechat-writer/README.md)
- [Skill完整英文教程](cea-wechat-writer/README_EN.md)
- [论文分析工作流](cea-wechat-writer/references/research-paper-analysis-workflow.md)
- [论文分析启动提示词](cea-wechat-writer/assets/prompts/START_RESEARCH_PAPER_ANALYSIS.md)
- [自然行文与干净文稿规范](cea-wechat-writer/references/natural-writing-and-clean-copy.md)
- [七套公众号示例文稿](cea-wechat-writer/sample/)

类似`CEA_Work_Test/`这类工作文件夹不属于可安装Skill，不要复制到Codex技能目录。

## 3. 安装或更新Skill

### 3.1 可移植路径标记说明

本README面向GitHub团队共享，不绑定任何贡献者用户名和本地目录。全文使用如下占位符：

| 占位符 | 含义 | 示例 |
| --- | --- | --- |
| `<repo-root>` | 克隆仓库根目录 | `/path/to/CEA_Skill` |
| `<skill-root>` | 存放`SKILL.md`的目录 | `/path/to/CEA_Skill/cea-wechat-writer` |
| `<codex-skills-directory>` | Codex本地技能目录 | `/path/to/.codex/skills` |

仓库内链接与命令尽量使用相对路径。实际执行任务、传入论文、指定输出目录时，将占位符替换为本机真实绝对路径。

若无特殊说明，下面所有仓库相关命令均在`<repo-root>`目录执行。

### 3.2 同步到Codex

```
CEA_REPO_ROOT="/path/to/CEA_Skill"
CEA_CODEX_SKILLS_ROOT="/path/to/.codex/skills"
mkdir -p "${CEA_CODEX_SKILLS_ROOT}/cea-wechat-writer"
rsync -a \
  --exclude '.DS_Store' \
  --exclude '__pycache__' \
  "${CEA_REPO_ROOT}/cea-wechat-writer/" \
  "${CEA_CODEX_SKILLS_ROOT}/cea-wechat-writer/"
```

运行前把`/path/to/...`替换成本机真实目录。
命令未使用`--delete`，不会删除目标目录内原有额外文件。同步完成后新建任务或重启任务，让Codex重新加载Skill。

### 3.3 确认安装成功

确认该文件存在：

```
<codex-skills-directory>/cea-wechat-writer/SKILL.md
```

调用Skill：

```
Use $cea-wechat-writer
```

如果没有自动触发，补充传入`SKILL.md`的绝对路径。

## 4. 五分钟快速上手

### 4.1 启动论文分析

论文分析工作流需要三份同步输入：

1. **论文PDF**：公式、表格、图表、脚注、复杂排版的权威依据。
2. **论文Markdown**：PDF转换而来，节省token、便于检索。
3. **论文图表目录**：从论文提取的图片，用于核对可视化内容。

推荐流程：

1. 下载论文PDF。
2. 单独导出论文图表，存放在独立文件夹。
3. 使用 [MarkItDown Online](https://markitdown.online/) 将PDF转为Markdown。
4. 向Skill传入输入时，明确指定：
   - 原始论文PDF路径
   - PDF转换后的Markdown文件路径
   - 存放论文图表的文件夹路径
5. 优先阅读Markdown版本，减少token消耗，提升查阅效率。
6. 如果Markdown转换出现公式错误、表格错乱、符号丢失等识别问题，回到原始PDF核对。
7. 生成Markdown终稿后，使用 [wemd.app](https://edit.wemd.app/) 做排版编辑，再发布公众号。

PDF始终是最终权威来源，Markdown仅作为阅读检索工具，不能替代原文。

```
Use $cea-wechat-writer to start the two‑stage paper analysis workflow.
For now, collect inputs and perform Stage 1 only. Do not begin the full paper analysis or create the final output files.
Ask me for the absolute paths to the Skill, paper PDF, paper Markdown, and paper figures, and ask where to save the result.
I may reply "default" for the save location. Begin Stage 2 only after I explicitly authorise it.
```

> 
> 中文释义：使用$cea‑wechat‑writer启动双阶段论文分析工作流。当前仅收集输入、执行第一阶段，不开展完整分析、不生成最终输出文件。向我询问Skill、论文PDF、论文Markdown、论文图表的绝对路径，以及结果保存位置。我可以回复“default”使用默认保存路径。只有收到我的明确授权后，才可启动第二阶段。

### 4.2 生成公众号稿件

```
Use $cea-wechat-writer to create a CEA WeChat Markdown draft from my source material.
First confirm the language, category, review mode, acronyms, fixed ending, and the caption decision for every figure and table.
Create only local Markdown and supporting files. Do not upload, create a WeChat platform draft, or publish.
```

> 
> 中文释义：使用$cea‑wechat‑writer基于我的素材生成CEA公众号Markdown稿件。首先确认语言、内容分类、审核模式、缩写词、固定结尾、每张图表的图注处理方案。仅生成本地Markdown及配套文件，不上传、不在公众号后台新建草稿、不执行发布。

## 5. 教程一：双阶段论文分析

### 步骤0：准备四项路径信息

准备：

1. Skill所在目录
2. 论文PDF
3. 同一论文转换得到的Markdown文件
4. 论文图表目录

结果保存位置为独立选项，不属于素材路径。若无图表目录，请回复`none`。

### 步骤1：生成论文Markdown

若无`.md`文件，前往 [MarkItDown Online](https://markitdown.online/) 转换PDF，下载到本地。

> 
> 上传未发表、受版权保护或涉密论文到第三方网站前，请确认授权。转换后的Markdown仅用于检索查阅；公式、表格、图表、脚注、复杂排版以PDF原文为准。

### 步骤2：填写输入表单

Skill首轮回复只收集输入，**不得提前开始论文分析**：

```
1. Skill目录：
2. 论文PDF：
3. 论文Markdown：
4. 论文图表目录：
5. 结果保存位置：default
```

询问论文Markdown路径的同时，需要说明：如需要可使用MarkItDown Online；上传未公开、版权受限、涉密论文到第三方网站需要确认权限；Skill不会静默上传论文。

如果Skill已经指定，Codex会回显路径，请用户确认。

### 步骤3：理解默认保存位置

当用户回复`default`：

- 保存目录为解析得到的`SKILL.md`所在目录；
- 默认输出文件：`<论文PDF文件名>_论文解读.md`、`<论文PDF文件名>_编辑核查记录.md`；
- 第一阶段不会生成结果文件；
- 如果目标文件已存在，必须询问用户重命名还是覆盖，禁止直接静默覆盖。

如果用户传入仓库根目录作为Skill目录，程序应自动定位到`<repo-root>/cea-wechat-writer/SKILL.md`，默认输出一般落在`<repo-root>/cea-wechat-writer/`。
如果希望输出到项目根目录或其他位置，请提供本机自定义绝对路径。

### 步骤4：完成第一阶段审核

第一阶段读取`SKILL.md`以及全部参考文档、模板、脚本、资源，校验PDF、Markdown、图表文件夹、两路输出路径。输出内容仅包含：

#### A. 任务说明

两份预期交付物、各论文源文件的作用、核心约束、拟定输出路径。

#### B. 拟定Markdown文稿结构

根据论文实际内容给出少量大板块，一般4‑6个二级标题。非因果识别类论文，不能强行套用DID、RCT的结构框架。

#### C. 需要用户确认的决策项

默认方案：

- 产出完整、聚焦重点的中等篇幅分析，不逐节复述原文；
- 默认中文撰写，专业术语首次出现附带英文；
- 均衡覆盖研究问题、理论、方法、证据、贡献、局限；
- 默认不额外拓展外部文献；
- 仅深度分析支撑核心结论的关键图表；
- 正文做自然转述；详细证据与判断映射放在编辑审核记录。

仍需要确认文稿语言：中文、英文、中英双语、其他语言。
选择中英双语时，确认每一个缩写的英文全称、中文译法、首次及后续出现的展示规则，再开始撰写。
选择其他语言时，确认具体语种、变体/书写体系，是单语种还是搭配中文对照。

#### D. 文件校验结果

Skill、PDF、Markdown、图表目录、两路输出路径的读取状态、格式问题、源文件一致性、输出冲突、阻塞项。

第一阶段到此停止。
以下回复**不代表授权启动第二阶段**：

- “收到”
- “继续检查”
- 继续补充文件
- 仅确认其中某一条路径

### 步骤5：显式授权启动第二阶段

接受默认方案，回复：

```
Use the default plan and start Stage 2.
```

自定义示例：

```
Use strict Chinese‑English. Focus on the theoretical mechanisms, identification strategy, and research‑design limitations.
Analyse only figures that affect the central conclusion, but do not embed images in the Markdown.
Start Stage 2 after the acronym confirmation is complete.
```

> 
> 释义：使用严格中英双语。重点分析理论机制、识别策略、研究设计局限。仅分析影响核心结论的图表，Markdown文稿不嵌入图片。缩写确认完成后启动第二阶段。

### 步骤6：接收最终论文分析文稿

最终文稿需要做到：

- 解释作者主张、研究思路、证据支撑，评估证据是否充分；
- 讲清研究问题、研究动机、研究缺口、实际贡献与局限；
- 解释公式的用途、变量、参数，以及它在论证中的作用；
- 对每张核心图表说明坐标轴、结果、作者要论证的观点、与研究问题的联系、异常点、局限；
- 报告效应方向、大小、不确定性、现实含义，不只报告统计显著性；
- 关键判断标注原文出处；
- 若存在影响理解的存疑问题，自然行文说明，细节状态写入编辑审核记录；
- 通过主语区分作者观点、论文证据、编辑判断，不用机械标签；
- 文稿中不得出现工作流标记、审核状态、提示词/Skill内部说明、碎片化模板标题。

中文分析文稿一般3000‑5000字；复杂论文若无用户许可，尽量控制在6000字以内。其他语言保持同等信息密度，不机械换算字符数。

交付消息中写明：面向读者的分析文稿路径、编辑审核记录路径、使用的源文件、未解析/存疑内容、Skill校验状态、提示词‑Skill冲突的处理方式。

## 6. 教程二：CEA公众号Markdown稿件撰写

### 步骤1：提供素材

输入可以是论文、Word文档、官方网页、会议议程、征稿通知、招聘材料、图片、用户笔记。用户笔记仅作为线索，事实部分仍需要原始/官方来源支撑。

### 步骤2：撰写前确认清单

Skill首先确认：

1. 语言：中文、英文、中英双语、其他语言；
2. 七大类内容中选定一类；
3. 普通学术审核 / 严格学术审核，是否允许风险稿件；
4. 固定结尾：默认不输出可见结尾文本，仅保留双语隐藏注释；
5. 图表图注：提取图表后，逐条列出编号、内容、拟定位置、拟定图注，确认添加、删除还是修改后添加。

中英双语模式，需要确认每个缩写的英文全称、中文译法、首次与后续出现的展示规则。
选择其他语言时，确认语种、变体/书写体系，是单语种还是搭配中文对照。

公众号稿件默认产出完整长文，不是几百字摘要；短新闻模式必须用户明确许可才启用。

### 步骤3：生成标准文章目录

```
python3 cea-wechat-writer/scripts/new_article.py \
  --output ./work/sample-article \
  --category 文章解读 \
  --language 中文 \
  --title "Working title"
```

未经明确许可，禁止直接覆盖已有非空目录。

### 步骤4：构建来源台账

事实段落使用隐藏来源锚点：

```
该研究使用2010‑2022年企业面板数据。<!-- source:S1 -->
```

在`sources.md`中对应S1条目记录来源、原文定位、支撑事实、核验状态、图片版权。
遇到来源冲突，并列展示，不私下消弭矛盾。

### 步骤5：处理图片与图注

优先使用用户提供图片、素材自带图表、官方图片。AI生成图片必须征得作者同意、没有合适原图、且确实有增益时才使用。

每张图片单独确认：

- 添加图注
- 不添加图注
- 修改后添加图注

决策记录为`user‑confirmed‑add`或`user‑confirmed‑omit`；标记为`NEEDS_REVIEW`待审核项不得进入终稿。

可见图注不带标点符号；来源写在双语隐藏注释内。表格单元格换行：单词、短标签不加标点，完整句子保留正常标点。

### 步骤6：处理固定结尾

Markdown稿件不会自动生成可见的往期回顾、CEA/JCEBS机构介绍、关注引导，只保留双语HTML注释，提示编辑从历史发布稿件复制完整结尾。

只有用户明确要求输出结尾文本，才直接使用 [`approved‑fixed‑ending‑copy.md`](cea-wechat-writer/references/approved-fixed-ending-copy.md) 的原文。

联合传播素材图片：[`扫码_搜索联合传播样式‑标准色版.png`](cea-wechat-writer/assets/brand/%E6%89%AB%E7%A0%81_%E6%90%9C%E7%B4%A2%E8%81%94%E5%90%88%E4%BC%A0%E6%92%AD%E6%A0%B7%E5%BC%8F-%E6%A0%87%E5%87%86%E8%89%B2%E7%89%88.png)。生成稿件会复制并引用该图片到`assets/扫码_搜索联合传播样式‑标准色版.png`。

### 步骤7：执行严格质量核查

```
python3 cea-wechat-writer/scripts/qa_markdown.py \
  ./work/sample-article/article.md \
  --sources ./work/sample-article/sources.md \
  --report ./work/sample-article/qa-report.md \
  --strict
```

`BLOCK=0`仅代表结构化检查未发现阻断问题，不能替代作者、编辑、学会人工审核。
还需要完成 [`qa‑policy.md`](cea-wechat-writer/references/qa-policy.md) 规定的人工语义审核；脚本无法替代事实核查、语言润色、学术判断。

### 步骤8：发布前复核

阅读`README_BEFORE_PUBLISHING.md`，核对事实、语言、图片版权、二维码、隐藏注释、固定结尾、公众号编辑器实际排版效果。

## 7. CEA强制写作与排版规范

### 7.1 事实与学术表述

- 数字、日期、作者、机构、身份、样本量、期刊指标、研究结论、会议信息、截止日期，必须标注来源。
- 不要把相关关系表述为因果关系。
- 不要将单篇论文结论当作学界共识。
- 不夸大稳健性、外部有效性、政策含义。
- 无法核实的事实保留风险提示，禁止主观脑补填补信息。

### 7.2 语言与缩写

- 每一次任务都要确认输出语言。
- 中英双语指完整平行对照文本，不是英文摘要。
- 即便是常见缩写，也需要交互确认。
- 选定中文后，行文自然通顺；专业术语首次出现写“中文（英文）”，后续遵循确认好的展示规则。

### 7.3 编辑指令

所有作者、编辑操作提示必须是双语HTML注释，不能出现在正文可见文本：

```
<!-- 请在公众号编辑器内补入固定结尾 / Add the fixed ending in the WeChat editor -->
```

### 7.4 干净终稿要求

- 面向读者的正文，不能出现工作流标记、审核状态、提示词/Skill注释、写作流程说明。
- 区分作者观点、论文证据、编辑判断，依靠上下文主语体现，不使用“分析师判断”这类机械标签。
- 只有主题发生实质变化才设置标题；单段式小节、堆砌列表、过度加粗、重复摘要需要合并或删除。
- 审核状态、来源映射、冲突、待核实问题全部放在配套审核文件。

完整规则参见 [`natural‑writing‑and‑clean‑copy.md`](cea-wechat-writer/references/natural-writing-and-clean-copy.md)。

## 8. 七大内容分类与五类模板

| 内容分类 | 默认模板 | 核心内容 |
| --- | --- | --- |
| 文章解读 | 研究解读模板 | 研究问题、方法、结论、机制、研究边界 |
| 学术前沿 | 方法前沿模板 | 方法、模型、文献脉络、局限 |
| 会议通知 | 通知/机会模板 | 时间、地点、议程、注册、投稿信息 |
| 行业资讯 | 资讯摘要模板 | 事件、人物、机构进展、意义 |
| 学会历史 | 历史/人物专题模板 | 回忆、机构发展、档案资料 |
| 特刊征稿 | 通知/机会模板 | 主题、征稿范围、编委、截止时间、投稿要求 |
| 人才招聘 | 通知/机会模板 | 岗位、领域、任职要求、材料、联系方式 |

详细映射参见 [`category‑and‑template‑guide.md`](cea-wechat-writer/references/category-and-template-guide.md)。

## 9. 训练数据与历史语料库

### 9.1 历史HTML素材

- 爬虫脚本：[`training_data/craw.py`](training_data/craw.py)
- 爬取输出目录：[`training_data/train_by_category_html/`](training_data/train_by_category_html/)

历史HTML用于学习分类、行文结构、段落节奏、品牌元素、排版习惯。乱码、结构损坏的内容不能拿来提取事实。

### 9.2 世经系列素材

- [`training_data/train_by_Shijie_Word/`](training_data/train_by_Shijie_Word/)

Word/PDF素材用于学习语言、措辞、术语、结构、排版。邮件接收不代表获得公开复用权限，仍要审核版权与个人信息。

### 9.3 训练策略

本项目优先完善Skill、模板、检索、质检，暂不直接对基础模型做微调。推荐路径：

1. 使用Skill生成初稿；
2. 记录作者修改内容与修改理由；
3. 用户明确要求归档时，才保存“初稿‑终稿”配对样本；
4. 维护固定评估集；
5. 在数据规模、一致性、授权全部到位后，再评估微调方案。

详见 [`training‑strategy.md`](cea-wechat-writer/references/training-strategy.md)。

## 10. 脚本、示例与校验

### 10.1 主要脚本

| 脚本 | 用途 |
| --- | --- |
| `new_article.py` | 创建标准公众号文章目录 |
| `retrieve_examples.py` | 根据分类、主题检索历史可用示例 |
| `qa_markdown.py` | 来源、图片、占位符、阻断状态质检 |
| `build_corpus.py` | 重建历史语料索引 |
| `archive_revision.py` | 用户明确归档请求时，保存稿件修改前后对照 |

检索示例：

```
python3 cea-wechat-writer/scripts/retrieve_examples.py \
  --corpus cea-wechat-writer/references/corpus/index.json \
  --category 文章解读 \
  --query "research topic or title" \
  --limit 3
```

检索返回不足3条，不要跨分类凑数，不要使用乱码损坏文本，依靠正式模板与质量规则输出。

### 10.2 七套示例文稿

完整示例放在 [`cea-wechat-writer/sample/`](cea-wechat-writer/sample/)，覆盖全部七大类。历史会议、特刊、招聘示例仅展示结构，不可直接当作现行通知发布。

### 10.3 Skill校验

本地Codex具备`skill‑creator`校验工具时运行：

```
CEA_SKILL_CREATOR_ROOT="/path/to/skill-creator"
python3 "${CEA_SKILL_CREATOR_ROOT}/scripts/quick_validate.py" \
  ./cea-wechat-writer
```

路径为示例，替换成本机真实`skill‑creator`与仓库路径。
`quick_validate.py`依赖Python与PyYAML。公众号示例文稿还需要单独运行`qa_markdown.py --strict`。

### 10.4 对比源文件与已安装版本

```
CEA_REPO_ROOT="/path/to/CEA_Skill"
CEA_CODEX_SKILLS_ROOT="/path/to/.codex/skills"
diff -qr \
  --exclude='.DS_Store' \
  --exclude='__pycache__' \
  "${CEA_REPO_ROOT}/cea-wechat-writer" \
  "${CEA_CODEX_SKILLS_ROOT}/cea-wechat-writer"
```

无输出代表两份目录除排除文件外完全一致。

## 11. 输出文件与发布边界

公众号模式标准输出：

- `article.md`：排版完成正文稿件
- `sources.md`：事实与图片来源台账
- `qa‑report.md`：自动化与人工审核状态
- `README_BEFORE_PUBLISHING.md`：双语发布前核对清单
- `assets/`：实际使用的本地图片

论文分析模式一般输出两份Markdown：面向读者的分析文稿，一份供作者编辑查阅的审核记录。

两种模式均不会自动上传或发布。公众号编辑器内仍需要人工完成：

1. 手动添加往期回顾、官方固定结尾；
2. 核对图片尺寸、版权、人物肖像授权；
3. 检查二维码、链接有效性；
4. 确认HTML注释不会暴露在预览页面；
5. 最终预览校验。

## 12. 故障排查

### Skill没有触发

显式输入`$cea‑wechat‑writer`，补充传入`cea‑wechat‑writer/SKILL.md`绝对路径。

### 缺少论文Markdown文件

前往 [MarkItDown Online](https://markitdown.online/) 转换下载。敏感论文上传第三方前确认权限。

### PDF与Markdown内容不一致

以PDF为准。关键内容不一致会阻塞第二阶段，需要重新转换或提供正确文件。

### 没有图表目录

回复`none`，确认是否允许直接从PDF查看/提取图表。

### 默认输出文件已存在

Skill必须询问重命名还是覆盖，推荐使用版本后缀如`_v2.md`。

### QA报告BLOCK阻断项

阅读`qa‑report.md`，解决来源、语言、图片、图注、编辑指令、固定结尾问题。只有用户明确接受特定风险，才允许绕过阻断；同时在`qa‑report.md`和`sources.md`记录`USER_OVERRIDE`、风险内容、操作人备注、时间。

### HTML注释出现在公众号预览

停止发布，排查编辑器是否转义HTML注释，再次预览渲染效果。

## 13. 资料来源与版权说明

本项目参考：

- [`ref‑duyi‑wechat‑skill‑suite‑main/`](ref-duyi-wechat-skill-suite-main/)

训练分析素材包含：

- [`training_data/craw.py`](training_data/craw.py)
- [`training_data/train_by_category_html/`](training_data/train_by_category_html/)
- [`training_data/train_by_Shijie_Word/`](training_data/train_by_Shijie_Word/)

以上素材用于内容分类、语言训练、结构分析、模板开发、质量规则制定。历史素材中的动态事实、图片版权、联系方式、职务信息、时效内容，不能直接当作现行有效信息。

**CEA保留本项目、Skill及相关文档的全部解释权。**

---

[阅读中文默认项目说明](README.md)
