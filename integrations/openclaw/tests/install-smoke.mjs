import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { randomBytes } from "node:crypto";
import { readFile, rm, unlink } from "node:fs/promises";
import { homedir } from "node:os";
import { basename, dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const openclawEntry = join(root, "node_modules", "openclaw", "openclaw.mjs");
const fixtureEntry = join(root, "tests", "fixtures", "openclaw-domain", "AGENTS.md");
const npmEntry = process.env.npm_execpath;
const profileName = `markdownllm-openclaw-smoke-${process.pid}-${randomBytes(6).toString("hex")}`;
const profileDir = join(homedir(), `.openclaw-${profileName}`);

if (!npmEntry) throw new Error("npm_execpath is required; run this through npm");
assert.match(profileName, /^markdownllm-openclaw-smoke-\d+-[a-f0-9]{12}$/);
assert.equal(profileDir, join(homedir(), `.openclaw-${profileName}`));

function run(command, args) {
  return new Promise((resolve, reject) => {
    execFile(command, args, {
      cwd: root,
      env: { ...process.env, CI: "1", NO_COLOR: "1" },
      encoding: "utf8",
      maxBuffer: 16 * 1024 * 1024,
      timeout: 10 * 60 * 1000,
      windowsHide: true,
      shell: false,
    }, (error, stdout, stderr) => {
      if (error) {
        error.message += `\nstdout:\n${stdout}\nstderr:\n${stderr}`;
        reject(error);
        return;
      }
      resolve({ stdout, stderr });
    });
  });
}

function openclaw(args) {
  return run(process.execPath, [openclawEntry, "--profile", profileName, ...args]);
}

function json(result, label) {
  try {
    return JSON.parse(result.stdout);
  } catch (error) {
    error.message = `${label} returned invalid JSON: ${error.message}`;
    throw error;
  }
}

let installed = false;
let tarball;
try {
  const fixtureBefore = await readFile(fixtureEntry, "utf8");
  const packed = await run(process.execPath, [
    npmEntry, "pack", "--ignore-scripts", "--json",
  ]);
  const packResult = JSON.parse(packed.stdout);
  assert.equal(packResult.length, 1);
  tarball = join(root, packResult[0].filename);
  assert.equal(dirname(tarball), root);
  assert.match(
    basename(tarball),
    /^markdownllm-openclaw-adapter-[0-9A-Za-z.-]+\.tgz$/,
  );

  await openclaw([
    "plugins", "install", `npm-pack:${tarball}`,
    "--force", "--accept-capabilities",
  ]);
  installed = true;
  await openclaw([
    "config", "set", "plugins.entries.markdownllm.config.agentIds",
    '["fixture-agent"]', "--strict-json",
  ]);
  await openclaw([
    "config", "set",
    "plugins.entries.markdownllm.hooks.allowConversationAccess",
    "true", "--strict-json",
  ]);
  await openclaw([
    "plugins", "enable", "markdownllm", "--accept-capabilities",
  ]);

  const validation = json(
    await openclaw(["config", "validate", "--json"]),
    "config validate",
  );
  assert.equal(validation.valid, true);
  assert.deepEqual(validation.warnings, []);

  const inspection = json(await openclaw([
    "plugins", "inspect", "markdownllm", "--runtime", "--json",
  ]), "plugins inspect");
  assert.equal(inspection.plugin.status, "loaded");
  assert.equal(inspection.plugin.imported, true);
  assert.equal(inspection.plugin.hookCount, 5);
  assert.equal(inspection.install.artifactKind, "npm-pack");
  assert.equal(inspection.policy.allowConversationAccess, true);
  assert.deepEqual(inspection.diagnostics, []);
  assert.deepEqual(
    inspection.typedHooks.map(({ name }) => name).sort(),
    [
      "after_compaction",
      "before_prompt_build",
      "before_reset",
      "session_end",
      "session_start",
    ],
  );

  const doctor = json(
    await openclaw(["plugins", "doctor", "--json"]),
    "plugins doctor",
  );
  assert.equal(doctor.ok, true);
  assert.deepEqual(doctor.pluginErrors, []);
  assert.deepEqual(doctor.diagnostics, []);
  assert.deepEqual(doctor.configurationWarnings, []);
  assert.equal(await readFile(fixtureEntry, "utf8"), fixtureBefore);

  await openclaw(["plugins", "uninstall", "markdownllm", "--force"]);
  installed = false;
  const postRemoval = json(
    await openclaw(["config", "validate", "--json"]),
    "post-removal config validate",
  );
  assert.equal(postRemoval.valid, true);
  console.log("OpenClaw clean-profile install smoke passed.");
} finally {
  if (installed) {
    try {
      await openclaw(["plugins", "uninstall", "markdownllm", "--force"]);
    } catch {
      // Exact disposable profile removal below is the final cleanup boundary.
    }
  }
  await rm(profileDir, { recursive: true, force: true });
  if (tarball) {
    try {
      await unlink(tarball);
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
  }
}
