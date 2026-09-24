import assert from "node:assert/strict";
import test from "node:test";

import {
  PROCESS_FAILURE,
  WAKE_FAILURE,
  buildWakeInvocation,
  buildWatchInvocation,
  canonicalSessionKey,
  parseBridgeArgs,
  runWatchBridge,
  type ProcessInvocation,
  type ProcessResult,
} from "../src/watch-bridge.ts";

const REQUIRED = [
  "--workspace",
  "C:/domains/alpha",
  "--agent-id",
  "alpha",
  "--session-key",
  "loop-17",
  "--role",
  "reviewer",
  "--definition",
  "spec-loop",
];

test("session keys are canonical and cannot cross agents", () => {
  assert.equal(
    canonicalSessionKey("alpha", "loop-17"),
    "agent:alpha:loop-17",
  );
  assert.equal(
    canonicalSessionKey("alpha", "agent:alpha:loop-17"),
    "agent:alpha:loop-17",
  );
  assert.throws(
    () => canonicalSessionKey("alpha", "agent:beta:loop-17"),
    /does not belong/,
  );
  assert.throws(() => canonicalSessionKey("alpha", "global"), /concrete/);
});

test("bridge arguments require an exact binding and retain argv prefixes", () => {
  assert.throws(() => parseBridgeArgs([]), /workspace/);
  const config = parseBridgeArgs([
    ...REQUIRED,
    "--run",
    "book-run",
    "--mdllm-command",
    "python",
    "--mdllm-arg",
    "tools/mdllm.py",
    "--openclaw-command",
    "node",
    "--openclaw-arg",
    "openclaw.mjs",
    "--timeout",
    "900",
  ]);
  assert.equal(config.sessionKey, "agent:alpha:loop-17");
  assert.equal(config.run, "book-run");
  assert.deepEqual(config.mdllmCommandArgs, ["tools/mdllm.py"]);
  assert.deepEqual(config.openclawCommandArgs, ["openclaw.mjs"]);
  assert.equal(config.timeoutSeconds, 900);
});

test("watch invocation preserves the MarkdownLLM exit contract", () => {
  const invocation = buildWatchInvocation(parseBridgeArgs([
    ...REQUIRED,
    "--run",
    "run-1",
    "--state",
    "C:/state/watch.json",
  ]));
  assert.equal(invocation.kind, "watch");
  assert.equal(invocation.command, "mdllm");
  assert.equal(invocation.cwd, "C:/domains/alpha");
  assert.deepEqual(invocation.args.slice(0, 7), [
    "watch",
    "C:/domains/alpha",
    "--role",
    "reviewer",
    "--definition",
    "spec-loop",
    "--field",
  ]);
  assert.equal(invocation.args.includes("--exit-on-wake"), true);
  assert.equal(invocation.args.includes("--once"), false);
  assert.deepEqual(invocation.args.slice(-4), [
    "--run",
    "run-1",
    "--state",
    "C:/state/watch.json",
  ]);
});

test("wake invocation targets one matching agent session without delivery", () => {
  const invocation = buildWakeInvocation(parseBridgeArgs(REQUIRED));
  assert.equal(invocation.kind, "wake");
  assert.deepEqual(invocation.args.slice(0, 6), [
    "agent",
    "--agent",
    "alpha",
    "--session-key",
    "agent:alpha:loop-17",
    "--message",
  ]);
  assert.match(invocation.args[6] ?? "", /role `reviewer`/);
  assert.equal(invocation.args.includes("--deliver"), false);
  assert.deepEqual(invocation.args.slice(-3), [
    "--json",
    "--timeout",
    "600",
  ]);
  assert.equal(invocation.args.includes("--json"), true);
});

function scriptedRunner(
  script: readonly ProcessResult[],
  calls: ProcessInvocation[],
) {
  let index = 0;
  return async (invocation: ProcessInvocation): Promise<ProcessResult> => {
    calls.push(invocation);
    const result = script[index];
    index += 1;
    if (!result) {
      throw new Error("runner script exhausted");
    }
    return result;
  };
}

const ok = { code: 0, signal: null } as const;

test("exit 0 wakes once, waits, then rearms the watch", async () => {
  const calls: ProcessInvocation[] = [];
  const result = await runWatchBridge(
    parseBridgeArgs(REQUIRED),
    scriptedRunner([
      ok,
      ok,
      { code: 2, signal: null },
    ], calls),
  );
  assert.equal(result, 2);
  assert.deepEqual(calls.map((call) => call.kind), [
    "watch",
    "wake",
    "watch",
  ]);
});

for (const code of [1, 2, 3] as const) {
  test("watch exit " + code + " never wakes an agent", async () => {
    const calls: ProcessInvocation[] = [];
    const result = await runWatchBridge(
      parseBridgeArgs(REQUIRED),
      scriptedRunner([{ code, signal: null }], calls),
    );
    assert.equal(result, code);
    assert.deepEqual(calls.map((call) => call.kind), ["watch"]);
  });
}


for (const [signal, expected] of [
  ["SIGINT", 130],
  ["SIGTERM", 143],
] as const) {
  test(signal + " preserves the conventional process exit", async () => {
    const result = await runWatchBridge(
      parseBridgeArgs(REQUIRED),
      scriptedRunner([{ code: null, signal }], []),
    );
    assert.equal(result, expected);
  });
}
test("failed or ambiguous wake stops without an unsafe retry", async () => {
  for (const wake of [
    { code: 1, signal: null },
    { code: null, signal: null, error: "ENOENT" },
  ] satisfies ProcessResult[]) {
    const calls: ProcessInvocation[] = [];
    const result = await runWatchBridge(
      parseBridgeArgs(REQUIRED),
      scriptedRunner([ok, wake], calls),
    );
    assert.equal(
      result,
      wake.code === null ? PROCESS_FAILURE : WAKE_FAILURE,
    );
    assert.deepEqual(calls.map((call) => call.kind), ["watch", "wake"]);
  }
});
