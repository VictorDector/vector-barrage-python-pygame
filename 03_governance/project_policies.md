# Project Policies

Project: **Vector Barrage**  
Release target: `v1.1.0`  
Publication profile: **Source-First Portfolio Repository**  
Status: ACTIVE

## Purpose

Define product-level rules that protect source quality, reproducibility, data integrity, validation accuracy, repository hygiene and public-publication correctness.

## 1. Technical Naming and Language

- Non-user-facing technical elements use clear English terminology and standard Python naming conventions.
- Modules/files use `snake_case`; classes use `PascalCase`; functions/methods/variables use `snake_case`; constants use `UPPER_SNAKE_CASE` where appropriate.
- Spanish is intentionally permitted in user-visible interface text.
- The legacy filename `puntajes.txt` is permitted only inside the explicit compatibility boundary.
- Naming changes must not silently alter component responsibility or accepted behavior.

## 2. Canonical Package Metadata

- `pyproject.toml` is the canonical runtime/dependency/build metadata source.
- Supported Python range: `>=3.13,<3.14`.
- Runtime dependency: `pygame==2.6.1`.
- pytest and PyInstaller are development/packaging dependencies, not normal end-user source requirements beyond their respective workflows.
- Additional dependency manifests require a concrete reproducibility benefit and must not conflict with `pyproject.toml`.

## 3. Repository Hygiene

Version in the public repository:

- Vector Barrage source;
- tests;
- product-engineering documentation;
- `pyproject.toml`;
- MIT `LICENSE`;
- concise `NOTICE.md`;
- approved synthetic `scores.txt` seed;
- admitted public evidence;
- controlled packaging configuration under `packaging/`.

Exclude from the public repository:

- virtual environments;
- Python/pytest/tool caches;
- host-specific IDE state;
- secrets/credentials/tokens;
- disposable QA output;
- generated PyInstaller `build/` and `dist/` output;
- package-validation records classified as internal-only;
- historical/private source, screenshots, executables or unrelated Git history.

The current profile does not publish or attach a generated Windows executable.

## 4. Event and Application Lifecycle Integrity

- The application coordinator owns application-state transitions.
- Each active screen or game session owns event retrieval only while active.
- Lower-level gameplay rules/models must not independently drain the Pygame event queue.
- Screens must not recursively launch another screen or the application coordinator.
- Navigation changes require affected-scope automated and runtime regression.

## 5. Score-Data Integrity

- `scores.txt` is canonical.
- `storage.py` is authoritative for parsing, ordering, migration, precedence and append behavior.
- Existing canonical data must not be overwritten by legacy data or seed initialization.
- Legacy `puntajes.txt` may be migrated only when canonical data is absent.
- If migration cannot be written, legacy data remains preserved/readable.
- Write-path tests use temporary/isolated files.
- The versioned public seed remains synthetic.
- Final public-tree preparation verifies the five-record seed rather than using repository data as disposable QA state.

## 6. Runtime Resource and Persistence Separation

- Read-only source/frozen resources and writable score data are separate concerns.
- Runtime behavior must not depend on user-specific absolute paths.
- Frozen execution stores durable scores beside the executable rather than only inside temporary extraction state.
- Source execution resolves its stable project/runtime root deterministically.

## 7. Public Media Integrity

- Visual presentation is generated from Pygame primitives and host-system font rendering.
- Audio presentation is synthesized from source-defined numeric tone patterns.
- No historical/copy-based gameplay artwork, music or sound-effect files are required.
- New third-party media requires provenance/license disposition before public use.
- Media changes affecting appearance/audio require fresh affected evidence.

## 8. Validation Accuracy

Validation claims are scope-specific:

```text
COMPILE
IMPORT
BEHAVIOR
GUI_AUDIO
INTEGRATION
PACKAGED_RUNTIME
PUBLICATION
```

Policies:

- compile success is not behavioral success;
- automated tests do not replace GUI/audio observation;
- source runtime PASS does not establish packaged-runtime PASS;
- a successful build does not establish packaged-runtime PASS;
- packaging evidence does not imply public binary distribution;
- a working product does not automatically establish publication readiness;
- PASS claims must identify matching evidence and scope.

## 9. Evidence Integrity

- Public evidence must come from the exact Vector Barrage candidate it claims to validate.
- Historical screenshots/executables from another implementation cannot be renamed into current evidence.
- Screenshots support observable visual claims, not hidden logic/persistence claims.
- Screenshot files require visual admission before public claim use.
- Persistence/relaunch evidence requires complete process termination between runs when that is part of the claim.
- Hardened Windows package evidence remains valid as internal engineering evidence but must not imply an executable download exists.

## 10. Documentation Accuracy

- Documentation describes the as-built public candidate and approved source-first publication profile.
- README is an entry/index layer, not a substitute for the engineering dossier.
- Context, architecture, governance, solution, implementation and readiness documents must remain mutually coherent.
- Paths/commands shown to users must match the package structure.
- States such as `PENDING`, `PASS`, `CANDIDATE`, `N/A`, `SUPERSEDED` and `INTERNAL EVIDENCE` must not be silently upgraded.
- Public documentation must not expose unrelated private project-management/framework mechanics.

## 11. Change Integrity

Changes affecting these areas require affected-scope validation:

- application state/navigation;
- gameplay rules;
- score persistence/data format;
- source/package dependencies;
- runtime resources/media;
- public interface/controls;
- packaging configuration;
- licensing/publication scope;
- documentation or evidence claims.

Tests/documentation should change within the same candidate scope when behavior or claims change.

## 12. Packaging Policy

PyInstaller packaging is retained as an optional local engineering workflow and reproducibility surface.

- `packaging/VectorBarrage.spec` is the controlled specification.
- The launcher and Pygame hook remain source-tracked.
- The hardened Windows package has already passed build/archive/runtime/first-run/persistence QA and is preserved internally.
- Generated `build/` and `dist/` output is not public source content.
- `VectorBarrage.exe` is not published under the current portfolio profile.
- Public executable distribution, if proposed later, reopens binary-specific compliance and release QA.

## 13. Licensing / Publication Policy

- Vector Barrage-owned material is released under the repository MIT `LICENSE`.
- `NOTICE.md` records authorship/provenance and third-party boundaries but does not relicense third-party software.
- Python, Pygame and development/build dependencies retain their own licenses.
- No bundled executable or bundled third-party runtime is publicly distributed under the current profile.
- Full binary redistribution compliance is `OPTIONAL FUTURE` and becomes mandatory only if public executable distribution is reactivated.
- Current publication gates are documentation/tree reconciliation, screenshot admission, clean public-tree assembly and clean-checkout/source QA.

## Current Policy Result

```text
SOURCE_QUALITY_POLICY          = ACTIVE
DATA_INTEGRITY_POLICY          = ACTIVE
MEDIA_BOUNDARY_POLICY          = ACTIVE
VALIDATION_POLICY              = ACTIVE
MIT_LICENSE                    = PASS / ACCEPTED
THIRD_PARTY_NOTICE             = PASS / ACCEPTED
PUBLIC_BINARY_DISTRIBUTION     = N/A
DOCUMENTATION_DEPTH            = PRESERVE_OR_IMPROVE
SCREENSHOT_ADMISSION           = PENDING
PUBLIC_RELEASE                 = GATED
```
