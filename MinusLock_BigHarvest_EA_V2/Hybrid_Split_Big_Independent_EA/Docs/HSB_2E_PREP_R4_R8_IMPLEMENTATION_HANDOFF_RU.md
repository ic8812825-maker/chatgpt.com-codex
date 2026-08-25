# HSB.2E PREP-R4-R8 — implementation handoff

R4-R8 остаётся offline executable specification. Production owners и broker dispatch не созданы.

## Transaction barrier

`Broker evidence → Validation → Fill classification → Broker proposal → Economic formula authority → Allocation → Persistence → FSM commit`.

| Future owner | Immutable DTO / API | Preconditions | Postconditions / reasons | R4-R8 proof | Persistence / restart / forbidden |
|---|---|---|---|---|---|
| `Include/Evidence/HSBI_RuntimeContext.mqh` | RuntimeContext / `ValidateContext` | sealed account, symbol, magic, cycle, broker grids | exact identity or fail-closed | `HSBI_RuntimeContext`, oracle rows, `R8_SNAPSHOT_CONTEXT_IDENTITY` | persist broker properties; no trade API |
| `Include/Evidence/HSBI_PriceAuthority.mqh` | Snapshot, PricePolicy / `ValidateExecutionPrice` | registered policy and normative Bid/Ask | bounded tick-grid price or authority reason | `validate_price_result`, price vectors, price mutations | replay snapshot/policy; no self-asserted bounds |
| `Include/Settlement/HSBI_FillClassifier.mqh` | Deal ledger / `ClassifyFill` | bound exactly-once deals | eight fill classes; overfill reconciliation | `classify_fill`, fill adversarial, fill mutations | reconciliation separate from settlement money |
| `Include/Economics/HSBI_FormulaRegistry.mqh` | EconomicPolicy / `ExecuteFormula` | nonempty registered IDs, broker grids | conserved Decimal proposal | `validate_economic_policy_result`, economic oracle/mutations | persist formula version/source; no broker calls |
| `Include/Persistence/HSBI_CommitBundle.mqh` | five source objects / `PersistBundle` | source recomputation succeeds | persistence before FSM | `validate_commit_replay`, 18 certificate cases | all source objects required on restart |
| `Include/FSM/HSBI_CommitBarrier.mqh` | Certificate / `ReplayOrCommit` | certificate version and three revision chains | exactly-once or exact reject reason | certificate matrix, revision invariants/mutations | state/evidence/settlement revisions rebound |
| `Include/Broker/HSBI_BrokerAdapter.mqh` | future adapter | separate written authorization | HARD_DISABLED | no R4-R8 production implementation | forbidden dependencies and dispatch |

Каждый owner обязан сохранить соответствующие oracle rows, positive/negative/metamorphic vectors, property invariant, unique mutation, reason codes и restart semantics без ослабления.
