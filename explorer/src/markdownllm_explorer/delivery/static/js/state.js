export const state = {
  estate: null,
  source: null,
  view: "overview",
  requestSerial: 0,
  requests: new Map(),
  openDirectories: new Set([""]),
  treeEntries: new Map(),
  treeCursors: new Map(),
  selectedPath: null,
  documentMode: "rendered",
  themeChoice: "system",
  sourceSettings: null,
  repository: null,
  search: {query: "", items: [], cursor: null, partial: false},
};

function identityKey(identity) {
  return JSON.stringify(Object.keys(identity).sort().map(key => [key, identity[key] ?? null]));
}

export function beginRequest(operation, identity) {
  state.requests.get(operation)?.controller.abort();
  const controller = new AbortController();
  const request = {operation, id: ++state.requestSerial, identity: identityKey(identity), controller, signal: controller.signal};
  state.requests.set(operation, request);
  return request;
}

export function isCurrent(request) {
  const current = state.requests.get(request.operation);
  return Boolean(current && current.id === request.id && current.identity === request.identity && !request.signal.aborted);
}

export function completeRequest(request) {
  if (isCurrent(request)) state.requests.delete(request.operation);
}

export function abortAllRequests() {
  state.requests.forEach(request => request.controller.abort());
  state.requests.clear();
}
