# Полный мануал Hybrid Split Big

## Область и назначение

Hybrid Split Big разруливает Far после Initial Lock. Initial Profit исключён;
Far является единственным хвостом. BigCore и BigTrend направлены против Far,
SmallBase — вместе с ним. Документ подтверждает математическую модель,
архитектуру исходного кода и Python-валидацию; работа терминала MT5 не входит
в данный этап.

## Термины и параметры

`C=BigCore`, `T=BigTrend`, `S=SmallBase`, `F=Far`, `N=ActualNewFar`.
`BigGross=C+T`; `NetRecoveryExposure=C+T-S-F`;
`NextDirectional=Cnext+Tnext-Snext-N`. Inputs: `BigCoreRatio`,
`BigTrendRatio`, `SmallBaseToFarRatio`, `ReserveShare`,
`TargetNewFarRatio`, `MaximumNewBigToOldFarRatio`,
`MinimumReserveCatchUpRatio`, `MinimumRecoverySlopeMoneyPerPoint`,
`MaximumTransitionLossMoney`, `MinimumReserveAfterTransition`.

## Big

Lots are rounded down to broker step. Before opening, the EA requires positive
net recovery exposure, `ReserveShare*(C+T-S)/F >= MinimumReserveCatchUpRatio`,
margin gate, and point-by-point projected broker-net RecoveryPL growth. The
trace includes F/C/T/S, Bid/Ask close price, commission, spread, swap, fee and
slippage. At Big harvest actual lifecycle net is split once between Final
Reserve and Partial Far budget; the same money cannot be credited twice.

## Small

Before OldFar close `HybridReversePlan` stores identities, projected leg money,
target and next geometry. It scans broker-rounded candidates from minimum lot
upward and chooses the **minimum safe** N. The order is SmallBase close →
OldFar close → BigTrend close → staged BigCore close. Actual remaining Core is
verified, previewed again, and only then promoted to the single NewFar.
BigTrend and Legacy ReverseSmall never become NewFar.

## Three laws

Law 1: projected coverage slope is `ReserveShare*(C+T-S)` and must exceed F.
Law 2: full slope is `C+T-S-F`; monetary close result is checked every point.
Law 3: `0<N<F`, NewFar risk decreases, `NextBigGross=Cnext+Tnext<F` when the
gate is enabled, and `N<=qMaxF` gives finite reverse bound. Invalid geometry,
expense or rounding conditions are rejected before an irreversible action.

## Profiles

| Profile | C | T | S | Reserve | Target cap | Purpose |
|---|---:|---:|---:|---:|---:|---|
| SAFE | 1.80 | .75 | .16 | .92 | .35 | lower gross/margin |
| BALANCED | 2.00 | .80 | .20 | .90 | .30 | selected proof candidate |
| STRONG_COMPRESSION | 2.36 | .99 | .20 | .93 | .20 | highest compression/margin |

The system is complex and sensitive to cost, lot step and TransitionNet; a
missing safe candidate is an intended no-trade/manual-safe outcome, not a
reason to weaken a law.
