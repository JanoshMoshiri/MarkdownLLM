export function renderCollection(container, page, kind, onOpen, onMore) {
  if (!page.items.length) {
    container.innerHTML = `<div class="empty">No ${kind === "skills" ? "skills" : "memory things"} were found in this source.</div>`;
    return;
  }
  container.innerHTML = '<div class="split-view"><section class="collection" aria-label="Collection items"></section><section class="reader"><div class="empty">Choose an item to read it.</div></section></div>';
  const list = container.querySelector(".collection");
  let group = "";
  for (const item of page.items) {
    if (item.group !== group) { group = item.group; const heading = document.createElement("div"); heading.className = "collection-group"; heading.textContent = group; list.append(heading); }
    appendItem(list, item, onOpen);
  }
  if (page.next_cursor) {
    const more = document.createElement("button"); more.className = "load-more"; more.textContent = "Load more";
    more.addEventListener("click", () => onMore(page.next_cursor, list, more)); list.append(more);
  }
}

export function appendItem(list, item, onOpen) {
  const button = document.createElement("button"); button.className = "collection-item";
  const title = document.createElement("strong"); title.textContent = item.title;
  const path = document.createElement("small"); path.textContent = item.path;
  button.append(title, path);
  if (item.issues?.length) { const issue = document.createElement("small"); issue.className = "issue"; issue.textContent = item.issues.join(" · "); button.append(issue); }
  button.addEventListener("click", () => { list.querySelectorAll(".active").forEach(node => node.classList.remove("active")); button.classList.add("active"); onOpen(item.path); });
  list.append(button);
}

