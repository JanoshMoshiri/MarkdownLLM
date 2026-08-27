export function routeFromHash() {
  return routeFromText(location.hash);
}

export function routeFromText(text) {
  const params = new URLSearchParams(String(text || "").replace(/^#/, ""));
  return {
    source: params.get("source"),
    tab: params.get("tab"),
    mode: params.get("mode"),
    path: params.get("path"),
  };
}

export function validView(view) {
  return ["overview", "skills", "memory", "settings"].includes(view) ? view : "overview";
}

export function writeRoute(state, replace = false) {
  if (!state.source) return;
  const params = new URLSearchParams({
    source: state.source.id,
    tab: state.view,
    mode: state.documentMode,
  });
  if (state.selectedPath) params.set("path", state.selectedPath);
  history[replace ? "replaceState" : "pushState"](null, "", `#${params}`);
}
