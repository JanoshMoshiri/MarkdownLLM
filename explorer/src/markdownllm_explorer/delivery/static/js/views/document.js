export function renderDocument(container, record, onMode, embedded = false) {
  const target = embedded ? container.querySelector(".reader") : container;
  if (!target) return;
  target.replaceChildren();
  const head = documentNode("div", "reader-head");
  const title = documentNode("h2"); title.textContent = record.path;
  const actions = documentNode("div", "reader-actions");
  const modes = /\.(?:md|markdown)$/i.test(record.path) ? ["rendered", "raw"] : ["raw"];
  for (const mode of modes) {
    const button = documentNode("button"); button.textContent = mode === "rendered" ? "Styled" : "Raw"; button.disabled = record.mode === mode;
    button.addEventListener("click", () => onMode(mode)); actions.append(button);
  }
  head.append(title, actions); target.append(head);
  // Raw mode puts the frontmatter block on screen already, so folding a
  // second copy above it is duplication the reader has to dismiss.
  if (record.mode !== "raw" && record.frontmatter?.state !== "absent") {
    const details = documentNode("details", "frontmatter"); const summary = documentNode("summary"); summary.textContent = `Frontmatter · ${record.frontmatter.state}`;
    const pre = documentNode("pre"); pre.textContent = JSON.stringify(record.frontmatter.values || {}, null, 2); details.append(summary, pre); target.append(details);
  }
  const body = documentNode("article", `reader-body ${record.mode === "raw" ? "raw" : "markdown"}`);
  if (record.mode === "rendered") body.innerHTML = record.content; else body.textContent = record.content;
  target.append(body);
}

function documentNode(tag, className) { const node = document.createElement(tag); if (className) node.className = className; return node; }
