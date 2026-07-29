#!/usr/bin/env python3
"""Run deterministic structure/source/image checks for a CEA Markdown draft."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path


SOURCE_ANCHOR_RE = re.compile(r"<!--\s*source:([A-Za-z0-9_, -]+)\s*-->")
SOURCE_HEADING_RE = re.compile(r"^##\s+(S\d+)\s*$", re.MULTILINE)
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
IMAGE_SOURCE_RE = re.compile(r"<!--\s*image-source:\s*.+?-->", re.DOTALL)
CAPTION_DECISION_RE = re.compile(r"<!--\s*caption-decision:\s*([a-z-]+|NEEDS_REVIEW)\s*-->")
TABLE_CAPTION_DECISION_RE = re.compile(r"<!--\s*table-caption-decision:\s*([a-z-]+|NEEDS_REVIEW)\s*-->")
CAPTION_RE = re.compile(
    r"^_\s*((?:图|表)\s*\d+|(?:Figure|Table)\s+\d+)\s+(.+?)\s*_\s*$",
    re.IGNORECASE | re.MULTILINE,
)
CAPTION_PUNCTUATION_RE = re.compile(r"""[，。！？；：、,.!?;:…“”‘’"'（）()【】\[\]{}《》〈〉—–\-／/\\·%％&+]""")
TABLE_BREAK_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
TRAILING_PUNCTUATION_RE = re.compile(r"""[，。！？；：、,.!?;:…]+$""")
NUMBER_RE = re.compile(r"(?:19|20)\d{2}|\d+(?:\.\d+)?\s*%|\d+\s*[—–-]\s*\d+|\b\d{2,}\b")
ACRONYM_RE = re.compile(r"\b[A-Z][A-Z0-9&-]{1,14}\b")
OVERCLAIMS = ("首次证明", "彻底解决", "完全证实", "必然导致", "毫无疑问", "颠覆性")
MIN_CJK = {
    "文章解读": 2400, "学术前沿": 2200, "会议通知": 1500,
    "新近动态": 1700, "学会历史": 2400, "特刊推荐": 1500,
    "广纳英才": 1500, "人才招聘": 1500,
}
REQUIRED_SECTION_GROUPS = {
    "文章解读": (("文章信息",), ("研究问题",), ("数据与方法", "方法简介"), ("核心结论",),
                 ("文章贡献",), ("稳健性", "结论讨论"), ("实践意义",), ("未来研究",)),
    "学术前沿": (("问题场景",), ("核心直觉", "核心原理"), ("前提与假设", "核心假设"),
                 ("操作步骤", "实现步骤"), ("示例", "代码"), ("相近方法", "方法比较"),
                 ("限制", "常见误区"), ("复现",)),
    "会议通知": (("关键信息",), ("背景", "主题"), ("面向对象", "征稿范围"),
                 ("重要日程", "会议日程"), ("如何参与", "报名", "投稿")),
    "特刊推荐": (("关键信息", "历史征稿信息"), ("背景", "主题"), ("面向对象", "研究问题", "选题"),
                 ("重要日程", "关键日期", "当前征稿"), ("如何参与", "投稿")),
    "广纳英才": (("招聘方向", "机构与方向"), ("岗位",), ("申请条件", "资格"),
                 ("申请材料",), ("申请流程", "如何申请")),
    "人才招聘": (("招聘方向", "机构与方向"), ("岗位",), ("申请条件", "资格"),
                 ("申请材料",), ("申请流程", "如何申请")),
    "新近动态": (("事件概况", "会议概况"), ("关键内容", "主要环节", "学术议题"),
                 ("为什么重要", "意义"), ("后续安排", "学会进展")),
    "学会历史": (("人物与时代背景", "人物与材料", "背景"), ("关键历程", "时间线", "联系"),
                 ("与CEA的关系", "与 CEA 的关系", "学术共同体"), ("历史意义",),
                 ("资料边界", "史料边界")),
}
FOOTER_MARKERS = (
    "从已发布的往期文章复制完整固定结尾",
    "copy the complete fixed ending from a previously published article",
    "扫码_搜索联合传播样式-标准色版.png",
)
VISIBLE_EDITORIAL_PROMPT_RE = re.compile(
    r"发布前(?:提醒|二次检查|必须)|时效警告|编辑提示|Editor(?:'s)? note|"
    r"待办|待确认|NEEDS_REVIEW|请核对|请确认",
    re.IGNORECASE,
)
PROMPT_COMMENT_RE = re.compile(
    r"编辑提示|Editor(?:'s)? note|发布前|Before publication|提醒|警告|"
    r"为方便起见|For convenience|待办|TODO",
    re.IGNORECASE,
)
LANGUAGE_ALIASES = {"简体中文": "中文", "中英双语": "中英文"}
LANGUAGES = {"中文", "英文", "中英文", "其他"}


def add_issue(issues: list[dict], level: str, item: str, detail: str) -> None:
    issues.append({"level": level, "item": item, "detail": detail})


def meaningful_paragraphs(text: str) -> list[str]:
    paragraphs = []
    for paragraph in re.split(r"\n\s*\n", text):
        value = paragraph.strip()
        if not value or value.startswith(("<!--", "#", "![", "```")):
            continue
        paragraphs.append(value)
    return paragraphs


def render_report(article: Path, sources: Path, issues: list[dict], override: str | None) -> str:
    blockers = [issue for issue in issues if issue["level"] == "BLOCK"]
    warnings = [issue for issue in issues if issue["level"] == "WARN"]
    if blockers and override:
        status = "USER_OVERRIDDEN_REVIEW_REQUIRED"
    elif blockers:
        status = "BLOCKED_NEEDS_REVIEW"
    else:
        status = "READY_FOR_AUTHOR_REVIEW"
    lines = [
        "# 二次检查报告", "", f"- 文章：`{article}`", f"- 来源台账：`{sources}`",
        f"- 检查时间：{dt.datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"- 总体状态：**{status}**", f"- BLOCK：{len(blockers)}", f"- WARN：{len(warnings)}", "",
        "## 自动检查结果", "", "| 级别 | 检查项 | 说明 |", "|---|---|---|",
    ]
    if issues:
        for issue in issues:
            detail = issue["detail"].replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {issue['level']} | {issue['item']} | {detail} |")
    else:
        lines.append("| PASS | 结构化检查 | 未发现自动检查问题 |")
    lines.extend([
        "", "## 必须人工二次检查", "",
        "- [ ] 数字、日期、样本量与来源逐项一致",
        "- [ ] 作者姓名、单位和职务来自原文或当前官方页面",
        "- [ ] 研究方法、显著性、效应量与因果表述准确",
        "- [ ] 图表编号、图注和正文解释与原文一致",
        "- [ ] 图片来源、权利和AI生成状态明确",
        "- [ ] 会议/特刊/岗位的日期、地点、费用、链接和联系人仍有效",
        "- [ ] 语言选项已由用户明确确认；“其他”语言的具体要求已记录",
        "- [ ] 中英文稿逐项保持严格平行双语，不是英文摘要或局部翻译",
        "- [ ] 中英文稿全部缩写的全称、中文译名和展示规则已由用户确认",
        "- [ ] 已完成错别字、语病、重复和标题党检查",
        "- [ ] CEA/JCEBS动态指标、二维码和账号信息已重新核验",
        "- [ ] 正文达到栏目所需深度，每个章节都有新事实、解释或行动信息",
        "- [ ] Markdown未自动生成往期文章、CEA/JCEBS介绍或关注提示",
        "- [ ] 已保留中英文注释，提示从已发布往期文章复制完整固定结尾",
        "- [ ] 所有作者或编辑提示只存在于中英文 HTML 注释中",
        "- [ ] 已生成并阅读中英文 README_BEFORE_PUBLISHING.md",
        "- [ ] 图片可见图注不显示来源；隐藏来源批注和图片台账完整",
        "- [ ] 图和表的可见图注完全不含标点",
        "- [ ] 每个图和表是否显示图注均已由用户逐项确认并记录",
        "- [ ] 表格换行内容已按语义处理标点：词语和短标签不加，完整句保留必要标点",
        "", "## 用户强制通过记录", "",
    ])
    if override:
        lines.extend([
            f"- 状态：USER_OVERRIDE", f"- 授权说明：{override}",
            f"- 时间：{dt.datetime.now().astimezone().isoformat(timespec='seconds')}",
            "- 注意：原始风险保留；本状态不等于事实已核实或正式发布批准。",
        ])
    else:
        lines.append("无。")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("article", type=Path)
    parser.add_argument("--sources", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--override")
    args = parser.parse_args()

    article_path = args.article.resolve()
    sources_path = args.sources.resolve()
    article = article_path.read_text(encoding="utf-8")
    sources = sources_path.read_text(encoding="utf-8")
    issues: list[dict] = []

    publication_readme = article_path.parent / "README_BEFORE_PUBLISHING.md"
    if not publication_readme.is_file():
        add_issue(issues, "BLOCK", "发表前阅读文档", "缺少中英文 README_BEFORE_PUBLISHING.md")
    else:
        publication_readme_text = publication_readme.read_text(encoding="utf-8")
        if not re.search(r"[\u4e00-\u9fff]", publication_readme_text) or not re.search(r"[A-Za-z]", publication_readme_text):
            add_issue(issues, "BLOCK", "发表前阅读文档", "README_BEFORE_PUBLISHING.md 必须同时包含中文和英文")

    if "{{" in article or "}}" in article:
        add_issue(issues, "BLOCK", "模板占位符", "article.md 仍有未替换的 {{...}} 占位符")
    language_match = re.search(r"<!--\s*language:\s*([^>]+)-->", article)
    language_raw = language_match.group(1).strip() if language_match else ""
    language = LANGUAGE_ALIASES.get(language_raw, language_raw)
    if language not in LANGUAGES:
        add_issue(issues, "BLOCK", "语言选择", "缺少用户确认的语言元数据")
    elif language == "其他" and not re.search(r"<!--\s*other-language:\s*\S.+?-->", article):
        add_issue(issues, "BLOCK", "其他语言", "选择“其他”后必须记录具体语言、地区变体/文字体系和单双语方式")
    elif language == "中英文":
        if "<!-- bilingual-mode: strict-parallel -->" not in article:
            add_issue(issues, "BLOCK", "严格中英文", "缺少 bilingual-mode: strict-parallel 元数据")
        if "<!-- abbreviation-policy: user-confirmed -->" not in article:
            add_issue(issues, "BLOCK", "缩写确认", "缺少 abbreviation-policy: user-confirmed 元数据")
        abbreviation_section = re.search(
            r"^##\s+用户确认的缩写表\s*/\s*User-confirmed Abbreviations\s*$"
            r"(.*?)(?=^##\s|\Z)", sources, re.MULTILINE | re.DOTALL,
        )
        if not abbreviation_section or "状态：USER_CONFIRMED" not in abbreviation_section.group(1):
            add_issue(issues, "BLOCK", "缩写确认", "sources.md 缺少状态为 USER_CONFIRMED 的用户确认缩写表")
        else:
            confirmed = set(re.findall(r"^\|\s*([A-Z][A-Z0-9&-]{1,14})\s*\|", abbreviation_section.group(1), re.MULTILINE))
            visible = re.sub(r"<!--.*?-->", "", article, flags=re.DOTALL)
            visible = re.sub(r"```.*?```", "", visible, flags=re.DOTALL)
            visible = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", visible)
            visible = re.sub(r"\]\([^)]+\)", "]", visible)
            used_acronyms = {item for item in ACRONYM_RE.findall(visible) if not re.fullmatch(r"S\d+", item)}
            missing_acronyms = sorted(used_acronyms - confirmed)
            if missing_acronyms:
                add_issue(
                    issues, "BLOCK", "未确认缩写",
                    "以下可见缩写未列入用户确认表：" + ", ".join(missing_acronyms),
                )
        bilingual_visible = re.sub(r"<!--.*?-->", "", article, flags=re.DOTALL)
        bilingual_visible = re.sub(r"```.*?```", "", bilingual_visible, flags=re.DOTALL)
        bilingual_visible = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", bilingual_visible)
        cjk_total = sum("\u4e00" <= char <= "\u9fff" for char in bilingual_visible)
        latin_total = sum(("A" <= char <= "Z") or ("a" <= char <= "z") for char in bilingual_visible)
        if cjk_total == 0 or latin_total < max(80, int(cjk_total * 0.35)):
            add_issue(
                issues, "BLOCK", "严格双语覆盖",
                f"全文中文约{cjk_total}字、英文字母约{latin_total}个；英文覆盖不足以构成严格平行全文",
            )
        bilingual_headings = re.findall(r"^#{1,6}\s+(.+)$", bilingual_visible, re.MULTILINE)
        unpaired_headings = [
            heading.strip() for heading in bilingual_headings
            if not re.search(r"[\u4e00-\u9fff]", heading) or not re.search(r"[a-z]", heading)
        ]
        if unpaired_headings:
            add_issue(
                issues, "BLOCK", "双语标题层级",
                "以下标题缺少中文或英文对应项：" + "；".join(unpaired_headings[:8]),
            )

    category_match = re.search(r"<!--\s*category:\s*([^>]+)-->", article)
    category = category_match.group(1).strip() if category_match else ""
    if category not in MIN_CJK:
        add_issue(issues, "BLOCK", "栏目元数据", "缺少有效的栏目元数据，无法执行栏目深度检查")
    else:
        short_approved = bool(re.search(r"<!--\s*length-mode:\s*short-brief-approved\s*-->", article))
        body = article.split("## 关于CEA", 1)[0]
        body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
        cjk_count = sum("\u4e00" <= char <= "\u9fff" for char in body)
        minimum = MIN_CJK[category]
        if cjk_count < minimum and not short_approved:
            add_issue(
                issues, "BLOCK" if args.strict else "WARN", "正文深度",
                f"{category}正文约{cjk_count}个汉字，低于严格模式最低值{minimum}；不得用短摘要替代完整成稿",
            )
        headings = [item.strip() for item in re.findall(r"^##\s+(.+)$", article, re.MULTILINE)]
        missing_groups = []
        for alternatives in REQUIRED_SECTION_GROUPS.get(category, ()):
            if not any(any(keyword in heading for keyword in alternatives) for heading in headings):
                missing_groups.append("/".join(alternatives))
        if missing_groups:
            add_issue(issues, "BLOCK" if args.strict else "WARN", "栏目完整度", f"缺少必需章节：{', '.join(missing_groups)}")

    missing_footer = [marker for marker in FOOTER_MARKERS if marker not in article]
    if missing_footer:
        add_issue(issues, "BLOCK", "CEA固定结尾", f"缺少固定结尾组件：{', '.join(missing_footer)}")
    fixed_ending_override = "<!-- fixed-ending-mode: user-requested-approved-copy -->" in article
    visible_fixed_ending_markers = (
        "## 往期精彩文章",
        "## 往期精彩文章 / Previous Highlights",
        "## 关于CEA",
        "## 关于JCEBS",
        "欢迎点击下方关注我们官方公众号",
        "欢迎点击下方二维码关注",
    )
    visible_fixed_ending = [marker for marker in visible_fixed_ending_markers if marker in article]
    if visible_fixed_ending and not fixed_ending_override:
        add_issue(
            issues, "BLOCK", "固定结尾可见",
            "Markdown初稿不得自动生成以下结尾内容，应从往期文章复制：" + ", ".join(visible_fixed_ending),
        )
    if fixed_ending_override:
        approved_copy = (
            Path(__file__).resolve().parent.parent
            / "references" / "approved-fixed-ending-copy.md"
        ).read_text(encoding="utf-8")
        approved_cea = re.search(r"^## CEA 介绍\s*\n\n(.+)$", approved_copy, re.MULTILINE)
        approved_jcebs = re.search(r"^## JCEBS 介绍\s*\n\n(.+)$", approved_copy, re.MULTILINE)
        missing_approved = []
        for label, match in (("CEA介绍", approved_cea), ("JCEBS介绍", approved_jcebs)):
            if match and match.group(1).strip() not in article:
                missing_approved.append(label)
        if missing_approved:
            add_issue(
                issues, "BLOCK", "核准结尾文案",
                "用户要求写入固定介绍时必须逐字采用核准文案，缺少或改写：" + ", ".join(missing_approved),
            )

    visible_article = re.sub(r"<!--.*?-->", "", article, flags=re.DOTALL)
    visible_prompt = VISIBLE_EDITORIAL_PROMPT_RE.search(visible_article)
    if visible_prompt:
        excerpt_start = max(0, visible_prompt.start() - 50)
        excerpt_end = min(len(visible_article), visible_prompt.end() + 90)
        excerpt = re.sub(r"\s+", " ", visible_article[excerpt_start:excerpt_end]).strip()
        add_issue(issues, "BLOCK", "提示性话语可见", f"作者或编辑提示必须移入中英文 HTML 注释：{excerpt}")

    for comment in re.findall(r"<!--(.*?)-->", article, flags=re.DOTALL):
        if not PROMPT_COMMENT_RE.search(comment):
            continue
        if not re.search(r"[\u4e00-\u9fff]", comment) or not re.search(r"[A-Za-z]", comment):
            excerpt = re.sub(r"\s+", " ", comment).strip()[:140]
            add_issue(issues, "BLOCK", "提示注释语言", f"提示注释必须同时包含中文和英文：{excerpt}")

    defined_sources = set(SOURCE_HEADING_RE.findall(sources))
    used_sources = set()
    for anchor in SOURCE_ANCHOR_RE.findall(article):
        used_sources.update(item.strip() for item in anchor.split(",") if item.strip())
    undefined = sorted(item for item in used_sources if item not in defined_sources)
    if undefined:
        add_issue(issues, "BLOCK", "来源编号", f"正文使用但台账未定义：{', '.join(undefined)}")
    if not used_sources:
        add_issue(issues, "BLOCK", "来源锚点", "正文没有任何 <!-- source:S1 --> 证据锚点")

    for paragraph in meaningful_paragraphs(article):
        if NUMBER_RE.search(paragraph) and not SOURCE_ANCHOR_RE.search(paragraph) and not IMAGE_SOURCE_RE.search(paragraph):
            excerpt = re.sub(r"\s+", " ", paragraph)[:120]
            add_issue(issues, "BLOCK" if args.strict else "WARN", "数字事实来源", f"数字段落缺少来源锚点：{excerpt}")

    for caption_number, caption_text in CAPTION_RE.findall(article):
        visible_caption = f"{caption_number} {caption_text}"
        punctuation = CAPTION_PUNCTUATION_RE.findall(visible_caption)
        if punctuation:
            add_issue(
                issues, "BLOCK" if args.strict else "WARN", "图表图注标点",
                f"图表图注不得含任何标点：{visible_caption}",
            )

    for line_number, line in enumerate(article.splitlines(), start=1):
        stripped_line = line.strip()
        if not (stripped_line.startswith("|") and TABLE_BREAK_RE.search(stripped_line)):
            continue
        for cell in re.split(r"(?<!\\)\|", stripped_line):
            if not TABLE_BREAK_RE.search(cell):
                continue
            for segment in TABLE_BREAK_RE.split(cell):
                plain = re.sub(r"<!--.*?-->", "", segment)
                plain = re.sub(r"[*_`~]", "", plain).strip()
                if not plain:
                    continue
                core = TRAILING_PUNCTUATION_RE.sub("", plain).strip()
                ends_with_punctuation = bool(TRAILING_PUNCTUATION_RE.search(plain))
                compact_length = len(re.sub(r"\s+", "", core))
                looks_like_short_label = (
                    compact_length <= 12
                    and not re.search(r"\s", core)
                    and not re.search(r"[。！？.!?]", core)
                )
                looks_like_long_sentence = compact_length >= 28
                if looks_like_short_label and ends_with_punctuation:
                    add_issue(
                        issues, "WARN", "表格换行标点",
                        f"第{line_number}行的短项可能不需要末尾标点，请按语义判断：{plain}",
                    )
                elif looks_like_long_sentence and not ends_with_punctuation:
                    add_issue(
                        issues, "WARN", "表格换行标点",
                        f"第{line_number}行的长项可能是完整句，请确认是否需要句末标点：{plain[:80]}",
                    )

    if re.search(r"状态：\s*(?:NEEDS_REVIEW|CONFLICT)", sources):
        add_issue(issues, "BLOCK", "来源状态", "sources.md 仍包含 NEEDS_REVIEW 或 CONFLICT")
    if re.search(r"权利状态：\s*NEEDS_REVIEW", sources):
        add_issue(issues, "BLOCK", "图片权利", "图片台账仍有待确认的权利状态")

    image_matches = list(IMAGE_RE.finditer(article))
    for index, match in enumerate(image_matches):
        alt, target = match.groups()
        if not alt.strip() or "{{" in alt:
            add_issue(issues, "WARN", "图片替代文本", f"图片缺少有效 alt：{target}")
        next_start = image_matches[index + 1].start() if index + 1 < len(image_matches) else len(article)
        image_block = article[match.end():next_start]
        if not IMAGE_SOURCE_RE.search(image_block):
            add_issue(issues, "BLOCK", "图片来源批注", f"图片后缺少隐藏 image-source 批注：{target}")
        caption_block = re.split(r"\n#{1,6}\s", image_block, maxsplit=1)[0]
        visible_image_block = re.sub(r"<!--.*?-->", "", caption_block, flags=re.DOTALL)
        visible_captions = CAPTION_RE.findall(caption_block)
        is_qr_image = (
            "qr" in target.lower()
            or "二维码" in alt
            or "联合传播" in target
            or "联合传播" in alt
        )
        caption_decision = CAPTION_DECISION_RE.search(caption_block)
        if not is_qr_image:
            if not caption_decision:
                add_issue(issues, "BLOCK", "图注交互确认", f"图表缺少用户图注决定：{target}")
            elif caption_decision.group(1) == "NEEDS_REVIEW":
                add_issue(issues, "BLOCK", "图注交互确认", f"图表是否添加图注仍待用户确认：{target}")
            elif caption_decision.group(1) == "user-confirmed-add" and not visible_captions:
                add_issue(issues, "BLOCK", "图注交互确认", f"用户选择添加图注，但正文没有可见图注：{target}")
            elif caption_decision.group(1) == "user-confirmed-omit" and visible_captions:
                add_issue(issues, "BLOCK", "图注交互确认", f"用户选择不添加图注，但正文仍有可见图注：{target}")
        if re.search(r"(?:来源\s*[：:]|Source\s*[：:])", visible_image_block, re.IGNORECASE):
            add_issue(issues, "BLOCK", "图片来源可见", f"图片来源必须移入隐藏批注：{target}")
        if target.startswith(("http://", "https://", "data:")):
            add_issue(issues, "WARN", "远程图片", f"建议下载到本地 assets 并记录来源：{target}")
            continue
        path = (article_path.parent / target).resolve()
        if not path.exists():
            add_issue(issues, "BLOCK", "图片文件", f"Markdown 引用的图片不存在：{target}")

    article_lines = article.splitlines()
    table_separator_re = re.compile(r"^\s*\|?(?:\s*:?-{3,}:?\s*\|)+\s*$")
    for line_number, line in enumerate(article_lines, start=1):
        if not table_separator_re.match(line):
            continue
        context_start = max(0, line_number - 8)
        preceding = "\n".join(article_lines[context_start:line_number - 1])
        table_decision = TABLE_CAPTION_DECISION_RE.search(preceding)
        table_captions = [item for item in CAPTION_RE.findall(preceding) if item[0].lower().startswith(("表", "table"))]
        if not table_decision:
            add_issue(issues, "BLOCK", "表注交互确认", f"第{line_number}行表格缺少用户图注决定")
        elif table_decision.group(1) == "NEEDS_REVIEW":
            add_issue(issues, "BLOCK", "表注交互确认", f"第{line_number}行表格是否添加图注仍待用户确认")
        elif table_decision.group(1) == "user-confirmed-add" and not table_captions:
            add_issue(issues, "BLOCK", "表注交互确认", f"用户选择添加表注，但第{line_number}行表格前没有可见表注")
        elif table_decision.group(1) == "user-confirmed-omit" and table_captions:
            add_issue(issues, "BLOCK", "表注交互确认", f"用户选择不添加表注，但第{line_number}行表格前仍有可见表注")

    for phrase in OVERCLAIMS:
        if phrase in article:
            add_issue(issues, "WARN", "可能夸大", f"请核对表述：{phrase}")
    if "AI生成" in article and "AI_GENERATED" not in sources:
        add_issue(issues, "BLOCK", "AI图片标记", "正文提到AI生成图片，但来源台账未标记 AI_GENERATED")

    report = render_report(article_path, sources_path, issues, args.override)
    args.report.resolve().write_text(report, encoding="utf-8")
    blockers = any(issue["level"] == "BLOCK" for issue in issues)
    print(f"BLOCK={sum(issue['level']=='BLOCK' for issue in issues)} WARN={sum(issue['level']=='WARN' for issue in issues)}")
    return 0 if not blockers or args.override else 2


if __name__ == "__main__":
    raise SystemExit(main())
