import {formatMoment} from "../format.js";

// Frontmatter fields that name other things rather than describe this one.
// They are lifted out of the metadata list and rendered as navigable chips,
// because a reader following a reference wants to arrive, not to read an
// identifier out of a JSON blob and search for it by hand.
const REFERENCE_FIELDS = [
  ["informed_by", "Informed by"],
  ["linked_things", "Linked things"],
  ["dependencies", "Dependencies"],
  ["blocks", "Blocks"],
  ["parent", "Parent"],
  ["definition", "Definition"],
  ["parties", "Parties"],
];

export function renderSourceContext(container, source, settings, repository = null) {
  container.replaceChildren(
    block("Source", [["Name", source.display_name], ["Identity", source.id], ["Kind", source.kind], ["Root", settings?.source_path || "Loading…"]]),
    block("Repository", [["State", repository?.kind || settings?.git_kind || source.git_kind], ["Branch", repository?.branch || "—"], ["HEAD", repository?.head_sha || "—"]]),
    block("Authority", [["Source of truth", "Local files and Git"], ["Access", "Read-only"]]),
  );
}

export function renderDocumentContext(container, source, document_, onReference) {
  // Stamping the panel with its document lets a late reference lookup tell
  // whether the chips it was asked to settle are still the ones on screen.
  container.dataset.documentPath = document_.path;
  const values = document_.frontmatter?.values || {};
  const references = collectReferences(values);
  const referenced = new Set(references.map(group => group.field));
  // Every remaining entry is shown. Silently cutting the list at a fixed
  // number left a reader with no way to tell a short frontmatter from a
  // truncated one.
  const metadata = Object.entries(values).filter(([key]) => !referenced.has(key));

  const blocks = [
    block("Document", [
      ["Path", document_.path],
      ["Size", `${Number(document_.size).toLocaleString()} bytes`],
      ["Modified", formatMoment(document_.modified_at)],
      ["Mode", document_.mode],
    ]),
    block("Source", [["Name", source.display_name], ["Identity", source.id], ["Kind", source.kind]]),
  ];
  if (references.length) blocks.push(referenceBlock(references, onReference));
  blocks.push(block("Frontmatter", metadata.length
    ? metadata.map(([key, value]) => [key, scalar(value)])
    : [["State", document_.frontmatter?.state || "absent"]]));
  container.replaceChildren(...blocks);
}

export function referencedIds(frontmatter) {
  const seen = [];
  for (const group of collectReferences(frontmatter?.values || {})) {
    for (const entry of group.entries) if (!seen.includes(entry.id)) seen.push(entry.id);
  }
  return seen;
}

export function applyReferenceResolution(container, resolved, documentPath, partial = false) {
  if (documentPath !== undefined && container.dataset.documentPath !== documentPath) return;
  for (const chip of container.querySelectorAll(".reference-chip")) {
    const path = resolved[chip.dataset.id];
    chip.classList.remove("resolving");
    if (path) {
      chip.dataset.path = path;
      chip.disabled = false;
      chip.title = path;
      chip.classList.remove("unresolved", "uncertain");
      continue;
    }
    // Never a dead control: a chip that cannot lead anywhere says so rather
    // than looking identical to one that can. And absence found in a complete
    // index is a different claim from absence found in a truncated one, so a
    // partial index is never allowed to assert "not found".
    chip.disabled = true;
    chip.classList.remove("unresolved", "uncertain");
    chip.classList.add(partial ? "uncertain" : "unresolved");
    chip.title = partial
      ? "This source's index was truncated, so this reference could not be checked."
      : "No thing with this identifier was found in this source.";
  }
}

function collectReferences(values) {
  const groups = [];
  for (const [field, label] of REFERENCE_FIELDS) {
    const entries = referenceEntries(values[field]);
    if (entries.length) groups.push({field, label, entries});
  }
  return groups;
}

function referenceEntries(value) {
  if (typeof value === "string") return value ? [{id: value}] : [];
  if (Array.isArray(value)) return value.flatMap(item => referenceEntries(item));
  if (value && typeof value === "object" && typeof value.id === "string") {
    return [{id: value.id, note: value.relation || value.commit || null}];
  }
  return [];
}

function referenceBlock(groups, onReference) {
  const section = document.createElement("section");
  section.className = "context-block";
  const heading = document.createElement("h2");
  heading.textContent = "References";
  section.append(heading);
  for (const group of groups) {
    const label = document.createElement("p");
    label.className = "reference-label";
    label.textContent = group.label;
    const row = document.createElement("div");
    row.className = "reference-row";
    for (const entry of group.entries) row.append(chip(entry, onReference));
    section.append(label, row);
  }
  return section;
}

function chip(entry, onReference) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "reference-chip resolving";
  button.dataset.id = entry.id;
  // Chips start disabled and settle once resolution answers, so a reference is
  // never clickable before anyone knows whether it leads anywhere.
  button.disabled = true;
  button.title = "Looking for this thing in the source…";
  const name = document.createElement("span");
  name.className = "reference-id";
  name.textContent = entry.id;
  button.append(name);
  if (entry.note) {
    const note = document.createElement("span");
    note.className = "reference-note";
    note.textContent = entry.note;
    button.append(note);
  }
  button.addEventListener("click", () => {
    if (button.dataset.path) onReference(button.dataset.path);
  });
  return button;
}

function block(title, rows) {
  const section = document.createElement("section"); section.className = "context-block";
  const heading = document.createElement("h2"); heading.textContent = title;
  const list = document.createElement("dl");
  for (const [label, value] of rows) { const term = document.createElement("dt"); term.textContent = label; const detail = document.createElement("dd"); detail.textContent = value ?? "—"; list.append(term, detail); }
  section.append(heading, list); return section;
}

function scalar(value) { return typeof value === "object" ? JSON.stringify(value) : String(value); }
