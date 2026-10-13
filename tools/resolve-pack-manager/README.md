# Kreovant Resolve Pack Manager

REA-inspired, local-first tooling for inspecting and repackaging DaVinci Resolve .drfx archives. Inspired by the evidence-first workflow of https://github.com/morluto/rea; this is an original utility, not a fork and not affiliated with REA or Blackmagic Design.

## What it does
- Inspects .drfx ZIP containers and inventories Fusion .setting files and preview assets.
- Fingerprints source and output files with SHA-256.
- Adds transparent Kreovant packaging notes without replacing existing creator attribution or license text.
- Updates visible Resolve Comments fields by appending a packaging note while preserving the existing comments.
- Rebuilds each archive and verifies archive readability, path safety, and unchanged non-setting assets.
- Can stage separate .drfx outputs in an authenticated local Git checkout and push them using the user's normal git credentials.

## Safety
The notes identify packaging/metadata curation only; they do not claim Kreovant created the original effects. Keep author and license notices. Redistribute only where permission and the applicable license allow it. Archive checks are not a substitute for testing in DaVinci Resolve.

## Local use
Requires Python 3.10+ and Git for the optional push step. No third-party Python packages.

    python3 resolve_pack_manager.py inspect /path/to/packs --report-dir ./audit
    python3 resolve_pack_manager.py rewrite /path/to/packs --output-dir ./processed-packs --report-dir ./audit
    python3 resolve_pack_manager.py rewrite /path/to/packs --output-dir ./processed-packs --report-dir ./audit --push-repo /path/to/kreovanr-kits

The optional --push-repo flag copies each updated .drfx into release-assets/resolve-packs/, copies audit reports, commits, and pushes the current branch using local Git credentials. No access token is stored by this utility.

## Audit summary for this batch
- 13 original .drfx packages inspected and rewritten.
- 1,514 archive entries checked.
- 757 .setting files tagged.
- 485 existing visible comment fields updated with a packaging note.
- All 13 resulting archives reopened successfully.
- Preview assets and every non-.setting file were byte-for-byte unchanged.
- Original creator text was retained; packs still need real DaVinci Resolve QA.
