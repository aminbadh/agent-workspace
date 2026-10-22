# Typst Cheat-Sheet (version 0.15)

Read this before editing `template.typ`. The engine pins Typst 0.15, and models often write syntax from older versions, from LaTeX or from Markdown. Most edits should only touch the "Look" block at the top of the template.

## Basics

```typst
#let accent = rgb("#1f3a5f")           // a variable; # starts code inside markup
#set text(font: "Libertinus Serif", size: 10.5pt)   // a default for everything after it
#show link: set text(fill: accent)     // restyle every element of one kind
#text(fill: accent, weight: "bold")[Hello]          // content goes in [square brackets]
#block(above: 1em, below: 0.5em, [...])             // spacing around a block
#grid(columns: (1fr, auto), [left], [right])        // a two-column row
#h(1fr)  #v(4pt)                        // horizontal fill, vertical space
```

## Common restyles

| Want | Change |
|---|---|
| Another colour | `#let accent = rgb("#0b6e4f")` |
| Bigger or smaller text | `#let size = 11pt` |
| Tighter page | smaller `margin` and `gap` in the Look block |
| Sans-serif font | put the font's .ttf files in `fonts/`, then `#let font = "Inter"` |
| Headings not in capitals | in `section-title`, replace `upper(str(title))` with `str(title)` |
| Left-aligned header | in the header, `align(center, ...)` becomes `align(left, ...)` |

Built-in fonts, which need no files: Libertinus Serif, New Computer Modern, DejaVu Sans Mono. System fonts are switched off on purpose, so any other font must sit in `fonts/`. Use fonts with an open licence (SIL OFL), such as those on Google Fonts.

## Mistakes models make

- **LaTeX habits:** there is no `\textbf`, `\vspace` or `\\`. Use `strong()`, `v()`, `linebreak()`.
- **Markdown habits:** `**bold**` is wrong in Typst markup; it is `*bold*`. Headings are `=`, not `#`.
- **Strings and content:** `"a" + [b]` fails. Wrap text with `text("a")` before adding content.
- **YAML numbers:** a bare `2026` arrives as an integer. Wrap fields in `str()` before printing.
- **Paths:** forward slashes only, relative to the CV folder. Backslashes are an error in 0.15.
- **Removed or renamed in recent versions:** check the error message and the docs at typst.app/docs rather than guessing an older name.

## After every edit

Build with `--png` and look at the page image before saying the change is done.
