# Этап 1 — Hybrid Finite Catch-Up

**Base SHA:** `f205f22` (документальные инварианты). **Scope:** только математическая Catch-Up model; StateMachine, TradeEngine, DecisionEngine и execution не меняются.

## Реализация

`EvaluateHybridFiniteCatchUpPreview` строит новый `HybridHarvestLevelResult` для каждого `n`. Bid/Ask вычисляются из `BigMoveStartPoints+(n-1)BigMoveStepPoints` с BUY/SELL symmetry. На каждом уровне отдельно вызывается `BrokerMoneyModel` для Far/Core/Trend/Small, а Base и Worst prices рассчитываются независимо.

Harvest исключает Far. Allocation использует `.10/.90/.00`, явный residual и conservation. Reserve/Partial/Carry кумулятивны; Far cost берётся из Far net. Recovery использует projected realized, floating gross и exit-cost provenance. Margin вызывается через `CalcProjectedMarginMoney`. PASS требует coverage, Recovery, margin Base/Worst и Worst money одновременно.

## Инварианты

* `ReserveAfter[n] >= ReserveAfter[n-1]`.
* `CoverageDeficit[n] <= CoverageDeficit[n-1]-HybridMinimumCoverageGainMoney`.
* `RecoveryPL[n] >= RecoveryPL[n-1]` внутри frozen market path.
* allocation conservation в `MoneyCalculationTolerance`.
* любой broker money/margin failure завершает модель ошибкой, не safe PASS.

## Trace

Каждая строка содержит LEVEL, BID/ASK, четыре leg net, HarvestNet, Reserve, CoverageDeficit, RecoveryPL, MarginBase/Worst и Decision. Полный trace возвращается в `HybridCatchUpResult.trace`; модель не пишет торговый журнал сама и остаётся pure.

## Tests

FC-01…FC-11 покрывают level 1/2/N, no coverage, Recovery, margin, Worst, BUY/SELL, spread/commission shock и invariants. MQL fixture catalogue добавлен; выполнение MetaEditor остаётся `NOT_EXECUTED_IN_CONTAINER`.

## Статус

`HYBRID_FINITE_CATCHUP_READY` на уровне исходного кода и воспроизводимых contract tests; MQL5 compile/runtime parity остаётся обязательным этапом 8.
