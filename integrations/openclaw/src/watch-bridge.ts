import { spawn } from "node:child_process";

export const WAKE_FAILURE = 4;
export const PROCESS_FAILURE = 5;

export type WatchBridgeConfig = Readonly<{
  workspace: string;
  agentId: string;
  sessionKey: string;
  role: string;
  definition: string;
  run?: string;
  field: string;
  remote: string;
  branch: string;
  interval: number;
  state?: string;
  mdllmCommand: string;
  mdllmCommandArgs: readonly string[];
  openclawCommand: string;
  openclawCommandArgs: readonly string[];
  timeoutSeconds: number;
}>;

export type ProcessInvocation = Readonly<{
  command: string;
  args: readonly string[];
  cwd: string;
  kind: "watch" | "wake";
}>;

export type ProcessResult = Readonly<{
  code: number | null;
  signal: NodeJS.Signals | null;
  error?: string;
}>;

export type ProcessRunner = (
  invocation: ProcessInvocation,
) => Promise<ProcessResult>;

function nonEmpty(value: unknown, name: string): string {
  if (typeof value !== "string" || value.trim().length === 0) {
    throw new TypeError(name + " must be a non-empty string");
  }
  return value.trim();
}

function positiveInteger(value: string, name: string): number {
  const parsed = Number(value);
  if (!Number.isSafeInteger(parsed) || parsed < 1) {
    throw new TypeError(name + " must be a positive integer");
  }
  return parsed;
}

export function canonicalSessionKey(
  agentIdValue: string,
  sessionKeyValue: string,
): string {
  const agentId = nonEmpty(agentIdValue, "agentId");
  const sessionKey = nonEmpty(sessionKeyValue, "sessionKey");
  if (agentId.includes(":")) {
    throw new TypeError("agentId must not contain ':'");
  }
  if (sessionKey === "global" || sessionKey === "unknown") {
    throw new TypeError("sessionKey must designate a concrete agent session");
  }
  if (sessionKey.startsWith("agent:")) {
    const expected = "agent:" + agentId + ":";
    if (!sessionKey.startsWith(expected) || sessionKey.length === expected.length) {
      throw new TypeError("sessionKey does not belong to agentId");
    }
    return sessionKey;
  }
  return "agent:" + agentId + ":" + sessionKey;
}

type MutableConfig = {
  workspace?: string;
  agentId?: string;
  sessionKey?: string;
  role?: string;
  definition?: string;
  run?: string;
  field: string;
  remote: string;
  branch: string;
  interval: number;
  state?: string;
  mdllmCommand: string;
  mdllmCommandArgs: string[];
  openclawCommand: string;
  openclawCommandArgs: string[];
  timeoutSeconds: number;
};

export function parseBridgeArgs(argv: readonly string[]): WatchBridgeConfig {
  const config: MutableConfig = {
    field: "status",
    remote: "origin",
    branch: "main",
    interval: 60,
    mdllmCommand: "mdllm",
    mdllmCommandArgs: [],
    openclawCommand: "openclaw",
    openclawCommandArgs: [],
    timeoutSeconds: 600,
  };

  const take = (index: number, flag: string): string => {
    const value = argv[index + 1];
    if (value === undefined) {
      throw new TypeError(flag + " requires a value");
    }
    return nonEmpty(value, flag);
  };

  for (let index = 0; index < argv.length; index += 1) {
    const flag = argv[index];
    switch (flag) {
      case "--workspace":
        config.workspace = take(index, flag);
        index += 1;
        break;
      case "--agent-id":
        config.agentId = take(index, flag);
        index += 1;
        break;
      case "--session-key":
        config.sessionKey = take(index, flag);
        index += 1;
        break;
      case "--role":
        config.role = take(index, flag);
        index += 1;
        break;
      case "--definition":
        config.definition = take(index, flag);
        index += 1;
        break;
      case "--run":
        config.run = take(index, flag);
        index += 1;
        break;
      case "--field":
        config.field = take(index, flag);
        index += 1;
        break;
      case "--remote":
        config.remote = take(index, flag);
        index += 1;
        break;
      case "--branch":
        config.branch = take(index, flag);
        index += 1;
        break;
      case "--interval":
        config.interval = positiveInteger(take(index, flag), flag);
        index += 1;
        break;
      case "--state":
        config.state = take(index, flag);
        index += 1;
        break;
      case "--mdllm-command":
        config.mdllmCommand = take(index, flag);
        index += 1;
        break;
      case "--mdllm-arg":
        config.mdllmCommandArgs.push(take(index, flag));
        index += 1;
        break;
      case "--openclaw-command":
        config.openclawCommand = take(index, flag);
        index += 1;
        break;
      case "--openclaw-arg":
        config.openclawCommandArgs.push(take(index, flag));
        index += 1;
        break;
      case "--timeout":
        config.timeoutSeconds = positiveInteger(take(index, flag), flag);
        index += 1;
        break;
      default:
        throw new TypeError("unknown argument: " + String(flag));
    }
  }

  const workspace = nonEmpty(config.workspace, "workspace");
  const agentId = nonEmpty(config.agentId, "agentId");
  const sessionKey = canonicalSessionKey(
    agentId,
    nonEmpty(config.sessionKey, "sessionKey"),
  );

  return Object.freeze({
    workspace,
    agentId,
    sessionKey,
    role: nonEmpty(config.role, "role"),
    definition: nonEmpty(config.definition, "definition"),
    ...(config.run ? { run: config.run } : {}),
    field: config.field,
    remote: config.remote,
    branch: config.branch,
    interval: config.interval,
    ...(config.state ? { state: config.state } : {}),
    mdllmCommand: config.mdllmCommand,
    mdllmCommandArgs: Object.freeze([...config.mdllmCommandArgs]),
    openclawCommand: config.openclawCommand,
    openclawCommandArgs: Object.freeze([...config.openclawCommandArgs]),
    timeoutSeconds: config.timeoutSeconds,
  });
}

export function buildWatchInvocation(
  config: WatchBridgeConfig,
): ProcessInvocation {
  const args = [
    ...config.mdllmCommandArgs,
    "watch",
    config.workspace,
    "--role",
    config.role,
    "--definition",
    config.definition,
    "--field",
    config.field,
    "--remote",
    config.remote,
    "--branch",
    config.branch,
    "--interval",
    String(config.interval),
    "--exit-on-wake",
  ];
  if (config.run) {
    args.push("--run", config.run);
  }
  if (config.state) {
    args.push("--state", config.state);
  }
  return Object.freeze({
    command: config.mdllmCommand,
    args: Object.freeze(args),
    cwd: config.workspace,
    kind: "watch",
  });
}

export function wakeMessage(config: WatchBridgeConfig): string {
  const scope = config.run ? " in run `" + config.run + "`" : "";
  return [
    "MarkdownLLM standing watch signalled a turn for role `" + config.role
      + "` on workflow `" + config.definition + "`" + scope + ".",
    "Re-enter this domain through the installed adapter, read the committed "
      + "workflow state from Git, and take only the declared turn.",
    "The watch already persisted its observation; do not advance workflow "
      + "state from this event alone.",
  ].join(" ");
}

export function buildWakeInvocation(
  config: WatchBridgeConfig,
): ProcessInvocation {
  return Object.freeze({
    command: config.openclawCommand,
    args: Object.freeze([
      ...config.openclawCommandArgs,
      "agent",
      "--agent",
      config.agentId,
      "--session-key",
      config.sessionKey,
      "--message",
      wakeMessage(config),
      "--json",
      "--timeout",
      String(config.timeoutSeconds),
    ]),
    cwd: config.workspace,
    kind: "wake",
  });
}

export const spawnProcess: ProcessRunner = (
  invocation: ProcessInvocation,
): Promise<ProcessResult> => new Promise((resolve) => {
  let settled = false;
  let child: ReturnType<typeof spawn>;
  const forward = (signal: NodeJS.Signals): void => {
    if (!child.killed) {
      child.kill(signal);
    }
  };
  const onInterrupt = (): void => forward("SIGINT");
  const onTerminate = (): void => forward("SIGTERM");
  const finish = (result: ProcessResult): void => {
    if (!settled) {
      settled = true;
      process.removeListener("SIGINT", onInterrupt);
      process.removeListener("SIGTERM", onTerminate);
      resolve(result);
    }
  };
  child = spawn(
    invocation.command,
    [...invocation.args],
    {
      cwd: invocation.cwd,
      shell: false,
      stdio: "inherit",
      windowsHide: true,
    },
  );
  process.once("SIGINT", onInterrupt);
  process.once("SIGTERM", onTerminate);
  child.once("error", (error) => {
    process.stderr.write(
      "markdownllm-openclaw-watch: " + invocation.kind
        + " process failed: " + error.name + "\n",
    );
    finish({
      code: null,
      signal: null,
      error: error.name,
    });
  });
  child.once("exit", (code, signal) => finish({ code, signal }));
});

function signalExitCode(signal: NodeJS.Signals | null): number {
  if (signal === "SIGINT") {
    return 130;
  }
  if (signal === "SIGTERM") {
    return 143;
  }
  return PROCESS_FAILURE;
}

export async function runWatchBridge(
  config: WatchBridgeConfig,
  runner: ProcessRunner = spawnProcess,
): Promise<number> {
  while (true) {
    const watched = await runner(buildWatchInvocation(config));
    if (watched.code === 0) {
      const woke = await runner(buildWakeInvocation(config));
      if (woke.code !== 0) {
        if (woke.signal) {
          return signalExitCode(woke.signal);
        }
        return woke.code === null ? PROCESS_FAILURE : WAKE_FAILURE;
      }
      continue;
    }
    if (watched.signal) {
      return signalExitCode(watched.signal);
    }
    if (watched.code === 1 || watched.code === 2 || watched.code === 3) {
      return watched.code;
    }
    return PROCESS_FAILURE;
  }
}
