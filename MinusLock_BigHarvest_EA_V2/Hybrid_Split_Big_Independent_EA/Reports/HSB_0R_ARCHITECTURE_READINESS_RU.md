# Документальная готовность архитектуры к HSB.1

Статус: READY_FOR_ACCEPTANCE, не разрешение на начало HSB.1.

Без изменения нормативных интерфейсов могут быть созданы: enums RuntimeMode/Role/State/ActionStatus/ReconciliationOutcome/ReasonCode; types IdentityKey, CycleContext, MarketSnapshot, CandidatePlan, TransitionPlan, PendingAction, FillRecord, EconomicLedgerRecord, AllocationRecord, VersionedSnapshot.

Определены обязательные interfaces:
- Core: immutable identity, context revision, FSM event application;
- Planning: geometry/catch-up/FutureSmall/NewFar solver inputs and typed result;
- Money: broker calculator, ledgers, allocation conservation, FinalClose result;
- Execution: ownership guard, action registry, request sender, OnTradeTransaction fill accumulator;
- Persistence: snapshot/journal/lock/recovery;
- Risk: ordered fail-closed gates and emergency decision;
- Diagnostics: read-only trace/evidence.

Основные contracts не зависят от будущих оптимизируемых ratios/shares/limits: они передаются как validated configuration. `DEFERRED_WITH_SAFE_CONTRACT` не требует изменения основных типов.

Не создавались `.mq5/.mqh`, OnTick, OnTradeTransaction implementation или торговые функции. Следующий этап может быть разрешён только итоговой HSB.0R acceptance и отдельным решением пользователя.
