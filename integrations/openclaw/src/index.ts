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

    const invalidate = (
      ctx: { agentId?: string; sessionKey?: string },
    ): void => {
      if (!isDesignatedAgent(config, ctx.agentId)) {
        return;
      }
      gate.invalidate(lifecycleKey(ctx.agentId, ctx.sessionKey));
    };

    api.on("session_start", (_event, ctx) => invalidate(ctx));
    api.on("before_reset", (_event, ctx) => invalidate(ctx));
    api.on("after_compaction", (_event, ctx) => invalidate(ctx));
    api.on("session_end", (_event, ctx) => invalidate(ctx));

    api.on(
      "before_prompt_build",
      async (_event, ctx) => {
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
