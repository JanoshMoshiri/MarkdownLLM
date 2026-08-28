import {formatMoment} from "../format.js";

export function renderOverview(container, overview, onMore, onCommit) {
  const repo = overview.repository;
  const dirty = repo.dirty === true ? " · working tree changed" : "";
  container.innerHTML = `
    <section class="hero">
      <div><h2></h2><p>${escapeText(overview.source.kind === "substrate" ? "Framework substrate" : "MarkdownLLM domain")}</p></div>
      <span class="badge">${escapeText(repo.kind)}${escapeText(dirty)}</span>
    </section>
    <section class="metric-grid">
      ${metric(overview.counts.eligible_files, "Files", overview.counts.partial)}
      ${metric(overview.counts.skills, "Skills", overview.counts.partial)}
      ${metric(overview.counts.memory, "Memory things", overview.counts.partial)}
      ${metric(overview.commits.items.length, "Commits shown")}
    </section>
    <div class="section-title"><h2>Commit history</h2><span class="badge">${repo.branch ? escapeText(repo.branch) : repo.kind}</span></div>
    <section class="list" id="commit-list"></section>`;
  container.querySelector(".hero h2").textContent = overview.source.display_name;
  const list = container.querySelector("#commit-list");
  if (!overview.commits.items.length) list.innerHTML = '<div class="empty">No reachable commits for this source.</div>';
  for (const commit of overview.commits.items) appendCommit(list, commit, onCommit);
  refreshCommitAbbreviations(list);
  if (overview.commits.next_cursor) {
    const button = document.createElement("button"); button.className = "load-more"; button.textContent = "Load more commits";
    button.addEventListener("click", () => onMore(overview.commits.next_cursor, list, button));
    list.after(button);
  }
}

export function appendCommit(list, commit, onCommit) {
  const row = document.createElement("button"); row.type = "button"; row.className = "list-row commit-row";
  row.dataset.sha = commit.sha;
  row.addEventListener("click", () => onCommit(commit.sha));
  const info = document.createElement("div");
  const title = document.createElement("h3");
  const sha = document.createElement("span"); sha.className = "commit-sha"; sha.textContent = commit.sha.slice(0, 12);
  sha.dataset.sha = commit.sha; sha.title = commit.sha; sha.setAttribute("aria-label", `Commit ${commit.sha}`);
  title.append(sha, document.createTextNode(` ${commit.subject}`));
  const author = document.createElement("p"); author.textContent = commit.author_name;
  info.append(title, author);
  const time = document.createElement("time"); time.dateTime = commit.authored_at; time.textContent = formatMoment(commit.authored_at);
  row.append(info, time); list.append(row); return row;
}

export function refreshCommitAbbreviations(list) {
  const nodes = [...list.querySelectorAll(".commit-sha")];
  const values = nodes.map(node => node.dataset.sha);
  nodes.forEach(node => {
    const value = node.dataset.sha; let length = 12;
    while (length < value.length && values.some(other => other !== value && other.startsWith(value.slice(0, length)))) length += 1;
    node.textContent = value.slice(0, length);
  });
}

function metric(value, label, partial = false) { return `<article class="metric"><strong>${partial ? "≥" : ""}${Number(value).toLocaleString()}</strong><span>${escapeText(label)}${partial ? " (partial)" : ""}</span></article>`; }
function escapeText(value) { const span = document.createElement("span"); span.textContent = String(value ?? ""); return span.innerHTML; }
