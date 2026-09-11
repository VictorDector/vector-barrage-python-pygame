# Behavioral Specification

Project: **Vector Barrage**  
Release target: `v1.1.0`  
Publication profile: **Source-First Portfolio Repository**  
Status: ACTIVE / AS-BUILT SOURCE BASELINE

## Purpose

Define the externally observable behavior and quality constraints that Vector Barrage must satisfy. This specification describes product outcomes, behavioral invariants, persistence semantics, runtime expectations and acceptance boundaries without duplicating component internals owned by the architecture documents.

The specification is as-built for the current source candidate. It is therefore both a behavioral contract and an acceptance reference for regression and release-readiness work.

## Product Identity

Vector Barrage is a local 2D fixed-shooter arcade game built with Python and Pygame.

Public identity constraints:

- product name: `Vector Barrage`;
- repository slug: `vector-barrage-python-pygame`;
- package: `vector_barrage`;
- author: Victor David Dector Ramirez;
- technical language: English;
- interface language: Spanish;
- no external franchise or course branding is used as the public product identity.

## 1. Application Navigation

The application exposes four Main Menu choices:

```text
MAIN MENU
├── GAME
├── SCORES
├── ABOUT
└── EXIT
```

Required outcomes:

```text
MENU -> GAME -> MENU
MENU -> SCORES -> MENU
MENU -> ABOUT -> MENU
MENU -> EXIT
```

Navigation invariants:

- one application coordinator owns state transitions;
- screens/gameplay return outcomes rather than recursively launching one another;
- repeated navigation must not grow a nested call chain;
- one active screen/session owns Pygame event retrieval at a time;
- audio ownership transitions deliberately with application state;
- cancellation/return outcomes must route through the coordinator;
- Exit terminates the application cleanly.

Acceptance requires repeated transitions to remain stable and non-recursive, not merely a successful first navigation.

## 2. Main Menu

The Main Menu shall:

- display Vector Barrage identity;
- expose Game, Scores, About and Exit;
- support keyboard-driven option movement and confirmation;
- dispatch one selected action once;
- start/stop menu audio through the semantic audio boundary;
- return one application outcome to the coordinator;
- avoid constructing secondary screens directly.

A menu-selection input must not produce multiple state transitions from one intended confirmation event.

## 3. Gameplay

### 3.1 Player

The player shall:

- be visually distinguishable from enemies;
- move horizontally in response to supported input;
- remain within configured horizontal bounds;
- fire through controlled input handling;
- avoid unintended duplicate projectile creation from one intended firing action;
- participate in collision, damage and life-loss rules;
- expose authoritative state to the renderer rather than maintaining a second presentation-only position/state copy.

### 3.2 Enemies

The game shall:

- create an enemy wave/formation from configured rules;
- update enemy movement deterministically for the defined model;
- keep enemy model state synchronized with rendering/collision processing;
- remove an enemy exactly once after one consuming valid collision;
- trigger progression only after the applicable wave-clear condition is satisfied;
- avoid retaining destroyed enemies in authoritative gameplay state.

### 3.3 Projectiles and Collisions

Player projectiles shall:

- originate from the active player state;
- move through the playable area;
- remain renderable while active;
- be removed when invalid/out of bounds or after a consuming collision;
- resolve no more than the intended target per consumed collision.

A confirmed kill obeys:

```text
valid projectile/enemy overlap
-> consume intended projectile
-> remove intended enemy
-> increase score once
-> emit one enemy-destruction event
```

One resolved collision must not double-score or emit duplicate destruction semantics.

### 3.4 Lives, Level and Game Over

Gameplay maintains one authoritative set of:

- lives;
- level;
- score;
- current wave/progression state;
- completion/loss outcome.

A life-loss event decrements according to the configured rule. A valid wave-clear condition advances progression. The applicable terminal loss condition reaches Game Over and returns a game result to the application coordinator.

### 3.5 HUD

The HUD shall visibly expose current:

- lives;
- score;
- level.

HUD values must reflect authoritative gameplay state for the current frame rather than stale initialization values or independently maintained counters.

### 3.6 Game Result Boundary

Gameplay returns a result to the application layer rather than directly owning post-game identity persistence.

Conceptually:

```text
gameplay loop
-> GameSessionResult
-> application coordinator
-> record eligibility decision
-> optional Name Entry
-> optional persistence
```

A non-completion/cancel/exit outcome does not enter record persistence merely because a score value exists.

## 4. Score Model

The application maintains one authoritative numeric gameplay score.

Required behavior:

- a new session begins from the configured initial score;
- only confirmed scoring events increase the score;
- one confirmed scoring event increments once;
- HUD score and final returned score refer to the same authoritative value;
- final record eligibility is evaluated only after the relevant completed game outcome.

A completed game is a new record only when:

```text
final_score > previous_max_score
```

A tie is not a new record. If no valid prior record exists, maximum score is `0`. A non-completion exit does not enter record handling.

## 5. Score Reading and Presentation

Records use:

```text
name,score
```

Storage shall:

- read UTF-8-compatible input, including tolerated BOM handling;
- trim surrounding whitespace;
- reject empty/whitespace-only names;
- ignore malformed rows rather than terminating the application;
- ignore non-numeric scores;
- reject invalid negative score values;
- sort valid records numerically in descending order;
- expose the maximum valid score or `0` when none exists;
- return at most the requested Top-N set, with Top 5 used by the Scores screen.

The Scores screen shall remain usable when:

- the score file is empty;
- no valid rows exist;
- malformed rows are mixed with valid rows;
- fewer than five valid records exist.

## 6. New-Record Name Entry

Only a strict new record enters name entry.

Required behavior:

- input is normalized before acceptance;
- names must be nonempty after trimming;
- commas and line breaks are rejected because they conflict with the record format;
- configured maximum length is enforced;
- cancellation produces an explicit non-submission outcome;
- accepted input returns to the application coordinator;
- Name Entry does not own the score-file append;
- one accepted submission results in exactly one persistence call.

Repeated frame processing or key handling must not duplicate one accepted record.

## 7. Persistence Contract

Canonical runtime filename:

```text
scores.txt
```

### 7.1 Source Runtime

Source execution resolves writable score data from the stable project/runtime root. The behavior must not depend on a developer-specific absolute path.

### 7.2 Frozen / Packaged Runtime

Frozen/local packaging execution resolves durable writable `scores.txt` beside the executable rather than attempting to persist only inside PyInstaller temporary extraction state.

The bundled score seed is read-only initialization material, not the authoritative persistent file after runtime initialization.

### 7.3 Canonical / Legacy / Seed Precedence

```text
scores.txt exists
-> use scores.txt

scores.txt absent + puntajes.txt exists
-> migrate/copy to scores.txt when possible
-> use canonical scores.txt

migration cannot be written
-> preserve/read puntajes.txt rather than destroy or ignore valid legacy data

neither runtime file exists + approved seed available
-> initialize scores.txt from the seed
```

Once canonical data exists it has precedence. Existing canonical data must never be overwritten by legacy input or bundled seed initialization.

### 7.4 Write Integrity

A score append shall:

- use the authoritative resolved writable path;
- persist one normalized accepted name/score record;
- preserve existing canonical data;
- avoid incidental writes from tests to the versioned public seed.

## 8. Public Seed

The versioned public seed remains synthetic:

```text
PLAYER_01,500
PLAYER_02,350
PLAYER_03,250
PLAYER_04,150
PLAYER_05,100
```

The repository seed is product data, not disposable QA state. Automated and manual write-path tests use isolated temporary/runtime data unless the explicit subject of validation is the actual public seed integrity check.

## 9. Audio Behavior

Vector Barrage uses procedural runtime audio rather than external game-audio files.

Semantic roles:

- Main Menu loop;
- gameplay loop;
- enemy-destruction one-shot;
- new-record cue/sequence.

Lifecycle expectations:

```text
MENU
-> menu audio active
-> stop/transition before leaving MENU

GAME
-> gameplay audio active
-> confirmed enemy destruction -> one destruction cue
-> stop/transition before leaving GAME

STRICT NEW RECORD
-> new-record cue
-> Name Entry flow
-> return to coordinator
```

Audio failures fail soft rather than preventing application startup or deterministic gameplay logic from operating. Tests may substitute an injectable no-op audio implementation where physical audio output is not part of the claim.

## 10. Visual / Font Behavior

Visual presentation is generated through Pygame primitives and text rendered with approved host-system fonts.

Required visual surfaces include:

- Main Menu;
- playfield/background;
- player;
- enemies;
- projectile;
- HUD;
- Game Over;
- Scores;
- About;
- Name Entry.

No copied gameplay artwork, audio asset or project font binary is required for `v1.1.0`.

Font resolution is centralized through the approved host-font boundary. Missing host-font capability must fail explicitly rather than silently introducing a copied font artifact into the repository.

## 11. About Screen

The About screen shall:

- identify the product as Vector Barrage;
- identify Victor David Dector Ramirez as author;
- identify Python/Pygame as the implementation technology;
- expose the approved repository target;
- route external navigation through the dedicated link boundary;
- avoid unapproved logos/branding;
- return cleanly to Main Menu through the coordinator.

Approved target:

```text
https://github.com/VictorDector/vector-barrage-python-pygame
```

## 12. Runtime and Reproducibility

Supported dependency contract:

```text
Python >=3.13,<3.14
Pygame ==2.6.1
```

`pyproject.toml` is canonical. Source entry point:

```bash
python -m vector_barrage
```

The project shall avoid user-specific absolute paths and hidden dependency manifests that conflict with `pyproject.toml`.

The source repository must remain installable through the documented virtual-environment/editable-install workflow.

## 13. Event Ownership

Only one active loop owns Pygame event retrieval at a time.

Rules:

- Menu owns menu event retrieval while active;
- Scores owns score-screen events while active;
- About owns About-screen events while active;
- Name Entry owns its local input events while active;
- gameplay session retrieves gameplay events once per frame;
- lower-level model/rules functions do not independently drain the event queue;
- the application coordinator dispatches states without recursively nesting complete UI lifecycles.

## 14. Resource / Persistence Separation

Read-only resource lookup and writable score persistence are separate concerns.

Required invariants:

- resource resolution must not own score writes;
- storage must not depend on Pygame GUI behavior;
- writable score paths remain stable across source/frozen execution semantics;
- public runtime does not require copied external gameplay media.

## 15. Optional Packaged Runtime Contract

Packaging is an engineering capability rather than a public-distribution requirement under the current profile.

A packaged candidate, when built, must preserve:

- Menu/Game/Scores/About flow;
- generated visual/audio behavior;
- approved host-font operation;
- synthetic first-run seed initialization;
- writable canonical scores beside the executable;
- canonical precedence over legacy/seed data;
- complete-relaunch persistence.

The accepted hardened Windows package has already passed these packaged-runtime requirements and is preserved as internal engineering evidence. It is **not distributed publicly** under the current source-first profile.

Public executable distribution would require a separate future scope/compliance decision; it is not part of this specification's current publication acceptance target.

## 16. Technical Naming

```text
modules/files       -> snake_case
classes             -> PascalCase
functions/methods   -> snake_case
variables           -> snake_case
constants           -> UPPER_SNAKE_CASE
```

Spanish remains valid for user-visible UI. `puntajes.txt` exists only at the explicit compatibility boundary.

## 17. Public Data / Provenance Boundary

Public source and evidence must not depend on unresolved historical/private game media or data.

Current intended boundary:

```text
public source expression         = Vector Barrage implementation
public score seed                = synthetic
visual presentation              = generated by project source + host font
runtime audio                    = generated by project source
external gameplay artwork/audio  = none required
historical/private player data   = excluded
public executable                = not distributed
```

Third-party software libraries remain under their own licenses and are not relicensed by the Vector Barrage MIT license.

## 18. Acceptance Matrix

| Area | Required Outcome | Current Status |
|---|---|---|
| Package/install | Candidate installs under supported Python | PASS |
| Automated regression | Full current suite passes | PASS — 125 |
| Main Menu/navigation | Game/Scores/About/Exit; repeated non-recursive transitions | PASS |
| Player | Bounded movement and controlled firing | PASS |
| Enemy progression | Deterministic formation/progression behavior | PASS |
| Collisions | One kill → one consumed collision / score / destruction event | PASS |
| Lives / Game Over | Authoritative state and terminal loss flow operate | PASS |
| HUD | Lives/score/level are current | PASS |
| Score parsing | Valid parse + malformed tolerance + invalid-row rejection | PASS |
| Top 5/max | Descending results and maximum | PASS |
| New record | Strict `>`; tie false | PASS |
| Name entry | Validation + explicit cancel/accept + one accepted submission | PASS |
| Canonical persistence | `scores.txt` read/write and precedence rules | PASS |
| Legacy compatibility | Migration/fallback only when canonical absent | PASS |
| Source GUI/audio | Supported graphical source run | PASS |
| Source E2E/relaunch | Record flow and restart persistence | PASS |
| Event ownership | One active event owner; no recursive lifecycle | PASS |
| Host-system font boundary | UI renders without copied project font asset | PASS |
| Generated media | No external gameplay image/audio dependency | PASS |
| Public seed | Synthetic only | PASS |
| Dependency metadata | `pyproject.toml` canonical and compatible | PASS |
| Documentation/licensing | MIT + NOTICE + source-first dossier | REMEDIATION IMPLEMENTED / QA REQUIRED |
| Windows package | Hardened standalone engineering artifact | PASS / INTERNAL EVIDENCE |
| Packaged persistence | Complete relaunch persistence | PASS / INTERNAL EVIDENCE |
| Fresh screenshots | Four captures | CAPTURED / QA PENDING |
| Clean public repository | Exact public tree assembled and validated | NOT CREATED |
| Public release | Source-first portfolio publication | OPEN |

## 19. Validation / Publication Boundary

Source validation does not automatically establish packaged validation; packaged validation does not imply public binary distribution. Automated tests do not replace GUI/audio observation. Screenshot captures do not become public evidence until admitted. Final publication requires the exact public source tree, accepted evidence and clean-checkout QA.

Current public profile:

```text
SOURCE_REPOSITORY           = YES
PUBLIC_EXECUTABLE_DOWNLOAD  = NO
AUTOMATED_BASELINE          = 125 PASS
MIT_LICENSE                 = PASS
THIRD_PARTY_NOTICE          = PASS
DOCUMENTATION_PARITY        = REMEDIATION IMPLEMENTED / QA REQUIRED
SCREENSHOT_ADMISSION        = BLOCKED UNTIL DOC QA/APPROVAL
```
