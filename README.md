# CEA WeChat Writer / CEA 公众号写作 Skill

## 中文说明

### 1. 这是什么

`cea-wechat-writer` 是为全英/全欧中国经济学会（CEA UK/Europe）设计的公众号写作、事实核查与 Markdown 排版 Skill。它把论文、Word 稿、网页、会议材料、招聘信息或用户笔记整理成可审阅的公众号初稿，同时保存来源记录、图片资产和质量检查结果。

它只生成本地文件，不登录公众号、不创建草稿箱，也不发布内容。

每次标准交付包含：

- `article.md`：完成排版的 Markdown 初稿；
- `sources.md`：来源、事实与图片权利台账；
- `qa-report.md`：自动检查结果和人工复核提醒；
- `README_BEFORE_PUBLISHING.md`：中英文发表前阅读与修改清单；
- `assets/`：正文实际使用的本地图片。

### 2. 为什么先做 Skill，而不是立即微调模型

当前语料规模适合提炼规则、模板和少样本示例，但还不足以单独训练一个可靠的基础模型。Skill 可以立即使用云端大模型，并把品牌规范、证据约束、图片策略、栏目模板和质量闸门固化在同一流程中。等积累足够多经作者确认的“生成稿—修改稿—终稿”后，再考虑监督微调或偏好优化。

建议路线是：

1. 先用本 Skill 生成初稿；
2. 由作者修改并记录修改理由；
3. 经用户明确同意后归档训练对；
4. 建立固定测试集，比较事实准确性、语言质量、栏目匹配和排版稳定性；
5. 数据量和一致性足够后，再决定是否微调模型。

### 3. 支持的七个栏目与五套模板

| 栏目 | 默认模板 | 主要用途 |
|---|---|---|
| 文章解读 | 研究解读 | 解释论文问题、方法、结果、机制与边界 |
| 学术前沿 | 方法前沿 | 介绍方法、模型、文献脉络与应用限制 |
| 会议通知 | 通知机会 | 提供时间、地点、议程、报名或投稿信息 |
| 新近动态 | 新闻回顾 | 报道活动、人物、组织进展与后续意义 |
| 学会历史 | 历史人物 | 整理人物回忆、学会沿革与档案材料 |
| 特刊推荐 | 通知机会 | 介绍特刊主题、范围、编辑、期限与投稿要求 |
| 广纳英才 / 人才招聘 | 通知机会 | 介绍岗位、方向、资格、材料与联系方式 |

五套稳定模板为：研究解读、方法前沿、通知机会、新闻回顾、历史人物。栏目与模板的详细映射见 `references/category-and-template-guide.md`。

### 4. 使用前必须确认的事项

Skill 在写正文前必须确认：

1. 写作语言：中文、英文、中英文或其他；选择其他时还要确认具体语言/变体及单双语方式；
2. 栏目：由用户指定，或由 Skill 推荐后让用户确认；
3. 审核方式：常规审核或严格学术审核，以及是否允许带风险生成；
4. 固定结尾：Markdown 不自动生成往期精彩文章、CEA/JCEBS介绍和关注提示，改在公众号编辑器内从已发布的往期文章复制；
5. 图表图注：对每个拟用图表分别选择添加、不添加或修改后添加，不能默认统一处理。

未指定语言时不能自行假定。选择中英文时执行严格平行双语，标题、标题层级、每段正文、列表/表格、图注、行动提示、声明和固定结尾都必须有事实与顺序一致的中文和英文版本，不能用英文摘要代替全文英文。写作前还必须把材料中的全部缩写交给用户确认英文全称、中文译名和展示规则；写作中出现新缩写时继续确认。

### 5. 快速开始

把整个目录放到 Codex 的 skills 目录后，可直接在任务中调用：

```text
请使用 cea-wechat-writer，根据我提供的论文 PDF 写一篇“文章解读”。
语言为中文，使用严格学术审核，只生成 Markdown 初稿及来源、QA 和图片文件。
```

也可以先创建标准工作目录：

```bash
python3 scripts/new_article.py \
  --output /absolute/path/to/output \
  --category 文章解读 \
  --language 中文 \
  --title "暂定标题"
```

推荐输入包括原始 PDF、DOCX、官方网页链接、会议日程、投稿启事、招聘公告和清晰的用户笔记。仅有线索而没有可靠来源时，Skill 会保留风险，不会补造事实。

### 6. 标准工作流

1. 收集原始材料并确认语言、栏目、审核方式和是否手动添加往期文章。
2. 读取完整材料，登记标题、作者、机构、日期、URL 和访问日期。
3. 按栏目检索历史示例，只借鉴结构、节奏、术语和排版。
4. 建立“事实—来源”映射，并标记来源冲突和待确认项。
5. 选择五套模板之一，撰写科学、准确、通顺的正文。
6. 自动提取可用图片，放在最合适的位置并补充图注和图片台账。
7. 按栏目深度要求展开正文，加入中英文固定结尾复制提示和联合传播图片。
8. 运行结构化 QA，再进行人工事实、语言、学术与版权检查。
9. 生成中英文 `README_BEFORE_PUBLISHING.md`，再交付全部本地文件。

### 7. 事实与来源规则

数字、日期、样本量、作者身份、单位职务、会议地点、截止日期、期刊指标、研究结果和因果结论都属于重要事实，只能来自用户原始材料或官方网页。

正文在相应事实段落末尾使用隐藏锚点：

```markdown
该研究使用2010—2022年的企业面板数据。<!-- source:S1 -->
```

`sources.md` 中的 `S1` 必须说明来源类型、标题、路径或 URL、支持的事实、定位和核验状态。原文与官方网页冲突时应并列记录，不得擅自选择。历史文章只能作为语言和排版示范，其中的时效性事实不能自动沿用。

### 8. 图片策略

图片使用顺序为：用户提供图片、原始材料中的图表、官方图片、明确授权的历史资产，最后才考虑 AI 图片。能不用 AI 图片时尽量不用。

每张采用的图片都要：

- 保存为本地文件；
- 先让用户逐项确认是否显示图注，并记录 `user-confirmed-add` 或 `user-confirmed-omit`；
- 用户选择添加时，在正文放置其确认后的清晰图注；
- 图和表的可见图注不使用任何标点；
- 在图注后用 `<!-- image-source: S1, 具体定位 -->` 保存隐藏来源，不在可见图注显示“来源”或 “Source”；
- 在 `sources.md` 记录来源、权利状态、处理方式和用途；
- 在发布前检查清晰度、裁切、人物说明、二维码有效性和版权。

AI 封面或插图只能在作者同意、缺少合适原图且确有阅读价值时生成，并必须明确记录为 AI 生成资产。

表格单元格需要换行时，不按视觉形式机械处理标点：单个词、短标签、名称、数字和并列短语不加标点；完整句子保留符合中文、英文或用户所选语言阅读习惯的必要标点。详见 `references/layout-punctuation-policy.md`。

任何作者或编辑提示只能使用中英文 HTML 注释，不得作为可见正文。底部固定使用 `assets/扫码_搜索联合传播样式-标准色版.png`。正式导入公众号前必须阅读 `README_BEFORE_PUBLISHING.md`，并在渲染预览中确认注释没有显示。

### 9. QA 与用户强制通过

严格检查命令：

```bash
python3 scripts/qa_markdown.py \
  article.md \
  --sources sources.md \
  --report qa-report.md \
  --strict
```

以下问题通常应阻止稿件进入发布环节：

- 数字、日期、样本量或研究结论没有来源；
- 作者、机构、职务、会议地点或截止日期不确定；
- 把相关性写成因果性，或把单篇研究写成学界共识；
- 原文和官方来源相互冲突但没有披露；
- 报名、投稿、邮箱、二维码或费用信息未核实；
- 图片版权、人物授权或 AI 图片标识不清；
- 仍有模板占位符、远程图片或缺失的本地资产；
- 存在明显错别字、语病、乱码或中英文术语不一致；
- 正文低于栏目最低深度、缺少必需章节，或把完整推文写成数百字摘要；
- Markdown自动生成往期精彩文章、CEA/JCEBS介绍或关注提示；
- 缺少从已发布往期文章复制完整固定结尾的中英文注释；
- 作者或编辑提示显示为正文，或提示注释没有同时提供中英文；
- 缺少中英文 `README_BEFORE_PUBLISHING.md`；
- 图片缺少隐藏来源批注，或可见图注直接显示“来源/Source”；
- 图表可见图注包含任何标点；
- 图表是否显示图注没有经过用户逐项确认；
- 中英文稿不是严格平行双语，或缩写未经用户交互确认。

用户可以明确要求强制通过，但风险不能被删除。执行时应在 `qa-report.md` 和 `sources.md` 中记录 `USER_OVERRIDE`、风险、操作者说明和时间。

### 10. 完整样例

`sample/` 下提供七个可独立阅读和运行 QA 的样例：

| 目录 | 栏目 | 内容 |
|---|---|---|
| `01-article-interpretation-esg/` | 文章解读 | ESG、全要素生产率与研发创新的论文解读 |
| `02-academic-frontier-bert/` | 学术前沿 | BERT 的基本机制与应用边界 |
| `03-conference-notice-2025/` | 会议通知 | 已结束的CEA年会历史通知样例 |
| `04-recent-news-2024/` | 新近动态 | CEA年会历史回顾 |
| `05-association-history-zhang-jun/` | 学会历史 | 张军教授与CEA的长期学术联系 |
| `06-special-issue-sustainability/` | 特刊推荐 | 已过期特刊的历史征稿样例 |
| `07-talent-recruitment-hit/` | 人才招聘 | 已过时招聘材料的安全改写样例 |

每个目录都包含 `article.md`、`sources.md`、`qa-report.md` 和 `assets/`。历史会议、征稿和招聘样例均不可直接发布；它们的作用是展示如何保留时效性警告和二次检查要求。

完整样例不是短摘要：文章解读和学会历史按长文展开，通知、动态、特刊与招聘也覆盖读者决策所需的信息。严格QA会按栏目检查最低正文深度、必需章节、固定结尾复制提示和联合传播图片。具体阈值见 `references/editorial-depth-and-footer.md`。

### 11. 脚本

- `scripts/new_article.py`：创建标准稿件目录；
- `scripts/retrieve_examples.py`：按栏目和主题检索可用语料；
- `scripts/qa_markdown.py`：检查来源锚点、图片、占位符和阻断状态；
- `scripts/build_corpus.py`：从历史 HTML 与 Word/PDF 材料重建语料索引；
- `scripts/archive_revision.py`：经用户明确同意后归档生成稿与终稿。

当前语料快照来自119篇历史 HTML 和一批 Word/PDF 训练材料。自动清洗结果并不等于可直接作为写作事实：乱码或结构退化的文章只能辅助判断排版，不能作为正文事实来源。需要更新索引时请重新运行语料构建脚本并检查报告。

### 12. 目录结构

```text
cea-wechat-writer/
├── SKILL.md
├── README.md
├── agents/
├── assets/
│   ├── brand/
│   └── templates/
├── references/
│   ├── corpus/
│   └── *.md
├── sample/
│   └── 01...07/
│       ├── article.md
│       ├── sources.md
│       ├── qa-report.md
│       ├── README_BEFORE_PUBLISHING.md
│       └── assets/
└── scripts/
```

### 13. 使用边界

- 输出只是初稿，不替代作者、编辑或学会的最终审核。
- 不把历史资料中的职务、费用、期限和联系方式视为当前信息。
- 不上传云端、不向外发送文件，除非用户明确授权并指定服务。
- 不在未经用户同意时归档作者修改稿作为训练数据。
- 不保证公众号 Markdown 渲染与微信编辑器完全一致，粘贴后仍需进行视觉检查。

---

## English Guide

### 1. What this skill does

`cea-wechat-writer` is a writing, fact-checking, and Markdown-layout skill for the Chinese Economic Association (UK/Europe). It converts papers, Word drafts, official webpages, conference materials, calls for papers, recruitment notices, or user notes into a reviewable WeChat article draft.

It produces local files only. It does not sign in to WeChat, create a platform draft, or publish anything.

A standard deliverable contains:

- `article.md`: the formatted article draft;
- `sources.md`: the evidence, fact, and image-rights ledger;
- `qa-report.md`: automated findings and human-review reminders;
- `README_BEFORE_PUBLISHING.md`: a bilingual pre-publication checklist;
- `assets/`: local images actually used in the article.

### 2. Why a skill comes before model fine-tuning

The current corpus is useful for extracting rules, templates, and few-shot examples, but it is not large or consistent enough to train a reliable foundation model by itself. A skill can immediately use a cloud model while enforcing CEA style, evidence requirements, image policy, category templates, and quality gates.

The recommended path is to use the skill first, collect author-approved revisions with explicit consent, maintain a fixed evaluation set, and consider supervised fine-tuning or preference optimization only after the dataset becomes sufficiently large and consistent.

### 3. Seven categories and five templates

| Category | Default template | Main purpose |
|---|---|---|
| Article interpretation | Research explainer | Explain a paper's question, method, findings, mechanism, and limits |
| Academic frontier | Method frontier | Introduce a method, model, literature context, and application limits |
| Conference notice | Notice/opportunity | Present dates, venue, programme, registration, or submission details |
| Recent news | News recap | Report events, people, organisational developments, and significance |
| Association history | History/profile | Organise memoirs, archival material, and institutional history |
| Special issue | Notice/opportunity | Explain scope, editors, deadlines, fees, and submission requirements |
| Talent recruitment | Notice/opportunity | Explain roles, fields, eligibility, materials, and contacts |

The five stable templates are Research Explainer, Method Frontier, Notice/Opportunity, News Recap, and History/Profile.

### 4. Required choices before drafting

The skill must confirm these choices before writing:

1. Language: Chinese, English, strict Chinese-English, or Other; Other requires the exact language/locale/script and whether it is standalone or paired with Chinese;
2. Category: selected by the user, or recommended by the skill and confirmed by the user;
3. Review mode: regular or strict academic review, and whether a risk-bearing draft is allowed;
4. Fixed ending: do not generate Previous Highlights the CEA or JCEBS introductions or the follow prompt in Markdown; copy the complete ending from a previously published article in the WeChat editor;
5. Figure and table captions: for every proposed visual, the user must choose add, omit, or revise and add; the skill must not apply one default to all visuals.

Language must not be silently assumed. “Chinese-English” means strict parallel bilingual text: every visible title, heading, paragraph, list/table label, caption, call to action, disclaimer, footnote, and brand-footer element must have factually equivalent Chinese and English counterparts in the same order. It is not a Chinese article with an English abstract. Before drafting, every acronym—including common ones—must be shown to the user for confirmation of its English expansion, Chinese rendering, and first/subsequent-use rule. Newly encountered acronyms require another confirmation.

### 5. Quick start

After placing the directory in the Codex skills folder, invoke it in a task:

```text
Use cea-wechat-writer to turn the attached paper into an Article Interpretation post.
Write in Chinese, use strict academic review, and produce only the
Markdown draft, source ledger, QA report, bilingual pre-publication README,
and local image assets.
```

To create an empty standard workspace first:

```bash
python3 scripts/new_article.py \
  --output /absolute/path/to/output \
  --category 文章解读 \
  --language 中文 \
  --title "Working title"
```

Preferred inputs include original PDFs, DOCX files, official URLs, conference programmes, formal calls, recruitment announcements, and well-identified user notes. A lead without reliable evidence remains a flagged lead; the skill must not invent missing facts.

### 6. Evidence and scientific-language rules

Numbers, dates, sample sizes, author identities, affiliations, positions, venues, deadlines, journal metrics, research findings, and causal claims are material facts. They must come from user-supplied original material or an official webpage.

Material factual paragraphs use a hidden source anchor:

```markdown
The study uses firm-level panel data from 2010 to 2022.<!-- source:S1 -->
```

The matching `S1` entry in `sources.md` records the source type, title, path or URL, supported claims, locator, and verification status. Conflicting sources must be disclosed side by side. Historical posts may guide style and layout, but their time-sensitive claims must never be reused as current facts.

Scientific language must distinguish association from causation, one study from a scholarly consensus, and reported robustness from universal validity. The draft should be grammatical, typo-free, readable, and conservative about policy implications.

Full articles must not be reduced to a few hundred Chinese characters. Strict QA enforces category-specific depth required sections the bilingual fixed-ending copy note and the joint-promotion image. The Markdown draft does not generate Previous Highlights or the CEA and JCEBS introductions. See `references/editorial-depth-and-footer.md` for the thresholds.

### 7. Image policy

The image priority is: user-provided images, figures from the original material, official images, authorised historical assets, and only then AI-generated artwork. AI images should be avoided when a useful and licensable original image exists.

Every selected image must be stored locally, entered in the image ledger, and checked for resolution, cropping, identity labels, QR-code validity, and rights. The user must decide for each figure or table whether its caption is shown, omitted, or revised before use. Visible figure and table captions must contain no punctuation at all. The source must appear in an immediately following hidden `image-source` comment, never as visible “Source:” caption text. AI artwork requires author approval and an explicit AI-generated label in the ledger.

When a table cell contains line breaks, punctuation follows meaning rather than layout: single words, short labels, names, numbers, and parallel phrases take no punctuation, while complete sentences retain the punctuation required for natural reading.

Every author or editor instruction must be a bilingual HTML comment and must never appear as visible article text. The footer uses `assets/扫码_搜索联合传播样式-标准色版.png`. Read `README_BEFORE_PUBLISHING.md` and verify in the rendered preview that no comments are exposed before importing the article into WeChat.

### 8. QA and user override

Run strict QA with:

```bash
python3 scripts/qa_markdown.py \
  article.md \
  --sources sources.md \
  --report qa-report.md \
  --strict
```

Unsourced numbers or findings, uncertain authorship or affiliation, unsupported causal language, undisclosed source conflicts, unchecked submission links or contacts, unclear image rights, missing local assets, unresolved placeholders, mojibake, and serious language errors should normally block publication.

A user may explicitly override a block, but the risk must remain visible. Record `USER_OVERRIDE`, the accepted risk, the operator note, and the time in both `qa-report.md` and `sources.md`.

### 9. Complete samples

The `sample/` directory contains one complete package for each of the seven categories. Every package includes an article, source ledger, QA report, and local assets. Several examples intentionally use historical conference, call-for-papers, or recruitment material to demonstrate safe expiry warnings. They are structural examples and must not be published as current notices.

### 10. Scripts and corpus

- `new_article.py` creates a standard article directory.
- `retrieve_examples.py` retrieves usable examples by category and topic.
- `qa_markdown.py` checks source anchors, images, placeholders, and blocking states.
- `build_corpus.py` rebuilds the historical HTML and Word/PDF corpus index.
- `archive_revision.py` archives generated and final drafts only with explicit user consent.

The corpus snapshot was built from 119 historical HTML files and a collection of Word/PDF training materials. Automated extraction quality varies. Degraded or garbled files may inform layout analysis, but they must not supply article facts.

### 11. Limits

- The output is a draft and does not replace final review by the author, editor, or association.
- Historical roles, fees, dates, deadlines, and contact information are not current by default.
- Files are not uploaded or transmitted unless the user explicitly authorises a named service.
- Author revisions are not archived as training data without explicit consent.
- Markdown may render differently in the WeChat editor, so a final visual check is still required.

---

## Skill 来源、训练材料与权利说明

本 Skill 的设计与公众号排版工作流参考了：

- `./ref-duyi-wechat-skill-suite-main`

分类 HTML 训练材料通过以下爬虫脚本获取：

- 爬虫脚本：`./training_data/craw.py`
- 爬取结果：`./training_data/train_by_category_html`

语言、写作和排版训练还使用了 Shijie 通过邮件提供的 Word 材料：

- `./training_data/train_by_Shijie_Word`

上述材料用于本 Skill 的栏目归纳、语言训练、结构分析、模板提炼、排版学习和质量检查规则建设。历史材料只作为训练与参考语料，其中的动态事实、图片权利、联系方式、人物职务和时效信息不能直接视为当前有效信息。

**本 Skill 及相关说明的全部解释权归 CEA 所有。**

## Skill Sources Training Materials and Rights Notice

The design and WeChat formatting workflow of this Skill referenced:

- `./ref-duyi-wechat-skill-suite-main`

The categorised HTML training materials were collected with:

- Crawler: `./training_data/craw.py`
- Crawled output: `./training_data/train_by_category_html`

The language writing and layout training also used Word materials sent by Shijie via email:

- `./training_data/train_by_Shijie_Word`

These materials were used for category analysis language training structural analysis template development layout learning and quality-control rules. Historical materials are training and reference sources only. Their dynamic facts image rights contact details professional positions and time-sensitive information must not be treated as currently valid without verification.

**CEA reserves all rights of interpretation regarding this Skill and the related documentation.**
