"""mdllm — the MarkdownLLM deterministic floor.

Mechanical validation and maintenance for MarkdownLLM domains. The division of
labour (validate.thing.md v2.0): this tool guarantees the mechanical checks
(structural, referential, schema); the LLM keeps the semantic ones (Level 4).

Subcommands:
  validate [path]      Levels 1-3 mechanical validation. Exit 1 on Errors.
                       Example domains under <path>/examples/ are validated
                       as their own corpora in the same run.
  triggers [path]      Evaluate time/dependency/threshold trigger conditions;
                       relationship triggers (and blocked_duration) are listed
                       as not mechanically evaluable — left to the agent.
  index    [path] check|rebuild [--signal triggers|schema|relationships]
  touchpoints <id> [path]  Assimilate beat (change-reconciliation): the declared
                       inbound set + literal references for one thing — "what did
                       I just put at risk?". Human-invoked, never hooked; live.
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
  install-hook [path]  Install a git pre-commit hook running `validate`.

Requires: Python 3.10+, PyYAML. tiktoken optional (tokens falls back to heuristic).
"""

from __future__ import annotations

import argparse
import sys

from .cascade import cmd_cascade
from .coherence import cmd_coherence
from .doctor import cmd_doctor
from .domain_kernel import cmd_domain_kernel
from .evals import cmd_eval
from .history import cmd_changelog, cmd_worklog
from .imports_check import cmd_imports_check
from .indexes import cmd_index
from .kernel_gen import cmd_kernel
from .mcp_server import cmd_mcp_serve
from .provenance import cmd_provenance
from .refresh import cmd_refresh
from .scaffold import cmd_install_hook, cmd_scaffold
from .session import cmd_session_start
from .tokens import cmd_tokens
from .touchpoints import cmd_touchpoints
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

    t = sub.add_parser("triggers", help="evaluate trigger conditions")
    t.add_argument("path", nargs="?", default=".")
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
                             "harness SessionStart hook to inject")
    ss.add_argument("path", nargs="?", default=".")
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
    d.set_defaults(fn=cmd_doctor)

    sc = sub.add_parser("scaffold", help="deterministic domain birth: templates, "
                                         "nested repo, .gitignore isolation, hook, "
                                         "first commit")
    sc.add_argument("path", help="folder to create (its name becomes the domain name)")
    sc.set_defaults(fn=cmd_scaffold)

    h = sub.add_parser("install-hook", help="install git pre-commit validation hook")
    h.add_argument("path", nargs="?", default=".")
    h.set_defaults(fn=cmd_install_hook)
    # Hook body is portable since v3.4.1: root/interpreter resolved at run time.

    ms = sub.add_parser("mcp-serve", help="serve a domain's exposed face over MCP "
                        "(stdio) — the cross-domain producing side (Phase 1: read-only)")
    ms.add_argument("path", help="path to the domain directory to serve")
    ms.set_defaults(fn=cmd_mcp_serve)

    ic = sub.add_parser("imports-check", help="re-quarantine-on-drift: check a "
                        "domain's external imports against their sources' exposed faces")
    ic.add_argument("path", nargs="?", default=".", help="the consumer domain")
    ic.set_defaults(fn=cmd_imports_check)

    return p


def main() -> int:
    # Windows consoles default to a legacy codepage; spec prose is UTF-8.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    args = build_cli().parse_args()
    return args.fn(args)
