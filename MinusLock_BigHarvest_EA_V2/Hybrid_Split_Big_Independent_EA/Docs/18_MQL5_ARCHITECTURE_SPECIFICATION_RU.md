# 18. Независимая MQL5-архитектура Hybrid Split Big

Версия HSB.0R-C.19. Статус: нормативный design, без production-кода.

## Слои
Core: RuntimeMode, Types, Context, Identity, StateMachine. Planning: CandidatePlan, GeometrySolver, NewFarSolver, CatchUpModel, FutureSmall, DecisionEngine. Money: BrokerMoneyModel, EconomicLedger, AllocationLedger, FinalReserve, PartialFarBudget, FinalCloseCalculator. Execution: TradeRequestEngine, TransactionEngine, ActionRegistry, FillAccumulator, OwnershipGuard, ExecutionRevalidator. Scenarios: InitialLock, BigBasketOpen, BigHarvest, PartialFar, FinalClose, SmallTransition. Persistence: SnapshotStore, EventStore, Recovery, Reconciliation. Risk: MarginModel, DrawdownGate, SpreadGate, BasketRisk, EmergencyPolicy. Diagnostics: Logger, Trace, ReasonCodes, Panel, EvidenceWriter.

## Decision mapping
| Decision | MQL5 owner | Input | Output | Dependency | Forbidden | Persistence | Test owner |
|---|---|---|---|---|---|---|---|
| DEC-001 | Planning/GeometrySolver | F, ratios, grid | normalized C/T/S proof | Planning→Money/Risk/Core DTO | OrderSend | CandidatePlan | MQL5 unit |
| DEC-002 | Money/AllocationLedger | source deals, shares | allocations | Money→Core types | trade calls | ledger+journal | ledger tests |
| DEC-003 | Planning/MarketSnapshot | tick/symbol props | typed prices | Planning→Core | state mutation | snapshot fingerprint | geometry tests |
| DEC-004 | Planning/FutureSmall | candidate cycle | recursive proof | Planning→Money/Risk | execution | plan digest | solver tests |
| DEC-005 | Planning/NewFarSolver | candidate grid/proofs | minimum-safe N | Planning→Money/Risk | promotion | candidate digest | solver tests |
| DEC-006 | Risk/EmergencyPolicy | risk/conflicts | emergency decision | Risk→Core outcome | recovery PASS | reason/snapshot | emergency tests |
| DEC-007 | Scenarios/SmallTransition+Money | actual deals/caps | loss decision | Scenarios→Money/Risk | direct ledger write | plan/ledger | transition tests |
| DEC-008 | Money/FinalCloseCalculator | recovery/coverage | typed gate | Money→Core | OrderSend | FinalClosePlan | FC tests |
| DEC-009 | Risk/* | account/basket/control | typed gates | Risk→Money/Core | role assignment | risk proof | stress tests |
| DEC-010 | Core/Identity | account/symbol/cycle/position | ownership result | all→Core types | comment-only identity | namespace | identity tests |
| DEC-011 | Persistence/* | state/ledgers/journal | recovered candidate | Persistence→Core/Money/Execution metadata | new basket | snapshots | crash tests |
| DEC-012 | Core/RuntimeMode+Risk | readiness/approval | REAL_LIMITED allowed/denied | Core→Risk | implicit enable | config evidence | production tests |
| DEC-013 | Planning/Geometry+SmallTransition | snapshots/debounce | confirmed trigger | Scenario→Planning | direct action | debounce | trigger tests |
| DEC-014 | Execution/TransactionEngine | pending/history/events | retry/reconcile outcome | Execution→Persistence/Core | new ActionID retry | attempts | transaction tests |

## Dependency rules
Money/Planning/Risk не отправляют ордера; Scenarios не пишут ledgers напрямую; Diagnostics read-only; Reconciliation не создаёт basket; StateMachine не считает broker money; Execution не выбирает strategy; include graph остаётся внутри нового root.

Future entry: OnInit validates/reconciles; OnTick only plans/dispatches when safe; OnTradeTransaction is completion ingress; OnTimer handles diagnostics/timeouts but cannot declare completion. Preconditions HSB.0 PASS+user approval. Production code на этом этапе отсутствует.