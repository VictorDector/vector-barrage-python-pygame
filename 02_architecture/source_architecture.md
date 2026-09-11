# Source Architecture

Project: **Vector Barrage**  
Release target: `v1.1.0`  
Publication profile: **Source-First Portfolio Repository**  
Status: AS-BUILT / RECONCILED

## Purpose

Document the physical package layout, dependency direction, source ownership, test architecture, implementation-independence boundary and build/runtime boundaries of the current public candidate.

## Repository Structure

```text
vector-barrage-python-pygame/
├── README.md
├── LICENSE
├── NOTICE.md
├── .gitignore
├── pyproject.toml
├── scores.txt
├── 00_control/
├── 01_context/
├── 02_architecture/
├── 03_governance/
├── 04_solution/
├── 05_implementation/
├── 06_readiness/
├── evidence/
├── packaging/
│   ├── VectorBarrage.spec
│   ├── vector_barrage_launcher.py
│   └── hooks/
│       └── hook-pygame.py
├── src/
│   └── vector_barrage/
│       ├── __init__.py
│       ├── __main__.py
│       ├── app.py
│       ├── config.py
│       ├── resources.py
│       ├── storage.py
│       ├── audio.py
│       ├── links.py
│       ├── ui_fonts.py
│       ├── gameplay/
│       │   ├── __init__.py
│       │   ├── model.py
│       │   ├── rules.py
│       │   ├── session.py
│       │   └── renderer.py
│       └── screens/
│           ├── __init__.py
│           ├── menu.py
│           ├── scores.py
│           ├── about.py
│           └── name_entry.py
└── tests/
    └── automated regression suite
```

Generated `build/`, `dist/`, virtual environments, caches and disposable QA artifacts are excluded from public source control.

## Package Metadata

`pyproject.toml` is canonical:

```text
Distribution name: vector-barrage
Package: vector_barrage
Version: 1.1.0a0
Python: >=3.13,<3.14
Runtime dependency: pygame==2.6.1
Development: pytest>=8,<9
Packaging: pyinstaller==6.22.2
Build backend: setuptools.build_meta
Build-system requirement: setuptools>=75
```

A duplicate `requirements.txt`/`environment.yml` is not required unless a later reproducibility need justifies it.

## Entry Point

```text
python -m vector_barrage
        -> vector_barrage.app.main()
```

`__main__.py` remains minimal and contains no gameplay/persistence/UI business logic.

The separate `packaging/vector_barrage_launcher.py` provides the controlled absolute-import bootstrap for PyInstaller.

## Application Boundary — `app.py`

Responsibilities include state coordination, screen/game orchestration, audio lifecycle, strict new-record decision, name-entry integration, exactly-one score append, source/frozen writable score location and first-run score initialization.

`app.py` is the composition root for complete UI/game lifecycles.

## Configuration — `config.py`

Owns product name, author, approved repository URL, dimensions, frame target and interface language.

## Storage — `storage.py`

Owns canonical/legacy filenames, parsing, malformed-record tolerance, descending ordering, Top 5, max score, canonical precedence, legacy migration/fallback, seed initialization and append safety. It has no Pygame dependency.

## Resources — `resources.py`

Owns read-only source/frozen resource location. Writable scores are intentionally separate.

## Audio — `audio.py`

Defines `ProceduralAudioService` for normal runtime and injectable `NullAudioService` for tests/explicit audio-disabled contexts. Procedural audio is generated from source-defined tone sequences.

## Host Font Boundary — `ui_fonts.py`

Resolves approved host-system font paths for UI rendering. This prevents individual screens/renderers from relying on Pygame's bundled default font asset.

## Links — `links.py`

Owns approved URL opening/platform bridging outside UI presentation.

## Gameplay Package

- `model.py` — state/geometry structures.
- `rules.py` — deterministic movement/collision/scoring/progression semantics.
- `session.py` — active Pygame gameplay runtime and event ownership.
- `renderer.py` — generated geometry, HUD and Game Over presentation.

## Screens Package

Each screen owns local presentation/input while active and returns a narrow result:

```text
menu.py        -> MenuChoice
scores.py      -> ScoresOutcome
about.py       -> AboutOutcome
name_entry.py  -> NameEntryResult
```

Screens do not invoke one another recursively.

## Dependency Rules

```text
__main__ -> app
app -> config/storage/resources/audio/gameplay.session/screens.*
gameplay.session -> model/rules/renderer
gameplay.rules -> model
gameplay.renderer -> model/config/ui_fonts
screens -> config/ui_fonts + narrow services
screens.about -> links
screens.scores -> storage
```

Prohibited:

- recursive screen/application launch;
- model/rules owning persistence;
- renderer owning storage;
- storage depending on Pygame GUI behavior;
- resources owning writable scores;
- private/historical modules imported by the public package;
- circular dependencies that blur the ownership boundaries above.

## Implementation-Independence Boundary

The public Vector Barrage package is an independent source implementation. Its runtime/import graph must remain self-contained within the public package and declared third-party dependencies.

Required independence rules:

```text
public source
-> may use current public design/specification records
-> may use Python/Pygame/tooling APIs
-> may preserve explicitly supported data compatibility such as puntajes.txt

public source
-> must not import private historical modules
-> must not require private repository paths
-> must not require historical image/audio assets
-> must not require private Git history
-> must not depend on hidden framework/project-management artifacts
```

Historical/private project material may explain provenance or earlier engineering decisions, but it must not be a runtime dependency or an undocumented implementation prerequisite of the public repository.

## Runtime Data

`scores.txt` is versioned as a synthetic public seed, not disposable test output.

- automated writes use temporary files;
- local users may generate scores normally;
- public-tree preparation verifies the five-record seed before publication;
- frozen builds may bundle the seed for initialization while durable scores remain beside the executable.

## Media Structure

No required `assets/` tree exists because current visuals/audio are generated from code. UI text uses host-system fonts.

Future external media requires provenance/license, repository path, resource-resolution logic, tests/build updates and documentation/evidence updates.

## Test Architecture

Testing is layered so deterministic behavior, integration behavior, graphical behavior and packaging behavior are not conflated.

### Domain / rule tests

Primary scope:

- movement and bounds;
- projectile behavior;
- collision consumption;
- score increments;
- life/progression transitions;
- strict new-record comparison.

These tests should remain independent of a visible GUI where practical.

### Storage / data tests

Primary scope:

- valid UTF-8/BOM-tolerant parsing;
- malformed-row tolerance;
- ordering and Top 5;
- maximum-score resolution;
- canonical `scores.txt` precedence;
- legacy `puntajes.txt` migration/fallback;
- seed initialization;
- append safety/exactly-once expectations;
- isolated temporary write paths.

### Screen / service tests

Primary scope:

- menu choices/outcomes;
- About/link behavior;
- score-screen behavior;
- name-entry validation;
- audio-service semantics/fail-soft behavior;
- host-font resolution contracts;
- resource-resolution contracts.

### Application integration tests

Primary scope:

- non-recursive application transitions;
- state/action mapping;
- Game Over to strict record decision;
- Name Entry to exactly-one persistence orchestration;
- screen/service coordination.

### Source runtime / E2E validation

Primary scope:

- real graphical startup;
- visible Main Menu/gameplay/HUD/Scores/About/Name Entry;
- navigation and audio behavior;
- source persistence/relaunch behavior.

These runtime observations complement automated tests; they are not inferred from pytest success alone.

### Packaging contract tests

Primary scope:

- controlled `VectorBarrage.spec` expectations;
- Pygame hook behavior;
- required/forbidden packaged resources;
- source/frozen resource and score-path contracts.

### Packaged runtime validation

Primary scope, when a package is built:

- native executable startup;
- generated visual/audio behavior;
- first-run seed initialization;
- durable score persistence beside the executable;
- complete process relaunch persistence.

Under the current source-first profile, packaged runtime evidence is internal engineering evidence rather than a publication prerequisite for a downloadable binary.

Current accepted automated result:

```text
AUTOMATED_REGRESSION = 125 PASS
```

Historical 108/109 results are superseded checkpoints.

## Build Boundary

PyInstaller is development/packaging tooling, not an end-user source runtime dependency. Controlled source-tracked packaging consists of:

```text
packaging/VectorBarrage.spec
packaging/vector_barrage_launcher.py
packaging/hooks/hook-pygame.py
```

The accepted hardened Windows package was built from source/configuration snapshot:

```text
0e1951c67f19b9eff24937ff1e1d228bfd72ff8b
```

and validated as:

```text
VectorBarrage.exe
11230689 bytes
SHA-256 170ED5502A1D2D955EFA3CB52D13B880830657FF456166E6610DD30AB7E430A6
```

That executable is preserved as **INTERNAL ENGINEERING EVIDENCE** and is not part of the public source-first distribution.

## Licensing Boundary

```text
LICENSE                 = MIT / Vector Barrage-owned material
NOTICE.md               = concise third-party boundary
Python/Pygame           = separately licensed / user-installed
public executable       = not distributed
binary compliance bundle= optional future
```

## Current Result

```text
PHYSICAL_SOURCE_ARCHITECTURE   = AS-BUILT / RECONCILED
PACKAGE_BOUNDARIES             = IMPLEMENTED
IMPLEMENTATION_INDEPENDENCE    = EXPLICIT / PASS BY DESIGN
TEST_ARCHITECTURE              = DEFINED
DEPENDENCY_METADATA            = CANONICAL IN pyproject.toml
SOURCE_TESTS                   = 125 PASS
SOURCE_RUNTIME                 = PASS
DOCUMENTATION_QUALITY_PARITY   = REMEDIATION IMPLEMENTED / QA REQUIRED
PACKAGING_CONFIGURATION        = PASS / SOURCE-TRACKED
WINDOWS_PACKAGE                = PASS / INTERNAL EVIDENCE
PUBLIC_EXECUTABLE_DOWNLOAD     = NO
```
