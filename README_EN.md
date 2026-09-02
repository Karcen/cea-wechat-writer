# CEA_Skill Project Guide and Tutorial

**Documentation language: [中文（默认）](README.md) \| English**

> Chinese is the default project-documentation entry only. It does not
> allow any writing task to skip language confirmation. Generated
> content must still be confirmed as Chinese, English, strict
> Chinese-English, or another language.

This directory contains the Chinese Economic Association UK/Europe (CEA)
workflow for WeChat writing and in-depth paper analysis, including the
installable Codex Skill, historical training material, the reference
formatting Skill, brand images, and complete examples.

The callable Skill is located in
[`cea-wechat-writer/`](cea-wechat-writer/).

## Contents

-   [1. What the project does](#1-what-the-project-does)
-   [2. Project directories](#2-project-directories)
-   [3. Install or update the Skill](#3-install-or-update-the-skill)
-   [4. Five-minute quick start](#4-five-minute-quick-start)
-   [5. Tutorial 1: two-stage paper
    analysis](#5-tutorial-1-two-stage-paper-analysis)
-   [6. Tutorial 2: CEA WeChat Markdown
    draft](#6-tutorial-2-cea-wechat-markdown-draft)
-   [7. Mandatory CEA writing and layout
    rules](#7-mandatory-cea-writing-and-layout-rules)
-   [8. Seven categories and five
    templates](#8-seven-categories-and-five-templates)
-   [9. Training data and historical
    corpus](#9-training-data-and-historical-corpus)
-   [10. Scripts, examples, and
    validation](#10-scripts-examples-and-validation)
-   [11. Output files and publication
    boundary](#11-output-files-and-publication-boundary)
-   [12. Troubleshooting](#12-troubleshooting)
-   [13. Sources and rights](#13-sources-and-rights)

## 1. What the project does

The project supports two separate modes:

  -----------------------------------------------------------------------
  Mode                    Main use                Default result
  ----------------------- ----------------------- -----------------------
  CEA WeChat writing      Paper interpretation,   A local WeChat Markdown
                          methods, conferences,   draft with source
                          news, history, special  ledger, QA report,
                          issues, and recruitment pre-publication guide,
                                                  and images

  In-depth paper analysis Reading notes,          One clean reader-facing
                          literature-review       analysis plus one
                          material,               editor-review record
                          research-design         
                          analysis, and theory    
                          and evidence evaluation 
  -----------------------------------------------------------------------

If a request says only "paper analysis," the Skill first asks whether
the intended result is a WeChat article or a paper-reading note. It does
not mix both structures by default.

### 1.1 WeChat writing mode

WeChat mode emphasises:

-   CEA tone and five stable templates;
-   material facts supported by original or official sources;
-   a source ledger in `sources.md`;
-   local images, hidden source comments, and per-figure caption
    confirmation;
-   strict QA and a bilingual pre-publication guide;
-   manual work that still has to be completed in the WeChat editor.

### 1.2 Paper-analysis mode

Research-analysis mode emphasises:

-   using the PDF, converted Markdown, and figures together;
-   a mandatory Stage 1 alignment followed by Stage 2 analysis;
-   internally separating author views, paper evidence, author
    interpretation, and editorial judgement while using natural
    attribution in the reader-facing text;
-   selecting the theory, methods, results, figures, contributions, and
    limitations that matter to the central argument rather than
    reproducing every section;
-   locating key judgments by Section, Figure, Table, Equation,
    Appendix, or PDF page;
-   normally using only four to six level-two headings for a cohesive,
    moderate-length analysis;
-   keeping workflow states, judgement mapping, and unresolved items in
    a separate editor-review record.

## 2. Project directories

``` text
CEA_Skill/
├── README.md                       Default Chinese project tutorial
├── README_EN.md                    English project guide
├── cea-wechat-writer/              Installable and callable Skill
│   ├── SKILL.md                    Execution-rule entry point
│   ├── README.md                   Full Chinese Skill tutorial
│   ├── README_EN.md                Full English Skill tutorial
│   ├── agents/openai.yaml          Codex interface metadata and default Prompt
│   ├── assets/                     Templates prompts and brand assets
│   ├── references/                 Detailed evidence language image and QA rules
│   ├── sample/                     Seven category examples
│   └── scripts/                    Creation retrieval QA and archival scripts
├── training_data/                  Historical HTML and Shijie Word/PDF material
├── ref-duyi-wechat-skill-suite-main/  Reference formatting Skill
└── QR_code-png/                    CEA QR and joint-promotion images
```

Important entry points:

-   [Skill execution rules](cea-wechat-writer/SKILL.md)
-   [Full Chinese Skill tutorial](cea-wechat-writer/README.md)
-   [Full English Skill tutorial](cea-wechat-writer/README_EN.md)
-   [Paper-analysis
    workflow](cea-wechat-writer/references/research-paper-analysis-workflow.md)
-   [Paper-analysis launch
    Prompt](cea-wechat-writer/assets/prompts/START_RESEARCH_PAPER_ANALYSIS.md)
-   [Natural writing and clean-copy
    rules](cea-wechat-writer/references/natural-writing-and-clean-copy.md)
-   [Seven WeChat examples](cea-wechat-writer/sample/)

Working folders such as `CEA_Work_Test/` are not part of the installable
Skill and should not be copied into the Codex skills directory.

## 3. Install or update the Skill

### 3.1 Portable path notation

This README is intended for GitHub team sharing and is not tied to any
contributor's username or local directory. The following sample
placeholders are used throughout:

  ---------------------------------------------------------------------------------------------
  Placeholder                  Meaning                 Example
  ---------------------------- ----------------------- ----------------------------------------
  `<repo-root>`                Root of the cloned      `/path/to/CEA_Skill`
                               repository              

  `<skill-root>`               Directory that actually `/path/to/CEA_Skill/cea-wechat-writer`
                               contains `SKILL.md`     

  `<codex-skills-directory>`   Local Codex Skills      `/path/to/.codex/skills`
                               directory               
  ---------------------------------------------------------------------------------------------

Links and commands inside the repository use relative paths wherever
possible. Replace placeholders with real absolute paths from the current
user's machine only when launching an actual task, supplying paper
inputs, or choosing an output directory.

Unless a command says otherwise, run all repository-relative commands
below from `<repo-root>`.

### 3.2 Synchronise to Codex

``` bash
CEA_REPO_ROOT="/path/to/CEA_Skill"
CEA_CODEX_SKILLS_ROOT="/path/to/.codex/skills"

mkdir -p "${CEA_CODEX_SKILLS_ROOT}/cea-wechat-writer"
rsync -a \
  --exclude '.DS_Store' \
  --exclude '__pycache__' \
  "${CEA_REPO_ROOT}/cea-wechat-writer/" \
  "${CEA_CODEX_SKILLS_ROOT}/cea-wechat-writer/"
```

Replace both `/path/to/...` sample values with the actual directories on
the current machine before running the command.

The command deliberately omits `--delete`, so it does not remove extra
files from the installed directory. Open a new task or reopen the task
after synchronisation so Codex reloads the Skill.

### 3.3 Confirm the installation

This file should exist:

``` text
<codex-skills-directory>/cea-wechat-writer/SKILL.md
```

Invoke the Skill with:

``` text
Use $cea-wechat-writer
```

If it does not trigger automatically, also provide the absolute path to
`SKILL.md`.

## 4. Five-minute quick start

### 4.1 Start paper analysis

A typical paper-analysis workflow uses three synchronized inputs:

1.  **Paper PDF**: the authoritative source for formulas, tables,
    figures, footnotes, and complex layouts.
2.  **Paper Markdown**: a token-efficient searchable version converted
    from the PDF.
3.  **Paper figures directory**: extracted images from the paper for
    visual inspection.

Recommended workflow:

1.  Download the paper PDF.
2.  Download the paper figures separately and store them in a dedicated
    folder.
3.  Convert the PDF into Markdown using a PDF-to-Markdown tool such as
    [MarkItDown Online](https://markitdown.online/).
4.  When providing inputs to the Skill, explicitly specify:
    -   which file is the original paper PDF;
    -   which file is the converted paper Markdown;
    -   which folder contains the paper figures.
5.  Read the Markdown version first to reduce token usage and improve
    navigation.
6.  When the Markdown conversion causes formula errors, table
    corruption, missing symbols, or other recognition failures, return
    to the original PDF for verification.
7.  After generating the final Markdown draft, use
    [wemd.app](https://edit.wemd.app/) for formatting and further
    editing before publishing to WeChat.

The PDF remains the final authority. Markdown is a reading and retrieval
layer rather than a replacement for the original paper.

``` text
Use $cea-wechat-writer to start the two-stage paper analysis workflow.
For now, collect inputs and perform Stage 1 only. Do not begin the full paper analysis or create the final output files.
Ask me for the absolute paths to the Skill, paper PDF, paper Markdown, and paper figures, and ask where to save the result.
I may reply "default" for the save location. Begin Stage 2 only after I explicitly authorise it.
```

### 4.2 Start a WeChat draft

``` text
Use $cea-wechat-writer to create a CEA WeChat Markdown draft from my source material.
First confirm the language, category, review mode, acronyms, fixed ending, and the caption decision for every figure and table.
Create only local Markdown and supporting files. Do not upload, create a WeChat platform draft, or publish.
```

## 5. Tutorial 1: two-stage paper analysis

### Step 0: prepare four paths

Prepare:

1.  the Skill directory;
2.  the paper PDF;
3.  Markdown converted from the same paper;
4.  the paper figures directory.

The result save location is a separate choice, not a fifth material
path. If no figures directory exists, reply `none`.

### Step 1: create the paper Markdown

If no `.md` file exists, convert the PDF at [MarkItDown
Online](https://markitdown.online/) and download the result locally.

> Confirm authorisation before uploading unpublished, copyrighted, or
> confidential papers to a third-party website. Converted Markdown is
> only a search and navigation aid. The PDF remains authoritative for
> formulas, tables, figures, footnotes, and complex layout.

### Step 2: complete the input form

The Skill's first response should ask only for inputs and should not
analyse the paper prematurely:

``` text
1. Skill directory:
2. Paper PDF:
3. Paper Markdown:
4. Paper figures directory:
5. Result save location: default
```

When asking for the paper Markdown path, simultaneously explain that
[MarkItDown Online](https://markitdown.online/) may be used if needed,
that third-party-upload permission must be confirmed for unpublished,
copyrighted, or confidential papers, and that the Skill will not upload
the paper silently.

If the Skill is already specified, Codex may echo its path and ask for
confirmation.

### Step 3: understand the default save location

When the user replies `default`:

-   the save directory is the directory containing the resolved
    `SKILL.md`;
-   the default files are `<paper PDF stem>_论文解读.md` and
    `<paper PDF stem>_编辑核查记录.md`;
-   Stage 1 creates no result file;
-   an existing file must trigger a rename or overwrite question and
    must never be overwritten silently.

If the user supplies `<repo-root>` as the Skill directory, the workflow
should still locate `<repo-root>/cea-wechat-writer/SKILL.md`; therefore,
the default output normally goes into `<repo-root>/cea-wechat-writer/`.
Provide a custom absolute path from the current machine if the result
should instead be stored at the project root or elsewhere.

### Step 4: review Stage 1

Stage 1 reads `SKILL.md` and all required references, templates,
scripts, and assets, then checks the PDF, Markdown, figures, and both
output paths. Its response contains only:

#### A. Task understanding

The two intended deliverables, the role of each paper source, the core
constraints, and the proposed output paths.

#### B. Proposed Markdown structure

A small number of broad sections adapted to the paper's actual design,
normally four to six level-two headings. A non-causal paper must not be
forced into a DID or RCT structure.

#### C. Decisions requiring confirmation

The default proposal is:

-   complete but focused analysis at a moderate length, without
    section-by-section retelling;
-   Chinese-first writing with English retained at the first appearance
    of a technical term;
-   balanced coverage of the question, theory, method, evidence,
    contribution, and limitations;
-   no external literature expansion by default;
-   close analysis only of core visuals that support the main argument;
-   natural attribution in the body, with detailed evidence and
    judgement mapping in the editor-review record.

The language must still be confirmed as Chinese, English,
Chinese-English, or Other. For Chinese-English, confirm every acronym's
English expansion, Chinese rendering, and first and subsequent display
rules before drafting. For `Other`, confirm the exact language, regional
variant or writing system, and whether it is monolingual or paired with
Chinese.

#### D. File-check results

The read status, format issues, source alignment, output conflicts, and
blockers for the Skill, PDF, Markdown, figures, and both output paths.

Stage 1 then stops. The following do not authorise Stage 2:

-   "received";
-   "continue checking";
-   supplying another file;
-   confirming only one path.

### Step 5: explicitly authorise Stage 2

To accept the defaults, reply:

``` text
Use the default plan and start Stage 2.
```

Custom example:

``` text
Use strict Chinese-English. Focus on the theoretical mechanisms, identification strategy, and research-design limitations.
Analyse only figures that affect the central conclusion, but do not embed images in the Markdown.
Start Stage 2 after the acronym confirmation is complete.
```

### Step 6: accept the final paper analysis

The final document should:

-   explain what the authors claim, why they take their approach, how
    they support it, and whether the evidence is sufficient;
-   explain the research question, motivation, gap, actual contribution,
    and limitations;
-   explain the purpose, variables, parameters, and argumentative role
    of equations;
-   explain each core figure's axes, result, intended claim, link to the
    research question, anomalies, and limitations;
-   report direction, magnitude, uncertainty, and practical meaning
    rather than only "significance";
-   locate material judgments in the original paper;
-   explain unresolved matters naturally when they affect understanding
    and record the detailed status in the editor-review file;
-   distinguish author views, paper evidence, and editorial judgement
    through concrete subjects;
-   contain no workflow labels, review states, Prompt/Skill commentary,
    or overly fragmented template headings.

A Chinese analysis will normally use about 3,000--5,000 Chinese
characters. Even a complex paper should usually stay within about 6,000
characters unless the user approves a longer treatment. Other languages
should preserve the same information density rather than mechanically
converting the character count.

The delivery message should identify the complete paths of the
reader-facing analysis and editor-review record, source files used,
unresolved or unparseable material, Skill-check status, and how any
Prompt--Skill conflict was handled.

## 6. Tutorial 2: CEA WeChat Markdown draft

### Step 1: provide source material

Inputs may include papers, Word documents, official webpages, conference
programmes, calls for papers, recruitment material, images, and user
notes. User notes are leads; material facts still require original or
official support.

### Step 2: complete pre-drafting confirmation

The Skill first confirms:

1.  language: Chinese, English, Chinese-English, or Other;
2.  one of the seven categories;
3.  regular or strict academic review, and whether a risk-bearing draft
    is allowed;
4.  fixed ending: no visible ending copy by default, only a bilingual
    hidden copy instruction;
5.  figure and table captions: after extracting and selecting visuals,
    list each number, content, proposed position, and proposed caption,
    then confirm add, omit, or revise and add.

Chinese-English mode also requires confirmation of every acronym's
English expansion, Chinese rendering, and first and subsequent display
rules.

When `Other` is selected, also confirm the exact language, regional
variant or writing system, and whether it is monolingual or paired with
Chinese.

A WeChat draft defaults to a complete long-form article, not a
few-hundred-word summary; use short-news mode only with explicit user
agreement.

### Step 3: create the standard directory

``` bash
python3 cea-wechat-writer/scripts/new_article.py \
  --output ./work/sample-article \
  --category 文章解读 \
  --language 中文 \
  --title "Working title"
```

Do not overwrite an existing non-empty directory without explicit
permission.

### Step 4: build the source ledger

Use hidden source anchors for material factual paragraphs:

``` markdown
The study uses firm-level panel data from 2010 to 2022.<!-- source:S1 -->
```

The matching `S1` entry in `sources.md` records the source, original
locator, supported facts, verification status, and image rights.
Conflicting sources are disclosed side by side rather than silently
resolved.

### Step 5: process images and captions

Prefer user images, figures from source materials, and official images.
AI artwork is used only when the author agrees, no suitable original
exists, and it adds genuine value.

Confirm each visual separately:

-   add a caption;
-   omit the caption;
-   revise and add the caption.

Record each decision as `user-confirmed-add` or `user-confirmed-omit`;
an unresolved `NEEDS_REVIEW` item must not enter the final draft.

Visible captions contain no punctuation. Put sources in bilingual hidden
comments. For table-cell line breaks, single words and short labels take
no punctuation, while complete sentences keep normal punctuation.

### Step 6: handle the fixed ending

The Markdown draft does not automatically generate visible Previous
Highlights, CEA/JCEBS introductions, or follow prompts. It contains only
a bilingual HTML comment instructing the editor to copy the complete
ending from a published post.

If the user explicitly requests the ending, use
[`approved-fixed-ending-copy.md`](cea-wechat-writer/references/approved-fixed-ending-copy.md)
verbatim.

The source joint-promotion asset is
[`扫码_搜索联合传播样式-标准色版.png`](cea-wechat-writer/assets/brand/扫码_搜索联合传播样式-标准色版.png).
The generated article copies and references it as
`assets/扫码_搜索联合传播样式-标准色版.png`.

### Step 7: run strict QA

``` bash
python3 cea-wechat-writer/scripts/qa_markdown.py \
  ./work/sample-article/article.md \
  --sources ./work/sample-article/sources.md \
  --report ./work/sample-article/qa-report.md \
  --strict
```

`BLOCK=0` means only that the structured checker found no blocking
issue. It does not replace review by the author, editor, or association.

Also complete the manual semantic review in
[`qa-policy.md`](cea-wechat-writer/references/qa-policy.md); the script
cannot replace fact checking, language editing, or academic judgement.

### Step 8: perform the pre-publication review

Read `README_BEFORE_PUBLISHING.md` and verify the facts, language, image
rights, QR code, hidden comments, fixed ending, and actual WeChat-editor
layout.

## 7. Mandatory CEA writing and layout rules

### 7.1 Facts and scientific language

-   Numbers, dates, authors, affiliations, roles, sample sizes, journal
    metrics, findings, venue information, and deadlines require sources.
-   Do not present association as causation.
-   Do not present one paper as a scholarly consensus.
-   Do not exaggerate robustness, external validity, or policy meaning.
-   Preserve risk when a fact cannot be verified; never fill it in
    speculatively.

### 7.2 Language and acronyms

-   Confirm language for every task.
-   Chinese-English means a strict parallel full text, not an English
    abstract.
-   Common acronyms still require interactive confirmation.
-   After Chinese is selected, use natural Chinese; introduce technical
    terms as "Chinese (English)" at first mention, then follow the
    confirmed display rule.

### 7.3 Editorial instructions

Every author or editor instruction must be a bilingual HTML comment and
must not appear as visible body text:

``` markdown
<!-- 请在公众号编辑器内补入固定结尾 / Add the fixed ending in the WeChat editor -->
```

### 7.4 Natural final copy

-   Reader-facing text does not expose workflow labels, review states,
    Prompt/Skill commentary, or explanations of the writing process.
-   Author views, paper evidence, and editorial judgement are attributed
    through concrete subjects rather than mechanical labels such as
    "analyst assessment."
-   Headings appear only when the topic genuinely changes; one-paragraph
    sections, stacked lists, excessive bold, and repeated summaries are
    merged or removed.
-   Review states, source mapping, conflicts, and unresolved items
    belong in the supporting review files.

See
[`natural-writing-and-clean-copy.md`](cea-wechat-writer/references/natural-writing-and-clean-copy.md)
for the complete rules.

## 8. Seven categories and five templates

  -----------------------------------------------------------------------
  Category                Default template        Core content
  ----------------------- ----------------------- -----------------------
  Article Interpretation  Research Explainer      Question, method,
                                                  findings, mechanisms,
                                                  and boundaries

  Academic Frontier       Method Frontier         Methods, models,
                                                  literature context, and
                                                  limitations

  Conference Notice       Notice/Opportunity      Dates, venue,
                                                  programme,
                                                  registration, or
                                                  submission

  Recent News             News Recap              Events, people,
                                                  organisational
                                                  progress, and
                                                  significance

  Association History     History/Profile         Memoirs, institutional
                                                  development, and
                                                  archives

  Special Issue           Notice/Opportunity      Theme, scope, editors,
                                                  deadlines, and
                                                  requirements

  Talent Recruitment      Notice/Opportunity      Roles, fields,
                                                  eligibility, materials,
                                                  and contacts
  -----------------------------------------------------------------------

See
[`category-and-template-guide.md`](cea-wechat-writer/references/category-and-template-guide.md)
for the detailed mapping.

## 9. Training data and historical corpus

### 9.1 Historical HTML

-   Crawler: [`training_data/craw.py`](training_data/craw.py)
-   Crawled output:
    [`training_data/train_by_category_html/`](training_data/train_by_category_html/)

Historical HTML is used to learn categories, structure, paragraph
rhythm, brand elements, and layout habits. Garbled or structurally
degraded content must not supply article facts.

### 9.2 Shijie material

-   [`training_data/train_by_Shijie_Word/`](training_data/train_by_Shijie_Word/)

These Word/PDF materials support language, writing, terminology,
structure, and layout learning. Email delivery does not automatically
establish public reuse rights; copyright and personal-information issues
still require review.

### 9.3 Training strategy

The project currently prioritises the Skill, templates, retrieval, and
QA rather than immediately fine-tuning a foundation model. The
recommended path is:

1.  generate a draft with the Skill;
2.  record author revisions and reasons;
3.  save draft--final pairs only when the user explicitly requests
    archival;
4.  maintain a fixed evaluation set;
5.  evaluate fine-tuning only when data volume, consistency, and
    permission are sufficient.

See
[`training-strategy.md`](cea-wechat-writer/references/training-strategy.md)
for details.

## 10. Scripts, examples, and validation

### 10.1 Main scripts

  -----------------------------------------------------------------------
  Script                              Purpose
  ----------------------------------- -----------------------------------
  `new_article.py`                    Create a standard WeChat article
                                      directory

  `retrieve_examples.py`              Retrieve usable historical examples
                                      by category and topic

  `qa_markdown.py`                    Check sources, images,
                                      placeholders, and blocking states

  `build_corpus.py`                   Rebuild the historical corpus index

  `archive_revision.py`               Save revision pairs only when the
                                      user explicitly requests archival
  -----------------------------------------------------------------------

Retrieval example:

``` bash
python3 cea-wechat-writer/scripts/retrieve_examples.py \
  --corpus cea-wechat-writer/references/corpus/index.json \
  --category 文章解读 \
  --query "research topic or title" \
  --limit 3
```

If the default retrieval returns fewer than three items, do not fill the
gap from another category and do not use `degraded_mojibake` body text;
rely on the formal template and quality rules instead.

### 10.2 Seven examples

Complete examples are available under
[`cea-wechat-writer/sample/`](cea-wechat-writer/sample/) and cover all
seven categories. Historical conference, special-issue, and recruitment
examples demonstrate structure only and must not be published as current
notices.

### 10.3 Validate the Skill

If the local Codex `skill-creator` validator is available, run:

``` bash
CEA_SKILL_CREATOR_ROOT="/path/to/skill-creator"

python3 "${CEA_SKILL_CREATOR_ROOT}/scripts/quick_validate.py" \
  ./cea-wechat-writer
```

The paths above are samples; replace them with the actual
`skill-creator` and repository locations in the current environment.
`quick_validate.py` requires Python and PyYAML. WeChat examples should
also be checked individually with `qa_markdown.py --strict`.

### 10.4 Compare source and installed copies

``` bash
CEA_REPO_ROOT="/path/to/CEA_Skill"
CEA_CODEX_SKILLS_ROOT="/path/to/.codex/skills"

diff -qr \
  --exclude='.DS_Store' \
  --exclude='__pycache__' \
  "${CEA_REPO_ROOT}/cea-wechat-writer" \
  "${CEA_CODEX_SKILLS_ROOT}/cea-wechat-writer"
```

No output means the two directories match apart from the excluded files.

## 11. Output files and publication boundary

Standard WeChat-mode output contains:

-   `article.md`: formatted body draft;
-   `sources.md`: fact and image-source ledger;
-   `qa-report.md`: automated and manual-review status;
-   `README_BEFORE_PUBLISHING.md`: bilingual pre-publication guide;
-   `assets/`: local images actually used.

Paper-analysis mode normally produces two Markdown files: a clean
reader-facing analysis and a separate record for author and editor
review.

Neither mode uploads or publishes automatically. In the WeChat editor,
the editor must still:

1.  manually add Previous Highlights and the approved fixed ending;
2.  check image dimensions, copyright, and portrait permissions;
3.  verify QR codes and links;
4.  confirm that HTML comments are hidden;
5.  perform a final visual preview.

## 12. Troubleshooting

### The Skill did not trigger

Write `$cea-wechat-writer` explicitly and provide the absolute path to
`cea-wechat-writer/SKILL.md`.

### The paper Markdown does not exist

Convert it at [MarkItDown Online](https://markitdown.online/) and
download it locally. Confirm third-party upload permission for sensitive
papers.

### The PDF and Markdown do not match

Use the PDF as the authority. A material mismatch blocks Stage 2 until
the Markdown is reconverted or the correct file is supplied.

### No figures directory exists

Reply `none`, then confirm whether figures may be checked or extracted
directly from the PDF.

### The default output already exists

The Skill must ask whether to rename or overwrite. A version suffix such
as `_v2.md` is recommended.

### QA reports a BLOCK

Read `qa-report.md` and resolve source, language, image, caption,
instruction, or fixed-ending problems. Override only when the user
explicitly accepts the specific risk; both `qa-report.md` and
`sources.md` must retain `USER_OVERRIDE`, the risk, the operator note,
and the time.

### A hidden comment appears in WeChat preview

Stop publication, inspect whether the editor transformed the HTML
comment, and repeat the rendered preview.

## 13. Sources and rights

This project referenced:

-   [`ref-duyi-wechat-skill-suite-main/`](ref-duyi-wechat-skill-suite-main/)

Training and analysis material includes:

-   [`training_data/craw.py`](training_data/craw.py)
-   [`training_data/train_by_category_html/`](training_data/train_by_category_html/)
-   [`training_data/train_by_Shijie_Word/`](training_data/train_by_Shijie_Word/)

These materials were used for category analysis, language training,
structural analysis, template development, layout learning, and
quality-control rules. Dynamic facts, image rights, contact details,
professional positions, and time-sensitive information in historical
material must not be treated as currently valid.

**CEA reserves all rights of interpretation regarding this project, the
Skill, and related documentation.**

------------------------------------------------------------------------

[阅读中文默认项目说明](README.md)
