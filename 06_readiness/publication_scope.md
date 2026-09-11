# Publication Scope

Project: **Vector Barrage**  
Release target: `v1.1.0`  
Status: **SOURCE-FIRST PORTFOLIO MASK / LICENSING + DOCUMENTATION + SCREENSHOT EVIDENCE ACCEPTED / PUBLIC REPOSITORY ASSEMBLY READY**

## Purpose

Define the exact publication boundary for the Vector Barrage portfolio repository: what will be public, what remains internal engineering evidence, what is optional future work, and what is excluded.

The approved target is a **public source repository with instructions to install Python/Pygame and run the application from source**. The current profile does not distribute a compiled Windows executable.

## Classification Model

| Classification | Meaning |
|---|---|
| `PUBLIC_SOURCE` | Intended to live in the public Git repository. |
| `PUBLIC_EVIDENCE` | Accepted evidence eligible for public use. |
| `INTERNAL_EVIDENCE` | Preserved engineering/QA evidence not required in the public repository. |
| `OPTIONAL_FUTURE` | Not required now; becomes active only if scope changes. |
| `PENDING_GATE` | Intended public material awaiting a stated prerequisite. |
| `EXCLUDE` | Generated, historical, private or unrelated material excluded from publication. |
| `N/A` | Not required by the current publication profile. |

## Public Repository Mask

| Artifact / Scope | Classification | Current disposition |
|---|---|---|
| `README.md` | PUBLIC_SOURCE | Reconciled to source-first portfolio profile. |
| `LICENSE` | PUBLIC_SOURCE | MIT / CREATED / ACCEPTED. |
| `NOTICE.md` | PUBLIC_SOURCE | Concise Python/Pygame third-party boundary / ACCEPTED. |
| `.gitignore` | PUBLIC_SOURCE | Repository hygiene. |
| `pyproject.toml` | PUBLIC_SOURCE | Canonical metadata; Python `>=3.13,<3.14`; `pygame==2.6.1`. |
| `scores.txt` | PUBLIC_SOURCE | Approved five-record synthetic seed. |
| `00_control/` | PUBLIC_SOURCE | Product-facing state, identifiers and material product changes only; private workflow/gate mechanics are excluded. |
| `01_context/` | PUBLIC_SOURCE | Product context, behavior, requirements/CTQs and references. |
| `02_architecture/` | PUBLIC_SOURCE | As-built architecture and material design decisions. |
| `03_governance/` | PUBLIC_SOURCE | Product policies, media strategy and validation policy. |
| `04_solution/` | PUBLIC_SOURCE | Capability/dependency/integration map. |
| `05_implementation/` | PUBLIC_SOURCE | Source execution and optional packaging engineering runbooks. |
| `06_readiness/` | PUBLIC_SOURCE | Acceptance, readiness and publication scope. |
| `src/vector_barrage/` | PUBLIC_SOURCE | Independently implemented application source. |
| `tests/` | PUBLIC_SOURCE | Current automated regression suite; accepted baseline `125 PASS`. |
| `packaging/` | PUBLIC_SOURCE | Controlled PyInstaller configuration retained as reproducible engineering evidence. |
| `evidence/README.md` | PUBLIC_SOURCE | Source-first evidence index. |
| `evidence/screenshots/` | PUBLIC_EVIDENCE | Four canonical PNG files present and accepted by release-owner decision; direct visual QA was explicitly waived. |
| source validation records `EVD-VB-005/006` | PUBLIC_EVIDENCE | Accepted and aligned to the public source claim boundary. |
| packaged build/runtime records `EVD-VB-007/008` | INTERNAL_EVIDENCE | Preserve internally; exclude from final public copy unless deliberately reclassified. |
| `dist/VectorBarrage.exe` | N/A | Do not publish or attach under current profile. |
| GitHub Release binary asset | N/A | No public executable distribution. |
| full binary third-party license/source bundle | OPTIONAL_FUTURE | Reactivate only if executable distribution is proposed. |
| `build/` | EXCLUDE | Generated build state. |
| virtual environments | EXCLUDE | Host-local state. |
| test/cache/IDE files | EXCLUDE | Generated/local state. |
| temporary QA score directories | EXCLUDE | Disposable validation state. |
| historical screenshots/executables | EXCLUDE | Not Vector Barrage public evidence. |
| unrelated/private Git history | EXCLUDE | Public repository starts with clean product history. |
| private workflow/gate records | EXCLUDE | Internal execution mechanics are not part of the public product dossier. |
| external gameplay image/audio directories | N/A | Current visuals/audio are generated from source. |

## Source Publication Boundary

```text
public portfolio repository
├── Python source
├── pinned Pygame dependency declaration
├── automated tests
├── engineering documentation
├── controlled build configuration
├── synthetic score seed
├── MIT license + concise third-party notice
├── admitted screenshots
└── no distributed executable
```

A reviewer can install dependencies through the normal Python package workflow and run Vector Barrage from source. Pygame runtime binaries are obtained by the user through package installation rather than redistributed by this repository as a bundled executable.

## Data Boundary

The repository default `scores.txt` is synthetic:

```text
PLAYER_01,500
PLAYER_02,350
PLAYER_03,250
PLAYER_04,150
PLAYER_05,100
```

Before public copy, verify that no QA/manual score has replaced or modified this seed.

## Evidence Boundary

Fresh Vector Barrage source evidence may be public when it matches the final source snapshot. Hardened Windows build/runtime evidence remains valid but is classified as internal engineering evidence because the executable is not distributed.

The four canonical screenshot files are physically present under `evidence/screenshots/` and are accepted for publication by release-owner decision. Direct independent visual QA was waived and must not be represented as a visual-QA PASS.

Current evidence state:

```text
DOCUMENTATION INTEGRATION QA = PASS
DOCUMENTATION GATE           = CLOSED / ACCEPTED
SCREENSHOT FILES             = PRESENT / 4 OF 4
SCREENSHOT FILENAMES         = CANONICAL / PASS
SCREENSHOT VISUAL QA         = WAIVED BY RELEASE OWNER
SCREENSHOT ADMISSION         = ACCEPTED / OWNER DECISION
```

## Executable Boundary

A hardened Windows executable was built and validated internally, including archive hardening, runtime, first-run score initialization and persistence/relaunch QA. The work is preserved, but current publication policy is:

```text
PUBLIC_EXE_DOWNLOAD       = NO
GITHUB_RELEASE_BINARY     = NO
BINARY_DISTRIBUTION_GATE  = N/A FOR CURRENT PROFILE
```

If public executable distribution is proposed later, binary-specific licensing/compliance becomes active again before distribution.

## Licensing Boundary

```text
LICENSE                       = MIT / ACCEPTED
NOTICE.md                     = ACCEPTED
VECTOR BARRAGE-OWNED MATERIAL = MIT
PYTHON/PYGAME                 = THIRD-PARTY / OWN LICENSES
PUBLIC BUNDLED BINARIES       = NONE
FULL BINARY COMPLIANCE        = OPTIONAL FUTURE
```

## Publication Sequence

```text
source + engineering documentation accepted                  = COMPLETE
-> source-first portfolio profile approved                   = COMPLETE
-> minimal repository licensing accepted                     = COMPLETE
-> documentation quality-parity review/remediation           = COMPLETE
-> cross-document integration correction                     = COMPLETE
-> documentation integration QA / final acceptance           = COMPLETE
-> screenshot admission                                      = COMPLETE / OWNER DECISION
-> clean public repository creation                          = NEXT
-> exact public-tree/source execution QA                     = LOCKED UNTIL ASSEMBLED
-> public portfolio release decision                         = LOCKED
```

## Current Decision

```text
PUBLICATION_PROFILE            = SOURCE-FIRST PORTFOLIO / APPROVED
MIT_LICENSE                    = PASS / ACCEPTED
CONCISE_THIRD_PARTY_NOTICE     = PASS / ACCEPTED
AUTOMATED_BASELINE             = 125 PASS
PUBLIC_WINDOWS_EXECUTABLE      = N/A / NOT DISTRIBUTED
FULL_BINARY_COMPLIANCE_BUNDLE  = OPTIONAL FUTURE
DOCUMENTATION_QUALITY_PARITY   = PASS / ACCEPTED
DOCUMENTATION_INTEGRATION      = PASS / ACCEPTED
SCREENSHOT_ADMISSION           = ACCEPTED / OWNER DECISION
PUBLIC_REPOSITORY_CREATED      = NO / ASSEMBLY READY
FINAL_PUBLIC_TREE_QA           = UNLOCKED AFTER ASSEMBLY
PUBLIC_RELEASE_READY           = NO
```
