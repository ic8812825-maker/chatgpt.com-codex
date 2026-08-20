# HSB.2E future production file map

Все записи — проект, не реализация.

| FILE | OWNER_REQUIREMENTS | PUBLIC_TYPES | PUBLIC_FUNCTIONS | ALLOWED_DEPENDENCIES | FORBIDDEN_DEPENDENCIES | STATE_MUTATION_ALLOWED | BROKER_CALLS_ALLOWED | TEST_RANGE | IMPLEMENTATION_STAGE |
|---|---|---|---|---|---|---|---|---|---|
| Include/Persistence/HSBI_ProductionJournal.mqh | exactly-once | JournalRecord | Prepare/Append/Commit | Core | Broker, Scenarios | journal only | NO | T465–T499 | 2E.1 |
| Include/Broker/HSBI_BrokerSnapshot.mqh | runtime properties | BrokerSnapshot | ReadSnapshot | Core | FSM, Scenarios | NO | read-only | T500–T539 | 2E.2 |
| Include/Execution/HSBI_PositionDiscovery.mqh | ownership | PositionSet | Discover | Broker/Core | FSM | NO | read-only | T540–T579 | 2E.3 |
| Include/Reconciliation/HSBI_ReconciliationEngine.mqh | external truth | ReconcileResult | Reconcile | Core/Persistence | direct dispatch | result only | NO | T580–T619 | 2E.4 |
| Include/Execution/HSBI_TransactionEngine.mqh | lifecycle | Intent/Outcome | Prepare/ApplyOutcome | Persistence/Reconciliation | direct FSM mutation | intent only | simulated until 2E.13 | T620–T669 | 2E.5 |
| Include/Scenarios/HSBI_InitialLockEngine.mqh | Initial Lock | Decision | Decide | Core/Planning | Broker | NO | NO | T670–T709 | 2E.6 |
| Include/Scenarios/HSBI_BigHarvestEngine.mqh | Big | Decision | Decide | Planning/Money/Risk | Broker | NO | NO | T710–T759 | 2E.7 |
| Include/Scenarios/HSBI_PartialFarReserveEngine.mqh | Partial Far/Reserve | AllocationDecision | Decide | Money/Risk | Broker | NO | NO | T760–T809 | 2E.8 |
| Include/Scenarios/HSBI_FinalCloseEngine.mqh | Final Close | Decision | Decide | Money/Risk | Broker | NO | NO | T810–T849 | 2E.9 |
| Include/Scenarios/HSBI_SmallTransitionEngine.mqh | Small | Decision | Decide | Planning/Money/Risk | Broker | NO | NO | T850–T909 | 2E.10 |
| Include/Scenarios/HSBI_NewFarCatchUpEngine.mqh | NewFar/Catch-Up | Decision | Decide | Planning/Money/Risk | Broker | NO | NO | T910–T949 | 2E.11 |
| Include/Execution/HSBI_SimulatedBrokerAdapter.mqh | simulation | SimOutcome | Dispatch | Execution | FSM | adapter state | simulated only | T1000–T1049 | 2E.5 |
| Include/Diagnostics/HSBI_ProductionDiagnostics.mqh | audit | LogEvent | Emit | Core | Broker | NO | NO | all | 2E.0 |
