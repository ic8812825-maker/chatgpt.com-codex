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

Текущие утверждённые `β=0.70`, `Core=1.60`, `Trend=0.25`, `Small=0.60` дают `K_R=0.875`, поэтому текущая комбинация обязана завершаться `HYBRID_REJECT_LAW1` до решения Администратора.

## Static baseline

`BASELINE_STATIC_FAILURE_RESOLVED`: контракт `SimRecordClosedDeal` восстановлен как совместимый wrapper над единым `SimRecordDeal`, поэтому static test больше не должен падать на отсутствии имени функции.

## Ограничения этапа

* Полной интеграции в реальные торговые open/close paths нет по заданию этапа 2.
* MetaEditor в текущем контейнере недоступен, поэтому фактический compile result должен быть получен в MT5 окружении.
