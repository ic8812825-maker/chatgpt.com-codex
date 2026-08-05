# Независимая MQL5-архитектура

Версия 1.0. Статус: нормативный design, без кода.

## Слои и owners

Core: RuntimeMode, Types, Context, Identity, StateMachine.
Planning: CandidatePlan, GeometrySolver, NewFarSolver, CatchUpModel, FutureSmall, DecisionEngine.
Money: BrokerMoneyModel, EconomicLedger, AllocationLedger, FinalReserve, PartialFarBudget, FinalCloseCalculator.
Execution: TradeRequestEngine, TransactionEngine, ActionRegistry, FillAccumulator, OwnershipGuard, ExecutionRevalidator.
Scenarios: InitialLock, BigBasketOpen, BigHarvest, PartialFar, FinalClose, SmallTransition.
Persistence: SnapshotStore, EventStore, Recovery, Reconciliation.
Risk: MarginModel, DrawdownGate, SpreadGate, BasketRisk, EmergencyPolicy.
Diagnostics: Logger, Trace, ReasonCodes, Panel, EvidenceWriter.

- `HSBI-GEN-030`: нет boolean mode выбора Legacy/Split/Hybrid; RuntimeMode фиксирован Hybrid-only.
- `HSBI-GEN-031`: include graph не выходит из нового project root.
- `HSBI-GEN-032`: interfaces передают immutable DTO и typed outcomes, не shared mutable globals.
- `HSBI-GEN-033`: OnTick планирует/dispatch; OnTradeTransaction является единственным completion ingress для trade actions.
- `HSBI-GEN-034`: Money/Planning/Risk не вызывают OrderSend.
- `HSBI-GEN-035`: Scenario не пишет ledger напрямую.
- `HSBI-GEN-036`: Diagnostics read-only.

## Будущий entry point

EA shell: OnInit validates schema/environment and reconciles; OnTick processes market triggers only when no pending conflict; OnTradeTransaction routes events to TransactionEngine; OnTimer handles bounded retries/reconciliation diagnostics, но не заменяет transaction confirmation.

## Контракт

Preconditions: HSB.0 PASS и user approval. Postconditions будущего mapping: каждая функция имеет Requirement IDs, owner и tests. Error route: forbidden dependency fails static architecture test. Restart owner — Persistence. Открытые вопросы: exact filenames/API DTOs, но границы слоёв нормативны.