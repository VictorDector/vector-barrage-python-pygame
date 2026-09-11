# Reference Register

Project: **Vector Barrage**  
Release target: `v1.1.0`  
Publication profile: **Source-First Portfolio Repository**  
Status: ACTIVE

## Purpose

Record technical and provenance references relevant to the public Vector Barrage product while keeping project claims distinct from external-source claims. This register is not a copied-source lineage map and does not import third-party material into the repository.

## Technical References

| Ref | Source | Relevance | Use |
|---|---|---|---|
| `REF-01` | Python documentation — https://docs.python.org/3/ | Python 3.13.x language/runtime semantics. | Runtime and standard library. |
| `REF-02` | Pygame documentation — https://www.pygame.org/docs/ | Display, events, drawing, font, timing and mixer APIs. | GUI/game-loop/audio implementation. |
| `REF-03` | PyInstaller documentation — https://pyinstaller.org/en/stable/ | Frozen-runtime and standalone packaging behavior. | Optional packaging engineering workflow. |
| `REF-04` | Python Packaging User Guide — https://packaging.python.org/ | `pyproject.toml`, metadata and installation conventions. | Reproducible source packaging. |
| `REF-05` | pytest documentation — https://docs.pytest.org/ | Automated test execution/fixtures. | Regression infrastructure. |

## Project Design Sources

Project-owned design records include:

- `behavioral_specification.md` — externally observable behavior;
- `requirement_ctq_map.md` — requirements/CTQs;
- `software_architecture.md` — logical architecture;
- `source_architecture.md` — physical package/dependency architecture;
- `architecture_decisions.md` — material design decisions;
- `validation_policy.md` — validation levels and claim boundaries.

These records govern Vector Barrage behavior unless superseded by an accepted later decision.

## Academic / Learning Provenance

The broader development effort was informed by academic Pygame learning material and general software-development references. Those materials remain learning/provenance context rather than files or source expression redistributed inside Vector Barrage.

```text
learning concepts / general programming knowledge
        -> may inform design reasoning

third-party instructional source expression
        -> not copied into public implementation

course-provided visual/audio material
        -> not required by Vector Barrage
```

## Media Reference Boundary

The current product uses Pygame primitive drawing plus host-system font rendering for visuals, and numeric tone definitions plus runtime PCM synthesis for audio. No external gameplay artwork, sprite pack, music track or sound-effect file is required.

If future media is introduced, source/license/provenance must be documented before public use.

## Licensing Reference Boundary

Current source-first repository licensing is resolved as:

```text
Vector Barrage-owned material = MIT / LICENSE present
Python                        = third-party / own terms
Pygame 2.6.1                  = third-party / own terms
pytest / setuptools / PyInstaller = third-party / own terms
public bundled executable     = none
```

`NOTICE.md` records the concise third-party separation. The previously completed hardened binary component/license analysis remains internal evidence and is not a current source-publication prerequisite. If downloadable executable distribution is later proposed, binary-specific compliance must be reopened.

## Reference Handling Principles

1. External technical documentation may establish API/runtime semantics but does not replace project-specific validation.
2. A reference to a tool/library does not imply endorsement or ownership.
3. Academic provenance does not automatically grant redistribution/relicensing rights.
4. Public source claims must be supported by the actual Vector Barrage implementation and tests/evidence.
5. Runtime evidence remains necessary even when an external API is documented.
6. Third-party code/media introduced in the future requires exact provenance/license disposition before public use.
7. Packaging references do not imply a public executable exists under the current source-first profile.

## Current Reference Result

```text
TECHNICAL_REFERENCE_BASELINE       = DEFINED
PROJECT_DESIGN_SOURCES             = DEFINED
ACADEMIC_PROVENANCE                = HIGH_LEVEL / NON-DISTRIBUTED
EXTERNAL_GAME_MEDIA_DEPENDENCY     = NONE
THIRD_PARTY_CODE_VENDORED          = NONE
MIT_LICENSE                        = PASS / ACCEPTED
CONCISE_THIRD_PARTY_NOTICE         = PASS / ACCEPTED
FULL_BINARY_LICENSE_REVIEW         = PRESERVED / OPTIONAL FUTURE
```
