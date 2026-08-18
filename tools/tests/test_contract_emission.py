"""Phase 1 of the ``cowork-adapter`` plan: contract emission.

``session-start --contract`` injects the Tier-0 contract CONTENT — the
operative kernel, the entry file, and a reading list derived from the
filesystem at emission time — ahead of orientation. Injection, not
instruction: in a harness with no entry-file discovery, "go read the
contract" loses to the live request (field evidence 2026-08-08), and the
session gate's attestation would otherwise vouch for ritual, not contract.

Pinned here:

- the derived list cannot be short — a file added under ``skills/`` or
  ``prompts/`` appears with no other change (the 2026-08-08 authored-list
  failure made structural);
- emission is bounded with MARKED elision naming the on-disk path;
- the attestation records real contract emission with a third token the
  gate ignores (token 0 stays the freshness fact old attestations carry);
- the plain hook path is byte-identical to before — hook budgets are two
  orders of magnitude too small for a contract, so hook bindings never
  pass ``--contract``.

Run: python -m pytest tools/tests/test_contract_emission.py -q
"""

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mdllm  # noqa: E402
from markdownllm.session import (  # noqa: E402
    CONTRACT_SECTION_CHARACTERS, _emit_contract,
)


def _ns(**kw):
    import argparse
    defaults = {"contract": False}
    defaults.update(kw)
    return argparse.Namespace(**defaults)


def _git_repo(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q"], cwd=p, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=p, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=p, check=True)


@pytest.fixture(scope="module")
def pristine(tmp_path_factory) -> Path:
    """One scaffolded domain reused by read-only tests."""
    parent = tmp_path_factory.mktemp("emission")
    _git_repo(parent)
    target = parent / "emission-domain"
    assert mdllm.cmd_scaffold(_ns(path=str(target))) == 0
    return target


@pytest.fixture()
def mutable(tmp_path) -> Path:
    """A scaffolded domain the test may mutate."""
    _git_repo(tmp_path)
    target = tmp_path / "emission-domain"
    assert mdllm.cmd_scaffold(_ns(path=str(target))) == 0
    return target


FW_ROOT = Path(mdllm.__file__).resolve().parents[1]


# ----------------------------------------------------------------- emission

def test_contract_precedes_orientation_and_carries_both_files(
        pristine, capsys):
    assert mdllm.cmd_session_start(
        _ns(path=str(pristine), contract=True)) == 0
    out = capsys.readouterr().out

    contract_at = out.index("MarkdownLLM — Tier-0 Contract (emitted)")
    kernel_at = out.index("Framework Operative Kernel")     # kernel CONTENT
    entry_at = out.index("## The entry file — `AGENTS.md`")
    ritual_at = out.index("MarkdownLLM — Session Start")
    assert contract_at < kernel_at < entry_at < ritual_at
    # The entry file arrives as content, not as a pointer: the scaffolded
    # AGENTS.md body is present verbatim past its heading.
    agents_body = (pristine / "AGENTS.md").read_text(encoding="utf-8")
    assert agents_body[-400:] in out
    # Step 1 stops instructing a read that emission already performed.
    assert "Already emitted above" in out


def test_plain_session_start_is_unchanged(pristine, capsys):
    assert mdllm.cmd_session_start(_ns(path=str(pristine))) == 0
    out = capsys.readouterr().out
    assert "Tier-0 Contract" not in out
    assert "Already emitted above" not in out
    assert out.startswith("# MarkdownLLM — Session Start")


def test_derived_list_cannot_be_short(mutable, capsys):
    """A file landing under skills/ or prompts/ appears in the next emission
    with no other change — the list is derived, so it cannot drift."""
    (mutable / "prompts" / "zz-added-ritual.md").write_text(
        "# added after scaffold\n", encoding="utf-8")
    (mutable / "skills" / "zz-added.skill.md").write_text(
        "# added after scaffold\n", encoding="utf-8")

    assert mdllm.cmd_session_start(
        _ns(path=str(mutable), contract=True)) == 0
    out = capsys.readouterr().out
    assert "- `prompts/zz-added-ritual.md`" in out
    assert "- `skills/zz-added.skill.md`" in out
    # And every scaffold-delivered file is still there beside them.
    for existing in sorted(p.name for p in (mutable / "prompts").glob("*.md")):
        assert f"- `prompts/{existing}`" in out


def test_derived_list_shares_the_tier_routing_source(pristine):
    """The emission's list and the generated tier-routing block route the
    same files — one source, so a handoff derived from either cannot be
    short against the other."""
    from markdownllm.domain_kernel import routed_prompts, routed_skills
    agents = (pristine / "AGENTS.md").read_text(encoding="utf-8")
    for skill in routed_skills(pristine):
        assert f"`skills/{skill}`" in agents
    for prompt in routed_prompts(pristine):
        assert f"`prompts/{prompt}`" in agents
    assert routed_skills(pristine), "scaffold delivers skills"
    assert routed_prompts(pristine), "scaffold delivers prompts"


# ------------------------------------------------------------------ bounds

def test_emission_is_bounded_with_marked_elision(mutable, capsys):
    agents = mutable / "AGENTS.md"
    original = agents.read_text(encoding="utf-8")
    agents.write_text(original + "\nX" * (CONTRACT_SECTION_CHARACTERS * 2),
                      encoding="utf-8")

    assert mdllm.cmd_session_start(
        _ns(path=str(mutable), contract=True)) == 0
    out = capsys.readouterr().out
    assert "[contract elided:" in out
    assert "read `AGENTS.md` in full" in out
    # The bound is real: the emitted entry-file section cannot exceed the
    # section budget plus its marker.
    entry_section = out.split("## The entry file — `AGENTS.md`")[1] \
                       .split("## Derived reading list")[0]
    assert len(entry_section) < CONTRACT_SECTION_CHARACTERS + 400


def test_missing_kernel_is_stated_not_papered_over(tmp_path):
    # A bare directory outside any framework: entry file missing too. The
    # emitter degrades to honest MISSING sections rather than crashing —
    # a bootstrap must be able to show a broken position truthfully.
    lines = _emit_contract(tmp_path)
    text = "\n".join(lines)
    assert "## The entry file — MISSING" in text
    assert "nothing governs this position" in text


# ----------------------------------------------------------- root position

def test_framework_root_position_emits_root_contract():
    lines = _emit_contract(FW_ROOT)
    text = "\n".join(lines)
    assert "Framework Operative Kernel" in text
    # The root's AGENTS.md is the entry file at this position.
    root_agents = (FW_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert root_agents[:200] in text


# -------------------------------------------------------------- attestation

def _attest(domain: Path) -> str:
    gd = subprocess.run(["git", "rev-parse", "--git-dir"], cwd=domain,
                        capture_output=True, text=True).stdout.strip()
    return ((domain / gd).resolve() / "mdllm-attest").read_text(
        encoding="utf-8")


def test_attestation_marks_real_emission_and_gate_accepts_both(
        mutable, capsys):
    # Plain ritual: two tokens, no contract mark.
    assert mdllm.cmd_session_start(_ns(path=str(mutable))) == 0
    capsys.readouterr()
    plain = _attest(mutable).strip()
    assert not plain.endswith(" contract")

    # Emission: third token records that the contract content went out.
    assert mdllm.cmd_session_start(
        _ns(path=str(mutable), contract=True)) == 0
    capsys.readouterr()
    emitted = _attest(mutable).strip()
    assert emitted.endswith(" contract")

    # The scaffolded domain declares session_gate: strict; the gate reads
    # token 0 only, so both attestation forms clear it.
    assert mdllm.cmd_validate(_ns(path=str(mutable), quiet=True)) == 0
    capsys.readouterr()
