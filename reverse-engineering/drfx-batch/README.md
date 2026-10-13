# Kreovant DRFX Reverse-Engineering and Test Bundle

Static audit records for 13 DaVinci Resolve `.drfx` archives.

## Files

- `DEEP_STATIC_AUDIT.md`: batch-level findings and limitations.
- `deep-analysis.json`: detailed per-package and per-setting inventory, hashes, and control counts.
- The downloadable test bundle contains extracted archive contents, original input archives, per-package `analysis.json` reports, and `TEST_CHECKLIST.md` files.

**Runtime status:** archive integrity checks passed. Resolve import, UI inspection, and render tests are still pending. Do not treat static inspection as a guarantee that every item works.
