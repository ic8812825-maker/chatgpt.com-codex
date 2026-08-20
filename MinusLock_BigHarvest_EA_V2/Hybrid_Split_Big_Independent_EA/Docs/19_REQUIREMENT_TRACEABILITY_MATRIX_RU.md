<!-- HSB_2D_V1_R7_CANONICAL_STATUS_BEGIN
CURRENT_STAGE=HSB.2D-V1-R7
HSB.2D_V1_R1_PREVIOUS_ACCEPTANCE=HISTORICAL_SUPERSEDED
HSB.2D_V1_R2_PREVIOUS_ACCEPTANCE=HISTORICAL_SUPERSEDED
HSB.2D_V1_R3_PREVIOUS_ACCEPTANCE=HISTORICAL_SUPERSEDED
HSB.2D_V1_R4_PREVIOUS_ACCEPTANCE=HISTORICAL_SUPERSEDED
HSB.2D_V1_R5_PREVIOUS_ACCEPTANCE=HISTORICAL_SUPERSEDED
HSB.2D_V1_R6_PREVIOUS_ACCEPTANCE=HISTORICAL_SUPERSEDED
HSB.2D_V1_R7=CORRECTED_OFFLINE_VERIFICATION
HSB.2E_PREP_R1_PREVIOUS_ACCEPTANCE=HISTORICAL_SUPERSEDED
HSB.2E_PREP_R2=READY_FOR_ADMIN_REVIEW
GLOBAL_TERMINAL_PATH_ANALYSIS=PASS
UNAUTHORIZED_NO_OP_GLOBAL_BLOCK=PASS
S037_NO_OP_EXACT_AUTHORIZATION=PASS
GUARD_EXECUTION_DOMINANCE=PASS
GUARD_OUTCOME_DOMINANCE=PASS
CONDITION_NORMALIZATION=PASS
METAEDITOR_MAIN_COMPILE=NOT_RUN
METAEDITOR_TEST_COMPILE=NOT_RUN
MQL5_TESTS_T01_T464=NOT_RUN
STRATEGY_TESTER=NOT_RUN
BROKER_MONEY_RUNTIME_PROOF=NOT_RUN
HSB.2E=NOT_STARTED
TRADING_LOGIC_START_ALLOWED=NO
BROKER_DISPATCH_IMPLEMENTED=NO
TRADE_REQUESTS_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
HSB_2D_V1_R7_CANONICAL_STATUS_END -->

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

## HSB.2B — Future Small и NewFar Solver

| Requirement | Owner | MQL5 type/function | Tests | Static status | Runtime | Compile | Evidence |
|---|---|---|---|---|---|---|---|
| HSBI-FS-001 | Docs/27 | FutureSmallTypes; HSBI_SolveFutureSmall | T71-T73,T81-T83,T88 | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | USER_VERIFICATION_REQUIRED | HSB_STAGE_2B_IMPLEMENTATION_RU |
| HSBI-FS-002 | Docs/27 | HSBI_ValidateConservativeBound | T74-T78,T86-T87 | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | USER_VERIFICATION_REQUIRED | HSB_STAGE_2B_IMPLEMENTATION_RU |
| HSBI-FS-003 | Docs/27 | HSBI_CalculateFutureSmallDepth; plateau gate | T79-T80,T84-T85 | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | USER_VERIFICATION_REQUIRED | HSB_STAGE_2B_IMPLEMENTATION_RU |
| HSBI-FS-004 | Docs/27 | money/risk/margin/loss recursion gates | T89-T91 | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | USER_VERIFICATION_REQUIRED | HSB_STAGE_2B_IMPLEMENTATION_RU |
| HSBI-NF-001 | Docs/28 | ActualNewFar; HSBI_ValidateNewFarSource | T92-T93 | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | USER_VERIFICATION_REQUIRED | HSB_STAGE_2B_IMPLEMENTATION_RU |
| HSBI-NF-002 | Docs/28 | full source identity validation | T94-T98 | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | USER_VERIFICATION_REQUIRED | HSB_STAGE_2B_IMPLEMENTATION_RU |
| HSBI-NF-003 | Docs/28 | residual volume/grid validation | T99-T103 | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | USER_VERIFICATION_REQUIRED | HSB_STAGE_2B_IMPLEMENTATION_RU |
| HSBI-NF-004 | Docs/28 | broker-grid enumeration | T104-T106 | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | USER_VERIFICATION_REQUIRED | HSB_STAGE_2B_IMPLEMENTATION_RU |
| HSBI-NF-005 | Docs/29 | minimum safe objective | T107 | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | USER_VERIFICATION_REQUIRED | HSB_STAGE_2B_IMPLEMENTATION_RU |
| HSBI-NF-006 | Docs/28/29 | snapshot/plan/digest immutability | T109-T111,T118-T119 | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | USER_VERIFICATION_REQUIRED | HSB_STAGE_2B_IMPLEMENTATION_RU |
| HSBI-NF-007 | Docs/28 | Future Small/money availability | T112-T113 | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | USER_VERIFICATION_REQUIRED | HSB_STAGE_2B_IMPLEMENTATION_RU |
| HSBI-NF-008 | Docs/28 | HSBI_EvaluateNewFarGates | T114-T116 | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | USER_VERIFICATION_REQUIRED | HSB_STAGE_2B_IMPLEMENTATION_RU |
| HSBI-NF-009 | Docs/28 | second-Far reconciliation guard | T117 | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | USER_VERIFICATION_REQUIRED | HSB_STAGE_2B_IMPLEMENTATION_RU |
| HSBI-NF-010 | Docs/29 | deterministic comparator/digest | T108,T120 | IMPLEMENTED_UNVERIFIED | RUNTIME_UNAVAILABLE | USER_VERIFICATION_REQUIRED | HSB_STAGE_2B_IMPLEMENTATION_RU |

`IMPLEMENTED_UNVERIFIED` означает статическую реализацию без MetaEditor/MT5 evidence; runtime/compile PASS и production readiness не заявляются.

## HSB.2B-R — корректировка broker-money proof

| Requirement | Files/functions | Tests | Static | Compile/runtime |
|---|---|---|---|---|
| HSBI-MONEY-021-R | LevelMoneyEvaluator; HSBI_EvaluateProjectedLegMoney | T121-T125 | IMPLEMENTED_UNVERIFIED | USER_VERIFICATION_REQUIRED |
| HSBI-MARGIN-001-R | LevelMarginEvaluator; HSBI_EvaluateProjectedLegMargin | T127-T129 | IMPLEMENTED_UNVERIFIED | USER_VERIFICATION_REQUIRED |
| HSBI-MONEY-022-R | BasketMoneyEvaluator; four independent legs | T126,T130-T131 | IMPLEMENTED_UNVERIFIED | USER_VERIFICATION_REQUIRED |
| HSBI-FS-001-R | HSBI_EvaluateFutureSmallLevel | T130-T143 | IMPLEMENTED_UNVERIFIED | USER_VERIFICATION_REQUIRED |
| HSBI-FS-002-R | two-level bound with proof flags | T133-T147 | IMPLEMENTED_UNVERIFIED | USER_VERIFICATION_REQUIRED |
| HSBI-FS-004-R | typed basket-derived risk/margin/loss | T138-T141 | IMPLEMENTED_UNVERIFIED | USER_VERIFICATION_REQUIRED |
| HSBI-NF-004-R | candidate-specific Future Small/money | T148-T150 | IMPLEMENTED_UNVERIFIED | USER_VERIFICATION_REQUIRED |
| HSBI-NF-006-R | expanded input/candidate-list plan digest | T152-T157 | IMPLEMENTED_UNVERIFIED | USER_VERIFICATION_REQUIRED |
| HSBI-NF-010-R | complete-proof objective isolation | T158-T159 | IMPLEMENTED_UNVERIFIED | USER_VERIFICATION_REQUIRED |
| HSBI-FAILCLOSED-001-R | linear shortcut guards | T132,T150,T160 | MAPPED_STATIC | USER_VERIFICATION_REQUIRED |

Runtime/compile/broker proof PASS не заявляется без MetaEditor/MT5. Evidence: `Reports/HSB_STAGE_2B_R_FINAL_ACCEPTANCE_RU.md`, `Tests/Evidence/HSB_2B_R_NO_TRADE_STATIC_AUDIT_RU.md`.

## HSB.2B-R2 — allocation, level snapshots и proof isolation

| Requirement | Files/functions | Tests | Static | Compile/runtime |
|---|---|---|---|---|
| HSBI-CATCHUP-002 | AllocationPolicyTypes; ReserveCatchUpEvaluator | T161-T171 | IMPLEMENTED_UNVERIFIED | USER_VERIFICATION_REQUIRED |
| HSBI-FS-005 | FutureSmallLevelDigest; FutureSmallProofDigest | T172-T180 | IMPLEMENTED_UNVERIFIED | USER_VERIFICATION_REQUIRED |
| HSBI-FS-006 | FutureSmallLevelMarketSnapshot; level market validator | T181-T185 | IMPLEMENTED_UNVERIFIED | USER_VERIFICATION_REQUIRED |
| HSBI-FS-007 | FutureSmallLevelCostSnapshot; level cost validator | T186 | IMPLEMENTED_UNVERIFIED | USER_VERIFICATION_REQUIRED |
| HSBI-FS-008 | FutureFarProjection; explicit projection source | T187-T191 | IMPLEMENTED_UNVERIFIED | USER_VERIFICATION_REQUIRED |
| HSBI-RISK-002 | FutureSmallRiskEvaluator; runtime/proxy separation | T192-T195 | IMPLEMENTED_UNVERIFIED | USER_VERIFICATION_REQUIRED |
| HSBI-NF-011 | complete candidate proof/digest isolation | T196-T200 | IMPLEMENTED_UNVERIFIED | USER_VERIFICATION_REQUIRED |

Все R2-строки имеют только статический статус. MetaEditor compile, MQL5 runtime, broker-money runtime и risk runtime proof требуют evidence администратора.

## HSB.2B-R3 — multi-level aggregation и allocation consumption

| Requirement | Files/functions | Tests | Static | Compile/runtime |
|---|---|---|---|---|
| HSBI-FS-009 | FutureSmallProofAggregator; HSBI_AggregateFutureSmallProof | T201-T220,T246-T252,T261 | IMPLEMENTED_UNVERIFIED | USER_VERIFICATION_REQUIRED |
| HSBI-NF-012 | aggregate NewFar gates; complete candidate proof | T204,T213-T218,T262-T263 | IMPLEMENTED_UNVERIFIED | USER_VERIFICATION_REQUIRED |
| HSBI-MONEY-023 | MoneyProofIdentity; Reserve/Far proof validators | T221-T234,T253,T259-T260 | IMPLEMENTED_UNVERIFIED | USER_VERIFICATION_REQUIRED |
| HSBI-ALLOC-002 | ReserveAllocationSource conservation | T235-T239,T254,T258 | IMPLEMENTED_UNVERIFIED | USER_VERIFICATION_REQUIRED |
| HSBI-ALLOC-003 | ReserveConsumptionKey duplicate/conflict guards | T240-T245,T255-T257 | IMPLEMENTED_UNVERIFIED | USER_VERIFICATION_REQUIRED |
| HSBI-CATCHUP-003 | independent source proofs and double-count guard | T237-T245,T258-T260 | IMPLEMENTED_UNVERIFIED | USER_VERIFICATION_REQUIRED |

Runtime-confirmed flags are mandatory in the static contract, but actual broker/risk runtime evidence remains `USER_VERIFICATION_REQUIRED`.

## HSB.2C — static orchestration

Сводная traceability HSB.2C находится в `Docs/HSB.2C_Traceability.md`. Требования HSBI-INTENT-001, PREFLIGHT-001, LIFECYCLE-001, JOURNAL-001, IDEMP-001, PERSIST-002 и RECON-002 покрыты T266–T340. Compile/runtime evidence: `USER_VERIFICATION_REQUIRED`; production trading: `NOT_IMPLEMENTED`.

## HSB.2C-R1

Подробная mapping-таблица находится в `Docs/HSB.2C_R1_Traceability_RU.md`. Intent/snapshot/journal/runtime guards покрыты T341–T380; runtime evidence остаётся `USER_VERIFICATION_REQUIRED`.
