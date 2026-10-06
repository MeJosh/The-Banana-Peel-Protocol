#!/usr/bin/env python3
"""Build a Reddit introduction with compact Storyteller advice from Markdown."""

from pathlib import Path
import re

from guide_source import markdown_sections

ROOT = Path(__file__).resolve().parents[1]


def opening_sentences(paragraph, count):
    """Select a compact opening passage from a source paragraph.

    This is an editorial convention, not an automatic summarizer. If a source
    paragraph's ordering changes, review the resulting post before publishing.
    """
    sentences = re.split(r"(?<=[.!?])\s+", paragraph)
    if len(sentences) < count:
        raise ValueError(f"Expected at least {count} sentences: {paragraph}")
    return " ".join(sentences[:count])


def main():
    overview = markdown_sections(ROOT / "source/01-overview.md")
    guide = markdown_sections(ROOT / "source/02-character-guide.md")
    replacements = {
        "title": next(iter(overview)),
        "premise": "\n\n".join(overview["Introduction"]),
        "evil_team": "\n\n".join(overview["Evil team"]),
        "hermit": "\n\n".join(guide["Hermit"]),
        "minor_adjustments": "\n\n".join(guide["Unchanged or minor adjustments"]),
        "changed_roles": "\n\n".join(
            "- " + (
                opening_sentences(paragraph, 3)
                if paragraph.startswith("**Investigator:**")
                else paragraph
            )
            for paragraph in guide["Changed roles and interactions"]
        ),
    }
    # Roster bullets are a separate source format; preserve their names verbatim.
    groups = {}
    current = None
    for line in (ROOT / "source/03-script-characters.md").read_text().splitlines():
        if line.startswith("### "):
            current = line[4:]
            groups[current] = []
        elif line.startswith("- "):
            groups[current].append(line[2:])
    replacements["roster"] = "\n\n".join(
        f"**{kind}:** {', '.join(names)}." for kind, names in groups.items()
    )
    template = (ROOT / "templates/reddit-post.md").read_text()
    def replace(match):
        return replacements[match.group(1)]
    rendered = re.sub(r"\{\{([a-z_]+)\}\}", replace, template)
    if "{{" in rendered or "}}" in rendered:
        raise ValueError("Unresolved template placeholder")
    output = ROOT / "output/reddit/banana-peel-protocol.txt"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered.rstrip() + "\n")
    print(f"Built Reddit post: {output} ({len(rendered.split())} words)")


if __name__ == "__main__":
    main()
