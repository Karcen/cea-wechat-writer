---
name: cea-wechat-writer
description: 为全英/全欧中国经济学会（CEA）撰写、核查并排版公众号 Markdown 初稿，也支持基于论文 PDF、对应 Markdown 和 figures 目录开展两阶段研究级论文解读。用于生成七类 CEA 公众号稿件，或制作可作为阅读笔记、文献综述素材和后续研究参考的深度 Markdown；自动建立证据映射、解释理论与方法、核对图表公式、区分作者结论与分析者评价，并执行科学语言与质量检查。只生成本地文件，不创建公众号草稿或正式发布。
---

# CEA 公众号写作与研究级论文解读

把原始材料转换为可审阅的 CEA 公众号 Markdown 初稿，或转换为研究级论文解读笔记。将 CEA 历史语料用于结构、语气和排版示范，不把旧文章中的时间敏感事实当作当前事实。

执行命令前，先把包含本 `SKILL.md` 的目录解析为 skill 根目录；下文的 `scripts/`、`references/` 和 `assets/` 都相对于该目录。

## 模式路由

先根据用户要求选择一种模式，不得混用交付边界：

- **公众号写作模式**：用户要求公众号推文、七类栏目、微信排版、`article.md`、来源台账或发布前检查时，执行下文“公众号写作模式”流程。
- **研究级论文解读模式**：用户要求系统解读论文、研究级阅读笔记、文献综述素材，或同时提供论文 PDF、Markdown 和 figures 时，必须完整读取 `references/research-paper-analysis-workflow.md`，并使用 `assets/templates/research-paper-analysis.md` 作为可调整的结构基线。
- 用户只说“论文解读”且交付用途不明确时，询问要“公众号文章”还是“研究级阅读笔记”。不得同时生成两种成品，除非用户明确要求。

研究级论文解读必须遵守两阶段闸门：

1. 启动时一次性询问四个绝对路径：Skill 目录、论文 PDF、论文 Markdown、论文 figures 目录。若当前 Skill 路径已由用户明确提供，可以回显并请用户确认，不要求重复粘贴。
2. 另行询问结果保存位置。用户可以给出自定义绝对路径，也可以回复“默认”；默认保存目录是**实际解析到的 `SKILL.md` 所在目录**，默认文件名为 `<论文PDF文件名去除扩展名>_研究级论文解读.md`。用户确认保存位置前不得写文件；已有同名文件时不得覆盖，必须先询问。
3. 询问 Markdown 路径时同时提示：若尚未生成，可在 [MarkItDown Online](https://markitdown.online/) 将 PDF 转换为 Markdown，下载到本地后再提供绝对路径；对未公开、受版权或保密限制的论文，上传第三方网站前先确认授权。不得替用户静默上传。
4. 收齐输入后只执行阶段 1：读取规则、检查文件、提出结构、列出真正需要确认的事项，然后停止。用户仅提供路径、回复“收到”或补充资料，不等于授权阶段 2。
5. 只有用户明确回复“开始阶段 2”“可以开始”或同等授权，并确认阶段 1 的必要选择后，才能进行完整分析和保存最终 Markdown。

可复制的中英文启动提示词见 `assets/prompts/START_RESEARCH_PAPER_ANALYSIS.md`。

## 公众号写作模式

### 硬边界

- 只交付本地 `article.md`、`sources.md`、`qa-report.md`、`README_BEFORE_PUBLISHING.md` 和 `assets/`；不上传公众号、不创建草稿箱、不群发。
- 重要事实只能来自用户提供的原始材料或官方网页。重要事实包括数字、日期、样本量、作者身份、单位职务、会议地点、截止日期、期刊指标、研究发现和因果结论。
- 不根据常识补造缺失事实。原文与官方来源冲突时并列记录冲突，不擅自选择。
- 不把相关性写成因果性，不把单篇研究写成学界共识，不夸大稳健性、外部效度或政策含义。
- 允许用户强制通过检查项，但必须在 `qa-report.md` 和 `sources.md` 保留 `USER_OVERRIDE`、风险、操作者说明与时间；不得静默删除风险。
- AI 图片仅在缺少可用原图且确有阅读价值时使用。优先使用用户图片、原始材料图表和官方图片。

### 开始前必须询问

在写正文之前先询问并记录以下选择：

1. **写作语言**：必须让用户在“中文、英文、中英文、其他”中明确选择，不得自行假定。选择“其他”时继续询问具体语言、地区变体/文字体系，以及是单语还是与中文并列。
2. **栏目**：让用户指定，或先推荐栏目再请用户确认。支持七个栏目。
3. **审核方式**：常规审核或严格学术审核；是否允许带风险生成。默认严格学术审核。
4. **固定结尾**：Markdown 初稿不生成往期精彩文章、CEA/JCEBS介绍或关注提示；仅用中英文 HTML 注释提醒编辑从已发布的往期文章复制完整结尾。
5. **图表图注**：提取并选定图表后，逐项列出编号、内容、建议位置和建议图注，让用户对每一项选择“添加图注”“不添加图注”或“修改后添加”。不得默认统一添加或省略。

选择“中英文”后，在写正文前扫描全部材料中的缩写，并用表格向用户集中确认“缩写、英文全称、中文译名、首次及后续展示规则”。包括 CEA、JCEBS、ESG、AI 等常见缩写；不得因其常见而跳过。用户确认前不得起草正文；写作中出现新缩写时暂停并继续确认。完整规则见 `references/language-and-abbreviation-policy.md`。

如果用户已在同一请求中明确给出某项选择，不重复询问。栏目不明确时读取 `references/category-and-template-guide.md`。

### 生产流程

#### 1. 建立工作目录

用脚本生成标准目录：

```bash
python3 scripts/new_article.py \
  --output /absolute/path/to/output \
  --category 文章解读 \
  --language 中文 \
  --title "暂定标题"
```

不要覆盖已有目录，除非用户明确授权。

#### 2. 读取原始材料

- PDF：读取完整论文及图表、脚注、附录和元数据；长论文至少覆盖摘要、研究设计、核心表图、稳健性、局限和结论。
- DOCX：读取正文、表格、图片顺序和批注；Word 样式只作为参考，不把视觉样式误当语义。
- 网页：优先官方来源。保存页面标题、机构、发布日期、访问日期和 URL。
- 零散笔记：把它们视为线索，不视为已核实事实。

将每个来源登记进 `sources.md`，遵循 `references/evidence-and-sources.md`。

#### 3. 选择示例与模板

先读取 `references/category-and-template-guide.md`，再按栏目从五套模板中选择。需要语料示例时运行：

```bash
python3 scripts/retrieve_examples.py \
  --corpus references/corpus/index.json \
  --category 文章解读 \
  --query "研究主题或标题" \
  --limit 3
```

只借鉴示例的结构、段落节奏、术语处理和 CEA 语气。不得复制示例中的研究事实、作者信息、期刊指标、会议信息或图片权利声明。
如果默认检索返回不足 3 篇，不得为了凑数而跨栏目或使用 `degraded_mojibake` 正文；直接依靠正式模板和质量规范。

#### 4. 建立证据地图

写正文前列出：

- 可核实事实及来源编号；
- 研究问题、方法、样本、主要结果、异质性、稳健性、限制；
- 待确认项和来源冲突；
- 可用图片、图表含义、版权状态和建议位置。
- 每个拟用图表的图注建议及用户逐项确认结果。
- 用户确认的语言选项；中英文模式还要记录经用户确认的缩写表。

正文中的重要事实段落后添加隐藏锚点，例如：

```markdown
该研究使用2010—2022年的企业面板数据。<!-- source:S1 -->
```

在 `sources.md` 中用同一编号说明出处和支持的事实。

#### 5. 撰写与排版

- 写作前必须读取 `references/editorial-depth-and-footer.md`。默认生成完整长文，不得把公众号成稿写成数百字摘要；只有用户明确同意时才使用短讯模式。
- 使用科学、准确、通顺的语言；消除错别字、语病、歧义和无意义的口号。
- 中文稿默认中文化表达；专业术语首次出现时用“中文（English）”，后文按用户确认规则处理。
- 中英文稿必须采用严格平行双语：标题、各级标题、正文段落、列表/表格标签、图注、行动提示、免责声明和脚注均须有事实、顺序和强调一致的中文与英文对应内容；不得以英文摘要替代全文英文。
- 语言和缩写须遵循 `references/language-and-abbreviation-policy.md`。不得自行展开、翻译或决定缩写的展示方式。
- 保留必要的英文题名、模型名、期刊名和专有名词，不机械翻译。
- 标题可以有传播力，但不得改变研究边界或制造确定性。
- 使用短段落、清晰标题、有限重点、图片和图注；不堆叠 emoji 或装饰组件。
- 按 `references/image-policy.md` 提取、筛选、保存并放置图片。
- 添加图表前集中向用户确认每一项是否显示图注。确认结果分别记录为 `user-confirmed-add` 或 `user-confirmed-omit`；用户要求修改时，先确认最终文字再记录为添加。未确认的 `NEEDS_REVIEW` 不得进入成稿。
- 图和表的可见图注不使用任何标点，包括句末标点、冒号、顿号、逗号、括号和连接号；通过自然语序、空格或“与”“及”等连接词表达。
- 表格单元格换行时，按每一行的语义决定标点：单个词、短标签、名称、数字或并列短语不加标点；完整句子才使用正常句内或句末标点。不得因为换行而机械添加或删除标点。详细规范见 `references/layout-punctuation-policy.md`。
- 使用 `assets/templates/` 中相应模板。不要把模板中的注释或占位符留在最终可见正文中。
- 任何面向作者或编辑的提示、警告、待办、核验说明和操作指令只能写在 HTML 注释 `<!-- 中文提示 / English note -->` 中，不得作为可见正文、标题、引用、图注或强调文本。所有提示必须同时提供中文和英文。
- 正文结束后使用 `assets/templates/00-cea-standard-footer.md`：不显示往期精彩文章、CEA/JCEBS介绍或关注提示，只保留中英文隐藏注释，提醒编辑从已发布的往期文章复制完整固定结尾。
- 如果用户明确要求在 Markdown 中写入往期精彩文章或 CEA/JCEBS 介绍，必须逐字采用 `references/approved-fixed-ending-copy.md` 中的核准文案和链接，不改写、不缩写、不自动补充。
- 底部固定图片必须使用 `assets/brand/扫码_搜索联合传播样式-标准色版.png`，生成稿中复制为 `assets/扫码_搜索联合传播样式-标准色版.png`；不得继续使用 `cea-europe-uk-qr.jpg`。
- 图片下方只显示描述性图注。来源写在紧随图注的隐藏批注 `<!-- image-source: S1, 原论文图2 -->` 中，并在 `sources.md` 图片台账完整登记；可见图注不得出现“来源：”或 “Source:”。

#### 6. 生成来源和检查报告

完成 `article.md` 后运行：

```bash
python3 scripts/qa_markdown.py \
  article.md \
  --sources sources.md \
  --report qa-report.md \
  --strict
```

同时按 `references/qa-policy.md` 做人工语义检查。脚本只能发现结构化风险，不能替代事实核验、语法审校和学术判断。

用户明确接受风险时，可记录强制通过：

```bash
python3 scripts/qa_markdown.py \
  article.md \
  --sources sources.md \
  --report qa-report.md \
  --strict \
  --override "用户已确认接受列明风险"
```

#### 7. 交付

交付以下内容并说明状态：

- `article.md`：排版后的公众号初稿；
- `sources.md`：来源与事实映射；
- `qa-report.md`：必须二次检查的项目及通过状态；
- `README_BEFORE_PUBLISHING.md`：中英文发表前阅读文档，列出需要核验、修改和在公众号编辑器内完成的事项；
- `assets/`：实际采用的本地图片。

如果仍有 `BLOCK`，明确写“初稿已生成，但不建议进入发布环节”。用户强制通过后写“已按用户授权强制通过，风险仍保留”。

作者完成修改后，如同意沉淀训练数据，运行 `scripts/archive_revision.py` 归档“生成稿—终稿—来源—检查报告”。只有用户明确要求归档时才执行。

## 资源导航

- 栏目与五套模板：`references/category-and-template-guide.md`
- 证据、官方来源与引用：`references/evidence-and-sources.md`
- 图片提取、版权和 AI 图片：`references/image-policy.md`
- 图表图注与表格换行标点：`references/layout-punctuation-policy.md`
- 语言、严格双语与缩写确认：`references/language-and-abbreviation-policy.md`
- 科学语言与质量闸门：`references/qa-policy.md`
- CEA 品牌基线：`references/brand-guide.md`
- CEA 核准固定结尾文案：`references/approved-fixed-ending-copy.md`
- 正文深度、最低篇幅与固定结尾：`references/editorial-depth-and-footer.md`
- 历史语料使用方法：`references/corpus-guide.md`
- Skill 与未来模型微调路线：`references/training-strategy.md`
- 两阶段研究级论文解读：`references/research-paper-analysis-workflow.md`
- Markdown 模板：`assets/templates/`
- 研究级论文解读结构：`assets/templates/research-paper-analysis.md`
- 研究级论文解读启动提示词：`assets/prompts/START_RESEARCH_PAPER_ANALYSIS.md`
- CEA 联合传播标准色版：`assets/brand/扫码_搜索联合传播样式-标准色版.png`
- 七个完整栏目样例：`sample/`
- 中文使用说明与完整教程：`README.md`
- English documentation and full tutorial: `README_EN.md`
