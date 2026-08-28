// Desktop region collapse.
//
// This is a different mechanism from the narrow-viewport overlay in
// overlays.js, and the two must not be conflated.  An overlay covers the
// workspace, so it is a real dialog: modal state, inert siblings, a focus
// trap and Escape to dismiss.  A collapsed region at desktop covers nothing —
// it yields its grid track back to the centre — so it takes none of that.
// Applying dialog semantics here would trap focus in a dialog the reader
// cannot see and did not open.

const DESKTOP = "(min-width: 900px)";

const REGIONS = {
  nav: {
    className: "nav-collapsed",
    storageKey: "mdllm-explorer-nav-collapsed",
    collapse: "#sidebar-collapse",
    open: "#sidebar-open",
  },
  context: {
    className: "context-collapsed",
    storageKey: "mdllm-explorer-context-collapsed",
    collapse: "#context-collapse",
    open: "#context-open",
  },
};

function atDesktop() {
  return matchMedia(DESKTOP).matches;
}

function stored(key) {
  try {
    return localStorage.getItem(key) === "true";
  } catch {
    // Storage can be unavailable; the region simply starts expanded.
    return false;
  }
}

function remember(key, value) {
  try {
    localStorage.setItem(key, value ? "true" : "false");
  } catch {
    // The choice still holds for this session.
  }
}

function sync(region) {
  const expanded = document.body.classList.contains(region.className) ? "false" : "true";
  document.querySelector(region.collapse).setAttribute("aria-expanded", expanded);
  document.querySelector(region.open).setAttribute("aria-expanded", expanded);
}

function setCollapsed(region, collapsed) {
  document.body.classList.toggle(region.className, collapsed);
  remember(region.storageKey, collapsed);
  sync(region);
  // The control the reader just used is the one about to be hidden, so focus
  // moves to its counterpart rather than falling back to the document body.
  document.querySelector(collapsed ? region.open : region.collapse).focus();
}

export function initialiseLayout(onOverlay) {
  for (const [kind, region] of Object.entries(REGIONS)) {
    document.body.classList.toggle(region.className, stored(region.storageKey));
    document.querySelector(region.collapse).addEventListener("click", () => setCollapsed(region, true));
    document.querySelector(region.open).addEventListener("click", () => {
      // One control, two meanings by width: expand a yielded track at desktop,
      // open a drawer when the regions have become overlays.
      if (atDesktop()) setCollapsed(region, false);
      else onOverlay(kind);
    });
    sync(region);
  }
}
