# Packaging Runbook

Project: **Vector Barrage**  
Release target: `v1.1.0`  
Publication profile: **Source-First Portfolio Repository**  
Packaging role: **OPTIONAL LOCAL ENGINEERING WORKFLOW / INTERNAL EVIDENCE**

## Purpose

Document the controlled PyInstaller build path used to produce and validate the hardened Windows package while making clear that a compiled executable is not distributed by the current public portfolio profile.

## Publication Boundary

```text
PUBLIC SOURCE REPOSITORY  = YES
CONTROLLED BUILD CONFIG   = YES
LOCAL WINDOWS BUILD       = SUPPORTED
PUBLIC EXE DOWNLOAD       = NO
GITHUB RELEASE BINARY     = NO
```

The packaging configuration is public engineering evidence. The generated executable is not a public repository or release asset.

## Controlled Packaging Files

```text
packaging/
├── VectorBarrage.spec
├── vector_barrage_launcher.py
└── hooks/
    └── hook-pygame.py
```

`VectorBarrage.spec` is the canonical build configuration. Do not replace it with an ad-hoc one-line PyInstaller command when reproducing the hardened build.

## Build Environment

Validated hardened build environment used:

```text
Windows 11 x64
Python 3.13.15
Pygame 2.6.1
PyInstaller 6.22.2
```

Create a dedicated build environment in the project root:

```powershell
py -3.13 -m venv .venv-build
.\.venv-build\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Confirm:

```powershell
python --version
python -c "import importlib.metadata; print(importlib.metadata.version('pygame'))"
python -m PyInstaller --version
```

## Controlled Build Command

From the repository root in Windows PowerShell:

```powershell
.\.venv-build\Scripts\python.exe -m PyInstaller `
  --clean `
  --noconfirm `
  .\packaging\VectorBarrage.spec
```

Expected output artifact:

```text
dist\VectorBarrage.exe
```

## Hardened Configuration Intent

The controlled spec/hook combination was designed to:

- use `packaging/vector_barrage_launcher.py` as the entry bootstrap;
- resolve the package from `src/`;
- bundle the synthetic `scores.txt` seed as read-only first-run input;
- use the project Pygame hook to collect required native runtime libraries without copying unnecessary Pygame data assets;
- exclude Pygame default font/icon assets from the final archive where not required;
- exclude bundled `VCRUNTIME140.dll` and `VCRUNTIME140_1.dll` so the compatible Microsoft Visual C++ runtime remains an external host prerequisite;
- produce a one-file, windowed executable named `VectorBarrage`.

## Accepted Hardened Artifact

The completed internal build is tied to this source/configuration snapshot:

```text
SOURCE_SNAPSHOT = 0e1951c67f19b9eff24937ff1e1d228bfd72ff8b
```

Artifact identity:

```text
EXE_NAME        = VectorBarrage.exe
EXE_SIZE_BYTES  = 11230689
EXE_SHA256      = 170ED5502A1D2D955EFA3CB52D13B880830657FF456166E6610DD30AB7E430A6
```

This supersedes the earlier first-package hash as the accepted hardened packaging evidence.

## Hardened Package QA Result

```text
NATIVE_WINDOWS_BUILD         = PASS
ARCHIVE_BLOCKER_ASSERTIONS   = PASS
REQUIRED_RUNTIME_ASSERTIONS  = PASS
PACKAGED_RUNTIME_QA          = PASS
FIRST_RUN_SCORE_INIT         = PASS
PERSISTENCE_RELAUNCH         = PASS
TECHNICAL_PACKAGE_QA         = PASS / COMPLETE
```

Validated Route-A exclusions:

```text
pygame/freesansbold.ttf  = ABSENT
pygame/pygame_icon.bmp   = ABSENT
VCRUNTIME140.dll         = ABSENT
VCRUNTIME140_1.dll       = ABSENT
```

The final filtered archive inventory contained 57 entries plus five Windows host/system dependencies reported externally. That binary-specific inventory is preserved as internal engineering/compliance evidence.

## Runtime Storage Behavior in Frozen Mode

When frozen, writable `scores.txt` is created/read beside the executable rather than inside PyInstaller's temporary extraction location. The bundled synthetic seed is a read-only initialization resource.

Expected first-run behavior:

```text
no canonical scores.txt beside executable
-> launch
-> bundled synthetic seed copied beside executable
-> runtime reads/writes external canonical scores.txt
```

This behavior has been validated on the accepted hardened artifact.

## Host-System Font Requirement

The project UI uses approved host-system fonts. The packaged application must not depend on a copied project font asset to render its UI. The Windows preflight and packaged runtime validation confirmed the system-font path for the accepted hardened build.

## Microsoft Runtime Boundary

The accepted hardened archive does not bundle `VCRUNTIME140.dll` or `VCRUNTIME140_1.dll`. A compatible Microsoft Visual C++ v14 x64 runtime is therefore treated as a host prerequisite for the internal Windows package workflow.

## Public Distribution Rule

The current portfolio profile intentionally stops before binary distribution:

```text
HARDENED_PACKAGE           = PASS / INTERNAL EVIDENCE
PUBLIC_BINARY_DISTRIBUTION = N/A
FULL_BINARY_COMPLIANCE     = OPTIONAL FUTURE
```

If a public executable download is proposed later:

1. reopen the binary component/license compliance gate;
2. validate the exact intended release artifact and hash;
3. provide the required third-party notices/licenses/source-access path for that binary;
4. run final release-specific package QA;
5. only then authorize public binary distribution.

## Generated Files

Do not commit generated output:

```text
build/
dist/
```

The controlled source-tracked spec remains under `packaging/`.
