# EVD-VB-005 — Source Runtime Validation

Project: **Vector Barrage**  
Release target: `v1.1.0`  
Evidence type: Integrated source runtime validation  
Status: **PASS — SOURCE / PUBLIC ENGINEERING EVIDENCE**

## Purpose

Record the observed integrated runtime behavior of the Vector Barrage source candidate in the validated WSL2/X11 execution profile. This evidence establishes source-runtime behavior only; package validation is a separate evidence surface.

## Environment

```text
Host context: Windows + WSL2 / Ubuntu
Graphical bridge: documented X11 graphical path
Python: 3.13.15
Pygame: 2.6.1
Package entry point: python -m vector_barrage
Source package: src/vector_barrage/
```

The runtime used the independently implemented Vector Barrage source with programmatically generated visuals and procedurally synthesized audio. Historical course/third-party gameplay media were not required.

## Observed Runtime Scope

| Runtime surface | Observed result |
|---|---|
| Application startup/window | PASS |
| Main Menu presentation | PASS |
| Main Menu → Game navigation | PASS |
| Horizontal player movement | PASS |
| Projectile firing | PASS |
| Enemy interaction/destruction | PASS |
| Lives / Score / Level HUD | PASS |
| Gameplay → Main Menu return | PASS |
| Scores screen | PASS |
| About screen | PASS |
| Menu procedural audio | PASS |
| Gameplay procedural audio | PASS |
| Enemy-destruction audio cue | PASS |
| Non-recursive application navigation | PASS |

## Regression Context

At the original formalization checkpoint, the then-current corrected source suite completed:

```text
Affected screen/service regression: 20 passed in 0.08s
Full corrected candidate suite:      109 passed in 0.27s
Failed:                              0
Errors:                              0
```

That result is preserved as the historical regression context of this evidence record. Subsequent source hardening added host-font and packaging-contract coverage. The **current accepted automated baseline is `125 PASS`**. The later additions do not invalidate the source runtime observations recorded here.

## Current Claim Boundary

This evidence establishes:

```text
SOURCE_GUI_RUNTIME        = PASS
SOURCE_AUDIO_RUNTIME      = PASS
SOURCE_NAVIGATION         = PASS
SOURCE_GAMEPLAY           = PASS
SOURCE_SCREEN_INTEGRATION = PASS
```

Separate later validation established the hardened Windows package as PASS; under the current source-first portfolio profile those package results are internal engineering evidence and do not imply a public executable download.

This record does not establish screenshot admission or final public-repository readiness.

## Related Requirements

- `FR-01` — application shell/navigation;
- `FR-02` — player movement/firing;
- `FR-03` — enemy/wave gameplay;
- `FR-04` — collision/damage/scoring;
- `FR-05` — HUD;
- `FR-06` — score presentation;
- `FR-09` — semantic audio;
- `FR-10` — generated visual presentation;
- `FR-11` — About/product identity;
- `NFR-10` — source GUI operability.

## Result

```text
EVIDENCE_ID                   = EVD-VB-005
VECTOR_BARRAGE_SOURCE_RUNTIME = PASS
HISTORICAL_RECORD_BASELINE    = 109 PASS
CURRENT_AUTOMATED_BASELINE    = 125 PASS
PUBLIC_EVIDENCE_DISPOSITION   = ELIGIBLE / SOURCE ENGINEERING EVIDENCE
PUBLIC_EXECUTABLE_CLAIM       = NONE
```
