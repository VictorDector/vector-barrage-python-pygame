# Solution Map

Project: **Vector Barrage**  
Release target: `v1.1.0`  
Publication profile: **Source-First Portfolio Repository**  
Status: AS-BUILT / DOCUMENTATION INTEGRATION CORRECTION IMPLEMENTED

## Purpose

Map product capabilities to physical implementation artifacts, requirements, integration contracts, validation surfaces and current publication state.

Detailed responsibilities belong in `02_architecture/`; acceptance criteria in `01_context/requirement_ctq_map.md`; validation semantics in `03_governance/validation_policy.md`.

## 1. Capability-to-Implementation Map

| Capability | Implementation | Requirement | Current State |
|---|---|---|---|
| Package entry | `src/vector_barrage/__main__.py` | `NFR-01` | PASS |
| Application coordination | `app.py` | `FR-01`, `NFR-03` | PASS |
| Runtime configuration | `config.py` | `NFR-01`, `NFR-08` | PASS |
| Read-only resources | `resources.py` | `NFR-07` | PASS |
| Score parsing/persistence | `storage.py` | `FR-06`, `FR-08`, `NFR-04` | PASS |
| Procedural audio | `audio.py` | `FR-09`, `NFR-06` | PASS |
| Host-system font resolution | `ui_fonts.py` | `FR-10`, source media boundary | PASS |
| External links | `links.py` | `FR-11` | PASS |
| Gameplay state | `gameplay/model.py` | `FR-02`–`FR-05` | PASS |
| Gameplay rules | `gameplay/rules.py` | `FR-02`–`FR-08` | PASS |
| Gameplay session | `gameplay/session.py` | `FR-02`–`FR-05`, `FR-09` | PASS |
| Gameplay rendering | `gameplay/renderer.py` | `FR-05`, `FR-10` | PASS |
| Main Menu | `screens/menu.py` | `FR-01` | PASS |
| Scores | `screens/scores.py` | `FR-06` | PASS |
| About | `screens/about.py` | `FR-11` | PASS |
| Name Entry | `screens/name_entry.py` | `FR-07` | PASS |
| Synthetic score seed | `scores.txt` | `NFR-05` | PASS |
| Dependency/build metadata | `pyproject.toml` | `NFR-01` | PASS |
| Automated regression | `tests/` | `NFR-09` | 125 PASS |
| Controlled packaging config | `packaging/` | `NFR-11` | PASS / PUBLIC ENGINEERING SOURCE |
| Hardened Windows package | generated `VectorBarrage.exe` | `NFR-11` | PASS / INTERNAL EVIDENCE |
| Packaged persistence | executable-dir `scores.txt` | `NFR-12` | PASS / INTERNAL EVIDENCE |
| MIT license | `LICENSE` | `NFR-14` | PASS / ACCEPTED |
| Third-party boundary | `NOTICE.md` | `NFR-14` | PASS / ACCEPTED |
| Engineering dossier | README + `00`–`06` | `NFR-13` | PARITY REMEDIATED / INTEGRATION CORRECTION IMPLEMENTED / QA REQUIRED |
| Screenshot evidence | `evidence/screenshots/` | `NFR-15` | CAPTURED / QA PENDING / BLOCKED BY DOC GATE |
| Clean public tree | target public repository | `NFR-16` | NOT CREATED |

## 2. Physical Dependency Map

```text
__main__.py
└── app.py
    ├── config.py
    ├── resources.py
    ├── storage.py
    ├── audio.py
    ├── gameplay/session.py
    │   ├── gameplay/model.py
    │   ├── gameplay/rules.py
    │   └── gameplay/renderer.py
    │       └── ui_fonts.py
    ├── screens/menu.py
    ├── screens/scores.py
    │   └── storage.py
    ├── screens/about.py
    │   └── links.py
    └── screens/name_entry.py
```

Screens also use the shared host-font/config boundaries as required. The application layer is the principal composition root.

## 3. Navigation Contract

```text
MENU -> GAME   -> MENU
MENU -> SCORES -> MENU
MENU -> ABOUT  -> MENU
MENU -> EXIT
```

Secondary states return outcomes to the application coordinator rather than recursively creating a new Main Menu.

## 4. Gameplay Contract

```text
input
  -> GameSession
      -> movement/fire interpretation
      -> enemy/projectile updates
      -> Rules
           -> collision / score / damage / progression
      -> Renderer
      -> enemy-destroyed semantic event -> AudioService
  -> GameSessionResult(final_score, outcome, completed)
```

One consumed collision may produce one destruction/score event only.

## 5. New-Record / Persistence Contract

```text
completed game
-> final score
-> storage.max_score(scores.txt)
-> strict > comparison
   false -> MENU
   true  -> new-record audio
         -> Name Entry
         -> normalized valid name
         -> append_score() once
         -> MENU
```

## 6. Score Resolution Contract

```text
scores.txt exists
-> authoritative canonical file

no scores.txt + puntajes.txt exists
-> migrate/copy when possible
-> otherwise preserve/read legacy

neither exists
-> initialize from bundled synthetic seed when available
```

Canonical data has precedence after it exists.

## 7. Media Contract

```text
model state
-> renderer/screens
-> Pygame primitives + host-system font
-> display

semantic event
-> AudioService
-> source-defined ToneSegment sequence
-> PCM synthesis
-> Pygame mixer
```

No gameplay image/audio asset tree is required.

## 8. Execution Paths

### Source — validated/public

```text
Python 3.13.x / Pygame 2.6.1
-> install from pyproject.toml
-> python -m vector_barrage
```

### Windows package — validated/internal evidence

```text
Windows
└── VectorBarrage.exe
    ├── packaged Python/Pygame runtime
    ├── generated media implementation
    ├── host-system UI font
    ├── bundled synthetic seed
    └── writable scores.txt beside executable
```

Exact accepted artifact:

```text
SOURCE_SNAPSHOT = 0e1951c67f19b9eff24937ff1e1d228bfd72ff8b
SIZE_BYTES      = 11230689
SHA-256         = 170ED5502A1D2D955EFA3CB52D13B880830657FF456166E6610DD30AB7E430A6
```

The executable is not distributed under the current portfolio profile.

## 9. Test-to-Solution Map

Current test surfaces include navigation/application integration, storage, scoring, collisions, runtime session, resources, screens/services, procedural audio, public seed, UI fonts and packaging-hardening contracts.

Current accepted regression:

```text
125 PASS
```

Earlier 108/109 results are historical/superseded checkpoints.

## 10. Change Impact Map

| Change Area | Minimum Review Surface |
|---|---|
| application transitions | navigation contracts, handlers, audio transitions |
| gameplay rules | rules/session, score/collision tests, runtime gameplay |
| renderer/screens/fonts | GUI runtime + visual evidence when appearance changes |
| score format/path | storage, Scores, record flow, persistence |
| audio | audio tests + affected runtime behavior |
| `pyproject.toml` | install/import/runtime compatibility; optional packaging impact |
| frozen/resource path | source/frozen tests + packaged runtime if packaging affected |
| packaging configuration | source-level packaging contracts + fresh package QA when rebuilt |
| licensing/publication | NOTICE/LICENSE/scope/readiness cross-check |
| public docs/claims | documentation QA + evidence/readiness mapping |

## 11. Publication-Sensitive Elements

Accepted:

- source implementation;
- `125 PASS` automated regression;
- source GUI/audio runtime;
- source record flow/persistence;
- generated media/host-font strategy;
- synthetic seed;
- controlled packaging configuration;
- hardened package QA as internal evidence;
- MIT license;
- concise third-party notice.

Documentation state:

- cross-version quality-parity audit completed;
- targeted six-document remediation implemented;
- cross-document integration correction implemented;
- integration QA still required before the documentation gate can close.

Still open:

- QA/acceptance of the corrected documentation integration state;
- visual admission and filename normalization of four screenshots;
- creation of clean public repository;
- final clean-checkout install/tests/source smoke QA;
- final publication decision.

## Current Result

```text
SOURCE_SOLUTION_COMPLETE          = YES
SOURCE_AUTOMATED_QA               = 125 PASS
SOURCE_INTEGRATION                = PASS
PUBLIC_DATA_MEDIA_BOUNDARY        = PASS
MIT_LICENSE                       = PASS
THIRD_PARTY_NOTICE                = PASS
WINDOWS_PACKAGE                   = PASS / INTERNAL EVIDENCE
PUBLIC_BINARY_DISTRIBUTION        = N/A
DOCUMENTATION_QUALITY_PARITY      = REMEDIATION IMPLEMENTED
DOCUMENTATION_INTEGRATION         = CORRECTION IMPLEMENTED / QA REQUIRED
SCREENSHOT_ADMISSION              = BLOCKED UNTIL DOCUMENTATION GATE CLOSES
PUBLIC_REPOSITORY                 = NOT CREATED
RELEASE                           = OPEN
```
