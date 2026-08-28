import {captureCapability, get} from "./api.js";
import {abortAllRequests, beginRequest, completeRequest, isCurrent, state} from "./state.js";
import {routeFromHash, routeFromText, validView, writeRoute} from "./routing.js";
import {applyThemeChoice as applyTheme, cycleThemeChoice} from "./theme.js";
import {activeOverlay, closeOverlays, openOverlay, visibleFocusable} from "./overlays.js";
import {initialiseLayout} from "./layout.js";
import {renderSources, renderTree} from "./views/navigation.js";
import {appendCommit, refreshCommitAbbreviations, renderOverview} from "./views/overview.js";
import {appendItem, renderCollection} from "./views/collection.js";
import {renderDocument} from "./views/document.js";
import {renderSettings} from "./views/settings.js";
import {appendSearchResult, renderSearchResults} from "./views/tree.js";
import {renderDocumentContext, renderSourceContext} from "./views/context.js";

const content = document.querySelector("#content");
const notice = document.querySelector("#notice");
const sourceNav = document.querySelector("#source-nav");
const fileTree = document.querySelector("#file-tree");
const contextContent = document.querySelector("#context-content");
const tabs = [...document.querySelectorAll('[role="tab"]')];
let searchTimer;

async function initialise() {
  applyThemeChoice(localStorage.getItem("mdllm-explorer-theme") || "system");
  bindChrome();
  if (!captureCapability()) {
    showError({message: "Open Explorer using the launch URL printed by mdllm-explorer.", code: "capability_required"});
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
    await selectSource(requested || estate.sources[0], false);
    if (routed.path) await restoreDocumentRoute(routed.path, state.documentMode, true);
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
  initialiseLayout(openOverlay);
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
      const opener = state.view === "skills" || state.view === "memory" ? openCollectionDocument : openDocument;
      opener(route.path, "rendered");
    }
  });
  window.addEventListener("popstate", restoreRoute);
  matchMedia("(prefers-color-scheme: light)").addEventListener?.("change", () => { if (state.themeChoice === "system") applyThemeChoice("system"); });
}

async function chooseTab(view) {
  abortAllRequests(); clearTimeout(searchTimer);
  state.view = validView(view); state.selectedPath = null;
  state.search = {query: "", items: [], cursor: null, partial: false};
  document.querySelector("#search-input").value = "";
  renderSourceContext(contextContent, state.source, state.sourceSettings, state.repository);
  activateTab(); updateRoute(); await loadView();
}

async function selectSource(source, pushRoute = true) {
  if (!source) throw new Error("No discoverable source is available.");
  abortAllRequests();
  clearTimeout(searchTimer);
  state.source = source; state.selectedPath = null; state.sourceSettings = null; state.repository = null;
  state.treeEntries.clear(); state.treeCursors.clear(); state.treePartials.clear(); state.openDirectories = new Set([""]);
  state.search = {query: "", items: [], cursor: null, partial: false};
  document.querySelector("#search-input").value = "";
  document.querySelector("#source-name").textContent = source.display_name;
  document.querySelector("#source-kind").textContent = source.kind === "substrate" ? "Framework source" : "Domain source";
  document.querySelector("#source-icon").textContent = source.display_name.slice(0, 1).toUpperCase();
  renderSources(sourceNav, state.estate, source.id, selectSource);
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
  const identity = {source: state.source.id, tab: state.view, cursor};
  const request = beginRequest("view", identity);
  try {
    if (state.view === "overview") {
      const value = await get("/api/v1/overview", {source: identity.source, cursor}, request.signal);
      if (isCurrent(request)) { state.repository = value.repository; renderOverview(content, value, loadMoreCommits); renderSourceContext(contextContent, state.source, state.sourceSettings, state.repository); }
    } else if (state.view === "skills" || state.view === "memory") {
      const value = await get("/api/v1/collection", {source: identity.source, kind: identity.tab, cursor}, request.signal);
      if (isCurrent(request)) renderCollection(content, value, identity.tab, openCollectionDocument, loadMoreCollection);
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
    const appended = value.commits.items.map(item => appendCommit(list, item));
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
    button.remove(); const appended = [];
    let group = [...list.querySelectorAll(".collection-group")].at(-1)?.textContent || "";
    value.items.forEach(item => {
      if (item.group !== group) {
        group = item.group; const heading = document.createElement("div");
        heading.className = "collection-group"; heading.textContent = group; list.append(heading);
      }
      appended.push(appendItem(list, item, openCollectionDocument));
    });
    if (value.next_cursor) { const next = moreButton("Load more", () => loadMoreCollection(value.next_cursor, list, next)); list.append(next); }
    if (value.partial) appendPartialNote(list);
    appended[0]?.focus();
  } catch (error) { if (error.name !== "AbortError" && isCurrent(request)) { button.disabled = false; showError(error, true); } }
  finally { completeRequest(request); }
}

async function openCollectionDocument(path, mode = "rendered", pushRoute = true) {
  content.querySelectorAll(".collection-item").forEach(item => {
    item.classList.toggle("active", item.dataset.path === path);
  });
  const reader = content.querySelector(".reader");
  if (reader) showLoading(reader);
  await fetchDocument(path, mode, true, pushRoute);
}

async function openDocument(path, mode = "rendered", pushRoute = true) {
  abortAllRequests(); state.selectedPath = path; state.documentMode = mode; renderCurrentTree(); showLoading();
  await fetchDocument(path, mode, false, pushRoute);
}

async function fetchDocument(path, mode, embedded, pushRoute) {
  if (state.selectedPath !== path || state.documentMode !== mode) {
    abortAllRequests(); state.selectedPath = path; state.documentMode = mode;
  }
  const identity = {source: state.source.id, tab: state.view, path, mode};
  const request = beginRequest("document", identity);
  try {
    const value = await get("/api/v1/document", {source: identity.source, path, mode}, request.signal);
    if (!isCurrent(request)) return;
    state.selectedPath = path; state.documentMode = value.mode;
    renderDocument(content, value, nextMode => fetchDocument(path, nextMode, embedded, true), embedded);
    renderDocumentContext(contextContent, state.source, value); renderCurrentTree();
    if (pushRoute) updateRoute();
  } catch (error) {
    if (error.name !== "AbortError" && isCurrent(request)) showDocumentError(error, embedded);
  } finally { completeRequest(request); }
}

async function search(query, cursor = null, append = false) {
  if (!append) {
    abortAllRequests(); state.selectedPath = null;
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
  if (sourceChanged) await selectSource(source, false);
  state.selectedPath = route.path || null; state.search = {query: "", items: [], cursor: null, partial: false}; activateTab();
  if (route.path) await restoreDocumentRoute(route.path, state.documentMode, sourceChanged);
  else { state.selectedPath = null; await loadView(); }
}

async function restoreDocumentRoute(path, mode, collectionLoaded = false) {
  await expandAncestors(path);
  if (state.view === "skills" || state.view === "memory") {
    if (!collectionLoaded) await loadView();
    await openCollectionDocument(path, mode, false);
    return;
  }
  await openDocument(path, mode, false);
}

function moreButton(label, action) { const button = document.createElement("button"); button.className = "load-more"; button.textContent = label; button.addEventListener("click", action); return button; }
function appendPartialNote(target) { const note = document.createElement("p"); note.className = "partial-note"; note.textContent = "This collection is partial because the source reached its scan limit."; target.append(note); }

initialise();
