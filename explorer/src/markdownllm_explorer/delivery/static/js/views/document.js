export function renderDocument(container, document, onMode, embedded = false) {
  const target = embedded ? container.querySelector(".reader") : container;
  if (!target) return;
  target.replaceChildren();
  const head = documentNode("div", "reader-head");
  const title = documentNode("h2"); title.textContent = document.path;
  const actions = documentNode("div", "reader-actions");
  const modes = /\.(?:md|markdown)$/i.test(document.path) ? ["rendered", "raw"] : ["raw"];
  for (const mode of modes) {
    const button = documentNode("button"); button.textContent = mode === "rendered" ? "Styled" : "Raw"; button.disabled = document.mode === mode;
    button.addEventListener("click", () => onMode(mode)); actions.append(button);
  }
  head.append(title, actions); target.append(head);
  // Raw mode puts the frontmatter block on screen already, so folding a
  // second copy above it is duplication the reader has to dismiss.
  if (document.mode !== "raw" && document.frontmatter?.state !== "absent") {
    const details = documentNode("details", "frontmatter"); const summary = documentNode("summary"); summary.textContent = `Frontmatter · ${document.frontmatter.state}`;
    const pre = documentNode("pre"); pre.textContent = JSON.stringify(document.frontmatter.values || {}, null, 2); details.append(summary, pre); target.append(details);
  }
  const body = documentNode("article", `reader-body ${document.mode === "raw" ? "raw" : "markdown"}`);
  if (document.mode === "rendered") body.innerHTML = document.content; else body.textContent = document.content;
  target.append(body);
}

function documentNode(tag, className) { const node = window.document.createElement(tag); if (className) node.className = className; return node; }
