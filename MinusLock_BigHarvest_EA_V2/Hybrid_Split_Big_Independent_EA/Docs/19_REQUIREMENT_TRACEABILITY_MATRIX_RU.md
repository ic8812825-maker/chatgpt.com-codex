# 19. Матрица требований и MQL5 mapping HSB.1

Версия HSB.1.29. Торговые сценарии на этом этапе имеют только интерфейсы.

| Requirement ID | Owner document | MQL5 file | MQL5 type/function | Unit test | Compile evidence | Status |
|---|---|---|---|---|---|---|
| HSBI-GEN-030 | 18 | Core/HSBI_Version.mqh; RuntimeMode.mqh | constants, HSBI_RuntimePolicy | T01-T03,T26 | HSB_STAGE_1_COMPILE_RESULT_RU | MAPPED_IMPLEMENTED |
| HSBI-ID-010 | 02/18 | Core/HSBI_Identifiers.mqh; Roles.mqh | HSBI_Identity, ownership comparators | T04-T12 | NOT_RUN | MAPPED_IMPLEMENTED |
| HSBI-FSM-002 | 06 | Core/HSBI_StateMachine.mqh; StateValidator.mqh | pure transition contract | T13-T17,T23 | NOT_RUN | MAPPED_IMPLEMENTED |
| HSBI-GEO-005 | 05 | Planning/HSBI_ControlPrices.mqh; GeometryTypes.mqh | snapshot/control DTO and validators | planned | NOT_RUN | MAPPED_IMPLEMENTED |
| HSBI-NF-001 | 13/14 | Planning/HSBI_NewFarCandidate.mqh | structural validation/tie-break | T09-T12,T21 | NOT_RUN | MAPPED_PARTIAL |
| HSBI-MONEY-014 | 08 | Money/EconomicLedgerTypes.mqh; AllocationLedgerTypes.mqh | source identity/conservation | T18-T20 | NOT_RUN | MAPPED_IMPLEMENTED |
| HSBI-PF-001 | 11 | Money/AllocationLedgerTypes.mqh; Scenarios/PartialFarTypes.mqh | Reserve isolation contract | T20 | NOT_RUN | INTERFACE_ONLY |
| HSBI-FC-001 | 12 | Money/HSBI_MoneyTypes.mqh; Scenarios/FinalCloseTypes.mqh | RecoveryPL/threshold DTO | planned | NOT_RUN | INTERFACE_ONLY |
| HSBI-TX-006 | 07 | Execution/ActionTypes.mqh; EventTypes.mqh; TransactionTypes.mqh | action/event/outcome contract | T15-T17 | NOT_RUN | MAPPED_IMPLEMENTED |
| HSBI-PERSIST-001 | 16 | Persistence/SnapshotTypes.mqh; JournalTypes.mqh; PersistenceInterface.mqh | schema/test digest/stub | T22 | NOT_RUN | MAPPED_PARTIAL |
| HSBI-RECON-002 | 17 | Persistence/HSBI_ReconciliationTypes.mqh | pure reconciliation DTO/comparison | T24 | NOT_RUN | MAPPED_PARTIAL |
| HSBI-RISK-001 | 15 | Risk/HSBI_RiskTypes.mqh; RiskGateResult.mqh | pure limits and gates | planned | NOT_RUN | MAPPED_IMPLEMENTED |
| HSBI-INIT-001..010 | 09 | Scenarios/HSBI_InitialLockTypes.mqh | scenario contract only | planned | N/A | INTERFACE_ONLY |
| HSBI-BIG-001..012 | 10 | Scenarios/HSBI_BigHarvestTypes.mqh | scenario contract only | planned | N/A | INTERFACE_ONLY |
| HSBI-SMALL-001..026 | 13 | Scenarios/HSBI_SmallTransitionTypes.mqh | scenario contract only | planned | N/A | INTERFACE_ONLY |
| HSBI-PROD-001 | 21 | Execution/HSBI_NoTradeExecution.mqh | fail-closed stubs | T25-T26 | static audit PASS | MAPPED_IMPLEMENTED |

## Итог

```text
OWNERLESS_REQUIREMENTS=0
MAPPED_IMPLEMENTED=11
MAPPED_PARTIAL=3
INTERFACE_ONLY=5
TRADING_SCENARIOS_IMPLEMENTED=0
METAEDITOR_COMPILE=NOT_RUN_ENVIRONMENT_UNAVAILABLE
MQL5_UNIT_TESTS=NOT_RUN_ENVIRONMENT_UNAVAILABLE
```

Ни один торговый сценарий не помечен IMPLEMENTED. Production persistence, broker-money solver и transaction lifecycle не реализованы.