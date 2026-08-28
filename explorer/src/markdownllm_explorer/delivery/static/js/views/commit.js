import {formatMoment} from "../format.js";

const CHANGE_LABEL = {added: "added", modified: "changed", deleted: "deleted"};

export function renderCommit(container, detail, onOpen, onBack) {
  container.replaceChildren();

  const head = node("section", "commit-head");
  const back = node("button", "quiet-button commit-back");
  back.type = "button";
  back.textContent = "‹ Commit history";
  back.addEventListener("click", onBack);
  const title = node("h2");
  title.textContent = detail.subject;
  const meta = node("p", "commit-meta");
  const sha = node("span", "commit-sha");
  sha.textContent = detail.sha.slice(0, 12);
  sha.title = detail.sha;
  meta.append(sha, document.createTextNode(` ${detail.author_name} · `));
  const when = node("time");
  when.dateTime = detail.authored_at;
  when.textContent = formatMoment(detail.authored_at);
  meta.append(when);
  head.append(back, title, meta);
  container.append(head);

  if (!detail.files.length) {
    const empty = node("div", "empty");
    empty.textContent = "This commit changed no files this source can show.";
    container.append(empty);
    return;
  }

  const split = node("div", "split-view");
  const list = node("section", "collection");
  list.setAttribute("aria-label", "Files changed in this commit");
  const reader = node("section", "reader");
  const prompt = node("div", "empty");
  prompt.textContent = "Choose a file to read it as this commit left it.";
  reader.append(prompt);

  for (const file of detail.files) list.append(fileButton(file, list, onOpen));
  if (detail.partial) {
    const note = node("p", "partial-note");
    note.textContent = "This commit touched more files than Explorer lists at once.";
    list.append(note);
  }
  split.append(list, reader);
  container.append(split);
}

function fileButton(file, list, onOpen) {
  const button = node("button", "collection-item");
  button.type = "button";
  button.dataset.path = file.path;
  const title = node("strong");
  title.textContent = file.path.split("/").pop();
  const where = node("small");
  where.textContent = file.path;
  const badge = node("small", `change-flag change-${file.change}`);
  badge.textContent = CHANGE_LABEL[file.change] || file.change;
  button.append(title, where, badge);
  if (!file.openable) {
    button.disabled = true;
    const why = node("small", "issue");
    // A deleted path has no content at this commit; anything else unopenable
    // was refused by source admission rather than by git.
    why.textContent = file.change === "deleted"
      ? "no content at this commit"
      : "not readable in this source";
    button.append(why);
  } else {
    button.addEventListener("click", () => onOpen(file.path));
  }
  return button;
}

export function renderCommitDocument(container, document_, change) {
  const target = container.querySelector(".reader");
  if (!target) return;
  target.replaceChildren();

  const head = node("div", "reader-head");
  const title = node("h2");
  title.textContent = document_.path;
  const badge = node("span", "badge");
  // A path reached by a link rather than from this commit's own list was not
  // necessarily touched by it, so "changed in <sha>" there would be a claim
  // nobody checked.
  badge.textContent = change
    ? `${CHANGE_LABEL[change] || change} in ${document_.sha.slice(0, 12)}`
    : `as at ${document_.sha.slice(0, 12)}`;
  head.append(title, badge);

  const legend = node("p", "historical-legend");
  // Say what is not here. A reader who sees only additions highlighted could
  // otherwise take the absence of removals as "nothing was removed". Naming
  // the line numbers also puts the change locations somewhere that does not
  // depend on seeing a colour, or on reading the gutter at all. And "not
  // determined" is never allowed to read as "nothing changed".
  if (document_.ranges_known === false) {
    legend.textContent = "This commit's change to this file is too large to mark line by line, so the file is shown as the commit left it without marking. Removed lines are not part of this view.";
  } else {
    legend.textContent = document_.added_ranges.length
      ? `Marked lines are what this commit added or changed — ${describeRanges(document_.added_ranges)}. Removed lines are not part of this view.`
      : "This commit added no lines to this file. Removed lines are not part of this view.";
  }

  target.append(head, legend, historicalBody(document_));
}

function normalisedRanges(ranges, total) {
  const clamped = [];
  for (const pair of Array.isArray(ranges) ? ranges : []) {
    const start = Math.max(1, Math.min(Number(pair[0]) || 0, total));
    const end = Math.max(start, Math.min(Number(pair[1]) || 0, total));
    if (start > total) continue;
    clamped.push([start, end]);
  }
  clamped.sort((left, right) => left[0] - right[0]);
  const merged = [];
  for (const [start, end] of clamped) {
    const last = merged[merged.length - 1];
    if (last && start <= last[1] + 1) last[1] = Math.max(last[1], end);
    else merged.push([start, end]);
  }
  return merged;
}

function historicalBody(document_) {
  const lines = document_.content.split("\n");
  // A file ending in a newline splits to a trailing empty element. Numbering it
  // would claim a line the file does not have, and would leave the gutter one
  // row short of the code beside it.
  if (lines.length > 1 && lines[lines.length - 1] === "") lines.pop();
  const body = node("div", "historical");

  // One normalisation feeding both panes. The gutter walked the ranges assuming
  // they arrive sorted and disjoint while the code pane clamped them, so a
  // malformed pair would have put the two columns out of step with each other.
  const ranges = normalisedRanges(document_.added_ranges, lines.length);
  const gutter = node("pre", "historical-gutter");
  gutter.setAttribute("aria-hidden", "true");
  gutter.textContent = gutterText(lines.length, ranges);

  // Contiguous added ranges become one <mark> each rather than one element per
  // line: a megabyte-sized file is a few marks, not tens of thousands of nodes.
  const code = node("pre", "historical-code");
  const segments = [];
  let cursor = 1;
  for (const [start, end] of ranges) {
    const from = Math.max(cursor, start);
    const to = Math.min(end, lines.length);
    if (to < from) continue;
    if (from > cursor) segments.push({added: false, from: cursor, to: from - 1});
    segments.push({added: true, from, to});
    cursor = to + 1;
  }
  if (cursor <= lines.length) segments.push({added: false, from: cursor, to: lines.length});

  // Newlines join segments rather than terminate them, so the rendered text is
  // exactly the file's own bytes and stays in step with the gutter.
  segments.forEach((segment, index) => {
    if (index) code.append(window.document.createTextNode("\n"));
    const text = lines.slice(segment.from - 1, segment.to).join("\n");
    if (!segment.added) { code.append(window.document.createTextNode(text)); return; }
    const mark = window.document.createElement("mark");
    mark.textContent = text;
    code.append(mark);
  });

  body.append(gutter, code);
  return body;
}

const NAMED_RANGES = 8;

function describeRanges(ranges) {
  const named = ranges.slice(0, NAMED_RANGES)
    .map(([start, end]) => (start === end ? `${start}` : `${start}–${end}`))
    .join(", ");
  const remainder = ranges.length - NAMED_RANGES;
  const places = `line${ranges.length === 1 && ranges[0][0] === ranges[0][1] ? "" : "s"} ${named}`;
  return remainder > 0 ? `${places} and ${remainder} more` : places;
}

function gutterText(total, ranges) {
  const rows = [];
  let index = 0;
  for (let line = 1; line <= total; line += 1) {
    while (index < ranges.length && ranges[index][1] < line) index += 1;
    const added = index < ranges.length && ranges[index][0] <= line && line <= ranges[index][1];
    rows.push(`${added ? "+" : " "}${line}`);
  }
  return rows.join("\n");
}

function node(tag, className) {
  const created = window.document.createElement(tag);
  if (className) created.className = className;
  return created;
}
