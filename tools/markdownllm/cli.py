"""mdllm — the MarkdownLLM deterministic floor.

Mechanical validation and maintenance for MarkdownLLM domains. The division of
labour (validate.thing.md): this tool guarantees the mechanical checks
(structural, referential, schema); the LLM keeps the semantic ones.

Core subcommands (curated — the FULL set is the usage line below; every
subcommand carries its own --help. This list stopped claiming completeness
after a review-loop finding caught it describing 12 of 26 under an
unqualified heading — a hand list drifts; argparse does not):
  validate [path]      Levels 1-3 mechanical validation. Exit 1 on Errors.
                       Example domains under <path>/examples/ are validated
                       as their own corpora in the same run.
  triggers [path]      Evaluate time/dependency/threshold/import trigger
                       conditions (import = live face reads via imports-check);
                       relationship triggers (and blocked_duration) are listed
                       as not mechanically evaluable — left to the agent.
  index    [path] check|rebuild [--signal triggers|schema|relationships|provenance]
  touchpoints <id> [path]  Assimilate beat (change-reconciliation): the declared
                       inbound set + literal references for one thing — "what did
                       I just put at risk?". Human-invoked, never hooked; live.
  calc     [path] [--thing ID] [--expr E]  Evaluate declared derivations
                       (`computed:` blocks): the floor does every sum, so a
                       figure is computed rather than asserted. Reports, never
                       writes. Exit 1 on disagreement or non-evaluability.
  cascade  <id> [path] Post-completion cascade (write.thing.md): the declared
                       downstream set a thing's completion unblocks — "what did I
                       just unblock?". Mirror of touchpoints; reports, never applies.
  coherence [path]     Dark-region checks: generated-artifact (kernel/index)
                       freshness, foundational_specs<->filesystem, stale labels.
                       Corpus-general; framework-only checks switch on at a root
                       with .markdownllm. Runs in the pre-commit hook.
  tokens   [path]      Measure spec token costs by loading tier.
  doctor   [path]      Probe the environment: floor prerequisites, hook
                       execution (not just presence), framework version drift.
  scaffold <path>      Deterministic domain birth: instantiated templates,
                       nested git repo, outer .gitignore isolation, hook,
                       first commit. The semantic half stays with the agent.
  boundary [path]      Disclosure-boundary check: staged additions/filenames,
                       --message FILE (commit-msg hook), or --history audit,
                       against the LOCAL gitignored .boundary-terms file.
                       Absent file => silent no-op (CI never enforces this).
  install-hook [path]  Install the three mdllm git hooks: pre-commit
                       (boundary + validate + coherence, blocking), commit-msg
                       (disclosure boundary, blocking), post-commit (autopush
                       publication leg, never blocking).

Requires: Python 3.10+, PyYAML. tiktoken optional (tokens falls back to heuristic).
"""

from __future__ import annotations

import argparse
import sys

from .adapters import names as adapter_names, selection_choices
from .boundary import cmd_boundary
from .adapter_install import cmd_adapter_install
from .calc import cmd_calc
from .cascade import cmd_cascade
from .coherence import cmd_coherence
from .doctor import cmd_doctor
from .domain_kernel import cmd_domain_kernel
from .evals import cmd_eval
from .history import cmd_changelog, cmd_worklog
from .harness_ports import LIFECYCLE_BINDINGS
from .imports_check import cmd_estate_check, cmd_imports_check
from .sync import cmd_autopush, cmd_estate_sync
from .indexes import cmd_index
from .kernel_gen import cmd_kernel
from .mcp_server import cmd_mcp_serve
from .provenance import cmd_provenance
from .refresh import cmd_refresh
from .scaffold import cmd_install_hook, cmd_scaffold
from .runtime import cmd_runtime_probe
from .lifecycle_runner import cmd_harness_event
from .session import cmd_session_start
from .tokens import cmd_tokens
from .touchpoints import cmd_candidates, cmd_touchpoints
from .triggers import cmd_triggers
from .validation import cmd_validate

def build_cli() -> argparse.ArgumentParser:
    # Separate from main() so the parser registry is introspectable: generated
    # prose that names a subcommand is tested against THIS, not against the
    # builder that wrote it (a same-builder check is blind to a
    # self-contradictory builder — the phantom `mdllm orient` incident).
    p = argparse.ArgumentParser(prog="mdllm", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate", help="Levels 1-3 mechanical validation")
    v.add_argument("path", nargs="?", default=".")
    v.add_argument("--quiet", action="store_true", help="only print on Errors")
    v.set_defaults(fn=cmd_validate)

    t = sub.add_parser("triggers", help="evaluate trigger conditions; --estate "
                       "sweeps every local clone with a roll-up (run after "
                       "estate-sync)")
    t.add_argument("path", nargs="?", default=".")
    t.add_argument("--estate", action="store_true",
                   help="batch per-domain evaluation over the local clones the "
                        "estate-sync walk finds — ephemeral, never an index")
    t.set_defaults(fn=cmd_triggers)

    i = sub.add_parser("index", help="check or rebuild derived indexes")
    i.add_argument("path", nargs="?", default=".")
    i.add_argument("action", choices=["check", "rebuild"])
    i.add_argument("--signal", choices=["triggers", "schema", "relationships", "provenance"])
    i.set_defaults(fn=cmd_index)

    tp = sub.add_parser("touchpoints", help="Assimilate beat: what a thing's change "
                                            "disturbs (declared edges + literal refs)")
    tp.add_argument("id", help="the thing id to assimilate around")
    tp.add_argument("path", nargs="?", default=".")
    tp.set_defaults(fn=cmd_touchpoints)

    cs = sub.add_parser("cascade", help="post-completion cascade: what a thing's "
                                        "completion unblocks downstream (mirror of touchpoints)")
    cs.add_argument("id", help="the thing id that just reached a terminal status")
    cs.add_argument("path", nargs="?", default=".")
    cs.set_defaults(fn=cmd_cascade)

    ca = sub.add_parser("calc", help="evaluate declared derivations (`computed:` "
                                     "blocks) — the floor does every sum; reports, "
                                     "never writes")
    ca.add_argument("path", nargs="?", default=".")
    ca.add_argument("--thing", metavar="ID", help="one thing's block, or the "
                    "context an --expr is evaluated in")
    ca.add_argument("--expr", metavar="E", help="an ad-hoc expression; with "
                    "--thing it reads that thing, without one it is pure arithmetic")
    ca.set_defaults(fn=cmd_calc)

    pv = sub.add_parser("provenance", help="validate provenance chains (provenance.md)")
    pv.add_argument("path", nargs="?", default=".")
    pv.set_defaults(fn=cmd_provenance)

    k = sub.add_parser("tokens", help="measure spec token costs by tier")
    k.add_argument("path", nargs="?", default=".")
    k.set_defaults(fn=cmd_tokens)

    ev = sub.add_parser("eval", help="check a golden-scenario fixture against domain state")
    ev.add_argument("path", nargs="?", default=".")
    ev.add_argument("--fixture")
    ev.add_argument("--run", action="store_true",
                    help="Stage 2: seed workspace + headless agent + assert")
    ev.add_argument("--model", default="haiku")
    ev.add_argument("--trials", type=int, default=1)
    ev.add_argument("--bare", action="store_true",
                    help="no-framework condition: strip AGENTS.md/skills/schema")
    ev.add_argument("--report", action="store_true",
                    help="aggregate evals/runs/*/result.json into per-cell pass rates")
    ev.add_argument("--dry-run", action="store_true")
    ev.add_argument("--timeout", type=int, default=900,
                    help="seconds per trial (default 900)")
    ev.set_defaults(fn=cmd_eval)

    kn = sub.add_parser("kernel", help="generate kernel.md from spec kernel blocks")
    kn.add_argument("path", nargs="?", default=".")
    kn.add_argument("--check", action="store_true",
                    help="drift check: compare kernel.md against a fresh build")
    kn.set_defaults(fn=cmd_kernel)

    dk = sub.add_parser("domain-kernel",
                        help="generate/refresh a domain AGENTS.md's managed operative blocks")
    dk.add_argument("path", nargs="?", default=".")
    dk.add_argument("--check", action="store_true",
                    help="drift check: compare managed blocks against a fresh build")
    dk.set_defaults(fn=cmd_domain_kernel)

    ss = sub.add_parser("session-start",
                        help="emit the session-start ritual (version + velocity) for a "
                             "harness startup hook to inject")
    ss.add_argument("path", nargs="?", default=".")
    ss.add_argument("--assistant", action="store_true",
                    help="PHASE 0 PROTOTYPE (assistant-register plan): "
                         "assistant-shaped orientation instead of the status dump")
    ss.set_defaults(fn=cmd_session_start)

    co = sub.add_parser("coherence", help="dark-region checks: generated-artifact "
                                          "freshness, catalog/filesystem, stale labels")
    co.add_argument("path", nargs="?", default=".")
    co.add_argument("--window", type=int, default=15,
                    help="stable-staleness lookback in commits (default 15)")
    co.add_argument("--quiet", action="store_true", help="only print on Errors")
    co.set_defaults(fn=cmd_coherence)

    c = sub.add_parser("changelog", help="draft a CHANGELOG entry from commits")
    c.add_argument("path", nargs="?", default=".")
    c.add_argument("--since", help="ref to start from (e.g. a version tag)")
    c.set_defaults(fn=cmd_changelog)

    wl = sub.add_parser("worklog", help="print a session-grouped view of the commit stream (on-demand; not committed)")
    wl.add_argument("path", nargs="?", default=".")
    wl.add_argument("--write", action="store_true", help="save a local (gitignored) WORKLOG.md snapshot; default prints to stdout")
    wl.set_defaults(fn=cmd_worklog)

    rf = sub.add_parser("refresh", help="floor-only domain refresh: report version "
                                        "delta + unseen CHANGELOG; --seal bumps seen")
    rf.add_argument("path", nargs="?", default=".", help="the domain directory")
    rf.add_argument("--seal", action="store_true",
                    help="after adoption: bump framework_version_seen in domain AGENTS.md")
    rf.set_defaults(fn=cmd_refresh)

    d = sub.add_parser("doctor", help="probe the environment: floor prerequisites, "
                                      "hook execution, framework version drift")
    d.add_argument("path", nargs="?", default=".")
    d.add_argument("--harness", choices=tuple(
        choice for choice in selection_choices() if choice != "none"),
                   help="show explicit adapter facts for one harness or all")
    d.set_defaults(fn=cmd_doctor)

    sc = sub.add_parser("scaffold", help="deterministic domain birth: templates, "
                                         "nested repo, .gitignore isolation, hook, "
                                         "first commit")
    sc.add_argument("path", help="folder to create (its name becomes the domain name)")
    sc.add_argument("--harness", choices=selection_choices(),
                    help="outer adapter projection: one harness, all, or none; "
                         "omitting preserves the compatibility default")
    sc.set_defaults(fn=cmd_scaffold)

    ai = sub.add_parser(
        "adapter-install",
        help="show and safely apply a project-local harness adapter diff")
    ai.add_argument("path", nargs="?", default=".")
    ai.add_argument("--harness", required=True,
                    choices=tuple(choice for choice in selection_choices()
                                  if choice != "none"),
                    help="one registered harness or all selected adapters")
    ai.add_argument("--dry-run", action="store_true",
                    help="show decisions and owned diff without writing")
    ai.set_defaults(fn=cmd_adapter_install)

    h = sub.add_parser("install-hook", help="install the three mdllm git hooks (pre-commit, commit-msg, post-commit) and execution-test pre-commit where git supports it")
    h.add_argument("path", nargs="?", default=".")
    h.set_defaults(fn=cmd_install_hook)
    # Hook body is portable since v3.4.1: root/interpreter resolved at run time.

    rp = sub.add_parser("runtime-probe",
                        help="report, per interpreter candidate, whether it "
                             "exists and whether the floor's dependency loads "
                             "— the reproducible runtime check for any "
                             "harness's shell (framework root or a directly "
                             "opened nested domain)")
    rp.add_argument("path", nargs="?", default=".")
    rp.set_defaults(fn=cmd_runtime_probe)

    he = sub.add_parser(
        "harness-event",
        help="internal project-hook dispatch for one ordered lifecycle binding")
    he.add_argument("harness", choices=adapter_names())
    he.add_argument("moment", choices=tuple(
        binding.moment for binding in LIFECYCLE_BINDINGS))
    he.add_argument("path", help="Git repository root supplied by the hook")
    he.add_argument("definition_hash",
                    help="renderer-embedded managed-definition fingerprint")
    he.set_defaults(fn=cmd_harness_event)

    ms = sub.add_parser("mcp-serve", help="serve a domain's exposed face over MCP "
                        "— the cross-domain producing side (read-only). Default "
                        "transport is stdio (the client spawns the server); --http "
                        "serves the same face over Streamable HTTP, loopback-only "
                        "(public exposure waits for the OAuth 2.1 leg)")
    ms.add_argument("path", help="path to the domain directory to serve")
    ms.add_argument("--http", action="store_true",
                    help="serve over Streamable HTTP instead of stdio (endpoint /mcp)")
    ms.add_argument("--port", type=int, default=8765, help="HTTP port (default 8765)")
    ms.add_argument("--host", default="127.0.0.1",
                    help="HTTP bind host — loopback only; non-loopback is refused")
    ms.add_argument("--token", nargs="?", const="auto", default=None,
                    help="gate every HTTP request behind `Authorization: Bearer "
                         "<token>`; with no value, a per-run token is generated "
                         "and printed to stderr — the probe control for "
                         "tunnelled cross-machine reads (dies with the process)")
    ms.set_defaults(fn=cmd_mcp_serve)

    ic = sub.add_parser("imports-check", help="re-quarantine-on-drift: check a "
                        "domain's external imports against their sources' exposed faces "
                        "(both directions: stale = source moved, diverged = mirror moved)")
    ic.add_argument("path", nargs="?", default=".", help="the consumer domain")
    ic.set_defaults(fn=cmd_imports_check)

    ec = sub.add_parser("estate-check", help="operator-axis batch of imports-check "
                        "over consumer roots — named explicitly, or (no args) the "
                        "local clones the estate-sync walk finds; ephemeral "
                        "per-consumer reads, never an index")
    ec.add_argument("paths", nargs="*", help="consumer domain roots; omit to walk "
                    "local clones (a filesystem fact, not an estate manifest)")
    ec.set_defaults(fn=cmd_estate_check)

    es = sub.add_parser("estate-sync", help="sync before orienting: fetch + "
                        "ff-only pull across the estate's repos (root + domain(s)/*); "
                        "divergence reported, never resolved; never pushes; "
                        "--status = publication debt from cached refs, no network")
    es.add_argument("paths", nargs="*", help="root to discover under (default .), "
                    "or several explicit repo paths")
    es.add_argument("--status", action="store_true",
                    help="no network: report unpushed/diverged/dirty repos only "
                         "(the session-end publication-debt view)")
    es.add_argument("--timeout", type=int, default=20,
                    help="seconds per network call before degrading (default 20)")
    es.set_defaults(fn=cmd_estate_sync)

    ap_ = sub.add_parser("autopush", help="post-commit publication leg: push the "
                         "current branch to its upstream unless AGENTS.md declares "
                         "git.autopush: false (absence = on); bounded, never forces, "
                         "rejection surfaced as DIVERGED never resolved; exit 0 always")
    ap_.add_argument("path", nargs="?", default=".")
    ap_.add_argument("--timeout", type=int, default=20,
                     help="seconds before the push degrades to publication debt")
    ap_.set_defaults(fn=cmd_autopush)

    cd = sub.add_parser("candidates", help="pre-commit advisory: for staged "
                        "MODIFIED things, surface the cue question (reasoned-from: "
                        "definition surface or fan-in) and the serve-side notice "
                        "(exposed => this change publishes); never blocks, exit 0 always")
    cd.add_argument("path", nargs="?", default=".")
    cd.set_defaults(fn=cmd_candidates)

    bd = sub.add_parser("boundary", help="disclosure-boundary check: staged "
                        "additions, filenames, or a commit message against the "
                        "LOCAL .boundary-terms file (gitignored; absent => no-op)")
    bd.add_argument("path", nargs="?", default=".")
    bd.add_argument("--message", metavar="FILE",
                    help="scan a commit-message file (commit-msg hook mode)")
    bd.add_argument("--history", action="store_true",
                    help="full-archive audit: all revs and messages (console only)")
    bd.add_argument("--quiet", action="store_true")
    bd.set_defaults(fn=cmd_boundary)

    return p


def main() -> int:
    # Windows consoles default to a legacy codepage; spec prose is UTF-8.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    args = build_cli().parse_args()
    return args.fn(args)
