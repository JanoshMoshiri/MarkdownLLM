---
description: Orient — session start whole (kernel + digest injected below), then the judgement walk; operator-invoked, the pull the startup hook cannot supply
allowed-tools: Bash(sh *)
---

**Why this is a command.** The startup hook's channel is capped at 10,000
characters and the session-start emission is near three times that, so the
hook delivers the digest cut and the kernel deferred — and a read the entry
file merely *instructs* is economised
(`emitted-content-is-read-instructed-content-is-economised`). The two blocks
below ran before you saw this prompt and their output replaced the commands:
content, not instruction. Read both end to end; then walk.

## The operative kernel (emitted)

!`sh -c 'f=$(sed -n "s/^framework_root: *//p" AGENTS.md 2>/dev/null | head -1 | tr -d "\042\047 \r"); d=; for c in "$f" "$PWD/$f"; do [ -n "$f" ] && [ -f "$c/.markdownllm" ] && { d=$c; break; }; done; if [ -z "$d" ]; then d=$PWD; while [ "$d" != / ] && [ ! -f "$d/.markdownllm" ]; do d=${d%/*}; [ -n "$d" ] || d=/; done; fi; if [ -f "$d/tools/mdllm.sh" ]; then sh "$d/tools/mdllm.sh" session-start . --kernel 2>&1; else echo "mdllm: no framework root found from $PWD — no .markdownllm above it and no usable framework_root in AGENTS.md; run session-start by hand through the launch route in AGENTS.md"; fi; exit 0'`

## The session-start digest (emitted)

!`sh -c 'f=$(sed -n "s/^framework_root: *//p" AGENTS.md 2>/dev/null | head -1 | tr -d "\042\047 \r"); d=; for c in "$f" "$PWD/$f"; do [ -n "$f" ] && [ -f "$c/.markdownllm" ] && { d=$c; break; }; done; if [ -z "$d" ]; then d=$PWD; while [ "$d" != / ] && [ ! -f "$d/.markdownllm" ]; do d=${d%/*}; [ -n "$d" ] || d=/; done; fi; if [ -f "$d/tools/mdllm.sh" ]; then sh "$d/tools/mdllm.sh" session-start . --digest 2>&1; else echo "mdllm: no framework root found from $PWD — no .markdownllm above it and no usable framework_root in AGENTS.md; run session-start by hand through the launch route in AGENTS.md"; fi; exit 0'`

## The walk — the judgement half, yours, now

Receipt first: does the kernel block end with its `[kernel emitted whole — …]`
trailer, and does the digest carry no `[truncated]` marker? If either fails,
say so and read the named file in full before continuing — a block that did
not land whole is not loaded.

Then the four steps the digest cannot perform
(`{framework_root}/templates/prompts/`; a scaffolded domain carries the same
four under its own `prompts/`):

1. **`session-orientation`** — what changed since you were last here
   (`git log` since the last `session-end:` commit), and the scoped staleness
   check: live insights × changed things, never a sweep.
2. **`domain-velocity`** — the residue behind the digest's trend line: churn
   without progress, unblocks nobody took, what each stall *means*.
3. **`evaluate-triggers`** — judge the triggers the floor could not evaluate;
   the digest's fired set is already the floor's.
4. **`surface-attention`** — order what the above produced; the digest's
   reconciliation cues, reckoning line and seat line are inputs, not outputs.

Then tell the operator where things stand, in their words, leading with what
matters and omitting what is fine. Consume the digest's figures; never
recompute them. If the operator opened with a specific request, this walk is
background to it — answer the request first.
