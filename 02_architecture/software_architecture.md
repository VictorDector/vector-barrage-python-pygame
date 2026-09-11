# Software Architecture

Project: **Vector Barrage**  
Release target: `v1.1.0`  
Publication profile: **Source-First Portfolio Repository**  
Status: AS-BUILT / VALIDATED

## Purpose

Describe the logical architecture, component responsibilities, runtime ownership, persistence boundaries and execution profiles of the current Vector Barrage implementation.

## Architectural Style

Vector Barrage is a single-process, event-driven desktop application built with Python and Pygame. It separates:

- application coordination;
- deterministic gameplay model/rules;
- active Pygame session;
- rendering;
- screen presentation;
- score persistence;
- procedural audio lifecycle;
- host-system font resolution;
- resource resolution;
- external-link handling.

The design favors explicit ownership boundaries over a large framework or deeply coupled hierarchy.

## Logical Architecture

```text
python -m vector_barrage
        |
        v
Application Entry Point
        |
        v
VectorBarrageApplication
        |
        +--------------------+--------------------+--------------------+
        |                    |                    |                    |
        v                    v                    v                    v
    Main Menu           Game Session          Scores              About
                             |                    |                    |
               +-------------+-------------+      v                    v
               |             |             |   Score Storage          Links
               v             v             v
          Gameplay Model   Rules        Renderer
                                         |
                                         v
                                   Host Font Resolver

Game Session -> Game Result -> Application Coordinator
                              -> strict record decision
                              -> Name Entry
                              -> Score Storage

Shared services:
- configuration
- procedural audio
- read-only resource resolution
```

## Application Coordination

`src/vector_barrage/app.py` owns application lifecycle and iterative state dispatch.

```text
MENU -> GAME   -> MENU
MENU -> SCORES -> MENU
MENU -> ABOUT  -> MENU
MENU -> EXIT
```

Screens/gameplay return outcomes rather than invoking another complete application lifecycle.

## Gameplay Architecture

### Model — `gameplay/model.py`

Defines runtime state for player, enemies, projectiles and game state without menu/filesystem responsibility.

### Rules — `gameplay/rules.py`

Owns deterministic movement, collision, scoring, life-loss, progression and strict new-record semantics. It is independently testable where practical.

### Session — `gameplay/session.py`

Owns the active gameplay loop, event retrieval, input interpretation, state advancement, rules invocation, rendering integration and semantic enemy-destruction events. Returns a `GameSessionResult` rather than persisting identity itself.

### Renderer — `gameplay/renderer.py`

Owns generated visual presentation: background, player/enemy/projectile geometry, HUD and Game Over. It has no persistence/navigation ownership.

### Host Font Resolver — `ui_fonts.py`

Resolves an approved host-system font for UI rendering. This isolates font selection from individual screens/renderers and avoids reliance on a copied/bundled project font asset. Resolution fails explicitly when no approved font can be found.

## Screen Architecture

All screens live under `src/vector_barrage/screens/`:

- `menu.py` -> primary navigation;
- `scores.py` -> ordered Top 5 presentation;
- `about.py` -> product/author/technology and approved link;
- `name_entry.py` -> normalized valid record name.

Each active screen owns only its local loop/input and returns a narrow result to `app.py`.

## Persistence Architecture

`storage.py` is the authoritative score-data boundary.

```text
Source execution
└── project/runtime root
    ├── scores.txt      -> canonical writable data
    └── puntajes.txt    -> optional legacy input if canonical absent

Frozen/local package execution
└── executable directory
    ├── scores.txt      -> canonical writable persistent data
    └── puntajes.txt    -> optional legacy input

Read-only packaged resources
└── bundled scores.txt  -> first-run seed only
```

Precedence:

```text
canonical exists -> canonical
canonical absent + legacy exists -> migrate/copy when possible
migration write unavailable -> read preserved legacy
no runtime data + seed available -> initialize canonical from seed
```

## New-Record Integration

```text
GameSessionResult
    |
    +-- not completed -> MENU / EXIT
    |
    +-- completed
            |
            v
     final_score > stored_max ?
            |
        no  +-----------> MENU
            |
           yes
            v
      new-record cue
            v
        Name Entry
            v
      append_score() once
            v
           MENU
```

## Audio Architecture

`audio.py` defines semantic audio behavior. Normal runtime uses `ProceduralAudioService`; tests/explicitly disabled contexts may inject `NullAudioService`.

The procedural service synthesizes signed 16-bit PCM from numeric tone segments and does not read gameplay audio files. Device failures fail soft.

## Visual / Media Architecture

```text
Visual output
-> Pygame primitives
-> host-system font resolved by ui_fonts.py

Audio output
-> numeric tone patterns
-> synthesized PCM
-> Pygame mixer playback
```

No external gameplay image/audio asset tree is required.

## Resource Architecture

`resources.py` separates read-only source/frozen resources from writable score ownership. In frozen mode it can resolve PyInstaller extraction resources; `app.py` separately resolves writable score storage.

## External Link Architecture

`links.py` encapsulates approved URL/platform handling so About remains presentation-oriented.

## Event Ownership

```text
Active Main Menu     -> menu event retrieval
Active Scores        -> scores event retrieval
Active About         -> about event retrieval
Active Name Entry    -> name-entry event retrieval
Active Game Session  -> gameplay event retrieval once/frame
```

Lower-level rules/models do not drain the event queue.

## Dependency Direction

```text
__main__ -> app
app -> config/storage/audio/resources/gameplay.session/screens.*
gameplay.session -> model/rules/renderer
gameplay.renderer -> model/config/ui_fonts
gameplay.rules -> model
screens.* -> config/ui_fonts and narrow services as required
screens.about -> links
screens.scores -> storage
```

Prohibited patterns include recursive screen/application lifecycle calls, rules owning filesystem persistence, renderer owning storage, model draining Pygame events and resource resolver owning writable persistence.

## Execution Profiles

### `SOURCE_WSL2_X11` — VALIDATED

```text
Windows host
└── WSL2 / Ubuntu
    └── Python 3.13.x + Pygame 2.6.1
        └── documented X11/WSLg-capable graphical path
            └── python -m vector_barrage
```

### `WINDOWS_PACKAGED_HARDENED` — VALIDATED / INTERNAL EVIDENCE

```text
Windows
└── VectorBarrage.exe
    ├── packaged Python/Pygame runtime
    ├── generated visual/audio implementation
    ├── host-system UI font
    ├── bundled synthetic first-run seed
    └── writable scores.txt beside executable
```

Accepted artifact:

```text
SOURCE_SNAPSHOT = 0e1951c67f19b9eff24937ff1e1d228bfd72ff8b
SIZE_BYTES      = 11230689
SHA-256         = 170ED5502A1D2D955EFA3CB52D13B880830657FF456166E6610DD30AB7E430A6
PACKAGE_QA      = PASS / COMPLETE
```

This profile is preserved as engineering evidence; the executable is not publicly distributed under the current source-first publication profile.

## Quality Attributes

The architecture supports testability, maintainability, reliability, reproducibility, portability, provenance hygiene and traceability through explicit boundaries and documentation.

## Current Architecture Result

```text
APPLICATION_COORDINATION     = IMPLEMENTED / PASS
GAMEPLAY_DOMAIN              = IMPLEMENTED / PASS
SCREEN_BOUNDARIES            = IMPLEMENTED / PASS
STORAGE_BOUNDARY             = IMPLEMENTED / PASS
HOST_FONT_BOUNDARY           = IMPLEMENTED / PASS
PROCEDURAL_MEDIA             = IMPLEMENTED / PASS
SOURCE_RUNTIME               = PASS
AUTOMATED_REGRESSION         = 125 PASS
WINDOWS_PACKAGED_RUNTIME     = PASS / INTERNAL EVIDENCE
PUBLIC_EXECUTABLE_DOWNLOAD   = NO
```
