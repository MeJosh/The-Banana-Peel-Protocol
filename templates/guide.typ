// Content comes from source/*.md via scripts/build_pdf.py.
#let data = json("/build/guide.json")
#let ink = rgb("252525")
#let muted = rgb("73706c")
#let accent = rgb("ad9d8c")
#let good = rgb("006da4")
#let evil = rgb("8c2024")
#let heading-height = 22pt

#set document(title: "The Banana Peel Protocol", description: "Script guide and Storyteller notes")
#set page(paper: "us-letter", margin: (x: 0.45in, y: 0.4in))
#set text(font: ("Source Sans 3", "Arial"), size: 11pt, fill: ink)
#set par(leading: 0.55em, spacing: 7pt, justify: false)

#let rich(runs) = {
  for run in runs {
    if run.style == "bold" { strong(run.text) }
    else if run.style == "italic" { emph(run.text) }
    else { text(run.text) }
  }
}

#let icon(name, size: 32pt) = image(data.icons.at(name), width: size, height: size, fit: "contain", alt: name + " character icon")

#let entry(paragraph) = {
  let name = paragraph.first().text.trim(":")
  if paragraph.first().style == "bold" and name in data.icons {
    grid(
      columns: (32pt, 1fr), gutter: 7pt,
      // Keep the icon outside vertical flow so short entries get the same text gap.
      box(width: 32pt, height: 0pt)[#place(top + left, icon(name))], [#rich(paragraph)],
    )
  } else if name in data.adjustments {
    let group = data.adjustments.at(name)
    stack(dir: ttb, spacing: 4pt,
      strong(name + ":"),
      grid(
        columns: group.characters.map(_ => 1fr), gutter: 5pt,
        ..group.characters.map(character => align(center, stack(dir: ttb, spacing: 1pt,
          icon(character, size: 28pt), text(size: 8.5pt, character),
        ))),
      ),
      ..if group.note.len() > 0 { (text(size: 10pt)[#rich(group.note)],) } else { () },
    )
  } else { rich(paragraph) }
}

#let section(title, paragraphs, color: ink, character: none) = [
  #block(above: 8pt, below: 9pt)[
    #block(height: heading-height, above: 0pt, below: 0pt)[
      #align(horizon)[
        #if character != none {
          grid(columns: (28pt, 1fr), gutter: 5pt, align: horizon,
            icon(character, size: heading-height),
            text(font: "Libertinus Serif", size: 12pt, fill: color, upper(title)),
          )
        } else {
          text(font: "Libertinus Serif", size: 12pt, fill: color, upper(title))
        }
      ]
    ]
    #v(2pt)
    #line(length: 100%, stroke: 0.5pt + accent)
  ]
  #set par(spacing: 0pt)
  #let is-group = paragraphs.len() > 0 and paragraphs.first().first().text.trim(":") in data.adjustments
  #stack(dir: ttb, spacing: if is-group { 16pt } else { 14pt },
    ..paragraphs.map(paragraph => block(breakable: false, above: 0pt, below: 0pt)[#entry(paragraph)]),
  )
  #v(5pt)
]

#text(size: 8pt, tracking: 1pt, fill: muted)[BLOOD ON THE CLOCKTOWER / SCRIPT GUIDE & STORYTELLER NOTES]
#v(3pt)
#text(font: "Libertinus Serif", size: 29pt)[The Banana Peel Protocol]
#h(8pt)
#text(font: "Libertinus Serif", size: 12pt, style: "italic")[by MeJosh]
#v(4pt)
#text(size: 10pt, fill: muted)[One Outsider. One Demon. Tread carefully and make sure not to slip!]
#v(8pt)
#line(length: 100%, stroke: 0.7pt + accent)
#v(8pt)

#grid(
  columns: (1fr, 1fr),
  gutter: 20pt,
  [
    #section("The premise", data.overview.at("Introduction"), character: "Klutz")
    #section("The evil team", data.overview.at("Evil team"), color: evil, character: "Vortox")
    #section("The Hermit", data.guide.at("Hermit"), color: good, character: "Drunk")
    #section("No Changes / Minor Adjustments", data.guide.at("Unchanged or minor adjustments"), color: good)
  ],
  [
    #section("Changed roles & interactions", data.guide.at("Changed roles and interactions"), color: good)
  ],
)

#v(1fr)
#block(width: 100%, breakable: false, inset: (top: 6pt), stroke: (top: 0.6pt + accent))[
  #set text(size: 8.5pt)
  #set par(leading: 0.4em, spacing: 3pt)
  #for (kind, characters) in data.roster [
    #strong(kind + ":") #characters.join(" · ") #parbreak()
  ]
  #v(4pt)
  #text(size: 8pt, fill: muted)[Character icons: #link("https://wiki.bloodontheclocktower.com/Main_Page")[Blood on the Clocktower Wiki] / The Pandemonium Institute & contributing artists.]
]
#context metadata(here().page()) <guide-end>
