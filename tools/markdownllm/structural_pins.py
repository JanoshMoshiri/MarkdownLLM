"""Structural commit pins must name a commit that exists.

A structural pin is the one class of field the floor cannot check by parsing:
it is a *transcribed* identifier, and a wrong SHA is byte-indistinguishable
from a right one to any reader, human or model
(`a-transcribed-identifier-is-unverifiable-by-reading`).  The seams sprint
mistranscribed two pins in two days — one caught by hand, one that survived
five commits — which is the evidence that promoted this from the coherence
backlog into the floor.

`definition_commit` was already resolved at validation (workflow revision
binding, validation.py); `informed_by` commits were resolved only when
`mdllm provenance` was run on demand, so the commit boundary accepted a pin
that named no commit.  This closes that gap for every LOCAL pin the
structural-reference registry declares, and only those: the registry decides
the field set, this module decides nothing but resolvability.

Three properties make this checkable rather than judgement in mechanical
clothing:

* **Same builder.** The authority is git's own object database, so the check
  cannot disagree with truth and no suppression list is possible.
* **One batched consultation.** Every pin in a corpus is resolved by a single
  `git cat-file --batch-check` process, not one subprocess per pin.
* **Honest degradation.** Where git cannot be consulted the check says it
  could not look; it never reports a clean corpus it did not read
  (`a-check-run-where-it-cannot-see-mints-a-false-finding`).

**On severity, and its relation to `mdllm provenance`.**  Provenance grades an
*already-committed* chain by whether it is still traceable: an unreachable pin
whose cited input is still in the corpus is a Warning there, because the
reasoning survives a stale anchor.  This check answers a different question at
a different moment — *is this candidate's pin a commit at all* — where the
overwhelmingly likely cause is a transcription error the author can fix in the
same edit.  That is Error severity: fix now, at the boundary.  The two are
deliberately not the same number.

**The cost this design accepts, recorded rather than discovered later.**  A
history rewrite re-hashes every commit, so it invalidates every pin in the
corpus at once — including pins on terminal things — and the floor would then
block until each is re-pinned.  That is a real bill, and it is the honest one:
after a rewrite those pins genuinely name nothing, and a check that stayed
quiet about them would be asserting a traceability the repository no longer
has.  The remedy stays performable for a terminal thing (a pin is a factual
reference, not a state claim — you look the commit up and correct it), which
is what keeps this inside the backlog's standing scoping test.

Why `git cat-file --batch-check` rather than a literal batched `git rev-parse`:
rev-parse over many revisions is not line-oriented — it aborts at the first
unresolvable argument and never reports the rest, so a corpus with two bad
pins would surface one.  `--batch-check` emits exactly one answer line per
input line, in order, and exits 0 whatever it finds.  It is the same batched
primitive `RepositoryView.prefetch` already uses, and it satisfies the
one-process constraint the design is explicit about.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from .model import Corpus, Finding, SEV_ERROR, SEV_WARNING
from .structural_refs import CommitPinScope, iter_commit_pins

#: Label for the corpus-level finding that reports a degraded consultation.
#: Not a thing id — the same convention `framework-version` and
#: `retrospective-cadence` already use for corpus-scoped findings.
PIN_SUBJECT = "structural-pins"

RESOLVED, UNRESOLVED, UNANSWERED = "resolved", "unresolved", "unanswered"


@dataclass(frozen=True)
class PinConsultation:
    """What one batched consultation of git established, and what it did not.

    ``obstacle`` is the null-result primitive made explicit: ``None`` means
    git was asked and answered, any other value means this run could not look
    and its silence about a pin is not evidence about that pin.
    """

    status: dict[str, str]
    obstacle: str | None = None

    def of(self, pin: str) -> str:
        return self.status.get(pin, UNANSWERED)


def _git(root: Path, args: list[str], stdin: str | None = None):
    """Run git, returning the completed process, or None if it cannot run.

    A missing git binary raises OSError from ``subprocess.run``; swallowing it
    here is what lets the caller report "could not look" instead of crashing
    the whole validation pass on an environment fact.
    """
    try:
        return subprocess.run(["git", *args], cwd=root, input=stdin,
                              capture_output=True, text=True,
                              encoding="utf-8", errors="replace")
    except OSError:
        return None


def repository_root(root: Path) -> Path | None:
    """The Git worktree root owning ``root``, or None if there is none.

    A corpus is often a nested slice of its repository — the framework's
    example corpora are the live case — and a pin in that slice names a commit
    in the owning repository, not in the slice.
    """
    out = _git(root, ["rev-parse", "--show-toplevel"])
    if out is None or out.returncode != 0 or not (out.stdout or "").strip():
        return None
    return Path(out.stdout.strip()).resolve()


def _sendable(pin: str) -> bool:
    """Whether a pin can be a line of the batch request.

    `--batch-check` reads one revision per line, so a value carrying
    whitespace could otherwise inject additional request lines and desynchronise
    the positional answer mapping.  Such a value also cannot be a commit id, so
    refusing to send it loses nothing: it is reported unresolved, which it is.
    """
    return bool(pin) and not any(ch.isspace() for ch in pin)


def consult_git(root: Path, pins: list[str]) -> PinConsultation:
    """Resolve every pin in ``pins`` with one git process.

    Answers are mapped positionally: `--batch-check` emits exactly one line per
    request line, in order.  Any pin left without an answer stays
    ``UNANSWERED`` rather than being read as either outcome.
    """
    status: dict[str, str] = {}
    askable: list[str] = []
    for pin in pins:
        if _sendable(pin):
            askable.append(pin)
            status[pin] = UNANSWERED
        else:
            status[pin] = UNRESOLVED
    if not askable:
        # Every pin already has a verdict; git was never needed, so this is a
        # complete answer rather than a degraded one.
        return PinConsultation(status)

    repo = repository_root(root)
    if repo is None:
        return PinConsultation(
            status, "no Git repository owns this corpus (or git is unavailable)")

    request = "".join(f"{pin}^{{commit}}\n" for pin in askable)
    out = _git(repo, ["cat-file", "--batch-check"], stdin=request)
    if out is None:
        return PinConsultation(status, "git could not be executed")
    if out.returncode != 0:
        detail = (out.stderr or "").strip().splitlines()
        return PinConsultation(
            status, f"git cat-file failed: {detail[0] if detail else 'no detail'}")

    for pin, line in zip(askable, (out.stdout or "").splitlines()):
        fields = line.split()
        # Success is `<oid> commit <size>`; every failure form (`missing`,
        # `ambiguous`, `dangling`, ...) echoes the request and names the
        # obstacle instead. Only an actual commit counts as resolved.
        status[pin] = (RESOLVED if len(fields) == 3 and fields[1] == "commit"
                       else UNRESOLVED)
    return PinConsultation(status)


def structural_pin_findings(root: Path, corpus: Corpus) -> list[Finding]:
    """Every local structural pin in ``corpus`` must name a real commit.

    Quiet when there is nothing to check: a corpus declaring no local pin gets
    no finding, in a Git repository or out of one.  There is then no absence to
    misread — the check made no claim because there was nothing to claim about.
    """
    declared: list[tuple[str, str, str]] = []  # (thing, field label, pin)
    for thing in corpus.things:
        name = thing.id or thing.path.name
        for pin in iter_commit_pins(thing.meta):
            if pin.scope is not CommitPinScope.LOCAL or pin.resolved_elsewhere:
                continue
            declared.append((name, pin.field, pin.pin))
    if not declared:
        return []

    unique = list(dict.fromkeys(pin for _, _, pin in declared))
    # A corpus may be a nested slice of its repository (the example corpora are
    # the live case), so start the repository walk where the view was bound —
    # the same discovery `WorkflowDefinitionResolver` performs for the same
    # reason.
    origin = corpus.view.root if corpus.view is not None else Path(root)
    consultation = consult_git(Path(origin).resolve(), unique)

    findings: list[Finding] = []
    unanswered: set[str] = set()
    for name, field, pin in declared:
        state = consultation.of(pin)
        if state == UNRESOLVED:
            findings.append(Finding(
                SEV_ERROR, name,
                f"`{field}` pin `{pin}` resolves to no commit in this "
                f"repository — re-pin from `git rev-parse` (a transcribed "
                f"identifier is unverifiable by reading)"))
        elif state == UNANSWERED:
            unanswered.add(pin)
    if unanswered:
        findings.append(Finding(
            SEV_WARNING, PIN_SUBJECT,
            f"{len(unanswered)} structural commit pin(s) could not be "
            f"resolved: {consultation.obstacle or 'git returned no answer for them'}"
            f" — this run could not look, so it reports nothing about whether "
            f"those pins are valid"))
    return findings
