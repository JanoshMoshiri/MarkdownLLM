export function renderCollection(container, page, kind, onOpen, onMore, collapsed) {
  if (!page.items.length) {
    container.innerHTML = `<div class="empty">No ${kind === "skills" ? "skills" : "memory things"} were found in this source.</div>`;
    return;
  }
  container.innerHTML = '<div class="split-view"><section class="collection" aria-label="Collection items"></section><section class="reader"><div class="empty">Choose an item to read it.</div></section></div>';
  const list = container.querySelector(".collection");
  for (const item of page.items) appendItem(list, item, onOpen, collapsed);
  if (page.next_cursor) {
    const more = document.createElement("button"); more.className = "load-more"; more.textContent = "Load more";
    more.addEventListener("click", () => onMore(page.next_cursor, list, more)); list.append(more);
  }
  if (page.partial) { const note = document.createElement("p"); note.className = "partial-note"; note.textContent = "This collection is partial because the source reached its scan limit."; list.append(note); }
}

export function appendItem(list, item, onOpen, collapsed) {
  const section = sectionFor(list, item.group, collapsed);
  const button = document.createElement("button"); button.type = "button"; button.className = "collection-item";
  button.dataset.path = item.path;
  const title = document.createElement("strong"); title.textContent = item.title;
  const path = document.createElement("small"); path.textContent = item.path;
  button.append(title, path);
  if (item.issues?.length) { const issue = document.createElement("small"); issue.className = "issue"; issue.textContent = item.issues.join(" · "); button.append(issue); }
  button.addEventListener("click", () => { list.querySelectorAll(".active").forEach(node => node.classList.remove("active")); button.classList.add("active"); onOpen(item.path); });
  section.querySelector(".collection-items").append(button);
  refreshCount(section);
  return button;
}

function sectionFor(list, group, collapsed) {
  const existing = [...list.querySelectorAll(".collection-section")].find(node => node.dataset.group === group);
  if (existing) return existing;

  const section = document.createElement("div");
  section.className = "collection-section";
  section.dataset.group = group;

  const heading = document.createElement("button");
  heading.type = "button";
  heading.className = "collection-group";
  const chevron = document.createElement("span");
  chevron.className = "chevron";
  chevron.setAttribute("aria-hidden", "true");
  const label = document.createElement("span");
  label.className = "group-name";
  label.textContent = group;
  // The count is what keeps a collapsed section honest: items loaded into it
  // later are hidden, and a number that moves is the reader's only sign that
  // something arrived.
  const count = document.createElement("span");
  count.className = "group-count";
  heading.append(chevron, label, count);

  const items = document.createElement("div");
  items.className = "collection-items";
  section.append(heading, items);

  const apply = shut => {
    section.classList.toggle("collapsed", shut);
    heading.setAttribute("aria-expanded", shut ? "false" : "true");
    chevron.textContent = shut ? "›" : "⌄";
  };
  apply(collapsed.has(group));
  heading.addEventListener("click", () => {
    const shut = !section.classList.contains("collapsed");
    apply(shut);
    if (shut) collapsed.add(group); else collapsed.delete(group);
  });

  list.append(section);
  return section;
}

function refreshCount(section) {
  const total = section.querySelectorAll(".collection-item").length;
  section.querySelector(".group-count").textContent = String(total);
}
