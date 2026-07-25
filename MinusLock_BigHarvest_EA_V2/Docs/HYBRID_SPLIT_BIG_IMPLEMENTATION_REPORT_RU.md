# Hybrid Split Big — отчёт реализации MQL5, этап 2

## Статус

`HYBRID_PREOPEN_DECISION_ENGINE_NOT_READY` до подтверждённой компиляции MetaEditor `0 errors / 0 warnings`.

## Реализовано в pre-open evaluator

* `EvaluateHybridCandidate()` остаётся чистой функцией предварительной оценки: не открывает ордера, не закрывает позиции, не меняет `StateMachine`.
* Добавлены отдельные Hybrid inputs `HybridPartialFarShare`, `HybridFinalReserveShare`, `HybridCarryShare`.
* Исправлен нормативный профиль округления: `Core DOWN`, `Trend DOWN`, `SmallBase UP`, `NewFar DOWN`.
* `UseHybridSplitBigGeometry=false` теперь возвращает `applicable=false`, `passed=false`, `finalCode=HYBRID_FINAL_NONE`, `reason=HYBRID_DISABLED`.
* Law 1 использует только `HybridFinalReserveShare`, а не legacy `WorkReserveShare`.

## ADM-MQL5-05

Исторический профиль `β=0.70`, `Core=1.60`, `Trend=0.25`, `Small=0.60` давал `K_R=0.875` и отклонялся по `HYBRID_REJECT_LAW1`. ADM-MQL5-05 теперь закрыт профилем `.10/.90/.00`.

## Static baseline

`BASELINE_STATIC_FAILURE_RESOLVED`: контракт `SimRecordClosedDeal` восстановлен как совместимый wrapper над единым `SimRecordDeal`, поэтому static test больше не должен падать на отсутствии имени функции.

## Ограничения этапа

* Полной интеграции в реальные торговые open/close paths нет по заданию этапа 2.
* MetaEditor в текущем контейнере недоступен, поэтому фактический compile result должен быть получен в MT5 окружении.

## Этап 0 — нормативная документация (2026-07-25)

* Base SHA: `0d0a8d195cb704859fa541257dd25bdc980c64b1`.
* ADM-MQL5-05 принят Администратором: `.10/.90/.00`, `K_R=1.125`.
* Создан полный алгоритмический контракт состояния, level table, risk prices, единого solver, Future transition, Final Close, ledgers и State Machine mapping.
* Торговая логика и State Machine не интегрировались; следующие этапы остаются обязательными.
* Strategy Tester: `NOT_EXECUTED_BY_PROGRAMMER`. Reason: Administrator will execute Strategy Tester independently.

## Этап 1 — finite Catch-Up (2026-07-25)

Упрощение с повторным `plan.projectedHarvestNet` удалено. Каждый level имеет собственные Bid/Ask и четыре `BrokerMoneyResult`; PASS объединяет coverage, RecoveryPL, margin Base/Worst и Worst Case. StateMachine, TradeEngine, DecisionEngine и execution не изменялись. FC-01…FC-11 добавлены. Strategy Tester: `NOT_EXECUTED_BY_PROGRAMMER`.
