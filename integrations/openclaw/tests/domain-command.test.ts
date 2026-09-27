import assert from "node:assert/strict";
import test from "node:test";

import type {
  OpenClawPluginApi,
  PluginCommandContext,
} from "openclaw/plugin-sdk/plugin-entry";

import { parsePluginConfig } from "../dist/core.js";
import {
  createTelegramTopicViaOpenClawCli,
  registerDomainCommand,
} from "../dist/domain-command.js";

function commandContext(
  config: PluginCommandContext["config"],
  args = "",
): PluginCommandContext {
  return {
    channel: "telegram",
    channelId: "telegram",
    isAuthorizedSender: true,
    senderIsOwner: true,
    agentId: "alpha-agent",
    messageThreadId: 77,
    args,
    commandBody: "/domain " + args,
    config,
    to: "telegram:-100123:topic:77",
    requestConversationBinding: async () => ({ status: "unsupported" }) as never,
    detachConversationBinding: async () => ({ removed: false }),
    getCurrentConversationBinding: async () => null,
  };
}

test("topic creation uses OpenClaw's native Telegram action", async () => {
  const calls: string[][] = [];
  const id = await createTelegramTopicViaOpenClawCli(
    {
      accountId: "work",
      chatId: "-100123",
      name: "Engineering",
    },
    async (args) => {
      calls.push([...args]);
      return [
        "OpenClaw diagnostic prelude",
        JSON.stringify({
          action: "topic-create",
          channel: "telegram",
          payload: {
            ok: true,
            topicId: 82,
            name: "Engineering",
            chatId: "-100123",
          },
        }),
      ].join("\n");
    },
  );

  assert.equal(id, 82);
  assert.deepEqual(calls, [[
    "message",
    "thread",
    "create",
    "--channel",
    "telegram",
    "--target",
    "-100123",
    "--thread-name",
    "Engineering",
    "--account",
    "work",
    "--json",
  ]]);
});

test("domain command reports, lists and opens isolated Telegram routes", async () => {
  const hostConfig: any = {
    agents: {
      list: [
        { id: "alpha-agent", workspace: "/domains/alpha-agent" },
        { id: "beta-agent", workspace: "/domains/beta-agent" },
        { id: "broken-agent", workspace: "/domains/broken-agent" },
      ],
    },
    channels: {
      telegram: {
        actions: { createForumTopic: true },
        groups: {
          "-100123": {
            topics: {
              "77": { agentId: "alpha-agent" },
            },
          },
        },
      },
    },
  };
  const pluginConfig = parsePluginConfig({
    domains: {
      alpha: { agentId: "alpha-agent", topicName: "Alpha" },
      beta: { agentId: "beta-agent", topicName: "Engineering" },
      broken: { agentId: "broken-agent" },
    },
  });
  const commands: any[] = [];
  const mutations: any[] = [];
  const created: string[] = [];
  const removed: number[] = [];
  const api = {
    config: hostConfig,
    runtime: {
      agent: {
        resolveAgentWorkspaceDir: (_config: unknown, agentId: string) =>
          "/domains/" + agentId,
      },
      config: {
        async mutateConfigFile(params: any) {
          mutations.push(params.afterWrite);
          await params.mutate(hostConfig, {});
          return { result: undefined, followUp: { requiresRestart: false } };
        },
      },
    },
    registerCommand(command: unknown) {
      commands.push(command);
    },
  } as unknown as OpenClawPluginApi;

  registerDomainCommand(api, pluginConfig, {
    async readDomainName(workspace) {
      if (workspace.endsWith("broken-agent")) {
        throw new Error("invalid domain");
      }
      return workspace.endsWith("beta-agent") ? "Engineering" : "Alpha";
    },
    telegram: {
      async create(params) {
        created.push(params.name);
        return 82;
      },
      async remove(params) {
        removed.push(params.topicId);
      },
    },
  });

  assert.equal(commands.length, 1);
  const handler = commands[0].handler as (
    ctx: PluginCommandContext,
  ) => Promise<{ text?: string }>;

  const denied = await handler({
    ...commandContext(hostConfig),
    senderIsOwner: false,
  });
  assert.match(denied.text ?? "", /Only an OpenClaw owner/);

  const status = await handler(commandContext(hostConfig));
  assert.match(status.text ?? "", /Domain: alpha/);
  assert.match(status.text ?? "", /Workspace: \/domains\/alpha-agent/);

  const unbound = await handler({
    ...commandContext(hostConfig),
    agentId: "beta-agent",
  });
  assert.equal(
    unbound.text,
    "No MarkdownLLM domain is bound to this conversation.",
  );

  const list = await handler(commandContext(hostConfig, "list"));
  assert.match(list.text ?? "", /alpha \(current\)/);
  assert.match(list.text ?? "", /beta \(not open\)/);

  const existing = await handler(commandContext(hostConfig, "open alpha"));
  assert.match(existing.text ?? "", /https:\/\/t\.me\/c\/123\/77/);
  assert.deepEqual(created, []);

  const opened = await handler(commandContext(hostConfig, "open beta"));
  assert.match(opened.text ?? "", /Engineering is ready/);
  assert.match(opened.text ?? "", /https:\/\/t\.me\/c\/123\/82/);
  assert.match(opened.text ?? "", /first message; session-start/);
  assert.deepEqual(created, ["Engineering"]);
  assert.deepEqual(mutations, [{ mode: "auto" }]);
  assert.equal(
    hostConfig.channels.telegram.groups["-100123"].topics["82"].agentId,
    "beta-agent",
  );
  assert.deepEqual(removed, []);

  const refused = await handler(commandContext(hostConfig, "open broken"));
  assert.match(refused.text ?? "", /was refused/);
  assert.deepEqual(created, ["Engineering"]);
});

test("domain command rolls back a topic when route persistence fails", async () => {
  const hostConfig: any = {
    agents: {
      list: [{ id: "beta-agent", workspace: "/domains/beta" }],
    },
    channels: {
      telegram: {
        actions: { createForumTopic: true },
        groups: { "-100123": { topics: {} } },
      },
    },
  };
  const commands: any[] = [];
  const removed: number[] = [];
  const api = {
    config: hostConfig,
    runtime: {
      agent: {
        resolveAgentWorkspaceDir: () => "/domains/beta",
      },
      config: {
        async mutateConfigFile() {
          throw new Error("write failed");
        },
      },
    },
    registerCommand(command: unknown) {
      commands.push(command);
    },
  } as unknown as OpenClawPluginApi;

  registerDomainCommand(
    api,
    parsePluginConfig({
      domains: { beta: { agentId: "beta-agent" } },
    }),
    {
      readDomainName: async () => "Engineering",
      telegram: {
        create: async () => 90,
        async remove(params) {
          removed.push(params.topicId);
        },
      },
    },
  );

  const handler = commands[0].handler as (
    ctx: PluginCommandContext,
  ) => Promise<{ text?: string }>;
  const result = await handler(commandContext(hostConfig, "open beta"));
  assert.match(result.text ?? "", /rolled back/);
  assert.deepEqual(removed, [90]);
});
