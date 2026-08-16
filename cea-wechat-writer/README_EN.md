# CEA WeChat Writing and Research-Grade Paper Analysis Skill

**Documentation language: [中文（默认）](README.md) | English**

> Chinese is the default documentation entry only. It does not allow the Skill to skip language confirmation for generated content. Each writing task must still confirm Chinese, English, Chinese-English, or another language.

`cea-wechat-writer` is a local content workflow for the Chinese Economic Association UK/Europe (CEA). It supports two separate delivery modes:

1. converting papers, Word files, webpages, conference materials, recruitment notices, or calls for papers into reviewable WeChat Markdown drafts;
2. jointly using a paper PDF, converted Markdown, and figures to create a research-grade paper analysis note.

The Skill creates local files only. It does not sign in to WeChat, create a platform draft, or publish content.

## Contents

- [1. Modes and deliverables](#1-modes-and-deliverables)
- [2. Installation and directories](#2-installation-and-directories)
- [3. Five-minute quick start](#3-five-minute-quick-start)
- [4. Tutorial 1: two-stage research-grade paper analysis](#4-tutorial-1-two-stage-research-grade-paper-analysis)
- [5. Tutorial 2: CEA WeChat Markdown draft](#5-tutorial-2-cea-wechat-markdown-draft)
- [6. Language, acronyms, and bilingual rules](#6-language-acronyms-and-bilingual-rules)
- [7. Images, captions, tables, and editorial notes](#7-images-captions-tables-and-editorial-notes)
- [8. Seven categories and five templates](#8-seven-categories-and-five-templates)
- [9. Sources, evidence, and quality assurance](#9-sources-evidence-and-quality-assurance)
- [10. Scripts](#10-scripts)
- [11. Troubleshooting](#11-troubleshooting)
- [12. Directory structure](#12-directory-structure)
- [13. Sources, training materials, and rights](#13-sources-training-materials-and-rights)

## 1. Modes and deliverables

| Mode | Use cases | Default deliverable |
|---|---|---|
| WeChat writing | Article Interpretation, Academic Frontier, Conference Notice, Recent News, Association History, Special Issue, Talent Recruitment | `article.md`, `sources.md`, `qa-report.md`, `README_BEFORE_PUBLISHING.md`, and `assets/` |
| Research-grade paper analysis | Reading notes, literature-review material, research-design analysis, theory and evidence evaluation | One research-grade Markdown file at the user-confirmed path |

If the user asks only for a “paper analysis,” the Skill first asks whether the intended output is a WeChat article or a research-grade reading note. It does not silently produce both.

The main documentation is split by language, but each WeChat delivery keeps `README_BEFORE_PUBLISHING.md` bilingual because publication instructions must support both Chinese- and English-speaking editors.

### 1.1 What WeChat mode does not do

- It does not sign in to WeChat.
- It does not create a platform draft.
- It does not broadcast or publish.
- It does not automatically generate visible Previous Highlights, CEA/JCEBS introductions, or follow prompts.
- It does not archive author revisions as training data without explicit permission.

### 1.2 What research-analysis mode does not do

- Stage 1 does not begin the complete paper analysis.
- Stage 1 does not create the final Markdown file.
- Providing paths, replying “received,” or adding files does not authorise Stage 2.
- Converted Markdown is not treated as more authoritative than the original PDF.
- Missing data, coefficients, sample sizes, hypotheses, figures, or page numbers are never invented.

## 2. Installation and directories

### 2.1 Portable path notation

This README is designed for GitHub team sharing and is not tied to any contributor's username or local directory:

- use `<repo-root>` for the repository root, for example `/path/to/CEA_Skill`;
- use `<repo-root>/cea-wechat-writer` for the Skill source;
- use `<codex-skills-directory>/cea-wechat-writer` for the Codex installation, for example `/path/to/.codex/skills/cea-wechat-writer`.

Use relative paths for repository resources wherever possible. Supply real absolute paths from the current user's machine only when executing a concrete task.

Unless a command says otherwise, run all relative commands below from `<repo-root>/cea-wechat-writer`.

The Skill root is the directory that actually contains `SKILL.md`. Scripts, templates, references, and assets are resolved relative to that directory.

### 2.2 Install or update the Skill

To manually synchronise the source and installed copies:

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

Replace both `/path/to/...` sample values with the actual directories on the current machine. The command deliberately omits `--delete`, so it does not remove extra files from the installed directory. Open a new task after synchronisation so Codex loads the latest Skill.

### 2.3 Invoke the Skill

Name it explicitly in a new task:

```text
Use $cea-wechat-writer
```

If it is not triggered automatically, also provide the real absolute path to `SKILL.md` on the current machine.

## 3. Five-minute quick start

### 3.1 Research-grade paper analysis

Copy this launcher:

```text
Use $cea-wechat-writer to start the two-stage research-grade paper analysis workflow.
For now, collect inputs and perform Stage 1 only. Do not begin the complete analysis or create the final Markdown file.
Ask me for the absolute paths to the Skill, paper PDF, paper Markdown, and paper figures, and ask where to save the result.
I may reply "default" for the save location. Begin analysis and writing only after I explicitly say "start Stage 2".
```

The full bilingual launcher is available at [`assets/prompts/START_RESEARCH_PAPER_ANALYSIS.md`](assets/prompts/START_RESEARCH_PAPER_ANALYSIS.md).

### 3.2 WeChat draft

```text
Use $cea-wechat-writer to generate a CEA WeChat Markdown draft from my source materials.
First confirm the language, category, review mode, acronyms, fixed ending, and figure-caption choices. Create only the local draft, source ledger, QA report, pre-publication README, and image assets. Do not upload or publish anything.
```

## 4. Tutorial 1: two-stage research-grade paper analysis

### Step 0: prepare the paper materials

Recommended inputs are:

- the original paper PDF;
- Markdown converted from the same PDF;
- a directory containing extracted paper figures;
- optional notes about the research questions or methods that matter most to you.

If the paper Markdown does not yet exist, convert it at [MarkItDown Online](https://markitdown.online/) and download the `.md` file.

> Before uploading unpublished, copyrighted, or confidential material to a third-party website, confirm that you are authorised to do so. Converted Markdown is only a search aid; formulas, tables, figures, footnotes, and complex layout must still be verified against the PDF.

### Step 1: start the Skill

Use the launcher above. The first response should contain only an input form, not a premature paper summary:

```text
Please reply once using the format below. Paste absolute paths for the first four items; the save location may be "default".

1. Skill directory:
2. Paper PDF:
3. Paper Markdown:
4. Paper figures directory:
5. Result save location: default
```

When asking for the paper Markdown path, simultaneously explain that [MarkItDown Online](https://markitdown.online/) may be used if needed, that third-party-upload permission must be confirmed for unpublished, copyrighted, or confidential papers, and that the Skill will not upload the paper silently.

If the current task already specifies the Skill path, it may be echoed for confirmation instead of being requested again. If no figures directory exists, item 4 may be `none`.

### Step 2: confirm the save location

The save location is a separate choice and is not a fifth material path.

- `default`: use the directory containing the resolved `SKILL.md`;
- default filename: `<paper PDF stem>_研究级论文解读.md`;
- a path ending in `.md`: treat it as the complete output path;
- a directory path: propose a filename during Stage 1;
- an existing file: ask whether to rename or overwrite; never overwrite silently.

### Step 3: review the Stage 1 report

Stage 1 first reads the specified `SKILL.md` in full, together with every reference, template, script, and asset that it explicitly requires for the task. It then checks feasibility and aligns requirements. The report must contain:

#### A. Task understanding

The intended deliverable, the role of each paper source, the main Skill constraints, and the proposed output path.

#### B. Proposed Markdown structure

Level-one and level-two headings adapted to the actual paper design. Theoretical, causal empirical, predictive, experimental, survey, case, and review papers should not be forced into one identical outline.

#### C. Decisions requiring confirmation

The default proposal is:

- full research-grade depth;
- Chinese-first writing with English retained when a technical term first appears;
- balanced coverage of the question, theory, method, evidence, contribution, and limitations;
- no external literature expansion by default;
- figure-by-figure analysis of core visuals;
- analyst assessments clearly separated from author statements.

The output language must be confirmed as Chinese, English, Chinese-English, or Other. Chinese-English means strict parallel bilingual writing; confirm every acronym's English expansion, Chinese rendering, and first and subsequent display rules before drafting. For `Other`, confirm the exact language, regional variant or writing system, and whether it is monolingual or paired with Chinese.

#### D. File-check results

At minimum, the report covers:

- the actual `SKILL.md` read;
- PDF readability and page count;
- Markdown readability, encoding, and conversion gaps;
- figure count, formats, and preliminary numbering alignment;
- whether the PDF and Markdown appear to represent the same paper;
- output conflicts;
- current blockers.

Stage 1 must end by saying that it is waiting for confirmation and has not entered Stage 2.

### Step 4: approve the plan

If the defaults are acceptable, reply:

```text
Use the default plan and start Stage 2.
```

For a customised analysis, reply for example:

```text
Use strict Chinese-English. Focus on identification, mechanism evidence, and research-design limitations.
Analyse every core figure but do not embed the images in the Markdown yet.
After recording these choices, start Stage 2.
```

If Chinese-English is selected, the Skill first supplies an acronym table for confirmation of each expansion, Chinese rendering, and first and subsequent display rule. Drafting does not start until this is resolved.

### Step 5: Stage 2 analysis

Stage 2 will:

1. use Markdown to search the text, sections, hypotheses, methods, and results;
2. use the PDF to verify formulas, tables, captions, footnotes, appendices, and complex layout;
3. use figures to explain axes, results, intended claims, links to the research question, and limitations;
4. build a claim-evidence-locator-speaker map;
5. distinguish author statements, direct evidence, author interpretation, and analyst assessment;
6. select the correct analytical branch for causal, theoretical, predictive, experimental, survey, case, or review research;
7. write the final research-grade Markdown and run a final verification pass.

A Chinese analysis of a standard empirical or theoretical paper will usually require approximately 5,000–10,000 Chinese characters, and complex papers may require more. English, Chinese-English, and other languages must provide equivalent research depth rather than mechanically following a Chinese-character count. Coverage of the argument takes priority over brevity.

### Step 6: accept the research note

Check that:

- the research question, motivation, gap, and actual contribution are clear;
- key claims include Section, Figure, Table, Equation, Appendix, or page locators;
- results describe direction, magnitude, uncertainty, and practical meaning rather than only “significance”;
- causal language matches the research design;
- author-acknowledged limitations and analyst assessments are separate;
- unresolved matters are marked as “cannot be confirmed from the paper”;
- the final file is at the confirmed path.

The delivery message should also state the complete output path, source files actually used, unresolved or unparseable content, Skill-check status, and how any Prompt–Skill conflict was handled.

See [`references/research-paper-analysis-workflow.md`](references/research-paper-analysis-workflow.md) for the full rules and [`assets/templates/research-paper-analysis.md`](assets/templates/research-paper-analysis.md) for the base structure.

## 5. Tutorial 2: CEA WeChat Markdown draft

### Step 1: prepare source materials

You may provide:

- a paper PDF or Word file;
- official webpages;
- conference programmes, calls for papers, or recruitment notices;
- images with identifiable sources;
- user notes or preferred emphasis.

User notes are leads, not substitutes for original or official evidence.

### Step 2: complete pre-drafting confirmation

Before drafting, the Skill must confirm:

1. language: Chinese, English, Chinese-English, or Other;
2. category: one of the seven supported categories;
3. review mode: regular or strict academic review, and whether a risk-bearing draft is allowed;
4. fixed ending: hidden bilingual copy instruction by default;
5. figure and table captions: after extracting and selecting visuals, list each number, content, proposed position, and proposed caption, then confirm add, omit, or revise and add.

The body should not be drafted before these choices are resolved.

When `Other` is selected, also confirm the exact language, regional variant or writing system, and whether it is monolingual or paired with Chinese. A WeChat draft defaults to a complete long-form article, not a few-hundred-word summary; use short-news mode only with explicit user agreement.

### Step 3: create a standard article directory

The Skill can do this, or you can run:

```bash
python3 scripts/new_article.py \
  --output ./work/sample-article \
  --category 文章解读 \
  --language 中文 \
  --title "Working title"
```

Do not overwrite an existing non-empty directory without explicit permission.

### Step 4: build the source and evidence map

Material facts—including numbers, dates, authors, affiliations, roles, sample sizes, journal metrics, findings, venues, and deadlines—must come from original materials or official webpages.

Use a hidden source anchor in the body:

```markdown
The study uses firm-level panel data from 2010 to 2022.<!-- source:S1 -->
```

The matching `S1` entry in `sources.md` records the source, locator, supported claims, verification status, and image rights. Conflicting sources are disclosed side by side rather than silently resolved.

### Step 5: select a category template and draft

The Skill selects one of five stable templates. Historical material may guide only:

- structure;
- paragraph rhythm;
- terminology handling;
- CEA tone;
- layout habits.

Dates, professional positions, contact details, journal metrics, and research facts from historical posts must not be reused as current facts.

### Step 6: process images and captions

Image priority is:

1. user-provided images;
2. figures from the source material;
3. official images;
4. explicitly authorised historical assets;
5. author-approved AI images.

AI covers and illustrations are allowed but should generally be avoided. Every proposed visual requires an individual caption decision.

Record each decision as `user-confirmed-add` or `user-confirmed-omit`; if revision is requested, confirm the final wording before recording an add decision. An unresolved `NEEDS_REVIEW` item must not enter the final draft.

### Step 7: handle the fixed ending

The Markdown draft does not automatically generate visible:

- Previous Highlights;
- the CEA introduction;
- the JCEBS introduction;
- the follow prompt.

It contains only a bilingual HTML comment instructing the editor to copy the complete ending from a published article. If the user explicitly requests the ending in Markdown, use `references/approved-fixed-ending-copy.md` verbatim.

The source footer asset inside the Skill is:

```text
assets/brand/扫码_搜索联合传播样式-标准色版.png
```

The generated article must copy and reference it as:

```text
assets/扫码_搜索联合传播样式-标准色版.png
```

### Step 8: run strict QA

```bash
python3 scripts/qa_markdown.py \
  ./work/sample-article/article.md \
  --sources ./work/sample-article/sources.md \
  --report ./work/sample-article/qa-report.md \
  --strict
```

`BLOCK=0` means the structured checker found no blocking issue. Also complete the manual semantic review in [`references/qa-policy.md`](references/qa-policy.md); the script cannot replace fact checking, language editing, academic judgement, or review by the author, editor, and association.

### Step 9: perform the pre-publication review

Read `README_BEFORE_PUBLISHING.md` before publication. Verify:

- numbers, dates, authors, and affiliations;
- association versus causation;
- registration, submission, email, fee, and QR details;
- image rights and portrait permissions;
- bilingual alignment and acronyms;
- that HTML comments stay hidden in preview;
- that the fixed ending has been copied manually in the WeChat editor;
- the actual layout in the WeChat editor.

## 6. Language, acronyms, and bilingual rules

| Selection | Behaviour |
|---|---|
| Chinese | Use natural Chinese; introduce technical terms as “Chinese (English)” at first mention, then follow the confirmed display rule |
| English | Write fully in English without unnecessary Chinese paragraphs |
| Chinese-English | Strict parallel bilingual text, not a Chinese article with an English abstract |
| Other | Confirm the language, locale, script, and whether it is standalone or paired with Chinese |

In Chinese-English mode, titles, headings, paragraphs, lists, table labels, captions, calls to action, notices, and footnotes must match in facts, order, and emphasis.

Every acronym—including CEA, JCEBS, ESG, and AI—requires confirmation of:

- the English expansion;
- the Chinese rendering;
- the first-use format;
- the subsequent-use format.

## 7. Images, captions, tables, and editorial notes

### 7.1 Figure and table captions

- Decide separately whether each caption is added, omitted, or revised and added.
- Visible captions contain no punctuation, including colons, parentheses, and terminal punctuation.
- Put the source in the immediately following hidden comment.
- Do not show `Source:` in visible body text.
- An unresolved `NEEDS_REVIEW` state blocks QA.

Example:

```markdown
![Regression results](assets/figure-01.png)

_Figure 1 Baseline regression results_
<!-- caption-decision: user-confirmed-add -->
<!-- image-source: S1, Original paper Figure 2 / 原论文 Figure 2 -->
```

### 7.2 Line breaks and punctuation in tables

- Single words, short labels, names, numbers, or parallel phrases take no punctuation.
- Complete sentences retain punctuation required for natural reading in the selected language.
- Do not add or remove punctuation mechanically because of a visual line break.

### 7.3 Author or editor instructions

Every warning, task, verification note, or instruction must be a bilingual HTML comment:

```markdown
<!-- 请在公众号编辑器内补入往期文章固定结尾 / Add the fixed ending from a published post in the WeChat editor -->
```

Do not expose instructions as visible body text. Confirm in rendered preview that comments remain hidden.

## 8. Seven categories and five templates

| Category | Default template | Core purpose |
|---|---|---|
| Article Interpretation | Research Explainer | Question, method, findings, mechanisms, and boundaries |
| Academic Frontier | Method Frontier | Methods, models, literature context, and application limits |
| Conference Notice | Notice/Opportunity | Dates, venue, programme, registration, or submission |
| Recent News | News Recap | Events, people, organisational progress, and significance |
| Association History | History/Profile | Memoirs, institutional development, and archives |
| Special Issue | Notice/Opportunity | Theme, scope, editors, deadlines, and submission requirements |
| Talent Recruitment | Notice/Opportunity | Roles, fields, eligibility, materials, and contacts |

Seven complete examples are available under [`sample/`](sample/). They demonstrate structure and rules only. Historical conference, special-issue, and recruitment examples must not be published as current notices.

## 9. Sources, evidence, and quality assurance

### 9.1 Material facts that require sources

- numbers, dates, and sample sizes;
- authors, affiliations, roles, and identities;
- journal metrics;
- research findings and causal claims;
- venue, deadline, fee, and contact details;
- image source, copyright, and permission status.

### 9.2 Issues that normally block publication

- unsourced material numbers or claims;
- uncertain authors, affiliations, roles, venues, or deadlines;
- association presented as causation;
- undisclosed source conflicts;
- unclear image rights or portrait permission;
- placeholders, mojibake, remote images, or missing assets;
- non-parallel bilingual text or unconfirmed acronyms;
- captions with punctuation or without individual confirmation;
- visible editorial instructions;
- automatically generated fixed-ending prose;
- a missing `README_BEFORE_PUBLISHING.md`.

Override only when the user explicitly accepts the specific risk; the risk cannot be erased. Record `USER_OVERRIDE`, the accepted risk, operator note, and time in both `qa-report.md` and `sources.md`.

## 10. Scripts

| Script | Purpose |
|---|---|
| `scripts/new_article.py` | Create a standard WeChat article directory |
| `scripts/retrieve_examples.py` | Retrieve usable historical examples by category and topic |
| `scripts/qa_markdown.py` | Check source anchors, images, placeholders, and blocking states |
| `scripts/build_corpus.py` | Rebuild the historical HTML and Word/PDF corpus index |
| `scripts/archive_revision.py` | Save generated and final drafts only when the user explicitly requests archival |

Example retrieval command:

```bash
python3 scripts/retrieve_examples.py \
  --corpus references/corpus/index.json \
  --category 文章解读 \
  --query "research topic or title" \
  --limit 3
```

If the default retrieval returns fewer than three items, do not fill the gap from another category and do not use `degraded_mojibake` body text; rely on the formal template and quality rules instead.

Run `archive_revision.py` only when the user explicitly asks to archive revisions.

## 11. Troubleshooting

### The Skill did not trigger

Write `$cea-wechat-writer` explicitly and provide the absolute `SKILL.md` path if needed.

### The paper Markdown does not exist

Convert it at [MarkItDown Online](https://markitdown.online/), download it, and provide its local absolute path. Confirm third-party upload permission for sensitive material.

### The PDF and Markdown do not match

Stage 1 reports title, author, section, Figure/Table numbering, or content mismatches. Prefer the original PDF. Reconvert a materially inconsistent Markdown before Stage 2.

### There is no figures directory

Enter `none` in the input form. Stage 1 asks whether figures may be checked or extracted directly from the PDF.

### The default output already exists

The Skill must ask whether to rename or overwrite. It must never overwrite silently. A version suffix such as `_v2.md` is recommended.

### QA reports a BLOCK

Read `qa-report.md`, resolve sources, caption decisions, image rights, fixed-ending comments, or language issues, and rerun the checker. Use an override only after the user explicitly accepts the specific risk.

### Hidden instructions are visible in WeChat

Stop publication, inspect whether the editor transformed the HTML comments, and verify the rendered preview again.

## 12. Directory structure

```text
cea-wechat-writer/
├── SKILL.md
├── README.md
├── README_EN.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── brand/
│   ├── prompts/
│   └── templates/
├── references/
│   ├── corpus/
│   └── *.md
├── sample/
│   └── 01...07/
└── scripts/
```

## 13. Sources, training materials, and rights

The design and WeChat formatting workflow of this Skill referenced:

- [`../ref-duyi-wechat-skill-suite-main/`](../ref-duyi-wechat-skill-suite-main/)

The categorised HTML training materials were collected with:

- crawler: [`../training_data/craw.py`](../training_data/craw.py)
- crawled output: [`../training_data/train_by_category_html/`](../training_data/train_by_category_html/)

Language, writing, and layout training also used materials sent by Shijie via email:

- [`../training_data/train_by_Shijie_Word/`](../training_data/train_by_Shijie_Word/)

These materials were used for category analysis, language training, structural analysis, template development, layout learning, and quality-control rules. Historical material is training and reference data only. Its dynamic facts, image rights, contact details, professional positions, and time-sensitive information must not be treated as currently valid.

**CEA reserves all rights of interpretation regarding this Skill and its documentation.**

---

[阅读中文默认文档](README.md)
