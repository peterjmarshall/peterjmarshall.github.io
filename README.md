# peterjmarshall.github.io

Source for peterjmarshall.com, built with Quarto and published to GitHub Pages
the same way as *About Development* and *Enacting Life*.

## Editing

1. Pull, then edit the `.qmd` files on `main` (`index.qmd` for the home page,
   `psychology-2125.qmd` for the Psychology in 2125 page, `cv.qmd` for the CV).
2. Commit and push to `main`.
3. The `Quarto Publish` GitHub Action renders the site and writes it to the
   `gh-pages` branch, which GitHub Pages serves. **Do not edit `gh-pages` by hand.**

The `.qmd` files are the only source. The Psychology in 2125 page is no longer
generated from a Google Doc.

Site design lives in `article.css`, `navigation.html`, `footer.html`,
`home-navigation.html`, and each page's front matter. `CNAME` is copied into
the published site through `resources` in `_quarto.yml`.

## Editing the CV

`cv.qmd` is plain Markdown inside a few wrappers:

- Dated lines (appointments, education, service, editorial, awards) sit inside
  `::: {.cv-list}` and start with the date in a span:
  `[2016–2026]{.cv-date} Chair, Department of Psychology & Neuroscience`.
  End a line with `\` to continue the same entry on the next line.
- Publications and presentations sit inside `::: {.cv-refs}`, one citation
  per paragraph (blank line between them).
- Grants sit inside `::: {.cv-grants}`, one grant per paragraph, lines joined
  with `\`.
- The "Sections" list near the top is hand-written HTML; update it if you add
  or rename a top-level `##` section.

Visitors who need a PDF can use the browser's Print → Save as PDF; the print
styles hide navigation.

## If a change doesn't appear online

Check the Actions tab. If "pages build and deployment" failed (usually a
GitHub-side timeout), open "Quarto Publish" and click "Run workflow" on `main`.
That always pushes a fresh copy and starts a new deployment.

## Preview locally

```bash
quarto preview
```

## GitHub Pages setting

Settings → Pages → Build and deployment: Source **Deploy from a branch**,
Branch **gh-pages**, Folder **/ (root)**.
