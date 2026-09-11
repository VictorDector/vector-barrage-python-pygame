# Validation Policy

Project: **Vector Barrage**  
Release target: `v1.1.0`  
Publication profile: **Source-First Portfolio Repository**  
Status: ACTIVE

## Purpose

Define validation levels, evidence expectations and claim boundaries so syntax, imports, deterministic behavior, graphical execution, integration, packaging and publication readiness are never treated as equivalent.

## Validation Levels

| Level | Name | Question | Typical Evidence | Current publication role |
|---|---|---|---|---|
| `V1` | COMPILE | Is Python syntax/compiler acceptance valid? | targeted compile / automated tests | Required |
| `V2` | IMPORT | Can product modules/dependencies be imported? | controlled installation/import | Required |
| `V3` | BEHAVIOR | Does a defined unit/contract behave as required? | pytest / targeted assertions | Required |
| `V4` | GUI_AUDIO | Does the visible/audible application operate in the stated graphical runtime? | controlled source execution | Required |
| `V5` | INTEGRATION | Do collaborating components work end-to-end? | integrated runtime scenario | Required |
| `V6` | PACKAGED_RUNTIME | Does a generated standalone executable preserve required behavior? | native Windows packaged QA | Internal evidence / optional publication capability |
| `V7` | PUBLICATION | Is the intended public repository ready for its declared profile? | requirements, docs, evidence, licensing, public-tree and clean-checkout review | Required |

## Source Validation Boundary

Supported source contract:

```text
Python >=3.13,<3.14
Pygame ==2.6.1
```

Compilation/import success does not establish behavior. Automated tests do not replace GUI/audio observation. GUI success does not establish persistence. Each claim must match its evidence surface.

Behavior validation covers application transitions, player/enemy/projectile rules, collisions, scoring, strict new-record comparison, score parsing and migration, name validation, procedural audio, resource resolution, host-system fonts and controlled packaging contracts.

Tests that write scores must use isolated temporary paths unless runtime persistence is the explicit subject of the test.

## GUI / Integration Validation

Observable source checks include window startup, Main Menu, gameplay objects, HUD, Scores, About, Name Entry, Game Over, navigation controls and semantic audio cues.

Integration scenarios include:

```text
Menu -> Game -> Menu
Menu -> Scores -> Menu
Menu -> About -> Menu
Game -> Game Over -> New Record -> Name Entry -> storage -> Menu
process restart -> persisted score visible
```

## Packaged Runtime Validation

Packaged execution remains a distinct engineering surface. The accepted hardened Windows package completed:

```text
native build                  = PASS
archive hardening             = PASS
packaged runtime              = PASS
first-run score initialization= PASS
complete-relaunch persistence = PASS
```

Preserved hardened artifact:

```text
SHA-256 = 170ED5502A1D2D955EFA3CB52D13B880830657FF456166E6610DD30AB7E430A6
```

Under the current source-first portfolio profile this is **INTERNAL ENGINEERING EVIDENCE**, not a prerequisite to publish a downloadable executable. A successful build alone would never establish packaged-runtime PASS.

## Public Source Repository Validation

Publication readiness requires, as applicable:

- functional/source requirements accepted;
- automated tests and source runtime accepted;
- documentation integrity accepted;
- synthetic public data verified;
- media/provenance boundary clean;
- MIT repository license present;
- concise third-party notice aligned to Python/Pygame;
- publication scope finalized;
- screenshot evidence visually admitted before public use;
- clean public repository assembled without private/historical material;
- clean-checkout installation, tests and source smoke QA completed.

A packaged executable is not a publication prerequisite while `PUBLIC_EXE_DOWNLOAD=NO`.

## Result States

| State | Meaning |
|---|---|
| `PASS` | Acceptance boundary satisfied by matching evidence. |
| `PASS_WITH_NOTES` | Passed with non-blocking observations. |
| `CONDITIONAL` | Valid only under explicit conditions. |
| `FAIL` | Acceptance criterion not satisfied. |
| `BLOCKED` | A prerequisite/external condition prevents completion. |
| `PENDING` | Required validation not yet executed. |
| `CANDIDATE` | Implementation/evidence exists but final acceptance remains open. |
| `INTERNAL_EVIDENCE` | Valid evidence intentionally outside the public distribution surface. |
| `N/A` | Not applicable to the current publication profile. |

## Score-Test Isolation

```text
unit/storage QA      -> tmp_path or equivalent
E2E source QA        -> isolated temporary runtime directory
packaged QA          -> isolated writable Windows validation directory
release seed check   -> verify repository scores.txt remains synthetic
```

The versioned public `scores.txt` must never be consumed as disposable QA data.

## Evidence Ownership

- Requirements define what must be true.
- Tests/runtime executions produce evidence.
- `evidence/` indexes preserved evidence.
- `requirements_acceptance.md` decides requirement acceptance.
- `release_readiness.md` decides publication readiness.

## Current Validation Baseline

```text
V1 COMPILE / PACKAGE           = PASS within automated/source baseline
V2 IMPORT / INSTALL            = PASS
V3 BEHAVIOR                    = PASS — 125 automated tests
V4 GUI_AUDIO SOURCE            = PASS
V5 INTEGRATION SOURCE          = PASS
SOURCE RELAUNCH PERSISTENCE    = PASS
DOCUMENTATION INTEGRITY        = RECONCILED / APPROVAL REQUIRED
V6 PACKAGED_RUNTIME            = PASS / INTERNAL ENGINEERING EVIDENCE
V7 PUBLICATION                 = OPEN
SCREENSHOT ADMISSION           = PENDING
CLEAN PUBLIC TREE QA           = LOCKED
```

Historical `108` and `109` automated-test results remain valid for their original checkpoints but are superseded by the current `125 PASS` regression baseline.
