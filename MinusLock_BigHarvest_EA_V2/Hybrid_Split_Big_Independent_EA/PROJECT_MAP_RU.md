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
NEXT_ALLOWED_STAGE=HSB.1V
AWAITING_FINAL_ACCEPTANCE=YES
REAL_TRADING_ALLOWED=NO
## Нормативный статус HSB.1V (2026-08-10)

```text
HSB_STAGE_0_DOCUMENTATION=PASS
HSB_STAGE_1_STRUCTURE=PASS
HSB_STAGE_1_NO_TRADE_GUARD=PASS
HSB_STAGE_1_DEPENDENCY_AUDIT=PASS
HSB_STAGE_1_COMPILE=NOT_VERIFIED
HSB_STAGE_1_MQL5_TESTS=NOT_VERIFIED
HSB_STAGE_1_STATUS=ENVIRONMENT_VERIFICATION_REQUIRED
HSB_STAGE_2_STARTED=NO
TRADING_IMPLEMENTED=NO
TRADE_REQUESTS_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
NEXT_ALLOWED_STAGE=HSB.1V
```

HSB.2 не разрешён. Этот блок заменяет прежние текущие статусные декларации; исторические результаты в тексте сохраняют только доказательное значение на дату их создания.
