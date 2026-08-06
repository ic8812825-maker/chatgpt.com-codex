# 19. Матрица требований и будущего MQL5 mapping

Версия HSB.0R-C.20. Статус: нормативный source of truth.

| Requirement/Decision | Owner document | Future MQL5 owner | Unit | Integration | Strategy Tester | Evidence | Decision dependency | Status |
|---|---|---|---|---|---|---|---|---|
| HSBI-GEN-010 | 00/18 | Core/RuntimeMode | dependency | init | all | charter | DEC-012 | READY |
| HSBI-ID-010 | 02/18 | Execution/OwnershipGuard | foreign/stale | open/close | multi-symbol | identity spec | DEC-010 | READY |
| HSBI-MATH-001..014 | 04 | Planning/GeometrySolver,CatchUpModel | formulas/rounding | CandidatePlan | trend/reversal | corrected math | DEC-001,003,004 | READY |
| HSBI-GEO-005,010..025 | 05 | Planning/MarketSnapshot,GeometrySolver | tick/freshness/debounce | triggers | gaps/spread | corrected math | DEC-003,013 | READY |
| HSBI-FSM-001..020 | 06 | Core/StateMachine | reachability | partial/retry | delayed fills | tx spec | DEC-014 | READY |
| HSBI-TX-001..032 | 07 | Execution/TransactionEngine | keys/retcodes | fills/restart | latency | tx evidence | DEC-014 | READY |
| HSBI-MONEY-001..020 | 08 | Money/EconomicLedger,AllocationLedger | conservation | harvest/replay | costs | allocation vector | DEC-002,007,008 | READY |
| HSBI-INIT-001..010 | 09 | Scenarios/InitialLock | exclusion/identity | rollback | both directions | initial spec | DEC-010,014 | READY |
| HSBI-BIG-001..012 | 10 | Scenarios/BigHarvest | source ownership | allocation | trends | harvest spec | DEC-001,002,003,009,014 | READY |
| HSBI-PF-001..010 | 11 | Scenarios/PartialFar | floor/isolation | partial fill | min lot | PF spec | DEC-002,014 | READY |
| HSBI-FC-001..012 | 12 | Money/FinalCloseCalculator | threshold | basket close | costs/gaps | FC vectors | DEC-008 | READY |
| HSBI-SMALL-001..026 | 13 | Scenarios/SmallTransition | order/debounce/caps | transition | repeated reversals | transition vectors | DEC-005,007,013,014 | READY |
| HSBI-NF-001..018 | 14 | Planning/NewFarSolver,FutureSmall | grid/tie/recursion | transition | coarse/min lot | NF vectors | DEC-004,005 | READY |
| HSBI-RISK-001..030 | 15 | Risk/* | ranges/gates | opening/emergency | stress/low margin | risk spec | DEC-006,007,009,012 | READY |
| HSBI-PERSIST-001..018 | 16 | Persistence/SnapshotStore,EventStore | checksum | crash/restart | fixtures | persistence spec | DEC-011,014 | READY |
| HSBI-RECON-001..020 | 17 | Persistence/Reconciliation | mismatch classes | restart | manual/delayed | recon spec | DEC-010,011,014 | READY |
| HSBI-GEN-030..060 | 18 | Architecture owners | static deps | skeleton | N/A | architecture | DEC-001..014 | READY |
| HSBI-PROD-001..020 | 21 | Reports/Acceptance+Core/RuntimeMode | gate set | demo | forward | readiness | DEC-012 | READY |
| HSBI-DEC-001..014 | owner docs 04..21 | mapping in 18 | decision-specific | scenario-specific | listed vectors | 23+corrected evidence | self | CLOSED_FOR_ARCHITECTURE |

## Аудит
OWNERLESS_REQUIREMENTS=0
REQUIREMENTS_WITHOUT_TEST_ROUTE=0
DECISIONS_WITHOUT_OWNER=0
DECISIONS_WITHOUT_MAIN_DOCUMENT_MAPPING=0
CONFLICTING_DEFINITIONS=0

Owner document содержит полную норму; evidence только подтверждает. Повтор ID в матрице является ссылкой. Наличие будущей функции без caller/runtime/transaction/test/evidence не является PASS.