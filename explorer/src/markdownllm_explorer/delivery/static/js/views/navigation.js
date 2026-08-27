function sourceButton(source, active) {
  const button = document.createElement("button");
  button.className = `source-button${active ? " active" : ""}`;
  button.dataset.source = source.id;
  button.setAttribute("aria-current", active ? "page" : "false");
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
  for (const [title, sources] of [["Substrate", substrate ? [substrate] : []], ["Domain estate", domains]]) {
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

export function renderTree(container, entries, cursors, openDirectories, selectedPath, onDirectory, onFile, onMore) {
  container.replaceChildren();
  const rootEntries = entries.get("") || [];
  if (!rootEntries.length) { const empty = document.createElement("div"); empty.className = "tree-empty"; empty.textContent = "No eligible files"; container.append(empty); return; }
  let firstItem = true;
  const renderLevel = (items, parent, level, parentPath) => {
    for (const entry of items) {
      const row = document.createElement("button");
      const isOpen = openDirectories.has(entry.path);
      row.className = `tree-row${selectedPath === entry.path ? " active" : ""}`;
      row.dataset.path = entry.path; row.dataset.kind = entry.kind; row.dataset.parent = parentPath;
      row.setAttribute("role", "treeitem"); row.setAttribute("aria-level", String(level));
      row.setAttribute("aria-selected", selectedPath === entry.path ? "true" : "false");
      if (entry.kind === "directory") row.setAttribute("aria-expanded", isOpen ? "true" : "false");
      row.tabIndex = selectedPath === entry.path || (!selectedPath && firstItem) ? 0 : -1;
      firstItem = false;
      row.innerHTML = `<span class="chevron" aria-hidden="true">${entry.kind === "directory" ? (isOpen ? "⌄" : "›") : ""}</span><span class="file-glyph" aria-hidden="true">${entry.kind === "directory" ? "▢" : "·"}</span>`;
      const label = document.createElement("span"); label.textContent = entry.name; row.append(label);
      row.addEventListener("click", () => entry.kind === "directory" ? onDirectory(entry.path) : onFile(entry.path));
      parent.append(row);
      if (entry.kind === "directory" && isOpen) {
        const children = document.createElement("div"); children.className = "tree-children"; children.setAttribute("role", "group");
        const childItems = entries.get(entry.path);
        if (childItems) renderLevel(childItems, children, level + 1, entry.path); else { const loading = document.createElement("div"); loading.className = "tree-empty"; loading.textContent = "Loading…"; children.append(loading); }
        parent.append(children);
      }
    }
    const cursor = cursors.get(parentPath);
    if (cursor) {
      const more = document.createElement("button"); more.className = "tree-more"; more.dataset.parent = parentPath;
      more.textContent = "Load more files"; more.addEventListener("click", () => onMore(parentPath, cursor, more)); parent.append(more);
    }
  };
  renderLevel(rootEntries, container, 1, "");
  installTreeKeyboard(container, onDirectory, onFile);
}

function installTreeKeyboard(container, onDirectory, onFile) {
  container.onkeydown = event => {
    const row = event.target.closest?.('[role="treeitem"]');
    if (!row) return;
    const visible = [...container.querySelectorAll('[role="treeitem"]')].filter(node => node.offsetParent !== null);
    const index = visible.indexOf(row);
    const focus = target => { if (!target) return; visible.forEach(node => { node.tabIndex = node === target ? 0 : -1; }); target.focus(); };
    if (event.key === "ArrowDown") { event.preventDefault(); focus(visible[index + 1] || visible[0]); }
    else if (event.key === "ArrowUp") { event.preventDefault(); focus(visible[index - 1] || visible.at(-1)); }
    else if (event.key === "Home") { event.preventDefault(); focus(visible[0]); }
    else if (event.key === "End") { event.preventDefault(); focus(visible.at(-1)); }
    else if (event.key === "ArrowRight" && row.dataset.kind === "directory") {
      event.preventDefault();
      if (row.getAttribute("aria-expanded") === "false") onDirectory(row.dataset.path); else focus(visible[index + 1]);
    } else if (event.key === "ArrowLeft") {
      event.preventDefault();
      if (row.dataset.kind === "directory" && row.getAttribute("aria-expanded") === "true") onDirectory(row.dataset.path);
      else focus(visible.find(node => node.dataset.path === row.dataset.parent));
    } else if (event.key === "Enter" || event.key === " ") {
      event.preventDefault(); row.dataset.kind === "directory" ? onDirectory(row.dataset.path) : onFile(row.dataset.path);
    }
  };
}
