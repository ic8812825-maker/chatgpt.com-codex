# Hybrid Split Big — справочник формул и инвариантов

## Размерности
`[LOTS]`: F,C,T,S,N; `[RATIO]`: c,t,s,q,β; `[POINTS]`: x; `[MONEY]`: PL,R,Deficit,Risk; `[PRICE]`: P; `[BOOLEAN]`: PASS; `[STATE]`: CycleID.

## Формулы уровня A
| Назначение | Формула | Условие |
|---|---|---|
| Абсолютная корзина | `PL0+(C+T-S-F)Vx` | V — только analytic |
| Закон 1 | `β(C+T-S)>F` | `0<β<=1` |
| Catch-Up Ratio | `KR=β(c+t-s)` | нужен `KR>1` |
| Закон 2 | `C+T-S-F>0` | следует из закона 1 |
| Catch point | `(LF0+KF-R0-βH0+βKH)/(V[β(C+T-S)-F])` | denominator > 0 |
| Compression | `0<N<F`, `q=N/F` | strict |
| Next Big | `(c+t)qF<F` | constant ratios: `q<1/(c+t)` |
| Core close | `CloseC=C-N=(c-q)F` | N is actual target |
| Constant q steps | `Nmin=ceil(ln(Fterminal/F0)/ln q)` | `0<q<1` |
| Variable q bound | `Nmax=ceil(ln(Fterminal/F0)/ln qmax)` | `qn<=qmax<1` |

## Формулы уровня B
* `LegNet=OrderCalcProfit(direction,symbol,lot,open,directional Bid/Ask close)-not-yet-included costs`.
* `RecoveryPLCloseNow=RealizedCyclePL+FloatingManagedPL-ExpectedExitCosts`; no duplicate commission or reserve.
* `FinalReserveProjected=FinalReserveReal+β*max(EligibleHarvestCloseNet,0)`.
* `CoverageDeficit=FarCloseCost-FinalReserveReal`; finite catch-up requires a planned level with `Deficit<=0`.
* `TransitionNet=NetF+NetS+NetT+NetCoreClosed+TransitionBudget-OtherTransitionCosts >= -MaximumAllowedTransitionLoss`.
* `RiskNext<RiskOld`, with both risks calculated by money loss to explicit control prices.
* Margin requires OrderCalcMargin for each planned leg, positive free margin and configured level/usage limits.

## Непересекающиеся money buckets
1. `RealizedCyclePL`: accounting result of deals.
2. `FinalReserveReal`: tagged subset of realized profit for final Far only.
3. `PartialFarBudget`: separately tagged harvest allocation.
4. `TransitionBudget`: only explicitly permitted non-FinalReserve funds.

## Mandatory gates
`IDENTITY`, `LOTS`, `MONEY`, `FINITE_CATCHUP`, `FUTURE_SMALL`, `ROUNDING`, `RISK`, `MARGIN`, `WORST_CASE`, `RECONCILIATION`.

## Final Close, allocation and limits
$$
ProjectedFinalRecoveryPL=RealizedCyclePL_{before}+ProjectedCloseNetAllManagedPositions
$$
passes only with the configured final-close safety buffer. After confirmed closes:
$$
ActualFinalRecoveryPL=RealizedCyclePL_{after\ all\ closes}.
$$
These identifiers must not be merged.

For `α+β+γ=1` and `E=max(HarvestNetActual,0)`: `PartialAdd=αE`, `ReserveAdd=βE`, `CarryAdd=E-PartialAdd-ReserveAdd`; residual always enters carry. `CoverageDeficit=max(-ProjectedFarCloseNet,0)+CoverageSafetyBuffer-FinalReserveReal`.

`CumulativeTransitionLossNew=CumulativeTransitionLossOld+max(-TransitionNet,0)`. A transition requires its per-loss, cumulative-money and cumulative-percent caps. `FinalReserveReal` is not a transition source.

## Margin and terminal rule
`MarginConservativeUpperBound=CurrentMargin+ΣIndividualNewOrderMargin`; use it even if broker-aware basket estimate is available. If `Nraw<VolumeMin`, `Nnorm<VolumeMin`, or `Nnorm>=Fold`, no new cycle is legal; use Final Close precheck or `TERMINAL_SAFE_STATE`.

**Oracle rounding profile:** `EA_CURRENT` means BigCore DOWN, BigTrend DOWN, SmallBase UP and NewFar DOWN; every gate is rerun on these rounded lots.
