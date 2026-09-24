import assert from "node:assert/strict";
import test from "node:test";

import {
  LifecycleGate,
  buildInvocation,
  contractFingerprint,
  executeLifecycle,
  isDesignatedAgent,
  lifecycleKey,
  parsePluginConfig,
} from "../src/core.ts";

test("configuration requires explicit unique designated agents", () => {
  assert.throws(() => parsePluginConfig({}), /agentIds/);
  assert.throws(
    () => parsePluginConfig({ agentIds: ["alpha", "alpha"] }),
    /unique/,
  );
  const config = parsePluginConfig({ agentIds: ["alpha"] });
  assert.deepEqual(config, {
    agentIds: ["alpha"],
    command: "mdllm",
    commandArgs: [],
    timeoutMs: 115_000,
  });
  assert.equal(isDesignatedAgent(config, "alpha"), true);
  assert.equal(isDesignatedAgent(config, "beta"), false);
});

test("binding identity requires both OpenClaw identifiers", () => {
  assert.equal(lifecycleKey("alpha", "session-1"), "alpha:session-1");
  assert.equal(lifecycleKey("alpha", undefined), undefined);
  assert.equal(lifecycleKey(undefined, "session-1"), undefined);
});

test("definition fingerprint is stable and version-sensitive", () => {
  const current = contractFingerprint();
  assert.match(current, /^sha256:[0-9a-f]{64}$/);
  assert.equal(contractFingerprint(), current);
  assert.notEqual(contractFingerprint({ version: 3 }), current);
});

test("invocation is an argv vector with no shell command", () => {
  const config = parsePluginConfig({
    agentIds: ["alpha"],
    command: "mdllm-custom",
    commandArgs: ["floor.py"],
    timeoutMs: 30_000,
  });
  const invocation = buildInvocation(
    config,
    "C:/domains/alpha",
    "sha256:pinned",
  );
  assert.equal(invocation.command, "mdllm-custom");
  assert.deepEqual(invocation.args, [
    "floor.py",
    "harness-event",
    "openclaw",
    "session-start",
    "C:/domains/alpha",
    "sha256:pinned",
  ]);
  assert.equal(invocation.cwd, "C:/domains/alpha");
  assert.equal(invocation.timeoutMs, 30_000);
});

test("gate runs once until invalidated or the contract changes", () => {
  const gate = new LifecycleGate();
  assert.equal(gate.claim("alpha:s1", "v1"), true);
  assert.equal(gate.claim("alpha:s1", "v1"), false);
  gate.complete("alpha:s1", "v1");
  assert.equal(gate.inspect("alpha:s1")?.state, "complete");
  assert.equal(gate.claim("alpha:s1", "v2"), true);
  gate.release("alpha:s1", "v2");
  assert.equal(gate.claim("alpha:s1", "v2"), true);
  gate.invalidate("alpha:s1");
  assert.equal(gate.inspect("alpha:s1"), undefined);
});

test("gate isolates agents and sessions", () => {
  const gate = new LifecycleGate();
  for (const key of ["alpha:s1", "alpha:s2", "beta:s1"]) {
    assert.equal(gate.claim(key, "v1"), true);
    gate.complete(key, "v1");
  }
  gate.invalidate("alpha:s1");
  assert.equal(gate.inspect("alpha:s1"), undefined);
  assert.equal(gate.inspect("alpha:s2")?.state, "complete");
  assert.equal(gate.inspect("beta:s1")?.state, "complete");
});

test("lifecycle output is injected and subprocess failure is retryable", async () => {
  const invocation = buildInvocation(
    parsePluginConfig({ agentIds: ["alpha"] }),
    "C:/domains/alpha",
    "sha256:pinned",
  );
  const calls: unknown[][] = [];
  const success = await executeLifecycle(
    invocation,
    ((...args: unknown[]) => {
      calls.push(args);
      const callback = args.at(-1) as (
        error: Error | null,
        stdout: string,
      ) => void;
      callback(null, "orientation");
      return {} as ReturnType<typeof import("node:child_process").execFile>;
    }) as typeof import("node:child_process").execFile,
  );
  assert.deepEqual(success, { ok: true, context: "orientation" });
  const options = calls[0]?.[2] as Record<string, unknown>;
  assert.equal(options.shell, false);
  assert.equal(options.cwd, "C:/domains/alpha");

  const failure = await executeLifecycle(
    invocation,
    ((...args: unknown[]) => {
      const callback = args.at(-1) as (
        error: Error | null,
        stdout: string,
      ) => void;
      callback(new Error("missing"), "");
      return {} as ReturnType<typeof import("node:child_process").execFile>;
    }) as typeof import("node:child_process").execFile,
  );
  assert.equal(failure.ok, false);
  assert.equal(failure.errorKind, "Error");
  assert.match(failure.context, /not certified/);
});
