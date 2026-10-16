# peterjmarshall.github.io

Source for peterjmarshall.com, built with Quarto and served by GitHub Pages
from the rendered `.html` files in this repository.

## Psychology in 2125 page

The text of `psychology-2125.qmd` comes from a Google Doc, which is the only
place the page's text is edited. Do not edit the `.qmd` by hand: the next
publish regenerates it from the Doc and would overwrite the change.

Google Doc: https://docs.google.com/document/d/1GFr1TucI4dnqg7XwTrutn47T3XDhD95U2Mb-KlqGwZE/edit

To publish a revision:

1. Fetch the Doc's structure with the Google Docs API (`documents.get`)
   and save it as JSON.
2. Regenerate the page source:
   `python3 tools/doc2qmd.py DOC.json psychology-2125.qmd`
3. Render: `quarto render psychology-2125.qmd`
4. Check the diff, then commit both `psychology-2125.qmd` and
   `psychology-2125.html` and push.

The script keeps the page's front matter (title, format, includes), skips
the Doc's Heading 1, turns Heading 2s into sections with anchors, and builds
the "On this page" menu from them. Anchors come from heading text, so
retitling a heading changes its link.

Site design lives here, not in the Doc: `article.css`, `navigation.html`,
`footer.html`, and each page's front matter.

The committed HTML uses Windows (CRLF) line endings; convert after rendering
so diffs show only real changes.
