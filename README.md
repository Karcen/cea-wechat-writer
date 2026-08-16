# CEA_Skill 项目说明与使用教程

**文档语言：中文（默认）｜[English documentation](README_EN.md)**

> “默认中文”只表示项目首页默认显示中文。生成内容的语言仍必须在每次任务中确认，可选择中文、英文、严格中英文或其他语言。

本目录保存全英／全欧中国经济学会（Chinese Economic Association UK/Europe，CEA）的公众号写作与研究级论文解读工作流，包括可安装的 Codex Skill、历史训练语料、参考排版 Skill、品牌图片和完整样例。

实际可调用的 Skill 位于 [`cea-wechat-writer/`](cea-wechat-writer/)。

## 目录

- [1. 项目能做什么](#1-项目能做什么)
- [2. 项目目录说明](#2-项目目录说明)
- [3. 安装或更新 Skill](#3-安装或更新-skill)
- [4. 五分钟快速开始](#4-五分钟快速开始)
- [5. 教程一：两阶段研究级论文解读](#5-教程一两阶段研究级论文解读)
- [6. 教程二：CEA 公众号 Markdown 初稿](#6-教程二cea-公众号-markdown-初稿)
- [7. CEA 写作与排版硬规则](#7-cea-写作与排版硬规则)
- [8. 七个栏目与五套模板](#8-七个栏目与五套模板)
- [9. 训练数据与历史语料](#9-训练数据与历史语料)
- [10. 脚本、样例与验证](#10-脚本样例与验证)
- [11. 输出文件与发布边界](#11-输出文件与发布边界)
- [12. 常见问题](#12-常见问题)
- [13. 来源与权利说明](#13-来源与权利说明)

## 1. 项目能做什么

项目支持两种独立模式：

| 模式 | 主要用途 | 默认结果 |
|---|---|---|
| CEA 公众号写作 | 论文解读、方法介绍、会议、新闻、历史、特刊、招聘 | 本地公众号 Markdown 初稿及配套来源、QA、发表前说明和图片 |
| 研究级论文解读 | 阅读笔记、文献综述素材、理论与方法拆解、证据评价 | 用户确认路径中的一份研究级 Markdown |

如果请求只写“论文解读”，Skill 会先询问需要“公众号文章”还是“研究级阅读笔记”，不会默认混合两种结构。

### 1.1 公众号写作模式

公众号模式强调：

- CEA 品牌语气与五套稳定模板；
- 原文或官方网页支持的重要事实；
- `sources.md` 中的来源台账；
- 本地图片、隐藏来源批注和逐图图注确认；
- 严格 QA 和中英文发表前检查；
- 微信编辑器内仍需人工完成的步骤。

### 1.2 研究级论文解读模式

研究级模式强调：

- 同时使用 PDF、转换后的 Markdown 和 figures；
- 强制分为“阶段 1 需求对齐”和“阶段 2 正式解读”；
- 区分作者陈述、证据直接支持、作者解释和分析者评价；
- 对理论、方法、数据、结果、图表、贡献与局限进行研究级拆解；
- 将关键判断定位到 Section、Figure、Table、Equation、Appendix 或 PDF 页码；
- 不把深度解读压缩成简单摘要。

## 2. 项目目录说明

```text
CEA_Skill/
├── README.md                       中文默认项目教程
├── README_EN.md                    English project guide
├── cea-wechat-writer/              可安装和调用的 Skill
│   ├── SKILL.md                    执行规则入口
│   ├── README.md                   Skill 中文完整教程
│   ├── README_EN.md                Skill English tutorial
│   ├── agents/openai.yaml          Codex 界面元数据与默认 Prompt
│   ├── assets/                     模板、Prompt 与品牌资产
│   ├── references/                 证据、语言、图片、QA 等详细规则
│   ├── sample/                     七个栏目样例
│   └── scripts/                    创建、检索、检查和归档脚本
├── training_data/                  历史 HTML 与 Shijie Word/PDF 材料
├── ref-duyi-wechat-skill-suite-main/ 参考排版 Skill
└── QR_code-png/                    CEA 二维码与联合传播图片
```

重要入口：

- [Skill 执行规则](cea-wechat-writer/SKILL.md)
- [Skill 中文完整教程](cea-wechat-writer/README.md)
- [Skill English tutorial](cea-wechat-writer/README_EN.md)
- [研究级论文解读工作流](cea-wechat-writer/references/research-paper-analysis-workflow.md)
- [研究级论文解读启动 Prompt](cea-wechat-writer/assets/prompts/START_RESEARCH_PAPER_ANALYSIS.md)
- [七个公众号样例](cea-wechat-writer/sample/)

`CEA_Work_Test/` 等工作目录不属于安装包，不应随 Skill 一起同步到 Codex skills 目录。

## 3. 安装或更新 Skill

### 3.1 通用路径写法

本 README 面向 GitHub 团队共享，不绑定任何成员的用户名或本机目录。下文统一使用以下示例占位符：

| 占位符 | 含义 | 示例 |
|---|---|---|
| `<repo-root>` | 克隆后的项目根目录 | `/path/to/CEA_Skill` |
| `<skill-root>` | 实际包含 `SKILL.md` 的目录 | `/path/to/CEA_Skill/cea-wechat-writer` |
| `<codex-skills-directory>` | 本机 Codex Skills 目录 | `/path/to/.codex/skills` |

仓库内部的文档链接和命令优先使用相对路径。只有在启动实际任务、填写论文材料地址或指定输出目录时，才应替换为当前使用者本机的真实绝对路径。

除非命令另有说明，下文所有仓库相对命令均从 `<repo-root>` 运行。

### 3.2 同步到 Codex

```bash
CEA_REPO_ROOT="/path/to/CEA_Skill"
CEA_CODEX_SKILLS_ROOT="/path/to/.codex/skills"

mkdir -p "${CEA_CODEX_SKILLS_ROOT}/cea-wechat-writer"
rsync -a \
  --exclude '.DS_Store' \
  --exclude '__pycache__' \
  "${CEA_REPO_ROOT}/cea-wechat-writer/" \
  "${CEA_CODEX_SKILLS_ROOT}/cea-wechat-writer/"
```

先把两个 `/path/to/...` 示例值替换为当前电脑上的实际目录，再运行命令。

该命令没有使用 `--delete`，不会主动删除安装目录中的额外文件。同步后建议新建任务或重新打开任务，使 Codex 重新载入 Skill。

### 3.3 确认安装

应能找到：

```text
<codex-skills-directory>/cea-wechat-writer/SKILL.md
```

在任务中使用：

```text
使用 $cea-wechat-writer
```

如果未自动触发，可同时提供 `SKILL.md` 的绝对路径。

## 4. 五分钟快速开始

### 4.1 启动研究级论文解读

```text
使用 $cea-wechat-writer 启动“两阶段研究级论文解读”工作流。
现在只收集输入并执行阶段 1，不得开始完整论文解读或生成最终 Markdown。
请向我询问 Skill、论文 PDF、论文 Markdown、论文 figures 四个绝对路径，以及结果保存位置。
保存位置可以回复“默认”；只有我明确说“开始阶段 2”后才能正式解读和保存。
```

### 4.2 启动公众号初稿

```text
使用 $cea-wechat-writer，根据我提供的材料生成 CEA 公众号 Markdown 初稿。
先确认语言、栏目、审核方式、缩写、固定结尾和每个图表的图注选择。
只生成本地 Markdown 与配套资料，不上传、不创建公众号草稿箱、不发布。
```

## 5. 教程一：两阶段研究级论文解读

### 第 0 步：准备四个地址

用户需要准备：

1. Skill 目录；
2. 论文 PDF；
3. 由同一论文转换得到的 Markdown；
4. 论文 figures 目录。

结果保存位置是额外选择，不算第五个材料地址。没有 figures 时可以回复“无”。

### 第 1 步：生成论文 Markdown

如果还没有 `.md` 文件，可以使用 [MarkItDown Online](https://markitdown.online/) 将 PDF 转换为 Markdown，然后下载到本地。

> 未公开、受版权保护或涉及保密限制的论文，在上传第三方网站前必须确认授权。转换后的 Markdown 只用于检索与定位，公式、表格、图表、脚注和复杂排版仍以 PDF 为准。

### 第 2 步：填写输入表

Skill 的首轮回复应只询问输入，不应提前解释论文：

```text
1. Skill 目录：
2. 论文 PDF：
3. 论文 Markdown：
4. 论文 figures 目录：
5. 结果保存位置：默认
```

询问论文 Markdown 路径时，必须同时提示：若尚未生成，可使用 [MarkItDown Online](https://markitdown.online/) 转换；未公开、受版权或保密限制的论文，上传第三方网站前先确认授权。不得替用户静默上传。

如果已明确指定 Skill，Codex 可以回显路径并请用户确认。

### 第 3 步：理解默认保存位置

当用户回复“默认”时：

- 保存目录是实际解析到的 `SKILL.md` 所在目录；
- 默认文件名是 `<论文PDF文件名去除扩展名>_研究级论文解读.md`；
- 阶段 1 不创建文件；
- 已有同名文件时必须询问，不得静默覆盖。

如果用户把项目根目录 `<repo-root>` 作为 Skill 路径，系统仍应定位到 `<repo-root>/cea-wechat-writer/SKILL.md`；因此“默认保存”通常落在 `<repo-root>/cea-wechat-writer/`。若希望保存在项目根目录或其他位置，请提供当前电脑上的自定义绝对路径。

### 第 4 步：查看阶段 1

阶段 1 必须完整读取 `SKILL.md` 及其指定的 references、templates、scripts 和 assets，并检查 PDF、Markdown、figures 与输出路径。回复只包含：

#### A. 对任务的理解

说明最终产出、三类论文材料的用途、核心约束和拟保存路径。

#### B. 预定 Markdown 结构

按论文实际研究类型列出一级和二级标题，不强行给非因果研究套用 DID/RCT 结构。

#### C. 需要确认的事项

默认建议：

- 研究级完整拆解；
- 中文为主，专业术语首次出现时保留英文；
- 平衡覆盖问题、理论、方法、证据、贡献与局限；
- 默认不扩展外部文献；
- 逐图分析核心图表；
- 分析者评价单独标记。

语言仍须明确选择中文、英文、中英文或其他。选择中英文时，在正文前确认全部缩写的英文全称、中文译名和首次及后续展示规则；选择“其他”时，确认具体语言、地区变体或文字体系，以及单语还是与中文并列。

#### D. 文件检查结果

报告 Skill、PDF、Markdown、figures 和输出路径的读取状态、格式异常、内容对应关系与阻断项。

阶段 1 完成后必须停止。以下回复不构成阶段 2 授权：

- “收到”；
- “继续检查”；
- 再提供一个文件；
- 仅确认某个路径。

### 第 5 步：明确授权阶段 2

采用默认方案时回复：

```text
按默认方案，开始阶段 2。
```

定制示例：

```text
选择严格中英文，重点关注理论机制、识别策略和研究设计局限。
核心图表逐图分析，但不在 Markdown 中嵌入图片。
完成缩写确认后开始阶段 2。
```

### 第 6 步：验收最终论文解读

最终文档应做到：

- 说明作者说了什么、为什么这样做、如何证明以及证据是否足够；
- 解释研究问题、动机、缺口、实际贡献和限制；
- 公式说明用途、变量、参数和论证作用；
- 图表说明坐标、结果、作者论点、研究问题联系、异常与限制；
- 结果说明方向、大小、不确定性与现实意义，而非只写“显著”；
- 重要判断提供原文定位；
- 无法核实的内容标记为“论文中无法确认”；
- 作者观点与分析者评价清楚分开。

中文输出的标准实证或理论论文通常约为 5,000—10,000 个中文字符；其他语言保持相当研究深度，不机械套用中文字符数。

交付说明应列出输出完整路径、使用的源文件、无法解析或确认的内容、Skill 检查状态，以及 Prompt 与 Skill 冲突的处理方式。

## 6. 教程二：CEA 公众号 Markdown 初稿

### 第 1 步：提供材料

可提供论文、Word、官方网页、会议议程、征稿启事、招聘材料、图片和用户笔记。用户笔记只作为线索，重要事实仍须原文或官方网页支持。

### 第 2 步：完成写作前确认

Skill 必须先确认：

1. 语言：中文、英文、中英文或其他；
2. 栏目：七个栏目之一；
3. 审核方式：常规或严格学术审核，以及是否允许带风险生成；
4. 固定结尾：默认不生成可见正文，只保留中英文隐藏复制提示；
5. 图表图注：提取并选定图表后，逐项列出编号、内容、建议位置和建议图注，再确认添加、不添加或修改后添加。

中英文模式还必须确认全部缩写的英文全称、中文译名和首次及后续展示规则。

选择“其他”时，继续确认具体语言、地区变体或文字体系，以及单语还是与中文并列。

公众号正文默认生成完整长文，不得写成数百字摘要；只有用户明确同意时才使用短讯模式。

### 第 3 步：创建标准目录

```bash
python3 cea-wechat-writer/scripts/new_article.py \
  --output ./work/sample-article \
  --category 文章解读 \
  --language 中文 \
  --title "暂定标题"
```

不得覆盖已有非空目录，除非用户明确授权。

### 第 4 步：建立来源台账

重要事实段落使用隐藏来源锚点：

```markdown
该研究使用2010—2022年的企业面板数据。<!-- source:S1 -->
```

`sources.md` 中的 `S1` 应说明来源、原文定位、支持事实、核验状态和图片权利。来源冲突并列披露，不擅自选择。

### 第 5 步：处理图片和图注

图片优先使用用户图片、原始材料图表和官方图片。AI 图片只有在作者同意、缺少合适原图且确有价值时使用。

每个图表都要单独确认图注：

- 添加图注；
- 不添加图注；
- 修改后添加。

确认结果分别记录为 `user-confirmed-add` 或 `user-confirmed-omit`；未确认的 `NEEDS_REVIEW` 不得进入成稿。

可见图注不使用任何标点，来源放在中英文隐藏注释中。表格单元格换行时，单个词和短标签不加标点，完整句子保留正常标点。

### 第 6 步：处理固定结尾

Markdown 默认不生成“往期精彩文章”、CEA/JCEBS 介绍和关注提示正文，只用中英文 HTML 注释提醒编辑从已发布文章复制。

用户明确要求写入时，必须逐字使用 [`approved-fixed-ending-copy.md`](cea-wechat-writer/references/approved-fixed-ending-copy.md)。

Skill 内的联合传播源资产是 [`扫码_搜索联合传播样式-标准色版.png`](cea-wechat-writer/assets/brand/扫码_搜索联合传播样式-标准色版.png)，生成稿中复制并引用为 `assets/扫码_搜索联合传播样式-标准色版.png`。

### 第 7 步：运行严格 QA

```bash
python3 cea-wechat-writer/scripts/qa_markdown.py \
  ./work/sample-article/article.md \
  --sources ./work/sample-article/sources.md \
  --report ./work/sample-article/qa-report.md \
  --strict
```

`BLOCK=0` 只表示结构化检查没有发现阻断项，不能替代作者、编辑和学会审核。

同时按 [`qa-policy.md`](cea-wechat-writer/references/qa-policy.md) 完成人工语义检查；脚本不能替代事实核验、语法审校和学术判断。

### 第 8 步：发表前复核

阅读 `README_BEFORE_PUBLISHING.md`，检查事实、语言、图片权利、二维码、隐藏注释、固定结尾和微信编辑器实际排版。

## 7. CEA 写作与排版硬规则

### 7.1 事实与科学语言

- 数字、日期、作者、机构、职务、样本量、期刊指标、研究结论、会议信息和截止日期必须有来源；
- 不把相关性写成因果性；
- 不把单篇论文写成学界共识；
- 不夸大稳健性、外部效度和政策意义；
- 无法核实的信息必须保留风险，不能自行补全。

### 7.2 语言与缩写

- 每次任务都确认语言；
- 中英文必须是严格平行全文，不是英文摘要；
- 常见缩写也不能跳过交互确认；
- 选择中文后采用自然中文表达；专业术语首次出现使用“中文（English）”，后文按确认规则处理。

### 7.3 提示文字

任何作者或编辑提示只能写成中英文 HTML 注释，不得显示在正文中：

```markdown
<!-- 请在公众号编辑器内补入固定结尾 / Add the fixed ending in the WeChat editor -->
```

## 8. 七个栏目与五套模板

| 栏目 | 默认模板 | 核心内容 |
|---|---|---|
| 文章解读 | 研究解读 | 问题、方法、结果、机制与边界 |
| 学术前沿 | 方法前沿 | 方法、模型、文献脉络与限制 |
| 会议通知 | 通知机会 | 时间、地点、议程、报名或投稿 |
| 新近动态 | 新闻回顾 | 活动、人物、组织进展与意义 |
| 学会历史 | 历史人物 | 人物回忆、组织沿革与档案 |
| 特刊推荐 | 通知机会 | 主题、范围、编辑、期限与要求 |
| 广纳英才 | 通知机会 | 岗位、方向、资格、材料与联系方式 |

详细映射见 [`category-and-template-guide.md`](cea-wechat-writer/references/category-and-template-guide.md)。

## 9. 训练数据与历史语料

### 9.1 历史 HTML

- 爬虫：[`training_data/craw.py`](training_data/craw.py)
- 爬取结果：[`training_data/train_by_category_html/`](training_data/train_by_category_html/)

历史 HTML 用于提炼栏目、结构、段落节奏、品牌元素和排版习惯。乱码或结构退化内容不得作为正文事实来源。

### 9.2 Shijie 材料

- [`training_data/train_by_Shijie_Word/`](training_data/train_by_Shijie_Word/)

这些 Word/PDF 材料用于语言、写作、术语、结构和排版训练。邮件材料不自动等于公开授权，涉及版权或个人信息时仍须审查。

### 9.3 训练策略

当前项目首先采用 Skill、模板、检索和 QA，而不是直接微调基础模型。推荐流程为：

1. Skill 生成初稿；
2. 作者修改并记录理由；
3. 仅在用户明确要求归档时保存生成稿与终稿；
4. 建立固定测试集；
5. 数据量、一致性和授权条件满足后再评估微调。

详细路线见 [`training-strategy.md`](cea-wechat-writer/references/training-strategy.md)。

## 10. 脚本、样例与验证

### 10.1 主要脚本

| 脚本 | 用途 |
|---|---|
| `new_article.py` | 创建标准公众号稿件目录 |
| `retrieve_examples.py` | 按栏目和主题检索可用历史样例 |
| `qa_markdown.py` | 检查来源、图片、占位符与阻断状态 |
| `build_corpus.py` | 重建历史语料索引 |
| `archive_revision.py` | 仅在用户明确要求归档时保存修改对 |

检索示例：

```bash
python3 cea-wechat-writer/scripts/retrieve_examples.py \
  --corpus cea-wechat-writer/references/corpus/index.json \
  --category 文章解读 \
  --query "研究主题或标题" \
  --limit 3
```

默认检索不足 3 篇时，不跨栏目补足，也不使用 `degraded_mojibake` 正文；直接依靠正式模板与质量规范。

### 10.2 七个样例

完整样例位于 [`cea-wechat-writer/sample/`](cea-wechat-writer/sample/)，覆盖七个栏目。历史会议、特刊和招聘样例只用于展示结构，不能当作当前通知发布。

### 10.3 验证 Skill

如本机存在 Codex 的 `skill-creator` 校验脚本，可运行：

```bash
CEA_SKILL_CREATOR_ROOT="/path/to/skill-creator"

python3 "${CEA_SKILL_CREATOR_ROOT}/scripts/quick_validate.py" \
  ./cea-wechat-writer
```

以上路径仅为示例；请替换为当前环境中 `skill-creator` 和本仓库的实际路径。`quick_validate.py` 需要 Python 与 PyYAML。公众号样例还应使用 `qa_markdown.py --strict` 逐一检查。

### 10.4 检查源目录与安装目录

```bash
CEA_REPO_ROOT="/path/to/CEA_Skill"
CEA_CODEX_SKILLS_ROOT="/path/to/.codex/skills"

diff -qr \
  --exclude='.DS_Store' \
  --exclude='__pycache__' \
  "${CEA_REPO_ROOT}/cea-wechat-writer" \
  "${CEA_CODEX_SKILLS_ROOT}/cea-wechat-writer"
```

无输出表示除排除项外两份目录一致。

## 11. 输出文件与发布边界

公众号模式标准输出：

- `article.md`：排版后的正文初稿；
- `sources.md`：事实与图片来源台账；
- `qa-report.md`：自动检查和人工复核状态；
- `README_BEFORE_PUBLISHING.md`：中英文发表前说明；
- `assets/`：实际使用的本地图片。

研究级论文解读模式默认输出一份 Markdown 到用户确认路径。

任何模式都不会自动上传或发布。公众号稿件仍须在微信编辑器内：

1. 手动添加往期精彩文章和核准固定结尾；
2. 检查图片尺寸、版权和人物授权；
3. 检查二维码和链接；
4. 确认 HTML 注释未显示；
5. 进行最终视觉预览。

## 12. 常见问题

### Skill 没有触发

在任务中明确写 `$cea-wechat-writer`，并提供 `cea-wechat-writer/SKILL.md` 的绝对路径。

### 没有论文 Markdown

使用 [MarkItDown Online](https://markitdown.online/) 转换并下载到本地。敏感论文先确认第三方上传权限。

### PDF 和 Markdown 不一致

以 PDF 为准。明显不一致会阻止进入阶段 2，应先重新转换或提供正确文件。

### 没有 figures

回复“无”，再确认是否允许直接从 PDF 核对或提取图表。

### 默认输出已存在

Skill 必须先询问改名或覆盖。建议使用 `_v2.md` 等版本后缀。

### QA 出现 BLOCK

阅读 `qa-report.md`，修复来源、语言、图片、图注、提示或固定结尾问题。仅在用户明确接受具体风险时强制通过；`qa-report.md` 和 `sources.md` 必须同时保留 `USER_OVERRIDE`、风险、操作者说明与时间。

### 注释在公众号预览中显示

停止发布，检查 HTML 注释是否被编辑器转换，并重新进行渲染预览。

## 13. 来源与权利说明

本项目参考：

- [`ref-duyi-wechat-skill-suite-main/`](ref-duyi-wechat-skill-suite-main/)

训练与分析材料包括：

- [`training_data/craw.py`](training_data/craw.py)
- [`training_data/train_by_category_html/`](training_data/train_by_category_html/)
- [`training_data/train_by_Shijie_Word/`](training_data/train_by_Shijie_Word/)

以上材料用于栏目归纳、语言训练、结构分析、模板提炼、排版学习和质量检查规则建设。历史材料中的动态事实、图片权利、联系方式、人物职务和时效信息不能直接视为当前有效信息。

**本项目、Skill 及相关说明的全部解释权归 CEA 所有。**

---

[Read this project guide in English](README_EN.md)
