# Obsidian Preview Gate

Use this gate only when the user explicitly asks for Obsidian preview, preview-only review, or local Markdown rhythm checking. In a complete `duyi-wechat` workflow, Obsidian preview is not a required stop before creating the WeChat draft.

## Purpose

Obsidian preview is a local content and rhythm review mode. It checks:

- whether the article still sounds like the author;
- whether paragraph breaks are comfortable;
- whether badge and image slots are in the right place;
- whether emphasis is restrained;
- whether the article is comfortable enough for local preview review.

It does not replace WeChat draft/mobile preview, which remains the final technical rendering check.

## Required Order

1. Generate `{filename}-paipan-analysis.md`.
2. Generate `{filename}-duyi-paipan.md`.
3. Add preview frontmatter to the final Markdown unless the file already has compatible frontmatter:
   ```yaml
   ---
   cssclasses:
     - wechat-preview
   ---
   ```
4. Insert the opening badge if enabled.
5. Insert generated images or explicit image slots.
6. Confirm the Obsidian CSS snippet is available and enabled when possible:
   ```bash
   obsidian snippets:enabled vault="<vault-name>"
   obsidian snippet:enable name=duyi-wechat-preview vault="<vault-name>"
   ```
   If the snippet is unavailable, install the packaged asset `assets/obsidian/duyi-wechat-preview.css` into the target vault's `.obsidian/snippets/` directory, then enable it. If installation is not possible, still open the Markdown, but treat it as a low-fidelity content/rhythm preview rather than a WeChat-like visual proof.
7. Open the final Markdown in Obsidian:
   ```bash
   python3 {skill_dir}/scripts/open_obsidian_preview.py {filename}-duyi-paipan.md
   ```
8. If the user asked for preview-only review, stop and wait for the user.
9. If this is part of a complete `duyi-wechat` workflow, treat Obsidian preview as optional local evidence and continue through HTML QA, screenshot check, dry-run, and draft creation.

## WeChat-like Obsidian Preview

When the `duyi-wechat-preview` snippet is enabled, use `cssclasses: [wechat-preview]` so Obsidian hides note properties/inline titles and renders the article body closer to a WeChat draft:

- 350px article column;
- title 22px;
- body 16px / 1.6 line-height / 2px letter spacing;
- black numeric section markers;
- full-width images inside the article column;
- table wrappers expanded to article width.

## Counter Rule

The public-record counter is read during Markdown generation but is not committed at this gate. Commit only after the article is confirmed published.

## Override

If the user explicitly asks to skip Obsidian preview, continue with HTML QA, screenshot check, dry-run, and draft creation when the current request targets the full draft-box workflow.
