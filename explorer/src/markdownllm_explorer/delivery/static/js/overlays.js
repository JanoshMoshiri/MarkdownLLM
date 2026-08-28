import {syncRegionState} from "./layout.js";

export function openOverlay(kind) {
  closeOverlays(false);
  const navigation = kind === "nav";
  document.body.classList.add(navigation ? "nav-open" : "context-open");
  const panel = document.querySelector(navigation ? ".sidebar" : ".context-panel");
  panel.setAttribute("role", "dialog");
  panel.setAttribute("aria-modal", "true");
  [...document.querySelector(".shell").children]
    .filter(node => node !== panel)
    .forEach(node => { node.inert = true; node.setAttribute("aria-hidden", "true"); });
  syncRegionState();
  visibleFocusable(panel)[0]?.focus();
}

export function closeOverlays(returnFocus = true) {
  const navigationWasOpen = document.body.classList.contains("nav-open");
  const contextWasOpen = document.body.classList.contains("context-open");
  document.body.classList.remove("nav-open", "context-open");
  document.querySelectorAll(".sidebar,.context-panel").forEach(panel => {
    panel.removeAttribute("role");
    panel.removeAttribute("aria-modal");
  });
  [...document.querySelector(".shell").children].forEach(node => {
    node.inert = false;
    node.removeAttribute("aria-hidden");
  });
  syncRegionState();
  if (returnFocus && navigationWasOpen) document.querySelector("#sidebar-open").focus();
  else if (returnFocus && contextWasOpen) document.querySelector("#context-open").focus();
}

export function activeOverlay() {
  if (document.body.classList.contains("nav-open")) return document.querySelector(".sidebar");
  if (document.body.classList.contains("context-open")) return document.querySelector(".context-panel");
  return null;
}

export function visibleFocusable(panel) {
  return [...panel.querySelectorAll('button:not([disabled]), input:not([disabled]), select:not([disabled]), a[href], [tabindex]:not([tabindex="-1"])')]
    .filter(node => node.offsetParent !== null);
}
