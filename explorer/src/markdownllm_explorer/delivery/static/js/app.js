import {captureCapability, get, touch} from "./api.js";
import {installActivityLease} from "./activity.js";
import {abortAllRequests, beginRequest, completeRequest, isCurrent, state} from "./state.js";
import {routeFromHash, routeFromText, validDocumentSurface, validView, writeRoute} from "./routing.js";
import {applyThemeChoice as applyTheme, cycleThemeChoice} from "./theme.js";
import {activeOverlay, closeOverlays, openOverlay, visibleFocusable} from "./overlays.js";
import {initialiseLayout} from "./layout.js";
import {renderSources, renderTree} from "./views/navigation.js";
import {appendCommit, refreshCommitAbbreviations, renderOverview} from "./views/overview.js";
import {appendItem, renderCollection} from "./views/collection.js";
import {renderDocument} from "./views/document.js";
import {renderCommit, renderCommitDocument} from "./views/commit.js";
import {renderSettings} from "./views/settings.js";
import {appendSearchResult, renderSearchResults} from "./views/tree.js";
import {applyReferenceResolution, referencedIds, renderDocumentContext, renderSourceContext} from "./views/context.js";

const content = document.querySelector("#content");
const notice = document.querySelector("#notice");
const sourceNav = document.querySelector("#source-nav");
const fileTree = document.querySelector("#file-tree");
const contextContent = document.querySelector("#context-content");
const tabs = [...document.querySelectorAll('[role="tab"]')];
let searchTimer;
let stopActivityLease;

async function initialise() {
  applyThemeChoice(localStorage.getItem("mdllm-explorer-theme") || "system");
  bindChrome();
  if (!captureCapability()) {
    showError({message: "Open Explorer using the launch URL printed by mdllm-explorer.", code: "capability_required"});
    return;
  }
  try {
    const session = await get("/api/v1/session");
    stopActivityLease = installActivityLease({
      timeoutSeconds: session.idle_timeout_seconds,
      sendTouch: touch,
      onExpire: () => showIdleExpired(session.idle_timeout_seconds),
    });
  } catch (error) {
    showError(error);
    return;
  }
  showLoading();
  const request = beginRequest("estate", {route: "/api/v1/estate"});
  try {
    const estate = await get("/api/v1/estate", {}, request.signal);
    if (!isCurrent(request)) return;
    state.estate = estate;
    if (estate.issues.length) showNotice(`${estate.issues.length} estate discovery issue${estate.issues.length === 1 ? "" : "s"} reported.`);
    const routed = routeFromHash();
    const requested = routed.source && estate.sources.find(item => item.id === routed.source);
    state.view = validView(routed.tab);
    state.documentMode = routed.mode === "raw" ? "raw" : "rendered";
    state.commit = routed.commit || null;
    await selectSource(requested || estate.sources[0], false);
    state.documentSurface = routed.path && !state.commit ? restoredSurface(routed) : null;
    if (state.commit) { if (routed.path) await openCommitFile(routed.path, false); else updateRoute(true); }
    else if (routed.path) await restoreDocumentRoute(routed.path, state.documentMode, state.documentSurface, true);
    else updateRoute(true);
  } catch (error) {
    if (error.name !== "AbortError" && isCurrent(request)) showError(error);
  } finally { completeRequest(request); }
}

function bindChrome() {
  tabs.forEach(button => button.addEventListener("click", () => chooseTab(button.dataset.view)));
  document.querySelector('[role="tablist"]').addEventListener("keydown", event => {
    if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
    event.preventDefault();
    const current = Math.max(0, tabs.indexOf(document.activeElement));
    const target = event.key === "Home" ? tabs[0] : event.key === "End" ? tabs.at(-1) : tabs[(current + (event.key === "ArrowRight" ? 1 : -1) + tabs.length) % tabs.length];
    target.focus(); chooseTab(target.dataset.view);
  });
  document.querySelector("#tree-refresh").addEventListener("click", () => loadRootTree(true));
  document.querySelector("#theme-toggle").addEventListener("click", cycleTheme);
  initialiseLayout(openOverlay, () => closeOverlays(false));
  document.querySelector("#sidebar-close").addEventListener("click", closeOverlays);
  document.querySelector("#context-close").addEventListener("click", closeOverlays);
  document.querySelector("#search-input").addEventListener("input", event => {
    clearTimeout(searchTimer); const query = event.target.value.trim();
    searchTimer = setTimeout(() => query ? search(query) : clearSearch(), 220);
  });
  document.addEventListener("keydown", event => {
    if (event.key === "Escape") closeOverlays();
    if (event.key !== "Tab") return;
    const panel = activeOverlay();
    if (!panel) return;
    const focusable = visibleFocusable(panel);
    if (!focusable.length) return;
    const first = focusable[0], last = focusable.at(-1);
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  });
  document.addEventListener("click", event => {
    const anchor = event.target.closest?.('a[href^="#source="]');
    if (!anchor) return;
    event.preventDefault(); const route = routeFromText(anchor.getAttribute("href"));
    if (route.path) {
      const opener = state.documentSurface === "collection" ? openCollectionDocument : openDocument;
      opener(route.path, "rendered");
    }
  });
  window.addEventListener("popstate", restoreRoute);
  matchMedia("(prefers-color-scheme: light)").addEventListener?.("change", () => { if (state.themeChoice === "system") applyThemeChoice("system"); });
}

async function chooseTab(view) {
  abortAllRequests(); clearTimeout(searchTimer);
  state.view = validView(view); state.selectedPath = null; state.documentSurface = null; state.commit = null;
  state.search = {query: "", items: [], cursor: null, partial: false};
  document.querySelector("#search-input").value = "";
  renderSourceContext(contextContent, state.source, state.sourceSettings, state.repository);
  activateTab(); updateRoute(); await loadView();
}

async function selectSource(source, pushRoute = true) {
  if (!source) throw new Error("No discoverable source is available.");
  abortAllRequests();
  clearTimeout(searchTimer);
  state.source = source; state.selectedPath = null; state.documentSurface = null; state.sourceSettings = null; state.repository = null;
  state.treeEntries.clear(); state.treeCursors.clear(); state.treePartials.clear(); state.openDirectories = new Set([""]);
  state.search = {query: "", items: [], cursor: null, partial: false};
  document.querySelector("#search-input").value = "";
  document.querySelector("#source-name").textContent = source.display_name;
  document.querySelector("#source-kind").textContent = source.kind === "substrate" ? "Framework source" : "Domain source";
  document.querySelector("#source-icon").textContent = source.display_name.slice(0, 1).toUpperCase();
  renderSources(sourceNav, state.estate, source.id, chosen => { state.commit = null; selectSource(chosen); });
  closeOverlays(false);
  if (pushRoute) updateRoute();
  await Promise.all([loadRootTree(), loadView(), loadSourceContext()]);
}

async function loadTreePage(path, cursor = null, append = false) {
  if (!state.source) return false;
  const sourceId = state.source.id;
  const request = beginRequest(`tree:${path}`, {source: sourceId, path, cursor});
  try {
    const page = await get("/api/v1/tree", {source: sourceId, path, cursor}, request.signal);
    if (!isCurrent(request)) return false;
    const prior = append ? (state.treeEntries.get(path) || []) : [];
    const known = new Set(prior.map(item => item.path));
    state.treeEntries.set(path, [...prior, ...page.items.filter(item => !known.has(item.path))]);
    state.treeCursors.set(path, page.next_cursor || null);
    state.treePartials.set(path, page.partial);
    renderCurrentTree();
    return true;
  } catch (error) {
    if (error.name !== "AbortError" && isCurrent(request)) setTreeError(error);
    return false;
  } finally { completeRequest(request); }
}

async function loadRootTree(force = false) {
  if (!state.source) return;
  if (!force && state.treeEntries.has("")) { renderCurrentTree(); return; }
  if (force) { state.treeEntries.clear(); state.treeCursors.clear(); state.treePartials.clear(); state.openDirectories = new Set([""]); }
  await loadTreePage("");
}

async function toggleDirectory(path, focusMode = "self") {
  if (state.openDirectories.has(path)) {
    state.openDirectories.delete(path); renderCurrentTree(); focusTreePath(path); return;
  }
  state.openDirectories.add(path); renderCurrentTree();
  if (!state.treeEntries.has(path)) await loadTreePage(path);
  if (focusMode === "child") {
    const child = (state.treeEntries.get(path) || [])[0];
    focusTreePath(child?.path || path);
  } else focusTreePath(path);
}

async function loadMoreTree(path, cursor, button) {
  button.disabled = true;
  const before = (state.treeEntries.get(path) || []).length;
  const loaded = await loadTreePage(path, cursor, true);
  if (!loaded) { document.querySelector(`.tree-more[data-parent="${CSS.escape(path)}"]`)?.focus(); return; }
  const appended = (state.treeEntries.get(path) || [])[before];
  if (appended) focusTreePath(appended.path);
  else document.querySelector(`.tree-more[data-parent="${CSS.escape(path)}"]`)?.focus();
}

async function expandAncestors(path) {
  const parts = path.split("/").slice(0, -1);
  let parent = "";
  for (const part of parts) {
    const target = parent ? `${parent}/${part}` : part;
    if (!state.treeEntries.has(parent)) await loadTreePage(parent);
    while (!(state.treeEntries.get(parent) || []).some(item => item.path === target) && state.treeCursors.get(parent)) {
      await loadTreePage(parent, state.treeCursors.get(parent), true);
    }
    state.openDirectories.add(target);
    if (!state.treeEntries.has(target)) await loadTreePage(target);
    parent = target;
  }
  renderCurrentTree();
}

function renderCurrentTree() {
  renderTree(fileTree, state.treeEntries, state.treeCursors, state.treePartials, state.openDirectories, state.selectedPath, toggleDirectory, openDocument, loadMoreTree);
}

function focusTreePath(path) {
  const rows = [...fileTree.querySelectorAll('[role="treeitem"]')];
  const target = rows.find(node => node.dataset.path === path);
  if (!target) return;
  rows.forEach(node => { node.tabIndex = node === target ? 0 : -1; });
  target.focus();
}

async function loadView(cursor = null) {
  if (!state.source) return;
  activateTab(); showLoading();
  if (state.view === "overview" && state.commit) { await loadCommit(); return; }
  const identity = {source: state.source.id, tab: state.view, cursor};
  const request = beginRequest("view", identity);
  try {
    if (state.view === "overview") {
      const value = await get("/api/v1/overview", {source: identity.source, cursor}, request.signal);
      if (isCurrent(request)) { state.repository = value.repository; renderOverview(content, value, loadMoreCommits, openCommit); renderSourceContext(contextContent, state.source, state.sourceSettings, state.repository); }
    } else if (state.view === "skills" || state.view === "memory") {
      const value = await get("/api/v1/collection", {source: identity.source, kind: identity.tab, cursor}, request.signal);
      if (isCurrent(request)) renderCollection(content, value, identity.tab, openCollectionDocument, loadMoreCollection, state.collapsedGroups);
    } else {
      const value = await get("/api/v1/settings", {source: identity.source}, request.signal);
      if (isCurrent(request)) renderSettings(content, value, state.themeChoice, applyThemeChoice);
    }
  } catch (error) {
    if (error.name !== "AbortError" && isCurrent(request)) showError(error);
  } finally { completeRequest(request); }
}

async function loadMoreCommits(cursor, list, button) {
  const identity = {source: state.source.id, tab: "overview", cursor};
  const request = beginRequest("overview-more", identity); button.disabled = true;
  try {
    const value = await get("/api/v1/overview", {source: identity.source, cursor}, request.signal);
    if (!isCurrent(request)) return;
    const appended = value.commits.items.map(item => appendCommit(list, item, openCommit));
    refreshCommitAbbreviations(list); button.remove();
    if (value.commits.next_cursor) { const next = moreButton("Load more commits", () => loadMoreCommits(value.commits.next_cursor, list, next)); list.after(next); }
    appended[0]?.focus?.();
  } catch (error) { if (error.name !== "AbortError" && isCurrent(request)) { button.disabled = false; showError(error, true); } }
  finally { completeRequest(request); }
}

async function loadMoreCollection(cursor, list, button) {
  const identity = {source: state.source.id, tab: state.view, cursor};
  const request = beginRequest("collection-more", identity); button.disabled = true;
  try {
    const value = await get("/api/v1/collection", {source: identity.source, kind: identity.tab, cursor}, request.signal);
    if (!isCurrent(request)) return;
    button.remove();
    const appended = value.items.map(item => appendItem(list, item, openCollectionDocument, state.collapsedGroups));
    if (value.next_cursor) { const next = moreButton("Load more", () => loadMoreCollection(value.next_cursor, list, next)); list.append(next); }
    if (value.partial) appendPartialNote(list);
    // An item appended into a collapsed section cannot take focus; its heading
    // can, and the heading's count is where the arrival is visible.
    const landing = appended[0];
    (landing?.offsetParent ? landing : landing?.closest(".collection-section")?.querySelector(".collection-group"))?.focus();
  } catch (error) { if (error.name !== "AbortError" && isCurrent(request)) { button.disabled = false; showError(error, true); } }
  finally { completeRequest(request); }
}

// Reference resolution runs after the document is on screen. It is a
// whole-source question, so making the reader wait for it would put a
// source-sized cost in front of every document they open.
async function resolveReferences(frontmatter, path) {
  const ids = referencedIds(frontmatter);
  if (!ids.length) return;
  const request = beginRequest("references", {source: state.source.id, tab: state.view, path});
  let resolved = {};
  let partial = false;
  try {
    const value = await get("/api/v1/references", {source: state.source.id, ids: ids.join(",")}, request.signal);
    resolved = value.resolved;
    partial = Boolean(value.partial);
  } catch (error) {
    // Timed out or refused: the chips settle inert rather than sitting in a
    // pending state no later event will ever clear.
    resolved = {};
  } finally {
    // A superseded request must not settle the chips a newer one is already
    // resolving, or a re-render mid-flight leaves them permanently unresolved.
    const superseded = request.signal.aborted;
    completeRequest(request);
    if (!superseded) applyReferenceResolution(contextContent, resolved, path, partial);
  }
}

function openReference(path) {
  const opener = state.documentSurface === "collection" ? openCollectionDocument : openDocument;
  opener(path, "rendered");
}

function revealCollectionItem(path) {
  const item = content.querySelector(`.collection-item[data-path="${CSS.escape(path)}"]`);
  const section = item?.closest(".collection-section");
  if (!section || !section.classList.contains("collapsed")) return;
  // Opening an item inside a folded group must show it, rather than leave the
  // reader with a document whose place in the list they cannot see.
  section.classList.remove("collapsed");
  const heading = section.querySelector(".collection-group");
  heading.setAttribute("aria-expanded", "true");
  heading.querySelector(".chevron").textContent = "⌄";
  state.collapsedGroups.delete(section.dataset.group);
}

async function openCommit(sha) {
  abortAllRequests(); clearTimeout(searchTimer);
  state.commit = sha; state.selectedPath = null; state.documentSurface = null; state.commitFiles = [];
  updateRoute(); showLoading();
  await loadCommit();
}

async function closeCommit() {
  abortAllRequests();
  state.commit = null; state.selectedPath = null; state.documentSurface = null; state.commitFiles = [];
  updateRoute();
  await loadView();
}

async function loadCommit() {
  const identity = {source: state.source.id, tab: "overview", commit: state.commit};
  const request = beginRequest("commit", identity);
  try {
    const detail = await get("/api/v1/commit", {source: identity.source, sha: state.commit}, request.signal);
    if (!isCurrent(request)) return;
    state.commitFiles = detail.files;
    renderCommit(content, detail, openCommitFile, closeCommit);
  } catch (error) {
    if (error.name !== "AbortError" && isCurrent(request)) showError(error);
  } finally { completeRequest(request); }
}

async function openCommitFile(path, pushRoute = true) {
  state.selectedPath = path;
  state.documentSurface = null;
  // Selection belongs to opening the file, not to the click that happened to
  // cause it: a restored deep link opened the file with nothing marked.
  content.querySelectorAll(".split-view .collection-item").forEach(item => {
    item.classList.toggle("active", item.dataset.path === path);
  });
  const reader = content.querySelector(".reader");
  if (reader) showLoading(reader);
  const identity = {source: state.source.id, tab: "overview", commit: state.commit, path};
  const request = beginRequest("commit-file", identity);
  try {
    const value = await get("/api/v1/commit-file", {source: identity.source, sha: state.commit, path}, request.signal);
    if (!isCurrent(request)) return;
    const known = state.commitFiles.find(item => item.path === path);
    renderCommitDocument(content, value, known ? known.change : null);
    if (pushRoute) updateRoute();
  } catch (error) {
    if (error.name !== "AbortError" && isCurrent(request)) showDocumentError(error, true);
  } finally { completeRequest(request); }
}

async function openCollectionDocument(path, mode = "rendered", pushRoute = true) {
  content.querySelectorAll(".collection-item").forEach(item => {
    item.classList.toggle("active", item.dataset.path === path);
  });
  revealCollectionItem(path);
  const reader = content.querySelector(".reader");
  if (reader) showLoading(reader);
  await fetchDocument(path, mode, "collection", pushRoute);
}

async function openDocument(path, mode = "rendered", pushRoute = true) {
  abortAllRequests(); state.commit = null; state.commitFiles = [];
  state.selectedPath = path; state.documentMode = mode; state.documentSurface = "standalone"; renderCurrentTree(); showLoading();
  await fetchDocument(path, mode, "standalone", pushRoute);
}

async function fetchDocument(path, mode, surface, pushRoute) {
  const embedded = surface === "collection";
  if (state.selectedPath !== path || state.documentMode !== mode || state.documentSurface !== surface) {
    abortAllRequests(); state.selectedPath = path; state.documentMode = mode; state.documentSurface = surface;
  }
  const identity = {source: state.source.id, tab: state.view, path, mode, surface};
  const request = beginRequest("document", identity);
  try {
    const value = await get("/api/v1/document", {source: identity.source, path, mode}, request.signal);
    if (!isCurrent(request)) return;
    state.selectedPath = path; state.documentMode = value.mode; state.documentSurface = surface;
    renderDocument(content, value, nextMode => fetchDocument(path, nextMode, surface, true), embedded);
    renderDocumentContext(contextContent, state.source, value, openReference); renderCurrentTree();
    resolveReferences(value.frontmatter, value.path);
    if (pushRoute) updateRoute();
  } catch (error) {
    if (error.name !== "AbortError" && isCurrent(request)) showDocumentError(error, embedded);
  } finally { completeRequest(request); }
}

async function search(query, cursor = null, append = false) {
  if (!append) {
    abortAllRequests(); state.selectedPath = null; state.documentSurface = null; state.commit = null; state.commitFiles = [];
    state.search = {query, items: [], cursor: null, partial: false};
  }
  const identity = {source: state.source.id, tab: state.view, query, cursor};
  const request = beginRequest("search", identity);
  if (!append) showLoading();
  try {
    const page = await get("/api/v1/search", {source: identity.source, q: query, cursor}, request.signal);
    if (!isCurrent(request)) return;
    const previous = append ? state.search.items : [];
    const known = new Set(previous.map(item => item.path));
    state.search = {query, items: [...previous, ...page.items.filter(item => !known.has(item.path))], cursor: page.next_cursor, partial: page.partial};
    const combined = {items: state.search.items, next_cursor: page.next_cursor, partial: page.partial};
    renderSearchResults(content, combined, openDocument, loadMoreSearch);
  } catch (error) {
    if (error.name !== "AbortError" && isCurrent(request)) showError(error);
  } finally { completeRequest(request); }
}

async function loadMoreSearch(cursor, section, button) {
  button.disabled = true; const before = state.search.items.length;
  await search(state.search.query, cursor, true);
  const rows = content.querySelectorAll(".collection-item"); rows[before]?.focus();
}

function clearSearch() { abortAllRequests(); state.search = {query: "", items: [], cursor: null, partial: false}; loadView(); }

function activateTab() {
  tabs.forEach(button => {
    const active = button.dataset.view === state.view;
    button.classList.toggle("active", active); button.setAttribute("aria-selected", active ? "true" : "false"); button.tabIndex = active ? 0 : -1;
  });
  content.setAttribute("aria-labelledby", `tab-${state.view}`);
}

function showLoading(target = content) { target.innerHTML = '<div class="skeleton"></div><div class="skeleton"></div><div class="skeleton"></div>'; }
function showNotice(message) { notice.hidden = false; notice.className = "notice"; notice.setAttribute("role", "status"); notice.textContent = message; }
function showError(error, preserveContent = false) {
  notice.hidden = false; notice.className = "notice error"; notice.setAttribute("role", "alert");
  const expired = ["capability_required", "capability_invalid"].includes(error?.code);
  notice.textContent = expired ? "Explorer session expired. Reopen it using a newly printed launch URL; your current location is preserved." : `${error.code ? `${error.code}: ` : ""}${safeMessage(error)}`;
  if (!preserveContent && !expired) setEmpty(content, "This view could not be loaded. The rest of the source remains available.");
}
function showDocumentError(error, embedded) { const target = embedded ? content.querySelector(".reader") : content; if (target) setEmpty(target, safeMessage(error)); showError(error, true); }
function setTreeError(error) { fileTree.replaceChildren(); const node = document.createElement("div"); node.className = "tree-empty"; node.textContent = safeMessage(error); fileTree.append(node); }
function setEmpty(target, message) { target.replaceChildren(); const node = document.createElement("div"); node.className = "empty"; node.textContent = message; target.append(node); }
function safeMessage(error) { return String(error?.message || "Explorer could not complete the request."); }

async function loadSourceContext() {
  const identity = {source: state.source.id, tab: state.view};
  const request = beginRequest("context", identity);
  try {
    const settings = await get("/api/v1/settings", {source: identity.source}, request.signal);
    if (!isCurrent(request)) return;
    state.sourceSettings = settings; renderSourceContext(contextContent, state.source, settings, state.repository);
  } catch (error) { if (error.name !== "AbortError" && isCurrent(request)) renderSourceContext(contextContent, state.source, null); }
  finally { completeRequest(request); }
}

function applyThemeChoice(choice) {
  applyTheme(state, content, choice);
}
function cycleTheme() { cycleThemeChoice(state, content); }

function updateRoute(replace = false) {
  writeRoute(state, replace);
}

async function restoreRoute() {
  if (!state.estate) return;
  abortAllRequests(); clearTimeout(searchTimer);
  const route = routeFromHash(); const source = state.estate.sources.find(item => item.id === route.source) || state.estate.sources[0];
  state.view = validView(route.tab); state.documentMode = route.mode === "raw" ? "raw" : "rendered";
  const sourceChanged = source.id !== state.source?.id;
  const previousCommit = state.commit;
  state.commit = route.commit || null;
  if (sourceChanged) await selectSource(source, false);
  state.selectedPath = route.path || null;
  state.documentSurface = route.path && !state.commit ? restoredSurface(route) : null;
  state.search = {query: "", items: [], cursor: null, partial: false}; activateTab();
  if (state.commit) {
    if (sourceChanged || state.commit !== previousCommit || !content.querySelector(".split-view")) await loadCommit();
    if (route.path) await openCommitFile(route.path, false);
    return;
  }
  if (route.path) await restoreDocumentRoute(route.path, state.documentMode, state.documentSurface, sourceChanged);
  else { state.selectedPath = null; state.documentSurface = null; await loadView(); }
}

async function restoreDocumentRoute(path, mode, surface, collectionLoaded = false) {
  await expandAncestors(path);
  if (surface === "collection") {
    if (!collectionLoaded) await loadView();
    await openCollectionDocument(path, mode, false);
    return;
  }
  await openDocument(path, mode, false);
}

function restoredSurface(route) {
  return validDocumentSurface(route.surface) || (["skills", "memory"].includes(validView(route.tab)) ? "collection" : "standalone");
}

function showIdleExpired(timeoutSeconds) {
  abortAllRequests();
  stopActivityLease?.();
  notice.hidden = false; notice.className = "notice error"; notice.setAttribute("role", "alert");
  const minutes = Math.max(1, Math.round(timeoutSeconds / 60));
  notice.textContent = `Explorer stopped after ${minutes} minutes of inactivity. Ask Claude Code to open it again.`;
}

function moreButton(label, action) { const button = document.createElement("button"); button.className = "load-more"; button.textContent = label; button.addEventListener("click", action); return button; }
function appendPartialNote(target) { const note = document.createElement("p"); note.className = "partial-note"; note.textContent = "This collection is partial because the source reached its scan limit."; target.append(note); }

initialise();
