#!/usr/bin/env python3
import argparse
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import markdown
from bs4 import BeautifulSoup

try:
    import cssutils
except ImportError:  # pragma: no cover - fallback only
    cssutils = None


STYLE_PRESETS = {
    "A": {
        "section": "margin:0 auto;padding:0;color:#3f3f3f;font-size:17px;line-height:2;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Helvetica Neue',Arial,sans-serif;text-align:left;letter-spacing:0;",
        "p": "margin:0 0 1.25em;padding:0;color:#3f3f3f;font-size:17px;line-height:2;text-align:left;letter-spacing:0;",
        "h2": "margin:2.2em 0 1em;padding:0;color:#222;font-size:21px;line-height:1.55;font-weight:700;text-align:left;",
        "h3": "margin:1.8em 0 .8em;padding:0;color:#333;font-size:18px;line-height:1.65;font-weight:700;text-align:left;",
        "blockquote": "margin:1.7em 0;padding:1.1em 1.25em;background:#fff7f7;border-left:4px solid #e11919;border-radius:6px;color:#333;font-size:17px;line-height:1.9;",
        "strong": "color:#d71920;font-weight:700;",
        "code": "font-family:Menlo,Monaco,Consolas,'Courier New',monospace;background:#f5f5f5;border-radius:3px;padding:0 4px;color:#444;font-size:.92em;",
        "figure": "margin:1.8em 0 1.8em;padding:0;text-align:center;",
        "img": "display:block;width:100%;height:auto;margin:0 auto;border-radius:2px;",
        "ul": "margin:0 0 1.25em 1.25em;padding:0;color:#3f3f3f;font-size:17px;line-height:1.95;",
        "ol": "margin:0 0 1.25em 1.25em;padding:0;color:#3f3f3f;font-size:17px;line-height:1.95;",
        "li": "margin:0 0 .65em;padding:0;color:#3f3f3f;font-size:17px;line-height:1.95;",
        "table": "width:100%;margin:0;border-collapse:collapse;color:#3f3f3f;font-size:15px;line-height:1.75;",
        "th": "padding:.8em .6em;border-bottom:1px solid #ddd;color:#222;font-weight:700;text-align:left;",
        "td": "padding:.8em .6em;border-bottom:1px solid #eee;color:#444;text-align:left;",
        "accent": "#d71920",
    },
    "R": {
        "section": "max-width:100%;margin:0 auto;padding:24px 20px 48px;color:#333;background:#fff;font-size:16px;line-height:1.78;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;text-align:justify;letter-spacing:.5px;",
        "p": "margin:20px 0!important;padding:0;color:#333;font-size:16px;line-height:1.78;text-align:justify;letter-spacing:.5px;",
        "h2": "margin:34px 0 18px;padding:0;color:#333;font-size:18px;line-height:1.65;font-weight:700;text-align:left;",
        "h3": "margin:28px 0 12px;padding:0;color:#333;font-size:17px;line-height:1.65;font-weight:700;text-align:left;",
        "blockquote": "margin:24px 0 30px;padding:30px 20px 28px 16px;background:#fff6f6;border-left:4px solid #d71920;border-radius:3px;color:#444;font-size:15.5px;line-height:2.05;text-align:justify;",
        "strong": "color:#333;font-weight:700;",
        "mark": "color:#d71920;font-weight:700;",
        "code": "font-family:Menlo,Monaco,Consolas,'Courier New',monospace;background:#f7f7f7;border-radius:3px;padding:0 4px;color:#444;font-size:.92em;",
        "figure": "margin:24px 0;padding:0;text-align:center;",
        "img": "display:block;width:100%;height:auto;margin:0 auto;border-radius:4px;",
        "ul": "margin:16px 0 20px 28px;padding:0;color:#333;font-size:16px;line-height:1.85;",
        "ol": "margin:16px 0 20px 28px;padding:0;color:#333;font-size:16px;line-height:1.85;",
        "li": "margin:8px 0;padding:0;color:#333;font-size:16px;line-height:1.85;",
        "table": "width:100%;margin:0;border-collapse:collapse;color:#333;font-size:15px;line-height:1.75;",
        "th": "padding:12px 10px;border-bottom:1px solid #f1c9c9;background:#fff6f6;color:#333;font-weight:700;text-align:left;",
        "td": "padding:12px 10px;border-bottom:1px solid #f1e1e1;color:#444;text-align:left;",
        "accent": "#d71920",
    },
    "E": {
        "section": "margin:0 auto;padding:0;color:#3d3d3d;font-size:17px;line-height:1.95;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Helvetica Neue',Arial,sans-serif;text-align:left;letter-spacing:0;",
        "p": "margin:0 0 1.18em;padding:0;color:#3d3d3d;font-size:17px;line-height:1.95;text-align:left;letter-spacing:0;",
        "h2": "margin:2.2em 0 1.05em;padding:.18em 0 .18em .75em;border-left:5px solid #1f5f99;color:#1f2a37;font-size:21px;line-height:1.55;font-weight:700;text-align:left;",
        "h3": "margin:1.65em 0 .8em;padding:0;color:#1f2a37;font-size:18px;line-height:1.65;font-weight:700;text-align:left;",
        "blockquote": "margin:1.6em 0;padding:1.05em 1.2em;background:#f5f8fb;border-left:4px solid #1f5f99;border-radius:6px;color:#333;font-size:17px;line-height:1.9;",
        "strong": "color:#1f5f99;font-weight:700;",
        "code": "font-family:Menlo,Monaco,Consolas,'Courier New',monospace;background:#f4f6f8;border-radius:3px;padding:0 4px;color:#334155;font-size:.92em;",
        "figure": "margin:1.7em 0 1.7em;padding:0;text-align:center;",
        "img": "display:block;width:100%;height:auto;margin:0 auto;border-radius:2px;",
        "ul": "margin:0 0 1.2em 1.25em;padding:0;color:#3d3d3d;font-size:17px;line-height:1.9;",
        "ol": "margin:0 0 1.2em 1.25em;padding:0;color:#3d3d3d;font-size:17px;line-height:1.9;",
        "li": "margin:0 0 .65em;padding:0;color:#3d3d3d;font-size:17px;line-height:1.9;",
        "table": "width:100%;margin:0;border-collapse:collapse;color:#3d3d3d;font-size:15px;line-height:1.75;",
        "th": "padding:.8em .6em;border-bottom:1px solid #cbd5e1;color:#1f2a37;font-weight:700;text-align:left;",
        "td": "padding:.8em .6em;border-bottom:1px solid #e5e7eb;color:#444;text-align:left;",
        "accent": "#1f5f99",
    },
    "F": {
        "section": "margin:0 auto;padding:0;color:#444;font-size:17px;line-height:2.05;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Helvetica Neue',Arial,sans-serif;text-align:left;letter-spacing:0;",
        "p": "margin:0 0 1.55em;padding:0;color:#444;font-size:17px;line-height:2.05;text-align:left;letter-spacing:0;",
        "h2": "margin:2.4em 0 1.15em;padding:0;color:#333;font-size:21px;line-height:1.6;font-weight:700;text-align:left;",
        "h3": "margin:1.9em 0 .9em;padding:0;color:#3a3a3a;font-size:18px;line-height:1.7;font-weight:700;text-align:left;",
        "blockquote": "margin:1.8em 0;padding:1.15em 1.35em;background:#f7f9fb;border-left:4px solid #1764a8;border-radius:6px;color:#3f3f3f;font-size:17px;line-height:1.95;",
        "strong": "color:#333;font-weight:700;",
        "code": "font-family:Menlo,Monaco,Consolas,'Courier New',monospace;background:#f6f6f6;border-radius:3px;padding:0 4px;color:#444;font-size:.92em;",
        "figure": "margin:2em 0 2em;padding:0;text-align:center;",
        "img": "display:block;width:100%;height:auto;margin:0 auto;border-radius:2px;",
        "ul": "margin:0 0 1.45em 1.25em;padding:0;color:#444;font-size:17px;line-height:2;",
        "ol": "margin:0 0 1.45em 1.25em;padding:0;color:#444;font-size:17px;line-height:2;",
        "li": "margin:0 0 .7em;padding:0;color:#444;font-size:17px;line-height:2;",
        "table": "width:100%;margin:0;border-collapse:collapse;color:#444;font-size:15px;line-height:1.8;",
        "th": "padding:.85em .6em;border-bottom:1px solid #ddd;color:#333;font-weight:700;text-align:left;",
        "td": "padding:.85em .6em;border-bottom:1px solid #eee;color:#444;text-align:left;",
        "accent": "#1764a8",
    },
    "J": {
        "section": "margin:0 auto;padding:0 16px;color:rgba(0,0,0,.9);font-size:16px;line-height:1.8;font-family:mp-quote,'PingFang SC',system-ui,-apple-system,BlinkMacSystemFont,'Helvetica Neue','Hiragino Sans GB','Microsoft YaHei UI','Microsoft YaHei',Arial,sans-serif;text-align:justify;letter-spacing:.02em;",
        "p": "margin:0 0 1.55em;padding:0;color:rgba(0,0,0,.9);font-size:16px;line-height:1.8;text-align:justify;letter-spacing:.02em;",
        "h2": "margin:2.2em 0 1.7em;padding:0;color:#d6a23a;font-size:17px;line-height:1.6;font-weight:700;text-align:left;letter-spacing:.02em;",
        "h3": "margin:1.8em 0 1em;padding:0;color:#333;font-size:16px;line-height:1.75;font-weight:700;text-align:left;letter-spacing:.02em;",
        "blockquote": "margin:1.8em 0;padding:1em 1.1em;background:#f8f8f8;border-left:3px solid #d6a23a;border-radius:4px;color:#444;font-size:16px;line-height:1.85;",
        "strong": "color:#222;font-weight:700;",
        "code": "font-family:Menlo,Monaco,Consolas,'Courier New',monospace;background:#f6f6f6;border-radius:3px;padding:0 4px;color:#444;font-size:.92em;",
        "figure": "margin:1.7em 0 1.35em;padding:0;text-align:center;",
        "img": "display:block;width:100%;height:auto;margin:0 auto;border:0;border-radius:0;",
        "ul": "margin:0 0 1.45em 1.25em;padding:0;color:rgba(0,0,0,.9);font-size:16px;line-height:1.85;",
        "ol": "margin:0 0 1.45em 1.25em;padding:0;color:rgba(0,0,0,.9);font-size:16px;line-height:1.85;",
        "li": "margin:0 0 .75em;padding:0;color:rgba(0,0,0,.9);font-size:16px;line-height:1.85;",
        "table": "width:100%;margin:0;border-collapse:collapse;color:rgba(0,0,0,.9);font-size:14px;line-height:1.75;",
        "th": "padding:.75em .55em;border-bottom:1px solid #ddd;color:#333;font-weight:700;text-align:left;",
        "td": "padding:.75em .55em;border-bottom:1px solid #eee;color:#444;text-align:left;",
        "accent": "#d6a23a",
    },
    "L": {
        "section": "margin:0 auto;padding:0;color:#3e3e3e;font-size:17px;line-height:2;font-family:'PingFang SC',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;text-align:left;letter-spacing:.544px;",
        "p": "max-width:232px;margin:0 auto 42px;padding:0;color:#3e3e3e;font-size:17px;line-height:2;text-align:left;text-indent:0;letter-spacing:.544px;",
        "h2": "margin:2.4em 0 1.7em;padding:0;text-align:center;color:#444;font-size:14px;line-height:1.8;font-weight:700;letter-spacing:1px;",
        "h3": "margin:2em 22px 1.1em;padding:0;color:#1f5f99;font-size:17px;line-height:1.8;font-weight:700;text-align:left;letter-spacing:1px;",
        "blockquote": "max-width:300px;margin:2em auto;padding:1.15em 1.35em;background:#f7f8fa;border-left:4px solid #1f5f99;border-radius:6px;color:#3f3f3f;font-size:17px;line-height:1.9;text-align:left;text-indent:0;",
        "strong": "color:#1f5f99;font-weight:700;",
        "code": "font-family:Menlo,Monaco,Consolas,'Courier New',monospace;background:#f6f6f6;border-radius:3px;padding:0 4px;color:#444;font-size:.92em;",
        "figure": "margin:2em auto;padding:0;text-align:center;",
        "img": "display:block;width:90%;height:auto;margin:0 auto;border-radius:0;box-shadow:none;",
        "ul": "max-width:232px;margin:0 auto 1.7em;padding:0 0 0 1.25em;color:#444;font-size:17px;line-height:1.95;letter-spacing:.544px;",
        "ol": "max-width:232px;margin:0 auto 1.7em;padding:0 0 0 1.25em;color:#444;font-size:17px;line-height:1.95;letter-spacing:.544px;",
        "li": "margin:0 0 .7em;padding:0;color:#444;font-size:17px;line-height:1.95;",
        "table": "width:100%;margin:0;border-collapse:collapse;color:#444;font-size:15px;line-height:1.8;",
        "th": "padding:.85em .6em;border-bottom:1px solid #d6dce5;color:#1f5f99;font-weight:700;text-align:left;",
        "td": "padding:.85em .6em;border-bottom:1px solid #eee;color:#444;text-align:left;",
        "accent": "#1f5f99",
    },
    "T": {
        "section": "margin:0 auto;padding:8px;color:#333;font-size:16px;line-height:2;font-family:Optima-Regular,PingFangSC-light,'PingFang SC',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;text-align:justify;letter-spacing:1.5px;",
        "p": "margin:30px 8px;padding:0;color:#333;font-size:16px;line-height:32px;text-align:justify;letter-spacing:2px;word-spacing:2px;",
        "h2": "margin:42px 8px 28px;padding:0;text-align:center;color:#333;font-size:17px;line-height:2;font-weight:400;letter-spacing:2px;word-spacing:2px;",
        "h3": "margin:34px 8px 18px;padding:0;color:#2f6f37;font-size:16px;line-height:30px;font-weight:700;text-align:left;letter-spacing:1.5px;",
        "blockquote": "margin:28px 8px;padding:14px 16px;background:#f6fff2;border-left:4px solid #d3f8b6;border-radius:6px;color:#333;font-size:16px;line-height:30px;text-align:justify;letter-spacing:1.5px;",
        "strong": "color:#2f6f37;font-weight:700;",
        "code": "font-family:Menlo,Monaco,Consolas,'Courier New',monospace;background:#f4f8f2;border-radius:3px;padding:0 4px;color:#2f6f37;font-size:.92em;",
        "figure": "margin:20px auto 30px;padding:0;text-align:center;",
        "img": "display:block;width:334px!important;max-width:calc(100% - 16px);height:auto;margin:0 auto;border-radius:6px;object-fit:contain;box-shadow:#999 2px 4px 7px;",
        "ul": "margin:24px 8px 30px 1.8em;padding:0;color:#333;font-size:16px;line-height:30px;letter-spacing:1.5px;",
        "ol": "margin:24px 8px 30px 1.8em;padding:0;color:#333;font-size:16px;line-height:30px;letter-spacing:1.5px;",
        "li": "margin:10px 0;padding:0;color:#333;font-size:16px;line-height:30px;",
        "table": "width:100%;margin:0;border-collapse:collapse;color:#333;font-size:15px;line-height:1.8;letter-spacing:1px;",
        "th": "padding:.85em .6em;border-bottom:1px solid #cfe8c1;background:#f6fff2;color:#2f6f37;font-weight:700;text-align:left;",
        "td": "padding:.85em .6em;border-bottom:1px solid #eee;color:#444;text-align:left;",
        "accent": "#2f6f37",
    },
    "G": {
        "section": "margin:0 auto;padding:0;color:#4a4a4a;font-size:17px;line-height:1.82;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Helvetica Neue',Arial,sans-serif;text-align:justify;letter-spacing:1px;",
        "p": "margin:0 5px 1.55em;padding:0;color:#4a4a4a;font-size:17px;line-height:1.82;text-align:justify;letter-spacing:1px;",
        "h2": "margin:2em 0 1em;padding:0;color:#222;font-size:20px;line-height:1.55;font-weight:700;text-align:center;",
        "h3": "margin:1.6em 0 .75em;padding:0 5px;color:#333;font-size:17px;line-height:1.65;font-weight:700;text-align:left;",
        "blockquote": "margin:1.6em 5px;padding:0 0 0 14px;border-left:3px solid #111;color:#555;font-size:17px;line-height:1.82;",
        "strong": "color:#222;font-weight:700;",
        "code": "font-family:Menlo,Monaco,Consolas,'Courier New',monospace;background:#f5f5f5;border-radius:3px;padding:0 4px;color:#444;font-size:.92em;",
        "figure": "margin:32px 0 38px;padding:0;text-align:center;",
        "img": "display:block;width:100%;height:auto;margin:0 auto;border-radius:0;",
        "ul": "margin:0 5px 1.35em 1.45em;padding:0;color:#3e3e3e;font-size:16px;line-height:1.75;",
        "ol": "margin:0 5px 1.35em 1.45em;padding:0;color:#3e3e3e;font-size:16px;line-height:1.75;",
        "li": "margin:0 0 .65em;padding:0;color:#3e3e3e;font-size:16px;line-height:1.75;",
        "table": "width:100%;margin:0;border-collapse:collapse;color:#3e3e3e;font-size:15px;line-height:1.7;",
        "th": "padding:.75em .5em;border-bottom:1px solid #ddd;color:#222;font-weight:700;text-align:left;",
        "td": "padding:.75em .5em;border-bottom:1px solid #eee;color:#444;text-align:left;",
        "accent": "#111",
    },
}

EVIDENCE_TOKEN_THEMES = {
    "WECHAT-CLASSIC-READABLE": {
        "evidence_level": "A",
        "source_refs": ["doocs/md", "mdnice/markdown-nice", "scfido/mp-styles"],
        "accent": "#d71920",
        "accent_bg": "#fff7f7",
        "accent_border": "#f1c9c9",
        "text": "#3f3f3f",
        "text_dark": "#222222",
        "text_muted": "#777777",
        "bg": "#ffffff",
        "card_bg": "#fafafa",
        "border": "#dddddd",
        "border_light": "#eeeeee",
        "font_body": "-apple-system,BlinkMacSystemFont,'PingFang SC','Helvetica Neue',Arial,sans-serif",
        "font_heading": "-apple-system,BlinkMacSystemFont,'PingFang SC','Helvetica Neue',Arial,sans-serif",
        "font_mono": "Menlo,Monaco,Consolas,'Courier New',monospace",
        "body_font_size": "17px",
        "body_line_height": "1.9",
        "paragraph_margin": "0 0 1.35em",
        "h2_font_size": "21px",
        "h2_line_height": "1.5",
        "h2_margin": "2.15em 0 1em",
        "h3_font_size": "18px",
        "h3_line_height": "1.6",
        "blockquote_margin": "1.6em 0",
        "blockquote_padding": "1.05em 1.2em",
        "blockquote_line_height": "1.9",
    },
    "GITHUB-PRIMER-DOC": {
        "evidence_level": "A",
        "source_refs": ["primer/css"],
        "accent": "#0969da",
        "accent_bg": "#f6f8fa",
        "accent_border": "#d0d7de",
        "text": "#24292f",
        "text_dark": "#1f2328",
        "text_muted": "#57606a",
        "bg": "#ffffff",
        "card_bg": "#f6f8fa",
        "border": "#d0d7de",
        "border_light": "#eaeef2",
        "font_body": "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans','Helvetica Neue',Arial,'PingFang SC',sans-serif",
        "font_heading": "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans','Helvetica Neue',Arial,'PingFang SC',sans-serif",
        "font_mono": "ui-monospace,SFMono-Regular,SFMono-Regular,Consolas,'Liberation Mono',Menlo,monospace",
        "body_font_size": "16px",
        "body_line_height": "1.78",
        "paragraph_margin": "0 0 1.35em",
        "h2_font_size": "22px",
        "h2_line_height": "1.45",
        "h2_margin": "2.05em 0 .95em",
        "h3_font_size": "18px",
        "h3_line_height": "1.55",
        "blockquote_margin": "1.55em 0",
        "blockquote_padding": "1em 1.1em",
        "blockquote_line_height": "1.85",
        "table_cell_padding": ".85em .65em",
    },
    "ECONOMIST-BRIEFING-LITE": {
        "evidence_level": "B",
        "source_refs": ["brucecbi/wechat-design-html", "brucecbi docs/economist-design.md"],
        "accent": "#e3120b",
        "accent_bg": "rgba(227,18,11,.06)",
        "accent_border": "rgba(227,18,11,.22)",
        "text": "#2a2a2a",
        "text_dark": "#111111",
        "text_muted": "#6b6b6b",
        "bg": "#f7f5f2",
        "card_bg": "#ffffff",
        "border": "#d9d4cd",
        "border_light": "#e5e1db",
        "font_body": "-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_heading": "Georgia,'Iowan Old Style','Times New Roman','Songti SC','STSong','SimSun',serif",
        "font_mono": "'SF Mono',Menlo,Consolas,'Courier New',monospace",
        "body_font_size": "16px",
        "body_line_height": "1.9",
        "paragraph_margin": "0 0 1.55em",
        "h2_font_size": "22px",
        "h2_line_height": "1.42",
        "h2_margin": "2.05em 0 1em",
        "h2_font_weight": "700",
        "h3_font_size": "17px",
        "h3_line_height": "1.55",
        "blockquote_margin": "1.7em 0",
        "blockquote_padding": "1.1em 1.15em",
        "blockquote_line_height": "1.92",
        "blockquote_font_family": "-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "image_radius": "0",
        "section_padding": "26px 20px 44px",
    },
    "CLAUDE-RESEARCH-LITE": {
        "evidence_level": "B",
        "source_refs": ["VoltAgent/awesome-design-md design-md/claude", "brucecbi/wechat-design-html themes/claude.json"],
        "accent": "#cc785c",
        "accent_bg": "rgba(204,120,92,.08)",
        "accent_border": "rgba(204,120,92,.22)",
        "text": "#3d3d3a",
        "text_dark": "#141413",
        "text_muted": "#6c6a64",
        "bg": "#faf9f5",
        "card_bg": "#f5f0e8",
        "border": "#e6dfd8",
        "border_light": "#ebe6df",
        "font_body": "-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_heading": "Georgia,'Songti SC','STSong','SimSun',serif",
        "font_mono": "Menlo,Consolas,'Courier New',monospace",
        "body_font_size": "16px",
        "body_line_height": "1.88",
        "paragraph_margin": "0 0 1.48em",
        "h2_font_size": "22px",
        "h2_line_height": "1.45",
        "h2_margin": "2.1em 0 1em",
        "h2_font_weight": "600",
        "h3_font_size": "17px",
        "h3_line_height": "1.6",
        "blockquote_margin": "1.65em 0",
        "blockquote_padding": "1em 1.15em",
        "blockquote_line_height": "1.9",
        "section_padding": "26px 20px 44px",
    },
    "STRIPE-DOC-LITE": {
        "evidence_level": "B",
        "source_refs": ["VoltAgent/awesome-design-md design-md/stripe", "brucecbi/wechat-design-html themes/stripe.json"],
        "accent": "#533afd",
        "accent_bg": "rgba(83,58,253,.06)",
        "accent_border": "rgba(83,58,253,.22)",
        "text": "#273951",
        "text_dark": "#0d253d",
        "text_muted": "#64748d",
        "bg": "#f6f9fc",
        "card_bg": "#ffffff",
        "border": "#e3e8ee",
        "border_light": "#eef2f7",
        "font_body": "-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_heading": "-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_mono": "Menlo,Consolas,'Courier New',monospace",
        "body_font_size": "16px",
        "body_line_height": "1.78",
        "paragraph_margin": "0 0 1.35em",
        "h2_font_size": "21px",
        "h2_line_height": "1.45",
        "h2_margin": "2em 0 .95em",
        "h2_font_weight": "700",
        "h3_font_size": "17px",
        "h3_line_height": "1.55",
        "section_padding": "26px 20px 44px",
    },
    "VERCEL-MINIMAL-DOC": {
        "evidence_level": "B",
        "source_refs": ["VoltAgent/awesome-design-md design-md/vercel", "brucecbi/wechat-design-html themes/vercel.json"],
        "accent": "#000000",
        "accent_bg": "rgba(0,0,0,.045)",
        "accent_border": "rgba(0,0,0,.18)",
        "text": "#3f3f46",
        "text_dark": "#000000",
        "text_muted": "#71717a",
        "bg": "#fafafa",
        "card_bg": "#ffffff",
        "border": "#e4e4e7",
        "border_light": "#f4f4f5",
        "font_body": "-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_heading": "-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_mono": "Menlo,Consolas,'Courier New',monospace",
        "body_font_size": "16px",
        "body_line_height": "1.72",
        "paragraph_margin": "0 0 1.28em",
        "h2_font_size": "21px",
        "h2_line_height": "1.42",
        "h2_margin": "2em 0 .9em",
        "h2_font_weight": "700",
        "h3_font_size": "17px",
        "h3_line_height": "1.52",
        "blockquote_margin": "1.5em 0",
        "blockquote_padding": "1em 1.1em",
        "blockquote_line_height": "1.82",
        "image_radius": "0",
        "section_padding": "26px 20px 44px",
    },
    "STRIPE-INFRA": {
        "source_refs": ["duyi-wechat-css-layer templates/styles.md", "duyi-wechat-css-layer templates/theme-index.json"],
        "accent": "#533afd",
        "accent_bg": "rgba(83,58,253,.08)",
        "accent_border": "rgba(83,58,253,.2)",
        "text": "#273951",
        "text_dark": "#0d253d",
        "text_muted": "#64748d",
        "bg": "#f6f9fc",
        "card_bg": "#ffffff",
        "border": "#e3e8ee",
        "border_light": "#eef2f7",
        "font_body": "-apple-system,BlinkMacSystemFont,'Inter','Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_heading": "-apple-system,BlinkMacSystemFont,'Inter','Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_mono": "'SF Mono',Menlo,Consolas,'Courier New',monospace",
        "body_font_size": "16px",
        "body_line_height": "1.78",
        "paragraph_margin": "0 0 1.35em",
        "h2_font_size": "21px",
        "h2_line_height": "1.42",
        "h2_margin": "2.05em 0 .85em",
        "h2_font_weight": "750",
        "h3_font_size": "17px",
        "h3_line_height": "1.5",
        "blockquote_margin": "1.6em 0",
        "blockquote_padding": "1em 1.1em",
        "blockquote_radius": "12px",
        "image_radius": "12px",
        "image_shadow": "0 12px 32px rgba(13,37,61,.08)",
        "section_padding": "28px 20px 46px",
    },
    "VERCEL-MINIMAL": {
        "source_refs": ["duyi-wechat-css-layer templates/styles.md", "duyi-wechat-css-layer templates/theme-index.json"],
        "accent": "#000000",
        "accent_bg": "rgba(0,0,0,.06)",
        "accent_border": "rgba(0,0,0,.18)",
        "text": "#3f3f46",
        "text_dark": "#000000",
        "text_muted": "#71717a",
        "bg": "#fafafa",
        "card_bg": "#ffffff",
        "border": "#e4e4e7",
        "border_light": "#f4f4f5",
        "font_body": "-apple-system,BlinkMacSystemFont,'Geist','Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_heading": "-apple-system,BlinkMacSystemFont,'Geist','Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_mono": "'SF Mono',Menlo,Consolas,'Courier New',monospace",
        "body_font_size": "16px",
        "body_line_height": "1.72",
        "paragraph_margin": "0 0 1.25em",
        "h2_font_size": "21px",
        "h2_line_height": "1.42",
        "h2_margin": "2.1em 0 .8em",
        "h2_font_weight": "740",
        "h3_font_size": "17px",
        "h3_line_height": "1.5",
        "blockquote_margin": "1.55em 0",
        "blockquote_padding": "1em 1.1em",
        "blockquote_radius": "8px",
        "image_radius": "8px",
        "section_padding": "28px 20px 46px",
    },
    "CLAUDE-RESEARCH": {
        "source_refs": ["duyi-wechat-css-layer templates/styles.md", "duyi-wechat-css-layer templates/theme-index.json"],
        "accent": "#cc785c",
        "accent_bg": "#f5f0e8",
        "accent_border": "#e6dfd8",
        "text": "#3d3d3a",
        "text_dark": "#141413",
        "text_muted": "#6c6a64",
        "bg": "#faf9f5",
        "card_bg": "#f5f0e8",
        "border": "#e6dfd8",
        "border_light": "#ebe6df",
        "font_body": "-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_heading": "Georgia,'Songti SC','STSong','SimSun',serif",
        "font_mono": "Menlo,Consolas,'Courier New',monospace",
        "body_font_size": "16px",
        "body_line_height": "1.88",
        "paragraph_margin": "0 0 1.48em",
        "h2_font_size": "22px",
        "h2_line_height": "1.45",
        "h2_margin": "2.15em 0 .9em",
        "h2_font_weight": "700",
        "h3_font_size": "17px",
        "h3_line_height": "1.58",
        "blockquote_margin": "1.65em 0",
        "blockquote_padding": "1.1em 1.15em",
        "blockquote_radius": "12px",
        "image_radius": "12px",
        "section_padding": "30px 20px 48px",
    },
    "ECONOMIST-BRIEFING": {
        "source_refs": ["duyi-wechat-css-layer templates/styles.md", "duyi-wechat-css-layer templates/theme-index.json"],
        "accent": "#e3120b",
        "accent_bg": "rgba(227,18,11,.08)",
        "accent_border": "rgba(227,18,11,.2)",
        "text": "#2a2a2a",
        "text_dark": "#111111",
        "text_muted": "#6b6b6b",
        "bg": "#f7f5f2",
        "card_bg": "#ffffff",
        "border": "#d9d4cd",
        "border_light": "#e5e1db",
        "font_body": "-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_heading": "Georgia,'Iowan Old Style','Times New Roman','Songti SC','STSong','SimSun',serif",
        "font_mono": "'SF Mono',Menlo,Consolas,'Courier New',monospace",
        "body_font_size": "16px",
        "body_line_height": "1.9",
        "paragraph_margin": "0 0 1.55em",
        "h2_font_size": "22px",
        "h2_line_height": "1.42",
        "h2_margin": "2.05em 0 .78em",
        "h2_padding": "10px 0 0",
        "h2_extra": "border-top:3px solid #e3120b;",
        "h2_font_weight": "700",
        "h3_font_size": "17px",
        "h3_line_height": "1.55",
        "blockquote_margin": "1.7em 0",
        "blockquote_padding": "1.1em 1.15em",
        "blockquote_radius": "0",
        "image_radius": "0",
        "section_padding": "30px 19px 48px",
    },
    "APPLE-GALLERY": {
        "source_refs": ["duyi-wechat-css-layer templates/theme-index.json", "brucecbi/wechat-design-html themes/apple.json"],
        "accent": "#0066cc",
        "accent_bg": "#f5f5f7",
        "accent_border": "#d2d2d7",
        "text": "#2c2c2e",
        "text_dark": "#1d1d1f",
        "text_muted": "#6e6e73",
        "bg": "#ffffff",
        "card_bg": "#f5f5f7",
        "border": "#d2d2d7",
        "border_light": "#e8e8ed",
        "font_body": "-apple-system,BlinkMacSystemFont,'SF Pro Text','Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_heading": "-apple-system,BlinkMacSystemFont,'SF Pro Display','Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_mono": "'SF Mono',Menlo,Consolas,monospace",
        "body_font_size": "17px",
        "body_line_height": "1.92",
        "paragraph_margin": "0 0 1.35em",
        "h2_font_size": "23px",
        "h2_line_height": "1.35",
        "h2_margin": "2.2em 0 .85em",
        "h2_font_weight": "700",
        "h3_font_size": "18px",
        "h3_line_height": "1.5",
        "blockquote_margin": "1.7em 0",
        "blockquote_padding": "1.15em 1.2em",
        "blockquote_radius": "18px",
        "blockquote_line_height": "1.82",
        "image_radius": "18px",
        "section_padding": "30px 20px 48px",
    },
    "LINEAR-MEMO": {
        "source_refs": ["duyi-wechat-css-layer templates/theme-index.json", "brucecbi/wechat-design-html themes/linear.json"],
        "accent": "#5e6ad2",
        "accent_bg": "rgba(94,106,210,.08)",
        "accent_border": "rgba(94,106,210,.2)",
        "text": "#3a3a40",
        "text_dark": "#0d0e10",
        "text_muted": "#62666d",
        "bg": "#fafafa",
        "card_bg": "#ffffff",
        "border": "#e6e6ea",
        "border_light": "#efeff2",
        "font_body": "-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_heading": "-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_mono": "Menlo,Consolas,'Courier New',monospace",
        "body_font_size": "16px",
        "body_line_height": "1.76",
        "paragraph_margin": "0 0 1.28em",
        "h2_font_size": "20px",
        "h2_line_height": "1.45",
        "h2_margin": "2.1em 0 .82em",
        "h2_padding": "0 0 0 12px",
        "h2_extra": "border-left:3px solid #5e6ad2;",
        "h3_font_size": "17px",
        "h3_line_height": "1.5",
        "blockquote_margin": "1.55em 0",
        "blockquote_padding": "1em 1.1em",
        "blockquote_radius": "10px",
        "image_radius": "10px",
        "section_padding": "28px 20px 46px",
    },
    "NOTION-KNOWLEDGE": {
        "source_refs": ["duyi-wechat-css-layer templates/theme-index.json", "brucecbi/wechat-design-html themes/notion.json"],
        "accent": "#5645d4",
        "accent_bg": "rgba(86,69,212,.08)",
        "accent_border": "rgba(86,69,212,.2)",
        "text": "#37352f",
        "text_dark": "#252323",
        "text_muted": "#787774",
        "bg": "#fdfdfb",
        "card_bg": "#fafaf9",
        "border": "#e6e3df",
        "border_light": "#ede9e4",
        "font_body": "-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_heading": "-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_mono": "Menlo,Consolas,'Courier New',monospace",
        "body_font_size": "16px",
        "body_line_height": "1.82",
        "paragraph_margin": "0 0 1.36em",
        "h2_font_size": "21px",
        "h2_line_height": "1.48",
        "h2_margin": "2.1em 0 .85em",
        "h3_font_size": "17px",
        "h3_line_height": "1.55",
        "blockquote_margin": "1.6em 0",
        "blockquote_padding": "1em 1.1em",
        "blockquote_radius": "6px",
        "image_radius": "6px",
        "section_padding": "28px 20px 46px",
    },
    "FT-NEWSPRINT": {
        "source_refs": ["duyi-wechat-css-layer templates/theme-index.json"],
        "accent": "#990f3d",
        "accent_bg": "#fff8f2",
        "accent_border": "#d8c3b0",
        "text": "#262a33",
        "text_dark": "#262a33",
        "text_muted": "#6b625c",
        "bg": "#fff1e5",
        "card_bg": "#fff8f2",
        "border": "#d8c3b0",
        "border_light": "#ead7c7",
        "font_body": "-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_heading": "Georgia,'Times New Roman','Songti SC','STSong','SimSun',serif",
        "font_mono": "Menlo,Consolas,'Courier New',monospace",
        "body_font_size": "16px",
        "body_line_height": "1.88",
        "paragraph_margin": "0 0 1.5em",
        "h2_font_size": "22px",
        "h2_line_height": "1.45",
        "h2_margin": "2.1em 0 .85em",
        "h2_padding": "0 0 8px",
        "h2_extra": "border-bottom:1px solid #262a33;",
        "h3_font_size": "17px",
        "h3_line_height": "1.55",
        "blockquote_margin": "1.7em 0",
        "blockquote_padding": "1.1em 1.15em",
        "blockquote_radius": "0",
        "image_radius": "0",
        "section_padding": "28px 20px 46px",
    },
    "NYT-ESSAY": {
        "source_refs": ["duyi-wechat-css-layer templates/theme-index.json"],
        "accent": "#111111",
        "accent_bg": "#f5f5f5",
        "accent_border": "#111111",
        "text": "#111111",
        "text_dark": "#111111",
        "text_muted": "#666666",
        "bg": "#ffffff",
        "card_bg": "#ffffff",
        "border": "#111111",
        "border_light": "#d6d6d6",
        "font_body": "Georgia,'Times New Roman','Songti SC','STSong','SimSun',serif",
        "font_heading": "Georgia,'Times New Roman','Songti SC','STSong','SimSun',serif",
        "font_mono": "Menlo,Consolas,'Courier New',monospace",
        "body_font_size": "17px",
        "body_line_height": "1.86",
        "paragraph_margin": "0 0 1.45em",
        "h2_font_size": "23px",
        "h2_line_height": "1.42",
        "h2_margin": "2.15em 0 .85em",
        "h3_font_size": "18px",
        "h3_line_height": "1.52",
        "blockquote_margin": "1.7em 0",
        "blockquote_padding": "0 0 0 18px",
        "blockquote_bg": "#ffffff",
        "blockquote_radius": "0",
        "blockquote_font_size": "20px",
        "blockquote_line_height": "1.55",
        "image_radius": "0",
        "section_padding": "30px 20px 48px",
    },
    "WIRED-CULTURE": {
        "source_refs": ["duyi-wechat-css-layer templates/theme-index.json", "VoltAgent/awesome-design-md design-md/wired"],
        "accent": "#151515",
        "accent_bg": "#f6ffe5",
        "accent_border": "#151515",
        "text": "#151515",
        "text_dark": "#151515",
        "text_muted": "#666666",
        "bg": "#ffffff",
        "card_bg": "#ffffff",
        "border": "#151515",
        "border_light": "#d7ff00",
        "font_body": "-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_heading": "-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_mono": "Menlo,Consolas,'Courier New',monospace",
        "body_font_size": "16px",
        "body_line_height": "1.78",
        "paragraph_margin": "0 0 1.36em",
        "h2_font_size": "22px",
        "h2_line_height": "1.32",
        "h2_margin": "2.05em 0 .82em",
        "h2_font_weight": "800",
        "h3_font_size": "17px",
        "h3_line_height": "1.5",
        "strong_color": "#151515",
        "mark_color": "#151515",
        "blockquote_margin": "1.7em 0",
        "blockquote_padding": "1.1em 1.15em",
        "blockquote_radius": "0",
        "image_radius": "0",
        "section_padding": "28px 20px 46px",
    },
    "VERGE-SIGNAL": {
        "source_refs": ["duyi-wechat-css-layer templates/theme-index.json", "VoltAgent/awesome-design-md design-md/theverge"],
        "accent": "#e6007a",
        "accent_bg": "#fff4fb",
        "accent_border": "#151515",
        "text": "#151515",
        "text_dark": "#151515",
        "text_muted": "#666666",
        "bg": "#ffffff",
        "card_bg": "#fff4fb",
        "border": "#151515",
        "border_light": "#f1d6e8",
        "font_body": "-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_heading": "-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_mono": "Menlo,Consolas,'Courier New',monospace",
        "body_font_size": "16px",
        "body_line_height": "1.76",
        "paragraph_margin": "0 0 1.34em",
        "h2_font_size": "22px",
        "h2_line_height": "1.35",
        "h2_margin": "2.05em 0 .82em",
        "h2_padding": "0 0 0 13px",
        "h2_extra": "border-left:5px solid #e6007a;",
        "h2_font_weight": "800",
        "h3_font_size": "17px",
        "h3_line_height": "1.5",
        "blockquote_margin": "1.7em 0",
        "blockquote_padding": "1.1em 1.15em",
        "blockquote_radius": "0",
        "image_radius": "0",
        "section_padding": "28px 20px 46px",
    },
    "FIGMA-FILE": {
        "source_refs": ["duyi-wechat-css-layer templates/theme-index.json", "brucecbi/wechat-design-html themes/figma.json"],
        "accent": "#f24e1e",
        "accent_bg": "rgba(242,78,30,.08)",
        "accent_border": "rgba(242,78,30,.2)",
        "text": "#1e1e1e",
        "text_dark": "#0d0d0d",
        "text_muted": "#6c6c6c",
        "bg": "#ffffff",
        "card_bg": "#f7f7f5",
        "border": "#e6e6e6",
        "border_light": "#f1f1f1",
        "font_body": "-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_heading": "-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
        "font_mono": "Menlo,Consolas,'Courier New',monospace",
        "body_font_size": "16px",
        "body_line_height": "1.8",
        "paragraph_margin": "0 0 1.34em",
        "h2_font_size": "21px",
        "h2_line_height": "1.45",
        "h2_margin": "2.05em 0 .82em",
        "h2_padding": "0 0 0 12px",
        "h2_extra": "border-left:4px solid #f24e1e;",
        "h3_font_size": "17px",
        "h3_line_height": "1.54",
        "blockquote_margin": "1.6em 0",
        "blockquote_padding": "1em 1.1em",
        "blockquote_radius": "12px",
        "image_radius": "12px",
        "section_padding": "28px 20px 46px",
    },
}


def token_theme_to_preset(tokens):
    accent = tokens["accent"]
    accent_bg = tokens.get("accent_bg", "rgba(0,0,0,.04)")
    accent_border = tokens.get("accent_border", accent)
    text = tokens["text"]
    text_dark = tokens["text_dark"]
    text_muted = tokens["text_muted"]
    bg = tokens.get("bg", "#ffffff")
    card_bg = tokens.get("card_bg", "#ffffff")
    border = tokens.get("border", "#dddddd")
    border_light = tokens.get("border_light", "#eeeeee")
    font_body = tokens["font_body"]
    font_heading = tokens.get("font_heading", font_body)
    font_mono = tokens.get("font_mono", "Menlo,Monaco,Consolas,'Courier New',monospace")
    body_size = tokens.get("body_font_size", "16px")
    body_line = tokens.get("body_line_height", "1.82")
    letter_spacing = tokens.get("letter_spacing", "0")
    paragraph_margin = tokens.get("paragraph_margin", "0 0 1.4em")
    h2_weight = tokens.get("h2_font_weight", "700")
    h3_weight = tokens.get("h3_font_weight", "700")
    table_padding = tokens.get("table_cell_padding", ".85em .65em")
    section_padding = tokens.get("section_padding", "0")
    blockquote_family = tokens.get("blockquote_font_family", font_body)
    h2_padding = tokens.get("h2_padding", "0")
    h2_extra = tokens.get("h2_extra", "")
    h3_padding = tokens.get("h3_padding", "0")
    h3_extra = tokens.get("h3_extra", "")
    return {
        "section": f"max-width:100%;box-sizing:border-box;margin:0 auto;padding:{section_padding};background:{bg};color:{text};font-size:{body_size};line-height:{body_line};font-family:{font_body};text-align:left;letter-spacing:{letter_spacing};",
        "p": f"margin:{paragraph_margin};padding:0;color:{text};font-size:{body_size};line-height:{body_line};text-align:left;letter-spacing:{letter_spacing};",
        "h2": f"margin:{tokens.get('h2_margin', '2.1em 0 1em')};padding:{h2_padding};color:{text_dark};font-family:{font_heading};font-size:{tokens.get('h2_font_size', '21px')};line-height:{tokens.get('h2_line_height', '1.5')};font-weight:{h2_weight};text-align:left;letter-spacing:0;{h2_extra}",
        "h3": f"margin:{tokens.get('h3_margin', '1.7em 0 .8em')};padding:{h3_padding};color:{text_dark};font-family:{font_heading};font-size:{tokens.get('h3_font_size', '18px')};line-height:{tokens.get('h3_line_height', '1.6')};font-weight:{h3_weight};text-align:left;letter-spacing:0;{h3_extra}",
        "blockquote": f"margin:{tokens.get('blockquote_margin', '1.6em 0')};padding:{tokens.get('blockquote_padding', '1em 1.15em')};background:{tokens.get('blockquote_bg', accent_bg)};border-left:4px solid {accent};border-radius:{tokens.get('blockquote_radius', '6px')};color:{text};font-family:{blockquote_family};font-size:{tokens.get('blockquote_font_size', body_size)};line-height:{tokens.get('blockquote_line_height', '1.9')};",
        "strong": f"color:{tokens.get('strong_color', accent)};font-weight:700;",
        "mark": f"background:transparent;color:{tokens.get('mark_color', accent)};font-weight:700;padding:0;",
        "code": f"font-family:{font_mono};background:{card_bg};border:1px solid {border_light};border-radius:4px;padding:0 4px;color:{text_dark};font-size:.9em;",
        "figure": f"margin:{tokens.get('figure_margin', '1.7em 0 1.9em')};padding:0;text-align:center;",
        "img": f"display:block;width:100%;height:auto;margin:0 auto;border-radius:{tokens.get('image_radius', '4px')};box-shadow:{tokens.get('image_shadow', 'none')};",
        "ul": f"margin:0 0 1.35em 1.25em;padding:0;color:{text};font-size:{body_size};line-height:{body_line};",
        "ol": f"margin:0 0 1.35em 1.25em;padding:0;color:{text};font-size:{body_size};line-height:{body_line};",
        "li": f"margin:0 0 .62em;padding:0;color:{text};font-size:{body_size};line-height:{body_line};",
        "table": f"width:100%;margin:0;border-collapse:collapse;color:{text};font-size:14px;line-height:1.68;background:{bg};",
        "th": f"padding:{table_padding};border-bottom:2px solid {border};background:{border_light};color:{text_dark};font-weight:700;text-align:left;",
        "td": f"padding:{table_padding};border-bottom:1px solid {border_light};color:{text};text-align:left;",
        "accent": accent,
        "accent_bg": accent_bg,
        "evidence_level": tokens.get("evidence_level", ""),
        "source_refs": tokens.get("source_refs", []),
    }


STYLE_PRESETS.update({key: token_theme_to_preset(tokens) for key, tokens in EVIDENCE_TOKEN_THEMES.items()})

IMAGERY_STYLES = [
    (
        "白瓷",
        "APPLE-GALLERY",
        {
            "blockquote": "margin:2.8em auto;padding:28px 24px 24px;border:none;border-radius:24px;background:#fcfcfc;color:#2c2c2e;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC',sans-serif;font-size:20px;line-height:1.6;font-weight:500;text-align:center;letter-spacing:0;box-shadow:0 2px 20px rgba(0,0,0,.04);",
            "mark": "background:transparent;color:#0066cc;font-weight:600;padding:0;",
        },
    ),
    (
        "蓝图",
        "STRIPE-INFRA",
        {
            "blockquote": "margin:1.65em 0;padding:18px 18px 16px;background:#ffffff;border:1px solid #e3e8ee;border-left:4px solid #533afd;border-radius:12px;color:#273951;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif;font-size:16px;line-height:1.82;box-shadow:0 10px 28px rgba(13,37,61,.08);",
            "code": "font-family:Menlo,Consolas,monospace;background:#eef2ff;border:1px solid #d9e2f3;border-radius:4px;padding:0 4px;color:#3b35a8;font-size:.9em;",
        },
    ),
    (
        "紫线",
        "LINEAR-MEMO",
        {
            "blockquote": "margin:1.5em 0;padding:0 0 0 14px;border-left:2px solid #5e6ad2;border-radius:0;background:transparent;color:#3a3a40;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif;font-size:16px;line-height:1.76;",
            "mark": "background:transparent;color:#5e6ad2;font-weight:740;padding:0;",
        },
    ),
    (
        "墨线",
        "VERCEL-MINIMAL",
        {
            "blockquote": "margin:1.55em 0;padding:0 0 0 16px;border-left:1.5px solid #000;border-radius:0;background:transparent;color:#27272a;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif;font-size:16px;line-height:1.72;font-weight:550;",
            "mark": "background:transparent;color:#000;font-weight:760;padding:0;",
        },
    ),
    (
        "陶土",
        "CLAUDE-RESEARCH",
        {
            "blockquote": "margin:1.7em 0;padding:1.2em 1.25em;background:#f3ece0;border-left:4px solid #c8845c;border-radius:14px;color:#4a3f35;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif;font-size:16px;line-height:1.88;font-style:italic;",
            "mark": "background:#f3ece0;color:#a0633f;font-weight:720;padding:1px 3px;",
        },
    ),
    (
        "宣纸",
        "NOTION-KNOWLEDGE",
        {
            "blockquote": "margin:1.6em 0;padding:18px 20px 16px;background:#faf9f6;border:1px solid #e8e5df;border-left:4px solid #6b5fd4;border-radius:8px;color:#3a3732;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif;font-size:16px;line-height:1.85;",
            "strong": "background:#fbf3db;color:#37352f;font-weight:720;padding:1px 3px;",
            "mark": "background:#fbf3db;color:#37352f;font-weight:720;padding:1px 3px;",
        },
    ),
    (
        "朱批",
        "ECONOMIST-BRIEFING",
        {
            "blockquote": "margin:2.4em auto;padding:24px 18px 16px;border-top:3px solid #c91010;border-left:none;border-radius:0;background:transparent;color:#1a1a1a;font-family:Georgia,'Songti SC',STSong,SimSun,serif;font-size:22px;line-height:1.5;font-weight:700;text-align:center;",
            "mark": "background:transparent;color:#c91010;font-weight:720;padding:0;",
        },
    ),
    (
        "杏纸",
        "FT-NEWSPRINT",
        {
            "blockquote": "margin:1.7em 0;padding:20px 20px 18px;background:#fef7ef;border:1px solid #e8d5bf;border-left:4px solid #991f3d;color:#2a2522;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif;font-size:16px;line-height:1.9;",
        },
    ),
    (
        "素纸",
        "NYT-ESSAY",
        {
            "blockquote": "margin:2.2em 0;padding:0 0 0 20px;border-left:2px solid #1a1a1a;border-radius:0;background:transparent;color:#1a1a1a;font-family:Georgia,'Times New Roman','Songti SC',STSong,SimSun,serif;font-size:21px;line-height:1.55;font-weight:700;",
            "strong": "color:#1a1a1a;font-weight:700;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px;",
        },
    ),
    (
        "萤石",
        "WIRED-CULTURE",
        {
            "blockquote": "margin:1.8em 0;padding:20px 20px 18px;background:#1a1a1a;border-left:4px solid #c8ff00;border-radius:0;color:#d0d0d0;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif;font-size:16px;line-height:1.82;",
            "strong": "background:#c8ff00;color:#1a1a1a;font-weight:800;padding:1px 4px;",
            "mark": "background:#c8ff00;color:#1a1a1a;font-weight:800;padding:1px 4px;",
            "code": "font-family:Menlo,Consolas,monospace;background:#1a1a1a;border:1px solid #333;color:#c8ff00;padding:2px 5px;font-size:.9em;border-radius:0;",
        },
    ),
    (
        "霓虹",
        "VERGE-SIGNAL",
        {
            "blockquote": "margin:1.8em 0;padding:20px 20px 18px;background:#1a1a1a;border-left:5px solid #ff2d8a;border-radius:0;color:#d0d0d0;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif;font-size:16px;line-height:1.8;",
            "mark": "background:transparent;color:#ff2d8a;font-weight:800;padding:0;",
            "code": "font-family:Menlo,Consolas,monospace;background:#1a1a1a;border:1px solid #333;color:#00d4ff;padding:2px 5px;font-size:.9em;border-radius:0;",
        },
    ),
    (
        "橙陶",
        "FIGMA-FILE",
        {
            "blockquote": "margin:1.6em 0;padding:20px 20px 18px;background:#f8f5f0;border:1px solid #e8e0d5;border-left:4px solid #e85d2c;border-radius:14px;color:#2a2420;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif;font-size:16px;line-height:1.82;box-shadow:0 4px 14px rgba(0,0,0,.04);",
        },
    ),
    (
        "朱砂",
        "R",
        {
            "blockquote": "margin:24px 0 30px;padding:20px 18px 18px 16px;background:#fff6f6;border-left:4px solid #d71920;border-radius:2px;color:#444;font-size:15.5px;line-height:1.95;text-align:justify;",
            "mark": "background:transparent;color:#d71920;font-weight:700;padding:0;",
        },
    ),
    (
        "金箔",
        "J",
        {
            "blockquote": "margin:1.8em 0;padding:1em 1.1em;background:#f8f8f8;border-left:3px solid #d6a23a;border-radius:4px;color:#444;font-size:16px;line-height:1.85;",
            "strong": "color:#d6a23a;font-weight:700;",
        },
    ),
    (
        "竹简",
        "L",
        {
            "section": "margin:0 auto;padding:0;color:#3a3530;font-size:17px;line-height:2;font-family:'PingFang SC',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;text-align:left;letter-spacing:.544px;",
            "p": "max-width:232px;margin:0 auto 42px;padding:0;color:#3a3530;font-size:17px;line-height:2;text-align:left;text-indent:0;letter-spacing:.544px;",
            "h2": "margin:2.4em 0 1.7em;padding:0;text-align:center;color:#6b5b4a;font-size:14px;line-height:1.8;font-weight:700;letter-spacing:1px;",
            "h3": "margin:2em 22px 1.1em;padding:0;color:#8b7355;font-size:17px;line-height:1.8;font-weight:700;text-align:left;letter-spacing:1px;",
            "blockquote": "max-width:300px;margin:2em auto;padding:1.15em 1.25em;background:#f5f0e8;border-left:1px solid #8b7355;border-right:1px solid #8b7355;border-radius:6px;color:#5a4a3a;font-size:16px;line-height:1.85;text-align:left;text-indent:0;",
            "strong": "color:#8b7355;font-weight:700;",
            "code": "font-family:Menlo,Monaco,Consolas,'Courier New',monospace;background:#ede5d9;border-radius:3px;padding:0 4px;color:#8b7355;font-size:.92em;",
        },
    ),
    (
        "青笺",
        "T",
        {
            "section": "margin:0 auto;padding:8px;background:#ffffff;color:#222;font-size:16px;line-height:2;font-family:Optima-Regular,PingFangSC-light,'PingFang SC',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;text-align:left;letter-spacing:1.5px;",
            "p": "margin:30px 8px;padding:0;color:#222;font-size:16px;line-height:32px;text-align:left;letter-spacing:1.5px;word-spacing:2px;",
            "blockquote": "margin:28px 8px;padding:0;background:transparent;border:none;border-radius:0;color:#222;font-size:16px;line-height:32px;text-align:left;letter-spacing:1.5px;",
            "strong": "background:#d3f8b6;color:#222;font-weight:500;padding:1px 4px;",
            "mark": "background:#d3f8b6;color:#222;font-weight:500;padding:1px 4px;",
        },
    ),
]


for style_name, base_style, overrides in IMAGERY_STYLES:
    style_preset = STYLE_PRESETS[base_style].copy()
    style_preset.update(overrides)
    STYLE_PRESETS[style_name] = style_preset

STYLE_ALIASES = {
    "C": "A",
    "D": "F",
    "WX": "WECHAT-CLASSIC-READABLE",
    "WECHAT": "WECHAT-CLASSIC-READABLE",
    "WECHAT-CLASSIC": "WECHAT-CLASSIC-READABLE",
    "CLASSIC": "WECHAT-CLASSIC-READABLE",
    "PRIMER": "GITHUB-PRIMER-DOC",
    "GITHUB": "GITHUB-PRIMER-DOC",
    "GITHUB-PRIMER": "GITHUB-PRIMER-DOC",
    "ECONOMIST": "ECONOMIST-BRIEFING",
    "BRIEFING": "ECONOMIST-BRIEFING",
    "CLAUDE": "CLAUDE-RESEARCH",
    "ANTHROPIC": "CLAUDE-RESEARCH",
    "STRIPE": "STRIPE-INFRA",
    "VERCEL": "VERCEL-MINIMAL",
    "ECONOMIST-LITE": "ECONOMIST-BRIEFING-LITE",
    "CLAUDE-LITE": "CLAUDE-RESEARCH-LITE",
    "STRIPE-LITE": "STRIPE-DOC-LITE",
    "VERCEL-LITE": "VERCEL-MINIMAL-DOC",
    "APPLE": "APPLE-GALLERY",
    "APPLE-GALLERY": "APPLE-GALLERY",
    "APPLE-NEWSROOM": "APPLE-GALLERY",
    "LINEAR": "LINEAR-MEMO",
    "LINEAR-MEMO": "LINEAR-MEMO",
    "NOTION": "NOTION-KNOWLEDGE",
    "NOTION-KNOWLEDGE": "NOTION-KNOWLEDGE",
    "FT": "FT-NEWSPRINT",
    "FINANCIAL-TIMES": "FT-NEWSPRINT",
    "FT-NEWSPRINT": "FT-NEWSPRINT",
    "NYT": "NYT-ESSAY",
    "NEW-YORK-TIMES": "NYT-ESSAY",
    "NYT-ESSAY": "NYT-ESSAY",
    "WIRED": "WIRED-CULTURE",
    "WIRED-CULTURE": "WIRED-CULTURE",
    "VERGE": "VERGE-SIGNAL",
    "THE-VERGE": "VERGE-SIGNAL",
    "VERGE-SIGNAL": "VERGE-SIGNAL",
    "FIGMA": "FIGMA-FILE",
    "FIGMA-FILE": "FIGMA-FILE",
    "白瓷": "白瓷",
    "BAICI": "白瓷",
    "蓝图": "蓝图",
    "LANTU": "蓝图",
    "BLUEPRINT": "蓝图",
    "紫线": "紫线",
    "ZIXIAN": "紫线",
    "墨线": "墨线",
    "MOXIAN": "墨线",
    "陶土": "陶土",
    "TAOTU": "陶土",
    "宣纸": "宣纸",
    "XUANZHI": "宣纸",
    "朱批": "朱批",
    "ZHUPI": "朱批",
    "杏纸": "杏纸",
    "XINGZHI": "杏纸",
    "素纸": "素纸",
    "SUZHI": "素纸",
    "萤石": "萤石",
    "YINGSHI": "萤石",
    "霓虹": "霓虹",
    "NIHONG": "霓虹",
    "NEON": "霓虹",
    "橙陶": "橙陶",
    "CHENGTAO": "橙陶",
    "朱砂": "朱砂",
    "ZHUSHA": "朱砂",
    "金箔": "金箔",
    "JINBO": "金箔",
    "竹简": "竹简",
    "ZHUJIAN": "竹简",
    "青笺": "青笺",
    "QINGJIAN": "青笺",
}
MD_EXTENSIONS = ["extra", "sane_lists", "smarty"]
SCRIPT_DIR = Path(__file__).resolve().parent
INLINE_CSS_SCRIPT = SCRIPT_DIR / "inline_css.mjs"


def normalize_style(style):
    style = style.upper()
    return STYLE_ALIASES.get(style, style)


def preset(style):
    return STYLE_PRESETS[normalize_style(style)]


def css_rule(selector, declarations):
    declarations = declarations.strip().rstrip(";")
    return f"{selector}{{{declarations};}}" if declarations else ""


def build_theme_css(style):
    style = normalize_style(style)
    styles = preset(style)
    accent = styles["accent"]
    accent_bg = styles.get("accent_bg", "#f8f8f8")
    rules = [
        css_rule("#output.duyi-root", styles["section"]),
        css_rule(".duyi-p", styles["p"]),
        css_rule(".duyi-h2", styles["h2"]),
        css_rule(".duyi-h3", styles["h3"]),
        css_rule(".duyi-blockquote", styles["blockquote"]),
        css_rule(".duyi-blockquote-p", "margin:0 0 .7em;padding:0;color:inherit;font-size:inherit;line-height:inherit;text-align:inherit"),
        css_rule(".duyi-strong", styles["strong"]),
        css_rule(".duyi-mark", styles.get("mark", styles["strong"])),
        css_rule(".duyi-em", "font-style:italic;color:inherit"),
        css_rule(".duyi-code-inline", styles["code"]),
        css_rule(".duyi-pre", "max-width:100%;overflow-x:auto;margin:1.5em 0;padding:12px;background:#f7f7f7;border-radius:5px;font-size:14px;line-height:1.65"),
        css_rule(".duyi-ul", styles["ul"]),
        css_rule(".duyi-ol", styles.get("ol", styles["ul"])),
        css_rule(".duyi-li", styles["li"]),
        css_rule(".duyi-li-p", "margin:0;padding:0;color:inherit;font-size:inherit;line-height:inherit;text-align:inherit"),
        css_rule(".duyi-figure", styles["figure"]),
        css_rule(".duyi-img", styles["img"]),
        css_rule(".duyi-table-wrap", "max-width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;margin:1.6em 0"),
        css_rule(".duyi-table", styles["table"]),
        css_rule(".duyi-th", styles["th"]),
        css_rule(".duyi-td", styles["td"]),
        css_rule(".duyi-hr", "height:1px;line-height:1px;overflow:hidden;margin:32px 0;background:#ececec"),
        css_rule(".duyi-link", f"color:{accent};text-decoration:none;border-bottom:1px solid rgba(0,0,0,.12)"),
        css_rule(".duyi-math-block", f"max-width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;margin:22px 0;padding:12px 14px;background:{accent_bg};border-left:4px solid {accent};border-radius:4px;color:#333;font-size:15px;line-height:1.9;text-align:left"),
        css_rule(".duyi-math-text", "display:inline;white-space:normal;word-break:break-word;font-family:Menlo,Monaco,Consolas,'Courier New','PingFang SC',sans-serif"),
        css_rule(".duyi-math-inline", "display:inline-block;margin:0 2px;padding:0 3px;border-radius:3px;background:rgba(0,0,0,.04);color:#444;font-size:.92em;line-height:1.6;font-family:Menlo,Monaco,Consolas,'Courier New','PingFang SC',sans-serif"),
        css_rule(".duyi-g-marker-wrap", "margin:2.4em 0 1.4em;text-align:center"),
        css_rule(".duyi-g-marker", "display:inline-block;padding:1px 5px;border-radius:0 0 9px 0;background:#111;color:#fff;font-size:12px;font-weight:700;line-height:1.4;letter-spacing:0"),
        css_rule(".duyi-g-caption", "margin:-.3em 0 1.5em;color:#777;font-size:13px;line-height:1.7;text-align:center"),
        css_rule(".duyi-g-short-quote-wrap", "margin:1.4em 0;text-align:center"),
        css_rule(".duyi-g-short-quote", "display:inline;background:#111;color:#fff;padding:2px 6px;font-size:15px;line-height:1.7"),
        css_rule(".duyi-j-section-no", STYLE_PRESETS["J"]["h2"]),
        css_rule(".duyi-j-section-title", "margin:0 0 1.55em;padding:0;color:#333;font-size:16px;line-height:1.75;font-weight:700;text-align:left;letter-spacing:.02em"),
        css_rule(".duyi-l-pill-wrap", "margin:56px 0 66px;padding:0;text-align:center;text-indent:0"),
        css_rule(".duyi-l-pill", "display:inline-block;min-width:7.8em;padding:7px 28px;background:#dedede;border-radius:22px;color:#444;font-size:14px;line-height:1.7;font-weight:700;letter-spacing:1px"),
        css_rule(".duyi-l-h2-long", "max-width:232px;margin:0 auto 42px;padding:0;color:#444;font-size:17px;line-height:2;font-weight:700;text-align:left;letter-spacing:.544px"),
        css_rule(".duyi-l-h3-wrap", "margin:1.9em 22px 1.1em;padding:0;text-align:left;text-indent:0"),
        css_rule(".duyi-l-h3-label", "display:inline-block;background:#5f9cef;color:#fff;padding:1px 10px;font-size:16px;line-height:1.7;font-weight:700;letter-spacing:1px"),
        css_rule(".duyi-t-label-wrap", "margin:42px 8px 28px;padding:0;text-align:center"),
        css_rule(".duyi-t-label", "display:inline;background:#d3f8b6;color:#333;padding:1px 4px;font-size:16px;line-height:2;font-weight:400;letter-spacing:2px"),
        css_rule(".duyi-t-short-quote-wrap", "margin:10px 0 30px;padding:0;text-align:center"),
        css_rule(".duyi-t-short-quote", "display:inline;background:#d3f8b6;color:#333;padding:1px 4px;font-size:16px;line-height:2;letter-spacing:1.5px"),
    ]
    return "\n".join(rule for rule in rules if rule)


def strip_frontmatter(text):
    return re.sub(r"^---\n.*?\n---\n?", "", text, flags=re.DOTALL)


def extract_title(text):
    body = strip_frontmatter(text)
    lines = body.splitlines()
    title = "Untitled"
    out = []
    consumed_title = False
    for line in lines:
        if not consumed_title and re.match(r"^\s*#\s+", line):
            title = re.sub(r"^\s*#\s+", "", line).strip()
            consumed_title = True
            continue
        out.append(line)
    return title, "\n".join(out).strip()


def read_braced(text, start):
    if start >= len(text) or text[start] != "{":
        return None, start
    depth = 0
    chars = []
    i = start
    while i < len(text):
        ch = text[i]
        if ch == "{":
            if depth:
                chars.append(ch)
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return "".join(chars), i + 1
            chars.append(ch)
        else:
            chars.append(ch)
        i += 1
    return None, start


def replace_underbrace(expr):
    needle = r"\underbrace"
    out = []
    i = 0
    while i < len(expr):
        idx = expr.find(needle, i)
        if idx < 0:
            out.append(expr[i:])
            break
        out.append(expr[i:idx])
        pos = idx + len(needle)
        inner, pos_after_inner = read_braced(expr, pos)
        if inner is None:
            out.append(needle)
            i = pos
            continue
        pos = pos_after_inner
        label = ""
        if pos < len(expr) and expr[pos] == "_":
            candidate, pos_after_label = read_braced(expr, pos + 1)
            if candidate is not None:
                label = latex_to_text(candidate)
                pos = pos_after_label
        inner_text = latex_to_text(inner)
        out.append(f"{inner_text}\uff08{label}\uff09" if label else inner_text)
        i = pos
    return "".join(out)


def replace_frac(expr):
    needle = r"\frac"
    out = []
    i = 0
    while i < len(expr):
        idx = expr.find(needle, i)
        if idx < 0:
            out.append(expr[i:])
            break
        out.append(expr[i:idx])
        pos = idx + len(needle)
        numerator, pos_after_num = read_braced(expr, pos)
        denominator, pos_after_den = read_braced(expr, pos_after_num)
        if numerator is None or denominator is None:
            out.append(needle)
            i = pos
            continue
        out.append(f"({latex_to_text(numerator)} / {latex_to_text(denominator)})")
        i = pos_after_den
    return "".join(out)


def latex_to_text(expr):
    expr = expr.strip()
    previous = None
    while previous != expr:
        previous = expr
        expr = replace_underbrace(expr)
        expr = replace_frac(expr)
    expr = re.sub(r"\\text\{([^{}]*)\}", r"\1", expr)
    replacements = {
        r"\times": "\u00d7",
        r"\cdot": "\u00b7",
        r"\rightarrow": "\u2192",
        r"\Rightarrow": "\u21d2",
        r"\leftarrow": "\u2190",
        r"\to": "\u2192",
        r"\leq": "\u2264",
        r"\geq": "\u2265",
        r"\neq": "\u2260",
        r"\approx": "\u2248",
        r"\%": "%",
    }
    for key, value in replacements.items():
        expr = expr.replace(key, value)
    expr = re.sub(r"\\[a-zA-Z]+", lambda m: m.group(0)[1:], expr)
    expr = expr.replace("{", "").replace("}", "")
    expr = re.sub(r"\s+", " ", expr)
    expr = re.sub(r"\s*([=+\-\u00d7\u00b7\u2192\u21d2\u2190\u2264\u2265\u2260\u2248])\s*", r" \1 ", expr)
    expr = re.sub(r"\(\s+", "(", expr)
    expr = re.sub(r"\s+\)", ")", expr)
    return re.sub(r"\s+", " ", expr).strip()


def math_block_html(raw):
    text = html.escape(latex_to_text(raw))
    return f'\n<div class="duyi-math-block">{text}</div>\n'


def math_inline_html(raw):
    text = html.escape(latex_to_text(raw))
    return f'<span class="duyi-math-inline">{text}</span>'


def protect_math(text):
    text = re.sub(
        r"(?ms)^[ \t]*\$\$[ \t]*\n(.*?)[ \t]*\n[ \t]*\$\$[ \t]*(?=\n|$)",
        lambda m: math_block_html(m.group(1)),
        text,
    )
    text = re.sub(
        r"(?ms)^[ \t]*\\\[(.*?)\\\][ \t]*(?=\n|$)",
        lambda m: math_block_html(m.group(1)),
        text,
    )
    text = re.sub(
        r"(?m)^[ \t]*\$\$(.+?)\$\$[ \t]*$",
        lambda m: math_block_html(m.group(1)),
        text,
    )
    text = re.sub(
        r"(?m)^[ \t]*\\\[(.+?)\\\][ \t]*$",
        lambda m: math_block_html(m.group(1)),
        text,
    )
    text = re.sub(r"\\\((.+?)\\\)", lambda m: math_inline_html(m.group(1)), text)
    text = re.sub(
        r"(?<!\$)\$(?!\$)([^$\n]+?)(?<!\$)\$(?!\$)",
        lambda m: math_inline_html(m.group(1)),
        text,
    )
    return text


def is_markdown_control_line(line):
    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith(("#", ">", "|", "<", "$$", r"\[", "```", "~~~")):
        return True
    if re.match(r"^\s*([-*+])\s+", line):
        return True
    if re.match(r"^\s*\d+[.)]\s+", line):
        return True
    if re.match(r"^\s{0,3}([-*_]\s*){3,}$", line):
        return True
    return False


def normalize_markdown_blocks(text):
    lines = text.splitlines()
    normalized = []
    in_fence = False
    for i, raw in enumerate(lines):
        line = raw
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
        if not in_fence:
            line = re.sub(r"^(\s*)\*\s+", r"\1- ", line)
            line = re.sub(
                r"^( {2,})([-+]\s+)",
                lambda m: (" " * (len(m.group(1)) * 2)) + m.group(2),
                line,
            )
        normalized.append(line)
        if in_fence or i + 1 >= len(lines):
            continue
        next_line = lines[i + 1]
        if (
            line.strip()
            and next_line.strip()
            and not is_markdown_control_line(line)
            and not is_markdown_control_line(next_line)
        ):
            normalized.append("")
    return "\n".join(normalized)


def convert_mark_syntax(text):
    return re.sub(
        r"(?<![=])==([^=\n]+)==(?![=])",
        lambda m: f"<mark>{html.escape(m.group(1).strip())}</mark>",
        text,
    )


def markdown_to_soup(body):
    protected = normalize_markdown_blocks(convert_mark_syntax(protect_math(body)))
    html_body = markdown.markdown(protected, extensions=MD_EXTENSIONS, output_format="html5")
    return BeautifulSoup(html_body, "html.parser")


def replace_with_fragment(tag, html_fragment):
    fragment = BeautifulSoup(html_fragment, "html.parser")
    tag.replace_with(*fragment.contents)


def transform_h2(tag, style, section_no):
    label = tag.get_text(" ", strip=True)
    if style == "G":
        num = label if re.fullmatch(r"\d+", label) else str(section_no)
        caption = ""
        if label and label != num:
            caption = f'<p class="duyi-g-caption">{html.escape(label)}</p>'
        return (
            '<section class="duyi-g-marker-wrap">'
            f'<span class="duyi-g-marker">{html.escape(num)}</span>'
            "</section>"
            + caption
        )
    if style == "J":
        num_match = re.fullmatch(r"0?\d+", label)
        num = label if num_match else f"{section_no:02d}"
        title = ""
        if label and not num_match:
            title = f'<h2 class="duyi-j-section-title">{html.escape(label)}</h2>'
        return f'<p class="duyi-j-section-no">{html.escape(num)}</p>{title}'
    if style == "L":
        compact = len(re.sub(r"\s+", "", label)) <= 12
        if compact:
            return (
                '<p class="duyi-l-pill-wrap">'
                f'<span class="duyi-l-pill">{html.escape(label)}</span>'
                "</p>"
            )
        return f'<h2 class="duyi-l-h2-long">{html.escape(label)}</h2>'
    if style == "T":
        return (
            '<p class="duyi-t-label-wrap">'
            f'<span class="duyi-t-label">{html.escape(label)}</span>'
            "</p>"
        )
    tag["class"] = ["duyi-h2"]
    return None


def prepare_formula_blocks(soup):
    for block in list(soup.select(".duyi-math-block")):
        text = block.get_text(" ", strip=True)
        replacement = soup.new_tag("section")
        replacement["class"] = ["duyi-math-block"]
        span = soup.new_tag("span")
        span["class"] = ["duyi-math-text"]
        span.string = text
        replacement.append(span)
        block.replace_with(replacement)
    for inline in list(soup.select(".duyi-math-inline")):
        inline["class"] = ["duyi-math-inline"]


def apply_semantic_classes(soup, style):
    style = style.upper()
    prepare_formula_blocks(soup)

    section_no = 0
    for h2 in list(soup.find_all("h2")):
        section_no += 1
        fragment = transform_h2(h2, style, section_no)
        if fragment is not None:
            replace_with_fragment(h2, fragment)
    for h3 in soup.find_all("h3"):
        if style == "L":
            label = h3.get_text(" ", strip=True)
            replace_with_fragment(
                h3,
                '<p class="duyi-l-h3-wrap">'
                f'<span class="duyi-l-h3-label">{html.escape(label)}</span>'
                "</p>",
            )
        else:
            h3["class"] = ["duyi-h3"]
    for h4 in soup.find_all("h4"):
        h4["class"] = ["duyi-h3"]
    for p in soup.find_all("p"):
        if p.find_parent("blockquote"):
            p["class"] = ["duyi-blockquote-p"]
        elif p.find_parent("li"):
            p["class"] = ["duyi-li-p"]
        else:
            p["class"] = ["duyi-p"]
    for blockquote in soup.find_all("blockquote"):
        text = blockquote.get_text(" ", strip=True)
        if style == "G" and len(text) <= 32:
            replace_with_fragment(
                blockquote,
                f'<p class="duyi-g-short-quote-wrap"><span class="duyi-g-short-quote">{html.escape(text)}</span></p>',
            )
        elif style == "T" and len(text) <= 40:
            replace_with_fragment(
                blockquote,
                '<p class="duyi-t-short-quote-wrap">'
                f'<span class="duyi-t-short-quote">{html.escape(text)}</span>'
                "</p>",
            )
        else:
            blockquote["class"] = ["duyi-blockquote"]
    for strong in soup.find_all("strong"):
        strong["class"] = ["duyi-strong"]
    for mark in soup.find_all("mark"):
        mark["class"] = ["duyi-mark"]
    for em in soup.find_all("em"):
        em["class"] = ["duyi-em"]
    for code in soup.find_all("code"):
        if not code.find_parent("pre"):
            code["class"] = ["duyi-code-inline"]
    for pre in soup.find_all("pre"):
        pre["class"] = ["duyi-pre"]
    for ul in soup.find_all("ul"):
        ul["class"] = ["duyi-ul"]
    for ol in soup.find_all("ol"):
        ol["class"] = ["duyi-ol"]
    for li in soup.find_all("li"):
        li["class"] = ["duyi-li"]
    for figure in soup.find_all("figure"):
        figure["class"] = ["duyi-figure"]
    for img in soup.find_all("img"):
        img["class"] = ["duyi-img"]
    for table in list(soup.find_all("table")):
        table["class"] = ["duyi-table"]
        if not table.find_parent("section"):
            wrapper = soup.new_tag("section")
            wrapper["class"] = ["duyi-table-wrap"]
            table.wrap(wrapper)
    for th in soup.find_all("th"):
        th["class"] = ["duyi-th"]
    for td in soup.find_all("td"):
        td["class"] = ["duyi-td"]
    for hr in list(soup.find_all("hr")):
        replacement = soup.new_tag("section")
        replacement["class"] = ["duyi-hr"]
        hr.replace_with(replacement)
    for a in soup.find_all("a"):
        a["class"] = ["duyi-link"]
    return soup


def merge_style(existing, addition):
    existing = (existing or "").strip().rstrip(";")
    addition = (addition or "").strip().rstrip(";")
    if existing and addition:
        return f"{existing};{addition};"
    if existing:
        return f"{existing};"
    if addition:
        return f"{addition};"
    return ""


def inline_css_fallback(fragment, css):
    if cssutils is None:
        return fragment
    cssutils.log.setLevel("FATAL")
    soup = BeautifulSoup(fragment, "html.parser")
    sheet = cssutils.parseString(css)
    for rule in sheet:
        if rule.type != rule.STYLE_RULE:
            continue
        declarations = rule.style.cssText.decode("utf-8") if isinstance(rule.style.cssText, bytes) else rule.style.cssText
        for selector in rule.selectorText.split(","):
            selector = selector.strip()
            if not selector or "::" in selector:
                continue
            try:
                matches = soup.select(selector)
            except Exception:
                continue
            for node in matches:
                node["style"] = merge_style(node.get("style"), declarations)
    return str(soup)


def inline_css(fragment, css):
    payload = json.dumps({"html": fragment, "css": css}, ensure_ascii=False)
    try:
        proc = subprocess.run(
            ["node", str(INLINE_CSS_SCRIPT)],
            input=payload,
            text=True,
            capture_output=True,
            check=False,
        )
    except Exception as exc:
        print(f"warn: juice helper unavailable, using python fallback: {exc}", file=sys.stderr)
        return inline_css_fallback(fragment, css)
    if proc.returncode == 0 and proc.stdout:
        return proc.stdout
    print((proc.stderr or "warn: juice helper failed, using python fallback").strip(), file=sys.stderr)
    return inline_css_fallback(fragment, css)


def postprocess_wechat_html(fragment):
    soup = BeautifulSoup(fragment, "html.parser")
    for style_tag in soup.find_all("style"):
        style_tag.decompose()
    for image in soup.find_all("img"):
        extra = []
        for attr in ("width", "height"):
            value = image.get(attr)
            if value:
                unit = "px" if re.fullmatch(r"\d+", value) else ""
                extra.append(f"{attr}:{value}{unit}")
                image.attrs.pop(attr, None)
        if extra:
            image["style"] = merge_style(image.get("style"), ";".join(extra))
    for tag in soup.find_all(True):
        tag.attrs.pop("class", None)
        for attr in list(tag.attrs):
            if attr.startswith("data-"):
                tag.attrs.pop(attr, None)
    # WeChat strips browser-default list-style; convert <ol> to manual numbering
    for ol in list(soup.find_all("ol")):
        ol_style = ol.get("style", "")
        items = ol.find_all("li", recursive=False)
        wrapper = soup.new_tag("section")
        if ol_style:
            wrapper["style"] = ol_style
        for idx, li in enumerate(items, 1):
            li_style = li.get("style", "")
            p = soup.new_tag("p")
            p["style"] = li_style
            num = soup.new_tag("span")
            num["style"] = "margin-right:0.5em;"
            num.string = f"{idx}."
            p.append(num)
            for child in list(li.children):
                p.append(child)
            wrapper.append(p)
        ol.replace_with(wrapper)
    # Same for <ul>: WeChat also strips bullet markers
    for ul in list(soup.find_all("ul")):
        ul_style = ul.get("style", "")
        items = ul.find_all("li", recursive=False)
        wrapper = soup.new_tag("section")
        if ul_style:
            wrapper["style"] = ul_style
        for li in items:
            li_style = li.get("style", "")
            p = soup.new_tag("p")
            p["style"] = li_style
            bullet = soup.new_tag("span")
            bullet["style"] = "margin-right:0.5em;"
            bullet.string = "—"
            p.append(bullet)
            for child in list(li.children):
                p.append(child)
            wrapper.append(p)
        ul.replace_with(wrapper)
    return str(soup).strip() + "\n"


def qa_gate(fragment):
    soup = BeautifulSoup(fragment, "html.parser")
    output = soup.select_one("#output")
    issues = []
    raw_checks = {
        "raw_display_math": "$$",
        "raw_text_command": r"\text",
        "raw_times_command": r"\times",
        "raw_arrow_command": r"\rightarrow",
        "raw_underbrace": r"\underbrace",
        "literal_backslash_n": r"\n",
    }
    for name, needle in raw_checks.items():
        if needle in fragment:
            issues.append(name)
    if output is None:
        issues.append("missing_output_wrapper")
    for p in soup.find_all("p"):
        text = p.get_text("", strip=True)
        if re.match(r"^[-*]\s+", text):
            issues.append("paragraph_list_marker")
            break
        if text == "---":
            issues.append("literal_hr_paragraph")
            break
    for tag_name in ("p", "h2", "h3", "blockquote", "li", "table", "th", "td", "img", "section", "strong", "mark"):
        for tag in soup.find_all(tag_name):
            if tag_name == "section" and tag.get("id") != "output" and not tag.get_text(strip=True):
                continue
            if not tag.get("style"):
                issues.append(f"missing_inline_style:{tag_name}")
                break
    return {
        "ok": not issues,
        "issues": sorted(set(issues)),
    }


def render_document(markdown_text, style):
    style = normalize_style(style)
    title, body = extract_title(markdown_text)
    soup = markdown_to_soup(body)
    semantic = apply_semantic_classes(soup, style)
    body_html = "\n".join(str(node) for node in semantic.contents).strip()
    fragment = "\n".join([
        f'<section id="output" class="duyi-root duyi-style-{style}">',
        body_html,
        "</section>",
    ]) + "\n"
    inlined = inline_css(fragment, build_theme_css(style))
    cleaned = postprocess_wechat_html(inlined)
    return title, cleaned


def render_standalone(title, fragment, base_href=""):
    base_tag = f'<base href="{html.escape(base_href)}">\n' if base_href else ""
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{base_tag}<title>{html.escape(title)}</title>
<style>
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: #f2f2f2; }}
.phone {{ width: 390px; min-height: 844px; margin: 0 auto; background: #fff; padding: 34px 20px 70px; }}
img {{ max-width: 100%; }}
</style>
</head>
<body>
<main class="phone">
{fragment}
</main>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--style", default="A")
    ap.add_argument("--output", required=True)
    ap.add_argument("--standalone", action="store_true", help="wrap the WeChat fragment in a local mobile preview page")
    ap.add_argument("--no-gate", action="store_true", help="write output even if the WeChat QA gate reports issues")
    args = ap.parse_args()
    input_path = Path(args.input).resolve()
    text = input_path.read_text(encoding="utf-8")
    title, fragment = render_document(text, args.style.upper())
    gate = qa_gate(fragment)
    if not gate["ok"] and not args.no_gate:
        print(json.dumps(gate, ensure_ascii=False, indent=2), file=sys.stderr)
        raise SystemExit(2)
    output_path = Path(args.output).resolve()
    if args.standalone:
        rel = os.path.relpath(input_path.parent, output_path.parent)
        base_href = "" if rel == "." else rel.replace(os.sep, "/") + "/"
        output = render_standalone(title, fragment, base_href)
    else:
        output = fragment
    output_path.write_text(output, encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
