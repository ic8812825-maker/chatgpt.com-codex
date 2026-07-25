# Hybrid Split Big — State Transition Truth Table

| Current | Event | Condition | Pending/actual requirement | Next | Failure |
|---|---|---|---|---|---|
| IDLE | Initial lock confirmed | identity/reconciliation PASS | both initial roles confirmed | FAR_ACTIVE | RECONCILIATION |
| FAR_ACTIVE | Candidate request | all pre-open gates PASS | immutable plan persisted | HYBRID_OPEN_PENDING | FAR_ACTIVE / TERMINAL_SAFE |
| HYBRID_OPEN_PENDING | Core fill | exact identifier/lot | persist confirmation | OPEN_TREND_PENDING | RECONCILIATION |
| OPEN_TREND_PENDING | Trend fill | exact identifier/lot | persist confirmation | OPEN_SMALL_PENDING | RECONCILIATION |
| OPEN_SMALL_PENDING | Small fill | all three roles reconciled | fingerprint matches | HYBRID_ACTIVE | RECONCILIATION |
| HYBRID_ACTIVE | Big trigger | Base+Worst+identity PASS | frozen close plan | HARVEST_PENDING | TERMINAL_SAFE |
| HYBRID_ACTIVE | Small trigger | solver/budget/Base+Worst PASS | frozen transition plan | SMALL_TRANSITION_PENDING | TERMINAL_SAFE |
| HARVEST_PENDING | all Harvest deals | all confirmed | actual net then allocation | HARVEST_RECONCILE | RECONCILIATION |
| HARVEST_RECONCILE | Final Close preview | PASS | immutable final plan | FINAL_CLOSE_PENDING | FAR_ACTIVE / HYBRID_ACTIVE |
| HARVEST_RECONCILE | no final coverage | continuation candidate PASS | no Reserve debit | FAR_ACTIVE | TERMINAL_SAFE |
| SMALL_TRANSITION_PENDING | all close deals | exact residual Core confirmed | cumulative loss update | NEW_FAR_PENDING | RECONCILIATION |
| NEW_FAR_PENDING | next basket plan | fingerprint/gates PASS | residual promotion persisted | HYBRID_OPEN_PENDING | TERMINAL_SAFE |
| FINAL_CLOSE_PENDING | all managed closes | positions=0 and actual threshold PASS | confirmed deals reconciled | CLOSED_PROFIT | TERMINAL_SAFE |
| ANY_ACTIVE | restart | persisted state exists | full identity/ledger reconciliation | previous safe state | RECONCILIATION |
| RECONCILIATION | exact match restored | no pending mismatch | event replay idempotent | persisted safe state | TERMINAL_SAFE |
| TERMINAL_SAFE | proven close-only action | WorstRiskAfter < WorstRiskBefore | confirmed close, recheck final | TERMINAL_SAFE / FINAL_CLOSE_PENDING | MANUAL_HOLD |
| MANUAL_HOLD | administrator reset | explicit audited decision | reconciliation complete | IDLE / TERMINAL_SAFE | MANUAL_HOLD |

**Temporal refinement:** строка HARVEST_RECONCILE выполняется для каждого последовательного level: confirmed/projected working legs текущего state закрыты один раз, Partial Far применяется, затем next basket создаёт новый `StateBefore`. Повторный расчёт исходных legs запрещён.

Temporal authority: `HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`.
