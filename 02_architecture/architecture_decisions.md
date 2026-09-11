# Architecture Decisions

Project: **Vector Barrage**  
Release target: `v1.1.0`  
Publication profile: **Source-First Portfolio Repository**  
Status: ACTIVE

## Purpose

Record decisions that materially shape the current Vector Barrage source, runtime, persistence, media, packaging and publication architecture.

## Decision Register

| ID | Decision | Status | Rationale |
|---|---|---|---|
| `AD-001` | Use Python 3.13.x and Pygame 2.6.1 as the primary runtime. | ACCEPTED | Constrains an explicitly tested compatibility boundary. |
| `AD-002` | Use a `src/vector_barrage/` package layout and `python -m vector_barrage` entry point. | ACCEPTED | Provides a conventional import/execution surface. |
| `AD-003` | Use `pyproject.toml` as canonical package/dependency metadata. | ACCEPTED | Avoids conflicting dependency sources. |
| `AD-004` | Use one iterative application coordinator for Menu, Game, Scores, About and Exit. | ACCEPTED | Prevents recursive screen construction. |
| `AD-005` | Separate deterministic gameplay model/rules from Pygame session/rendering. | ACCEPTED | Improves testability and ownership clarity. |
| `AD-006` | Give the active screen/session exclusive event retrieval ownership. | ACCEPTED | Prevents competing event-queue drains. |
| `AD-007` | Use one authoritative score-storage boundary in `storage.py`. | ACCEPTED | Centralizes parsing, ordering, migration, precedence and writes. |
| `AD-008` | Use `scores.txt` as canonical data while retaining explicit `puntajes.txt` compatibility. | ACCEPTED | Establishes a clear canonical filename without silently losing legacy data. |
| `AD-009` | Separate bundled/read-only resources from writable persistence. | ACCEPTED | Supports source and frozen execution correctly. |
| `AD-010` | Use programmatic Pygame geometry for public visuals. | ACCEPTED | Eliminates external gameplay artwork dependency. |
| `AD-011` | Use procedural PCM synthesis for public audio. | ACCEPTED | Preserves semantic audio without copied audio assets. |
| `AD-012` | Retain an injectable `NullAudioService`. | ACCEPTED | Supports testing/audio-disabled contexts without changing normal runtime semantics. |
| `AD-013` | Keep external-link/platform bridging in `links.py`. | ACCEPTED | Isolates host-specific link behavior from UI presentation. |
| `AD-014` | Use synthetic score seed data only in the public candidate. | ACCEPTED | Prevents publication of historical/private player data. |
| `AD-015` | Use PyInstaller for the controlled Windows packaging workflow. | ACCEPTED / VALIDATED | Provides a reproducible packaging path and completed hardened Windows engineering evidence. |
| `AD-016` | Treat source and packaged runtime validation as independent surfaces. | ACCEPTED | Prevents source PASS from being inherited by an untested executable. |
| `AD-017` | Publish a substantial engineering dossier (`00`–`06`) in addition to README/NOTICE. | ACCEPTED | Preserves architecture, traceability, runbooks and readiness depth. |
| `AD-018` | Require candidate-specific screenshots/evidence. | ACCEPTED | Evidence must match the product/version whose claims it supports. |
| `AD-019` | License Vector Barrage-owned material under MIT and keep third-party software under its own terms. | ACCEPTED / IMPLEMENTED | Fits the source-first portfolio boundary while preserving third-party licensing separation. |
| `AD-020` | Resolve UI fonts from approved host-system fonts instead of relying on Pygame's bundled default font asset. | ACCEPTED / VALIDATED | Reduces bundled media/provenance surface while preserving readable UI. |
| `AD-021` | Track the controlled PyInstaller spec and Pygame hook as source engineering artifacts. | ACCEPTED / VALIDATED | Makes packaging constraints reproducible and testable without publishing generated build output. |
| `AD-022` | Publish Vector Barrage as a source-first portfolio repository and do not distribute `VectorBarrage.exe` under the current profile. | ACCEPTED | Matches portfolio evidence needs and avoids unnecessary binary-distribution overhead while preserving completed package QA internally. |
| `AD-023` | Preserve full binary component/compliance analysis as internal/optional-future evidence. | ACCEPTED | No-Loss preservation supports future binary distribution without making it a current publication prerequisite. |

## Key Decision Notes

### Application lifecycle is coordinator-owned

Screens return outcomes; they do not launch another complete screen/application lifecycle. This keeps the control graph shallow and deterministic.

### Game result is an integration boundary

Gameplay returns a result. The application determines strict new-record eligibility, invokes Name Entry and owns the exactly-once persistence call.

### Generated media is intentional

Programmatic visuals and procedural audio are the intended `v1.1.0` design. No empty `assets/` tree is required merely to mirror a conceptual architecture.

### Host fonts are a deliberate dependency boundary

`ui_fonts.py` resolves approved fonts supplied by the host OS. Vector Barrage therefore does not need to copy a font file into the repository or bundle Pygame's default font asset for its UI.

### Public seed and runtime data are separate concerns

The versioned `scores.txt` is a synthetic public/source seed. Tests do not mutate it. Frozen/local packages may initialize writable data from the bundled seed, but durable runtime scores remain outside the read-only bundle.

### Packaging capability is not publication scope

The hardened Windows package is technically validated and preserved as engineering evidence. The current public portfolio deliberately distributes source, tests, docs and build configuration—not the executable itself.

### Documentation depth remains part of product quality

README is the entry layer, not a substitute for requirement, architecture, governance, solution, implementation or readiness artifacts. Public sanitization removes private/historical mechanics without reducing useful engineering content.

## Decision Change Policy

A future change requires a new/amended decision when it materially affects package/module architecture, lifecycle ownership, persistence semantics, dependency compatibility, media strategy, packaging/distribution model, public evidence requirements or licensing/publication boundary.

Local refactors preserving these contracts need not create artificial decision records.
