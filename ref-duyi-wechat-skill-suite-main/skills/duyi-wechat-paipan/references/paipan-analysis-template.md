# Paipan Analysis Template

Create this file before formatting an article:

`{filename}-paipan-analysis.md`

The goal is strong mobile reading: protect the author's voice, then make the article easier to read on a phone.

## Required Output

```md
# 排版分析：{filename}

## 1. 文章主线

- 读者读完应该带走的一句话：
- 文章当前的推进顺序：
- 是否需要保留原顺序：是 / 否（layout-only 默认必须是）

## 2. 自然分节

| 位置 | 分节名/标记 | 为什么这里换挡 | 建议模块 |
|---|---|---|---|
| 开头第 X 段 | 例如：1 / ## Skill 是什么 | 场景进入观点 | G 数字章标 / A 小标题 |

Rules:
- "换挡" means topic, scene, argument layer, or emotional rhythm changes.
- Do not invent new arguments when naming sections.
- In layout-only mode, headings must come from existing source wording or neutral markers such as numbers.

## 3. 长段落诊断

| 原段落开头 | 问题 | 拆分建议 |
|---|---|---|
| ... | 同时讲了背景和判断 | 在 "...句子" 后断开 |

Diagnose only paragraphs that hurt mobile reading. Do not split just to create visual noise.

## 4. 独立成段候选

- `原句` -> 原因：转折 / 判断 / 节奏停顿 / 读者需要消化

These are sentences that should stand alone, not necessarily bold.

## 5. 加粗候选

- `原句` -> 原因：核心判断 / 行动建议 / 文章钉子

Bold only conclusions. Do not bold decorative words.

## 6. 图片与视觉休息点

| 位置 | 作用 | 建议 |
|---|---|---|
| 第 X 节后 | 让读者休息 / 增加证据 / 帮助理解 | 插入截图 / 小黑图 / 留空 |

Images must do one of three jobs: understanding, credibility, or rest.

## 7. 风格 preset 决策

- 推荐 preset：A / C / D / E / F / G
- 判断依据：
- 不选其他 preset 的原因：

## 8. 不改写检查

- 是否新增事实：否
- 是否删减观点：否
- 是否改变论证顺序：否
- 是否只改 presentation layer：是
```

## Decision Hints

- Choose A when the article is conversational and does not need visible structure.
- Choose C when beginner explanations are central.
- Choose D when the article is short and judgment-heavy.
- Choose E when the article has several logic modules, comparisons, or steps.
- Choose F for quiet weekly-note or reading-journal long reads.
- Choose G for narrative long reads that should use black numeric markers and low decoration.

## Hard Rules

- The analysis file is not optional for full-article formatting.
- Do not skip it because the article "looks simple".
- Do not use it to rewrite the author's ideas.
- If the source is too short, the analysis can be brief but must still state the style preset and no-rewrite status.
