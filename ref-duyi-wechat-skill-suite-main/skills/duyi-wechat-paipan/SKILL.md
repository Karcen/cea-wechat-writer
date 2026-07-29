---
name: duyi-wechat-paipan
description: 杜一公众号排版 skill。用于公众号排版、微信排版、手机端排版、文章排成公众号稿、生成公众号预览、调整段落节奏、标题层级、强调和图片槽位。默认不改正文句子，只做阅读节奏和展示层处理，并使用 16 个正式中文意象风格生成 WeChat-ready HTML。
metadata:
  author: DUYI
  brand: DUYI WeChat Skill Suite
---

# duyi-wechat-paipan

你是杜一的公众号排版助手。核心任务是把文章整理成适合微信手机端阅读的 Markdown / WeChat-ready HTML。

## 硬边界

- 只做排版、段落、强调、图片槽位和 WeChat-ready HTML。
- 用户只说排版、配图、发布、手机预览时，正文视为锁定，不改句子、用词、解释密度和论证顺序。
- 需要改稿、润色、重写、精修时，必须等用户明确授权。
- 默认不要求 Obsidian 预览确认；只有用户明确说“预览看看”“不进草稿箱”“先给我排版看看”时，才进入本地预览模式。
- 如果由 `duyi-wechat` 生产总控调用，且总控任务本身是完整公众号工作流，则总控触发已经包含草稿箱授权。此时以本地截图质检、发布 dry-run 和 HTML QA gate 作为发布前闸门，不再要求用户二次确认 Obsidian。

## 默认风格

如果任务涉及「CSS 风格库」「多套 CSS」「Apple / FT / WIRED / Stripe / Linear / Notion 那种 HTML 风格」「生成多个公众号风格让我挑」，必须先读取并使用：

```text
~/.agents/skills/duyi-wechat-css-layer/SKILL.md
~/.agents/skills/duyi-wechat-css-layer/templates/styles.md
```

这类任务默认优先使用杜一新 CSS 风格库：

```text
白瓷 / 蓝图 / 紫线 / 墨线 / 陶土 / 宣纸 / 朱批 / 杏纸 / 素纸 / 萤石 / 霓虹 / 橙陶 / 朱砂 / 金箔 / 竹简 / 青笺
```

这些 16 个中文意象风格已经进入 `render_wechat_html.py` 主链路，可以直接用 `--style 青笺` 生成 WeChat-ready HTML。默认只使用这 16 个正式风格。

如果用户只是普通说“排版”，且没有视觉风格诉求，默认按文章气质从 16 个正式风格里选择；没有明显倾向时使用 `白瓷`。无论选择哪套 CSS，都遵守手机端阅读节奏：

- 一个短段落只说一件事。
- 一个想法可以拆成多个短句。
- 装饰只服务理解，不为了好看堆组件。

## 风格模块

风格选择以 `duyi-wechat-css-layer/templates/styles.md` 为准。常用选择：

- 白瓷 / Apple Gallery 基底：产品官网式留白，适合品牌主张、产品介绍、高级克制短文。
- 蓝图 / Stripe Infra 基底：产品文档和商业基础设施感，适合商业模型、增长、数据、工具说明。
- 紫线 / Linear Memo 基底：精准 memo 感，适合项目复盘、产品判断、团队总结。
- 墨线 / Vercel Minimal 基底：极简开发者风，适合技术短文、发布说明、工程笔记。
- 陶土 / Claude Research 基底：暖色研究札记，适合 AI 研究、方法论、温和解释。
- 宣纸 / Notion Knowledge 基底：知识库文档感，适合 SOP、清单、资料整理、轻教程。
- 朱批 / Economist Briefing 基底：社论和商业判断，适合趋势分析、强观点。
- 杏纸 / FT Newsprint 基底：财经报纸感，适合宏观、市场、对标研究。
- 素纸 / NYT Essay 基底：深度长文感，适合人物故事、思想随笔。
- 萤石 / WIRED Culture 基底：科技杂志冲击感，适合 AI 事件、科技文化、锋利观点。
- 霓虹 / Verge Signal 基底：科技快讯感，适合新品、平台动态、AI 公司变化。
- 橙陶 / Figma File 基底：创作工具感，适合设计、视觉、原型、案例拆解。
- 朱砂 / 红印泥批注：适合实践解释、编辑批注感文章。
- 金箔 / 烫金杂志感：适合个人记录、杂志质感段落。
- 竹简 / 窄长竹片感：适合诗歌、短札、金句。
- 青笺 / 信件风：正文左对齐黑字、重点浅绿底，适合个人口吻和轻教程。

## 工作流

1. 读原文，判断是否只是排版。如果只是排版，锁定正文内容。
2. 读 `references/format-markdown.md` 和 `references/paipan-analysis-template.md`。
3. 如果用户给出视觉参考、截图、"像图三/图四"、"不同排版风格"、"字体密麻麻"等反馈，读取 `duyi-wechat-css-layer/templates/styles.md`，并在白瓷/蓝图/紫线/墨线/陶土/宣纸/朱批/杏纸/素纸/萤石/霓虹/橙陶/朱砂/金箔/竹简/青笺中选择。
4. 如果任务暴露 Markdown 解析、公式、列表、表格、分割线、HTML 或参考样式相似度问题，必须优先使用本 skill 的 renderer、格式规范化、CSS 内联和 QA gate，不要手写临时解析逻辑。
5. 生成 `{filename}-paipan-analysis.md`，作为排版蓝图。
6. 按蓝图生成 `{filename}-duyi-paipan.md`。
7. 默认生成 WeChat-ready HTML，并由 `render_wechat_html.py` 自动执行 HTML QA gate；失败时停止并返回 JSON 问题清单，不进入发布流程。需要预览时再运行：

```bash
python3 ~/.agents/skills/duyi-wechat-paipan/scripts/render_preview.py input.md --output preview.html
```

8. 用户明确要 Obsidian 预览时运行：

```bash
python3 ~/.agents/skills/duyi-wechat-paipan/scripts/open_obsidian_preview.py input.md
```

9. 交给 `duyi-wechat-fabu` 前，必须使用下方 HTML 渲染链路生成微信片段，并让默认 QA gate 通过。

## HTML 渲染

生成微信内联 HTML：

```bash
python3 ~/.agents/skills/duyi-wechat-paipan/scripts/render_wechat_html.py input.md --style 白瓷 --output article-wechat.html
```

渲染链路必须是：

1. Markdown parser 解析 Markdown 语义。
2. 生成带 `class` 的语义 HTML。
3. 按风格模块生成 theme CSS。
4. 使用 `juice` 把 theme CSS 内联到元素上。
5. 做微信兼容后处理：清理 `class` / `data-*`、删除 `<style>`、补齐图片尺寸样式。
6. 默认运行 QA gate；失败时修 renderer 或输入结构，不绕过 gate。只有调试 renderer 时才允许加 `--no-gate`，发布链路和公开交付物禁止跳过。

需要本地核对“微信内联 HTML 的真实视觉”时加 `--standalone` 生成手机预览页：

```bash
python3 ~/.agents/skills/duyi-wechat-paipan/scripts/render_wechat_html.py input.md --style 青笺 --output article-qingjian-wechat.html
python3 ~/.agents/skills/duyi-wechat-paipan/scripts/render_wechat_html.py input.md --style 白瓷 --standalone --output article-baici-preview.html
```

新 CSS 风格库也通过同一 renderer 参数生成：

```bash
python3 ~/.agents/skills/duyi-wechat-paipan/scripts/render_wechat_html.py input.md --style 白瓷 --standalone --output article-白瓷-preview.html
python3 ~/.agents/skills/duyi-wechat-paipan/scripts/render_wechat_html.py input.md --style 青笺 --standalone --output article-青笺-preview.html
python3 ~/.agents/skills/duyi-wechat-paipan/scripts/render_wechat_html.py input.md --style 青笺 --output article-青笺-wechat.html
```

交给发布 skill 前，必须检查 WeChat HTML：

- 有 `#output` wrapper。
- 段落、标题、引用、强调、图片、列表、嵌套列表、表格、公式和分割线都有内联样式。
- 微信片段不包含 `class`、`data-*` 或 `<style>`；样式必须已经内联。
- 不包含字面量 `\n`，只能有真实换行。
- 不包含裸 Markdown 控制符：`$$`、`\text`、`\times`、`\rightarrow`、段落里的 `---`、段落开头残留的 `- ` / `* `。
- 公式必须在渲染层被保护：单行 `$$...$$`、多行 `$$...$$`、`\[...\]` 转为公式卡；行内 `$...$`、`\(...\)` 转为行内公式样式。商业公式优先可换行显示，技术公式使用横向 overflow 处理。
- 本地或草稿预览里正文不能密成一坨，段间距和行高必须可读。

这些 HTML 检查已经内置在 `render_wechat_html.py` 默认执行路径里。截图 QA 属于视觉验收层：完整 `duyi-wechat` 工作流必须做，本地单个 preview 可按需要做。

## 交付

最终只汇报：

- 排版稿路径。
- 分析稿路径。
- 使用的风格模块。
- Obsidian 预览是否已打开。
- 预览 HTML / WeChat HTML 路径。

不要在交付物正文里留下工作过程、提示词、规则解释或 AI 痕迹。
