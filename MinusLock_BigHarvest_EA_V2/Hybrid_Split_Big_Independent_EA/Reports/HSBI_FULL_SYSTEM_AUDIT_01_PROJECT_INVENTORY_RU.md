# Карта проекта HSBI

BASE_SHA=4185b84f7a6a8847f6a9c5796f07113907be447d

Режим READ-ONLY ANALYSIS + AUDIT/TEST-ONLY. Источники не изменены. **AUDIT_COMPLETENESS=PARTIAL.** Native MQL5/MT5/broker/durable execution NOT_RUN. Proposed R0A–R0H не становятся нормативом из-за тестовых PASS. Все административные разрешения остаются NO.

Из Git tree baseline независимо получено **1361 файлов**, production **74**, строки по splitlines **1812** (wc -l отличается для файлов без завершающего LF), определений функций **199**. Docs/root index **133**, Reports **226**, existing Python test scripts **279**. SHA256/blob/mode каждого baseline-file — INVENTORY/PRESERVATION.

| Production module | Lines | Functions | EA use | Issues |
|---|---|---|---|---|
| Hybrid_Split_Big_Independent_EA.mq5 | 44 | 4 | ENTRY_REACHABLE_FUNCTIONS | FSA-014 |
| Include/Core/HSBI_Context.mqh | 60 | 6 | ENTRY_REACHABLE_FUNCTIONS | FSA-009 |
| Include/Core/HSBI_Enums.mqh | 11 | 0 | INCLUDED_NOT_ENTRY_CALLED | No absence-of-defect claim |
| Include/Core/HSBI_Identifiers.mqh | 24 | 6 | INCLUDED_NOT_ENTRY_CALLED | No absence-of-defect claim |
| Include/Core/HSBI_Invariants.mqh | 14 | 9 | INCLUDED_NOT_ENTRY_CALLED | No absence-of-defect claim |
| Include/Core/HSBI_ReasonCodes.mqh | 5 | 1 | ENTRY_REACHABLE_FUNCTIONS | No absence-of-defect claim |
| Include/Core/HSBI_Roles.mqh | 11 | 5 | ENTRY_REACHABLE_FUNCTIONS | No absence-of-defect claim |
| Include/Core/HSBI_RuntimeMode.mqh | 7 | 1 | INCLUDED_NOT_ENTRY_CALLED | No absence-of-defect claim |
| Include/Core/HSBI_RuntimePolicy.mqh | 30 | 6 | ENTRY_REACHABLE_FUNCTIONS | No absence-of-defect claim |
| Include/Core/HSBI_StateMachine.mqh | 11 | 6 | INCLUDED_NOT_ENTRY_CALLED | FSA-012,FSA-022 |
| Include/Core/HSBI_StateValidator.mqh | 6 | 2 | INCLUDED_NOT_ENTRY_CALLED | No absence-of-defect claim |
| Include/Core/HSBI_Types.mqh | 8 | 1 | INCLUDED_NOT_ENTRY_CALLED | No absence-of-defect claim |
| Include/Core/HSBI_Version.mqh | 12 | 0 | INCLUDED_NOT_ENTRY_CALLED | No absence-of-defect claim |
| Include/Diagnostics/HSBI_Diagnostics.mqh | 7 | 2 | ENTRY_REACHABLE_FUNCTIONS | No absence-of-defect claim |
| Include/Diagnostics/HSBI_Logger.mqh | 7 | 1 | ENTRY_REACHABLE_FUNCTIONS | No absence-of-defect claim |
| Include/Diagnostics/HSBI_PanelModel.mqh | 6 | 1 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Execution/HSBI_ActionTypes.mqh | 8 | 2 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Execution/HSBI_EventTypes.mqh | 8 | 2 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Execution/HSBI_ExecutionIntent.mqh | 45 | 7 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Execution/HSBI_ExecutionPreflight.mqh | 49 | 3 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Execution/HSBI_ExternalOutcome.mqh | 33 | 2 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Execution/HSBI_NoTradeExecution.mqh | 9 | 4 | ENTRY_REACHABLE_FUNCTIONS | No absence-of-defect claim |
| Include/Execution/HSBI_OwnershipGuardTypes.mqh | 17 | 3 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Execution/HSBI_TransactionTypes.mqh | 24 | 5 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | FSA-006 |
| Include/Money/HSBI_AllocationLedgerTypes.mqh | 11 | 5 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | FSA-002,FSA-007 |
| Include/Money/HSBI_AllocationPolicyTypes.mqh | 32 | 2 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Money/HSBI_BasketMoneyEvaluator.mqh | 29 | 3 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | FSA-029 |
| Include/Money/HSBI_BrokerMarginModel.mqh | 18 | 1 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Money/HSBI_BrokerMoneyModel.mqh | 22 | 2 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Money/HSBI_BrokerMoneyTypes.mqh | 20 | 2 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Money/HSBI_CandidateMoneyEvaluator.mqh | 28 | 1 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Money/HSBI_CatchUpModel.mqh | 17 | 1 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Money/HSBI_CatchUpTypes.mqh | 6 | 0 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Money/HSBI_CostModel.mqh | 20 | 3 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | FSA-019 |
| Include/Money/HSBI_EconomicLedgerTypes.mqh | 13 | 6 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | FSA-001 |
| Include/Money/HSBI_LevelMarginEvaluator.mqh | 13 | 1 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Money/HSBI_LevelMoneyEvaluator.mqh | 16 | 1 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Money/HSBI_MoneyProofIdentity.mqh | 30 | 3 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Money/HSBI_MoneyState.mqh | 6 | 1 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | FSA-008 |
| Include/Money/HSBI_MoneyTypes.mqh | 10 | 1 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Money/HSBI_ReserveAllocationTypes.mqh | 35 | 6 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Money/HSBI_ReserveCatchUpEvaluator.mqh | 83 | 4 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | FSA-003,FSA-004 |
| Include/Persistence/HSBI_ExecutionJournal.mqh | 45 | 6 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | FSA-027 |
| Include/Persistence/HSBI_ExecutionStateSnapshot.mqh | 44 | 5 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Persistence/HSBI_JournalTypes.mqh | 8 | 2 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Persistence/HSBI_PersistenceInterface.mqh | 8 | 1 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | FSA-013 |
| Include/Persistence/HSBI_ReconciliationTypes.mqh | 8 | 1 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Persistence/HSBI_SnapshotTypes.mqh | 11 | 3 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Planning/HSBI_BrokerGrid.mqh | 38 | 10 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Planning/HSBI_CandidatePlan.mqh | 9 | 3 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Planning/HSBI_ControlPrices.mqh | 25 | 6 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | FSA-021 |
| Include/Planning/HSBI_DecisionResult.mqh | 5 | 0 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Planning/HSBI_FutureSmallProofAggregator.mqh | 60 | 2 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | FSA-015 |
| Include/Planning/HSBI_FutureSmallSolver.mqh | 151 | 11 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | FSA-017,FSA-018,FSA-028 |
| Include/Planning/HSBI_FutureSmallTypes.mqh | 82 | 0 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Planning/HSBI_GeometrySolver.mqh | 38 | 3 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | FSA-011 |
| Include/Planning/HSBI_GeometryTypes.mqh | 7 | 0 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Planning/HSBI_NewFarCandidate.mqh | 42 | 4 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Planning/HSBI_NewFarSolver.mqh | 154 | 9 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | FSA-010,FSA-023 |
| Include/Risk/HSBI_CalculationGateTypes.mqh | 14 | 2 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Risk/HSBI_FutureSmallRiskEvaluator.mqh | 52 | 1 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Risk/HSBI_NewFarGateTypes.mqh | 18 | 1 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Risk/HSBI_RiskGateResult.mqh | 7 | 1 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | FSA-005 |
| Include/Risk/HSBI_RiskTypes.mqh | 5 | 0 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Runtime/HSBI_RuntimeDecisionTypes.mqh | 18 | 1 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Runtime/HSBI_RuntimeDecisionValidator.mqh | 30 | 3 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Runtime/HSBI_RuntimeRestartValidator.mqh | 18 | 1 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh | 19 | 1 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Scenarios/HSBI_BigHarvestTypes.mqh | 5 | 0 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Scenarios/HSBI_FinalCloseTypes.mqh | 5 | 0 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Scenarios/HSBI_InitialLockTypes.mqh | 5 | 0 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Scenarios/HSBI_PartialFarTypes.mqh | 5 | 0 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Scenarios/HSBI_ScenarioTypes.mqh | 6 | 0 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |
| Include/Scenarios/HSBI_SmallTransitionTypes.mqh | 5 | 0 | DORMANT_LIBRARY_NOT_INCLUDED_BY_EA | No absence-of-defect claim |

Основной вход Hybrid_Split_Big_Independent_EA.mq5:19/29/35/41. OnTradeTransaction отсутствует. Никаких input-параметров торгового профиля в main нет: конфигурация существует в DTO/документах, не в валидированном runtime loader. Functions/signatures/inputs/outputs/dependencies и line locators — REQUIREMENT_MATRIX.CodeToRequirement/ModuleReview и INVENTORY.Functions.

Все74 файла статически разобраны/рассмотрены; это не74 nativePASS и не покрытие всех веток. Только16 входят в main includeclosure,13 project functions консервативно достижимы из entry callbacks;58futureheaders не подключены главным EA. Included-but-uncalled отдельно от not-included; не предлагается автоматически удалить эти модули как deadcode. Подробная история и evidence индексируются отдельно HISTORICAL_INDEX, source/test inventory неизменны.
