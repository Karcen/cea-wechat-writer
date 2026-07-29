#!/usr/bin/env python3
import argparse
import importlib.util
from pathlib import Path


def load_wechat_renderer(script_dir):
    path = Path(script_dir) / "render_wechat_html.py"
    spec = importlib.util.spec_from_file_location("render_wechat_html", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--style", default="A")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    input_path = Path(args.input).resolve()
    mod = load_wechat_renderer(Path(__file__).parent)
    title, fragment = mod.render_document(input_path.read_text(encoding="utf-8"), args.style.upper())
    output = mod.render_standalone(title, fragment)
    Path(args.output).write_text(output, encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
