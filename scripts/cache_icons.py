#!/usr/bin/env python3
"""Cache official wiki PNG icons. PDF builds remain entirely offline."""

import argparse
import hashlib
import json
from pathlib import Path
import struct
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
WIKI = "https://wiki.bloodontheclocktower.com"
CACHE = ROOT / "assets/icons"
AGENT = "BananaPeelProtocolGuide/1.0 (local character icon cache)"


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def png_size(content):
    if len(content) < 24 or content[:8] != b"\x89PNG\r\n\x1a\n" or content[12:16] != b"IHDR":
        raise ValueError("Expected a PNG icon, not an HTML error page")
    size = struct.unpack(">II", content[16:24])
    if not all(size):
        raise ValueError("Empty PNG icon")
    return size


def slug(name):
    return name.lower().replace(" ", "")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true", help="Re-fetch existing icons")
    args = parser.parse_args()
    names = [line[2:] for line in (ROOT / "source/03-script-characters.md").read_text().splitlines()
             if line.startswith("- ")]
    CACHE.mkdir(parents=True, exist_ok=True)
    manifest_path = CACHE / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    pending = []
    for name in names:
        path = CACHE / (slug(name) + ".png")
        entry = manifest.get(name)
        if not args.refresh and path.exists() and entry:
            content = path.read_bytes()
            png_size(content)
            if hashlib.sha256(content).hexdigest() == entry["sha256"]:
                print(f"Cached: {name}")
                continue
        pending.append(name)
    if not pending:
        print(f"All {len(names)} icons cached; no network requests.")
        return
    filenames = {"File:Icon_" + slug(name) + ".png": name for name in pending}
    query = urllib.parse.urlencode({
        "action": "query", "prop": "imageinfo", "iiprop": "url",
        "titles": "|".join(filenames), "format": "json", "formatversion": "2",
    })
    result = json.loads(fetch(WIKI + "/api.php?" + query))
    # MediaWiki normalizes underscores in file titles to spaces.
    normalized_names = {title.replace("_", " "): name for title, name in filenames.items()}
    urls = {}
    for page in result["query"]["pages"]:
        if page["title"] in normalized_names and page.get("imageinfo"):
            urls[normalized_names[page["title"]]] = page["imageinfo"][0]["url"]
    missing = set(pending) - urls.keys()
    if missing:
        raise ValueError("Wiki icons not found: " + ", ".join(sorted(missing)))
    for name in pending:
        url = urls[name]
        if urllib.parse.urlparse(url).netloc != urllib.parse.urlparse(WIKI).netloc:
            raise ValueError(f"Unexpected icon host: {url}")
        content = fetch(url)
        width, height = png_size(content)
        path = CACHE / (slug(name) + ".png")
        temporary = path.with_suffix(".png.tmp")
        temporary.write_bytes(content)
        temporary.replace(path)
        manifest[name] = {
            "file": path.name, "page": WIKI + "/" + name.replace(" ", "_"),
            "image": url, "width": width, "height": height,
            "sha256": hashlib.sha256(content).hexdigest(),
        }
        temporary_manifest = manifest_path.with_suffix(".json.tmp")
        temporary_manifest.write_text(json.dumps(manifest, indent=2) + "\n")
        temporary_manifest.replace(manifest_path)
        print(f"Downloaded: {name} ({width} x {height})")


if __name__ == "__main__":
    try:
        main()
    except (urllib.error.URLError, ValueError, KeyError) as error:
        raise SystemExit(f"Icon cache failed: {error}")
