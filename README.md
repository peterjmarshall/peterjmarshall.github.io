# peterjmarshall.github.io

Source for peterjmarshall.com, built with Quarto and published to GitHub Pages
the same way as *About Development* and *Enacting Life*.

## Editing

1. Pull, then edit the `.qmd` files on `main` (`index.qmd` for the home page,
   `psychology-2125.qmd` for the Psychology in 2125 page).
2. Commit and push to `main`.
3. The `Quarto Publish` GitHub Action renders the site and writes it to the
   `gh-pages` branch, which GitHub Pages serves. **Do not edit `gh-pages` by hand.**

The `.qmd` files are the only source. The Psychology in 2125 page is no longer
generated from a Google Doc.

Site design lives in `article.css`, `navigation.html`, `footer.html`,
`home-navigation.html`, and each page's front matter. `CNAME` and
`Peter-Marshall-CV.pdf` are copied into the published site through
`resources` in `_quarto.yml`.

## Preview locally

```bash
quarto preview
```

## GitHub Pages setting

Settings → Pages → Build and deployment: Source **Deploy from a branch**,
Branch **gh-pages**, Folder **/ (root)**.
