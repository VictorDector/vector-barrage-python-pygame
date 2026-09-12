# Vector Barrage Evidence Index

Project: **Vector Barrage**  
Release target: `v1.1.0`  
Publication profile: **Source-First Portfolio Repository**

## Purpose

Define which validation records support public portfolio claims and which completed package-validation records remain internal engineering evidence under the current source-first publication profile.

## Current Validation Baseline

```text
AUTOMATED_REGRESSION          = 125 PASS
SOURCE_RUNTIME                = PASS / ACCEPTED
SOURCE_PERSISTENCE            = PASS / ACCEPTED
WINDOWS_SOURCE_RUNTIME        = PASS / RECONFIRMED
WINDOWS_HARDENED_BUILD        = PASS / INTERNAL EVIDENCE
PACKAGED_RUNTIME              = PASS / INTERNAL EVIDENCE
PACKAGED_FIRST_RUN            = PASS / INTERNAL EVIDENCE
PACKAGED_PERSISTENCE_RELAUNCH = PASS / INTERNAL EVIDENCE
PUBLIC_EXECUTABLE_DOWNLOAD    = NO
DOCUMENTATION_INTEGRATION     = PASS / ACCEPTED
DOCUMENTATION_GATE            = CLOSED / ACCEPTED
SCREENSHOT_FILES              = PRESENT / 4 OF 4
SCREENSHOT_VISUAL_QA          = WAIVED BY RELEASE OWNER
SCREENSHOT_ADMISSION          = ACCEPTED / OWNER DECISION
EVD-VB-004                    = PRE-FIX REFERENCE / REPLACEMENT WAIVED
ABOUT_LAYOUT_FINAL            = PASS / OWNER VERIFIED
FINAL_PUBLIC_TREE_QA          = PASS / ACCEPTED
```

The current automated baseline supersedes earlier 108/109-test documentation-stage snapshots. Those historical results remain valid for their original checkpoints but do not define the final source release.

## Public Evidence Set

| Evidence ID | Evidence | Status | Public disposition |
|---|---|---|---|
| `EVD-VB-001` | Main Menu screenshot | PRESENT / ACCEPTED | Current visual reference; independent direct visual QA not claimed |
| `EVD-VB-002` | Gameplay/HUD screenshot | PRESENT / ACCEPTED | Current visual reference; independent direct visual QA not claimed |
| `EVD-VB-003` | Scores screenshot | PRESENT / ACCEPTED | Current visual reference; independent direct visual QA not claimed |
| `EVD-VB-004` | About screenshot | PRESENT / ACCEPTED / PRE-FIX REFERENCE | Captured before the final responsive About-layout correction; replacement explicitly waived by release owner; not exact final-layout evidence |
| `EVD-VB-005` | Source runtime validation | PASS / FORMALIZED | Public engineering evidence |
| `EVD-VB-006` | Source persistence/relaunch validation | PASS / FORMALIZED | Public engineering evidence |

## Internal Packaging Evidence

Package-validation work is preserved because it demonstrates that the application can be hardened, built and exercised as a native Windows package. It does **not** make the executable a public release asset.

Current hardened artifact identity:

```text
SOURCE_SNAPSHOT = 0e1951c67f19b9eff24937ff1e1d228bfd72ff8b
EXE_NAME        = VectorBarrage.exe
EXE_SIZE_BYTES  = 11230689
EXE_SHA256      = 170ED5502A1D2D955EFA3CB52D13B880830657FF456166E6610DD30AB7E430A6
TECHNICAL_QA    = PASS / COMPLETE
PUBLIC_USE      = INTERNAL ENGINEERING EVIDENCE ONLY
```

Staging records `EVD-VB-007` and `EVD-VB-008`, where present, are classified as **INTERNAL_EVIDENCE / EXCLUDE_FROM_FINAL_PUBLIC_COPY** under the current source-first profile. They must not be used to imply that a Windows executable is available for download.

## Screenshot Evidence Boundary

The public repository contains the four canonical files:

```text
evidence/screenshots/EVD-VB-001_main_menu.png
evidence/screenshots/EVD-VB-002_gameplay_hud.png
evidence/screenshots/EVD-VB-003_scores.png
evidence/screenshots/EVD-VB-004_about.png
```

Verified admission inputs:

```text
PHYSICAL_FILE_PRESENCE = PASS / 4 OF 4
CANONICAL_FILENAMES    = PASS
PNG_STRUCTURE          = PASS
RESOLUTION_CONSISTENCY = PASS
DIRECT_VISUAL_QA       = WAIVED BY RELEASE OWNER
SCREENSHOT_ADMISSION   = ACCEPTED / OWNER DECISION
```

The final About layout was subsequently corrected and verified by the release owner. `EVD-VB-004` was intentionally retained rather than refreshed. Its accepted claim boundary is therefore historical/pre-fix visual reference only.

The four screenshots are admitted for the public source-first evidence set by release-owner decision. This must not be represented as an independent direct visual-QA PASS.

## Claim Rules

- Screenshot evidence may be presented as accepted public evidence within its declared claim boundary.
- Do not claim that independent direct visual QA was performed; that check was waived by the release owner.
- `EVD-VB-004` must not be represented as exact final-layout evidence.
- Do not publish historical/private screenshots as current Vector Barrage evidence unless explicitly dispositioned.
- Do not present the internally validated Windows executable as a downloadable public artifact.
- Source claims must match the public source snapshot and current automated baseline.
- Earlier package hashes and superseded package experiments remain historical/internal and must not be presented as the current public artifact.
- If executable distribution is activated later, binary-specific compliance and release evidence must be reopened.

## Current Decision

```text
SOURCE_EVIDENCE_READY          = YES
AUTOMATED_BASELINE             = 125 PASS
DOCUMENTATION_INTEGRATION      = PASS / ACCEPTED
DOCUMENTATION_GATE             = CLOSED / ACCEPTED
SCREENSHOT_FILES               = PRESENT / 4 OF 4
SCREENSHOT_VISUAL_QA           = WAIVED BY RELEASE OWNER
SCREENSHOT_ADMISSION           = ACCEPTED / OWNER DECISION
EVD-VB-004                     = PRE-FIX REFERENCE / REPLACEMENT WAIVED
ABOUT_LAYOUT_FINAL             = PASS / OWNER VERIFIED
PACKAGED_EVIDENCE              = INTERNAL ONLY
PUBLIC_BINARY_EVIDENCE_CLAIM   = NO DISTRIBUTED BINARY
PUBLIC_EVIDENCE_SET_COMPLETE   = YES
PUBLIC_REPOSITORY              = PUBLISHED / CLEAN ROOT HISTORY
FINAL_PUBLIC_TREE_QA           = PASS / ACCEPTED
DOCUMENTATION_RECONCILIATION   = PASS / ACCEPTED
PUBLIC_RELEASE_READY           = YES
TAG_v1.1.0                     = PENDING
```

## Next Evidence Gate

No evidence gate remains open for the current source-first release profile. The next release action is creation and verification of the `v1.1.0` tag after the documentation reconciliation commit is remotely verified.
