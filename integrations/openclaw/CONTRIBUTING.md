# Contributing

The adapter is part of the MarkdownLLM repository. Open an issue before
changing its OpenClaw seam, lifecycle ownership or compatibility range.

## Required checks

From `integrations/openclaw`:

```bash
npm ci
npm test
npm run test:install
npm pack --dry-run --json
```

From the MarkdownLLM repository root:

```bash
python -m pytest tools/tests/test_openclaw_adapter.py tools/tests/test_lifecycle_runner.py tools/tests/test_watch.py -q
python tools/mdllm.py validate .
python tools/mdllm.py index . check
```

Keep BookRite and private-estate data outside adapter fixtures and evidence.
Do not add private OpenClaw distribution imports, direct session/transcript
storage access, trusted-only Gateway calls or a second workflow scheduler.

See the repository root `CONTRIBUTING.md` for commit, Thing and pull-request
conventions.
