"""Read the guide's shared Markdown without external dependencies."""

import re


def markdown_sections(path):
    result = {}
    current = None
    for block in re.split(r"\n\s*\n", path.read_text().strip()):
        if block.startswith("#"):
            current = block.lstrip("#").strip()
            if current in result:
                raise ValueError(f"Duplicate heading in {path}: {current}")
            result[current] = []
        elif current is not None:
            result[current].append(" ".join(block.splitlines()))
        else:
            raise ValueError(f"Content before heading in {path}")
    return result


def inline(text):
    """Supported source markup: **bold** and _italic_; never evaluate content."""
    return [
        {"style": "bold", "text": part[2:-2]}
        if part.startswith("**")
        else {"style": "italic", "text": part[1:-1]}
        if part.startswith("_")
        else {"style": "plain", "text": part}
        for part in re.split(r"(\*\*[^*]+\*\*|_[^_]+_)", text)
        if part
    ]


def sections(path):
    return {heading: [inline(text) for text in paragraphs]
            for heading, paragraphs in markdown_sections(path).items()}
