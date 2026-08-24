# HSB.2E PREP-R4-R7 — implementation handoff

Этап остаётся offline executable specification. Production MQL5 и broker adapter не созданы; последний остаётся hard-disabled.

## Граница транзакции

`Broker evidence → Validation → Fill accounting → Broker proposal → Economic proposal → Allocation → Persistence → FSM commit`.

| Будущий owner path | Immutable DTO / API | Preconditions и postconditions | Reference / proof | Persistence, restart, запреты |
|---|---|---|---|---|
| `Include/Evidence/HSBI_DealEvidence.mqh` | Deal, Snapshot, Policy / `ValidateDeal` | Полная identity, Bid/Ask policy; только bound record | `validate_binding`, price adversarial, `R7_SNAPSHOT_CONTEXT_BINDING` | sealed ledger; без trade API |
| `Include/Settlement/HSBI_FillAccounting.mqh` | BrokerProposal / `RecomputeFills` | exactly-once; volume conservation | `derive`, `broker_object`, source mutations | replay from deals; no caches as truth |
| `Include/Economics/HSBI_EconomicProposal.mqh` | EconomicPolicy, Proposal / `Calculate` | sealed policy; money conservation | `build_economic_proposal`, economic formulas | proposal persisted; no raw broker calls |
| `Include/Economics/HSBI_NewFar.mqh` | residual proof / `DeriveNewFar` | Big partial intent and confirmed fill | `big_residual`, `R7_NEW_FAR_VOLUME_CONSERVATION` | replay exact; no input residualVolume |
| `Include/Persistence/HSBI_CommitBundle.mqh` | six commit objects / `PersistBundle` | all source objects available | `pipeline`, certificate adversarial | persistence before FSM; fail closed |
| `Include/FSM/HSBI_SettlementBarrier.mqh` | Certificate / `CommitOnce` | output revision exactly +1 | `replay`, output-state recomputation | full restart validation; no dispatch |
| `Include/Broker/HSBI_BrokerAdapter.mqh` | future DTO adapter | separate administrative authorization | no R4-R7 implementation | HARD_DISABLED; `OrderSend*` forbidden |

## Обязательные причины fail-closed

`SNAPSHOT_CONTEXT_IDENTITY_MISMATCH`, `NORMATIVE_CLOSE_SIDE_MISMATCH`, `ORPHAN_DEAL`, `DEAL_ROLE_MISMATCH`, `DEAL_INTENT_BINDING_MISMATCH`, `BIG_VOLUME_CONSERVATION_FAILED`, `COMMIT_SOURCE_OBJECT_MISSING`, `COMMIT_PIPELINE_RECOMPUTATION_MISMATCH`.

Все public API должны переносить Decimal/grid semantics, immutable source objects, canonical digest, persistence-before-mutation и restart recomputation без ослабления.
