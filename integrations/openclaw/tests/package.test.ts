import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);

async function json(name: string): Promise<Record<string, any>> {
  return JSON.parse(await readFile(new URL(name, root), "utf8"));
}

test("package points at built JavaScript and pins experimental compatibility", async () => {
  const pkg = await json("package.json");
  assert.deepEqual(pkg.openclaw.extensions, ["./dist/index.js"]);
  assert.equal(
    pkg.bin["markdownllm-openclaw-watch"],
    "./dist/cli.js",
  );
  assert.equal(pkg.peerDependencies.openclaw, ">=2026.9.3 <2026.10.0");
  assert.equal(
    pkg.openclaw.compat.pluginApi,
    ">=2026.9.3 <2026.10.0",
  );
  assert.equal(pkg.openclaw.build.openclawVersion, "2026.9.3");
});

test("manifest is strict and requires explicit agent designation", async () => {
  const manifest = await json("openclaw.plugin.json");
  assert.equal(manifest.id, "markdownllm");
  assert.equal(manifest.activation.onStartup, true);
  assert.deepEqual(manifest.activation.onCapabilities, ["hook"]);
  assert.equal(manifest.configSchema.additionalProperties, false);
  assert.deepEqual(manifest.configSchema.required, ["agentIds"]);
  assert.equal(manifest.configSchema.properties.agentIds.minItems, 1);
  assert.equal(manifest.configSchema.properties.agentIds.uniqueItems, true);
  assert.deepEqual(manifest.configSchema.properties.commandArgs.default, []);
});

test("runtime uses additive context and excludes rejected private seams", async () => {
  const source = await readFile(new URL("src/index.ts", root), "utf8");
  assert.match(source, /before_prompt_build/);
  assert.match(source, /prependContext/);
  assert.doesNotMatch(source, /systemPrompt/);
  assert.doesNotMatch(source, /runtime\.gateway\.request/);
  assert.doesNotMatch(source, /createSessionEntry/);
  assert.doesNotMatch(source, /sessions\.json|transcript/i);
});
