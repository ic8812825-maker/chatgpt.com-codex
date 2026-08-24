# HSB.2E PREP-R4-R4 — monotonic implementation handoff

Это только план административной проверки: `TRADING_LOGIC_START_ALLOWED=NO`. Будущие owner-файлы не создаются в R4-R4.

## Mapping Python/JSON → MQL5

| Python/JSON | MQL5 | Ограничение |
|---|---|---|
| identifier string | `string` | nonempty, trimmed, max 128 |
| revision integer | `long/ulong` | integer, state >= 0, version > 0 |
| broker ticket | `ulong` | positive, lossless |
| Decimal money | scaled `long` + currency digits | exact rounding, no hidden float epsilon |
| Boolean | `bool` | only `true/false` |
| enum string | exhaustive MQL5 enum | unknown rejected |

Для IMPL-01…IMPL-17 из предыдущего handoff сохраняются точные owner paths. Каждый блок обязан реализовать структуры `HSBI_*DTO`, enum `HSBI_Status/HSBI_Reason`, сигнатуры pure `Validate*/Evaluate*`, allowed includes только предыдущих блоков, forbidden includes `Trade/Trade.mqh`, `OrderSend`, `OrderSendAsync`, `CTrade`; precondition — validated immutable DTO; postcondition — immutable result; persistence/restart — согласно proof registry. Acceptance: compile-only плюс соответствующие R4 vectors, invariants, tests и real mutations.

| Блок | Точный owner | Структуры/функции | Persistence/restart | Acceptance |
|---|---|---|---|---|
| IMPL-01 | `Include/HSB2E/HSBI_IdentityTypes.mqh` | identity DTO/enums | canonical serialization | R4 identity proofs |
| IMPL-02 | `Include/HSB2E/HSBI_PrimitiveValidators.mqh` | `ValidateBoolean/Identifier/Revision/Price/Volume` | none | primitive vectors/mutations |
| IMPL-03 | `Include/HSB2E/HSBI_PositionOwnership.mqh` | `ValidatePositionContext` | snapshot digest | ownership proofs |
| IMPL-04 | `Include/HSB2E/HSBI_IntentBinding.mqh` | `ValidateIntentBindings` | intent digest | one-to-one proof |
| IMPL-05 | `Include/HSB2E/HSBI_DealEventRegistry.mqh` | bijective registry/consume-once | consumed/seen/bindings | exactly-once proofs |
| IMPL-06 | `Include/HSB2E/HSBI_FreshnessValidator.mqh` | deterministic window | window snapshot | timestamp proofs |
| IMPL-07 | `Include/HSB2E/HSBI_ScenarioSchema.mqh` | required roles | schema decision | leg proofs |
| IMPL-08 | `Include/HSB2E/HSBI_FillAccounting.mqh` | per-ticket cumulative fill | partial evidence | fill/restart proofs |
| IMPL-09 | `Include/HSB2E/HSBI_SettlementProposal.mqh` | immutable proposal | proposal digest | conservation proofs |
| IMPL-10 | `Include/HSB2E/HSBI_SettlementPersistence.mqh` | persistence DTO | ordered records | ordering proof |
| IMPL-11 | `Include/HSB2E/HSBI_RestartReconciliation.mqh` | `RestartReconcile` | idempotent lifecycle | restart sequence |
| IMPL-12 | `Include/HSB2E/HSBI_InitialLockPure.mqh` | pure Initial | proposal only | Initial vectors |
| IMPL-13 | `Include/HSB2E/HSBI_BigPure.mqh` | pure Big | proposal only | Big vectors |
| IMPL-14 | `Include/HSB2E/HSBI_SmallFarPure.mqh` | pure Small/Far | proposal only | no-dual-tail |
| IMPL-15 | `Include/HSB2E/HSBI_TransactionBarrier.mqh` | `AdmitTransaction` | decision before mutation | barrier proof |
| IMPL-16 | `Include/HSB2E/HSBI_FsmCommit.mqh` | `CommitStateRevision` | revision +1/idempotence | revision proofs |
| IMPL-17 | `Include/HSB2E/HSBI_DisabledBrokerAdapter.mqh` | always-disabled adapter | no broker state | separate admin review |
