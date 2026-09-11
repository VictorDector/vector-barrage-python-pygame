# Execution Runbook

Project: **Vector Barrage**  
Release target: `v1.1.0`  
Publication profile: **Source-First Portfolio Repository**

## Purpose

Provide a reproducible source-execution, test and troubleshooting procedure for developers and reviewers of the public Vector Barrage repository.

The primary public execution path is Python/Pygame from source. A compiled Windows executable is not distributed under the current portfolio profile.

## Runtime Requirements

```text
Python >=3.13,<3.14
pygame==2.6.1
```

Development tooling is declared under the `dev` optional dependency group in `pyproject.toml`.

## Execution Profile Summary

| Profile | Role | Host | Primary command | Status |
|---|---|---|---|---|
| `SOURCE_STANDARD` | Preferred public source workflow | Linux / WSL / macOS / Windows | `python -m vector_barrage` | SUPPORTED |
| `SOURCE_WSL2_X11` | Reproducible validated WSL/X11 diagnostic profile | Windows + WSL2 / Ubuntu | explicit `DISPLAY` + `SDL_VIDEODRIVER=x11` | VALIDATED |
| `WINDOWS_PACKAGED_HARDENED` | Optional packaging engineering profile | Windows 11 x64 | packaged `VectorBarrage.exe` | VALIDATED / INTERNAL EVIDENCE |

The standard source workflow is the public default. The explicit WSL2/X11 route is retained because it reproduces a validated graphical source environment when normal WSLg/display integration is unavailable or unreliable.

## Source Setup — Linux / WSL / macOS

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Run:

```bash
python -m vector_barrage
```

Run tests:

```bash
python -m pytest
```

Current accepted automated baseline:

```text
125 passed
```

No timing is asserted for this baseline unless a specific execution record provides one.

## Source Setup — Windows PowerShell

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m vector_barrage
```

Tests:

```powershell
python -m pytest
```

## Validated WSL2 / X11 Source Profile

This profile is not mandatory for every WSL user. Use it when an explicit external X11 path is required or when reproducing the validated WSL2/X11 environment.

### Host prerequisites

- Windows with WSL2 / Ubuntu;
- Python 3.13 virtual environment inside WSL;
- project installed with `python -m pip install -e ".[dev]"`;
- an X11 server on Windows such as XLaunch or VcXsrv when the normal WSL graphical route is not being used.

Keep the X server limited to the local/trusted machine context. Do not expose an X server to untrusted networks merely to run the project.

### Resolve the Windows host from WSL2

```bash
WIN_HOST=$(ip route show default | awk '{print $3; exit}')
echo "$WIN_HOST"
```

### Launch through the validated X11 path

With the project virtual environment active:

```bash
DISPLAY="${WIN_HOST}:0.0" \
SDL_VIDEODRIVER=x11 \
python -m vector_barrage
```

If the environment is not activated, invoke the project interpreter explicitly, for example:

```bash
DISPLAY="${WIN_HOST}:0.0" \
SDL_VIDEODRIVER=x11 \
.venv/bin/python -m vector_barrage
```

Expected profile boundary:

```text
Windows host
├── XLaunch / VcXsrv (when external X11 is used)
└── WSL2 / Ubuntu
    └── Python 3.13 + Pygame 2.6.1
        └── Vector Barrage source package
```

XLaunch/VcXsrv is an environment aid for this source route. It is not a Python dependency, game-architecture dependency or requirement of the Windows packaged profile.

## Expected Application Flow

```text
Main Menu
├── Juego
│   ├── gameplay
│   ├── Game Over
│   └── New Record / name entry when applicable
├── Puntuaciones
├── Acerca de
└── Salir
```

Navigation is coordinated iteratively rather than by recursively nesting screens.

## Runtime Checks

For a manual source smoke test, verify:

- application window is visible;
- Spanish menu text renders correctly;
- no missing-glyph/font error occurs;
- Game starts;
- player movement works;
- player fire works;
- enemies progress;
- score/lives/level HUD is visible;
- procedural audio is audible where expected;
- Scores opens and returns;
- About opens and returns;
- application exits cleanly.

Persistence validation should always use a temporary/disposable score directory or test fixture rather than modifying the repository seed.

## Score File Behavior

Canonical filename:

```text
scores.txt
```

Repository seed:

```text
PLAYER_01,500
PLAYER_02,350
PLAYER_03,250
PLAYER_04,150
PLAYER_05,100
```

Storage behavior includes:

- UTF-8-compatible parsing;
- malformed-record tolerance;
- descending score ordering;
- strict new-record comparison;
- canonical score-file initialization;
- legacy `puntajes.txt` migration/fallback behavior where applicable;
- exactly-once accepted score write.

Do not use the repository seed itself as mutable QA data.

## Font Boundary

UI font rendering uses `src/vector_barrage/ui_fonts.py` to resolve an approved host-system font. The project does not rely on Pygame's bundled default `freesansbold.ttf` as its public UI asset.

If font resolution fails, validate that an approved system font is installed and accessible rather than adding a copied font binary to the repository.

## Audio Boundary

Audio is synthesized at runtime from source-defined numeric tone patterns. There is no required external sound-effect/music directory for the public candidate.

For environments without usable audio devices, automated tests should exercise injectable/no-op audio boundaries rather than requiring physical audio hardware.

## Automated Validation

Run complete suite:

```bash
python -m pytest
```

Current accepted baseline:

```text
AUTOMATED_REGRESSION = 125 PASS
```

The suite includes gameplay, storage, navigation, screen/service behavior, UI-font controls and packaging-hardening contracts.

Earlier 108/109-test snapshots remain historical checkpoints and are superseded by the current 125-test baseline.

## Optional Packaging Engineering Path

The repository retains controlled PyInstaller files under `packaging/`. Building a local executable is an optional engineering workflow, not a public-release requirement.

Use `05_implementation/packaging_runbook.md` for the controlled build procedure.

Current portfolio rule:

```text
LOCAL_PACKAGE_BUILD        = SUPPORTED / ENGINEERING WORKFLOW
PUBLIC_EXE_DOWNLOAD        = NO
GITHUB_RELEASE_BINARY      = NO
```

## Troubleshooting

### Import errors

Confirm the virtual environment is active and install the project in editable mode:

```bash
python -m pip install -e ".[dev]"
```

### Pygame import/version

```bash
python -c "import pygame; print(pygame.version.ver)"
```

Expected project dependency:

```text
2.6.1
```

### Display problems under WSL

Treat host display/graphics integration separately from gameplay/application logic.

First inspect the normal WSL graphical environment:

```bash
echo "$DISPLAY"
echo "$WAYLAND_DISPLAY"
```

If the process starts but the window is not usable and an external X11 route is appropriate, recompute the Windows host and use the validated explicit path:

```bash
WIN_HOST=$(ip route show default | awk '{print $3; exit}')

DISPLAY="${WIN_HOST}:0.0" \
SDL_VIDEODRIVER=x11 \
python -m vector_barrage
```

If an X server is required, verify XLaunch/VcXsrv is running before modifying source code. A host WSLg/X11/graphics failure must not be misclassified as a gameplay defect without application-level evidence.

### Window opens as a process/taskbar item but is not visible

This symptom may indicate host graphical integration rather than an application logic failure. Verify:

- `DISPLAY` / `WAYLAND_DISPLAY` state;
- whether the selected graphical bridge is actually running;
- SDL video driver selection;
- host/WSL graphics health.

Use the explicit `SOURCE_WSL2_X11` route as a reproducible fallback when appropriate.

### Score data changed during testing

Restore the five-record synthetic seed and move the test to a disposable temporary location. Tests and manual QA should not consume real/public seed state.

### Font resolution failure

Confirm an approved host-system font is installed and accessible. Do not solve the issue by committing an arbitrary copied font binary without first changing the media/provenance boundary.

### Audio device unavailable

A missing/unusable mixer device should be treated as an environment/audio-output issue when application logic continues through the fail-soft audio boundary. Automated tests may use `NullAudioService` or other controlled injection appropriate to the tested scope.

## Public Claim Boundary

Permitted current engineering claims include:

- source implementation accepted;
- current automated regression baseline is 125 PASS;
- application runtime/persistence behavior has been validated;
- a reproducible WSL2/X11 source profile is documented;
- a hardened Windows package was built and validated internally;
- no public executable is distributed under the current profile.

Do not claim screenshot evidence is accepted until visual admission closes, and do not imply an executable download exists.
