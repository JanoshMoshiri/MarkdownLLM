import { createHash } from "node:crypto";
import { execFile } from "node:child_process";

export const PLUGIN_ID = "markdownllm";
export const DEFAULT_TIMEOUT_MS = 115_000;
export const MAX_OUTPUT_BYTES = 512 * 1024;

export const LIFECYCLE_CONTRACT = Object.freeze({
  version: 2,
  harness: "openclaw",
  moment: "session-start",
  delivery: "prependContext",
  invocation: [
    "harness-event",
    "openclaw",
    "session-start",
    "{workspace}",
    "{definitionHash}",
  ],
});

export type DomainDefinition = Readonly<{
  id: string;
  agentId: string;
  topicName?: string;
}>;

export type PluginConfig = Readonly<{
  domains: readonly DomainDefinition[];
  command: string;
  commandArgs: readonly string[];
  timeoutMs: number;
}>;

export type LifecycleInvocation = Readonly<{
  command: string;
  args: readonly string[];
  cwd: string;
  timeoutMs: number;
}>;

export type LifecycleResult = Readonly<{
  ok: boolean;
  context: string;
  errorKind?: string;
}>;

function nonEmptyString(value: unknown, field: string): string {
  if (typeof value !== "string" || value.trim().length === 0) {
    throw new TypeError(field + " must be a non-empty string");
  }
  return value.trim();
}

export function parsePluginConfig(raw: Record<string, unknown>): PluginConfig {
  if (typeof raw.domains !== "object"
      || raw.domains === null
      || Array.isArray(raw.domains)
      || Object.keys(raw.domains).length === 0) {
    throw new TypeError("domains must contain at least one domain");
  }
  const domains = Object.entries(raw.domains).map(([id, value]) => {
    if (!/^[a-z0-9][a-z0-9_-]*$/.test(id)) {
      throw new TypeError(
        "domain ids must use lowercase letters, numbers, hyphens or underscores",
      );
    }
    if (typeof value !== "object" || value === null || Array.isArray(value)) {
      throw new TypeError("domains." + id + " must be an object");
    }
    const record = value as Record<string, unknown>;
    const agentId = nonEmptyString(record.agentId, "domains." + id + ".agentId");
    const topicName = record.topicName === undefined
      ? undefined
      : nonEmptyString(record.topicName, "domains." + id + ".topicName");
    if (topicName !== undefined && topicName.length > 128) {
      throw new TypeError("domains." + id + ".topicName must be at most 128 characters");
    }
    return Object.freeze(topicName === undefined
      ? { id, agentId }
      : { id, agentId, topicName });
  });
  const agentIds = domains.map((domain) => domain.agentId);
  if (new Set(agentIds).size !== agentIds.length) {
    throw new TypeError("each domain must use a unique agentId");
  }

  const command = raw.command === undefined
    ? "mdllm"
    : nonEmptyString(raw.command, "command");
  const commandArgs = raw.commandArgs === undefined
    ? []
    : raw.commandArgs;
  if (!Array.isArray(commandArgs)) {
    throw new TypeError("commandArgs must be an array of strings");
  }
  const parsedCommandArgs = commandArgs.map((value, index) =>
    nonEmptyString(value, "commandArgs[" + index + "]"));
  const timeoutMs = raw.timeoutMs === undefined
    ? DEFAULT_TIMEOUT_MS
    : raw.timeoutMs;
  if (!Number.isSafeInteger(timeoutMs)
      || Number(timeoutMs) < 1_000
      || Number(timeoutMs) > 120_000) {
    throw new TypeError("timeoutMs must be an integer from 1000 to 120000");
  }

  return Object.freeze({
    domains: Object.freeze(domains),
    command,
    commandArgs: Object.freeze(parsedCommandArgs),
    timeoutMs: Number(timeoutMs),
  });
}

export function isDesignatedAgent(
  config: PluginConfig,
  agentId: string | undefined,
): agentId is string {
  return typeof agentId === "string"
    && config.domains.some((domain) => domain.agentId === agentId);
}

export function domainById(
  config: PluginConfig,
  domainId: string,
): DomainDefinition | undefined {
  return config.domains.find((domain) => domain.id === domainId);
}

export function domainForAgent(
  config: PluginConfig,
  agentId: string | undefined,
): DomainDefinition | undefined {
  return config.domains.find((domain) => domain.agentId === agentId);
}

export function lifecycleKey(
  agentId: string | undefined,
  sessionKey: string | undefined,
): string | undefined {
  if (!agentId || !sessionKey) {
    return undefined;
  }
  return agentId + ":" + sessionKey;
}

export function contractFingerprint(
  contract: object = LIFECYCLE_CONTRACT,
): string {
  return "sha256:" + createHash("sha256")
    .update(JSON.stringify(contract))
    .digest("hex");
}

export function buildInvocation(
  config: PluginConfig,
  workspace: string,
  fingerprint = contractFingerprint(),
): LifecycleInvocation {
  const cwd = nonEmptyString(workspace, "workspace");
  return Object.freeze({
    command: config.command,
    args: Object.freeze([
      ...config.commandArgs,
      "harness-event",
      "openclaw",
      "session-start",
      cwd,
      fingerprint,
    ]),
    cwd,
    timeoutMs: config.timeoutMs,
  });
}

type GateState = Readonly<{
  fingerprint: string;
  state: "running" | "complete";
}>;

export class LifecycleGate {
  readonly #state = new Map<string, GateState>();

  claim(key: string, fingerprint: string): boolean {
    const current = this.#state.get(key);
    if (current?.fingerprint === fingerprint) {
      return false;
    }
    this.#state.set(key, { fingerprint, state: "running" });
    return true;
  }

  complete(key: string, fingerprint: string): void {
    const current = this.#state.get(key);
    if (current?.fingerprint === fingerprint) {
      this.#state.set(key, { fingerprint, state: "complete" });
    }
  }

  release(key: string, fingerprint: string): void {
    const current = this.#state.get(key);
    if (current?.fingerprint === fingerprint) {
      this.#state.delete(key);
    }
  }

  invalidate(key: string | undefined): void {
    if (key) {
      this.#state.delete(key);
    }
  }

  inspect(key: string): GateState | undefined {
    return this.#state.get(key);
  }
}

type ExecFileLike = typeof execFile;

function failureContext(kind: string): string {
  return [
    "<markdownllm-adapter outcome=\"unavailable\">",
    "MarkdownLLM session-start could not run.",
    "Failure class: " + kind + ".",
    "The domain binding was not certified for this turn.",
    "</markdownllm-adapter>",
  ].join("\n");
}

export function executeLifecycle(
  invocation: LifecycleInvocation,
  runner: ExecFileLike = execFile,
): Promise<LifecycleResult> {
  return new Promise((resolve) => {
    runner(
      invocation.command,
      [...invocation.args],
      {
        cwd: invocation.cwd,
        timeout: invocation.timeoutMs,
        maxBuffer: MAX_OUTPUT_BYTES,
        windowsHide: true,
        shell: false,
        encoding: "utf8",
      },
      (error, stdout) => {
        const context = typeof stdout === "string" ? stdout.trim() : "";
        if (error) {
          const kind = error.name || "Error";
          resolve({
            ok: false,
            context: context || failureContext(kind),
            errorKind: kind,
          });
          return;
        }
        if (!context) {
          resolve({
            ok: false,
            context: failureContext("EmptyOutput"),
            errorKind: "EmptyOutput",
          });
          return;
        }
        resolve({ ok: true, context });
      },
    );
  });
}
