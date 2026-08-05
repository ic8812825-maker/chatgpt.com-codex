# Этап 3.1.6.3 — include graph и call graph MQL5

## 3.1.6.3.2 — полный include graph

Главный compilation unit `MinusLock_BigHarvest_EA.mq5` напрямую подключает 25 project include-файлов в следующем порядке:

```text
Config → Types → LotUtils → SimulationEngine → PositionUtils → GeometryEngine
→ Logger → TradeEngine → RecoveryMath → BrokerMoneyModel
→ HybridRoundingModel → HybridGeometrySolver → HybridTransitionPlanner
→ HybridCatchUpModel → HybridMarginModel → HybridWorstCaseModel
→ HybridFutureSmallSolver → HybridDecisionEngine → RiskManager
→ StateMachine → PendingContractEngine → PositionResolutionEngine
→ StateIntegrityEngine → ReconciliationEngine
```

### Классификация модулей

| Файл | Назначение | Поколение/слой | Production reachability | Основной риск | Статус |
|---|---|---|---|---|---|
| `Config.mqh` | inputs, runtime work values, simulation predicate | MIXED_MODE | ACTIVE | Legacy/Split/Hybrid flags без единого enum | CONFLICTING |
| `Types.mqh` | states, roles, contexts, plans, ledger structs | MIXED_MODE | ACTIVE | единый context содержит несколько поколений | PARTIAL |
| `LotUtils.mqh` | broker volume normalization | COMMON | ACTIVE | разные направления rounding в старых/new paths | PARTIAL |
| `SimulationEngine.mqh` | виртуальные позиции и execution | SIMULATION_ONLY | ACTIVE при `!AllowRealTrading` | запрет real trading меняет execution semantics | UNSAFE |
| `PositionUtils.mqh` | поиск/подсчёт/выбор позиций | COMMON/MIXED | ACTIVE | ticket/identifier/role fallback требует строгого ownership | PARTIAL |
| `GeometryEngine.mqh` | Legacy/Split/adaptive geometry | MIXED_MODE | ACTIVE | альтернативный источник lots/levels | CONFLICTING |
| `Logger.mqh` | journal/CSV/diagnostics | COMMON | ACTIVE | trace не является transaction confirmation | PARTIAL |
| `TradeEngine.mqh` | CTrade/симуляция open-close wrappers | COMMON/MIXED | ACTIVE | synchronous success используется как подтверждение | UNSAFE |
| `RecoveryMath.mqh` | recovery P/L и close conditions | LEGACY/COMMON | ACTIVE | конкурирующие Final Close semantics | CONFLICTING |
| `BrokerMoneyModel.mqh` | projected broker money | HYBRID_SUPPORT | ACTIVE в gates/preview | projected не заменяет actual deal | PARTIAL |
| `HybridRoundingModel.mqh` | role-specific rounding | HYBRID | reachable through solver | малый thin wrapper | PARTIAL |
| `HybridGeometrySolver.mqh` | Hybrid initial lots/candidate | HYBRID | только при Hybrid flag | не единый immutable execution plan | HYBRID_PARTIAL |
| `HybridTransitionPlanner.mqh` | reverse plan/NewFar candidate | HYBRID | Small path | plan сохраняется в context, но execution повторно вычисляет часть values | HYBRID_PARTIAL |
| `HybridCatchUpModel.mqh` | finite harvest/catch-up projection | HYBRID_PREVIEW | gate/preview | не actual ledger execution | HYBRID_PREVIEW_ONLY |
| `HybridMarginModel.mqh` | margin projection | HYBRID_PREVIEW | gate/preview | отсутствует доказательство full runtime coverage | UNPROVEN |
| `HybridWorstCaseModel.mqh` | adverse projection | HYBRID_PREVIEW | gate/preview | не actual execution confirmation | HYBRID_PREVIEW_ONLY |
| `HybridFutureSmallSolver.mqh` | future reverse check | HYBRID_PREVIEW | solver path | ограниченная модель, production depth не доказана | HYBRID_PARTIAL |
| `HybridPartialFarPreview.mqh` | projected Partial Far route | HYBRID_PREVIEW | decision path | actual execution остаётся в StateMachine | HYBRID_PREVIEW_ONLY |
| `HybridDecisionEngine.mqh` | aggregate preview/decision | HYBRID_PREVIEW | вызываемость требует отдельной проверки | фактический OnTick dispatch идёт через StateMachine | HYBRID_PARTIAL |
| `RiskManager.mqh` | spread/margin/drawdown/position gates | COMMON | ACTIVE | risk gate не блокирует весь FSM; semantics зависят от caller | PARTIAL |
| `StateMachine.mqh` | фактический FSM, persistence, reserve, Legacy/Split/Hybrid execution | MIXED_MODE | ACTIVE | монолит смешивает поколения и synchronous trade flow | UNSAFE |
| `PendingContractEngine.mqh` | pending operation contracts | COMMON/SPLIT | ACTIVE | контракт не заменяет OnTradeTransaction | PARTIAL |
| `PositionResolutionEngine.mqh` | role resolution/restart | COMMON/MIXED | ACTIVE | fallback может смешать legacy/split roles | PARTIAL |
| `StateIntegrityEngine.mqh` | topology/state validation | COMMON/MIXED | ACTIVE | проверяет несколько topology, не делает Hybrid единственным | PARTIAL |
| `ReconciliationEngine.mqh` | positions/history reconciliation | COMMON/MIXED | ACTIVE | не полноценный deal-event ledger 3.1.5 | PARTIAL |

### Структурные выводы

1. Include graph физически плоский: все project modules подключаются главным `.mq5`.
2. Архитектура зависит от порядка include, поскольку более поздние модули используют типы, globals и функции ранних модулей без явных интерфейсных boundaries.
3. `StateMachine.mqh` является фактическим центром не только FSM, но и persistence, Reserve ledger, Big/Small execution и Hybrid promotion; разделение ответственности неполное.
4. Hybrid-модули преимущественно формируют projected/gate semantics, тогда как irreversible actions остаются в смешанном `StateMachine.mqh`/`TradeEngine.mqh`.
5. Отдельного production transaction adapter, который связывает CandidatePlan → request → order → deal → applied state, в include graph нет.

### Итог

```text
INCLUDE_FILES_TOTAL=25
PHYSICAL_INCLUDE_GRAPH=COMPLETE
LOGICAL_DEPENDENCY_GRAPH=PARTIAL
PRODUCTION_MQL5_CHANGED=NO
```
