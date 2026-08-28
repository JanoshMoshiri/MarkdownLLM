"""Self-tests for the operating-layer vocabulary check (coherence, domain scope).

The check reads the skills and the entry file against the schema they claim to
describe, and names any type, status, or frontmatter field the corpus never
declared. It must fire on undeclared vocabulary, stay silent on declared and
on framework-reserved vocabulary, and stay silent where the corpus declares no
authority at all — "could not look" is not "nothing wrong".

The fixtures below are the shapes the 2026-08-28 hand-found defects wore:
a `### \\`type: x\\`` heading, a fenced frontmatter template, a
`- \\`status\\` — \\`a\\` | \\`b\\`` vocabulary line, and a **Key fields:** list.

Run: python -m pytest tools/tests/test_skill_vocabulary.py -q
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mdllm  # noqa: E402

from corpus_harness import thing_text, write  # noqa: E402

SCHEMA = """\
schema_version: 1
domain: dom
types:
  invoice:
    statuses: [open, filed]
  supplier:
    statuses: [approved, retired]
    required_fields: [supplier_ref]
known_fields:
  - net_amount
  - name
"""

SCHEMA_NO_FIELDS = "\n".join(
    line for line in SCHEMA.splitlines()
    if line not in ("known_fields:", "  - net_amount", "  - name"))


def _domain(tmp_path, body, *, schema=SCHEMA, status="draft",
            rel="skills/dom-write.thing.skill.md", typ="skill",
            entry="# Dom\n\nAuthored entry file.\n"):
    write(tmp_path, "AGENTS.md", entry)
    if schema is not None:
        write(tmp_path, "things/_schema.yaml", schema)
    write(tmp_path, rel, thing_text(
        f"id: dom-write-thing-skill\ntype: {typ}\nstatus: {status}\n"
        f"name: Dom Write\ncreated: 2026-06-01\n", body))
    return tmp_path


def _vocab(root):
    return [f for f in mdllm.coherence_findings(root, 15)
            if "instructs" in f.message]


def _messages(root):
    return [f.message for f in _vocab(root)]


# ----------------------------------------------------------------- it fires


def test_undeclared_type_in_a_heading_fires(tmp_path):
    _domain(tmp_path, "# Write\n\n### `type: purchase-order`\n\nA thing.\n")
    assert any("`purchase-order`" in m and "thing type" in m
               for m in _messages(tmp_path))


def test_undeclared_type_in_a_frontmatter_template_fires(tmp_path):
    _domain(tmp_path, """\
# Write

### Creating a thing

```yaml
---
id: po-[slug]
type: purchase-order
status: open
created: [ISO-date]
---
```
""")
    assert any("`purchase-order`" in m for m in _messages(tmp_path))


def test_undeclared_type_in_a_numbered_step_fires(tmp_path):
    # The workflow-skill shape: an imperative step mid-sentence.
    _domain(tmp_path, "# Write\n\n1. Create a `type: purchase-order` thing\n")
    assert any("`purchase-order`" in m for m in _messages(tmp_path))


def test_status_outside_the_declared_vocabulary_fires(tmp_path):
    _domain(tmp_path, """\
# Write

### `type: invoice`

**Key fields:**
- `status` — `open` | `disputed` | `filed`
""")
    msgs = _messages(tmp_path)
    assert any("`disputed`" in m and "type `invoice`" in m for m in msgs)
    assert not any("`open`" in m or "`filed`" in m for m in msgs)


def test_status_in_a_frontmatter_template_is_scoped_to_its_own_type(tmp_path):
    _domain(tmp_path, """\
# Write

```yaml
---
id: inv-1
type: invoice
status: reconciled
created: 2026-06-01
---
```
""")
    assert any("`reconciled`" in m and "type `invoice`" in m
               for m in _messages(tmp_path))


def test_unregistered_field_in_a_key_fields_list_fires(tmp_path):
    _domain(tmp_path, """\
# Write

### `type: invoice`

**Key fields:**
- `net_amount` — the sum excluding tax
- `output_vat`, `input_vat` — the tax legs
""")
    msgs = _messages(tmp_path)
    assert any("`output_vat`" in m and "`input_vat`" in m
               and "registered nowhere" in m for m in msgs)
    assert not any("`net_amount`" in m for m in msgs)


def test_unregistered_field_in_a_frontmatter_template_fires(tmp_path):
    _domain(tmp_path, """\
# Write

```yaml
---
id: inv-1
type: invoice
status: open
created: 2026-06-01
net_amount: 10.00
receipt_reference: R-1
---
```
""")
    msgs = _messages(tmp_path)
    assert any("`receipt_reference`" in m for m in msgs)
    assert not any("`net_amount`" in m or "`created`" in m for m in msgs)


def test_the_entry_file_is_read_too(tmp_path):
    _domain(tmp_path, "# Write\n\nNothing to see.\n",
            entry="# Dom\n\n## Thing Types\n\n- `type: purchase-order` — a PO\n")
    assert any(f.thing == "AGENTS.md" and "`purchase-order`" in f.message
               for f in _vocab(tmp_path))


def test_a_specification_typed_skill_file_is_in_the_population(tmp_path):
    # The archetype: the estate's *specification* skills carry
    # `type: specification`, and two of the 2026-08-28 defects lived in one.
    _domain(tmp_path, "# Spec\n\n### `type: purchase-order`\n",
            rel="skills/dom-specification.skill.md", typ="specification",
            status="evolving")
    assert any("`purchase-order`" in m for m in _messages(tmp_path))


def test_a_draft_skill_is_in_the_population(tmp_path):
    # The archetype instance was `draft` while being read daily; a draft skill
    # is loaded at session start like any other.
    _domain(tmp_path, "# Write\n\n### `type: purchase-order`\n", status="draft")
    assert _messages(tmp_path)


def test_findings_are_warnings(tmp_path):
    _domain(tmp_path, "# Write\n\n### `type: purchase-order`\n")
    assert all(f.severity == mdllm.SEV_WARNING for f in _vocab(tmp_path))


# ---------------------------------------------------------------- it is quiet

DECLARED_BODY = """\
# Write

### `type: supplier`

**Key fields:**
- `supplier_ref` — required by the schema, so admitted by being required
- `name` — registered in known_fields
- `status` — `approved` | `retired`

```yaml
---
id: sup-1
type: supplier
status: approved
created: 2026-06-01
supplier_ref: S-1
---
```
"""


def test_the_quiet_fixture_is_actually_read(tmp_path):
    # Null-result discipline applied to the suite itself: "quiet" below must
    # mean "read it and it was clean", never "extracted nothing".
    uses = mdllm.vocabulary_uses(DECLARED_BODY)
    assert {u.kind for u in uses} == {"type", "status", "field"}


def test_declared_vocabulary_is_quiet(tmp_path):
    _domain(tmp_path, DECLARED_BODY)
    assert _messages(tmp_path) == []


def test_framework_reserved_vocabulary_is_quiet(tmp_path):
    _domain(tmp_path, """\
# Write

### `type: insight`

**Key fields:**
- `status` — `active` | `promoted` | `dismissed`
- `disposition`, `disposition_reason` — CORE_FIELDS, owned by the tool

```yaml
---
id: an-insight
type: insight
status: promoted
created: 2026-06-01
---
```
""")
    assert _messages(tmp_path) == []


def test_no_schema_is_quiet(tmp_path):
    _domain(tmp_path, "# Write\n\n### `type: purchase-order`\n\n"
                      "**Key fields:**\n- `output_vat` — a field\n",
            schema=None)
    assert _messages(tmp_path) == []


def test_field_leg_is_silent_without_known_fields(tmp_path):
    # Field registration is opt-in; a domain that never registered has no
    # authority to key to, so the field leg must not invent one.
    _domain(tmp_path, "# Write\n\n### `type: invoice`\n\n"
                      "**Key fields:**\n- `output_vat` — a field\n",
            schema=SCHEMA_NO_FIELDS)
    msgs = _messages(tmp_path)
    assert not any("registered nowhere" in m for m in msgs)


def test_a_parenthetical_illustration_is_quiet(tmp_path):
    _domain(tmp_path, "# Write\n\n- **Emergent schema** — new types "
                      "(e.g., `type: migration-plan`) emerge from real need.\n")
    assert _messages(tmp_path) == []


def test_inline_prose_outside_a_declaration_position_is_quiet(tmp_path):
    _domain(tmp_path, "# Write\n\nA paragraph mentioning `type: migration-plan` "
                      "in passing is writing about a type, not instructing "
                      "one.\n")
    assert _messages(tmp_path) == []


def test_a_deprecated_skill_is_out_of_the_population(tmp_path):
    # Its instructions are withdrawn; rewriting a retired file is not a
    # remedy anyone would perform.
    _domain(tmp_path, "# Write\n\n### `type: purchase-order`\n",
            status="deprecated")
    assert _messages(tmp_path) == []


def test_generated_blocks_are_not_read(tmp_path):
    # A finding inside a generator's output names a remedy the operator
    # cannot perform.
    _domain(tmp_path, "# Write\n\nNothing.\n", entry="""\
# Dom

<!-- generated:types -->
- `type: purchase-order` — rendered by the generator, not by the author
<!-- /generated:types -->
""")
    assert _messages(tmp_path) == []


def test_a_yaml_block_without_frontmatter_delimiters_is_not_read(tmp_path):
    # A bindings example is YAML, but its keys are not frontmatter.
    _domain(tmp_path, """\
# Write

```yaml
bindings:
  - hook: retrospective
    invoke: [review-skill-coherence]
```
""")
    assert _messages(tmp_path) == []


def test_placeholder_values_are_not_read_as_vocabulary(tmp_path):
    _domain(tmp_path, """\
# Write

```yaml
---
id: [slug]
type: [thing type]
status: [status]
created: [ISO-date]
---
```
""")
    assert _messages(tmp_path) == []


# ------------------------------------------------------- extraction precision


def test_status_alternatives_stop_at_prose():
    uses = mdllm.vocabulary_uses("""\
### `type: filing-deadline`

- `status` — `upcoming` | `met` | `missed`. **Exactly three.** The urgency
  bands the lens reports — `approaching`, `imminent` — are computed.
""")
    statuses = {u.value for u in uses if u.kind == "status"}
    assert statuses == {"upcoming", "met", "missed"}


def test_status_alternatives_survive_a_parenthetical_gloss():
    uses = mdllm.vocabulary_uses("""\
### `type: filing-deadline`

- `status` — `upcoming` | `approaching` (<=30 days) | `imminent` (<=7 days) | `met`
""")
    statuses = {u.value for u in uses if u.kind == "status"}
    assert statuses == {"upcoming", "approaching", "imminent", "met"}


def test_field_extraction_takes_only_the_leading_run():
    uses = mdllm.vocabulary_uses("""\
**Key fields:**
- `boxes` — the nine boxes (`box1_vat_on_sales` through `box9_acquisitions`)
""")
    fields = {u.value for u in uses if u.kind == "field"}
    assert fields == {"boxes"}


def test_a_fields_list_ends_at_the_next_paragraph():
    uses = mdllm.vocabulary_uses("""\
**Key fields:**
- `net_amount` — the sum

Prose that ends the list.

- `not_a_field` — a bullet in some later list
""")
    fields = {u.value for u in uses if u.kind == "field"}
    assert fields == {"net_amount"}
