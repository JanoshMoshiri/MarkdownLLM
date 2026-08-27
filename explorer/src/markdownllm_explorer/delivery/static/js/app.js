import {captureCapability, get} from "./api.js";
import {beginRequest, isCurrent, state} from "./state.js";
import {renderSources, renderTree} from "./views/navigation.js";
import {appendCommit, refreshCommitAbbreviations, renderOverview} from "./views/overview.js";
import {appendItem, renderCollection} from "./views/collection.js";
import {renderDocument} from "./views/document.js";
import {renderSettings} from "./views/settings.js";
import {renderSearchResults} from "./views/tree.js";
import {renderDocumentContext, renderSourceContext} from "./views/context.js";

const content = document.querySelector("#content");
const notice = document.querySelector("#notice");
const sourceNav = document.querySelector("#source-nav");
const fileTree = document.querySelector("#file-tree");
const contextContent = document.querySelector("#context-content");
const tabs = [...document.querySelectorAll(".tabs button")];

async function initialise() {
  applyThemeChoice(localStorage.getItem("mdllm-explorer-theme") || "system");
  bindChrome();
  if (!captureCapability()) {
    showError({message: "Open Explorer using the launch URL printed by mdllm-explorer.", code: "capability_required"});
    return;
  }
  showLoading();
  try {
    state.estate = await get("/api/v1/estate");
    if (state.estate.issues.length) showNotice(`${state.estate.issues.length} estate discovery issue${state.estate.issues.length === 1 ? "" : "s"} reported.`);
    const routed = routeFromHash();
    const requested = routed.source && state.estate.sources.find(item => item.id === routed.source);
    state.view = ["overview", "skills", "memory", "settings"].includes(routed.tab) ? routed.tab : "overview";
    state.documentMode = routed.mode === "raw" ? "raw" : "rendered";
    await selectSource(requested || state.estate.sources[0], false);
    if (routed.path) { await expandAncestors(routed.path); await openDocument(routed.path, state.documentMode, false); }
    else updateRoute(true);
  } catch (error) { showError(error); }
}

function bindChrome() {
  tabs.forEach(button => button.addEventListener("click", () => { state.view = button.dataset.view; state.selectedPath = null; activateTab(); updateRoute(); loadView(); }));
  document.querySelector("#tree-refresh").addEventListener("click", () => loadRootTree(true));
  document.querySelector("#theme-toggle").addEventListener("click", () => cycleTheme());
  document.querySelector("#sidebar-open").addEventListener("click", () => openOverlay("nav"));
  document.querySelector("#sidebar-close").addEventListener("click", () => closeOverlays());
  document.querySelector("#context-open").addEventListener("click", () => openOverlay("context"));
  document.querySelector("#context-close").addEventListener("click", () => closeOverlays());
  let timer;
  document.querySelector("#search-input").addEventListener("input", event => {
    clearTimeout(timer); const query = event.target.value.trim();
    timer = setTimeout(() => query ? search(query) : loadView(), 220);
  });
  document.addEventListener("keydown", event => {
    if (event.key === "Escape") closeOverlays();
    if (event.key !== "Tab") return;
    const panel = document.body.classList.contains("nav-open") ? document.querySelector(".sidebar") : document.body.classList.contains("context-open") ? document.querySelector(".context-panel") : null;
    if (!panel) return;
    const focusable = [...panel.querySelectorAll('button:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])')].filter(node => node.offsetParent !== null);
    if (!focusable.length) return;
    const first = focusable[0], last = focusable.at(-1);
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  });
  document.addEventListener("click", event => {
    const anchor = event.target.closest?.('a[href^="#source="]');
    if (!anchor) return;
    event.preventDefault(); const route = routeFromText(anchor.getAttribute("href"));
    if (route.path) openDocument(route.path, "rendered");
  });
  window.addEventListener("popstate", () => restoreRoute());
  matchMedia("(prefers-color-scheme: light)").addEventListener?.("change", () => { if (state.themeChoice === "system") applyThemeChoice("system"); });
}

async function selectSource(source, pushRoute = true) {
  if (!source) throw new Error("No discoverable source is available.");
  state.source = source; state.selectedPath = null; state.sourceSettings = null; state.repository = null; state.treeEntries.clear(); state.openDirectories = new Set([""]);
  document.querySelector("#source-name").textContent = source.display_name;
  document.querySelector("#source-kind").textContent = source.kind === "substrate" ? "Framework source" : "Domain source";
  document.querySelector("#source-icon").textContent = source.display_name.slice(0, 1).toUpperCase();
  renderSources(sourceNav, state.estate, source.id, selectSource);
  document.body.classList.remove("nav-open");
  if (pushRoute) updateRoute();
  await Promise.all([loadRootTree(), loadView(), loadSourceContext()]);
}

async function loadRootTree(force = false) {
  if (!state.source) return;
  const sourceId = state.source.id;
  if (!force && state.treeEntries.has("")) return renderCurrentTree();
  try {
    const page = await get("/api/v1/tree", {source: sourceId});
    if (state.source?.id !== sourceId) return;
    state.treeEntries.set("", page.items); renderCurrentTree();
  } catch (error) { fileTree.innerHTML = `<div class="tree-empty">${safeMessage(error)}</div>`; }
}

async function toggleDirectory(path) {
  const sourceId = state.source.id;
  if (state.openDirectories.has(path)) { state.openDirectories.delete(path); renderCurrentTree(); return; }
  state.openDirectories.add(path); renderCurrentTree();
  if (!state.treeEntries.has(path)) {
    try { const page = await get("/api/v1/tree", {source: sourceId, path}); if (state.source?.id !== sourceId) return; state.treeEntries.set(path, page.items); }
    catch (error) { showError(error); state.treeEntries.set(path, []); }
  }
  renderCurrentTree();
}

async function expandAncestors(path) {
  const parts = path.split("/").slice(0, -1);
  let current = "";
  for (const part of parts) {
    current = current ? `${current}/${part}` : part;
    state.openDirectories.add(current);
    if (!state.treeEntries.has(current)) {
      try { const page = await get("/api/v1/tree", {source: state.source.id, path: current}); state.treeEntries.set(current, page.items); }
      catch { state.treeEntries.set(current, []); break; }
    }
  }
  renderCurrentTree();
}

function renderCurrentTree() {
  renderTree(fileTree, state.treeEntries, state.openDirectories, state.selectedPath, toggleDirectory, openDocument);
}

async function loadView(cursor = null) {
  if (!state.source) return;
  activateTab(); showLoading();
  const request = beginRequest();
  try {
    if (state.view === "overview") {
      const value = await get("/api/v1/overview", {source: state.source.id, cursor}, request.signal);
      if (isCurrent(request.id)) { state.repository = value.repository; renderOverview(content, value, loadMoreCommits); renderSourceContext(contextContent, state.source, state.sourceSettings, state.repository); }
    } else if (state.view === "skills" || state.view === "memory") {
      const value = await get("/api/v1/collection", {source: state.source.id, kind: state.view, cursor}, request.signal);
      if (isCurrent(request.id)) renderCollection(content, value, state.view, path => openCollectionDocument(path), loadMoreCollection);
    } else {
      const value = await get("/api/v1/settings", {source: state.source.id}, request.signal);
      if (isCurrent(request.id)) renderSettings(content, value, state.themeChoice, applyThemeChoice);
    }
  } catch (error) { if (error.name !== "AbortError" && isCurrent(request.id)) showError(error); }
}

async function loadMoreCommits(cursor, list, button) {
  button.disabled = true;
  try {
    const value = await get("/api/v1/overview", {source: state.source.id, cursor});
    value.commits.items.forEach(item => appendCommit(list, item));
    refreshCommitAbbreviations(list);
    button.remove();
    if (value.commits.next_cursor) { const next = document.createElement("button"); next.className = "load-more"; next.textContent = "Load more commits"; next.addEventListener("click", () => loadMoreCommits(value.commits.next_cursor, list, next)); list.after(next); }
  } catch (error) { button.disabled = false; showError(error); }
}

async function loadMoreCollection(cursor, list, button) {
  button.disabled = true;
  try {
    const value = await get("/api/v1/collection", {source: state.source.id, kind: state.view, cursor});
    value.items.forEach(item => appendItem(list, item, path => openCollectionDocument(path)));
    button.remove();
  } catch (error) { button.disabled = false; showError(error); }
}

async function openCollectionDocument(path, mode = "rendered") {
  const sourceId = state.source.id;
  const reader = content.querySelector(".reader");
  if (reader) reader.innerHTML = '<div class="reader-body"><div class="skeleton"></div><div class="skeleton"></div></div>';
  try {
    const value = await get("/api/v1/document", {source: sourceId, path, mode});
    if (state.source?.id !== sourceId) return;
    renderDocument(content, value, nextMode => openCollectionDocument(path, nextMode), true);
    state.selectedPath = path; state.documentMode = value.mode; updateRoute(); renderDocumentContext(contextContent, state.source, value);
  } catch (error) { if (reader) reader.innerHTML = `<div class="empty">${safeMessage(error)}</div>`; else showError(error); }
}

async function openDocument(path, mode = "rendered", pushRoute = true) {
  state.selectedPath = path; state.documentMode = mode; renderCurrentTree(); showLoading();
  const request = beginRequest();
  try {
    const value = await get("/api/v1/document", {source: state.source.id, path, mode}, request.signal);
    if (isCurrent(request.id)) {
      state.documentMode = value.mode;
      renderDocument(content, value, nextMode => openDocument(path, nextMode));
      renderDocumentContext(contextContent, state.source, value);
      if (pushRoute) updateRoute();
    }
  } catch (error) { if (error.name !== "AbortError" && isCurrent(request.id)) showError(error); }
}

async function search(query) {
  showLoading(); const request = beginRequest();
  try {
    const page = await get("/api/v1/search", {source: state.source.id, q: query}, request.signal);
    if (isCurrent(request.id)) renderSearchResults(content, page, openDocument);
  } catch (error) { if (error.name !== "AbortError" && isCurrent(request.id)) showError(error); }
}

function activateTab() { tabs.forEach(button => button.classList.toggle("active", button.dataset.view === state.view)); }
function showLoading() { content.innerHTML = '<div class="skeleton"></div><div class="skeleton"></div><div class="skeleton"></div>'; }
function showNotice(message) { notice.hidden = false; notice.className = "notice"; notice.textContent = message; }
function showError(error) { notice.hidden = false; notice.className = "notice error"; notice.textContent = `${error.code ? `${error.code}: ` : ""}${safeMessage(error)}`; content.innerHTML = '<div class="empty">This view could not be loaded. The rest of the source remains available.</div>'; }
function safeMessage(error) { return String(error?.message || "Explorer could not complete the request."); }

async function loadSourceContext() {
  const source = state.source;
  try { const settings = await get("/api/v1/settings", {source: source.id}); if (state.source?.id !== source.id) return; state.sourceSettings = settings; renderSourceContext(contextContent, source, settings, state.repository); }
  catch { renderSourceContext(contextContent, state.source, null); }
}

function applyThemeChoice(choice) {
  state.themeChoice = ["system", "light", "dark"].includes(choice) ? choice : "system";
  const actual = state.themeChoice === "system" ? (matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark") : state.themeChoice;
  document.documentElement.dataset.theme = actual;
  document.documentElement.dataset.themeChoice = state.themeChoice;
  localStorage.setItem("mdllm-explorer-theme", state.themeChoice);
  const button = document.querySelector("#theme-toggle");
  button.textContent = state.themeChoice === "system" ? "◐" : actual === "dark" ? "☀" : "☾";
  button.setAttribute("aria-label", `Colour theme: ${state.themeChoice}. Activate to change.`);
  const settingsSelect = content.querySelector('select[aria-label="Colour theme"]'); if (settingsSelect) settingsSelect.value = state.themeChoice;
}

function cycleTheme() {
  const choices = ["system", "light", "dark"];
  applyThemeChoice(choices[(choices.indexOf(state.themeChoice) + 1) % choices.length]);
}

function updateRoute(replace = false) {
  if (!state.source) return;
  const params = new URLSearchParams({source: state.source.id, tab: state.view, mode: state.documentMode});
  if (state.selectedPath) params.set("path", state.selectedPath);
  history[replace ? "replaceState" : "pushState"](null, "", `#${params}`);
}

function routeFromHash() { return routeFromText(location.hash); }
function routeFromText(text) {
  const params = new URLSearchParams(String(text || "").replace(/^#/, ""));
  return {source: params.get("source"), tab: params.get("tab"), mode: params.get("mode"), path: params.get("path")};
}

async function restoreRoute() {
  if (!state.estate) return;
  const route = routeFromHash();
  const source = state.estate.sources.find(item => item.id === route.source) || state.estate.sources[0];
  if (source.id !== state.source?.id) await selectSource(source, false);
  state.view = ["overview", "skills", "memory", "settings"].includes(route.tab) ? route.tab : "overview";
  state.documentMode = route.mode === "raw" ? "raw" : "rendered";
  activateTab();
  if (route.path) { await expandAncestors(route.path); await openDocument(route.path, state.documentMode, false); }
  else { state.selectedPath = null; await loadView(); }
}

function openOverlay(kind) {
  closeOverlays(false);
  document.body.classList.add(kind === "nav" ? "nav-open" : "context-open");
  const panel = document.querySelector(kind === "nav" ? ".sidebar" : ".context-panel");
  panel.querySelector("button, input, [tabindex]")?.focus();
}

function closeOverlays(returnFocus = true) {
  const navWasOpen = document.body.classList.contains("nav-open");
  const contextWasOpen = document.body.classList.contains("context-open");
  document.body.classList.remove("nav-open", "context-open");
  if (returnFocus && navWasOpen) document.querySelector("#sidebar-open").focus();
  else if (returnFocus && contextWasOpen) document.querySelector("#context-open").focus();
}

initialise();
