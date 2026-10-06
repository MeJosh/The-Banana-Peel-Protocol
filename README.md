# Banana Peel Protocol

Markdown source for the script guide, with Typst PDF and Reddit text outputs.

## Build the Reddit post

Requires only Python 3. No network, Typst, or icons needed.

```sh
python3 scripts/build_reddit.py
```

Output: `output/reddit/banana-peel-protocol.txt`, a UTF-8 text file containing Reddit Markdown. Paste its contents into Reddit's Markdown editor; use the first heading as the post title if desired.

The post introduces the premise and evil team, then covers character interactions, compact Storyteller advice, and the roster. It includes the full Hermit and changed-role entries, except the Investigator's generic closing advice (only its first three sentences are used). Librarian and Empath remain brief because their source entries contain no additional Storyteller advice. Review these selections if you reorder source sentences. `templates/reddit-post.md` controls the post structure and byline. Both targets read the same Markdown through `scripts/guide_source.py`.

## Build the PDF

Requires Python 3 and the [Typst CLI](https://typst.app/open-source/). No Python packages or Typst packages are needed.

From this directory:

```sh
python3 scripts/cache_icons.py  # First setup; skips valid cached icons
python3 scripts/build_pdf.py
```

Output: `output/pdf/banana-peel-protocol.pdf`.

Edit prose in `source/`, then rebuild. `build/guide.json` is generated content; do not edit it. Typography and layout live in `templates/guide.typ`. The build checks that the guide ends on page 1 and reports overflow if the source grows beyond the layout.

The first draft uses US Letter, two columns, a serif title, bronze rules, blue/red headings, and a compact roster, inspired by `Banana_Peel_Protocol_v1_1.png`. It retains substantive source paragraphs, rearranged for the page layout, and omits introductory character-guide framing. It includes Storyteller advice and has not undergone a rules review.

The source converter supports paragraphs, headings, **bold**, _italics_, and the roster's bullet lists. New sections must be added to the template's arrangement.

The official wiki character icons are cached in `assets/icons/`, with source URLs and checksums in `manifest.json`. PDF builds use these local files without network access. Run `python3 scripts/cache_icons.py --refresh` to update them. The downloader discovers image URLs through the wiki's MediaWiki API and validates PNGs before caching.

For the Typst web editor, upload `templates/guide.typ`, generated `build/guide.json`, and `assets/icons/`, preserving those directories. The template uses Source Sans 3 with Arial fallback, plus Libertinus Serif for headings; fonts must be available or uploaded for matching typography.

Layout reference: [Typst documentation](https://typst.app/docs/).
