# Identifier Registry

Project: **Vector Barrage**  
Release target: `v1.1.0`  
Publication profile: **Source-First Portfolio Repository**  
Status: ACTIVE

## Purpose

Maintain stable, human-readable identifiers for the public product, runtime components, data artifacts, build surfaces and validation evidence. The registry describes the current Vector Barrage implementation; it is not a migration ledger for earlier private source names.

## Product Identifiers

| Field | Value |
|---|---|
| Product name | `Vector Barrage` |
| Repository slug | `vector-barrage-python-pygame` |
| Repository target | `VictorDector/vector-barrage-python-pygame` |
| Python distribution | `vector-barrage` |
| Python package | `vector_barrage` |
| Release target | `v1.1.0` |
| Current package version | `1.1.0a0` |
| Author | Victor David Dector Ramirez |
| UI language | Spanish (`es`) |
| Technical language | English |
| Publication profile | Source-First Portfolio Repository |
| Public executable | Not distributed |

## State Vocabulary

| State | Meaning |
|---|---|
| `ACTIVE` | Current product artifact or component. |
| `CANDIDATE` | Implemented or prepared but awaiting the applicable acceptance gate. |
| `PASS` | The stated validation boundary has been satisfied. |
| `CLOSED` | A defined product change or decision completed its acceptance boundary. |
| `VALIDATED` | A named runtime/build/profile surface has matching observed evidence. |
| `INTERNAL EVIDENCE` | Accepted engineering evidence intentionally excluded from the current public publication surface. |
| `PENDING` | Required work has not yet been completed. |
| `N/A` | Not applicable to the current product/publication design. |
| `OPTIONAL FUTURE` | Not required now; becomes active only after a future scope decision. |
| `COMPATIBILITY ONLY` | Retained only at an explicit backward-compatibility boundary. |
| `SUPERSEDED` | Replaced by a later accepted artifact/decision while remaining traceable. |

Scoped qualifiers may accompany a core state when the boundary matters. Such qualifiers narrow a state; they do not silently upgrade it.

## Runtime Component Registry

| ID | Component | Physical artifact | Primary responsibility | State |
|---|---|---|---|---|
| `VB-APP-001` | Package entry point | `src/vector_barrage/__main__.py` | Dispatch package execution to the application entry point. | ACTIVE |
| `VB-APP-002` | Application coordinator | `src/vector_barrage/app.py` | Own application states, transitions, screen/game orchestration, record flow and runtime score-path selection. | ACTIVE |
| `VB-CFG-001` | Application configuration | `src/vector_barrage/config.py` | Product identity, dimensions, FPS and interface-language configuration. | ACTIVE |
| `VB-RES-001` | Resource boundary | `src/vector_barrage/resources.py` | Resolve stable source/frozen read-only resource roots independently of writable persistence. | ACTIVE |
| `VB-DAT-001` | Score storage | `src/vector_barrage/storage.py` | Parse, order, migrate, resolve and append local score records. | ACTIVE |
| `VB-AUD-001` | Audio service | `src/vector_barrage/audio.py` | Semantic audio contract and procedural PCM synthesis. | ACTIVE |
| `VB-LNK-001` | External-link service | `src/vector_barrage/links.py` | Validate/open approved URLs and isolate browser/platform bridging. | ACTIVE |
| `VB-FNT-001` | UI font resolver | `src/vector_barrage/ui_fonts.py` | Resolve approved host-system fonts and fail closed if none are available. | ACTIVE / VALIDATED |
| `VB-GAM-001` | Gameplay model | `src/vector_barrage/gameplay/model.py` | Represent player, enemy, projectile and game state. | ACTIVE |
| `VB-GAM-002` | Gameplay rules | `src/vector_barrage/gameplay/rules.py` | Deterministic movement, collision, scoring, damage and record rules. | ACTIVE |
| `VB-GAM-003` | Gameplay session | `src/vector_barrage/gameplay/session.py` | Own the active Pygame gameplay loop and return one session result. | ACTIVE |
| `VB-GAM-004` | Gameplay renderer | `src/vector_barrage/gameplay/renderer.py` | Render geometry, HUD and state presentation. | ACTIVE |
| `VB-UI-001` | Main Menu | `src/vector_barrage/screens/menu.py` | Present primary navigation and return one menu choice. | ACTIVE |
| `VB-UI-002` | Scores | `src/vector_barrage/screens/scores.py` | Present ordered Top-5 score records and return control. | ACTIVE |
| `VB-UI-003` | About | `src/vector_barrage/screens/about.py` | Present product/author/technology information and approved external links. | ACTIVE |
| `VB-UI-004` | Name Entry | `src/vector_barrage/screens/name_entry.py` | Capture and normalize one record name without directly persisting it. | ACTIVE |

## Packaging Component Registry

| ID | Component | Physical artifact | Responsibility | State |
|---|---|---|---|---|
| `VB-PKG-001` | Windows packaging launcher | `packaging/vector_barrage_launcher.py` | Absolute-import bootstrap used by PyInstaller. | VALIDATED / PUBLIC SOURCE |
| `VB-PKG-002` | Controlled PyInstaller specification | `packaging/VectorBarrage.spec` | Define hardened one-file/windowed build, resource inclusion and explicit exclusions. | VALIDATED / PUBLIC SOURCE |
| `VB-PKG-003` | Pygame packaging hook | `packaging/hooks/hook-pygame.py` | Collect required Pygame dynamic libraries without copying unnecessary Pygame data. | VALIDATED / PUBLIC SOURCE |

These files are public as reproducible engineering evidence. The generated Windows executable is not distributed under the current publication profile.

## Data Artifact Registry

| ID | Artifact | Contract | State |
|---|---|---|---|
| `VB-DATA-001` | `scores.txt` | Canonical UTF-8 `name,score` data file and synthetic public seed. | ACTIVE |
| `VB-DATA-002` | `puntajes.txt` | Optional legacy compatibility input recognized only when canonical data is absent. | COMPATIBILITY ONLY |
| `VB-DATA-003` | Public seed | `PLAYER_01`..`PLAYER_05` synthetic records. | PASS |

## Runtime / Build Profiles

| ID | Profile | Definition | State |
|---|---|---|---|
| `VB-RUN-001` | `SOURCE_WSL2_X11` | Python 3.13.x + Pygame 2.6.1 source execution in the validated WSL2/X11 environment. | VALIDATED |
| `VB-RUN-002` | `WINDOWS_PACKAGED_HARDENED` | Hardened `VectorBarrage.exe` built with Python 3.13.15 / Pygame 2.6.1 / PyInstaller 6.22.2 on Windows 11 x64. | VALIDATED / INTERNAL EVIDENCE |
| `VB-QA-001` | Automated suite | Current pytest suite under the target Python/Pygame environment. | 125 PASS / CURRENT BASELINE |

Historical test checkpoints:

```text
108 PASS = CLOSED / HISTORICAL
109 PASS = CLOSED / SUPERSEDED BASELINE
125 PASS = CURRENT ACCEPTED BASELINE
```

Accepted hardened Windows artifact identity:

```text
SOURCE_SNAPSHOT = 0e1951c67f19b9eff24937ff1e1d228bfd72ff8b
VectorBarrage.exe
11230689 bytes
SHA-256: 170ED5502A1D2D955EFA3CB52D13B880830657FF456166E6610DD30AB7E430A6
PUBLICATION: INTERNAL EVIDENCE / NOT DISTRIBUTED
```

## Evidence Identifiers

| ID | Surface | State / publication disposition |
|---|---|---|
| `EVD-VB-001` | Main Menu screenshot | CAPTURED / QA PENDING |
| `EVD-VB-002` | Gameplay/HUD screenshot | CAPTURED / QA PENDING |
| `EVD-VB-003` | Scores screenshot | CAPTURED / QA PENDING |
| `EVD-VB-004` | About screenshot | CAPTURED / QA PENDING |
| `EVD-VB-005` | Source runtime validation | PASS / PUBLIC ENGINEERING EVIDENCE |
| `EVD-VB-006` | Source persistence/relaunch validation | PASS / PUBLIC ENGINEERING EVIDENCE |
| `EVD-VB-007` | Packaged runtime validation record | INTERNAL EVIDENCE / EXCLUDE FROM FINAL PUBLIC COPY |
| `EVD-VB-008` | Packaged persistence/relaunch validation record | INTERNAL EVIDENCE / EXCLUDE FROM FINAL PUBLIC COPY |

Current physical screenshot filenames use `EVD-001` through `EVD-004`. Canonical documentation IDs use `EVD-VB-001` through `EVD-VB-004`. This mismatch is intentionally left OPEN until the screenshot-admission gate, where content and filename normalization will be handled together.

## Media Identifiers

Vector Barrage `v1.1.0` does not require binary gameplay media assets.

| ID | Media surface | Implementation | State |
|---|---|---|---|
| `VB-MEDIA-001` | Visual presentation | Pygame primitives + host-system font rendering. | VALIDATED |
| `VB-MEDIA-002` | Menu audio | Procedurally synthesized PCM tone pattern. | VALIDATED |
| `VB-MEDIA-003` | Gameplay audio | Procedurally synthesized PCM tone pattern. | VALIDATED |
| `VB-MEDIA-004` | Enemy-destruction cue | Procedural one-shot PCM effect. | VALIDATED |
| `VB-MEDIA-005` | New-record cue | Procedural success PCM sequence. | VALIDATED |

No external gameplay image/audio directory is required unless a future approved product change introduces independently created or appropriately licensed media.

## Licensing Identifiers

```text
VB-LIC-001 = MIT repository LICENSE / ACCEPTED
VB-LIC-002 = concise third-party NOTICE / ACCEPTED
VB-LIC-003 = full binary compliance package / OPTIONAL FUTURE
```

Python, Pygame and development/build tooling remain governed by their own licenses.

## Naming Contract

```text
modules/files       -> snake_case
classes             -> PascalCase
functions/methods   -> snake_case
variables           -> snake_case
constants           -> UPPER_SNAKE_CASE
package             -> snake_case
```

Spanish is intentionally retained for user-facing interface text. Legacy Spanish appears in the technical layer only at the explicit `puntajes.txt` compatibility boundary.
