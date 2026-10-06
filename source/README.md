# Guide source

These Markdown files are the editable source for the Banana Peel Protocol guide.

Read or assemble them in this order:

1. [Overview](01-overview.md): the script's premise and evil team.
2. [Character guide](02-character-guide.md): character interactions and Storyteller advice.
3. [Script characters](03-script-characters.md): the character roster, grouped by type.

Keep guide content here so future PDF and Reddit outputs can share the same source. This README is organizational documentation, not part of the guide.

Build the PDF with `python3 scripts/build_pdf.py` from the project root. The Typst layout places the premise, evil team, Hermit, and small adjustment in the left column; all changed roles in the right; and the roster and attribution at the bottom of the page. Small-adjustment groups render their comma-separated character names as labeled horizontal icon rows, followed by the explanatory sentence. Section headings are layout labels. The title and brief subtitle live in the template. Introductory guide framing is omitted from the PDF; substantive source content is retained.

The character guide currently mixes player-facing explanations with Storyteller advice. Rules and interactions remain draft notes pending review.

Build the Reddit introduction with `python3 scripts/build_reddit.py`. It uses the same overview and roster, both small-adjustment groups, the full Hermit entry, and changed-role entries with compact Storyteller advice. The Investigator's generic closing sentence is omitted; its first three sentences are used. Review the post after source edits that change this order. Its structure lives in `templates/reddit-post.md`; output is `output/reddit/banana-peel-protocol.txt`.
