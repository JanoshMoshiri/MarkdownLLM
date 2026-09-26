import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { readdir, readFile } from "node:fs/promises";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

const root = new URL("../", import.meta.url);
const run = promisify(execFile);

async function json(name: string): Promise<Record<string, any>> {
  return JSON.parse(await readFile(new URL(name, root), "utf8"));
}

async function sources(): Promise<Map<string, string>> {
  const directory = new URL("src/", root);
  const entries = await readdir(directory);
  return new Map(await Promise.all(
    entries
      .filter((name) => name.endsWith(".ts"))
      .map(async (name) => [
        name,
        await readFile(new URL(name, directory), "utf8"),
      ] as const),
  ));
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

test("package carries public release metadata and notices", async () => {
  const pkg = await json("package.json");
  assert.equal(pkg.engines.node, ">=24.0.0");
  assert.equal(pkg.repository.directory, "integrations/openclaw");
  assert.deepEqual(pkg.files, [
    "dist",
    "openclaw.plugin.json",
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
  ]);
  assert.match(await readFile(new URL("LICENSE", root), "utf8"), /MIT License/);
  assert.match(await readFile(new URL("CHANGELOG.md", root), "utf8"), /Unreleased/);
});

test("packed artifact contains only the intended public files", async () => {
  const npmEntry = process.env.npm_execpath;
  assert.ok(npmEntry, "npm_execpath is required; run this test through npm");
  const { stdout } = await run(process.execPath, [
    npmEntry,
    "pack",
    "--ignore-scripts",
    "--dry-run",
    "--json",
  ], {
    cwd: fileURLToPath(root),
    encoding: "utf8",
    maxBuffer: 16 * 1024 * 1024,
  });
  const packed = JSON.parse(stdout) as Array<{
    files: Array<{ path: string }>;
  }>;
  assert.equal(packed.length, 1);
  assert.deepEqual(
    packed[0]?.files.map(({ path }) => path).sort(),
    [
      "CHANGELOG.md",
      "CONTRIBUTING.md",
      "LICENSE",
      "README.md",
      "dist/cli.d.ts",
      "dist/cli.js",
      "dist/cli.js.map",
      "dist/core.d.ts",
      "dist/core.js",
      "dist/core.js.map",
      "dist/domain-command.d.ts",
      "dist/domain-command.js",
      "dist/domain-command.js.map",
      "dist/index.d.ts",
      "dist/index.js",
      "dist/index.js.map",
      "dist/watch-bridge.d.ts",
      "dist/watch-bridge.js",
      "dist/watch-bridge.js.map",
      "openclaw.plugin.json",
      "package.json",
    ],
  );
});

test("manifest is strict and requires explicit domain routing", async () => {
  const manifest = await json("openclaw.plugin.json");
  assert.equal(manifest.id, "markdownllm");
  assert.equal(manifest.activation.onStartup, true);
  assert.deepEqual(manifest.activation.onCommands, ["domain"]);
  assert.deepEqual(manifest.activation.onCapabilities, ["hook"]);
  assert.equal(manifest.configSchema.additionalProperties, false);
  assert.deepEqual(manifest.configSchema.required, ["domains"]);
  assert.equal(manifest.configSchema.properties.domains.minProperties, 1);
  assert.deepEqual(
    manifest.configSchema.properties.domains.additionalProperties.required,
    ["agentId"],
  );
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
test("source stays on public seams and has one lifecycle owner", async () => {
  const sourceMap = await sources();
  const combined = [...sourceMap.values()].join("\n");
  const imports = [...combined.matchAll(/from "([^"]+)"/g)]
    .map((match) => match[1])
    .filter((name): name is string => name !== undefined)
    .filter((name) => name.startsWith("openclaw/"));
  assert.deepEqual(
    [...new Set(imports)],
    [
      "openclaw/plugin-sdk/plugin-entry",
      "openclaw/plugin-sdk/telegram-account",
    ],
  );
  assert.doesNotMatch(combined, /openclaw\/(?:dist|src)\//);
  assert.doesNotMatch(
    combined,
    /sessions\.pluginPatch|registerSessionExtension|sessions\.json|transcript/i,
  );
  assert.doesNotMatch(
    combined,
    /runtime\.gateway\.request|createSessionEntry|runWithWorkAdmission/,
  );

  const lifecycleOwners = [...sourceMap]
    .filter(([, source]) => source.includes('"harness-event"'))
    .map(([name]) => name);
  assert.deepEqual(lifecycleOwners, ["core.ts"]);

  const bridge = sourceMap.get("watch-bridge.ts") ?? "";
  assert.doesNotMatch(bridge, /from "node:fs"/);
  assert.doesNotMatch(bridge, /yaml|frontmatter|current_stage|linked_things/i);
});
