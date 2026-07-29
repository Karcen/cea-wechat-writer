#!/usr/bin/env python3
"""Retrieve a few same-category historical examples for structure and tone."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def normalize(value: str) -> str:
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]", "", value.lower())


def grams(value: str, width: int = 2) -> set[str]:
    value = normalize(value)
    if len(value) < width:
        return {value} if value else set()
    return {value[index:index + width] for index in range(len(value) - width + 1)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--category", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--kind", choices=("html", "word", "any"), default="any")
    parser.add_argument("--include-degraded", action="store_true")
    parser.add_argument("--cross-category", action="store_true")
    args = parser.parse_args()

    payload = json.loads(args.corpus.read_text(encoding="utf-8"))
    base = args.corpus.parent
    query_grams = grams(args.query)
    results = []
    for entry in payload["entries"]:
        if entry.get("status") != "ok" or not entry.get("file"):
            continue
        if entry.get("text_quality") == "degraded_mojibake" and not args.include_degraded:
            continue
        if args.kind != "any" and entry.get("kind") != args.kind:
            continue
        if entry.get("category") != args.category and not args.cross_category:
            continue
        path = base / entry["file"]
        text = path.read_text(encoding="utf-8")
        title_grams = grams(entry.get("title", ""))
        body_grams = grams(text[:12000])
        title_overlap = len(query_grams & title_grams) / max(1, len(query_grams | title_grams))
        body_overlap = len(query_grams & body_grams) / max(1, len(query_grams))
        category_bonus = 0.55 if entry.get("category") == args.category else 0.0
        score = category_bonus + title_overlap * 0.30 + body_overlap * 0.15
        results.append((score, entry, path))

    for score, entry, path in sorted(results, key=lambda item: item[0], reverse=True)[: max(1, args.limit)]:
        print(json.dumps({
            "score": round(score, 4), "category": entry.get("category"),
            "title": entry.get("title"), "kind": entry.get("kind"),
            "example_path": str(path.resolve()), "source_path": entry.get("source_path"),
            "warning": "仅学习结构与文风；不得复用其中的事实。",
        }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
