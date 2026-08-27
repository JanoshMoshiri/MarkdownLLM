export function applyThemeChoice(state, content, choice) {
  state.themeChoice = ["system", "light", "dark"].includes(choice) ? choice : "system";
  const actual = state.themeChoice === "system"
    ? (matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark")
    : state.themeChoice;
  document.documentElement.dataset.theme = actual;
  document.documentElement.dataset.themeChoice = state.themeChoice;
  localStorage.setItem("mdllm-explorer-theme", state.themeChoice);
  const button = document.querySelector("#theme-toggle");
  button.textContent = state.themeChoice === "system" ? "◐" : actual === "dark" ? "☀" : "☾";
  button.setAttribute("aria-label", `Colour theme: ${state.themeChoice}. Activate to change.`);
  const settingsSelect = content.querySelector('select[aria-label="Colour theme"]');
  if (settingsSelect) settingsSelect.value = state.themeChoice;
}

export function cycleThemeChoice(state, content) {
  const choices = ["system", "light", "dark"];
  applyThemeChoice(state, content, choices[(choices.indexOf(state.themeChoice) + 1) % choices.length]);
}
