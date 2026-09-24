import assert from "node:assert/strict";
import { execFileSync, spawn } from "node:child_process";
import {
  mkdirSync,
  mkdtempSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import test from "node:test";

import {
  parseBridgeArgs,
  runWatchBridge,
  type ProcessInvocation,
  type ProcessResult,
} from "../src/watch-bridge.ts";

const FRAMEWORK_ROOT = resolve(import.meta.dirname, "../../..");
const MDLLM = join(FRAMEWORK_ROOT, "tools", "mdllm.py");
const PYTHON = process.env.PYTHON
  ?? (process.platform === "win32" ? "python" : "python3");

function run(command: string, args: readonly string[], cwd: string): string {
  return execFileSync(command, [...args], {
    cwd,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
  });
}

function git(cwd: string, ...args: string[]): string {
  return run("git", args, cwd).trim();
}

function commit(cwd: string, message: string): void {
  git(
    cwd,
    "-c",
    "user.name=MarkdownLLM Fixture",
    "-c",
    "user.email=fixture@example.invalid",
    "commit",
    "-q",
    "-m",
    message,
  );
}

type RecoveryFixture = Readonly<{
  root: string;
  writer: string;
  reviewer: string;
  state: string;
  wakeRecord: string;
  fakeOpenClaw: string;
}>;

function createRecoveryFixture(): RecoveryFixture {
  const root = mkdtempSync(join(tmpdir(), "mdllm-openclaw-recovery-"));
  const origin = join(root, "origin.git");
  const writer = join(root, "writer");
  const reviewer = join(root, "reviewer");
  git(root, "init", "-q", "--bare", origin);
  git(root, "--git-dir", origin, "symbolic-ref", "HEAD", "refs/heads/main");
  git(root, "init", "-q", writer);
  git(writer, "checkout", "-q", "-b", "main");
  mkdirSync(join(writer, "things"), { recursive: true });
  writeFileSync(
    join(writer, "_schema.yaml"),
    [
      "schema_version: 1",
      "domain: watch-fixture",
      "types:",
      "  design-spec:",
      "    statuses: [draft, review, cleared]",
      "    terminal_statuses: [cleared]",
      "",
    ].join("\n"),
    "utf8",
  );
  writeFileSync(
    join(writer, "things", "spec-loop.md"),
    [
      "---",
      "id: spec-loop",
      "type: workflow-definition",
      "status: draft",
      "created: 2026-09-24",
      "stages:",
      "  - id: draft",
      "    to: [review]",
      "    actor: writer",
      "  - id: review",
      "    to: [cleared]",
      "    actor: reviewer",
      "  - id: cleared",
      "    to: []",
      "---",
      "",
      "# Spec Loop",
      "",
    ].join("\n"),
    "utf8",
  );
  writeFileSync(
    join(writer, "things", "m04-design.md"),
    [
      "---",
      "id: m04-design",
      "type: design-spec",
      "status: draft",
      "created: 2026-09-24",
      "---",
      "",
      "# Design",
      "",
    ].join("\n"),
    "utf8",
  );
  git(writer, "add", "-A");
  commit(writer, "create: recovery fixture");
  git(writer, "remote", "add", "origin", origin);
  git(writer, "push", "-q", "-u", "origin", "main");
  git(root, "clone", "-q", origin, reviewer);

  const fakeOpenClaw = join(root, "fake-openclaw.mjs");
  writeFileSync(
    fakeOpenClaw,
    [
      "import { writeFileSync } from 'node:fs';",
      "writeFileSync(process.argv[2], JSON.stringify(process.argv.slice(3)));",
      "",
    ].join("\n"),
    "utf8",
  );
  return {
    root,
    writer,
    reviewer,
    state: join(root, "watch-state.json"),
    wakeRecord: join(root, "wake.json"),
    fakeOpenClaw,
  };
}
function baseline(fixture: RecoveryFixture): void {
  run(
    PYTHON,
    [
      MDLLM,
      "watch",
      fixture.writer,
      "--role",
      "writer",
      "--definition",
      "spec-loop",
      "--once",
      "--state",
      fixture.state,
    ],
    fixture.writer,
  );
}

function commitUnpublishedTurn(fixture: RecoveryFixture): void {
  const spec = join(fixture.writer, "things", "m04-design.md");
  writeFileSync(
    spec,
    readFileSync(spec, "utf8").replace("status: draft", "status: review"),
    "utf8",
  );
  git(fixture.writer, "add", "-A");
  commit(fixture.writer, "handover (unpublished)");
}

function publishCompetingTurn(fixture: RecoveryFixture): void {
  writeFileSync(
    join(fixture.reviewer, "things", "reviewer-note.md"),
    [
      "---",
      "id: reviewer-note",
      "type: design-spec",
      "status: draft",
      "created: 2026-09-24",
      "---",
      "",
      "# Reviewer Note",
      "",
    ].join("\n"),
    "utf8",
  );
  git(fixture.reviewer, "add", "-A");
  commit(fixture.reviewer, "reviewer publishes");
  git(fixture.reviewer, "push", "-q", "origin", "main");
}

function execute(invocation: ProcessInvocation): Promise<ProcessResult> {
  return new Promise((resolveResult) => {
    let output = "";
    const child = spawn(
      invocation.command,
      [...invocation.args],
      {
        cwd: invocation.cwd,
        shell: false,
        stdio: ["ignore", "pipe", "pipe"],
        windowsHide: true,
      },
    );
    child.stdout?.on("data", (chunk: Buffer | string) => {
      output += chunk.toString();
    });
    child.stderr?.on("data", (chunk: Buffer | string) => {
      output += chunk.toString();
    });
    child.once("error", (error) => {
      resolveResult({
        code: null,
        signal: null,
        error: error.name,
        ...(output ? { output } : {}),
      });
    });
    child.once("exit", (code, signal) => {
      resolveResult({
        code,
        signal,
        ...(output ? { output } : {}),
      });
    });
  });
}
for (const scenario of [
  {
    name: "unpublished",
    prepare: (_fixture: RecoveryFixture) => undefined,
    expected: "1 commit(s) ahead of origin/main (unpublished)",
    relation: "1\t0",
  },
  {
    name: "diverged",
    prepare: publishCompetingTurn,
    expected: "the remote moved under it (diverged)",
    relation: "1\t1",
  },
] as const) {
  test(
    scenario.name + " turn wakes the exact session without Git resolution",
    async () => {
      const fixture = createRecoveryFixture();
      try {
        baseline(fixture);
        commitUnpublishedTurn(fixture);
        scenario.prepare(fixture);
        const headBefore = git(fixture.writer, "rev-parse", "HEAD");
        const calls: ProcessInvocation[] = [];
        let invocationCount = 0;
        const result = await runWatchBridge(
          parseBridgeArgs([
            "--workspace",
            fixture.writer,
            "--agent-id",
            "writer-agent",
            "--session-key",
            "loop-1",
            "--role",
            "writer",
            "--definition",
            "spec-loop",
            "--interval",
            "1",
            "--state",
            fixture.state,
            "--mdllm-command",
            PYTHON,
            "--mdllm-arg",
            MDLLM,
            "--openclaw-command",
            process.execPath,
            "--openclaw-arg",
            fixture.fakeOpenClaw,
            "--openclaw-arg",
            fixture.wakeRecord,
          ]),
          async (invocation) => {
            calls.push(invocation);
            invocationCount += 1;
            if (invocationCount === 3) {
              return { code: 2, signal: null };
            }
            return execute(invocation);
          },
        );

        assert.equal(result, 2);
        assert.deepEqual(calls.map((call) => call.kind), [
          "watch",
          "wake",
          "watch",
        ]);
        const wakeArgs = JSON.parse(
          readFileSync(fixture.wakeRecord, "utf8"),
        ) as string[];
        const sessionAt = wakeArgs.indexOf("--session-key");
        assert.equal(wakeArgs[sessionAt + 1], "agent:writer-agent:loop-1");
        const messageAt = wakeArgs.indexOf("--message");
        assert.match(
          wakeArgs[messageAt + 1] ?? "",
          new RegExp(scenario.expected.replace(/[()]/g, "\\$&")),
        );
        assert.equal(git(fixture.writer, "rev-parse", "HEAD"), headBefore);
        assert.equal(
          git(
            fixture.writer,
            "rev-list",
            "--left-right",
            "--count",
            "HEAD...origin/main",
          ),
          scenario.relation,
        );
      } finally {
        rmSync(fixture.root, { recursive: true, force: true });
      }
    },
  );
}
