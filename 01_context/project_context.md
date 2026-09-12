# Project Context — Vector Barrage

Release target: `v1.1.0`  
Publication profile: **Source-First Portfolio Repository**

## Product Definition

Vector Barrage is an independently implemented fixed-shooter arcade game built with Python and Pygame. The public portfolio release demonstrates application coordination, deterministic gameplay, persistence, procedural presentation, automated testing and engineering documentation.

Public product identity:

```text
Product           = Vector Barrage
Repository target = VictorDector/vector-barrage-python-pygame
Author            = Victor David Dector Ramirez
Technical stack   = Python 3.13.x + Pygame 2.6.1
UI language       = Spanish
Public profile    = SOURCE-FIRST PORTFOLIO
Package version   = 1.1.0
```

The public product identity does not use historical course/provider branding or third-party game branding as its own product identity.

## Project Classification

| Field | Value |
|---|---|
| Project type | Desktop software / portfolio engineering project |
| Domain | 2D fixed-shooter game development |
| Runtime | Python / Pygame |
| Package model | Installable Python package under `src/vector_barrage/` |
| Primary execution target | Source execution with Python 3.13.x |
| Secondary engineering target | Controlled PyInstaller Windows packaging |
| Persistence model | Local filesystem score persistence |
| Public distribution model | Source-first Git repository |
| Public executable | Not distributed under the current profile |
| Technical language | English |
| User-interface language | Spanish |

## Engineering / Portfolio Value

The project is intended to demonstrate more than a working game loop. Its engineering value includes:

- explicit application-state coordination rather than recursive screen construction;
- deterministic gameplay rules separated from active Pygame runtime and rendering concerns;
- clear ownership of event retrieval, score persistence, resource resolution, audio and UI fonts;
- canonical score parsing, migration/fallback and exactly-once persistence behavior;
- reproducible package/dependency metadata through `pyproject.toml`;
- automated regression across gameplay, storage, navigation, services, fonts and packaging contracts;
- source/runtime evidence separated from packaged-runtime evidence and public-release claims;
- provenance-safe generated visual/audio presentation;
- controlled packaging configuration retained as reproducible engineering evidence;
- requirement, architecture, governance, implementation and release traceability through the engineering dossier.

For portfolio review, the repository is expected to show not only what the application does, but how its behavior, architecture, validation evidence and publication boundary are controlled.

## Intended Audience

The public repository is designed for:

- software-engineering and Python reviewers;
- technical recruiters or hiring managers evaluating implementation quality;
- developers who want to install and run the project from source;
- reviewers interested in architecture, testing, persistence, packaging or release-readiness practices.

The repository does not assume access to the historical private development repository or its internal project-management history.

## Publication Objective

The source-first repository allows a reviewer to:

- inspect the application source and architecture;
- install declared dependencies using standard Python tooling;
- run the game from source;
- run the automated regression suite;
- inspect requirements, architecture decisions, policies, runbooks and readiness evidence;
- review accepted screenshot evidence within its declared claim boundary;
- inspect the controlled PyInstaller configuration as engineering evidence.

A downloadable standalone Windows executable is **not** part of the current publication profile.

## Functional Scope

The implemented application includes:

- main menu with Game, Scores, About and Exit flows;
- iterative, non-recursive application navigation;
- player movement and firing;
- deterministic enemy progression;
- collision handling, score, lives and levels;
- Game Over and strict new-record flow;
- valid-name entry and exactly-once score persistence;
- UTF-8 score parsing, malformed-record tolerance and Top 5 display;
- canonical `scores.txt` initialization and legacy migration/fallback behavior;
- procedural audio;
- procedural/geometric visual presentation;
- host-system font resolution;
- source and packaging-focused automated tests.

## Runtime Boundary

Declared runtime requirements:

```text
Python >=3.13,<3.14
pygame==2.6.1
```

The public repository does not vendor Python or Pygame binaries. Users install dependencies through the normal Python package workflow.

## Development and Execution Environments

The product architecture is platform-oriented rather than tied to one developer machine.

### General source execution

The public path uses a Python 3.13 virtual environment, editable project installation and:

```bash
python -m vector_barrage
```

The source workflow is documented for Linux/WSL/macOS and Windows PowerShell in `05_implementation/execution_runbook.md`.

### Validated WSL2 / X11 source profile

A WSL2 graphical source route has been exercised and remains a reproducible diagnostic/validation profile. When the normal graphical path is unavailable, an explicit X11 bridge such as XLaunch or VcXsrv can be used with the documented `DISPLAY`/`SDL_VIDEODRIVER` configuration.

This host display bridge is an environment-specific source-execution aid. It is not an architectural dependency of the game logic or of the Windows package.

### Windows packaged engineering profile

A hardened Windows package was built and validated using the controlled PyInstaller configuration. That profile is preserved as internal engineering evidence and is not the public distribution model for the current release target.

## Data Boundary

The default public score seed is synthetic:

```text
PLAYER_01,500
PLAYER_02,350
PLAYER_03,250
PLAYER_04,150
PLAYER_05,100
```

Historical/private player data is not part of the public release.

## Media Boundary

Vector Barrage does not require copied external gameplay artwork, sprite assets, music files, sound-effect files or a bundled project font asset.

```text
Visuals    = generated with Pygame primitives
UI fonts   = resolved from approved host-system fonts
Audio      = procedurally generated PCM tones
Score seed = synthetic text data
```

This boundary is both a technical design decision and a provenance control.

## Architecture Boundary

Public source is organized as a Python package under `src/vector_barrage/` with explicit responsibilities for:

- application coordination;
- configuration/resource location;
- storage;
- audio;
- host-system fonts;
- gameplay model/rules/session/rendering;
- screen-specific UI behavior.

Detailed structures are documented in `02_architecture/` and `04_solution/`.

## Project Constraints

1. `pyproject.toml` remains the canonical dependency/build metadata source unless a later reproducibility need justifies an additional synchronized manifest.
2. Public source must not depend on user-specific absolute filesystem paths.
3. Application navigation must remain non-recursive and event ownership must remain explicit.
4. Canonical score data must not be overwritten by legacy input or seed initialization once it exists.
5. Tests that mutate score data must use isolated temporary/runtime locations rather than the repository seed.
6. Public visual/audio behavior must remain within the approved generated-media/provenance boundary unless a later media change completes provenance and licensing review.
7. Source validation, packaged-runtime validation and public-release readiness remain separate claim boundaries.
8. The current publication profile must not imply that a public `VectorBarrage.exe` download exists.
9. Public documentation must describe the as-built product and current release state rather than private workflow mechanics.
10. Evidence used for public claims must match the exact Vector Barrage claim boundary it supports.

## Out of Scope

The current release target does not require:

- multiplayer or network gameplay;
- authentication or user accounts;
- online leaderboards or backend services;
- cloud deployment infrastructure;
- production telemetry or live-service operations;
- mobile/web ports;
- a public downloadable Windows executable;
- binary-specific redistribution compliance while binary distribution remains disabled;
- external gameplay artwork/audio merely to imitate the historical implementation.

Future scope changes may introduce these capabilities only through explicit design, validation and publication decisions.

## Quality Baseline

Current accepted source/configuration regression:

```text
AUTOMATED_TESTS = 125 PASS
FINAL_PUBLIC_TREE_QA = PASS / ACCEPTED
```

Earlier 108/109-test results are preserved as historical checkpoints but are superseded by the current baseline.

The source implementation has also undergone manual runtime/persistence validation. A hardened Windows package was built and validated internally as an additional engineering exercise.

## Packaging Boundary

Controlled packaging material is retained under `packaging/` for reproducibility and engineering review. The final internal hardened package was produced from source/configuration snapshot:

```text
0e1951c67f19b9eff24937ff1e1d228bfd72ff8b
```

and validated as:

```text
VectorBarrage.exe
11230689 bytes
SHA-256 170ED5502A1D2D955EFA3CB52D13B880830657FF456166E6610DD30AB7E430A6
```

This artifact is **INTERNAL ENGINEERING EVIDENCE**. It is not committed to or distributed from the public portfolio repository under the current profile.

## Licensing Boundary

Vector Barrage-owned material is licensed under MIT through the repository `LICENSE`.

Python, Pygame and development/build tooling remain third-party software under their own licenses. `NOTICE.md` records this separation. Because the current public profile distributes source rather than the bundled Windows executable, full binary redistribution compliance remains optional future work.

## Evidence Boundary

Current public-evidence direction:

```text
source/runtime evidence       = accepted
source persistence evidence   = accepted
screenshots EVD-VB-001..003   = accepted current references
EVD-VB-004 About screenshot   = accepted pre-fix reference
screenshot replacement        = waived by release owner
independent screenshot QA     = not claimed
final About layout            = pass / owner verified
packaged Windows evidence     = internal engineering evidence
public executable             = not distributed
```

Only evidence aligned to its declared claim boundary may support public claims.

## Current Project State

```text
SOURCE_IMPLEMENTATION                  = PASS / ACCEPTED
PACKAGE_VERSION                        = 1.1.0
AUTOMATED_REGRESSION                   = 125 PASS
MIT_LICENSE                            = PASS / ACCEPTED
THIRD_PARTY_NOTICE                     = PASS / ACCEPTED
SOURCE_FIRST_PUBLICATION_PROFILE       = APPROVED
PUBLIC_EXECUTABLE_DOWNLOAD             = NO
SCREENSHOT_ADMISSION                   = ACCEPTED / OWNER DECISION
EVD-VB-004                             = PRE-FIX REFERENCE / REPLACEMENT WAIVED
ABOUT_LAYOUT_FINAL                     = PASS / OWNER VERIFIED
PUBLIC_REPOSITORY                      = PUBLISHED
FINAL_PUBLIC_TREE_QA                   = PASS / ACCEPTED
DOCUMENTATION_RECONCILIATION           = PASS / ACCEPTED
PUBLIC_RELEASE_READY                   = YES
TAG_v1.1.0                             = PENDING
```
