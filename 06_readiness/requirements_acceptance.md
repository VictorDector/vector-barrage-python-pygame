# Requirements Acceptance

Project: **Vector Barrage**  
Release target: `v1.1.0`  
Publication profile: **Source-First Portfolio Repository**  
Status: **SOURCE REQUIREMENTS + DOCUMENTATION + EVIDENCE ACCEPTED / PUBLIC REPOSITORY PUBLISHED / CLEAN-CHECKOUT QA PENDING**

## Purpose

Determine whether the implemented Vector Barrage candidate satisfies the requirement and CTQ baseline defined in `01_context/requirement_ctq_map.md`, while keeping source acceptance, internal packaging evidence and final public-release authorization as separate decisions.

This document answers:

> Did the implemented product satisfy each requirement it was expected to satisfy, with evidence matching the claimed acceptance scope?

## 1. Acceptance Scope

Acceptance is evaluated against:

- Functional requirements: `FR-01` through `FR-11`.
- Non-functional requirements: `NFR-01` through `NFR-16`.
- Current source/configuration regression baseline: `125 PASS`.
- Accepted source GUI/audio, integration and persistence/relaunch evidence.
- Accepted internal Windows packaging evidence where explicitly mapped to `NFR-11` and `NFR-12`.
- Accepted documentation integration state.
- Four canonical screenshot files admitted by release-owner decision; direct independent visual QA was explicitly waived and is not claimed as PASS.

Requirements define what must be true. Evidence proves a matching scope. This file records the acceptance result. Final publication authorization remains owned by `release_readiness.md`.

## 2. Functional Requirements Acceptance

| ID | Requirement | Acceptance Criterion | Evidence / Implementation Surface | Result |
|---|---|---|---|---|
| `FR-01` | Complete application shell/navigation | Main Menu exposes Game, Scores, About and Exit; secondary states return without recursive application construction. | `app.py`, `screens/menu.py`, secondary screens; navigation/integration tests; accepted source runtime | PASS |
| `FR-02` | Player movement/firing | Horizontal movement remains bounded and firing creates controlled projectile behavior. | `gameplay/model.py`, `rules.py`, `session.py`; gameplay tests; source runtime | PASS |
| `FR-03` | Enemy/wave gameplay | Enemy formation exists, moves deterministically and progresses coherently after wave completion. | gameplay model/rules/session; automated regression; source gameplay runtime | PASS |
| `FR-04` | Collision, damage and scoring | One valid collision consumes intended entities, increments score once and emits one destruction event; loss reaches Game Over correctly. | `rules.py`, `session.py`; collision/scoring tests; integrated runtime | PASS |
| `FR-05` | Live HUD | Lives, level and score visibly reflect authoritative runtime state. | `gameplay/renderer.py`; GUI/runtime validation; canonical `EVD-VB-002` file accepted by release-owner decision | PASS |
| `FR-06` | High-score presentation | Valid records parse safely, sort descending and Top 5 display; malformed records do not terminate the application. | `storage.py`, `screens/scores.py`; storage tests; source Scores runtime | PASS |
| `FR-07` | Strict new-record handling | Only `final_score > prior_max`; valid name required; exactly one accepted append. | `rules.py`, `app.py`, `screens/name_entry.py`, `storage.py`; targeted source record-flow validation | PASS |
| `FR-08` | Local score persistence/compatibility | Canonical `scores.txt` is authoritative; controlled legacy migration/fallback works; persisted score survives process relaunch. | `storage.py`, `app.py`; automated storage coverage; `EVD-VB-006` source persistence/relaunch validation | PASS |
| `FR-09` | Semantic audio | Menu/gameplay loops and destruction/new-record cues transition with state; audio failure is fail-soft. | `audio.py`, `app.py`, `session.py`; service tests; accepted GUI/audio runtime | PASS |
| `FR-10` | Generated visual presentation | Required UI/game surfaces render without external game-art files or copied project font assets. | renderer/screens, `ui_fonts.py`; generated-media tests; source GUI validation | PASS |
| `FR-11` | About/product identity | Product, author, technology and approved repository link are shown; return navigation works. | `screens/about.py`, `links.py`, `config.py`; screen/service tests; source runtime | PASS |

Functional result:

```text
FUNCTIONAL_REQUIREMENTS = 11 / 11 PASS
FUNCTIONAL_ACCEPTANCE   = PASS
```

## 3. Non-Functional Requirements Acceptance

| ID | Requirement | CTQ / Acceptance Criterion | Evidence / Measurement | Result |
|---|---|---|---|---|
| `NFR-01` | Reproducible source runtime | Metadata constrains supported Python/Pygame and project installs through the documented source workflow. | `pyproject.toml`; Python `>=3.13,<3.14`; `pygame==2.6.1`; execution runbook | PASS |
| `NFR-02` | Deterministic/testable rules | Core game rules can be validated without a visible GUI where practical. | pytest coverage across gameplay/rules/storage boundaries | PASS |
| `NFR-03` | Explicit event ownership | One active screen/session owns Pygame event retrieval at a time. | architecture contracts + navigation/session tests + runtime behavior | PASS |
| `NFR-04` | Score-data integrity | Malformed input tolerated; canonical precedence preserved; writes isolated; seed protected. | storage tests, isolated E2E, public seed checks | PASS |
| `NFR-05` | Public data hygiene | Default repository data is synthetic and non-personal. | `scores.txt`; seed integrity tests; five `PLAYER_XX` records | PASS |
| `NFR-06` | Public media independence | No copied gameplay art/audio is required; visuals/audio are generated from source. | renderer/audio implementation, media strategy, source runtime | PASS |
| `NFR-07` | Resource/persistence separation | Read-only resources are separate from writable score ownership. | `resources.py`, `app.py`, `storage.py`, source/frozen tests | PASS |
| `NFR-08` | Naming consistency | Public technical naming follows Python conventions; Spanish remains UI/legacy compatibility only. | package structure, identifier registry, source review | PASS |
| `NFR-09` | Automated regression | Current full suite completes with zero failures/errors. | `125 PASS` current accepted baseline | PASS |
| `NFR-10` | Source GUI operability | Integrated application renders/responds in a documented graphical source profile. | accepted source runtime validation; documented standard + validated WSL2/X11 path | PASS |
| `NFR-11` | Optional Windows packaging capability | Hardened package builds and preserves accepted behavior. | controlled spec/hook + internal native build/runtime evidence | PASS / INTERNAL EVIDENCE |
| `NFR-12` | Optional packaged persistence | First-run initialization and complete-relaunch score persistence work. | isolated packaged first-run/relaunch QA | PASS / INTERNAL EVIDENCE |
| `NFR-13` | Documentation integrity | Public dossier matches current architecture, states, commands and source-first publication boundary with quality parity at least equal to the accepted baseline. | cross-version quality audit + parity remediation + cross-document integration correction + final re-verification | PASS / ACCEPTED |
| `NFR-14` | Licensing clarity | MIT covers owned material; NOTICE separates Python/Pygame/tooling; no public binary is implied. | `LICENSE`, `NOTICE.md`, `pyproject.toml` | PASS / ACCEPTED |
| `NFR-15` | Fresh evidence integrity | Public screenshots/validation records match the exact Vector Barrage candidate. | `EVD-VB-005/006` accepted; four canonical screenshot files present and admitted by release-owner decision; direct visual QA waived | PASS / ACCEPTED BY OWNER DECISION |
| `NFR-16` | Clean public-tree integrity | Public repository contains only allowed source/evidence and passes clean-checkout install/tests/smoke QA. | clean root publication + final public-tree QA | PARTIAL / STATIC REMOTE QA PASS / CLEAN-CHECKOUT PENDING |

Non-functional result:

```text
CORE_SOURCE_NFR             = PASS
NFR-11_PACKAGING            = PASS / INTERNAL EVIDENCE
NFR-12_PACKAGED_PERSISTENCE = PASS / INTERNAL EVIDENCE
NFR-13_DOCUMENTATION        = PASS / ACCEPTED
NFR-14_LICENSING            = PASS / ACCEPTED
NFR-15_EVIDENCE             = PASS / ACCEPTED BY OWNER DECISION
NFR-16_PUBLIC_TREE          = PARTIAL / STATIC REMOTE QA PASS / CLEAN-CHECKOUT PENDING
```

## 4. Validation-Level Coverage

| Validation Level | Current Scope | Result |
|---|---|---|
| `V1` COMPILE | production/package source within accepted regression baseline | PASS |
| `V2` IMPORT / INSTALL | supported Python/Pygame source environment | PASS |
| `V3` BEHAVIOR | gameplay, storage, navigation, services, fonts, packaging contracts | PASS / 125 automated tests |
| `V4` GUI_AUDIO | integrated source application and procedural media | PASS |
| `V5` INTEGRATION | navigation, game result, record flow and persistence orchestration | PASS |
| `V6` PACKAGED_RUNTIME | hardened Windows package | PASS / INTERNAL EVIDENCE |
| `V7` PUBLICATION | exact public repository + admitted evidence + clean-checkout QA | PARTIAL / STATIC REMOTE QA PASS / CLEAN-CHECKOUT PENDING |

Automated success does not replace GUI/audio observation. Source runtime success does not establish packaged-runtime success. Packaged-runtime success does not authorize public binary distribution. Screenshot admission by owner decision does not imply that independent direct visual QA was performed.

## 5. Evidence Mapping

```text
FR-01..FR-11
-> current automated suite
-> accepted source runtime/integration
-> source evidence EVD-VB-005 / EVD-VB-006 where applicable
-> admitted canonical screenshots where applicable

NFR-01..NFR-10
-> pyproject/source tree
-> 125 PASS
-> source runtime / persistence evidence

NFR-11..NFR-12
-> hardened Windows build/runtime evidence
-> INTERNAL EVIDENCE only

NFR-13
-> cross-version documentation quality audit
-> six-document quality-parity remediation
-> cross-document integration correction across state/CTQ/solution/publication/evidence surfaces
-> targeted re-verification PASS
-> documentation gate CLOSED / ACCEPTED

NFR-14
-> LICENSE + NOTICE + dependency metadata

NFR-15
-> source evidence accepted
-> four canonical PNG files physically present
-> screenshot admission ACCEPTED BY RELEASE OWNER
-> direct visual QA WAIVED, not represented as PASS

NFR-16
-> clean public repository published with independent root history
-> static remote-tree verification PASS
-> exact clean-checkout/source QA NEXT
```

## 6. Packaging Engineering Evidence

Packaging is not a public-distribution requirement under the source-first profile, but completed work is preserved:

```text
SOURCE_SNAPSHOT = 0e1951c67f19b9eff24937ff1e1d228bfd72ff8b
EXE_NAME        = VectorBarrage.exe
EXE_SIZE_BYTES  = 11230689
EXE_SHA256      = 170ED5502A1D2D955EFA3CB52D13B880830657FF456166E6610DD30AB7E430A6
ARCHIVE_QA      = PASS
RUNTIME_QA      = PASS
FIRST_RUN_QA    = PASS
PERSISTENCE_QA  = PASS
PUBLIC_DOWNLOAD = NO
```

This evidence supports `NFR-11`/`NFR-12`; it does not create a public executable release surface.

## 7. Public Repository Acceptance Controls

| Control | Status | Note |
|---|---|---|
| MIT `LICENSE` | PASS / ACCEPTED | Applies to Vector Barrage-owned material. |
| Concise `NOTICE.md` | PASS / ACCEPTED | Separates Python/Pygame/tooling licensing and states no public executable. |
| Dependency metadata | PASS | Python/Pygame boundary declared canonically in `pyproject.toml`. |
| Documentation quality parity | PASS / ACCEPTED | Six targeted documents were strengthened against the accepted first-version quality baseline. |
| Documentation integration | PASS / ACCEPTED | Corrected integration state passed targeted re-verification and the documentation gate is closed. |
| Screenshot evidence | PRESENT / ACCEPTED BY RELEASE OWNER | Four canonical PNG files are admitted; direct independent visual QA was waived. |
| Screenshot ID/filename normalization | PASS | `EVD-VB-001` through `EVD-VB-004` canonical filenames are present. |
| Clean public repository | PUBLISHED / STATIC REMOTE QA PASS | Target `VictorDector/vector-barrage-python-pygame`; root commit has zero parents. |
| Clean-checkout install/tests/smoke | PENDING / NEXT | Run against the exact published public repository state after documentation-state synchronization. |

## 8. Publication Profile Decision

```text
PUBLIC_SOURCE_REPOSITORY       = YES
PUBLIC_EXECUTABLE_DOWNLOAD     = NO
GITHUB_RELEASE_BINARY          = NO
FULL_BINARY_COMPLIANCE_BUNDLE  = OPTIONAL FUTURE
```

If executable distribution is later activated, the preserved hardened component/license analysis must be reopened and completed for that distribution scenario.

## 9. Current Acceptance Decision

```text
FUNCTIONAL_REQUIREMENTS             = PASS / 11 OF 11
CORE_SOURCE_NFR                     = PASS
AUTOMATED_REGRESSION                = PASS / 125
SOURCE_RUNTIME                      = PASS
SOURCE_RELAUNCH_PERSISTENCE         = PASS
PACKAGING_CAPABILITY                = PASS / INTERNAL EVIDENCE
MINIMAL_SOURCE_REPOSITORY_LICENSING = PASS / ACCEPTED
DOCUMENTATION_QUALITY_PARITY        = PASS / ACCEPTED
DOCUMENTATION_INTEGRATION           = PASS / ACCEPTED
SCREENSHOT_ADMISSION                = ACCEPTED / OWNER DECISION
SCREENSHOT_VISUAL_QA                = WAIVED
PUBLIC_TREE_QA                      = PARTIAL / STATIC REMOTE QA PASS / CLEAN-CHECKOUT PENDING
PUBLIC_REPOSITORY                   = PUBLISHED / CLEAN ROOT HISTORY
PUBLIC_BINARY_DISTRIBUTION          = N/A
PUBLIC_RELEASE_READY                = NO
```

The implemented product, documentation and admitted evidence are accepted within the current source-first scope. The clean public repository is published with independent root history and has passed static remote-tree verification. Final public release acceptance remains intentionally open until exact clean-checkout install/tests/source-smoke QA passes.
