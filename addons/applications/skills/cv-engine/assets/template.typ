// The CV's look. The content lives in a YAML file next to this one; the build script passes
// its path in as `sys.inputs.content`. Restyle by changing the "Look" block first. To use
// another font, put its .ttf or .otf files in fonts/ beside this file and name it below.

#let data = yaml(sys.inputs.content)

// ---- Look -------------------------------------------------------------------
#let font = "Libertinus Serif"   // built in, needs no files
#let size = 10.5pt
#let accent = rgb("#1f3a5f")     // name, headings and links
#let ink = rgb("#222222")        // body text
#let muted = rgb("#666666")      // dates, places, notes
#let margin = (x: 16mm, y: 13mm)
#let gap = 0.55em                // space between lines and paragraphs
// -----------------------------------------------------------------------------

// Plain text with *bold* spans and [label](url) links. Nothing else is interpreted, so
// characters such as @ # $ print as written. Apostrophes become typographic.
#let bold-split(s) = for (i, part) in s.replace("'", "’").split("*").enumerate() {
  if calc.odd(i) { strong(part) } else { text(part) }
}
#let rich(s) = {
  let s = str(s)
  let pos = 0
  for m in s.matches(regex("\[([^\]]+)\]\(([^)\s]+)\)")) {
    bold-split(s.slice(pos, m.start))
    link(m.captures.at(1), bold-split(m.captures.at(0)))
    pos = m.end
  }
  bold-split(s.slice(pos))
}

#let maybe-link(body, url) = if url == none { body } else { link(url, body) }

#set document(title: str(data.name) + " - CV", author: str(data.name))
#set page(paper: data.at("paper", default: "a4"), margin: margin)
#set text(font: font, size: size, fill: ink, lang: data.at("lang", default: "en"))
#set par(leading: gap, spacing: gap, justify: false)
#set list(indent: 0.2em, body-indent: 0.5em, spacing: gap)
#show link: set text(fill: accent)

// ---- Header -----------------------------------------------------------------
#align(center, {
  text(size: 2em, weight: "bold", fill: accent, str(data.name))
  if "headline" in data {
    linebreak()
    text(fill: muted, rich(data.headline))
  }
  if "contact" in data {
    linebreak()
    data.contact
      .map(c => if type(c) == dictionary {
        maybe-link(text(str(c.text)), c.at("url", default: none))
      } else { text(str(c)) })
      .join(text(fill: muted)[ #h(0.3em)|#h(0.3em) ])
  }
})

// ---- Section parts ----------------------------------------------------------
#let section-title(title) = block(
  above: 1.1em, below: 0.6em, sticky: true, width: 100%,
  stroke: (bottom: 0.5pt + accent), inset: (bottom: 2pt),
  text(size: 1.1em, weight: "bold", fill: accent, tracking: 0.04em, upper(str(title))),
)

#let entry(e) = block(above: 0.85em, below: 0.4em, {
  let head = strong(maybe-link(text(str(e.title)), e.at("url", default: none)))
  if "role" in e { head = [#head, #emph(rich(e.role))] }
  grid(
    columns: (1fr, auto), column-gutter: 1em,
    head, text(fill: muted, str(e.at("date", default: ""))),
  )
  let details = (e.at("place", default: none), e.at("note", default: none)).filter(x => x != none)
  if details.len() > 0 { block(above: 0.3em, text(fill: muted, rich(details.map(str).join(" · ")))) }
  if "bullets" in e { list(..e.bullets.map(rich)) }
})

#let lines(items) = grid(
  columns: (auto, 1fr), column-gutter: 0.8em, row-gutter: gap,
  ..items.map(l => (strong(text(str(l.label))), rich(l.text))).flatten(),
)

// ---- Body -------------------------------------------------------------------
#for s in data.sections {
  section-title(s.title)
  if "text" in s { rich(s.text) }
  if "entries" in s { for e in s.entries { entry(e) } }
  if "lines" in s { lines(s.lines) }
}

// Read back by the build script to report the page count against the limit.
#context [#metadata(counter(page).final().first()) <pages>]
#metadata(data.at("max_pages", default: 1)) <max-pages>
