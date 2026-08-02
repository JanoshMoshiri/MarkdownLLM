"""Deterministic calculation — the floor does every sum.

The framework's division of labour is that mechanical work belongs to the
floor and never to reasoning (`validate.thing.md`). Arithmetic is the most
mechanical work there is, and it was the one mechanical class the floor had
no answer for: a total in a thing's frontmatter was *asserted* by an agent,
not computed, and nothing could ever re-check it.

The primitive is not "maths" — Python has maths. It is the **declared
derivation**: a figure that states, in the thing, how it was reached.

    boxes:
      box4_vat_reclaimed: 16.80          # the assertion
    computed:
      boxes.box4_vat_reclaimed: "sum(purchases_breakdown.vat)"   # the derivation

Two surfaces over one evaluator, the same shape `triggers` has — declared in
the thing, evaluated by the floor:

  * `mdllm calc` computes on demand (the ingestion workflow's surface: the
    tool sums, the agent transcribes);
  * `validate` re-evaluates every declared derivation and reports where an
    assertion and its own derivation disagree (the surface that makes the
    first one durable).

Properties this module holds to, all of them load-bearing:

  * **Report, never write.** `calc` prints; it never edits frontmatter. Same
    posture as `touchpoints` and `cascade`.
  * **Decimal, never float.** Values parse from source text straight to
    `Decimal`. Binary floating point never touches a money figure.
  * **No implicit tolerance.** Computed and asserted compare exactly. Anything
    needing rounding declares `round(x, 2)` — with ROUND_HALF_UP, the money
    convention, not Python's banker's rounding.
  * **Scale is presentation, and stays the domain's to declare.** YAML parses
    `10.00` as a float, so trailing zeros are already gone before the floor
    sees the figure; a sum prints `15.5`, not `15.50`. Comparison is numeric,
    so nothing turns on it — and a domain that wants two decimal places says
    `round(x, 2)`, which is the same place it would say so anyway. The floor
    does not guess that a number is money.
  * **No silent default.** An unresolvable reference or unparseable expression
    raises `CalcError` with a reason, which the callers report. Nothing
    coerces a missing value to zero.
  * **No `eval`.** Expressions are parsed with `ast` and walked node by node
    against a whitelist. There is no name lookup outside the thing itself.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, getcontext

getcontext().prec = 28

# Money text as it actually arrives: currency symbols, thousands separators,
# and the accounting convention of parentheses for negatives.
_STRIP = str.maketrans("", "", "£$€,    ")


class CalcError(Exception):
    """An expression could not be evaluated, with the reason in the message.

    Never swallowed and never defaulted: every caller reports the reason
    verbatim. A calculation that cannot be performed must say so — a zero
    standing in for "I could not tell" is the failure this whole module
    exists to end.
    """


@dataclass
class Column:
    """An ordered set of values drawn from one source — a frontmatter list, a
    table column, a field across many things. Aggregates take these; scalars
    do not. `source` names where it came from, for error messages that point
    at the corpus rather than at the expression.

    `owner`/`row_ids` are set when the column came from a table, so a filter
    can evaluate a predicate against the *other* columns of the same rows.
    """
    values: list
    source: str
    owner: object | None = None
    row_ids: list | None = None

    def __len__(self) -> int:
        return len(self.values)


# ---------------------------------------------------------------- numbers


def to_decimal(v, where: str = "value") -> Decimal:
    """Coerce one source value to Decimal, or raise with the offending value.

    Floats are routed through `str` so that a YAML `16.80` becomes exactly
    `Decimal("16.8")` rather than the binary expansion. Text is stripped of
    currency symbols and separators; parentheses mean negative (accounting
    convention, and how most bank exports render debits).
    """
    if isinstance(v, Decimal):
        return v
    if isinstance(v, bool):  # bool is an int subclass; never a money figure
        raise CalcError(f"{where}: boolean {v!r} is not a number")
    if isinstance(v, int):
        return Decimal(v)
    if isinstance(v, float):
        return Decimal(str(v))
    if isinstance(v, str):
        s = v.strip().translate(_STRIP)
        neg = s.startswith("(") and s.endswith(")")
        if neg:
            s = s[1:-1]
        if s in ("", "-", "—", "–"):
            raise CalcError(f"{where}: {v!r} is blank, not a number")
        try:
            d = Decimal(s)
        except InvalidOperation:
            raise CalcError(f"{where}: {v!r} is not a number") from None
        return -d if neg else d
    raise CalcError(f"{where}: {type(v).__name__} {v!r} is not a number")


def fmt(v) -> str:
    """Render a Decimal for humans without exponent notation or lost scale."""
    if isinstance(v, Decimal):
        return f"{v:f}"
    return str(v)


def values_equal(a, b) -> bool:
    """Exact numeric equality between a computed and an asserted figure.

    Decimal comparison is numeric, not textual, so `16.80` and `16.8` agree
    while `16.80` and `16.81` do not. Non-numeric assertions fall back to
    string comparison so a computed text value can still be checked.
    """
    try:
        return to_decimal(a) == to_decimal(b)
    except CalcError:
        return str(a).strip() == str(b).strip()


# ---------------------------------------------------------------- context


@dataclass
class Context:
    """What an expression may see: this thing's frontmatter, and (later
    phases) its body and the corpus around it. Nothing else is reachable —
    there is no builtins namespace, no filesystem, no import."""
    meta: dict
    body: str = ""
    corpus: object | None = None
    thing_id: str = "?"
    notes: list = None  # type: ignore[assignment]

    def __post_init__(self):
        if self.notes is None:
            self.notes = []


def resolve_path(meta: dict, path: str):
    """Resolve a dotted path through frontmatter to a scalar or a Column.

    `boxes.box4_vat_reclaimed` walks nested mappings to a scalar.
    `purchases_breakdown.vat` walks *into a list of mappings* and yields the
    column of `vat` values — the single most common shape a derivation needs,
    and the reason a plain `dict.get` chain is not enough.
    """
    parts = path.split(".")
    cur = meta
    walked: list[str] = []
    for part in parts:
        walked.append(part)
        if isinstance(cur, dict):
            if part not in cur:
                raise CalcError(f"unknown reference `{'.'.join(walked)}`")
            cur = cur[part]
        elif isinstance(cur, list):
            # A list of mappings + a key = that key's column across the list.
            out, missing = [], 0
            for row in cur:
                if isinstance(row, dict) and part in row:
                    out.append(row[part])
                else:
                    missing += 1
            if not out:
                raise CalcError(
                    f"`{'.'.join(walked[:-1])}` has no `{part}` in any entry")
            if missing:
                # Reported, never silent: a partially-present key changes the
                # denominator of every aggregate over it.
                raise CalcError(
                    f"`{'.'.join(walked[:-1])}` is missing `{part}` in "
                    f"{missing} of {len(cur)} entries")
            cur = Column(out, ".".join(walked))
        elif isinstance(cur, Column):
            raise CalcError(f"cannot index into the column `{cur.source}`")
        else:
            raise CalcError(
                f"`{'.'.join(walked[:-1])}` is a value, not a mapping — "
                f"nothing to read `{part}` from")
    return cur


# ---------------------------------------------------------------- tables


@dataclass
class Table:
    """One markdown table from a thing's body.

    Line-item detail belongs in the body, not in frontmatter and not as one
    thing per row — a transaction has one identity and *zero* reasons to
    change, so it is data, not a thing. That ruling is only safe if the floor
    can do arithmetic over the body, which is what this is.
    """
    headers: list
    rows: list
    heading: str
    index: int

    @property
    def source(self) -> str:
        return f'table {self.index}' + (f' ("{self.heading}")' if self.heading else "")

    def header_index(self, name: str) -> int:
        """Match a column name to a header, tolerantly but never ambiguously.

        Exact first, then case-insensitively, then ignoring everything that is
        not alphanumeric — so `.Amount` reaches a header written `Amount (£)`
        without the expression having to carry a currency symbol. Two matches
        is an error, not a guess: picking one silently is how the wrong column
        gets summed.
        """
        def norm(s):
            return "".join(ch for ch in str(s).lower() if ch.isalnum())
        for candidates in (
            [i for i, h in enumerate(self.headers) if h == name],
            [i for i, h in enumerate(self.headers) if h.lower() == str(name).lower()],
            [i for i, h in enumerate(self.headers) if norm(h) == norm(name)],
        ):
            if len(candidates) == 1:
                return candidates[0]
            if len(candidates) > 1:
                raise CalcError(
                    f"`{name}` matches {len(candidates)} columns of "
                    f"{self.source} — name it exactly")
        raise CalcError(
            f"{self.source} has no column `{name}` (columns: "
            f"{', '.join(repr(h) for h in self.headers)})")

    def column(self, name) -> Column:
        i = self.header_index(name)
        return Column([r[i] for r in self.rows],
                      f"{self.source}.{self.headers[i]}",
                      owner=self, row_ids=list(range(len(self.rows))))

    def cell(self, row_id: int, name):
        return self.rows[row_id][self.header_index(name)]


# Emphasis is presentation; a bolded total is still a number. Stripped at the
# edges only, so a value containing one of these is left intact.
_CELL_TRIM = "*_` "


def parse_tables(body: str) -> list:
    """Every markdown table in a body, in order, each tagged with the nearest
    preceding heading — which is how a derivation names one in prose terms
    (`table("Transactions")`) rather than by counting."""
    tables: list = []
    heading = ""
    lines = body.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
            i += 1
            continue
        if line.startswith("|") and i + 1 < len(lines):
            sep = lines[i + 1].strip()
            cells = _split_row(sep)
            if cells and all(set(c) <= set("-: ") and "-" in c for c in cells):
                headers = _split_row(line)
                rows = []
                j = i + 2
                while j < len(lines) and lines[j].strip().startswith("|"):
                    r = _split_row(lines[j])
                    # Pad or trim to the header width: a ragged row is the
                    # table's problem, and dropping it silently would change
                    # the denominator of every aggregate over it.
                    if len(r) < len(headers):
                        r = r + [""] * (len(headers) - len(r))
                    rows.append(r[:len(headers)])
                    j += 1
                tables.append(Table(headers, rows, heading, len(tables) + 1))
                i = j
                continue
        i += 1
    return tables


def _split_row(line: str) -> list:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip().strip(_CELL_TRIM).strip() for c in s.split("|")]


def find_table(ctx: Context, selector) -> Table:
    tables = parse_tables(ctx.body)
    if not tables:
        raise CalcError("this thing's body has no markdown table")
    if isinstance(selector, Decimal):
        n = int(selector)
        if n < 1 or n > len(tables):
            raise CalcError(
                f"table({n}) — this body has {len(tables)} table(s)")
        return tables[n - 1]
    want = str(selector).strip().lower()
    hits = [t for t in tables if want in t.heading.lower()]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        raise CalcError(
            f'no table under a heading matching "{selector}" (headings: '
            f'{", ".join(repr(t.heading) for t in tables)})')
    raise CalcError(
        f'"{selector}" matches {len(hits)} tables — use table(n) by position')


def set_path(meta: dict, path: str):
    """The asserted sibling of a derivation, or a sentinel when absent.

    Returns (found, value). A derivation with no asserted counterpart is
    legitimate — the figure lives only as its derivation — so absence is not
    an error here, it is a fact the caller reports differently.
    """
    cur = meta
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return False, None
        cur = cur[part]
    return True, cur


# ---------------------------------------------------------------- functions


def _column(arg, fname: str) -> Column:
    if isinstance(arg, Column):
        return arg
    raise CalcError(f"{fname}() takes a set of values, got a single value")


def _note(ctx: Context, fname: str, c: Column) -> None:
    """Record the denominator every aggregate ran over.

    A total says nothing about how many values went into it, and a filter that
    silently matched nothing produces a confident zero. The count travels with
    the figure so the operator sees `sum over 2 value(s)` rather than having
    to trust it.
    """
    ctx.notes.append(f"{fname} over {len(c)} value(s) from {c.source}")


def _fn_sum(ctx: Context, col) -> Decimal:
    c = _column(col, "sum")
    _note(ctx, "sum", c)
    total = Decimal(0)
    for i, v in enumerate(c.values):
        total += to_decimal(v, f"{c.source}[{i}]")
    return total


def _fn_count(ctx: Context, col) -> Decimal:
    c = _column(col, "count")
    _note(ctx, "count", c)
    return Decimal(len(c))


def _fn_avg(ctx: Context, col) -> Decimal:
    c = _column(col, "avg")
    if not c.values:
        raise CalcError("avg() over an empty set has no value")
    _note(ctx, "avg", c)
    total = Decimal(0)
    for i, v in enumerate(c.values):
        total += to_decimal(v, f"{c.source}[{i}]")
    return total / Decimal(len(c.values))


def _fn_min(ctx: Context, col) -> Decimal:
    c = _column(col, "min")
    if not c.values:
        raise CalcError("min() over an empty set has no value")
    _note(ctx, "min", c)
    return min(to_decimal(v, f"{c.source}[{i}]") for i, v in enumerate(c.values))


def _fn_max(ctx: Context, col) -> Decimal:
    c = _column(col, "max")
    if not c.values:
        raise CalcError("max() over an empty set has no value")
    _note(ctx, "max", c)
    return max(to_decimal(v, f"{c.source}[{i}]") for i, v in enumerate(c.values))


def _fn_abs(ctx: Context, v) -> Decimal:
    return abs(to_decimal(v))


def _fn_round(ctx: Context, v, places=None) -> Decimal:
    d = to_decimal(v)
    n = 0 if places is None else int(to_decimal(places))
    if n < 0:
        raise CalcError("round() places must be 0 or more")
    # ROUND_HALF_UP, not Python's banker's rounding: this is the convention
    # money is kept in, and a silent half-even would be a figure the operator
    # cannot reproduce by hand.
    return d.quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP)


FUNCTIONS = {
    "sum": _fn_sum, "count": _fn_count, "avg": _fn_avg,
    "min": _fn_min, "max": _fn_max, "abs": _fn_abs, "round": _fn_round,
}


# ---------------------------------------------------------------- evaluator


_BINOPS = {ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/"}


def evaluate_expression(expr: str, ctx: Context):
    """Evaluate one declared derivation against a thing's context.

    Parsed with `ast` and walked node by node against a whitelist — never
    `eval`. An expression cannot reach a builtin, an import, an attribute of a
    Python object, or anything outside the frontmatter (and, from Phase 2, the
    body and corpus) it is given.
    """
    if not isinstance(expr, str) or not expr.strip():
        raise CalcError("empty expression")
    try:
        tree = ast.parse(expr.strip(), mode="eval")
    except SyntaxError as e:
        raise CalcError(f"cannot parse: {e.msg}") from None
    return _eval_node(tree.body, ctx)


def _dotted(node: ast.AST) -> str | None:
    """Flatten a Name/Attribute chain to a dotted path, or None if the base is
    not a plain name (a `table(...)` call, say — a later phase's concern)."""
    parts: list[str] = []
    cur = node
    while isinstance(cur, ast.Attribute):
        parts.append(cur.attr)
        cur = cur.value
    if not isinstance(cur, ast.Name):
        return None
    parts.append(cur.id)
    return ".".join(reversed(parts))


def _eval_node(node: ast.AST, ctx: Context):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or node.value is None:
            raise CalcError(f"{node.value!r} is not a value an expression may use")
        if isinstance(node.value, (int, float)):
            return to_decimal(node.value)
        if isinstance(node.value, str):
            return node.value
        raise CalcError(f"unsupported literal {node.value!r}")

    if isinstance(node, (ast.Name, ast.Attribute)):
        path = _dotted(node)
        if path is None:
            # Not a frontmatter path — the base is an expression of its own,
            # e.g. `table("Transactions").Amount`.
            base = _eval_node(node.value, ctx)
            if isinstance(base, Table):
                return base.column(node.attr)
            raise CalcError(f"cannot read `{node.attr}` from that value")
        v = resolve_path(ctx.meta, path)
        # A numeric scalar becomes Decimal here, at the boundary, so no float
        # ever travels further into the evaluator. Text stays text (filters
        # compare against it); columns coerce per-element inside aggregates.
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            return to_decimal(v, path)
        return v

    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            return -to_decimal(_eval_node(node.operand, ctx))
        if isinstance(node.op, ast.UAdd):
            return to_decimal(_eval_node(node.operand, ctx))
        raise CalcError("unsupported unary operator")

    if isinstance(node, ast.BinOp):
        op = type(node.op)
        if op not in _BINOPS:
            raise CalcError(
                f"unsupported operator `{type(node.op).__name__}` "
                f"(the floor evaluates + - * / only)")
        left = to_decimal(_eval_node(node.left, ctx))
        right = to_decimal(_eval_node(node.right, ctx))
        if op is ast.Add:
            return left + right
        if op is ast.Sub:
            return left - right
        if op is ast.Mult:
            return left * right
        if right == 0:
            raise CalcError("division by zero")
        return left / right

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise CalcError("only the floor's own functions may be called")
        fname = node.func.id
        if node.keywords and fname not in ("things",):
            raise CalcError(f"{fname}() takes no keyword arguments")
        if fname == "table":
            args = [_eval_node(a, ctx) for a in node.args]
            if len(args) != 1:
                raise CalcError('table() takes one argument: a heading or a position')
            return find_table(ctx, args[0])
        if fname in FUNCTIONS:
            args = [_eval_node(a, ctx) for a in node.args]
            fn = FUNCTIONS[fname]
            try:
                return fn(ctx, *args)
            except TypeError:
                raise CalcError(f"{fname}() got {len(args)} argument(s)") from None
        raise CalcError(
            f"unknown function `{fname}()` "
            f"(available: {', '.join(sorted(FUNCTIONS))})")

    if isinstance(node, ast.Subscript):
        base = _eval_node(node.value, ctx)
        idx = node.slice
        # Two distinct meanings, told apart by the *shape* of the index and
        # never guessed: a string names a column, a comparison filters rows.
        if isinstance(base, Table):
            if isinstance(idx, ast.Constant) and isinstance(idx.value, str):
                return base.column(idx.value)
            raise CalcError('a table is subscripted by column name, e.g. '
                            'table("T")["Amount (£)"]')
        if isinstance(base, Column):
            if isinstance(idx, (ast.Compare, ast.BoolOp)):
                return _filter_column(base, idx, ctx)
            raise CalcError("a set of values is subscripted by a condition, "
                            'e.g. .Amount[Category == "Fuel"]')
        raise CalcError("only a table or a set of values can be subscripted")

    raise CalcError(f"unsupported expression element `{type(node).__name__}`")


# ---------------------------------------------------------------- filters


_CMPS = {ast.Eq: "==", ast.NotEq: "!=", ast.Lt: "<",
         ast.LtE: "<=", ast.Gt: ">", ast.GtE: ">="}


def _filter_column(col: Column, pred: ast.AST, ctx: Context) -> Column:
    """Keep the rows of a table column whose row satisfies a condition.

    The predicate reads the *other* columns of the same row, which is the
    whole point: `table("Transactions").Amount[Category == "Fuel"]` sums one
    column selected by another. Only a table column can be filtered — a
    frontmatter list has no sibling row to test.
    """
    if col.owner is None or col.row_ids is None:
        raise CalcError(f"`{col.source}` is not a table column, so there are "
                        f"no rows to filter")
    keep_vals, keep_ids = [], []
    for pos, rid in enumerate(col.row_ids):
        if _eval_pred(pred, col.owner, rid, ctx):
            keep_vals.append(col.values[pos])
            keep_ids.append(rid)
    return Column(keep_vals, f"{col.source} (filtered)",
                  owner=col.owner, row_ids=keep_ids)


def _eval_pred(node: ast.AST, table: Table, row_id: int, ctx: Context) -> bool:
    if isinstance(node, ast.BoolOp):
        results = [_eval_pred(v, table, row_id, ctx) for v in node.values]
        return all(results) if isinstance(node.op, ast.And) else any(results)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        return not _eval_pred(node.operand, table, row_id, ctx)
    if not isinstance(node, ast.Compare):
        raise CalcError("a filter is a comparison, optionally joined by and/or")
    if len(node.ops) != 1:
        raise CalcError("chained comparisons are not evaluated — join them "
                        "with `and` so each side is explicit")
    op = type(node.ops[0])
    if op not in _CMPS:
        raise CalcError(f"unsupported comparison `{type(node.ops[0]).__name__}`")
    left = _pred_operand(node.left, table, row_id, ctx)
    right = _pred_operand(node.comparators[0], table, row_id, ctx)
    return _compare(left, right, op, _CMPS[op])


def _pred_operand(node: ast.AST, table: Table, row_id: int, ctx: Context):
    """Inside a filter, a bare name is this row's cell in that column. Frontmatter
    is still reachable by dotted path, so a row can be compared against a
    figure the thing declares (`Amount > limits.large`)."""
    if isinstance(node, ast.Name):
        return table.cell(row_id, node.id)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, str):
            return node.value
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return to_decimal(node.value)
        raise CalcError(f"{node.value!r} cannot appear in a filter")
    return _eval_node(node, ctx)


def _compare(left, right, op, symbol: str) -> bool:
    try:
        ln, rn = to_decimal(left), to_decimal(right)
        numeric = True
    except CalcError:
        numeric = False
    if numeric:
        return {"==": ln == rn, "!=": ln != rn, "<": ln < rn,
                "<=": ln <= rn, ">": ln > rn, ">=": ln >= rn}[symbol]
    ls, rs = str(left).strip(), str(right).strip()
    if symbol in ("==", "!="):
        # Case-insensitive: a category typed `Fuel` in one row and `fuel` in
        # the next is the same category, and a filter that quietly disagreed
        # would under-count without ever saying so.
        eq = ls.casefold() == rs.casefold()
        return eq if symbol == "==" else not eq
    raise CalcError(f"cannot order text: {ls!r} {symbol} {rs!r}")


# ---------------------------------------------------------------- the block


@dataclass
class Derivation:
    """One evaluated line of a `computed:` block — everything a report or a
    validation finding needs, with the failure reason carried rather than
    raised, so one bad line never hides the rest."""
    target: str
    expr: str
    value: object = None
    error: str | None = None
    asserted_found: bool = False
    asserted: object = None
    notes: list = None  # type: ignore[assignment]

    def __post_init__(self):
        if self.notes is None:
            self.notes = []

    @property
    def agrees(self) -> bool | None:
        """True/False when there is something to compare, None when the
        derivation stands alone or could not be evaluated."""
        if self.error is not None or not self.asserted_found:
            return None
        return values_equal(self.value, self.asserted)


def evaluate_block(thing_meta: dict, ctx: Context) -> list[Derivation]:
    """Evaluate a thing's whole `computed:` block, in declaration order.

    Returns one `Derivation` per declared target whether it succeeded or not:
    a block is a set of independent claims, and one unparseable line must not
    take the others' results away from the operator.
    """
    block = thing_meta.get("computed")
    if not isinstance(block, dict):
        return []
    out: list[Derivation] = []
    for target, expr in block.items():
        d = Derivation(target=str(target), expr=str(expr) if expr is not None else "")
        ctx.notes.clear()  # each derivation reports its own denominators
        try:
            v = evaluate_expression(d.expr, ctx)
            if isinstance(v, Column):
                raise CalcError(
                    f"resolves to a set of {len(v)} values, not a single "
                    f"figure — wrap it in sum(), count(), min(), max() or avg()")
            d.value = v
        except CalcError as e:
            d.error = str(e)
        d.notes = list(ctx.notes)
        d.asserted_found, d.asserted = set_path(thing_meta, d.target)
        out.append(d)
    return out


def context_for(thing, corpus=None) -> Context:
    return Context(meta=thing.meta, body=thing.body, corpus=corpus,
                   thing_id=thing.id or thing.path.name)


def _report(thing, ctx: Context, derivations: list[Derivation]) -> tuple[int, int]:
    """Print one thing's derivations. Returns (disagreements, errors)."""
    name = thing.id or thing.path.name
    print(f"## {name}")
    if is_quarantined(thing.meta):
        print("   UNVERIFIED — origin: external, verified: false. These figures "
              "are provisional;\n   no decision or filing may rest on them until "
              "a human flips the quarantine.")
    bad = errs = 0
    for d in derivations:
        print(f"\n{d.target}")
        print(f"  = {d.expr}")
        if d.error is not None:
            print(f"  NOT EVALUABLE — {d.error}")
            errs += 1
            continue
        line = f"  computed {fmt(d.value)}"
        if d.asserted_found:
            if d.agrees:
                line += f"   asserted {fmt(d.asserted)}   agrees"
            else:
                line += f"   asserted {fmt(d.asserted)}   DISAGREES"
                bad += 1
        else:
            line += "   (no asserted value — the derivation stands alone)"
        print(line)
        for note in d.notes:
            print(f"    {note}")
    print()
    return bad, errs


def cmd_calc(args) -> int:
    """Compute declared derivations — the floor does every sum.

    Three modes, one evaluator:
      `calc <path>`                     every thing carrying a `computed:` block
      `calc <path> --thing ID`          one thing's block
      `calc <path> [--thing ID] --expr` an ad-hoc figure, in that thing's context
                                        (the pivot: "fuel spend this quarter")

    Reports, never writes: the figures print, and the agent transcribes what
    belongs in the thing. Exit 1 when a derivation disagrees with its asserted
    value or cannot be evaluated, so a pre-flight script can gate on it.
    """
    from pathlib import Path
    from .model import scan

    root = Path(args.path).resolve()

    # An expression with no thing named is pure arithmetic — useful on its own
    # ("what is 20% of this invoice?") and reachable without a corpus at all.
    if args.expr and not args.thing:
        try:
            print(fmt(evaluate_expression(args.expr, Context(meta={}))))
            return 0
        except CalcError as e:
            print(f"mdllm: cannot evaluate — {e}")
            return 1

    corpus, _ = scan(root)
    by_id = corpus.by_id()

    if args.thing:
        if args.thing not in by_id:
            print(f"mdllm: no thing with id `{args.thing}` in {root}")
            return 1
        thing = by_id[args.thing]
        ctx = context_for(thing, corpus)
        if args.expr:
            if is_quarantined(thing.meta):
                print(f"## {thing.id}  UNVERIFIED (origin: external, "
                      f"verified: false) — provisional figure")
            try:
                v = evaluate_expression(args.expr, ctx)
            except CalcError as e:
                print(f"mdllm: cannot evaluate — {e}")
                return 1
            if isinstance(v, Column):
                print(f"{len(v)} value(s) from {v.source} — wrap in sum(), "
                      f"count(), min(), max() or avg() for a figure")
                for x in v.values:
                    print(f"  {fmt(x)}")
                return 0
            print(fmt(v))
            for note in ctx.notes:
                print(f"note: {note}")
            return 0
        derivations = evaluate_block(thing.meta, ctx)
        if not derivations:
            print(f"## {thing.id}\n   no `computed:` block — nothing declared "
                  f"as derived, so there is nothing for the floor to compute.")
            return 0
        bad, errs = _report(thing, ctx, derivations)
        return 1 if (bad or errs) else 0

    total_bad = total_errs = seen = 0
    for t in corpus.things:
        if not isinstance(t.meta.get("computed"), dict):
            continue
        seen += 1
        ctx = context_for(t, corpus)
        bad, errs = _report(t, ctx, evaluate_block(t.meta, ctx))
        total_bad += bad
        total_errs += errs
    if not seen:
        print(f"## Calculated — {root}\nNo thing declares a `computed:` block. "
              f"Figures a domain derives can declare how, and the floor will "
              f"compute and re-check them (docs/calculation-reference.md).")
        return 0
    print(f"## Calculated — {root}\n{seen} thing(s) with declared derivations; "
          f"{total_bad} disagreement(s), {total_errs} not evaluable.")
    return 1 if (total_bad or total_errs) else 0


def is_quarantined(meta: dict) -> bool:
    """External and not yet verified by a human (provenance.md).

    Within-thing computation over such a thing is allowed — computing the
    totals is precisely how the human comes to verify it — but every figure
    drawn from it is stamped, so it cannot be lifted out of a provisional
    context without that being visible.
    """
    return (str(meta.get("origin", "")).strip() == "external"
            and meta.get("verified") is not True)
