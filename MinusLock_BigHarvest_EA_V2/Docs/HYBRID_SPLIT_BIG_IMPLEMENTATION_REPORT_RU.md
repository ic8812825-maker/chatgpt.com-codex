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

## Stage 1.1-A — temporal semantics

Последовательная модель утверждена: каждый Harvest закрывает текущие working legs ровно один раз, PartialFarNet входит в RealizedPL, residual Far порождает next basket и независимые Base/Worst states. Код Stage 1.1-B выполняется отдельным commit.

Temporal authority: `HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`.

## Stage 1.1-B/C — sequential source and audit

`HybridCatchUpModel` now evolves immutable Base/Worst states. Each level closes only current working legs, allocates its own Harvest, applies the pure Partial Far solver, updates `RealizedCyclePL` with `PartialFarNet`, recalculates residual-Far coverage and builds the next basket from the residual and current anchor. FT-01…FT-47 provide causal and static evidence. Status is `HYBRID_FINITE_CATCHUP_SOURCE_READY`; MetaEditor/runtime parity remain not executed.

## Stage 1.2 — typed outcomes, Worst execution path и margin semantics

Основной pure evaluator теперь возвращает типизированный `HybridCatchUpOutcome`; compatibility wrapper возвращает `true` только для согласованного Base/Worst `FINITE_PASS`. Final Close Preview является валидным ROUTE, а не calculation error. Агрегация Base/Worst централизована в truth-table helper.

Worst execution shock применяется к базовому trigger ровно один раз на уровень и не переносится в `baselineSpread` или следующий геометрический anchor. Margin preview выбирает BUY→Ask и SELL→Bid по текущей контрольной паре, хранит individual release только как `EstimatedReleasedMarginUpper` и принимает решение по conservative state-after upper bound.

Python oracle покрывает FO/WP/MG/CL и усиленные FT-07/10/27/33. Исполняемый MQL5 runner добавлен, но не запускался в контейнере.

Final status: `HYBRID_FINITE_CATCHUP_SOURCE_READY`; `HYBRID_FINITE_CATCHUP_RUNTIME_NOT_VERIFIED`.

MetaEditor compile: `NOT_EXECUTED_IN_CONTAINER`. Reason: MetaEditor executable not available.
MQL5 runtime fixtures: `NOT_EXECUTED`.
Strategy Tester: `NOT_EXECUTED_BY_PROGRAMMER`. Reason: Administrator will execute Strategy Tester independently.

Stage 1.2.1 authority: Final Close route сохраняет отдельный pre-Partial immutable state; route не строит continuation basket. См. `HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md` и `HYBRID_SPLIT_BIG_CATCHUP_OUTCOME_TRUTH_TABLE.md`.
