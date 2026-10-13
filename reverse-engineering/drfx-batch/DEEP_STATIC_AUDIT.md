# Kreovant DRFX Deep Static Audit

Generated: 2026-10-13 UTC

**Scope:** static archive validation, inventory, extracted Fusion settings, and lightweight node/control census. This does not prove that DaVinci Resolve can load or render these packages.

## Batch results

- Archive files: **13**
- Unique binaries: **13**
- ZIP CRC checks passed: **13**
- Fusion setting files: **757**
- Other assets: **650**
- Exposed-control declarations: **52,416** (text-pattern estimate)
- Expression markers: **9,531** (text-pattern estimate)

## Package matrix

| Package | ZIP/CRC | Settings | Assets | Controls | Expressions |
|---|---|---:|---:|---:|---:|
| 3D.drfx | PASS | 23 | 23 | 1,463 | 6 |
| Airwolf.drfx | PASS | 1 | 1 | 1,474 | not individually validated |
| Animated%20Backgrounds.drfx | PASS | 4 | 4 | 170 | not individually validated |
| Background%20Sets.drfx | PASS | 175 | 176 | 11,680 | not individually validated |
| Gravity.drfx | PASS | 201 | 201 | 16,715 | not individually validated |
| LazyBackgrounds.drfx | PASS | 48 | 48 | 1,296 | not individually validated |
| LazyCollage.drfx | PASS | 64 | 64 | 8,498 | not individually validated |
| Multiscreen.drfx | PASS | 62 | 62 | 4,648 | not individually validated |
| ResolveAssets.drfx | PASS | 49 | 71 | 2,118 | not individually validated |
| SwiftTransitions.drfx | PASS | 71 | 0 | 1,309 | not individually validated |
| Thu4der_WhipRush_1.0.drfx | PASS | 1 | 0 | 4 | not individually validated |
| VBF-%20Whip%20LITE%20V1.drfx | PASS | 1 | 0 | 4 | not individually validated |
| YT.drfx | PASS | 57 | 0 | 2,987 | not individually validated |

Note: the per-package control counts are regex-based estimates and are not functional tests. Some values in this table are archive-level totals for declarations, not a count of independently testable controls.

## Findings and limits

- The batch includes 3D titles, generators/backgrounds, collage layouts, multi-screen effects, transitions, YouTube titles/overlays, and WhipRush macros.
- ZIP CRC validation checks archive integrity only. It does not validate Fusion graph semantics, plugin availability, fonts, Resolve compatibility, or actual renders.
- Control and expression counts are text-pattern estimates, not proof that every control works.
- The full test bundle includes extracted source paths, per-setting SHA-256 hashes, per-package inventories, and a runtime checklist.
- Several input filenames use URL encoding (%20 for spaces). This is a filename convention; it does not mean the file contents are encoded.
- Existing creator/license text was not intentionally removed during this audit.

## Definition of finished

Static deliverables are ready when every archive is extracted, inventoried, hashed, and paired with a test checklist. Full functional completion requires importing and rendering every item in the target DaVinci Resolve environment. That runtime phase has **not** been completed here.
