function sourceButton(source, active) {
  const button = document.createElement("button");
  button.className = `source-button${active ? " active" : ""}`;
  button.dataset.source = source.id;
  button.innerHTML = `<span class="source-glyph" aria-hidden="true">${source.kind === "substrate" ? "◇" : "▢"}</span>`;
  const label = document.createElement("span");
  label.textContent = source.display_name;
  button.append(label);
  return button;
}

export function renderSources(container, estate, activeId, onSelect) {
  container.replaceChildren();
  const substrate = estate.sources.find(source => source.kind === "substrate");
  const domains = estate.sources.filter(source => source.kind === "domain");
  const groups = [["Substrate", substrate ? [substrate] : []], ["Domains", domains]];
  for (const [title, sources] of groups) {
    const group = document.createElement("div"); group.className = "source-group";
    const heading = document.createElement("div"); heading.className = "group-label"; heading.textContent = title;
    group.append(heading);
    for (const source of sources) {
      const button = sourceButton(source, source.id === activeId);
      button.addEventListener("click", () => onSelect(source));
      group.append(button);
    }
    if (!sources.length) { const empty = document.createElement("div"); empty.className = "tree-empty"; empty.textContent = "No sources found"; group.append(empty); }
    container.append(group);
  }
}

export function renderTree(container, entries, openDirectories, selectedPath, onDirectory, onFile) {
  container.replaceChildren();
  const rootEntries = entries.get("") || [];
  if (!rootEntries.length) { container.innerHTML = '<div class="tree-empty">No eligible files</div>'; return; }
  const renderLevel = (items, parent) => {
    for (const entry of items) {
      const row = document.createElement("button");
      row.className = `tree-row${selectedPath === entry.path ? " active" : ""}`;
      row.style.paddingLeft = "5px";
      row.setAttribute("role", "treeitem");
      const isOpen = openDirectories.has(entry.path);
      row.innerHTML = `<span class="chevron" aria-hidden="true">${entry.kind === "directory" ? (isOpen ? "⌄" : "›") : ""}</span><span class="file-glyph" aria-hidden="true">${entry.kind === "directory" ? "▢" : "·"}</span>`;
      const label = document.createElement("span"); label.textContent = entry.name; row.append(label);
      row.addEventListener("click", () => entry.kind === "directory" ? onDirectory(entry.path) : onFile(entry.path));
      parent.append(row);
      if (entry.kind === "directory" && isOpen) {
        const children = document.createElement("div"); children.className = "tree-children"; children.setAttribute("role", "group");
        const childItems = entries.get(entry.path);
        if (childItems) renderLevel(childItems, children); else children.innerHTML = '<div class="tree-empty">Loading…</div>';
        parent.append(children);
      }
    }
  };
  renderLevel(rootEntries, container);
}

