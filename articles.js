/* ============================================================
   MY ARTICLES — the only metadata file you edit to publish.

   To publish a new piece:
     1. Write it in Markdown and save as  articles/<slug>.md
        (slug = lowercase-with-dashes, e.g. articles/why-i-build.md)
     2. Add a line below. Fields:
          slug  — the filename without .md, e.g. "why-i-build"   (required)
          title — display title                                  (required)
          date  — "YYYY-MM-DD", used for sorting + display        (required)

   Newest is shown first automatically (sorted by date).
   ============================================================ */

var articles = [
  { slug: "hello-world", title: "Hello, world", date: "2026-06-04" },
  { slug: "lights-on-nobody-home", title: "Lights on, nobody home", date: "2026-06-28" },
  { slug: "cougars-metal-soccer", title: "Cougars and Master of Puppets", date: "2026-07-11" }
];
