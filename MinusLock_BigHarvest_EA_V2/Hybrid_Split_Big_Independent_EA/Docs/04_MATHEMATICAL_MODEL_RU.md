# Математическая модель Hybrid Split Big

Версия 1.0. Статус: нормативный.

## Обозначения и направления

`F,C,T,S,N` — lots OldFar, BigCore, BigTrend, SmallBase, NewFar. `Bnet=C+T-S`. Для FAR SELL Big legs BUY, Small SELL; для FAR BUY — зеркально.

- `HSBI-MATH-010`: `F>0,C>0,T>0,S>0` на active basket.
- `HSBI-MATH-011`: `Bnet>0`.
- `HSBI-MATH-012`: аналитический slope `C+T-S-F>0` является необходимым, но не достаточным production-gate.

## Закон 1 — Reserve Catch-Up

Лотовое необходимое условие: `ReserveShare×(C+T-S)>F`. Production-gate:

`ReserveGainMoney(Pcontrol) > FarLossIncreaseMoney(Pcontrol)+ExecutionSafetyBufferMoney`.

Все величины — account money, рассчитанные через broker side, `OrderCalcProfit`, commission, swap, slippage и asymmetric tick values. FAR SELL: adverse loss растёт при росте Ask; BUY recovery закрывается по Bid. FAR BUY симметричен.

- `HSBI-MATH-013`: control price нормализуется по tick size.
- `HSBI-MATH-014`: лотовое inequality не заменяет money proof.

## Закон 2 — RecoveryPL

`RecoveryPLCloseNow=RealizedCycleNet+ΣOpenPositionCloseNowNet`.
`OpenPositionCloseNowNet=ProjectedCloseProfit-ExpectedCloseCommission-ExecutionBuffer`, с включением swap/fees согласно broker model.

Point-by-point gate: для каждого broker-valid price step в Big-направлении `RecoveryPL(Pnext)>RecoveryPL(P)+Tolerance`, кроме ухудшений с явно доказанной market/cost provenance.

- `HSBI-MATH-015`: FinalReserve, PartialFarBudget, TransitionBudget и Carry не прибавляются повторно.
- `HSBI-MATH-016`: BUY/SELL sequence проверяется симметрично.

## Закон 3 — компрессия и конечность

`0<N<F`; `N<=MaximumNewFarRatio×F`; `F-N>=MinimumFarCompressionLots`; `(F-N)/F>=MinimumFarCompressionRatio`.
Дополнительно: `NextBigGross<OldBigGross`, `NextGross<OldGross`, `RiskNext<RiskOld-RiskTolerance`, margin gate PASS.

Если после rounding для каждого transition `F(k+1)<=qF(k)`, `0<q<1`, то верхняя оценка числа переходов:

`K=ceil(ln(MinTerminalLot/F0)/ln(q))`, при `ln(q)<0`.

На дискретной сетке solver обязан доказать, что sequence строго убывает минимум на один volume step либо корректно достигает terminal lot; иначе terminal-safe.

## Broker money и примеры

ДЕМОНСТРАЦИОННЫЙ ПРОФИЛЬ, НЕ PRODUCTION DEFAULT: `F=1.00,C=1.60,T=0.25,S=0.60`; `Bnet=1.25`, slope=0.25 lot. При ReserveShare=0.90 лотовая база catch-up=1.125>1.00, но money proof всё равно обязателен.

При q=0.50, F0=1.00 и terminal=0.01: `K=ceil(ln(0.01)/ln(0.5))=7`. На step 0.01 sequence 1.00→0.50→0.25→0.12→0.06→0.03→0.01; каждый rounded transition повторно проходит gates.

Partial example: budget 120 money, cost 400 money/lot → raw 0.30 lot → floor step 0.01 =0.30. При SELL Far broker close side Ask; при BUY Far — Bid.

## Границы и отказ

NaN, invalid tick grid, zero point value, insufficient range, non-monotonic money proof, no safe N или dimension mismatch → candidate reject, без trade action.

## Контракт

Входы: broker snapshot, profile, current state. Выходы: typed proofs и reason codes. Preconditions: fresh/reconciled snapshot. Postconditions: все gates доказаны на округлённых значениях. Restart: proofs сохраняются в immutable plan fingerprint. Owner: Planning/CatchUp, Money/BrokerMoneyModel, Risk. Тесты: BUY/SELL, asymmetric tick values, gaps, costs, coarse lot step. Открытые вопросы: control ranges, q-policy, tolerances и production ratios.