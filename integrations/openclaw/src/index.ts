import { definePluginEntry, type OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-entry";

import {
  LifecycleGate,
  buildInvocation,
  contractFingerprint,
  executeLifecycle,
  isDesignatedAgent,
  lifecycleKey,
  parsePluginConfig,
} from "./core.js";

export function registerMarkdownLLMPlugin(
  api: OpenClawPluginApi,
  execute: typeof executeLifecycle = executeLifecycle,
): void {
    const config = parsePluginConfig(api.pluginConfig ?? {});
    const gate = new LifecycleGate();
    const fingerprint = contractFingerprint();

    type LifecycleContext = {
      agentId?: string;
      sessionId?: string;
      sessionKey?: string;
    };
    type LifecycleEvent = {
      previousSessionId?: string;
      reason?: string;
      sessionId?: string;
      sessionKey?: string;
    };

    const sessionIdsByKey = new Map<string, string>();
    const sessionKeysById = new Map<string, string>();
    const messageCountsByKey = new Map<string, number>();

    const remember = (key: string, sessionId: string | undefined): void => {
      if (!sessionId) return;
      const previousSessionId = sessionIdsByKey.get(key);
      if (previousSessionId && previousSessionId !== sessionId) {
        sessionKeysById.delete(previousSessionId);
      }
      sessionIdsByKey.set(key, sessionId);
      sessionKeysById.set(sessionId, key);
    };

    const resolveLifecycleKey = (
      event: LifecycleEvent,
      ctx: LifecycleContext,
    ): string | undefined => {
      const sessionKey = ctx.sessionKey ?? event.sessionKey;
      if (isDesignatedAgent(config, ctx.agentId) && sessionKey) {
        return lifecycleKey(ctx.agentId, sessionKey);
      }
      for (const sessionId of [
        ctx.sessionId,
        event.sessionId,
        event.previousSessionId,
      ]) {
        if (sessionId && sessionKeysById.has(sessionId)) {
          return sessionKeysById.get(sessionId);
        }
      }
      return undefined;
    };

    const invalidate = (
      event: LifecycleEvent,
      ctx: LifecycleContext,
    ): string | undefined => {
      const key = resolveLifecycleKey(event, ctx);
      if (key) {
        gate.invalidate(key);
      }
      return key;
    };

    const invalidateLifecycleBoundary = (
      event: LifecycleEvent,
      ctx: LifecycleContext,
    ): void => {
      if (invalidate(event, ctx)) return;
      // OpenClaw may emit reset/compaction hooks without any session identity.
      // Re-running a read-only projection is safer than retaining a stale gate.
      for (const key of sessionIdsByKey.keys()) {
        gate.invalidate(key);
      }
    };

    api.on("session_start", (event, ctx) => {
      const key = invalidate(event, ctx);
      if (key) {
        remember(key, ctx.sessionId ?? event.sessionId);
      }
    });
    api.on("before_reset", (event, ctx) => {
      invalidateLifecycleBoundary(event, ctx);
    });
    api.on("after_compaction", (event, ctx) => {
      invalidateLifecycleBoundary(event, ctx);
    });
    api.on("session_end", (event, ctx) => {
      const key = invalidate(event, ctx);
      const sessionId = ctx.sessionId ?? event.sessionId;
      if (key && sessionId && event.reason !== "compaction") {
        sessionKeysById.delete(sessionId);
        if (sessionIdsByKey.get(key) === sessionId) {
          sessionIdsByKey.delete(key);
          messageCountsByKey.delete(key);
        }
      }
    });

    api.on(
      "before_prompt_build",
      async (event, ctx) => {
        if (!isDesignatedAgent(config, ctx.agentId)) {
          return;
        }

        const key = lifecycleKey(ctx.agentId, ctx.sessionKey);
        if (!key) {
          return {
            prependContext: [
              "<markdownllm-adapter outcome=\"unbound\">",
              "OpenClaw did not provide a canonical session key.",
              "MarkdownLLM domain binding was refused for this turn.",
              "</markdownllm-adapter>",
            ].join("\n"),
          };
        }
        if (ctx.sessionId) {
          const previousSessionId = sessionIdsByKey.get(key);
          if (previousSessionId && previousSessionId !== ctx.sessionId) {
            gate.invalidate(key);
          }
          remember(key, ctx.sessionId);
        }
        if (Array.isArray(event.messages)) {
          const messageCount = event.messages.length;
          const previousMessageCount = messageCountsByKey.get(key);
          if (previousMessageCount !== undefined
              && messageCount < previousMessageCount) {
            gate.invalidate(key);
          }
          messageCountsByKey.set(key, messageCount);
        }
        if (!gate.claim(key, fingerprint)) {
          return;
        }

        try {
          const workspace = api.runtime.agent.resolveAgentWorkspaceDir(
            api.config,
            ctx.agentId,
          );
          const result = await execute(
            buildInvocation(config, workspace, fingerprint),
          );
          if (result.ok) {
            gate.complete(key, fingerprint);
          } else {
            gate.release(key, fingerprint);
            api.logger.warn(
              "MarkdownLLM session-start unavailable: "
                + (result.errorKind ?? "unknown"),
            );
          }
          return { prependContext: result.context };
        } catch (error) {
          gate.release(key, fingerprint);
          const kind = error instanceof Error ? error.name : "Error";
          api.logger.warn("MarkdownLLM binding failed: " + kind);
          return {
            prependContext: [
              "<markdownllm-adapter outcome=\"unavailable\">",
              "MarkdownLLM domain binding failed before session-start.",
              "Failure class: " + kind + ".",
              "</markdownllm-adapter>",
            ].join("\n"),
          };
        }
      },
      { timeoutMs: config.timeoutMs + 5_000 },
    );
}

export default definePluginEntry({
  id: "markdownllm",
  name: "MarkdownLLM",
  description: "Bind designated OpenClaw agents to MarkdownLLM lifecycle context",
  register: registerMarkdownLLMPlugin,
});
