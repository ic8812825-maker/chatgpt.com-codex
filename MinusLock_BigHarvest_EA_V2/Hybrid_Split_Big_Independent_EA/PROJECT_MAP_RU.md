# Карта независимого проекта Hybrid Split Big

Версия: 1.0. Статус: нормативный документ HSB.0.

## Назначение

Проект создаёт с нуля одну торговую систему `HYBRID_SPLIT_BIG_ONLY`. Причина независимой реализации — исключить смешение прежних поколений, polling-исполнение, конкурирующие Final Close и неоднозначный источник NewFar.

## Граница

Входит: документация, будущий MQL5-код, MQL5/Strategy Tester-тесты, sets, evidence и отчёты только внутри текущего корня. Не входят: старые include, Legacy/отдельный Split Big, Python production-oracle, DUAL_TAIL, второй Far.

## Структура

- `Docs/` — единственная нормативная база; не исполняет сделки.
- `Include/Core/` — типы, context, identity, FSM; не считает broker money.
- `Include/Planning/` — immutable CandidatePlan, GeometrySolver, NewFarSolver, CatchUp, FutureSmall, DecisionEngine; не отправляет заявки.
- `Include/Money/` — BrokerMoneyModel, EconomicLedger, AllocationLedger, FinalReserve, PartialFarBudget, FinalCloseCalculator; не вызывает Execution.
- `Include/Execution/` — request, OnTradeTransaction, ActionRegistry, FillAccumulator, OwnershipGuard, revalidation; не выбирает стратегию.
- `Include/Scenarios/` — InitialLock, BasketOpen, BigHarvest, PartialFar, FinalClose, SmallTransition; использует Planning/Money/Execution через контракты.
- `Include/Persistence/` — versioned SnapshotStore, EventStore, Recovery, Reconciliation; не создаёт корзины.
- `Include/Risk/` — margin, drawdown, spread, basket risk, emergency policy; не назначает NewFar.
- `Include/Diagnostics/` — logger, trace, reason codes, panel, evidence; только читает состояние.
- `Tests/` — MQL5 unit/integration, Strategy Tester и evidence.

## Направление зависимостей

```text
Scenarios → Planning → Money → Core
Scenarios → Execution → Core
Execution → Money (только подтверждённые actual facts)
Persistence → Core + Money + execution metadata
Risk → Money + Core
Diagnostics → read-only ко всем слоям
```

Запрещено: Money→Execution; Geometry→TradeRequest; Diagnostics→FSM mutation; FSM→самостоятельный broker-money расчёт; Scenarios→прямое изменение ledger; Execution→выбор сценария; Reconciliation→новая корзина; Logger→source of truth.

## Будущие этапы

1. `HSB.0` — нормативная документация.
2. `HSB.1` — типы, identity, reason codes, runtime shell без торговли.
3. `HSB.2` — broker money, ledgers, persistence.
4. `HSB.3` — event-driven execution и OnTradeTransaction.
5. `HSB.4` — planning/geometry/NewFar solver.
6. `HSB.5` — сценарии и FSM.
7. `HSB.6` — MQL5 tests и compile.
8. `HSB.7` — Strategy Tester/stress/restart.
9. `HSB.8` — demo forward.
10. `HSB.9` — ограниченный real только по явному решению Администратора.

## Requirement IDs

- `HSBI-GEN-001`: проект имеет один runtime mode — Hybrid Split Big.
- `HSBI-GEN-002`: старые include и execution-модули не подключаются.
- `HSBI-GEN-003`: каждый слой изменяет только принадлежащее ему состояние.
- `HSBI-GEN-004`: production-код запрещён до `HSB_STAGE_0_DOCUMENTATION=PASS` и `USER_APPROVAL=YES`.
- `HSBI-GEN-005`: Diagnostics не имеет права на irreversible action.

## Общий контракт документа

Вход: утверждённое ТЗ HSB.0. Выход: карта модулей и границ. Preconditions: ветка `work`, разрешённый родительский каталог. Postconditions: будущая архитектура не зависит от старого советника. Error route: конфликт зависимости блокирует HSB.1. Restart semantics: не применимо к документу; будущий owner — `Core/Architecture`. Тест: статический dependency audit. Открытые вопросы вынесены в `Docs/22_OPEN_DECISIONS_REGISTER_RU.md`.