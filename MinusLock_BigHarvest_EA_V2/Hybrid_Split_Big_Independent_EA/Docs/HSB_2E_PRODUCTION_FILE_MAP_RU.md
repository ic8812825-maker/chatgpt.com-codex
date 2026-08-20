# HSB.2E production file map

Проектируемые production-файлы отсутствуют до разрешения этапа.

| FILE | PUBLIC FUNCTION | DEPENDENCIES | STATE MUTATION | BROKER CALLS | STAGE |
|---|---|---|---|---|---|
| Include/Broker/HSBI_IBrokerAdapter.mqh | HSBI_IBrokerAdapter_Execute | Core + Runtime contracts | NO | NO | HSB.2E.0 |
| Include/Broker/HSBI_BrokerSnapshot.mqh | HSBI_BrokerSnapshot_Execute | Core + Runtime contracts | NO | NO | HSB.2E.1 |
| Include/Broker/HSBI_TradeRequestBuilder.mqh | HSBI_TradeRequestBuilder_Execute | Core + Runtime contracts | NO | NO | HSB.2E.2 |
| Include/Broker/HSBI_TradeRetcodeClassifier.mqh | HSBI_TradeRetcodeClassifier_Execute | Core + Runtime contracts | NO | NO | HSB.2E.3 |
| Include/Broker/HSBI_DealHistoryReader.mqh | HSBI_DealHistoryReader_Execute | Core + Runtime contracts | NO | NO | HSB.2E.4 |
| Include/Persistence/HSBI_AtomicFileStore.mqh | HSBI_AtomicFileStore_Execute | Core + Runtime contracts | NO | NO | HSB.2E.5 |
| Include/Persistence/HSBI_ProductionJournal.mqh | HSBI_ProductionJournal_Execute | Core + Runtime contracts | NO | NO | HSB.2E.6 |
| Include/Persistence/HSBI_ProductionSnapshotStore.mqh | HSBI_ProductionSnapshotStore_Execute | Core + Runtime contracts | NO | NO | HSB.2E.7 |
| Include/Persistence/HSBI_SnapshotMigration.mqh | HSBI_SnapshotMigration_Execute | Core + Runtime contracts | NO | NO | HSB.2E.8 |
| Include/Reconciliation/HSBI_ReconciliationEngine.mqh | HSBI_ReconciliationEngine_Execute | Core + Runtime contracts | NO | NO | HSB.2E.9 |
| Include/Reconciliation/HSBI_PositionReconciler.mqh | HSBI_PositionReconciler_Execute | Core + Runtime contracts | NO | NO | HSB.2E.10 |
| Include/Reconciliation/HSBI_DealReconciler.mqh | HSBI_DealReconciler_Execute | Core + Runtime contracts | NO | NO | HSB.2E.11 |
| Include/Reconciliation/HSBI_PendingActionReconciler.mqh | HSBI_PendingActionReconciler_Execute | Core + Runtime contracts | NO | NO | HSB.2E.12 |
| Include/Execution/HSBI_PositionDiscovery.mqh | HSBI_PositionDiscovery_Execute | Core + Runtime contracts | NO | NO | HSB.2E.13 |
| Include/Execution/HSBI_TransactionEngine.mqh | HSBI_TransactionEngine_Execute | Core + Runtime contracts | NO | NO | HSB.2E.14 |
| Include/Execution/HSBI_TradeTransactionRouter.mqh | HSBI_TradeTransactionRouter_Execute | Core + Runtime contracts | NO | NO | HSB.2E.15 |
| Include/Execution/HSBI_ExecutionCoordinator.mqh | HSBI_ExecutionCoordinator_Execute | Core + Runtime contracts | NO | NO | HSB.2E.16 |
| Include/Execution/HSBI_SimulatedBrokerAdapter.mqh | HSBI_SimulatedBrokerAdapter_Execute | Core + Runtime contracts | NO | SIMULATED_ONLY | HSB.2E.0 |
| Include/Execution/HSBI_DemoBrokerAdapter.mqh | HSBI_DemoBrokerAdapter_Execute | Core + Runtime contracts | NO | DEMO_AFTER_2E13 | HSB.2E.1 |
| Include/Money/HSBI_ProductionEconomicLedger.mqh | HSBI_ProductionEconomicLedger_Execute | Core + Runtime contracts | NO | NO | HSB.2E.2 |
| Include/Money/HSBI_ProductionAllocationLedger.mqh | HSBI_ProductionAllocationLedger_Execute | Core + Runtime contracts | NO | NO | HSB.2E.3 |
| Include/Money/HSBI_RealizedDealMoney.mqh | HSBI_RealizedDealMoney_Execute | Core + Runtime contracts | NO | NO | HSB.2E.4 |
| Include/Runtime/HSBI_CycleOrchestrator.mqh | HSBI_CycleOrchestrator_Execute | Core + Runtime contracts | ONLY_RECONCILED_COMMIT | NO | HSB.2E.5 |
| Include/Runtime/HSBI_FsmCommitCoordinator.mqh | HSBI_FsmCommitCoordinator_Execute | Core + Runtime contracts | ONLY_RECONCILED_COMMIT | NO | HSB.2E.6 |
| Include/Runtime/HSBI_TerminalSafeController.mqh | HSBI_TerminalSafeController_Execute | Core + Runtime contracts | ONLY_RECONCILED_COMMIT | NO | HSB.2E.7 |
| Include/Scenarios/HSBI_InitialLockEngine.mqh | HSBI_InitialLockEngine_Execute | Core + Runtime contracts | NO | NO | HSB.2E.8 |
| Include/Scenarios/HSBI_BigHarvestEngine.mqh | HSBI_BigHarvestEngine_Execute | Core + Runtime contracts | NO | NO | HSB.2E.9 |
| Include/Scenarios/HSBI_PartialFarReserveEngine.mqh | HSBI_PartialFarReserveEngine_Execute | Core + Runtime contracts | NO | NO | HSB.2E.10 |
| Include/Scenarios/HSBI_FinalCloseEngine.mqh | HSBI_FinalCloseEngine_Execute | Core + Runtime contracts | NO | NO | HSB.2E.11 |
| Include/Scenarios/HSBI_SmallTransitionEngine.mqh | HSBI_SmallTransitionEngine_Execute | Core + Runtime contracts | NO | NO | HSB.2E.12 |
| Include/Scenarios/HSBI_NewFarCatchUpEngine.mqh | HSBI_NewFarCatchUpEngine_Execute | Core + Runtime contracts | NO | NO | HSB.2E.13 |
| Include/Diagnostics/HSBI_ProductionDiagnostics.mqh | HSBI_ProductionDiagnostics_Execute | Core + Runtime contracts | NO | NO | HSB.2E.14 |
