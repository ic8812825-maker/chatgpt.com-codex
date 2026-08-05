# Этап 3.1.6.3.16 — итоговая матрица MQL5 mapping Hybrid Split Big

| Requirement | MQL5 mapping | Runtime/FSM | Actual deal confirmation | Persistence | Reconciliation | Status | Критичность |
|---|---|---|---|---|---|---|---|
| Initial Lock open | `OpenInitialLock`, `OpenPosition` | Legacy/common, STATE_IDLE | synchronous only | partial | partial | MAPPED_PARTIAL | P1 |
| Rollback second-leg failure | Initial rollback close | common | synchronous only | limited | polling | MAPPED_PARTIAL | P1 |
| Initial Profit exclusion | history comment skip + context flags | recovery stats | history scan | yes fields | partial | MAPPED_PARTIAL | P1 |
| Far assignment | `ConvertInitialLockToFar` | compatibility transition | no event barrier | yes | partial | MAPPED_PARTIAL | P1 |
| CandidatePlan | `EvaluateHybridCandidate` | Hybrid preview | N/A | incomplete | N/A | MAPPED_PARTIAL | P1 |
| BigCore open | Split open core state | Split+Hybrid modifier | synchronous only | yes fields | partial | MAPPED_PARTIAL | P1 |
| BigTrend open | Split open trend state | Split+Hybrid modifier | synchronous only | yes fields | partial | MAPPED_PARTIAL | P1 |
| SmallBase open | Split open base state | Split+Hybrid modifier | synchronous only | yes fields | partial | MAPPED_PARTIAL | P1 |
| Big Harvest trigger | Split Big target handlers | Split+Hybrid modifier | N/A | state | partial | MAPPED_PARTIAL | P1 |
| BigCore close | Split close phase | mixed | synchronous/history | pending fields | partial | MAPPED_PARTIAL | P1 |
| BigTrend close | Split close phase | mixed | synchronous/history | pending fields | partial | MAPPED_PARTIAL | P1 |
| SmallBase close | Split close phase | mixed | synchronous/history | pending fields | partial | MAPPED_PARTIAL | P1 |
| Realized DealNet | history helpers | mixed | post-factum | partial ledger | partial | MAPPED_PARTIAL | P1 |
| Allocation | Reserve transaction + budgets | mixed | not unified with deal event | yes reserve tx | partial | MAPPED_PARTIAL | P1 |
| Immediate Final Close | multiple routes/gates | Legacy/Split/Hybrid | synchronous/history | partial | partial | CONFLICTING | P1 |
| Partial Far | close lot + actual volume refresh | mixed | synchronous/history | pending/budget fields | partial | MAPPED_PARTIAL | P1 |
| Next level | StateMachine | Legacy/Split | no event barrier | state | periodic | MAPPED_PARTIAL | P1 |
| Small trigger | `EvaluateCurrentSmallPreTrade` | Split+Hybrid | N/A | plan saved | partial | MAPPED_PARTIAL | P1 |
| OldFar full close | `ProcessSplitSmallCloseOldFar` | Split+Hybrid | wrapper + immediate verify | yes | local audit | MAPPED_PARTIAL | P1 |
| BigCore staged close | `ProcessSplitSmallCloseCorePart` | Split+Hybrid | wrapper + position read | yes | local audit | MAPPED_PARTIAL | P1 |
| Actual NewFar | actual remaining BigCore promoted | Hybrid branch | position polling | yes | one-position check | MAPPED_AND_ACTIVE | P1 safety |
| Persistence | Global Variables | all modes | N/A | non-atomic | restart checks | MAPPED_PARTIAL | P1 |
| Restart | `RecoverState` | all modes | history/position scan | yes | yes partial | MAPPED_PARTIAL | P1 |
| Reconciliation | `RunReconciliation`, periodic | all modes | no transaction event | yes | partial | MAPPED_PARTIAL | P1 |
| Terminal-safe | error/manual/emergency states | mixed | varies | yes | varies | MAPPED_PARTIAL | P1 |
| Multi-symbol isolation | `_Symbol`, Magic and state key | common | partial | symbol-scoped | partial | MAPPED_PARTIAL | P0 |
| Symbol+Magic+CycleID+identifier | distributed checks | mixed | not atomic in TradeEngine | partial | partial | NOT_FULLY_MAPPED | P0 |
| OnTradeTransaction | absent | none | absent | absent | absent | NOT_MAPPED | P1 |
| StateRevision bound execution | incomplete | none unified | absent | incomplete | incomplete | NOT_MAPPED | P1 |

## Сводка

```text
MAPPED_AND_ACTIVE=1
MAPPED_PARTIAL=24
CONFLICTING=1
NOT_MAPPED_OR_NOT_FULLY_MAPPED=3
PRODUCTION_MQL5_MAPPING=AUDITED
PRODUCTION_MQL5_READY=NO
```

Главный вывод: Hybrid geometry и actual NewFar partially active; полный нормативный production lifecycle не подключён.
