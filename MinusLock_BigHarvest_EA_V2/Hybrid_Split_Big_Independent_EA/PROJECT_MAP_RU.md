# Карта проекта Hybrid Split Big Independent EA

## Фактический HSB.1

Созданы независимые слои Core, Planning, Money, Execution, Scenarios, Persistence, Risk, Diagnostics и MQL5 test harness. Production broker execution отсутствует.

```text
EA shell
→ Core
→ Execution/NoTrade stub
→ Diagnostics
Planning → Core
Money → Core types
Execution → Core
Scenarios → contracts only
Persistence → DTO/schema only
Risk → pure validation
Diagnostics → read-only
```

Реализованы: versions/enums/types/reasons, identity/roles/context, pure FSM/invariants, market/control DTO, CandidatePlan/NewFar candidate, money/ledger DTO, action/event/outcome, ownership guard, scenario DTO, snapshot/journal/reconciliation, risk gates, logger/diagnostics, 26-test harness.

Не реализованы: broker execution, production OnTradeTransaction lifecycle, scenario execution, broker-money calculations, NewFar full solver, production storage, MetaEditor/MT5 evidence.

HSB_STAGE_1_STATUS=READY_FOR_ACCEPTANCE
NEXT_ALLOWED_STAGE=NONE
AWAITING_FINAL_ACCEPTANCE=YES
REAL_TRADING_ALLOWED=NO