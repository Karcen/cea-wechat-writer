---
name: duyi-wechat-fabu
description: "将微信公众号内容发送到草稿箱：普通文章走 WeChat API，贴图/图文和浏览器兜底走 Chrome CDP。用于发布公众号、发公众号草稿箱、上传公众号、贴图发布、生成手机预览、检查封面，或在 duyi-wechat-peitu 和 duyi-wechat-paipan 后完成最后发布步骤。"
---

# DUYI WeChat Fabu

把已经完成配图和排版的公众号内容送入微信公众号草稿箱。本 skill 是完整流程的最后一环：

`duyi-wechat-peitu` -> cover/body images  
`duyi-wechat-paipan` -> final Markdown -> WeChat-ready inline HTML  
`duyi-wechat-fabu` -> channel selection, local checks, draft creation, mobile preview checklist

发布后端使用 `scripts/wechat-posting-backend/`。Markdown 渲染使用本地 `wechat-md.ts`；浏览器控制使用本地 `wechat-chrome-cdp.ts`。

## 硬边界

- 作者名优先使用 CLI / 用户输入 / frontmatter / 账号配置；不要写死个人作者名。
- The workflow ends at the WeChat draft box.
- Prefer API publishing for normal articles.
- Use local Chrome CDP publishing for 贴图 and browser fallback.
- Cover is required only for API `news` articles and must be checked before draft creation.
- Run dry-run or browser preview before draft creation. Use `--submit` only when the current request context targets draft creation.
- Do not reformat the article here. If HTML is not ready, route back to `duyi-wechat-paipan`.
- In a complete `duyi-wechat` workflow or an explicit draft-box request, local QA and dry-run are the draft-box gate; do not ask for another approval before creating the draft.
- Do not add custom no-image 贴图 behavior in this phase unless the user explicitly asks for an extension.

## Channel Selection

| User intent | Backend | Script |
| --- | --- | --- |
| 普通公众号文章 / 草稿箱 | WeChat API | `wechat-api.ts` |
| 贴图 / 图文 / 有图短内容 | Chrome CDP | `wechat-browser.ts` |
| 普通文章但 API 不适合 | Chrome CDP | `wechat-article.ts` |
| 环境检查 | Local checks | `check-permissions.ts` |

## API Article Workflow

1. Check that the input is a WeChat-ready HTML file from `duyi-wechat-paipan`, ideally containing `#output`. Render Markdown with `render_wechat_html.py` before this step.
2. Resolve metadata:
   - title: CLI/user value -> `<title>` -> first `<h1>`.
   - author: CLI/user value -> frontmatter -> account config.
   - digest: CLI/user value -> first meaningful paragraph, trimmed.
3. Require a cover path. Check existence, image dimensions, file size, and rough Official Account suitability before `--submit`.
4. Run dry-run:
   ```bash
   cd {skill_dir}/scripts/wechat-posting-backend
   bun wechat-api.ts /absolute/path/article.html --cover /absolute/path/cover.png --author "作者名"
   ```
5. Review the dry-run report as an automatic gate: title, author, digest, content length, placeholder image count, cover path/existence, and account. Dry-run is the default and does not fetch tokens or call WeChat APIs.
   - `literalBackslashNCount` should be `0`.
   - `removedLiteralBackslashNCharsAtEdges` should be `0` after `duyi-wechat-paipan` rendering. If this is non-zero, the API guard removed a boundary artifact before it reached the draft.
   - If `literalBackslashNCount` remains non-zero, inspect the HTML manually before submitting, unless the article intentionally discusses escape characters such as `\n`.
6. If the current request context targets draft creation and the dry-run gate is clean, run:
   ```bash
   cd {skill_dir}/scripts/wechat-posting-backend
   bun wechat-api.ts /absolute/path/article.html --cover /absolute/path/cover.png --author "作者名" --submit
   ```
7. Report the resulting draft `media_id` and ask the user to check the phone preview in the WeChat Official Account app/backend.
8. After the user confirms the article was actually published, commit the public-record counter if it was used:
   ```bash
   python3 ../duyi-wechat-paipan/scripts/record_counter.py commit public_record
   ```

## Browser 贴图 Workflow

Use the local Chrome CDP path for image-text/贴图:

```bash
cd {skill_dir}/scripts/wechat-posting-backend
bun wechat-browser.ts --markdown /absolute/path/article.md --images /absolute/path/images
```

Explicit title/content mode:

```bash
cd {skill_dir}/scripts/wechat-posting-backend
bun wechat-browser.ts \
  --title "短标题" \
  --content "短内容" \
  --image /absolute/path/image.png
```

Actual draft creation:

```bash
cd {skill_dir}/scripts/wechat-posting-backend
bun wechat-browser.ts \
  --title "短标题" \
  --content "短内容" \
  --image /absolute/path/image.png \
  --submit
```

Browser mode opens or reuses an isolated Chrome profile and may require QR login. Without `--submit`, it composes in preview mode only.

## Browser Article Fallback

Use only when API publishing is unsuitable:

```bash
cd {skill_dir}/scripts/wechat-posting-backend
bun wechat-article.ts --html /absolute/path/article.html
```

Actual draft creation:

```bash
cd {skill_dir}/scripts/wechat-posting-backend
bun wechat-article.ts --html /absolute/path/article.html --submit
```

## API Article Commands

Use explicit metadata when the title or digest matters:

```bash
cd {skill_dir}/scripts/wechat-posting-backend
bun wechat-api.ts /absolute/path/article.html \
  --cover /absolute/path/cover.png \
  --title "文章标题" \
  --summary "一句话摘要" \
  --author "作者名"
```

Actual draft creation:

```bash
cd {skill_dir}/scripts/wechat-posting-backend
bun wechat-api.ts /absolute/path/article.html \
  --cover /absolute/path/cover.png \
  --title "文章标题" \
  --summary "一句话摘要" \
  --author "作者名" \
  --submit
```

## Credentials

The backend reads API credentials and browser/account preferences from environment variables or local config files:

- `WECHAT_APP_ID`
- `WECHAT_APP_SECRET`

Config file search order:

1. Environment variables
2. account config in `.wechat-article-suite/wechat-fabu/EXTEND.md`
3. `<cwd>/.wechat-article-suite/.env`
4. `~/.wechat-article-suite/.env`

Chrome CDP publishing uses the selected account's isolated Chrome profile from `EXTEND.md`, or an auto-generated `~/.wechat-article-suite/chrome-profile` profile when no explicit profile is set.

## Output

In preview-only or dry-run-only mode, report whether the draft is ready to create and what still needs checking.

After `--submit`, report:

- draft saved or failed
- `media_id`
- title
- author
- cover path
- local images uploaded
- phone preview status or next check

## References

This split skill keeps publishing rules in this file. Do not look for merged `duyi-wechat` release references.
