export function renderSearchResults(container, page, onOpen, onMore) {
  const section = document.createElement("section"); section.className = "search-results list"; section.setAttribute("aria-label", "Path search results");
  if (!page.items.length) { const empty = document.createElement("div"); empty.className = "empty"; empty.textContent = "No matching paths."; section.append(empty); }
  for (const item of page.items) appendSearchResult(section, item, onOpen);
  if (page.next_cursor) {
    const more = document.createElement("button"); more.className = "load-more"; more.textContent = "Load more results";
    more.addEventListener("click", () => onMore(page.next_cursor, section, more)); section.append(more);
  }
  if (page.partial) { const note = document.createElement("p"); note.className = "partial-note"; note.textContent = "Results are partial because the source reached its scan limit."; section.append(note); }
  container.replaceChildren(section);
}

export function appendSearchResult(section, item, onOpen) {
  const button = document.createElement("button"); button.className = "collection-item"; button.textContent = item.path;
  button.addEventListener("click", () => onOpen(item.path)); section.append(button); return button;
}
