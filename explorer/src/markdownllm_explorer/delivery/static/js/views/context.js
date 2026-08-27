export function renderSourceContext(container, source, settings, repository = null) {
  container.replaceChildren(
    block("Source", [["Name", source.display_name], ["Identity", source.id], ["Kind", source.kind], ["Root", settings?.source_path || "Loading…"]]),
    block("Repository", [["State", repository?.kind || settings?.git_kind || source.git_kind], ["Branch", repository?.branch || "—"], ["HEAD", repository?.head_sha || "—"]]),
    block("Authority", [["Source of truth", "Local files and Git"], ["Access", "Read-only"]]),
  );
}

export function renderDocumentContext(container, source, document) {
  const metadata = Object.entries(document.frontmatter?.values || {}).slice(0, 12);
  container.replaceChildren(
    block("Document", [["Path", document.path], ["Size", `${Number(document.size).toLocaleString()} bytes`], ["Modified", new Date(document.modified_at).toLocaleString()], ["Mode", document.mode]]),
    block("Source", [["Name", source.display_name], ["Identity", source.id], ["Kind", source.kind]]),
    block("Frontmatter", metadata.length ? metadata.map(([key, value]) => [key, scalar(value)]) : [["State", document.frontmatter?.state || "absent"]]),
  );
}

function block(title, rows) {
  const section = document.createElement("section"); section.className = "context-block";
  const heading = document.createElement("h2"); heading.textContent = title;
  const list = document.createElement("dl");
  for (const [label, value] of rows) { const term = document.createElement("dt"); term.textContent = label; const detail = document.createElement("dd"); detail.textContent = value ?? "—"; list.append(term, detail); }
  section.append(heading, list); return section;
}

function scalar(value) { return typeof value === "object" ? JSON.stringify(value) : String(value); }
