# Change Log

Project: **Vector Barrage**  
Release target: `v1.1.0`  
Status: ACTIVE

## Purpose

Record material changes to the public Vector Barrage product and its release artifacts. This log intentionally excludes private development-process mechanics, transient tooling attempts and historical source-expression details that are not part of the public product.

## Material Product Changes

| Change ID | Version | Change | Reason | State |
|---|---|---|---|---|
| `VB-CHG-001` | `v1.1.0a0` | Public identity established as **Vector Barrage** with repository target `VictorDector/vector-barrage-python-pygame`. | Establish an independent public product identity and publication destination. | CLOSED |
| `VB-CHG-002` | `v1.1.0a0` | Behavioral specification defined for menu, gameplay, scores, persistence, navigation, audio, data and release constraints. | Separate required behavior from any historical implementation expression. | CLOSED |
| `VB-CHG-003` | `v1.1.0a0` | Package architecture defined under `src/vector_barrage/`. | Provide explicit application, gameplay, UI and infrastructure boundaries. | CLOSED |
| `VB-CHG-004` | `v1.1.0a0` | Iterative application coordinator implemented. | Prevent recursive screen construction and centralize application-state transitions. | CLOSED |
| `VB-CHG-005` | `v1.1.0a0` | Canonical score storage implemented in `storage.py`. | Centralize parsing, Top-5 ordering, max score, append safety, legacy compatibility and source/frozen path behavior. | CLOSED |
| `VB-CHG-006` | `v1.1.0a0` | Deterministic gameplay model and rule layer implemented. | Make movement, collisions, scoring, lives, wave progression and new-record comparison independently testable. | CLOSED |
| `VB-CHG-007` | `v1.1.0a0` | Pygame gameplay session and renderer implemented. | Separate active event-loop/runtime orchestration from deterministic rules and visual presentation. | CLOSED |
| `VB-CHG-008` | `v1.1.0a0` | Main Menu, Scores, About and Name Entry screens implemented. | Complete the public UI surfaces while preserving coordinator-owned navigation. | CLOSED |
| `VB-CHG-009` | `v1.1.0a0` | External-link handling isolated in `links.py`. | Keep platform-specific browser launching outside presentation logic. | CLOSED |
| `VB-CHG-010` | `v1.1.0a0` | Programmatic visual presentation adopted. | Remove dependency on external/copy-based gameplay artwork and keep release media self-contained in source. | CLOSED |
| `VB-CHG-011` | `v1.1.0a0` | Procedural PCM audio service implemented for menu, gameplay, enemy-destruction and new-record cues. | Eliminate external game-audio files while preserving semantic audio behavior. | CLOSED |
| `VB-CHG-012` | `v1.1.0a0` | Synthetic public score seed created. | Ensure default public data contains no private or historical player names. | CLOSED |
| `VB-CHG-013` | `v1.1.0a0` | Full automated source suite completed with `108 passed in 0.25s`. | Establish the pre-documentation-correction source regression baseline under Python 3.13.15 / Pygame 2.6.1. | CLOSED — HISTORICAL BASELINE |
| `VB-CHG-014` | `v1.1.0a0` | Source GUI/runtime validation completed through WSL2/X11. | Validate the real integrated menu, gameplay, HUD, screens, navigation and procedural media. | CLOSED |
| `VB-CHG-015` | `v1.1.0a0` | Isolated new-record and score-persistence flow validated. | Verify Game Over → strict record decision → Name Entry → exactly-one append without mutating the repository seed. | CLOSED |
| `VB-CHG-016` | `v1.1.0a0` | Complete-process source relaunch persistence confirmed. | Prove persisted score data remains readable after full application restart. | CLOSED |
| `VB-CHG-017` | `v1.1.0a0` | Full public engineering-documentation dossier reconstructed. | Preserve or improve context, architecture, governance, solution, runbook, acceptance and release documentation quality. | CLOSED — BASELINE FOR QA |
| `VB-CHG-018` | `v1.1.0a0` | Documentation-QA correction bundle applied to public About wording, About contract test, README/runtime documentation, state vocabulary, audio semantics and packaging guidance. | Remove unsupported redistribution wording, remove internal release-step identifiers, align documentation to actual audio behavior, document exact controls and prevent an unvalidated PyInstaller entry path from being presented as preferred. | CLOSED |
| `VB-CHG-019` | `v1.1.0a0` | Corrected candidate completed targeted and full regression: `20 passed in 0.08s` and `109 passed in 0.27s`. Documentation integrity was accepted after the correction cross-check. | Establish the automated baseline for the corrected source/documentation candidate and close the documentation rework condition. | CLOSED — SUPERSEDED TEST BASELINE |
| `VB-CHG-020` | `v1.1.0a0` | UI rendering migrated to explicit approved host-system font resolution and dedicated font contracts were added. | Remove reliance on bundled default-font assets while preserving Spanish UI rendering. | CLOSED |
| `VB-CHG-021` | `v1.1.0a0` | Controlled PyInstaller spec and Pygame hook added; packaging-hardening contracts integrated. Full regression advanced to `125 PASS`. | Make the packaging configuration reproducible and enforce binary-hardening constraints in source-level QA. | CLOSED |
| `VB-CHG-022` | `v1.1.0a0` | Hardened Windows package built from pinned source/config snapshot and validated through archive, runtime, first-run initialization and persistence/relaunch QA. | Demonstrate a complete native packaging path and remove previously identified bundled-font/icon/VC-runtime blockers. | CLOSED — INTERNAL ENGINEERING EVIDENCE |
| `VB-CHG-023` | `v1.1.0a0` | Publication scope changed to **Source-First Portfolio Repository**; public executable download and GitHub binary release removed from current scope. | Match publication effort to portfolio evidence needs while preserving completed packaging work as internal evidence. | CLOSED |
| `VB-CHG-024` | `v1.1.0a0` | MIT `LICENSE` created for Vector Barrage-owned material and concise Python/Pygame third-party `NOTICE.md` implemented. | Close the licensing boundary required for a source-first public repository without activating full binary redistribution compliance. | CLOSED |
| `VB-CHG-025` | `v1.1.0a0` | Publication-facing documentation and repository mask reconciled to the source-first profile and current `125 PASS` baseline. | Remove stale binary-release requirements, obsolete 109-test claims and outdated licensing HOLD language before public-tree assembly. | CLOSED / ACCEPTED |
| `VB-CHG-026` | `v1.1.0a0` | Cross-version documentation quality audit used the accepted first-version dossier as a quality benchmark and applied targeted parity remediation to six Vector Barrage documents. | Preserve or improve documentation quality without copying obsolete private/binary-release content or inflating the public dossier. Restored project-context depth, behavioral contract granularity, explicit test/independence architecture, validated WSL2/X11 runbook detail, requirement-level acceptance traceability and the final public-tree acceptance gate. | CLOSED / ACCEPTED |
| `VB-CHG-027` | `v1.1.0` | Clean public repository materialized as an independent root history and statically verified against the approved public tree. | Establish the autonomous public portfolio repository without private Git ancestry while preserving exact approved content. | CLOSED / STATIC REMOTE QA PASS |
| `VB-CHG-028` | `v1.1.0a0` | Public documentation state was reconciled after clean-repository publication, aligning the public dossier to the independently published source-first tree. | Remove stale staging/publication wording without changing runtime behavior. | CLOSED / ACCEPTED |
| `VB-CHG-029` | `v1.1.0a0` | About layout was made responsive to keep text within the viewport; the affected screen/service test was strengthened and the full regression remained `125 PASS`. The existing About screenshot was retained as a pre-fix reference after the release owner waived replacement. | Correct the observed About text-overflow defect while preserving explicit evidence history. | CLOSED / ACCEPTED |
| `VB-CHG-030` | `v1.1.0` | Package and runtime version metadata were promoted from `1.1.0a0` to `1.1.0`; candidate and public-tree regression remained `125 PASS`. | Establish the stable release version without changing product behavior. | CLOSED / ACCEPTED |
| `VB-CHG-031` | `v1.1.0` | The exact published `1.1.0` source tree completed clean-checkout installation, import, full regression, public-seed and worktree-integrity QA. | Prove reproducibility of the exact public source snapshot intended for release. | CLOSED / ACCEPTED |
| `VB-CHG-032` | `v1.1.0` | Final public documentation taxonomy and release-state projections were reconciled across README, control, context, governance, solution, implementation, readiness and evidence surfaces. | Eliminate residual cross-document drift and establish a single consistent release-ready public dossier. | CLOSED / ACCEPTED |

## Current Candidate Result

```text
PRODUCT_IDENTITY                     = PASS
SOURCE_IMPLEMENTATION                = PASS
PUBLIC_MEDIA_BOUNDARY                = PASS
PUBLIC_SYNTHETIC_DATA                = PASS
AUTOMATED_SOURCE_QA                  = 125 PASS
SOURCE_INTEGRATED_RUNTIME            = PASS
SOURCE_RELAUNCH_PERSISTENCE          = PASS
SYSTEM_FONT_HARDENING                = PASS
CONTROLLED_PACKAGING_CONFIGURATION   = PASS
HARDENED_WINDOWS_PACKAGE             = PASS / INTERNAL EVIDENCE
MIT_LICENSE                          = PASS / ACCEPTED
THIRD_PARTY_NOTICE                   = PASS / ACCEPTED
PUBLIC_BINARY_DISTRIBUTION           = N/A
DOC_QUALITY_PARITY_REMEDIATION       = PASS / ACCEPTED
SCREENSHOT_ADMISSION                 = ACCEPTED / OWNER DECISION
EVD-VB-004                           = PRE-FIX REFERENCE / REPLACEMENT WAIVED
PUBLIC_REPOSITORY                    = PUBLISHED / CLEAN ROOT HISTORY
FINAL_PUBLIC_TREE_QA                 = PASS / ACCEPTED
DOCUMENTATION_RECONCILIATION         = PASS / ACCEPTED
PUBLIC_RELEASE_READY                 = YES
TAG_v1.1.0                           = PENDING
```

## Change Record Policy

Record a change when it materially affects product behavior, architecture, public data, runtime dependencies, packaging, public documentation, validation claims or release readiness. Minor lexical edits and internal workflow operations should not inflate this product-facing log. Superseded product decisions remain traceable when they materially explain the current architecture or publication boundary.
