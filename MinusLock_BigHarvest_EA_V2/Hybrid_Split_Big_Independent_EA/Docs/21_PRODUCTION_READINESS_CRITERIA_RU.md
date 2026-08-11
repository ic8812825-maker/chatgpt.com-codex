# Критерии production-готовности

Версия HSB.0R-C.26. Нормативный статус.

Для реальной торговли одновременно требуются: NORMATIVE_DOCUMENTATION, MQL5_MAPPING, METAEDITOR_COMPILE, ON_TRADE_TRANSACTION, OWNERSHIP_GUARD, ECONOMIC_LEDGER, ALLOCATION_LEDGER, PERSISTENCE, RECONCILIATION, FINAL_CLOSE, PARTIAL_FAR, SMALL_TRANSITION, STRATEGY_TESTER, STRESS_TESTS, DEMO_FORWARD и REAL_LIMITED_APPROVAL=EXPLICIT.

Сейчас подтверждена только нормативная документация. BROKER_MONEY_RUNTIME_PROOF=NOT_PROVEN; METAEDITOR/STRATEGY_TESTER=NOT_APPLICABLE; REAL_TRADING_ALLOWED=NO. HSB.1 может начаться только после отдельного решения администратора и только как неторгующий каркас.
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

> **Граница реализации HSB.1V (2026-08-10).** Описанный production lifecycle остаётся нормативной спецификацией, а не реализованным сценарием. В каркасе нет production execution, broker-money runtime и production persistence. Действуют: ровно один Far; promotion только из actual BigCore residual; FinalReserve запрещён для Partial Far; allocations не прибавляются к actual money повторно; Final Close определяется только actual money; только COMPLETED_FILL снимает transaction barrier; retry сохраняет ActionID; conflict ведёт в RECONCILING; unresolved critical error — в TERMINAL_SAFE; no auto-resume; REAL_LIMITED и HSB.2 запрещены.
