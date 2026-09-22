{%- comment -%}
Spliced into `mermaid.initialize(...)` by the theme, so an expression is
allowed: the diagrams follow the reader's prefers-color-scheme, as
head_custom.html makes the page do. The note is a Liquid comment, never a JS
`//` one: the theme compresses the page onto one line, and a line comment
would swallow the rest of the script (the first build's blank diagrams).
{%- endcomment -%}
{ theme: (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) ? "dark" : "default" }
