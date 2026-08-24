# HSB.2E PREP-R4-R3 — исполнимый implementation handoff

Это план для отдельного административно разрешённого этапа. `TRADING_LOGIC_START_ALLOWED=NO`; production-файлы ниже ещё не создаются.

Для каждого блока действуют общие `FORBIDDEN_DEPENDENCIES=OrderSend,OrderSendAsync,CTrade,broker dispatch`, `OUTPUT_SCHEMA=status,reason,immutable DTO`, `ACCEPTANCE_COMMANDS=offline verifier + будущая compile-only проверка`.

| BLOCK_ID | OWNER_FILE | ALLOWED_DEPENDENCIES | PUBLIC_TYPES / PUBLIC_FUNCTIONS | INPUT_SCHEMA / STATUS_CODES / REASON_CODES | PRECONDITIONS / POSTCONDITIONS | INVARIANTS / VECTOR_IDS / TEST_IDS / MUTATION_IDS | PERSISTENCE_RECORDS / RESTART_BEHAVIOR |
|---|---|---|---|---|---|---|---|
| IMPL-01 | Include/HSB2E/HSBI_IdentityTypes.mqh | none | ContextIdentity,PositionIdentity,IntentIdentity,DealIdentity | R3 identity schemas; PASS/REJECT | immutable valid DTO | identity invariants; VALID_BIG; R3T001; R3M009-R3M014 | none; serialize identically |
| IMPL-02 | Include/HSB2E/HSBI_SchemaValidator.mqh | IMPL-01 | ValidateSchema | collections; REJECT/schema reasons | typed input / no exception | collection vectors; R3T036-R3T040; R3M031 | validation record; fail closed |
| IMPL-03 | Include/HSB2E/HSBI_PositionOwnership.mqh | IMPL-01,02 | ValidatePositionOwner | position snapshot | fresh owner / bound position | POSITION_CONTEXT; foreign position vectors; R3M013-R3M014 | snapshot digest; reconcile stale |
| IMPL-04 | Include/HSB2E/HSBI_IntentBinding.mqh | IMPL-01-03 | ValidateIntentBinding | intent DTO | one position/one intent | intent invariants; foreign intent vectors; R3M009-R3M012 | intent record; replay immutable |
| IMPL-05 | Include/HSB2E/HSBI_DealEventRegistry.mqh | IMPL-01-04 | DealEventRegistry,ConsumeOnce | deals/events | unique binding | exactly-once; DUP vectors; R3M001-R3M006 | consumed/seen/bindings; idempotent replay |
| IMPL-06 | Include/HSB2E/HSBI_FreshnessValidator.mqh | IMPL-01,02 | ValidateWindow | timestamps | fresh deterministic window | freshness invariant; timestamp vectors; R3M007-R3M008 | window snapshot; no wall clock |
| IMPL-07 | Include/HSB2E/HSBI_ScenarioSchema.mqh | IMPL-01-06 | ValidateRequiredLegs | scenario legs | exact roles | mandatory roles; missing/extra vectors; R3M015-R3M018 | schema decision; deterministic |
| IMPL-08 | Include/HSB2E/HSBI_FillAccounting.mqh | IMPL-01-07 | AggregatePerTicket | authoritative volumes | per-ticket fill | volume invariants; volume vectors; R3M024-R3M025 | cumulative fills; resume only new deals |
| IMPL-09 | Include/HSB2E/HSBI_SettlementProposal.mqh | IMPL-01-08 | BuildProposal | validated evidence | immutable proposal | conservation; VALID vectors; R3M027 | proposal digest; rebuild identical |
| IMPL-10 | Include/HSB2E/HSBI_SettlementPersistence.mqh | IMPL-01-09 | PersistEvidence | proposal | records before mutation | persistence invariants; R3M027 | fill, registry, decision records |
| IMPL-11 | Include/HSB2E/HSBI_RestartReconciliation.mqh | IMPL-01-10 | ReconcileReplay | persisted state | exactly once | restart invariants; restart vectors; R3M028-R3M030 | restore all ledgers; idempotent |
| IMPL-12 | Include/HSB2E/HSBI_InitialLockPure.mqh | IMPL-01-11 | EvaluateInitial | Initial schema | pure result | Initial vectors | proposal only |
| IMPL-13 | Include/HSB2E/HSBI_BigPure.mqh | IMPL-01-11 | EvaluateBig | Big schema | pure result | Big vectors; R3M015-R3M016 | proposal only |
| IMPL-14 | Include/HSB2E/HSBI_SmallFarPure.mqh | IMPL-01-11 | EvaluateSmallFar | Small/Far schema | no dual tail | Small vectors; R3M017 | proposal only |
| IMPL-15 | Include/HSB2E/HSBI_TransactionBarrier.mqh | IMPL-01-14 | AdmitSettlement | all proofs | atomic admission | barrier invariants; R3M027 | barrier decision before mutation |
| IMPL-16 | Include/HSB2E/HSBI_FsmCommit.mqh | IMPL-01-15 | CommitRevision | admitted settlement | revision +1 | revision invariant; R3M030 | commit record; replay idempotent |
| IMPL-17 | Include/HSB2E/HSBI_DisabledBrokerAdapter.mqh | IMPL-01-16 | DisabledDispatch | serialized intent | always disabled | no-trade checks | no broker state; hard-disabled |
