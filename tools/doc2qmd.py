#!/usr/bin/env python3
"""Regenerate a page's .qmd from its Google Doc.

The Google Doc is the only place the page's text is edited. This script
converts the Doc's structure (as returned by the Google Docs API,
documents.get) into the .qmd mechanically, so nothing is retyped:

  - the page's YAML front matter is kept from the existing .qmd
    (title, format and includes are site settings, not Doc content);
  - the Doc's first Heading 1 is skipped (the page title comes from
    the front matter);
  - Heading 2 paragraphs become "## Text {#slug}" headings;
  - every other non-empty paragraph becomes <p>...</p>, keeping italics
    and links;
  - the "On this page" contents menu is built from the headings.

Heading IDs are made from the heading text, so retitling a heading
changes its anchor. Check for outside links to an anchor before
retitling.

Usage:
  python3 tools/doc2qmd.py DOC.json psychology-2125.qmd

DOC.json is the documents.get response (optionally wrapped in a
{"content": ...} object). Then render with:
  quarto render psychology-2125.qmd
"""
import html
import json
import re
import sys


def slug(text):
    s = text.lower().replace("’", "").replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def run_html(run):
    text = run["content"].replace("\n", "")
    if not text:
        return ""
    style = run.get("textStyle", {})
    s = html.escape(text, quote=False)
    if style.get("italic") and s.strip():
        core = s.strip()
        lead = s[: len(s) - len(s.lstrip())]
        trail = s[len(s.rstrip()):]
        s = f"{lead}<em>{core}</em>{trail}"
    url = style.get("link", {}).get("url")
    if url:
        s = f'<a href="{html.escape(url)}">{s}</a>'
    return s


def merge_links(s):
    # Adjacent runs with the same link become one <a> element.
    pattern = re.compile(r'(<a href="([^"]+)">)(.*?)</a><a href="\2">')
    while True:
        new = pattern.sub(r"\1\3", s)
        if new == s:
            break
        s = new
    # Keep a link's leading space outside the link, so it isn't underlined.
    return re.sub(r'<a href="([^"]+)">(\s+)', r'\2<a href="\1">', s)


def main(doc_path, qmd_path):
    data = json.load(open(doc_path, encoding="utf-8"))
    doc = data.get("content", data)
    if "tabs" in doc:
        body = doc["tabs"][0]["documentTab"]["body"]["content"]
    else:
        body = doc["body"]["content"]

    old = open(qmd_path, encoding="utf-8").read()
    m = re.match(r"(---\n.*?\n---\n)", old.replace("\r\n", "\n"), re.S)
    if not m:
        sys.exit("No YAML front matter found in " + qmd_path)
    front = m.group(1)

    blocks, toc = [], []
    seen_title = False
    for el in body:
        para = el.get("paragraph")
        if not para:
            continue
        kind = para.get("paragraphStyle", {}).get("namedStyleType", "")
        runs = [e["textRun"] for e in para.get("elements", []) if "textRun" in e]
        plain = "".join(r["content"] for r in runs).strip()
        if not plain:
            continue
        if kind in ("TITLE", "HEADING_1") and not seen_title:
            seen_title = True
            continue
        if kind.startswith("HEADING"):
            ident = slug(plain)
            level = "##" if kind in ("HEADING_1", "HEADING_2") else "###"
            blocks.append(f"{level} {plain} {{#{ident}}}")
            if level == "##":
                toc.append((ident, plain))
            continue
        inner = merge_links("".join(run_html(r) for r in runs))
        blocks.append(f"<p>{inner}</p>")

    nav = ['<nav aria-label="Contents"><details class="contents">'
           '<summary>On this page</summary><ul>']
    nav += [f'<li><a href="#{i}">{html.escape(t, quote=False)}</a></li>'
            for i, t in toc]
    nav.append("</ul></details></nav>")

    out = front + "\n" + "\n".join(nav) + "\n\n" + "\n\n".join(blocks) + "\n"
    open(qmd_path, "w", encoding="utf-8", newline="\n").write(out)
    print(f"Wrote {qmd_path}: {len(blocks)} blocks, {len(toc)} sections")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
