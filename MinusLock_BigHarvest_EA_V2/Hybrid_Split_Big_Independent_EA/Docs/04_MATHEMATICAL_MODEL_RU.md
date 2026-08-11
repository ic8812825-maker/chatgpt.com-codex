# 04. Полная математическая модель Hybrid Split Big

Версия HSB.0R-C.5. Статус: нормативный source of truth.

## Размерности
F,C,T,S,N — lot; цены — account symbol price; money — валюта счёта; ratios безразмерны; tick/point различаются.

## Объёмы
`C=FloorBrokerGrid(F×Rc)`, `T=FloorBrokerGrid(F×Rt)`, `S=CeilBrokerGrid(F×Rs)`, `Bnet=C+T-S`. Rc>0, Rt≥0, Rs>0. После rounding каждый lot должен быть в [Vmin,Vmax] и кратен Vstep.

## Recovery slope
`RecoverySlopeLots=C+T-S-F`. Необходимое условие после rounding: `RecoverySlopeLots>0`. Для Far SELL рост цены улучшает BUY-side basket; для Far BUY падение цены улучшает SELL-side basket. Это только аналитический фильтр.

## Reserve Catch-Up
Необходимая lot-оценка: `ReserveShare×Bnet>F`. Production gate: `ReserveGainMoney(Pcontrol)>FarLossIncreaseMoney(Pcontrol)+ExecutionSafetyBufferMoney`, рассчитано broker money model, BUY/Bid, SELL/Ask, commission, swap, slippage, asymmetric tick value. Неизвестный расчёт отклоняется.

## RecoveryPL
`RecoveryPLCloseNow=RealizedCycleNet+ΣOpenPositionCloseNowNet`; `OpenPositionCloseNowNet=OrderCalcProfit-at-close commission-execution buffer`. FinalReserve, PartialFarBudget, TransitionBudget, Carry и Residual не прибавляются повторно, поскольку являются allocation subsets.

## Compression
`0<N<F`; `N≤MaximumNewFarRatio×F`; `F-N≥MinimumFarCompressionLots`; `(F-N)/F≥MinimumFarCompressionRatio`; одновременно `NextBigGross<OldBigGross`, `NextGrossExposure<OldGrossExposure`, `RiskNext<RiskOld-RiskTolerance`, `MarginNext≤AllowedMargin`.

## Transition Loss
`TransitionNet=ΣActualClosingDealNet`; `TransitionLossMoney=max(0,-TransitionNet)`. AllowedTransitionLoss=min(AbsoluteCap,EquityCap,OldFarRiskCap,CumulativeCycleCap).

## Final Close
`RecoveryPLCloseNow≥MinimumRecoveryProfitMoney+ExecutionSafetyBufferMoney+MoneyTolerance`. Все члены money; отрицательный или недостаточный результат — reject.

## Allocation conservation
Для каждого SourceDealKey: `Rsv+PF+Tr+Carry+Residual=AllocatableDealNet`, все allocations≥0 и сумма не превышает положительный available amount. Negative DealNet уменьшает economic result, но не создаёт allocatable profit. Duplicate identical event=NO-OP; conflict=RECONCILIATION.

## Future Small
Exact recursion строит следующий cycle до terminal lot, configured depth или доказанного bound. Затем допустим conservative bound `F(k+j)≤q^jF(k)`, 0<q<1, только если rounding, costs, risk, margin и transition loss включены.

## Дискретная конечность
Пусть после rounding `F(k+1)≤qF(k)`, q<1. Теоретическая граница `K≥ceil(ln(Vmin/F0)/ln(q))`. На broker grid дополнительно требуется строгое уменьшение минимум на Vstep либо переход к operational terminal close; plateau candidate отклоняется.

## Направления
Far SELL: F SELL, C/T BUY, S SELL; close BUY=Bid, close SELL=Ask. Far BUY зеркален. Формулы сохраняют знак через broker profit function.

## Fail-closed
Reject при invalid dimensions, stale price, rounding-law failure, nonfinite money, no safe N, failed recursion или insufficient margin. Documentary algebraic consistency не является broker runtime proof.
> **Граница реализации HSB.1V (2026-08-10).** Описанный production lifecycle остаётся нормативной спецификацией, а не реализованным сценарием. В каркасе нет production execution, broker-money runtime и production persistence. Действуют: ровно один Far; promotion только из actual BigCore residual; FinalReserve запрещён для Partial Far; allocations не прибавляются к actual money повторно; Final Close определяется только actual money; только COMPLETED_FILL снимает transaction barrier; retry сохраняет ActionID; conflict ведёт в RECONCILING; unresolved critical error — в TERMINAL_SAFE; no auto-resume; REAL_LIMITED и HSB.2 запрещены.
