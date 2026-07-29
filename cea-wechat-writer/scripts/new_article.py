#!/usr/bin/env python3
"""Create a non-destructive CEA article workspace from the matching template."""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
from pathlib import Path


TEMPLATES = {
    "文章解读": "01-research-explainer.md",
    "学术前沿": "02-frontier-tutorial.md",
    "会议通知": "03-notice-opportunity.md",
    "特刊推荐": "03-notice-opportunity.md",
    "广纳英才": "03-notice-opportunity.md",
    "新近动态": "04-association-news.md",
    "学会历史": "05-history-profile.md",
}
LANGUAGE_ALIASES = {"简体中文": "中文", "中英双语": "中英文"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--category", choices=tuple(TEMPLATES), required=True)
    parser.add_argument("--language", choices=("中文", "英文", "中英文", "其他", "简体中文", "中英双语"), required=True)
    parser.add_argument("--other-language", help="选择“其他”时必填：具体语言、地区变体/文字体系和单双语方式")
    parser.add_argument("--title", required=True)
    args = parser.parse_args()
    language = LANGUAGE_ALIASES.get(args.language, args.language)
    if language == "其他" and not args.other_language:
        parser.error("--other-language is required when --language 其他")
    if language != "其他" and args.other_language:
        parser.error("--other-language can only be used with --language 其他")

    output = args.output.resolve()
    if output.exists() and any(output.iterdir()):
        parser.error(f"output directory is not empty: {output}")
    output.mkdir(parents=True, exist_ok=True)
    assets = output / "assets"
    assets.mkdir(exist_ok=True)

    skill = Path(__file__).resolve().parent.parent
    template_path = skill / "assets" / "templates" / TEMPLATES[args.category]
    article = template_path.read_text(encoding="utf-8")
    footer = (skill / "assets" / "templates" / "00-cea-standard-footer.md").read_text(encoding="utf-8").strip()
    article = article.replace("{{CEA_STANDARD_FOOTER}}", footer)
    article = article.replace("{{LANGUAGE}}", language)
    article = article.replace("{{会议通知/特刊推荐/广纳英才}}", args.category)
    article = article.replace("{{传播标题}}", args.title)
    article = article.replace("{{方法或工具标题}}", args.title)
    article = article.replace("{{准确、包含关键行动的标题}}", args.title)
    article = article.replace("{{新闻标题}}", args.title)
    article = article.replace("{{历史或人物标题}}", args.title)
    metadata = []
    if language == "其他":
        metadata.append(f"<!-- other-language: {args.other_language} -->")
    if language == "中英文":
        metadata.extend([
            "<!-- bilingual-mode: strict-parallel -->",
            "<!-- abbreviation-policy: pending-user-confirmation -->",
        ])
    if metadata:
        language_marker = f"<!-- language: {language} -->"
        article = article.replace(language_marker, language_marker + "\n" + "\n".join(metadata), 1)
    (output / "article.md").write_text(article, encoding="utf-8")

    created = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    sources = (skill / "assets" / "templates" / "sources-template.md").read_text(encoding="utf-8")
    sources = sources.replace("{{TITLE}}", args.title).replace("{{CATEGORY}}", args.category)
    sources = sources.replace("{{LANGUAGE}}", language).replace("{{CREATED_AT}}", created)
    if language == "中英文":
        sources += (
            "\n## 用户确认的缩写表 / User-confirmed Abbreviations\n\n"
            "- 状态：NEEDS_REVIEW\n\n"
            "| 缩写 | English full form | 中文译名 | 首次/后续展示规则 |\n"
            "|---|---|---|---|\n"
            "| {{待用户确认}} |  |  |  |\n"
        )
    (output / "sources.md").write_text(sources, encoding="utf-8")

    qa = (skill / "assets" / "templates" / "qa-report-template.md").read_text(encoding="utf-8")
    qa = qa.replace("{{TITLE}}", args.title).replace("{{CATEGORY}}", args.category)
    qa = qa.replace("{{LANGUAGE}}", language)
    (output / "qa-report.md").write_text(qa, encoding="utf-8")

    publication_readme = (
        skill / "assets" / "templates" / "README_BEFORE_PUBLISHING-template.md"
    ).read_text(encoding="utf-8")
    publication_readme = publication_readme.replace("{{TITLE}}", args.title)
    publication_readme = publication_readme.replace("{{CATEGORY}}", args.category)
    publication_readme = publication_readme.replace("{{LANGUAGE}}", language)
    publication_readme = publication_readme.replace("{{CREATED_AT}}", created)
    (output / "README_BEFORE_PUBLISHING.md").write_text(publication_readme, encoding="utf-8")

    qr = skill / "assets" / "brand" / "扫码_搜索联合传播样式-标准色版.png"
    if qr.exists():
        shutil.copy2(qr, assets / "扫码_搜索联合传播样式-标准色版.png")

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
