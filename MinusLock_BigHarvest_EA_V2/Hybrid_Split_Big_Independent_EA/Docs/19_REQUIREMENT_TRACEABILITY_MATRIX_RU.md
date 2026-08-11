# 19. Матрица требований и MQL5 mapping HSB.1

Версия HSB.1.29. Торговые сценарии на этом этапе имеют только интерфейсы.

| Requirement ID | Owner document | MQL5 file | MQL5 type/function | Unit test | Compile evidence | Status |
|---|---|---|---|---|---|---|
| HSBI-GEN-030 | 18 | Core/HSBI_Version.mqh; RuntimeMode.mqh | constants, HSBI_RuntimePolicy | T01-T03,T26 | HSB_STAGE_1_COMPILE_RESULT_RU | UNVERIFIED |
| HSBI-ID-010 | 02/18 | Core/HSBI_Identifiers.mqh; Roles.mqh | HSBI_Identity, ownership comparators | T04-T12 | NOT_RUN | UNVERIFIED |
| HSBI-FSM-002 | 06 | Core/HSBI_StateMachine.mqh; StateValidator.mqh | pure transition contract | T13-T17,T23 | NOT_RUN | UNVERIFIED |
| HSBI-GEO-005 | 05 | Planning/HSBI_ControlPrices.mqh; GeometryTypes.mqh | snapshot/control DTO and validators | planned | NOT_RUN | UNVERIFIED |
| HSBI-NF-001 | 13/14 | Planning/HSBI_NewFarCandidate.mqh | structural validation/tie-break | T09-T12,T21 | NOT_RUN | MAPPED_PARTIAL |
| HSBI-MONEY-014 | 08 | Money/EconomicLedgerTypes.mqh; AllocationLedgerTypes.mqh | source identity/conservation | T18-T20 | NOT_RUN | UNVERIFIED |
| HSBI-PF-001 | 11 | Money/AllocationLedgerTypes.mqh; Scenarios/PartialFarTypes.mqh | Reserve isolation contract | T20 | NOT_RUN | INTERFACE_ONLY |
| HSBI-FC-001 | 12 | Money/HSBI_MoneyTypes.mqh; Scenarios/FinalCloseTypes.mqh | RecoveryPL/threshold DTO | planned | NOT_RUN | INTERFACE_ONLY |
| HSBI-TX-006 | 07 | Execution/ActionTypes.mqh; EventTypes.mqh; TransactionTypes.mqh | action/event/outcome contract | T15-T17 | NOT_RUN | UNVERIFIED |
| HSBI-PERSIST-001 | 16 | Persistence/SnapshotTypes.mqh; JournalTypes.mqh; PersistenceInterface.mqh | schema/test digest/stub | T22 | NOT_RUN | MAPPED_PARTIAL |
| HSBI-RECON-002 | 17 | Persistence/HSBI_ReconciliationTypes.mqh | pure reconciliation DTO/comparison | T24 | NOT_RUN | MAPPED_PARTIAL |
| HSBI-RISK-001 | 15 | Risk/HSBI_RiskTypes.mqh; RiskGateResult.mqh | pure limits and gates | planned | NOT_RUN | UNVERIFIED |
| HSBI-INIT-001..010 | 09 | Scenarios/HSBI_InitialLockTypes.mqh | scenario contract only | planned | N/A | INTERFACE_ONLY |
| HSBI-BIG-001..012 | 10 | Scenarios/HSBI_BigHarvestTypes.mqh | scenario contract only | planned | N/A | INTERFACE_ONLY |
| HSBI-SMALL-001..026 | 13 | Scenarios/HSBI_SmallTransitionTypes.mqh | scenario contract only | planned | N/A | INTERFACE_ONLY |
| HSBI-PROD-001 | 21 | Execution/HSBI_NoTradeExecution.mqh | fail-closed stubs | T25-T26 | static audit PASS | UNVERIFIED |

## Итог

```text
OWNERLESS_REQUIREMENTS=0
MAPPED_IMPLEMENTED=0
MAPPED_PARTIAL=3
INTERFACE_ONLY=5
TRADING_SCENARIOS_IMPLEMENTED=0
BROKER_MONEY_RUNTIME=NOT_IMPLEMENTED
PRODUCTION_PERSISTENCE=NOT_IMPLEMENTED
METAEDITOR_COMPILE=NOT_RUN_ENVIRONMENT_UNAVAILABLE
MQL5_UNIT_TESTS=NOT_RUN_ENVIRONMENT_UNAVAILABLE
```

Ни один торговый сценарий не помечен IMPLEMENTED. Production persistence, broker-money solver и transaction lifecycle не реализованы.
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

## Правило статуса HSB.1V

`MAPPED_IMPLEMENTED` не присваивается до фактических MQL5 compile и test evidence. Код validators и pure contracts с назначенными, но не запущенными тестами имеет статус `UNVERIFIED`; DTO/контракты без production lifecycle — `MAPPED_PARTIAL`; торговые сценарии — `INTERFACE_ONLY`. Наличие структуры само по себе не доказывает production implementation.

> **Граница реализации HSB.1V (2026-08-10).** Описанный production lifecycle остаётся нормативной спецификацией, а не реализованным сценарием. В каркасе нет production execution, broker-money runtime и production persistence. Действуют: ровно один Far; promotion только из actual BigCore residual; FinalReserve запрещён для Partial Far; allocations не прибавляются к actual money повторно; Final Close определяется только actual money; только COMPLETED_FILL снимает transaction barrier; retry сохраняет ActionID; conflict ведёт в RECONCILING; unresolved critical error — в TERMINAL_SAFE; no auto-resume; REAL_LIMITED и HSB.2 запрещены.
