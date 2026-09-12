# Vector Barrage

A fixed-shooter arcade game built with **Python 3.13** and **Pygame 2.6.1**, designed as a source-first software-engineering portfolio project.

Vector Barrage demonstrates explicit application-state coordination, deterministic gameplay rules, local persistence, procedural visual and audio presentation, automated testing, reproducible source execution, controlled packaging engineering and traceable technical documentation.

> **Publication profile:** source code, tests, engineering documentation, controlled build configuration and approved evidence are public. A compiled `VectorBarrage.exe` is not distributed under the current release profile.

## Project Status

```text
Release target                 = v1.1.0
Package version                = 1.1.0
Public profile                 = SOURCE-FIRST PORTFOLIO

Source implementation          = PASS / ACCEPTED
Automated regression           = 125 PASS
Final public-tree QA           = PASS / ACCEPTED
Documentation reconciliation   = PASS / ACCEPTED

MIT license                    = PRESENT
Third-party notice             = PRESENT

Public repository              = PUBLISHED
Public executable download     = NO

Windows packaged QA            = PASS / INTERNAL ENGINEERING EVIDENCE

Screenshot admission           = ACCEPTED / OWNER DECISION
Independent screenshot QA      = NOT CLAIMED
EVD-VB-004                     = PRE-FIX REFERENCE / REPLACEMENT WAIVED

Public release ready           = YES
Release tag                    = PENDING
```

The source implementation, exact published source tree and documentation state satisfy the current source-first release-readiness boundary. The remaining release action is creation and verification of the `v1.1.0` tag.

## Features

- Spanish-language menu and user interface.
- Iterative, non-recursive application navigation.
- Horizontal player movement and projectile firing.
- Deterministic enemy progression and collision handling.
- Score, lives, level progression and Game Over flow.
- Strict new-record handling and exactly-once score persistence.
- UTF-8 score parsing with malformed-record tolerance.
- Descending Top-5 score presentation.
- Canonical `scores.txt` storage with legacy `puntajes.txt` migration/fallback behavior.
- Procedural visual presentation using Pygame primitives.
- Procedural PCM audio generated at runtime.
- Host-system font resolution without a bundled gameplay font asset.
- Automated regression across gameplay, storage, navigation, screens, services, fonts and packaging contracts.
- Controlled PyInstaller packaging configuration preserved as reproducible engineering evidence.

## Technology Stack

| Surface | Technology |
|---|---|
| Language | Python 3.13 |
| Game/runtime library | Pygame 2.6.1 |
| Testing | pytest |
| Packaging engineering | PyInstaller 6.22.2 |
| Package/build metadata | `pyproject.toml` |
| Version control | Git / GitHub |

The canonical dependency and package metadata is defined in `pyproject.toml`.

## Getting Started

### Prerequisites

For normal source execution:

- Python `>=3.13,<3.14`
- Git
- a graphical desktop environment supported by Pygame

Pygame `2.6.1` is installed through the project dependency declaration.

### Installation

Clone the repository:

```bash
git clone https://github.com/VictorDector/vector-barrage-python-pygame.git
cd vector-barrage-python-pygame
```

Create a virtual environment.

Linux / WSL / macOS:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the application:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

For development and automated tests:

```bash
python -m pip install -e ".[dev]"
```

### Run

Start Vector Barrage:

```bash
python -m vector_barrage
```

For the validated WSL2/X11 reproduction profile and display troubleshooting, see `05_implementation/execution_runbook.md`.

## Controls

| Context | Control | Action |
|---|---|---|
| Menu | Arrow keys | Change selection |
| Menu | Enter | Open selected option |
| Game | Left / Right | Move player |
| Game | Space | Fire |
| Game Over | Enter | Continue to record flow when applicable |
| Name entry | Keyboard | Enter player name |
| Name entry | Enter | Save a valid name |
| Name entry | Esc | Cancel |
| Secondary screens | Esc / configured return action | Return to main menu |

## Validation

Vector Barrage is validated through separate automated, runtime, integration, persistence and packaging evidence surfaces. A PASS in one surface is not treated as evidence for another.

### Automated Tests

Run:

```bash
python -m pytest
```

Current accepted baseline:

```text
125 passed
```

Coverage includes gameplay rules, score persistence, navigation, screen/service behavior, generated media boundaries, host-system font resolution and controlled packaging contracts.

### Runtime and Integration Validation

Accepted source validation includes:

- package installation and import;
- application startup;
- Main Menu navigation;
- gameplay entry and return;
- Scores and About navigation;
- player movement and firing;
- HUD rendering;
- procedural audio behavior;
- score persistence;
- complete process relaunch persistence;
- exact public-tree clean-checkout validation.

A hardened Windows package was also built and exercised successfully, but that package is retained as **internal engineering evidence** rather than a downloadable public release artifact.

## Architecture

Vector Barrage is a single-process, event-driven desktop application organized as an installable Python package.

```text
python -m vector_barrage
        |
        v
Application Coordinator
        |
        +---------+----------+---------+
        |         |          |         |
        v         v          v         v
      Menu    Gameplay     Scores    About
                  |          |         |
          +-------+------+   v         v
          |       |      | Storage    Links
          v       v      v
        Model   Rules  Renderer
                        |
                        v
                 Host Font Resolver
```

Key boundaries:

- `app.py` owns application-state coordination.
- `gameplay/model.py` represents gameplay state.
- `gameplay/rules.py` owns deterministic gameplay rules.
- `gameplay/session.py` owns the active Pygame gameplay loop.
- `gameplay/renderer.py` owns gameplay rendering.
- `storage.py` owns canonical score parsing, migration and persistence.
- `audio.py` owns procedural sound generation and audio lifecycle.
- `ui_fonts.py` resolves approved host-system fonts.
- `screens/` owns individual interface screens.
- `resources.py` separates read-only resources from writable runtime persistence.

Detailed architecture is documented under `02_architecture/` and `04_solution/`.

## Repository Structure

```text
.
├── README.md
├── LICENSE
├── NOTICE.md
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
├── src/
└── tests/
```

The numbered directories form the engineering dossier:

```text
00_control        project identity, state and change history
01_context        context, behavior, requirements and references
02_architecture   as-built architecture and material decisions
03_governance     product and validation policies
04_solution       capability and implementation mapping
05_implementation execution and packaging runbooks
06_readiness      acceptance, publication scope and release readiness
```

## Data and Persistence

The public repository contains a synthetic demonstration seed:

```text
PLAYER_01,500
PLAYER_02,350
PLAYER_03,250
PLAYER_04,150
PLAYER_05,100
```

`scores.txt` is the canonical score file.

Persistence rules include:

- UTF-8-compatible score parsing;
- malformed-record tolerance;
- descending score ordering;
- strict new-record comparison;
- exactly-once accepted score writes;
- preservation of existing canonical data;
- migration/fallback support for legacy `puntajes.txt` only when canonical data is absent.

Tests and validation workflows use isolated runtime locations rather than consuming the versioned public seed as disposable test data.

## Packaging and Distribution

The repository includes controlled PyInstaller engineering files under `packaging/`.

A hardened Windows executable was built and validated for:

- native build completion;
- archive hardening;
- startup and application runtime;
- first-run score initialization;
- persistence after complete process relaunch.

This demonstrates packaging capability.

The current distribution policy remains:

```text
PUBLIC SOURCE REPOSITORY   = YES
CONTROLLED BUILD CONFIG    = YES
LOCAL WINDOWS BUILD        = SUPPORTED
PUBLIC EXE DOWNLOAD        = NO
GITHUB RELEASE BINARY      = NO
```

The compiled executable is therefore not committed to the repository and is not offered as a GitHub Release binary under the current source-first profile.

See `05_implementation/packaging_runbook.md` for the controlled build procedure.

## Evidence

The public evidence set includes four canonical application screenshots plus source-runtime and source-persistence validation records.

`EVD-VB-001`, `EVD-VB-002` and `EVD-VB-003` remain current visual references for their respective surfaces.

`EVD-VB-004_about.png` is intentionally preserved as the accepted **pre-fix About reference**. The About layout was subsequently corrected and verified by the release owner; replacement of the screenshot was explicitly waived. The preserved file must therefore not be represented as an exact image of the final About layout.

Direct independent visual QA of the screenshot set was waived by the release owner and is **not** represented as a visual-QA PASS.

See `evidence/README.md` for the evidence/claim boundary.

## License and Third-Party Software

Vector Barrage-owned material is released under the **MIT License**. See `LICENSE`.

Python, Pygame, pytest, PyInstaller and other third-party tooling retain their own licenses and are not relicensed by the Vector Barrage MIT license.

See `NOTICE.md` and `pyproject.toml` for the applicable dependency and third-party boundary.

## Author

**Victor David Dector Ramirez**

Repository: `VictorDector/vector-barrage-python-pygame`
