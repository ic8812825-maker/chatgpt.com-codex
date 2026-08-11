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
METAEDITOR_COMPILE=NOT_RUN_ENVIRONMENT_UNAVAILABLE
MQL5_UNIT_TESTS=NOT_RUN_ENVIRONMENT_UNAVAILABLE
HSB_STAGE_1V_STATUS=PARTIAL_ENVIRONMENT_BLOCKED
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

## Единый итоговый статус HSB.1V (2026-08-11)

```text
HSB_STAGE_0_DOCUMENTATION=PASS
HSB_STAGE_1_STRUCTURE=PASS
HSB_STAGE_1V_STATUS=PARTIAL_ENVIRONMENT_BLOCKED
METAEDITOR_COMPILE=NOT_RUN_ENVIRONMENT_UNAVAILABLE
MQL5_UNIT_TESTS=NOT_RUN_ENVIRONMENT_UNAVAILABLE
HSB_STAGE_2_STARTED=NO
BROKER_MONEY_RUNTIME=NOT_IMPLEMENTED
PRODUCTION_PERSISTENCE=NOT_IMPLEMENTED
PRODUCTION_TRANSACTION_ENGINE=NOT_IMPLEMENTED
TRADING_SCENARIOS_IMPLEMENTED=0
TRADING_IMPLEMENTED=NO
REAL_TRADING_ALLOWED=NO
NEXT_ALLOWED_STAGE=HSB.1V
```

`NEXT_ALLOWED_STAGE=HSB.1V` означает только продолжение доказательной проверки HSB.1V. HSB.2 не разрешён.

## HSB.2A — расчётные модули

| Requirement ID | Owner | MQL5 file | Type/function | Unit tests | Static evidence | Compile | Runtime | State |
|---|---|---|---|---|---|---|---|---|
| HSBI-MONEY-021 | Docs/24 | Money/HSBI_BrokerMoneyTypes.mqh; BrokerMoneyModel.mqh | HSBI_BrokerProperties; HSBI_CalculateProjectedProfit | T27-T33,T56-T60 | source/no-trade audit | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | MAPPED_STATIC |
| HSBI-MONEY-022 | Docs/27 | Planning/HSBI_ControlPrices.mqh; Money/HSBI_CostModel.mqh | HSBI_ControlPrice; HSBI_CostSnapshot | T51-T58 | source/no-trade audit | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | MAPPED_STATIC |
| HSBI-MARGIN-001 | Docs/24 | Money/HSBI_BrokerMarginModel.mqh | HSBI_CalculateProjectedMargin | T61-T63 | source/no-trade audit | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | IMPLEMENTED_UNVERIFIED |
| HSBI-GRID-001 | Docs/25 | Planning/HSBI_BrokerGrid.mqh | price-grid functions | T34-T40 | pure-function review | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | MAPPED_STATIC |
| HSBI-GRID-002 | Docs/25 | Planning/HSBI_BrokerGrid.mqh | volume-grid functions | T30,T41-T50 | pure-function review | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | MAPPED_STATIC |
| HSBI-GEO-001 | Docs/26 | Planning/HSBI_GeometrySolver.mqh | HSBI_SolveBigGeometry | T64,T68 | pure-function review | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | IMPLEMENTED_UNVERIFIED |
| HSBI-GEO-002 | Docs/26 | Planning/HSBI_GeometrySolver.mqh | HSBI_ValidateRecoverySlope | T65-T67 | pure-function review | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | MAPPED_STATIC |
| HSBI-GEO-003 | Docs/26 | Planning/HSBI_GeometryTypes.mqh; GeometrySolver.mqh | HSBI_RecoveryDirectionResult | T68 | pure-contract review | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | MAPPED_STATIC |
| HSBI-CATCHUP-001 | Docs/24/26 | Money/HSBI_CatchUpTypes.mqh; CatchUpModel.mqh | HSBI_EvaluateCatchUp | T69-T70 | pure-contract review | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | IMPLEMENTED_UNVERIFIED |
| HSBI-FAILCLOSED-001 | Docs/24-27 | Risk/HSBI_CalculationGateTypes.mqh | HSBI_FailClosed; result flags | T32,T57,T70 | fail-closed review | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | MAPPED_STATIC |

Ни один статус HSB.2A не означает production readiness. MetaEditor compile, MT5 runtime и broker-money runtime proof требуют проверки администратора.
