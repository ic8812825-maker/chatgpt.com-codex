# PREP-R4-R2 implementation handoff

Handoff предназначен только для административной проверки. `TRADING_LOGIC_START_ALLOWED=NO`.

| Блок | Будущий owner | API/DTO и reference | Preconditions/postconditions | Invariants/vectors/persistence/restart | Acceptance |
|---|---|---|---|---|---|
| IMPL-01 | planned Types/Validation owners | immutable Context, Intent, Deal, FillEvidence; `context_error`, `deal_error` | typed finite identity; no side effects | numeric/identity vectors; deterministic digest | compile-only |
| IMPL-02 | planned FillAccounting owner | `classify_fill` | persisted intent; cumulative per ticket | volume conservation, duplicate/foreign/stale vectors; persist cumulative IDs | R2 fill proofs |
| IMPL-03 | planned InitialLock owner | `initial_lock` | winner intent persisted | full fill and positive net; partial restart blocked | Initial vectors |
| IMPL-04 | planned Big owner | `big_settlement` | each leg separately full | no cross-ticket netting; persistence before settlement | Big vectors |
| IMPL-05 | planned Small/Far owner | `small_settlement` | Small/Old Far/Big legs full | no dual tail; no NewFar before full fill | Small vectors |
| IMPL-06 | planned Restart owner | `restart_replay` | persisted cumulative evidence | exactly-once consumed IDs; reconcile partial/overfill | Restart vectors |
| IMPL-07 | planned FSM owner | phase DTO | settlement persisted | revision monotonic; commit after proof | scenario contracts |
| IMPL-08 | planned DisabledAdapter owner | serialized intents only | all earlier acceptance complete | dispatch remains hard-disabled | separate admin review |

Broker dispatch остаётся последним отдельным этапом и не разрешён этим handoff.
