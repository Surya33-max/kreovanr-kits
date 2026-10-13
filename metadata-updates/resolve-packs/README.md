# Resolve Pack Metadata Updates

The current metadata-update batch includes 13 separate DaVinci Resolve .drfx packages. A local rewrite run checked 1,514 ZIP entries, tagged 757 Fusion settings, appended a packaging note to 485 existing Resolve Comments fields, and reopened all 13 generated archives successfully. Every non-.setting archive entry was verified byte-for-byte unchanged.

Files in this folder:
- METADATA_CHANGELOG.md: summary and limits.
- metadata-manifest.json: source/output SHA-256 values and per-package verification summary.
- metadata-audit.csv: spreadsheet-friendly detail.

The individual .drfx binaries have not been committed to this GitHub branch by the connector. Run the committed tool from an authenticated local clone to add each output as a separate file:

    python3 tools/resolve-pack-manager/resolve_pack_manager.py rewrite /path/to/original-packs --output-dir ./processed-packs --report-dir ./audit --push-repo /path/to/kreovanr-kits

The script stages separate files under release-assets/resolve-packs and pushes with your configured local Git credentials. Do not redistribute any third-party pack unless permission and license terms allow it. Original attribution text is preserved.
