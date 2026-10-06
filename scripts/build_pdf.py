#!/usr/bin/env python3
"""Build the guide from Markdown with Python's standard library and Typst."""

import json
from pathlib import Path
import shutil
import subprocess

from guide_source import inline, sections

ROOT = Path(__file__).resolve().parents[1]


def main():
    if not shutil.which("typst"):
        raise SystemExit("Typst CLI required: https://typst.app/open-source/")
    overview = sections(ROOT / "source/01-overview.md")
    guide = sections(ROOT / "source/02-character-guide.md")
    roster = {}
    current = None
    for line in (ROOT / "source/03-script-characters.md").read_text().splitlines():
        if line.startswith("### "):
            current = line[4:]
            roster[current] = []
        elif line.startswith("- "):
            roster[current].append(line[2:])
    cache = ROOT / "assets/icons"
    manifest_path = cache / "manifest.json"
    if not manifest_path.exists():
        raise SystemExit("Icons missing. Run: python3 scripts/cache_icons.py")
    manifest = json.loads(manifest_path.read_text())
    names = [name for characters in roster.values() for name in characters]
    icons = {}
    for name in names:
        entry = manifest.get(name)
        if not entry or not (cache / entry["file"]).is_file():
            raise SystemExit(f"Icon missing for {name}. Run: python3 scripts/cache_icons.py")
        icons[name] = "/assets/icons/" + entry["file"]
    adjustments = {}
    for paragraph in guide["Unchanged or minor adjustments"]:
        label = paragraph[0]["text"].rstrip(":")
        body = "".join(run["text"] for run in paragraph[1:]).strip()
        character_list, _, note = body.partition(". ")
        characters = character_list.rstrip(".").split(", ")
        if not all(name in icons for name in characters):
            raise SystemExit(f"Unrecognized small-adjustment character list: {character_list}")
        adjustments[label] = {"characters": characters, "note": inline(note)}
    data = {"overview": overview, "guide": guide, "roster": roster, "icons": icons,
            "adjustments": adjustments}
    generated = ROOT / "build"
    generated.mkdir(exist_ok=True)
    (generated / "guide.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    output = ROOT / "output/pdf/banana-peel-protocol.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "typst", "compile", "--root", str(ROOT),
        str(ROOT / "templates/guide.typ"), str(output),
    ], check=True)
    # Fail visibly if source growth overflows the one-page layout.
    result = subprocess.run([
        "typst", "eval", "--root", str(ROOT),
        "--in", str(ROOT / "templates/guide.typ"),
        "query(metadata).map(item => item.value)",
    ], check=True, capture_output=True, text=True)
    pages = json.loads(result.stdout)
    if pages != [1]:
        raise SystemExit(f"Layout overflow: guide ends on page {pages}. Adjust template before publishing.")
    print(f"Built one-page PDF: {output}")


if __name__ == "__main__":
    main()
