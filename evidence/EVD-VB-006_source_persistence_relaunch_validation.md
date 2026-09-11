# EVD-VB-006 — Source Persistence / Relaunch Validation

Project: **Vector Barrage**  
Release target: `v1.1.0`  
Evidence type: Isolated source persistence and complete-process relaunch validation  
Status: **PASS — SOURCE / PUBLIC ENGINEERING EVIDENCE**

## Purpose

Record observed source-mode new-record persistence without mutating the versioned public `scores.txt` seed. This evidence supports the source persistence contract only; packaged persistence is a separate evidence surface.

## Validation Boundary

The validation used an isolated writable score store rather than the repository seed.

Initial isolated data:

```text
QA_SEED,0
```

After the accelerated completed-game/new-record flow:

```text
QA_SEED,0
QA_Player,130
```

`QA_Player,130` appeared exactly once.

## Observed Flow

```text
completed gameplay
-> final score evaluated against previous maximum
-> strict new-record decision
-> Name Entry
-> accepted non-empty name
-> one append to isolated canonical score storage
-> application process terminated completely
-> application relaunched
-> persisted score remained available
```

## Acceptance Checks

| Check | Observed result |
|---|---|
| QA used isolated writable data | PASS |
| Repository seed stayed outside write test | PASS |
| New record entered record flow | PASS |
| Accepted name produced one append | PASS |
| Duplicate append during same submission | NOT OBSERVED |
| Persisted record after first write | PASS |
| Complete process termination before relaunch | PASS |
| Record available after relaunch | PASS |

## Contract Context

The source storage contract remains:

1. canonical `scores.txt` is authoritative when present;
2. legacy `puntajes.txt` is considered only when canonical data is absent;
3. successful legacy migration preserves canonical precedence;
4. seed initialization must not overwrite existing canonical data;
5. malformed records are tolerated by reads;
6. accepted new-record submissions append exactly once through the application/storage boundary.

At the original evidence checkpoint, the corrected candidate suite completed:

```text
109 passed in 0.27s
Failed: 0
Errors: 0
```

That test count is preserved as historical context for this evidence event. Subsequent host-font and packaging-contract hardening expanded the accepted suite to:

```text
CURRENT_AUTOMATED_BASELINE = 125 PASS
```

## Current Claim Boundary

This evidence establishes:

```text
SOURCE_NEW_RECORD_FLOW          = PASS
SOURCE_EXACTLY_ONE_APPEND       = PASS
SOURCE_RELAUNCH_PERSISTENCE     = PASS
QA_SCORE_ISOLATION              = PASS
```

Separate later validation established packaged first-run and persistence/relaunch behavior. Those package results are internal engineering evidence under the current source-first profile and do not imply a public executable download.

This record does not establish screenshot admission or final publication readiness.

## Related Requirements

- `FR-07` — strict new-record handling;
- `FR-08` — local score persistence and compatibility;
- `NFR-04` — safe score-data integrity.

## Result

```text
EVIDENCE_ID                       = EVD-VB-006
SOURCE_EXACTLY_ONE_WRITE          = PASS
SOURCE_COMPLETE_RELAUNCH          = PASS
SOURCE_PERSISTENCE_AFTER_RELAUNCH = PASS
HISTORICAL_RECORD_BASELINE        = 109 PASS
CURRENT_AUTOMATED_BASELINE        = 125 PASS
PUBLIC_EVIDENCE_DISPOSITION       = ELIGIBLE / SOURCE ENGINEERING EVIDENCE
```
