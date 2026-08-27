export const state = {
  estate: null,
  source: null,
  view: "overview",
  requestId: 0,
  controller: null,
  openDirectories: new Set([""]),
  treeEntries: new Map(),
  selectedPath: null,
  documentMode: "rendered",
  themeChoice: "system",
  sourceSettings: null,
  repository: null,
};

export function beginRequest() {
  state.controller?.abort();
  state.controller = new AbortController();
  state.requestId += 1;
  return {id: state.requestId, signal: state.controller.signal};
}

export function isCurrent(id) { return id === state.requestId; }
