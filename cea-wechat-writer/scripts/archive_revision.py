#!/usr/bin/env python3
"""Archive an author-approved revision pair for possible future model training."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
import uuid
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--final", type=Path, required=True)
    parser.add_argument("--sources", type=Path, required=True)
    parser.add_argument("--qa", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--category", required=True)
    parser.add_argument("--language", choices=("中文", "英文", "中英文", "其他", "简体中文", "中英双语"), required=True)
    parser.add_argument("--template", required=True)
    parser.add_argument("--author-approved", action="store_true", required=True)
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    files = {
        "generated.md": args.generated.resolve(),
        "final.md": args.final.resolve(),
        "sources.md": args.sources.resolve(),
        "qa-report.md": args.qa.resolve(),
    }
    for path in files.values():
        if not path.is_file():
            parser.error(f"missing input file: {path}")
    if sha256(files["generated.md"]) == sha256(files["final.md"]):
        parser.error("generated and final files are identical; archive after author review or record an explicit evaluation elsewhere")

    now = dt.datetime.now().astimezone()
    record_id = f"{now.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}"
    record_dir = args.output.resolve() / record_id
    if record_dir.exists():
        parser.error(f"record already exists: {record_dir}")
    record_dir.mkdir(parents=True)

    manifest = {
        "schema_version": 1,
        "record_id": record_id,
        "created_at": now.isoformat(timespec="seconds"),
        "author_approved": True,
        "category": args.category,
        "language": args.language,
        "template": args.template,
        "notes": args.notes,
        "files": {},
    }
    for name, source in files.items():
        target = record_dir / name
        shutil.copy2(source, target)
        manifest["files"][name] = {"sha256": sha256(target), "source_path": str(source)}
    (record_dir / "record.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(record_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
