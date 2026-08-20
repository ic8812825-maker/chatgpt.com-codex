# HSB.2E точные API-контракты

Все типы и функции закреплены machine-readable JSON.

## Типы

| Type | Owner | Fields |
|---|---|---|
| HSBI_IBrokerAdapterRequest | Include/Broker/HSBI_IBrokerAdapter.mqh | cycleId:ulong; actionId:ulong |
| HSBI_BrokerSnapshotRequest | Include/Broker/HSBI_BrokerSnapshot.mqh | cycleId:ulong; actionId:ulong |
| HSBI_TradeRequestBuilderRequest | Include/Broker/HSBI_TradeRequestBuilder.mqh | cycleId:ulong; actionId:ulong |
| HSBI_TradeRetcodeClassifierRequest | Include/Broker/HSBI_TradeRetcodeClassifier.mqh | cycleId:ulong; actionId:ulong |
| HSBI_DealHistoryReaderRequest | Include/Broker/HSBI_DealHistoryReader.mqh | cycleId:ulong; actionId:ulong |
| HSBI_AtomicFileStoreRequest | Include/Persistence/HSBI_AtomicFileStore.mqh | cycleId:ulong; actionId:ulong |
| HSBI_ProductionJournalRequest | Include/Persistence/HSBI_ProductionJournal.mqh | cycleId:ulong; actionId:ulong |
| HSBI_ProductionSnapshotStoreRequest | Include/Persistence/HSBI_ProductionSnapshotStore.mqh | cycleId:ulong; actionId:ulong |
| HSBI_SnapshotMigrationRequest | Include/Persistence/HSBI_SnapshotMigration.mqh | cycleId:ulong; actionId:ulong |
| HSBI_ReconciliationEngineRequest | Include/Reconciliation/HSBI_ReconciliationEngine.mqh | cycleId:ulong; actionId:ulong |
| HSBI_PositionReconcilerRequest | Include/Reconciliation/HSBI_PositionReconciler.mqh | cycleId:ulong; actionId:ulong |
| HSBI_DealReconcilerRequest | Include/Reconciliation/HSBI_DealReconciler.mqh | cycleId:ulong; actionId:ulong |
| HSBI_PendingActionReconcilerRequest | Include/Reconciliation/HSBI_PendingActionReconciler.mqh | cycleId:ulong; actionId:ulong |
| HSBI_PositionDiscoveryRequest | Include/Execution/HSBI_PositionDiscovery.mqh | cycleId:ulong; actionId:ulong |
| HSBI_TransactionEngineRequest | Include/Execution/HSBI_TransactionEngine.mqh | cycleId:ulong; actionId:ulong |
| HSBI_TradeTransactionRouterRequest | Include/Execution/HSBI_TradeTransactionRouter.mqh | cycleId:ulong; actionId:ulong |
| HSBI_ExecutionCoordinatorRequest | Include/Execution/HSBI_ExecutionCoordinator.mqh | cycleId:ulong; actionId:ulong |
| HSBI_SimulatedBrokerAdapterRequest | Include/Execution/HSBI_SimulatedBrokerAdapter.mqh | cycleId:ulong; actionId:ulong |
| HSBI_DemoBrokerAdapterRequest | Include/Execution/HSBI_DemoBrokerAdapter.mqh | cycleId:ulong; actionId:ulong |
| HSBI_ProductionEconomicLedgerRequest | Include/Money/HSBI_ProductionEconomicLedger.mqh | cycleId:ulong; actionId:ulong |
| HSBI_ProductionAllocationLedgerRequest | Include/Money/HSBI_ProductionAllocationLedger.mqh | cycleId:ulong; actionId:ulong |
| HSBI_RealizedDealMoneyRequest | Include/Money/HSBI_RealizedDealMoney.mqh | cycleId:ulong; actionId:ulong |
| HSBI_CycleOrchestratorRequest | Include/Runtime/HSBI_CycleOrchestrator.mqh | cycleId:ulong; actionId:ulong |
| HSBI_FsmCommitCoordinatorRequest | Include/Runtime/HSBI_FsmCommitCoordinator.mqh | cycleId:ulong; actionId:ulong |
| HSBI_TerminalSafeControllerRequest | Include/Runtime/HSBI_TerminalSafeController.mqh | cycleId:ulong; actionId:ulong |
| HSBI_InitialLockEngineRequest | Include/Scenarios/HSBI_InitialLockEngine.mqh | cycleId:ulong; actionId:ulong |
| HSBI_BigHarvestEngineRequest | Include/Scenarios/HSBI_BigHarvestEngine.mqh | cycleId:ulong; actionId:ulong |
| HSBI_PartialFarReserveEngineRequest | Include/Scenarios/HSBI_PartialFarReserveEngine.mqh | cycleId:ulong; actionId:ulong |
| HSBI_FinalCloseEngineRequest | Include/Scenarios/HSBI_FinalCloseEngine.mqh | cycleId:ulong; actionId:ulong |
| HSBI_SmallTransitionEngineRequest | Include/Scenarios/HSBI_SmallTransitionEngine.mqh | cycleId:ulong; actionId:ulong |
| HSBI_NewFarCatchUpEngineRequest | Include/Scenarios/HSBI_NewFarCatchUpEngine.mqh | cycleId:ulong; actionId:ulong |
| HSBI_ProductionDiagnosticsRequest | Include/Diagnostics/HSBI_ProductionDiagnostics.mqh | cycleId:ulong; actionId:ulong |

## Функции

| Function | Return | Owner | Failure | Idempotency |
|---|---|---|---|---|
| HSBI_IBrokerAdapter_Execute | HSBI_RuntimeDecisionResult | Include/Broker/HSBI_IBrokerAdapter.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_BrokerSnapshot_Execute | HSBI_RuntimeDecisionResult | Include/Broker/HSBI_BrokerSnapshot.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_TradeRequestBuilder_Execute | HSBI_RuntimeDecisionResult | Include/Broker/HSBI_TradeRequestBuilder.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_TradeRetcodeClassifier_Execute | HSBI_RuntimeDecisionResult | Include/Broker/HSBI_TradeRetcodeClassifier.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_DealHistoryReader_Execute | HSBI_RuntimeDecisionResult | Include/Broker/HSBI_DealHistoryReader.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_AtomicFileStore_Execute | HSBI_RuntimeDecisionResult | Include/Persistence/HSBI_AtomicFileStore.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_ProductionJournal_Execute | HSBI_RuntimeDecisionResult | Include/Persistence/HSBI_ProductionJournal.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_ProductionSnapshotStore_Execute | HSBI_RuntimeDecisionResult | Include/Persistence/HSBI_ProductionSnapshotStore.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_SnapshotMigration_Execute | HSBI_RuntimeDecisionResult | Include/Persistence/HSBI_SnapshotMigration.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_ReconciliationEngine_Execute | HSBI_RuntimeDecisionResult | Include/Reconciliation/HSBI_ReconciliationEngine.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_PositionReconciler_Execute | HSBI_RuntimeDecisionResult | Include/Reconciliation/HSBI_PositionReconciler.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_DealReconciler_Execute | HSBI_RuntimeDecisionResult | Include/Reconciliation/HSBI_DealReconciler.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_PendingActionReconciler_Execute | HSBI_RuntimeDecisionResult | Include/Reconciliation/HSBI_PendingActionReconciler.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_PositionDiscovery_Execute | HSBI_RuntimeDecisionResult | Include/Execution/HSBI_PositionDiscovery.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_TransactionEngine_Execute | HSBI_RuntimeDecisionResult | Include/Execution/HSBI_TransactionEngine.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_TradeTransactionRouter_Execute | HSBI_RuntimeDecisionResult | Include/Execution/HSBI_TradeTransactionRouter.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_ExecutionCoordinator_Execute | HSBI_RuntimeDecisionResult | Include/Execution/HSBI_ExecutionCoordinator.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_SimulatedBrokerAdapter_Execute | HSBI_RuntimeDecisionResult | Include/Execution/HSBI_SimulatedBrokerAdapter.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_DemoBrokerAdapter_Execute | HSBI_RuntimeDecisionResult | Include/Execution/HSBI_DemoBrokerAdapter.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_ProductionEconomicLedger_Execute | HSBI_RuntimeDecisionResult | Include/Money/HSBI_ProductionEconomicLedger.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_ProductionAllocationLedger_Execute | HSBI_RuntimeDecisionResult | Include/Money/HSBI_ProductionAllocationLedger.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_RealizedDealMoney_Execute | HSBI_RuntimeDecisionResult | Include/Money/HSBI_RealizedDealMoney.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_CycleOrchestrator_Execute | HSBI_RuntimeDecisionResult | Include/Runtime/HSBI_CycleOrchestrator.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_FsmCommitCoordinator_Execute | HSBI_RuntimeDecisionResult | Include/Runtime/HSBI_FsmCommitCoordinator.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_TerminalSafeController_Execute | HSBI_RuntimeDecisionResult | Include/Runtime/HSBI_TerminalSafeController.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_InitialLockEngine_Execute | HSBI_RuntimeDecisionResult | Include/Scenarios/HSBI_InitialLockEngine.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_BigHarvestEngine_Execute | HSBI_RuntimeDecisionResult | Include/Scenarios/HSBI_BigHarvestEngine.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_PartialFarReserveEngine_Execute | HSBI_RuntimeDecisionResult | Include/Scenarios/HSBI_PartialFarReserveEngine.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_FinalCloseEngine_Execute | HSBI_RuntimeDecisionResult | Include/Scenarios/HSBI_FinalCloseEngine.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_SmallTransitionEngine_Execute | HSBI_RuntimeDecisionResult | Include/Scenarios/HSBI_SmallTransitionEngine.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_NewFarCatchUpEngine_Execute | HSBI_RuntimeDecisionResult | Include/Scenarios/HSBI_NewFarCatchUpEngine.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
| HSBI_ProductionDiagnostics_Execute | HSBI_RuntimeDecisionResult | Include/Diagnostics/HSBI_ProductionDiagnostics.mqh | HSBI_DECISION_CONFLICT/HSBI_RD_RECONCILIATION_CONFLICT | cycleId+actionId+inputDigest |
