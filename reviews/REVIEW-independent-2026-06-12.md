---
id: independent-review-2026-06-12-fable
type: artifact
status: stable
created: 2026-06-12
linked_things:
  - id: independent-review-2026-06-11-fable
    relation: extends
    notes: "Second independent review, one day after the first; verifies the 3.5.0 response and adds new findings"
  - id: portability-claims-need-execution-tests
    relation: supports
    notes: "The insight now applies to the floor's own test suite — two self-tests are environment-dependent"
---

# Independent Review — MarkdownLLM Framework v3.5.0 (HEAD e90e2f2)

Second independent review, one day after the first. Full re-read of specs, kernel, tool, templates, evals, domains, and everything that changed since `REVIEW-independent-2026-06-11.md`. Verification run from a clean HEAD extract: `mdllm validate` clean across all three corpora (51 + 6 + 12 things, 0 findings), kernel in sync, 35 of 37 floor self-tests passing — the two failures are themselves findings, below. Reviewer: Claude (Fable), 2026-06-12, via Cowork.

## Verdict

The headline is the response speed. Eight of yesterday's recommendations landed within twenty-four hours, and I verified them rather than taking the commit messages' word: they are real, done properly, not checkbox-cleared. The birth-path staleness is fixed, the relation vocabulary genuinely pruned 35 → 13 with the corpus migrated, the examples are under the floor and life-manager actually has things, the README claims are honestly softened, and `first-hour.md` is the best human-facing page in the repository. On top of the queue you shipped three things nobody asked for — `doctor`, `scaffold`, and the cold-start fixture — and `scaffold` immediately proved the whole mechanisation thesis by discovering that `_schema.yaml.template` was unparseable YAML *as shipped*. The hand process had been silently routing around a broken template; the deterministic version hit it on first contact. That is the framework working exactly as designed.

But the speed has a cost, and it is this review's main new material: **the last twenty-four hours of code shipped with environment-dependent self-tests, a reference to a version that doesn't exist, and evidence that lives outside git.** The corrective loop is now fast enough to generate its own class of defect — and every one of the new defects is an instance of a lesson the framework has already written down as an insight. The framework learns well; it doesn't yet *apply* its lessons at the speed it ships.

And the deepest point survives a day of excellent work unchanged: this is still a framework about itself, reviewed by the same reviewer two days running, at the request of the same single operator who is also the author. The marginal information in this review is a fraction of yesterday's. The cold-start eval with a human who isn't you remains worth more than anything I can write here.

## Verified: What Landed From Yesterday

Staleness pass (template, framework-discovery, guide §294) — done; the template now teaches the kernel pattern and the version-check. Examples under the floor — done; `mdllm validate` discovers `examples/*` as sub-corpora, both declare schemas, life-manager has a 12-thing interlinked dataset including a pinned, provenance-verified decision record. Relation prune — done, 13 relations with rationale comments in `_schema.yaml`. README/manifesto claim softening — done; the 2×2 is now framed as a tested hypothesis with the honest reading attached, and the `.skill.md` "standard" claim is correctly downgraded to "emerging convention". Measured token figures — done. `first-hour.md` — new, and excellent: the break-something-on-purpose exercise in minutes 45–55 teaches the floor's bargain better than any spec prose. `doctor` — new, and its design carries the right idea into code: it *executes* the hook rather than checking it exists, because "resolution is not verification."

## New Findings

**1. Two floor self-tests fail outside the authoring machine — CI is probably red right now.** `test_scaffold_birth_sequence` asserts "first commit made", but `scaffold`'s nested domain repo inherits no git identity from the test fixture (which configures the *outer* repo only) — the commit needs *global* `user.name`/`user.email`. Your Windows machine has them; this sandbox doesn't, and GitHub Actions runners don't either. Unless something sets identity in CI that I can't see, the commit `e90e2f2` you pushed tonight fails its own CI. Separately, `test_doctor_floor_active_with_hook` asserts "EXECUTES", which requires `git hook run` (git ≥ 2.36) — it passes on ubuntu-latest but fails on Ubuntu 22.04's system git 2.34, i.e. on a large share of real machines. Both are `portability-claims-need-execution-tests` recursing one level down: the tests that verify portability are themselves unportable. Fix: tests provision identity via environment (`GIT_AUTHOR_NAME`/`GIT_COMMITTER_NAME` env vars or an isolated `HOME`), and the doctor test should branch or skip on git version the same way doctor itself does.

**2. `scaffold` exits 0 when the birth sequence partially fails.** A failed first commit, or a failed outer `.gitignore` commit, produces a WARN line and a success exit code. This is the *mechanised hard hook* — the entire point of moving it into code was that partial completion stops being possible to miss. An agent (or CI) reading the exit code concludes the invariant held when it didn't. The isolation ordering steps deserve the same severity discipline the validator has: invariant broken = exit 1, with the WARN text as the message.

**3. orchestration.md §pre-domain-scaffold says "Mechanised since v3.6" — there is no v3.6.** Sentinel, AGENTS.md, and CHANGELOG all say 3.5.0. A hand-written version claim drifted at the moment of writing, in the same release that built sentinel-sync checking for exactly this class of error one surface over. Version references in spec prose are now the last unguarded hand-maintained surface; either the validator learns to check them against the sentinel, or spec prose stops naming versions and says "since the scaffold subcommand" instead.

**4. The eval evidence is gitignored.** `evals/runs/` is excluded, yet the README, an insight, and the continuity brief all cite the 2×2 numbers as the framework's first empirical support. By the framework's own axiom — committed state is the only real state — the evidence for its central claim does not exist. The run *workspaces* are bulky and rightly ignored; the `result.json` files are tiny and should be committed. Right now a `git clone` of this repository contains the claim and not the data.

**5. The cold-start fixture hardcodes `framework_version_seen: 3.5.0`.** It breaks on the next release, silently turning a passing scaffold into a failing assertion. The fixture should read the expected version from the sentinel at run time — the runner has the framework checkout in hand.

**6. Two of three live domains are stale, and so is the staleness procedure inside them.** *(Re-verified 2026-06-12 late session, after the operator's domain update pass.)* The good news first: **eco-essentials completed a real refresh** — `refresh: absorbed framework v3.5.0 changes (from v2.8)`, floor adopted, schema declared, 12 things validating clean, and the version-check wording corrected to the v3 procedure. That is the first end-to-end evidence the domain-refresh contract works across a five-version gap. But on disk right now, jmtm-software still reads `framework_version_seen: 3.0` and property-ventures `2.9`, and **both** still carry the *pre-v3 procedure* in their version-check text ("load validate.thing.md and validate all domain things" — validation by reasoning, the exact thing v3 abolished). The version-check hard hook can detect that a domain is behind, but the *procedure it then follows* is itself the stale artifact — refresh instructions can't reach the refresh instructions; eco-essentials escaped only by running the full refresh. jmtm's working tree shows uncommitted AGENTS.md/WORKLOG modifications, so its refresh may be in flight — if so, finish and commit it; by the framework's own rule, an uncommitted refresh isn't real. Two responses worth considering together: make `domain-refresh` cheaper than the release cadence (most of a refresh is now "re-copy three boilerplate blocks from the current template" — scaffold-adjacent, mechanisable), and slow the release cadence so domains aren't perpetually one to five versions behind a framework that versions daily. jmtm is the one with statutory deadlines; refresh it first.

**7. Carried forward, still true.** The manifesto still promises cross-domain linking (§242: "Your financial tracking can link to your projects") that no spec defines and the validator would flag as a broken reference. The README still says "There is no setup step. There is no installation." while first-hour.md correctly lists git, Python 3.10+, and PyYAML as prerequisites and the floor's whole value depends on installing a hook — pick one story; the honest one is first-hour's. And limitations.md, concurrency, and the read-side of quarantine remain open exactly as queued — the queue order (eval first) is right; this is noted so they don't quietly fall off it.

## Over- and Under-Engineering

Yesterday's structural assessment stands and I won't repeat it: the soft orchestration layer is still an event system with no runtime and no real adopters; the deferred-spec mass still taxes every reader; both are unchanged in a day and were never going to change in one. Two additions. First, the WORKLOG is now ~93KB of append-only hand-maintained prose — the largest single file in a repository whose core doctrine is decomposition and generated-or-validated surfaces; its session blocks duplicate what git log, the continuity brief, and the insights already hold, and its To-Do section was yesterday's worked example of tracking drift. It is the next REVIEWLOG. Second — and gently — **reviews themselves are becoming a tracking surface.** This is the second full independent review in two days, requested before the first review's centrepiece action has run. Review #1 produced eight actioned findings; review #2 produced two genuinely new defect classes and a stack of confirmations. Review #3 on this cadence would produce near nothing. The instrument is exhausted until new evidence — a real outside user, a harder fixture, a refreshed domain — gives it something to measure.

## On "I Think What We Got Is Pretty Special"

You asked for honesty, so: partially earned. The things that are genuinely uncommon here — and I do not say this loosely — are the self-correction loop with teeth (failure → insight → structural fix → mechanical verification of the fix), the validation division of labour ("never re-perform mechanical checks by reasoning" is the clearest idea in the corpus and deserves to travel), the kernel as context engineering, and the evals' fairness discipline, which is more honest than most published benchmarks. Those four are real contributions and they compound.

What is *not yet earned* is the broad-implications claim. One operator, who is the author. One production domain with ~20 things. One harness genuinely exercised. Zero users who aren't you. The framework over-validates self-referential elegance by construction — every session it runs on itself confirms that it works *on itself*. The 2×2's own honest reading says the reasoning claim is untested. "First of its kind" claims also need the comparison document you haven't written: the newcomer's question — why not CLAUDE.md plus a notes folder and a linter? — is answerable, and the answer is favourable to you (the floor, the provenance chain, and the refresh contract are the differentiators), but the corpus never makes the argument. Special is plausible. Demonstrated requires exactly one thing, and it's the same thing yesterday's review ended on: put it in front of a person who isn't you, and watch.

## Priority Recommendations

1. **Fix the two environment-dependent self-tests and check whether CI on `e90e2f2` is red** — today, before anything else ships on top.
2. **Make `scaffold` exit non-zero on partial birth**, and fix the "v3.6" reference in orchestration.md.
3. **Commit the eval `result.json` evidence; template the fixture's version assertion** from the sentinel.
4. **Run the cold-start eval with a real human.** Everything else, including further reviews, is lower value until this happens.
5. **Refresh jmtm-software** (statutory stakes, stale procedure text), and decide the release-cadence vs refresh-cost trade-off consciously.
6. Then the standing queue, in its current order: limitations.md and the comparison answer, read-side quarantine, concurrency page.

---

One process note: the `post-write:commit` hard hook is unfulfilled for this file. The harness I reviewed from cannot safely commit — git operations through its filesystem mount showed index errors mid-session — so the commit is left to the operator. Which is itself the day's last data point for `agents-md-discovery-is-harness-dependent`: the floor's guarantees end where the harness's filesystem begins.
