# Requirement–CTQ Map

Project: **Vector Barrage**  
Release target: `v1.1.0`  
Publication profile: **Source-First Portfolio Repository**  
Status: ACTIVE

## Purpose

Map product requirements to critical-to-quality (CTQ) criteria, implementation surfaces and current evidence. Packaging remains an independently validated engineering capability but is not a public binary-distribution requirement under the approved source-first profile.

## Functional Requirements

| ID | Requirement | CTQ / Acceptance Criterion | Primary Implementation | Current Result |
|---|---|---|---|---|
| `FR-01` | Complete application shell/navigation. | Main Menu exposes Game, Scores, About and Exit; secondary states return without recursive application construction. | `app.py`, `screens/menu.py`, secondary screens | PASS |
| `FR-02` | Player movement/firing. | Horizontal movement remains bounded and firing produces controlled projectile behavior. | `gameplay/model.py`, `rules.py`, `session.py` | PASS |
| `FR-03` | Enemy/wave gameplay. | Formation exists, moves deterministically and progresses coherently across wave completion. | gameplay model/rules/session | PASS |
| `FR-04` | Collision, damage and scoring. | One valid collision consumes intended entities, increments once and emits one destruction event; loss reaches Game Over appropriately. | `gameplay/rules.py`, `session.py` | PASS |
| `FR-05` | Live HUD. | Lives, level and score visibly reflect authoritative runtime state. | `gameplay/renderer.py` | PASS |
| `FR-06` | High-score presentation. | Valid records parse safely, sort descending and Top 5 display; malformed records do not terminate application. | `storage.py`, `screens/scores.py` | PASS |
| `FR-07` | Strict new-record handling. | Only `final_score > prior_max`; valid name; exactly-one accepted append. | rules/app/name-entry/storage | PASS |
| `FR-08` | Local score persistence/compatibility. | Canonical `scores.txt` authoritative; controlled legacy migration/fallback; score survives process relaunch. | `storage.py`, `app.py` | PASS |
| `FR-09` | Semantic audio. | Menu/gameplay loops and destruction/new-record cues transition with state; audio failure is fail-soft. | `audio.py`, `app.py`, `session.py` | PASS |
| `FR-10` | Generated visual presentation. | Required UI/game surfaces render without external game-art files or copied project font assets. | renderer + screens + `ui_fonts.py` | PASS |
| `FR-11` | About/product identity. | Product, author, technology and approved project link are shown; return navigation works. | About/links/config | PASS |

## Non-Functional Requirements

| ID | Requirement | CTQ / Acceptance Criterion | Evidence / Measurement | Current Result |
|---|---|---|---|---|
| `NFR-01` | Reproducible source runtime. | Metadata constrains Python/Pygame and source package installs cleanly. | `pyproject.toml`; Python 3.13.x / Pygame 2.6.1 | PASS |
| `NFR-02` | Deterministic/testable rules. | Core game rules testable without visible GUI where practical. | automated tests | PASS |
| `NFR-03` | Explicit event ownership. | One active screen/session owns event retrieval. | architecture + tests + runtime | PASS |
| `NFR-04` | Score-data integrity. | Malformed input tolerated; canonical precedence; writes isolated; seed protected. | tests + isolated E2E | PASS |
| `NFR-05` | Public data hygiene. | Default data synthetic/non-personal. | `scores.txt` + seed tests | PASS |
| `NFR-06` | Public media independence. | No copied gameplay art/audio; visuals/audio generated from source. | renderer/audio + runtime | PASS |
| `NFR-07` | Resource/persistence separation. | Read-only resources separated from writable scores. | resources/app/tests | PASS |
| `NFR-08` | Naming consistency. | Public technical naming uses Python conventions; Spanish limited to UI/legacy compatibility. | source/package structure | PASS |
| `NFR-09` | Automated regression. | Current suite completes with zero failures/errors. | `125 PASS` | PASS |
| `NFR-10` | Source GUI operability. | Integrated application renders/responds in documented graphical source profile. | source runtime validation | PASS |
| `NFR-11` | Optional Windows packaging capability. | Hardened package builds and preserves accepted behavior. | native build + packaged runtime | PASS / INTERNAL EVIDENCE |
| `NFR-12` | Optional packaged persistence. | First-run score initialization and complete relaunch persistence work. | isolated packaged QA | PASS / INTERNAL EVIDENCE |
| `NFR-13` | Documentation integrity. | Public dossier matches current architecture, status, commands and source-first publication boundary while preserving or improving the accepted documentation-quality baseline. | cross-version quality audit + targeted parity remediation + integration correction | REMEDIATION IMPLEMENTED / INTEGRATION QA REQUIRED |
| `NFR-14` | Licensing clarity. | MIT covers owned material; NOTICE separates Python/Pygame/tooling; no public binary implied. | `LICENSE`, `NOTICE.md`, `pyproject.toml` | PASS / ACCEPTED |
| `NFR-15` | Fresh evidence integrity. | Public screenshots/validation records match the exact Vector Barrage candidate. | `evidence/` | PARTIAL — SCREENSHOTS QA PENDING / BLOCKED BY DOC GATE |
| `NFR-16` | Clean public-tree integrity. | Public repository contains only allowed source/evidence and passes clean-checkout install/tests/smoke QA. | final public-tree QA | LOCKED |

## CTQ Claim Rules

- Automated tests do not replace GUI/audio observation.
- Source runtime success does not automatically prove packaged runtime.
- Packaged-runtime PASS does not imply public binary distribution.
- Historical evidence from another implementation cannot satisfy Vector Barrage evidence requirements.
- Public screenshot claims require visual admission.
- Current publication claims must match the source-first profile.
- Documentation states must remain synchronized across context, solution, readiness and evidence surfaces before screenshot admission unlocks.

## Evidence Mapping

| Requirement Group | Current Evidence |
|---|---|
| `FR-01`–`FR-11` | current automated suite + accepted integrated source execution |
| `NFR-01`–`NFR-10` | metadata, source tree, `125 PASS`, runtime and isolated source-persistence checks |
| `NFR-11`–`NFR-12` | hardened Windows package QA / INTERNAL EVIDENCE |
| `NFR-13` | documentation-quality audit complete; six-document parity remediation implemented; cross-document integration correction implemented; integration QA still required |
| `NFR-14` | MIT `LICENSE` + concise `NOTICE.md` / ACCEPTED |
| `NFR-15` | source evidence accepted; four screenshots captured but not yet admitted; evidence gate blocked until documentation gate closes |
| `NFR-16` | pending clean public-repository assembly |

## Current Acceptance Summary

```text
FUNCTIONAL_REQUIREMENTS             = PASS / 11 OF 11
CORE_SOURCE_NFR                     = PASS
AUTOMATED_REGRESSION                = 125 PASS
SOURCE_INTEGRATED_RUNTIME           = PASS
SOURCE_RELAUNCH_PERSISTENCE         = PASS
PACKAGING_CAPABILITY                = PASS / INTERNAL EVIDENCE
LICENSE_READINESS                   = PASS / SOURCE-FIRST PROFILE
DOCUMENTATION_QUALITY_PARITY        = REMEDIATION IMPLEMENTED
DOCUMENTATION_INTEGRATION           = CORRECTION IMPLEMENTED / QA REQUIRED
SCREENSHOT_ADMISSION                = BLOCKED UNTIL DOCUMENTATION GATE CLOSES
PUBLIC_TREE_QA                      = LOCKED
PUBLIC_BINARY_DISTRIBUTION          = N/A
FINAL_PUBLICATION_ACCEPTANCE        = OPEN
```

Final publication acceptance remains in `06_readiness/requirements_acceptance.md` and `release_readiness.md`; this file defines the requirement/CTQ baseline rather than the final release decision.
