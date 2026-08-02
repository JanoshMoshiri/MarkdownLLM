"""Self-tests for the deterministic calculation floor (calc.py).

These pin the properties the whole point rests on: Decimal never float, no
silent default, no `eval`, report-never-write. A regression here does not
produce a wrong report — it produces a wrong *money figure* in a filed
return, which is why this file is held to the same standard as validation.

Run: python -m pytest tools/tests -q
"""

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mdllm  # noqa: E402
import pytest  # noqa: E402

from test_mdllm import _ns, thing_text, write  # noqa: E402


def ctx(meta=None, body="", corpus=None):
    return mdllm.Context(meta=meta or {}, body=body, corpus=corpus)


def ev(expr, meta=None, body="", corpus=None):
    return mdllm.evaluate_expression(expr, ctx(meta, body, corpus))


# ---------------------------------------------------------------- numbers


def test_money_text_parses_to_exact_decimal():
    # Currency symbols, thousands separators and the accounting parenthesis
    # for negatives are how money actually arrives from a bank export.
    assert mdllm.to_decimal("£1,200.00") == Decimal("1200.00")
    assert mdllm.to_decimal("(45.60)") == Decimal("-45.60")
    assert mdllm.to_decimal("-£8.50") == Decimal("-8.50")
    assert mdllm.to_decimal(" 84 ") == Decimal(84)


def test_floats_route_through_str_not_binary():
    # A YAML `16.80` arrives as a float. Decimal(float) would give
    # 16.8000000000000007105427357601... — the classic money bug.
    assert mdllm.to_decimal(16.80) == Decimal("16.8")
    assert str(mdllm.to_decimal(0.1) + mdllm.to_decimal(0.2)) == "0.3"


def test_non_numbers_raise_rather_than_default_to_zero():
    for bad in ("", "-", "n/a", None, True, [1]):
        with pytest.raises(mdllm.CalcError):
            mdllm.to_decimal(bad)


def test_decimal_equality_is_numeric_not_textual():
    assert mdllm.values_equal(Decimal("16.80"), 16.8)
    assert not mdllm.values_equal(Decimal("16.80"), 16.81)


# ---------------------------------------------------------------- resolution


def test_dotted_path_reaches_nested_scalar():
    meta = {"boxes": {"box4": 16.80}}
    assert ev("boxes.box4", meta) == Decimal("16.8")


def test_path_through_a_list_of_mappings_yields_a_column():
    meta = {"purchases": [{"net": 69.00, "vat": 13.80},
                          {"net": 15.00, "vat": 3.00}]}
    col = ev("purchases.vat", meta)
    assert isinstance(col, mdllm.Column) and len(col) == 2
    assert ev("sum(purchases.vat)", meta) == Decimal("16.80")
    assert ev("sum(purchases.net)", meta) == Decimal("84.00")


def test_unknown_reference_names_itself_and_never_defaults():
    with pytest.raises(mdllm.CalcError) as e:
        ev("sum(nowhere.vat)", {"purchases": []})
    assert "unknown reference `nowhere`" in str(e.value)


def test_partially_present_key_is_an_error_not_a_smaller_denominator():
    # The silent-shrink bug: one row missing `vat` would quietly change what
    # `sum(purchases.vat)` means. It must refuse instead.
    meta = {"purchases": [{"net": 10, "vat": 2}, {"net": 5}]}
    with pytest.raises(mdllm.CalcError) as e:
        ev("sum(purchases.vat)", meta)
    assert "missing `vat` in 1 of 2" in str(e.value)


# ---------------------------------------------------------------- arithmetic


def test_operators_and_precedence():
    meta = {"a": 10, "b": 4, "c": 2}
    assert ev("a - b - c", meta) == Decimal(4)
    assert ev("a - b * c", meta) == Decimal(2)
    assert ev("(a - b) * c", meta) == Decimal(12)
    assert ev("-a + b", meta) == Decimal(-6)
    assert ev("a / b", meta) == Decimal("2.5")


def test_aggregates_over_a_column():
    meta = {"rows": [{"x": 1}, {"x": 2}, {"x": 6}]}
    assert ev("count(rows.x)", meta) == Decimal(3)
    assert ev("min(rows.x)", meta) == Decimal(1)
    assert ev("max(rows.x)", meta) == Decimal(6)
    assert ev("avg(rows.x)", meta) == Decimal(3)
    assert ev("abs(0 - total)", {"total": 12.5}) == Decimal("12.5")


def test_scale_is_presentation_and_round_is_where_a_domain_declares_it():
    # YAML has already dropped the trailing zero of `10.00` before the floor
    # sees it, so a sum prints 15.5. Comparison is numeric, so nothing turns
    # on it; a domain wanting 2dp says so in the expression.
    meta = {"rows": [{"x": 10.00}, {"x": 5.50}]}
    assert mdllm.fmt(ev("sum(rows.x)", meta)) == "15.5"
    assert mdllm.fmt(ev("round(sum(rows.x), 2)", meta)) == "15.50"


def test_round_is_half_up_not_bankers():
    # Python's round(2.5) == 2. Money does not work that way, and an operator
    # reproducing the figure by hand would get 3.
    assert ev("round(2.5)", {}) == Decimal(3)
    assert ev("round(1.005, 2)", {}) == Decimal("1.01")
    assert ev("round(16.8055, 2)", {}) == Decimal("16.81")


def test_division_by_zero_is_reported_not_raised_as_python():
    with pytest.raises(mdllm.CalcError) as e:
        ev("10 / 0", {})
    assert "division by zero" in str(e.value)


# ---------------------------------------------------------------- the sandbox


def test_no_eval_no_builtins_no_imports_no_attributes_of_objects():
    # The whitelist walk is the security property. Each of these is a distinct
    # escape route a naive eval() would hand over.
    for hostile in (
        "__import__('os').system('echo pwned')",
        "open('/etc/passwd').read()",
        "(1).__class__",
        "[x for x in (1, 2)]",
        "lambda: 1",
        "1 if True else 2",
        "2 ** 64",
        "'a' * 99999999",
    ):
        with pytest.raises(mdllm.CalcError):
            ev(hostile, {})


def test_unknown_function_lists_the_available_ones():
    with pytest.raises(mdllm.CalcError) as e:
        ev("median(rows.x)", {"rows": [{"x": 1}]})
    assert "unknown function `median()`" in str(e.value)
    assert "sum" in str(e.value)


def test_unparseable_expression_says_so():
    with pytest.raises(mdllm.CalcError) as e:
        ev("sum(rows.x", {"rows": []})
    assert "cannot parse" in str(e.value)


# ---------------------------------------------------------------- the block


def test_evaluate_block_compares_against_the_asserted_sibling():
    meta = {
        "boxes": {"box3": 0.00, "box4": 16.80, "box5": -16.80, "box7": 84},
        "purchases": [{"net": 69.00, "vat": 13.80}, {"net": 15.00, "vat": 3.00}],
        "computed": {
            "boxes.box4": "sum(purchases.vat)",
            "boxes.box7": "sum(purchases.net)",
            "boxes.box5": "boxes.box3 - boxes.box4",
        },
    }
    ds = {d.target: d for d in mdllm.evaluate_block(meta, ctx(meta))}
    assert all(d.agrees for d in ds.values()), {k: (v.value, v.asserted) for k, v in ds.items()}


def test_evaluate_block_catches_the_drifted_total():
    # A line item was added and the total was not updated — the actual failure
    # mode, and the one an asserted figure can never surface on its own.
    meta = {"total": 69.00,
            "rows": [{"net": 69.00}, {"net": 15.00}],
            "computed": {"total": "sum(rows.net)"}}
    d = mdllm.evaluate_block(meta, ctx(meta))[0]
    assert d.agrees is False
    assert d.value == Decimal("84.00") and d.asserted == 69.00


def test_one_bad_line_does_not_take_the_others_results_away():
    meta = {"a": 3, "rows": [{"x": 1}, {"x": 2}],
            "computed": {"a": "sum(rows.x)", "b": "sum(nowhere.x)"}}
    ds = mdllm.evaluate_block(meta, ctx(meta))
    assert len(ds) == 2
    assert ds[0].agrees is True
    assert ds[1].error and ds[1].agrees is None


def test_a_derivation_resolving_to_a_set_says_to_aggregate_it():
    meta = {"rows": [{"x": 1}, {"x": 2}], "computed": {"total": "rows.x"}}
    d = mdllm.evaluate_block(meta, ctx(meta))[0]
    assert "not a single figure" in d.error and "sum()" in d.error


def test_a_derivation_with_no_asserted_value_is_legitimate_not_a_failure():
    meta = {"rows": [{"x": 1}], "computed": {"total": "sum(rows.x)"}}
    d = mdllm.evaluate_block(meta, ctx(meta))[0]
    assert d.asserted_found is False and d.agrees is None and d.error is None


def test_no_computed_block_means_no_derivations():
    assert mdllm.evaluate_block({"total": 5}, ctx({"total": 5})) == []


# ---------------------------------------------------------------- quarantine


def test_quarantine_state_is_read_from_provenance_fields():
    assert mdllm.is_quarantined({"origin": "external", "verified": False})
    assert mdllm.is_quarantined({"origin": "external"})
    assert not mdllm.is_quarantined({"origin": "external", "verified": True})
    assert not mdllm.is_quarantined({"origin": "stated"})


# ---------------------------------------------------------------- the command


def test_calc_reports_a_disagreement_and_exits_1(tmp_path, capsys):
    write(tmp_path, "things/vat.md", thing_text(
        "id: vat-return\ntype: note\nstatus: in-progress\ncreated: 2026-08-02\n"
        "total: 69.00\n"
        "purchases:\n  - net: 69.00\n  - net: 15.00\n"
        "computed:\n  total: \"sum(purchases.net)\""))
    rc = mdllm.cmd_calc(_ns(path=str(tmp_path), thing=None, expr=None))
    out = capsys.readouterr().out
    assert rc == 1
    assert "DISAGREES" in out and "computed 84" in out
    assert "1 disagreement(s)" in out


def test_calc_is_quiet_and_clean_when_the_corpus_agrees(tmp_path, capsys):
    write(tmp_path, "things/vat.md", thing_text(
        "id: vat-return\ntype: note\nstatus: in-progress\ncreated: 2026-08-02\n"
        "total: 84.00\n"
        "purchases:\n  - net: 69.00\n  - net: 15.00\n"
        "computed:\n  total: \"sum(purchases.net)\""))
    rc = mdllm.cmd_calc(_ns(path=str(tmp_path), thing=None, expr=None))
    out = capsys.readouterr().out
    assert rc == 0
    assert "agrees" in out and "DISAGREES" not in out


def test_calc_stamps_a_quarantined_thing(tmp_path, capsys):
    write(tmp_path, "things/stmt.md", thing_text(
        "id: statement-jan\ntype: note\nstatus: in-progress\ncreated: 2026-08-02\n"
        "origin: external\nverified: false\n"
        "rows:\n  - amount: 10.00\n  - amount: 5.50\n"
        "computed:\n  total: \"sum(rows.amount)\""))
    rc = mdllm.cmd_calc(_ns(path=str(tmp_path), thing="statement-jan", expr=None))
    out = capsys.readouterr().out
    assert rc == 0
    assert "UNVERIFIED" in out and "provisional" in out
    assert "computed 15.5" in out


def test_calc_expr_without_a_thing_is_pure_arithmetic(capsys):
    rc = mdllm.cmd_calc(_ns(path=".", thing=None, expr="round(1200.00 * 0.2, 2)"))
    assert rc == 0 and capsys.readouterr().out.strip() == "240.00"


def test_calc_expr_in_a_things_context_is_the_pivot(tmp_path, capsys):
    write(tmp_path, "things/stmt.md", thing_text(
        "id: statement-jan\ntype: note\nstatus: in-progress\ncreated: 2026-08-02\n"
        "rows:\n  - amount: 10.00\n  - amount: 5.50\n"))
    rc = mdllm.cmd_calc(_ns(path=str(tmp_path), thing="statement-jan",
                            expr="sum(rows.amount)"))
    assert rc == 0 and capsys.readouterr().out.strip() == "15.5"


def test_calc_on_an_empty_corpus_explains_rather_than_reporting_nothing(tmp_path, capsys):
    write(tmp_path, "things/plain.md", thing_text(
        "id: plain\ntype: note\nstatus: in-progress\ncreated: 2026-08-02"))
    rc = mdllm.cmd_calc(_ns(path=str(tmp_path), thing=None, expr=None))
    out = capsys.readouterr().out
    assert rc == 0 and "No thing declares a `computed:` block" in out


def test_calc_names_a_missing_thing(tmp_path, capsys):
    rc = mdllm.cmd_calc(_ns(path=str(tmp_path), thing="ghost", expr=None))
    assert rc == 1 and "no thing with id `ghost`" in capsys.readouterr().out
