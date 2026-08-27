# Note to self — documentation clean-up

Run this short pass whenever the public Explorer guides or screenshots change.

- [ ] Rebuild the fictional estate from
  `tools/build_public_demo_estate.py`; never substitute a live estate.
- [ ] Check every screenshot for personal names, real domain names, private
  file content, capability tokens and user-profile paths.
- [ ] Keep only images referenced by the installation or user guide.
- [ ] Remove generated estates from `explorer/build/` and any temporary public
  demo path after capture. The generator stays; its output does not.
- [ ] Check the installer filename and documented Windows behaviour against the
  release candidate.
- [ ] Run the documentation tests and open both guides once at normal width and
  once on a narrow screen.
- [ ] Confirm the README links still work, then commit the guide, screenshots
  and evidence together.

Before producing a public release candidate, also inspect the ignored local
construction surface and remove only the generated outputs that can be rebuilt:

- [ ] Remove `explorer/.windows-build-tools/`,
  `explorer/.windows-build-venv/`, `explorer/build/`, `explorer/dist/`,
  `explorer/src/markdownllm_explorer.egg-info/`, Python bytecode and test/tool
  caches after the operator has finished reviewing the current build.
- [ ] Keep the packaging sources, fictional-estate generator, documentation
  sources and committed test evidence.
- [ ] Rebuild the installer from the final immutable candidate rather than
  retaining an earlier generated executable.
- [ ] Run `git status --ignored` and `git ls-files` to prove that ignored build
  output has not entered the tracked release surface.

This note is the clean-up checklist, not authority to delete the current local
build before review. The working construction output remains recoverable from
source and should be removed at the release gate.

The screenshots in the current guide were captured from the generated
**Northstar Studio** estate at the intentionally generic path
`C:\MarkdownLLM-Public-Demo`.
