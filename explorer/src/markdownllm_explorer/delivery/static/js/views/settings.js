export function renderSettings(container, settings, themeChoice, onTheme) {
  const rows = [
    ["Source identity", settings.source_id], ["Kind", settings.kind], ["Filesystem root", settings.source_path],
    ["Discovery markers", settings.markers.length ? settings.markers.join(", ") : "None"], ["Git classification", settings.git_kind],
    ["Authority", "Local files and Git; Explorer never writes"],
  ];
  const list = document.createElement("dl"); list.className = "settings-grid";
  for (const [label, value] of rows) { const term = document.createElement("dt"); term.textContent = label; const detail = document.createElement("dd"); detail.textContent = value; list.append(term, detail); }
  const themeTerm = document.createElement("dt"); themeTerm.textContent = "Colour theme";
  const themeDetail = document.createElement("dd"); themeDetail.className = "theme-field";
  const select = document.createElement("select"); select.setAttribute("aria-label", "Colour theme");
  for (const choice of ["system", "light", "dark"]) { const option = document.createElement("option"); option.value = choice; option.textContent = choice[0].toUpperCase() + choice.slice(1); select.append(option); }
  select.value = themeChoice; select.addEventListener("change", () => onTheme(select.value)); themeDetail.append(select);
  list.append(themeTerm, themeDetail);
  container.replaceChildren(list);
}

