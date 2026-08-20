# HSB.2E-PREP-R2 — semantic API и ownership contracts

Production-файлы ниже являются только проектируемыми и в этом этапе отсутствуют. Каждый input включает account/symbol/magic/cycle/action и уникальное component-specific поле; output всегда содержит status/reason/digest.

| Owner | Component field | Function | Tests |
|---|---|---|---|
| `Include/Broker/HSBI_IBrokerAdapter.mqh` | `broker_identity` | `HSBI_IBrokerAdapter_Evaluate` | T465, T497 |
| `Include/Broker/HSBI_BrokerSnapshot.mqh` | `snapshot_time` | `HSBI_BrokerSnapshot_Evaluate` | T466, T498 |
| `Include/Broker/HSBI_TradeRequestBuilder.mqh` | `request_volume` | `HSBI_TradeRequestBuilder_Evaluate` | T467, T499 |
| `Include/Broker/HSBI_TradeRetcodeClassifier.mqh` | `retcode` | `HSBI_TradeRetcodeClassifier_Evaluate` | T468, T500 |
| `Include/Broker/HSBI_DealHistoryReader.mqh` | `deal_ticket` | `HSBI_DealHistoryReader_Evaluate` | T469, T501 |
| `Include/Persistence/HSBI_AtomicFileStore.mqh` | `atomic_digest` | `HSBI_AtomicFileStore_Evaluate` | T470, T502 |
| `Include/Persistence/HSBI_ProductionJournal.mqh` | `journal_sequence` | `HSBI_ProductionJournal_Evaluate` | T471, T503 |
| `Include/Persistence/HSBI_ProductionSnapshotStore.mqh` | `snapshot_version` | `HSBI_ProductionSnapshotStore_Evaluate` | T472, T504 |
| `Include/Persistence/HSBI_SnapshotMigration.mqh` | `migration_version` | `HSBI_SnapshotMigration_Evaluate` | T473, T505 |
| `Include/Reconciliation/HSBI_ReconciliationEngine.mqh` | `reconciliation_digest` | `HSBI_ReconciliationEngine_Evaluate` | T474, T506 |
| `Include/Reconciliation/HSBI_PositionReconciler.mqh` | `position_ticket` | `HSBI_PositionReconciler_Evaluate` | T475, T507 |
| `Include/Reconciliation/HSBI_DealReconciler.mqh` | `deal_id` | `HSBI_DealReconciler_Evaluate` | T476, T508 |
| `Include/Reconciliation/HSBI_PendingActionReconciler.mqh` | `pending_action_id` | `HSBI_PendingActionReconciler_Evaluate` | T477, T509 |
| `Include/Execution/HSBI_PositionDiscovery.mqh` | `ownership_filter` | `HSBI_PositionDiscovery_Evaluate` | T478, T510 |
| `Include/Execution/HSBI_TransactionEngine.mqh` | `transaction_state` | `HSBI_TransactionEngine_Evaluate` | T479, T511 |
| `Include/Execution/HSBI_TradeTransactionRouter.mqh` | `event_id` | `HSBI_TradeTransactionRouter_Evaluate` | T480, T512 |
| `Include/Execution/HSBI_ExecutionCoordinator.mqh` | `barrier_state` | `HSBI_ExecutionCoordinator_Evaluate` | T481, T513 |
| `Include/Execution/HSBI_SimulatedBrokerAdapter.mqh` | `dispatch_mode` | `HSBI_SimulatedBrokerAdapter_Evaluate` | T482, T514 |
| `Include/Execution/HSBI_DemoBrokerAdapter.mqh` | `account_currency` | `HSBI_DemoBrokerAdapter_Evaluate` | T483, T515 |
| `Include/Money/HSBI_ProductionEconomicLedger.mqh` | `allocation_id` | `HSBI_ProductionEconomicLedger_Evaluate` | T484, T516 |
| `Include/Money/HSBI_ProductionAllocationLedger.mqh` | `realized_pnl` | `HSBI_ProductionAllocationLedger_Evaluate` | T485, T517 |
| `Include/Money/HSBI_RealizedDealMoney.mqh` | `fsm_state` | `HSBI_RealizedDealMoney_Evaluate` | T486, T518 |
| `Include/Runtime/HSBI_CycleOrchestrator.mqh` | `state_revision` | `HSBI_CycleOrchestrator_Evaluate` | T487, T519 |
| `Include/Runtime/HSBI_FsmCommitCoordinator.mqh` | `terminal_safe_reason` | `HSBI_FsmCommitCoordinator_Evaluate` | T488, T520 |
| `Include/Runtime/HSBI_TerminalSafeController.mqh` | `initial_pair` | `HSBI_TerminalSafeController_Evaluate` | T489, T521 |
| `Include/Scenarios/HSBI_InitialLockEngine.mqh` | `big_level` | `HSBI_InitialLockEngine_Evaluate` | T490, T522 |
| `Include/Scenarios/HSBI_BigHarvestEngine.mqh` | `close_far_budget` | `HSBI_BigHarvestEngine_Evaluate` | T491, T523 |
| `Include/Scenarios/HSBI_PartialFarReserveEngine.mqh` | `recovery_pl` | `HSBI_PartialFarReserveEngine_Evaluate` | T492, T524 |
| `Include/Scenarios/HSBI_FinalCloseEngine.mqh` | `reversal_count` | `HSBI_FinalCloseEngine_Evaluate` | T493, T525 |
| `Include/Scenarios/HSBI_SmallTransitionEngine.mqh` | `new_far_ticket` | `HSBI_SmallTransitionEngine_Evaluate` | T494, T526 |
| `Include/Scenarios/HSBI_NewFarCatchUpEngine.mqh` | `log_event` | `HSBI_NewFarCatchUpEngine_Evaluate` | T495, T527 |
| `Include/Diagnostics/HSBI_ProductionDiagnostics.mqh` | `diagnostic_severity` | `HSBI_ProductionDiagnostics_Evaluate` | T496, T528 |
