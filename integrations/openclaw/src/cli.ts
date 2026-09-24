#!/usr/bin/env node
import { parseBridgeArgs, runWatchBridge } from "./watch-bridge.js";

const HELP = `Usage: markdownllm-openclaw-watch [options]

Required:
  --workspace PATH
  --agent-id ID
  --session-key KEY
  --role ROLE
  --definition ID

Optional:
  --run ID
  --field FIELD                 default: status
  --remote NAME                 default: origin
  --branch NAME                 default: main
  --interval SECONDS            default: 60
  --state PATH
  --mdllm-command COMMAND       default: mdllm
  --mdllm-arg ARG               repeatable prefix argument
  --openclaw-command COMMAND    default: openclaw
  --openclaw-arg ARG            repeatable prefix argument
  --timeout SECONDS             OpenClaw turn timeout; default: 600
  --help

The bridge runs mdllm watch --exit-on-wake, invokes one exact OpenClaw
agent/session turn on exit 0, waits for that turn, then rearms the watch.
Exit 1 reports a failed watch, 2 an arming refusal, 3 an existing watcher,
4 a failed or ambiguous OpenClaw turn, and 5 a process launch failure.
`;

async function main(): Promise<number> {
  if (process.argv.slice(2).includes("--help")) {
    process.stdout.write(HELP);
    return 0;
  }
  try {
    return await runWatchBridge(parseBridgeArgs(process.argv.slice(2)));
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    process.stderr.write("markdownllm-openclaw-watch: " + message + "\n");
    return 2;
  }
}

process.exitCode = await main();
