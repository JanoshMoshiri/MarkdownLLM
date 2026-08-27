export function renderSearchResults(container, page, onOpen) {
  const section = document.createElement("section"); section.className = "search-results list";
  if (!page.items.length) section.innerHTML = '<div class="empty">No matching paths.</div>';
  for (const item of page.items) {
    const button = document.createElement("button"); button.className = "collection-item"; button.textContent = item.path;
    button.addEventListener("click", () => onOpen(item.path)); section.append(button);
  }
  container.replaceChildren(section);
}

