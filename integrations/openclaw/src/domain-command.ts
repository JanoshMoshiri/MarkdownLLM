import { execFile } from "node:child_process";
import { readFile, stat } from "node:fs/promises";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

import type {
  OpenClawConfig,
  OpenClawPluginApi,
  PluginCommandContext,
  PluginCommandResult,
} from "openclaw/plugin-sdk/plugin-entry";
import { resolveTelegramAccount } from "openclaw/plugin-sdk/telegram-account";

import {
  type DomainDefinition,
  type PluginConfig,
  domainById,
  domainForAgent,
} from "./core.js";

type JsonObject = Record<string, unknown>;

type OpenClawCliExecutor = (args: readonly string[]) => Promise<string>;

const execFileAsync = promisify(execFile);

type TelegramTopicOps = Readonly<{
  create: (params: {
    config: OpenClawConfig;
    accountId: string | undefined;
    chatId: string;
    name: string;
  }) => Promise<number>;
  remove: (params: {
    config: OpenClawConfig;
    accountId: string | undefined;
    chatId: string;
    topicId: number;
  }) => Promise<void>;
}>;

export type DomainCommandDependencies = Readonly<{
  readDomainName?: (workspace: string) => Promise<string>;
  telegram?: TelegramTopicOps;
}>;

type DomainCommandState = Readonly<{
  pendingOpens: Map<string, Promise<PluginCommandResult>>;
  openedTopics: Map<string, number>;
}>;

function asObject(value: unknown): JsonObject | undefined {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? value as JsonObject
    : undefined;
}

function ensureObject(parent: JsonObject, key: string): JsonObject {
  const current = parent[key];
  if (current === undefined) {
    const created: JsonObject = {};
    parent[key] = created;
    return created;
  }
  const record = asObject(current);
  if (!record) {
    throw new TypeError(key + " must be an object");
  }
  return record;
}

function stripYamlScalar(value: string): string {
  const trimmed = value.trim();
  if (trimmed.length >= 2
      && ((trimmed.startsWith('"') && trimmed.endsWith('"'))
        || (trimmed.startsWith("'") && trimmed.endsWith("'")))) {
    return trimmed.slice(1, -1).trim();
  }
  return trimmed;
}

export async function readDomainName(workspace: string): Promise<string> {
  const agentsPath = join(workspace, "AGENTS.md");
  const metadata = await stat(agentsPath);
  if (!metadata.isFile() || metadata.size > 128 * 1024) {
    throw new Error("AGENTS.md is missing or too large");
  }
  const source = (await readFile(agentsPath, "utf8")).replace(/\r\n/g, "\n");
  if (!source.startsWith("---\n")) {
    throw new Error("AGENTS.md has no YAML frontmatter");
  }
  const end = source.indexOf("\n---", 4);
  if (end < 0) {
    throw new Error("AGENTS.md frontmatter is not closed");
  }
  const match = source.slice(4, end).match(/^name:\s*(.+?)\s*$/m);
  const name = match ? stripYamlScalar(match[1] ?? "") : "";
  if (!name) {
    throw new Error("AGENTS.md has no domain name");
  }
  return name;
}

function extractChatId(ctx: PluginCommandContext): string | undefined {
  for (const candidate of [ctx.to, ctx.channelId]) {
    if (candidate === undefined) continue;
    const match = String(candidate).match(/(?:telegram:)?(-100\d+|-?\d+)/);
    if (match?.[1]) return match[1];
  }
  return undefined;
}

function topicId(value: unknown): number | undefined {
  const parsed = typeof value === "number" ? value : Number(value);
  return Number.isSafeInteger(parsed) && parsed > 0 ? parsed : undefined;
}

function telegramConfigRoot(config: OpenClawConfig): JsonObject | undefined {
  return asObject(asObject(config.channels)?.telegram);
}

function groupConfigOwner(
  config: OpenClawConfig,
  accountId: string | undefined,
): JsonObject | undefined {
  const telegram = telegramConfigRoot(config);
  if (!telegram) return undefined;
  const accounts = asObject(telegram.accounts);
  const account = accountId ? asObject(accounts?.[accountId]) : undefined;
  return account && Object.hasOwn(account, "groups") ? account : telegram;
}

function configuredTopics(
  config: OpenClawConfig,
  accountId: string | undefined,
  chatId: string,
): JsonObject {
  const owner = groupConfigOwner(config, accountId);
  const groups = asObject(owner?.groups);
  const group = asObject(groups?.[chatId]);
  return asObject(group?.topics) ?? {};
}

function findTopicForAgent(
  config: OpenClawConfig,
  accountId: string | undefined,
  chatId: string,
  agentId: string,
): number | undefined {
  for (const [id, raw] of Object.entries(
    configuredTopics(config, accountId, chatId),
  )) {
    if (id === "*") continue;
    if (asObject(raw)?.agentId === agentId) {
      const parsed = topicId(id);
      if (parsed) return parsed;
    }
  }
  return undefined;
}

function topicLink(chatId: string, id: number): string {
  if (!chatId.startsWith("-100")) {
    throw new Error("Domain topics require a Telegram supergroup");
  }
  return "https://t.me/c/" + chatId.slice(4) + "/" + id;
}

async function executeOpenClawCli(args: readonly string[]): Promise<string> {
  const cliEntry = fileURLToPath(import.meta.resolve("openclaw/cli-entry"));
  const result = await execFileAsync(
    process.execPath,
    [cliEntry, ...args],
    {
      encoding: "utf8",
      maxBuffer: 1024 * 1024,
      timeout: 20_000,
      windowsHide: true,
    },
  );
  return String(result.stdout);
}

function parseOpenClawCliResult(stdout: string): JsonObject {
  const start = stdout.indexOf("{");
  const end = stdout.lastIndexOf("}");
  if (start < 0 || end < start) {
    throw new Error("OpenClaw returned no JSON result");
  }
  const parsed = JSON.parse(stdout.slice(start, end + 1)) as unknown;
  const result = asObject(parsed);
  if (!result) throw new Error("OpenClaw returned an invalid JSON result");
  return result;
}

export async function createTelegramTopicViaOpenClawCli(
  params: {
    accountId: string | undefined;
    chatId: string;
    name: string;
  },
  execute: OpenClawCliExecutor = executeOpenClawCli,
): Promise<number> {
  const args = [
    "message",
    "thread",
    "create",
    "--channel",
    "telegram",
    "--target",
    params.chatId,
    "--thread-name",
    params.name,
  ];
  if (params.accountId) args.push("--account", params.accountId);
  args.push("--json");

  const result = parseOpenClawCliResult(await execute(args));
  const payload = asObject(result.payload) ?? result;
  const id = topicId(payload.topicId);
  if (payload.ok !== true || !id) {
    throw new Error("OpenClaw returned no topic id");
  }
  return id;
}

async function telegramRequest<T>(
  config: OpenClawConfig,
  accountId: string | undefined,
  method: string,
  body: JsonObject,
): Promise<T> {
  const account = resolveTelegramAccount({ cfg: config, accountId: accountId ?? null });
  if (!account.enabled || !account.token) {
    throw new Error("The Telegram account is not enabled or has no token");
  }
  try {
    const response = await fetch(
      "https://api.telegram.org/bot" + account.token + "/" + method,
      {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(body),
        signal: AbortSignal.timeout(15_000),
      },
    );
    const payload = await response.json() as {
      ok?: boolean;
      result?: T;
    };
    if (!response.ok || payload.ok !== true || payload.result === undefined) {
      throw new Error("Telegram rejected the request");
    }
    return payload.result;
  } catch {
    throw new Error("Telegram topic operation failed");
  }
}

const defaultTelegramOps: TelegramTopicOps = Object.freeze({
  async create({ config, accountId, chatId, name }) {
    const account = resolveTelegramAccount({ cfg: config, accountId: accountId ?? null });
    if (asObject(account.config.actions)?.createForumTopic !== true) {
      throw new Error(
        "Telegram topic creation is disabled; enable actions.createForumTopic",
      );
    }
    return createTelegramTopicViaOpenClawCli({ accountId, chatId, name });
  },
  async remove({ config, accountId, chatId, topicId: id }) {
    await telegramRequest<boolean>(
      config,
      accountId,
      "deleteForumTopic",
      { chat_id: chatId, message_thread_id: id },
    );
  },
});

function hasConfiguredAgent(config: OpenClawConfig, agentId: string): boolean {
  const agents = asObject(config.agents);
  const entries = asObject(agents?.entries);
  if (asObject(entries?.[agentId])) return true;

  return Array.isArray(agents?.list)
    && agents.list.some((entry) => asObject(entry)?.id === agentId);
}

async function resolveDomain(
  api: OpenClawPluginApi,
  hostConfig: OpenClawConfig,
  domain: DomainDefinition,
  reader: (workspace: string) => Promise<string>,
): Promise<{ domainName: string; workspace: string }> {
  if (!hasConfiguredAgent(hostConfig, domain.agentId)) {
    throw new Error("The domain agent is not configured");
  }
  const workspace = api.runtime.agent.resolveAgentWorkspaceDir(
    hostConfig,
    domain.agentId,
  );
  const domainName = await reader(workspace);
  return { domainName, workspace };
}

function hasOperatorAuthority(ctx: PluginCommandContext): boolean {
  return ctx.senderIsOwner === true
    || ctx.gatewayClientScopes?.includes("operator.admin") === true;
}

function currentStatus(
  api: OpenClawPluginApi,
  config: PluginConfig,
  ctx: PluginCommandContext,
): PluginCommandResult {
  const domain = domainForAgent(config, ctx.agentId);
  if (!domain || !hasConfiguredAgent(ctx.config, domain.agentId)) {
    return { text: "No MarkdownLLM domain is bound to this conversation." };
  }
  if (ctx.channel === "telegram") {
    const chatId = extractChatId(ctx);
    const currentTopic = topicId(ctx.messageThreadId);
    const routedTopic = chatId
      ? findTopicForAgent(ctx.config, ctx.accountId, chatId, domain.agentId)
      : undefined;
    if (!currentTopic || routedTopic !== currentTopic) {
      return {
        text: "No MarkdownLLM domain is bound to this conversation.",
      };
    }
  }
  const workspace = api.runtime.agent.resolveAgentWorkspaceDir(
    ctx.config,
    domain.agentId,
  );
  return {
    text: [
      "Domain: " + domain.id,
      "Agent: " + domain.agentId,
      "Workspace: " + workspace,
      "Telegram topic: " + (ctx.messageThreadId ?? "none"),
    ].join("\n"),
  };
}

function listDomains(
  config: PluginConfig,
  ctx: PluginCommandContext,
): PluginCommandResult {
  const chatId = extractChatId(ctx);
  const lines = config.domains.map((domain) => {
    const route = chatId
      ? findTopicForAgent(ctx.config, ctx.accountId, chatId, domain.agentId)
      : undefined;
    const currentTopic = topicId(ctx.messageThreadId);
    const state = domain.agentId === ctx.agentId && route === currentTopic
      ? "current"
      : route
        ? "topic " + route
        : "not open";
    return "- " + domain.id + " (" + state + ")";
  });
  return { text: ["Available MarkdownLLM domains:", ...lines].join("\n") };
}

function persistTopicRoute(
  api: OpenClawPluginApi,
  accountId: string | undefined,
  chatId: string,
  id: number,
  agentId: string,
): Promise<unknown> {
  return api.runtime.config.mutateConfigFile({
    afterWrite: { mode: "auto" },
    mutate(draft) {
      const root = draft as unknown as JsonObject;
      const channels = ensureObject(root, "channels");
      const telegram = ensureObject(channels, "telegram");
      const accounts = asObject(telegram.accounts);
      const account = accountId ? asObject(accounts?.[accountId]) : undefined;
      const owner = account && Object.hasOwn(account, "groups")
        ? account
        : telegram;
      const groups = ensureObject(owner, "groups");
      const group = ensureObject(groups, chatId);
      const topics = ensureObject(group, "topics");
      const current = asObject(topics[String(id)]) ?? {};
      topics[String(id)] = { ...current, agentId };
    },
  });
}

async function openDomain(
  api: OpenClawPluginApi,
  config: PluginConfig,
  ctx: PluginCommandContext,
  id: string,
  dependencies: Required<DomainCommandDependencies>,
  state: DomainCommandState,
): Promise<PluginCommandResult> {
  if (ctx.channel !== "telegram") {
    return { text: "/domain open is available only from Telegram." };
  }
  const chatId = extractChatId(ctx);
  if (!chatId) {
    return { text: "Could not identify the current Telegram group." };
  }
  const domain = domainById(config, id);
  if (!domain) {
    return { text: "Unknown domain '" + id + "'. Use /domain list." };
  }
  const routeKey = (ctx.accountId ?? "default") + ":" + chatId + ":"
    + domain.agentId;

  let verified: { domainName: string; workspace: string };
  try {
    verified = await resolveDomain(
      api,
      ctx.config,
      domain,
      dependencies.readDomainName,
    );
  } catch {
    return {
      text: "Domain '" + id
        + "' was refused: its agent or AGENTS.md domain is not valid.",
    };
  }

  const existing = findTopicForAgent(
    ctx.config,
    ctx.accountId,
    chatId,
    domain.agentId,
  );
  const cached = state.openedTopics.get(routeKey);
  const routed = existing ?? cached;
  if (routed) {
    return {
      text: verified.domainName + " is already open:\n"
        + topicLink(chatId, routed),
    };
  }

  const pendingKey = routeKey;
  const inFlight = state.pendingOpens.get(pendingKey);
  if (inFlight) return inFlight;

  const operation = (async (): Promise<PluginCommandResult> => {
    let created: number;
    try {
      created = await dependencies.telegram.create({
        config: ctx.config,
        accountId: ctx.accountId,
        chatId,
        name: domain.topicName ?? verified.domainName,
      });
    } catch (error) {
      const disabled = error instanceof Error
        && error.message.startsWith("Telegram topic creation is disabled");
      return {
        text: disabled
          ? error.message
          : "Telegram could not open the domain topic.",
      };
    }

    try {
      await persistTopicRoute(
        api,
        ctx.accountId,
        chatId,
        created,
        domain.agentId,
      );
    } catch {
      try {
        await dependencies.telegram.remove({
          config: ctx.config,
          accountId: ctx.accountId,
          chatId,
          topicId: created,
        });
      } catch {
        return {
          text: "The route could not be saved and rollback failed. "
            + "Orphan Telegram topic: " + created + ".",
        };
      }
      return {
        text: "The route could not be saved; the new topic was rolled back.",
      };
    }

    state.openedTopics.set(routeKey, created);
    return {
      text: [
        verified.domainName + " is ready in its own topic:",
        topicLink(chatId, created),
        "Open it and send the first message; session-start will run there.",
      ].join("\n"),
    };
  })();

  state.pendingOpens.set(pendingKey, operation);
  try {
    return await operation;
  } finally {
    if (state.pendingOpens.get(pendingKey) === operation) {
      state.pendingOpens.delete(pendingKey);
    }
  }
}

export function registerDomainCommand(
  api: OpenClawPluginApi,
  config: PluginConfig,
  supplied: DomainCommandDependencies = {},
): void {
  const dependencies: Required<DomainCommandDependencies> = {
    readDomainName: supplied.readDomainName ?? readDomainName,
    telegram: supplied.telegram ?? defaultTelegramOps,
  };
  const state: DomainCommandState = {
    pendingOpens: new Map(),
    openedTopics: new Map(),
  };

  api.registerCommand({
    name: "domain",
    description: "Show, list or open a MarkdownLLM domain",
    channels: ["telegram"],
    acceptsArgs: true,
    requireAuth: true,
    requiredScopes: ["operator.admin"],
    exposeSenderIsOwner: true,
    async handler(ctx) {
      if (!hasOperatorAuthority(ctx)) {
        return { text: "Only an OpenClaw owner can open domains." };
      }
      const args = (ctx.args ?? "").trim().split(/\s+/).filter(Boolean);
      if (args.length === 0) {
        return currentStatus(api, config, ctx);
      }
      if (args.length === 1 && args[0] === "list") {
        return listDomains(config, ctx);
      }
      if (args.length === 2 && args[0] === "open") {
        return openDomain(api, config, ctx, args[1] ?? "", dependencies, state);
      }
      return {
        text: "Usage: /domain, /domain list, or /domain open <domain>",
      };
    },
  });
}
