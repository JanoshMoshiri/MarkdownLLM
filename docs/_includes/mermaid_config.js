{
  // Spliced into `mermaid.initialize(...)` by the theme, so an expression is
  // allowed: the diagrams follow the reader's prefers-color-scheme, as
  // head_custom.html makes the page do.
  theme: (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) ? "dark" : "default"
}
