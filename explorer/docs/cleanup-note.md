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

The screenshots in the current guide were captured from the generated
**Northstar Studio** estate at the intentionally generic path
`C:\MarkdownLLM-Public-Demo`.
