# Синхронизация математики, геометрии и NewFar Solver

Нормативное дополнение к Docs/04, 05, 14 и 15.

## Формулы и размерности

F,C,T,S,N — lot; Rc,Rt,Rs — ratio; prices — price; risk/recovery/reserve — account money. `Bnet=C+T-S`; необходимый slope: `C+T-S-F>0` после broker rounding. Catch-Up проходит только денежный proof `ReserveGainMoney(P)>FarLossIncreaseMoney(P)+ExecutionBufferMoney`.

`RecoveryPLCloseNow=RealizedCycleNet+ΣOpenPositionCloseNowNet`; allocation buckets не прибавляются повторно. Broker model: BUY close Bid, SELL close Ask, OrderCalcProfit/OrderCalcMargin, commission/swap/slippage/buffers.

## Control range

Каждый proof использует typed fresh control price, normalized to tick. Recovery monotonicity проверяется point-by-point либо на доказанном piecewise-linear segment с boundary/event checks.

## NewFar

Solver перечисляет broker-valid N, требует `MinimumOperationalFarLot<=N<F`, compression, next-basket decrease, RecoveryPL, catch-up, risk, margin, recursive Future Small, transition caps и finite bound. Выбирается minimum-safe; actual NEW_FAR — только actual residual original BigCore.

## Limits

RiskNext и RiskOld считаются в money к adverse control price. Transition cap — minimum absolute/equity/OldFarRisk/cumulative limits. Любая invalid dimension, stale price, missing broker result или failed rounding gate даёт REJECT.
