# Матрица требований и будущего MQL5 mapping

Версия 2.0 — HSB.0R.20. Статус: нормативный baseline, open P1 отсутствуют.

| Requirement/Decision | Owner document | Принятая норма | Будущий MQL5 module/function | Unit | Integration | Strategy Tester | Evidence | Status |
|---|---|---|---|---|---|---|---|---|
| HSBI-GEN-010 | 00/18 | Hybrid-only runtime | Core/RuntimeMode | dependency | init | all | charter | READY |
| HSBI-ID-010 | 02/07 | full ownership tuple | Execution/OwnershipGuard | foreign identity | close/open | multi-symbol | DEC-010 | READY |
| HSBI-MATH-014 | 04/23 | broker-money catch-up | Planning/CatchUpModel | money grid | basket | trend | DEC-001/003 | READY |
| HSBI-GEO-005 | 05/23 | all gates after rounding | Planning/GeometrySolver | coarse step | planning | min lot | DEC-001 | READY |
| HSBI-FSM-002 | 06/07 | advance after completed outcome | Core/StateMachine | transition guard | partial fill | delayed fill | P2 contract | READY |
| HSBI-INIT-002 | 09 | Initial Profit excluded | Scenarios/InitialLock | exclusion | rollback | both directions | money sync | READY |
| HSBI-BIG-003 | 10/08 | actual sources + exactly-once | Scenarios/BigHarvest | replay | allocation | trend | DEC-002 | READY |
| HSBI-PF-001 | 11/08 | Reserve forbidden | Scenarios/PartialFar | bucket isolation | partial fill | loss Far | DEC-002 | READY |
| HSBI-FC-001 | 12/23 | one money authority | Money/FinalCloseCalculator | threshold | basket close | costs | DEC-008 | READY |
| HSBI-SMALL-001 | 13/07 | confirmed sequential transition | Scenarios/SmallTransition | debounce | partial fills | reversals | DEC-005/007 | READY |
| HSBI-NF-001 | 14/23 | actual Core residual only | Planning/NewFarSolver | enumeration | transition | coarse grid | DEC-005 | READY |
| HSBI-MONEY-014 | 08/23 | Event/Consumption/Source keys | Money/Ledgers | duplicate | restart | replay | DEC-002 | READY |
| HSBI-TX-006 | 07/23 | OnTradeTransaction barrier | Execution/TransactionEngine | retcodes | fills | latency | P2 contract | READY |
| HSBI-PERSIST-001 | 16/23 | versioned file snapshot | Persistence/SnapshotStore | checksum | crash | restart | DEC-011 | READY |
| HSBI-RECON-002 | 17 | no guessed Far | Persistence/Reconciliation | conflict | restart | duplicate Far | DEC-010/011 | READY |
| HSBI-RISK-001 | 15/23 | money risk and fail-closed gates | Risk/BasketRisk | adverse price | margin | gap | DEC-003/009 | READY |
| HSBI-PROD-001 | 21/23 | explicit readiness + approval | Reports/Acceptance | gate set | demo | forward | DEC-012 | READY |
| HSBI-DEC-001 | 23 | ranges + research-only profile | Planning/GeometrySolver | ratios | plan | optimization | HSB_0R_DEC_001 | DEFERRED_WITH_SAFE_CONTRACT |
| HSBI-DEC-002 | 23 | configurable conserved shares | Money/AllocationLedger | conservation | harvest | replay | HSB_0R_DEC_002 | DEFERRED_WITH_SAFE_CONTRACT |
| HSBI-DEC-003 | 23 | typed fresh control prices | Planning/ControlPriceModel | sides | gates | spread | HSB_0R_DEC_003 | RESOLVED |
| HSBI-DEC-004 | 23 | recursive Future Small + bound | Planning/FutureSmall | recursion | solver | reversals | HSB_0R_DEC_004 | RESOLVED |
| HSBI-DEC-005 | 23 | minimum-safe deterministic N | Planning/NewFarSolver | tie-break | transition | min lot | HSB_0R_DEC_005 | RESOLVED |
| HSBI-DEC-006 | 23 | emergency separate from recovery | Risk/EmergencyPolicy | triggers | liquidation | stress | HSB_0R_DEC_006 | RESOLVED |
| HSBI-DEC-007 | 23 | four transition loss caps | Risk/TransitionGate | caps | transition | reversals | HSB_0R_DEC_007 | DEFERRED_WITH_SAFE_CONTRACT |
| HSBI-DEC-008 | 23 | money threshold + buffer | Money/FinalCloseCalculator | equality | final close | costs | HSB_0R_DEC_008 | DEFERRED_WITH_SAFE_CONTRACT |
| HSBI-DEC-009 | 23 | mandatory risk gate order | Risk/* | fail closed | opening | low margin | HSB_0R_DEC_009 | DEFERRED_WITH_SAFE_CONTRACT |
| HSBI-DEC-010 | 23 | one cycle per symbol | Core/Identity | scope | multi-symbol | same Magic | HSB_0R_DEC_010 | RESOLVED |
| HSBI-DEC-011 | 23 | versioned files + journal | Persistence/* | checksum | recovery | restart | HSB_0R_DEC_011 | RESOLVED |
| HSBI-DEC-012 | 23 | REAL_LIMITED contract | Core/RuntimeMode | approval | critical error | demo forward | HSB_0R_DEC_012 | RESOLVED |

Правила: один owner на нормативное определение; ссылки не являются повторным определением. Нет requirement без будущего owner и тестового маршрута. Наличие функции без caller/runtime/transaction/evidence не является PASS.
