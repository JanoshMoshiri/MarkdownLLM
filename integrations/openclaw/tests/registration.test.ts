import assert from "node:assert/strict";
import test from "node:test";

import type { OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-entry";

import { registerMarkdownLLMPlugin } from "../dist/index.js";

type Hook = {
  handler: (event: unknown, ctx: any) => unknown;
  options?: Record<string, unknown>;
};

test("registration binds designated sessions and reruns after lifecycle changes", async () => {
  const hooks = new Map<string, Hook[]>();
  const warnings: string[] = [];
  const invocations: any[] = [];
  const api = {
    pluginConfig: {
      agentIds: ["alpha"],
      command: "mdllm-test",
      commandArgs: ["floor.py"],
      timeoutMs: 20_000,
    },
    config: {},
    runtime: {
      agent: {
        resolveAgentWorkspaceDir: (_config: unknown, agentId: string) =>
          "/fixtures/" + agentId,
      },
    },
    logger: {
      debug() {},
      info() {},
      warn(message: string) {
        warnings.push(message);
      },
      error() {},
    },
    on(name: string, handler: Hook["handler"], options?: Hook["options"]) {
      const entries = hooks.get(name) ?? [];
      entries.push({ handler, options });
      hooks.set(name, entries);
    },
  } as unknown as OpenClawPluginApi;

  registerMarkdownLLMPlugin(api, async (invocation) => {
    invocations.push(invocation);
    return { ok: true, context: "fixture orientation" };
  });

  assert.deepEqual([...hooks.keys()], [
    "session_start",
    "before_reset",
    "after_compaction",
    "session_end",
    "before_prompt_build",
  ]);
  const prompt = hooks.get("before_prompt_build")?.[0];
  assert.ok(prompt);
  assert.deepEqual(prompt.options, { timeoutMs: 25_000 });

  assert.equal(
    await prompt.handler({}, { agentId: "other", sessionKey: "s1" }),
    undefined,
  );
  const unbound = await prompt.handler({}, { agentId: "alpha" });
  assert.match((unbound as any).prependContext, /binding was refused/);

  const ctx = { agentId: "alpha", sessionKey: "s1", sessionId: "sid-1" };
  assert.deepEqual(await prompt.handler({ messages: [] }, ctx), {
    prependContext: "fixture orientation",
  });
  assert.equal(
    await prompt.handler({
      messages: [{ role: "user" }, { role: "assistant" }],
    }, ctx),
    undefined,
  );
  assert.equal(invocations.length, 1);
  assert.equal(invocations[0].command, "mdllm-test");
  assert.equal(invocations[0].cwd, "/fixtures/alpha");
  assert.deepEqual(invocations[0].args.slice(0, 5), [
    "floor.py",
    "harness-event",
    "openclaw",
    "session-start",
    "/fixtures/alpha",
  ]);

  const compact = hooks.get("after_compaction")?.[0];
  assert.ok(compact);
  compact.handler(
    { messageCount: 2, compactedCount: 1 },
    { sessionId: "sid-1" },
  );
  assert.deepEqual(await prompt.handler({ messages: [{ role: "system" }] }, ctx), {
    prependContext: "fixture orientation",
  });
  assert.equal(invocations.length, 2);

  const reset = hooks.get("before_reset")?.[0];
  assert.ok(reset);
  reset.handler({ reason: "reset" }, {});
  assert.deepEqual(await prompt.handler({ messages: [] }, ctx), {
    prependContext: "fixture orientation",
  });
  assert.equal(invocations.length, 3);

  assert.equal(
    await prompt.handler({
      messages: [{ role: "user" }, { role: "assistant" }],
    }, ctx),
    undefined,
  );
  assert.deepEqual(await prompt.handler({ messages: [] }, ctx), {
    prependContext: "fixture orientation",
  });
  assert.equal(invocations.length, 4);

  const rolled = {
    agentId: "alpha",
    sessionKey: "s1",
    sessionId: "sid-2",
  };
  assert.deepEqual(await prompt.handler({ messages: [] }, rolled), {
    prependContext: "fixture orientation",
  });
  assert.equal(invocations.length, 5);
  assert.equal(
    await prompt.handler({
      messages: [{ role: "user" }, { role: "assistant" }],
    }, rolled),
    undefined,
  );
  assert.equal(invocations.length, 5);
  assert.deepEqual(warnings, []);
});
