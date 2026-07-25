# Hybrid Split Big — нормативная временная модель Catch-Up

**Статус:** `NORMATIVE`. Единственный нормативный источник временной семантики Big Harvest. Модель строго последовательная, не alternative-price. Каждый level закрывает только существующие в его `StateBefore` рабочие позиции, после чего строит новый state.

## 1. `HybridCatchUpState`

```cpp
struct HybridCatchUpState {
 int level; datetime snapshotTime; ulong cycleId; ulong stateRevision;
 Direction farDirection; double farLot; double farOpenPrice;
 Direction bigDirection; double coreLot; double coreOpenPrice;
 double trendLot; double trendOpenPrice;
 Direction smallDirection; double smallLot; double smallOpenPrice;
 double anchorBid; double anchorAsk;
 double realizedCyclePL; double partialFarBudgetAvailable;
 double finalReserveReal; double carryAvailable;
 double currentMargin; double equity; double freeMargin;
 double cumulativeHarvestNet; double cumulativePartialFarNet;
 double cumulativeOpeningCosts; long positionFingerprint;
};
```

| Поле | Единица / источник | Branch | Изменение | Fingerprint | Zero | Reject |
|---|---|---|---|---|---|---|
| level | count, evaluator | Base/Worst | `+1` after transition | да | initial 0 | negative/skip |
| snapshotTime | server datetime | own | next projected snapshot | да | нет | stale |
| cycleId | identity | shared | не меняется | да | нет | identity |
| stateRevision | count | own | `+1` | да | initial permitted | stale |
| Far direction | enum, broker/state | own | сохраняется на Big Harvest | да | нет | direction |
| Far lot/open | lot/price | own | lot уменьшается; price сохраняется projected | да | lot only terminal | volume/money |
| Big direction | enum opposite Far | own | rebuilt | да | нет | geometry |
| Core/Trend lot/open | lot/price, rebuilt basket | own | закрываются, затем создаются от FarRemain/current anchor | да | only terminal/policy | volume |
| Small direction | enum same Far | own | rebuilt | да | нет | geometry |
| Small lot/open | lot/price | own | closed/rebuilt | да | only terminal/policy | volume |
| anchorBid/Ask | symbol price | own | close prices текущего level становятся next anchor | да | нет | price |
| realizedCyclePL | account money, confirmed/projected deals | own | `+HarvestNet+PartialFarNet` | да | да | reconciliation |
| Partial budget | account money | own | `+PartialAdd-consumed` | да | да | ledger |
| FinalReserve | account money | own | `+ReserveAdd`; no partial debit | да | да | ledger |
| Carry | account money | own | `+CarryAdd` | да | да | ledger |
| margin/equity/free | account money/model | own | recomputed after closes/reopen | margin in fingerprint | margin can 0 | margin |
| cumulativeHarvestNet | diagnostic money | own | `+current disjoint HarvestNet` | нет | да | accounting |
| cumulativePartialFarNet | diagnostic money | own | `+current PartialFarNet` | нет | да | accounting |
| cumulativeOpeningCosts | diagnostic money | own | next basket open costs once | нет | да | cost provenance |
| positionFingerprint | deterministic hash | own | rebuilt from next state | self | нет | reconciliation |

Base и Worst имеют независимые экземпляры всех mutable полей. Identity/config могут быть shared, но ни один Base allocation, partial lot, residual Far или open price не копируется в Worst без отдельного вычисления.

## 2. Единственная последовательность level

```text
StateBefore[n]
 → Trigger[n]
 → HarvestDeals[n] (Core/Trend/Small close 100%)
 → Allocation[n]
 → PartialFarAction[n]
 → StateAfterHarvest[n]
 → NextBasket[n+1]
 → StateBefore[n+1]
```

`StateBefore[n+1] = Transition(StateBefore[n], Harvest[n], PartialFar[n], NextBasket[n+1])`.

После полного закрытия role больше не существует. Запрещено использовать `StateBefore[1]` на следующих уровнях и запрещена сумма `Σ Profit(Open[1]→Close[k])`. Единственная допустимая сумма: `Σ Profit(Open[k]→Close[k])` по непересекающимся deal intervals.

## 3. Trigger и цены

Первый level использует `Distance[1]=BigMoveStartPoints`. Для Big BUY: `BidClose=AnchorBid+Distance*Point`, `AskClose=BidClose+spread`; для Big SELL: `AskClose=AnchorAsk-Distance*Point`, `BidClose=AskClose-spread`.

После projected reopen каждый следующий level использует **только** `BigMoveStepPoints` от нового anchor. Поэтому absolute path может быть 100,150,200,250 points, но deal intervals — `0→100`, `100→150`, `150→200`, `200→250`, а не `0→100`, `0→150`, `0→200`, `0→250`.

## 4. Harvest и allocation

`HarvestNet[n]=CoreCloseNet[n]+TrendCloseNet[n]+SmallCloseNet[n]`, где каждый net вызывает broker money с direction/lot/open price из `StateBefore[n]` и close price текущего trigger. Far исключён.

`E=max(HarvestNet,0)`; `PartialAdd=MoneyRound(.10E)`; `ReserveAdd=MoneyRound(.90E)`; `CarryBase=MoneyRound(0E)`; `CarryAdd=MoneyRound(CarryBase+MoneyRound(E-PartialAdd-ReserveAdd-CarryBase))`. Требуется exact conservation в tolerance. Reserve — классификация RealizedPL, не дополнительная прибыль.

## 5. Partial Far preview

`PartialBudgetGross=PartialBudgetBefore+PartialAdd`. Для broker-valid `x`, `PartialFarNet(x)=BrokerMoney(FarDirection,x,FarOpenPrice,FarCloseSide)` и `Cost(x)=max(-PartialFarNet(x),0)`.

Solver перебирает volume step и выбирает **максимальный безопасный** `x`, где `Cost<=Budget+MoneyTolerance`, `0<=x<=FarLot`, а residual равен 0 либо `>=VolumeMin`. Residual `(0,VolumeMin)` запрещён.

Если полный Far доступен по partial budget, solver не закрывает его: возвращает `requiresFinalCloseCheck=true`. Без отдельного Final Close PASS он ограничивает partial close так, чтобы остался broker-valid Far.

`Consumed=Cost(x)`; `BudgetAfter=Gross-Consumed>=0`. FinalReserve не является input solver. `RealizedAfterPartial=RealizedBefore+HarvestNet+PartialFarNet`; отрицательный PartialFarNet уменьшает RealizedPL.

## 6. Far evolution и next basket

`FarLotNext=FarLot-PartialCloseLot`. Projected residual сохраняет Far open price. Actual state всегда перестраивается по broker reconciliation; изменение identifier/open price делает projected snapshot stale.

При residual Far:

* CoreNext=`NormalizeDown(FarRemain*BigCoreRatio)`;
* TrendNext=`NormalizeDown(FarRemain*BigTrendRatio)`;
* SmallNext=`NormalizeUp(FarRemain*SmallBaseToFarRatio)`;
* Core/Trend direction opposite Far; Small same Far.

Для Big BUY Core/Trend open по Ask текущего level, Small по Bid; для Big SELL Core/Trend по Bid, Small по Ask. Один helper владеет Bid/Ask semantics. После rounding повторяются Volume/Law1/Law2/Compression/NextBig/Gross/Margin/Worst.

## 7. Recovery names

`RecoveryPLAfterHarvestBeforeReopen=RealizedAfterPartial+FloatingNetRemainingFar-UnincludedExitCosts`.

`RecoveryPLAfterReopen=RealizedAfterPartial+FloatingNetRemainingFar+FloatingNetNextBasket-UnincludedExitCosts`. Эти значения запрещено смешивать. CumulativeHarvest — только diagnostic sum и никогда не заменяет `state.realizedCyclePL`.

## 8. Margin temporal semantics

Отдельно сохраняются MarginBeforeHarvest, ReleasedMarginFromClosedCoreTrendSmall, ReleasedMarginFromPartialFar, RemainingFarMargin, NextCore/Trend/SmallMargin, PeakExecutionMargin, SteadyStateMarginAfterReopen, WorstSteadyStateMargin.

При close-before-open workflow: `SteadyStateUpper=RemainingFarMargin+NextCoreMargin+NextTrendMargin+NextSmallMargin`; `PeakExecutionUpper=max(MarginBeforeHarvest,SteadyStateUpper)`. Если конкретный execution допускает overlap, применяется `MarginBeforeHarvest+all next margins`; overlap нельзя предполагать молча.

## 9. Base и Worst branches

`BaseState[n]` и `WorstState[n]` проходят одинаковый transition algorithm с разными profile prices/cost buffers. Каждый branch самостоятельно решает Partial Far, allocation, FarRemain, next lots/open prices, realized PL, margin, Coverage и Recovery. Общими остаются только immutable identity/config.

## 10. Invariants и PASS

Reserve nondecreasing; Far nonincreasing and strictly decreases when safe broker-valid partial exists; deficit improves минимум на configured gain; Recovery degradation ограничена `HybridAllowedMarketCostDeteriorationMoney`. Проверки применяются к последовательным states.

Level PASS требует: remaining-Far coverage, Recovery, Base and Worst, margin, allocation conservation, partial-budget conservation, temporal invariants и next-state volume. `FarRemain=0` не даёт Catch-Up PASS: это route к Projected Final Close.


## 11. Identity-complete state and immutable API

Production source uses `levelIndex`, `symbol`, `magic`, `cycleId`, `stateRevision`, `snapshotTime`, profile-specific `fingerprint`, `spread`, `terminal` and `terminalReason` in addition to the economic fields above. `symbol` is non-empty; magic/cycle/fingerprint are identity values; Bid/Ask/spread are finite and nonnegative; terminalReason is non-empty iff terminal. All economically mutable values belong separately to Base or Worst.

The API is immutable by contract:

```cpp
bool EvaluateHybridCatchUpLevel(const HybridCatchUpState &before,
                                const HybridCatchUpProfile &profile,
                                HybridHarvestLevelResult &levelResult,
                                HybridCatchUpState &after);
```

## 12. Reopen-price single owner

`BuildProjectedReopenPrices(bigDirection,levelBid,levelAsk,prices)` is the only owner of Bid/Ask reopen semantics. Big BUY opens Core/Trend at Ask and Small SELL at Bid. Big SELL opens Core/Trend at Bid and Small BUY at Ask. Actual future integration replaces projected prices with confirmed deal prices.

## 13. Commission provenance

Every state/level distinguishes `openCommissionAlreadyRealized`, `projectedOpenCommissionIncluded`, and `projectedCloseCommissionIncluded`. Existing positions use close-only projection when their open commission is already realized. A projected next basket includes its open commission once in `cumulativeOpeningCosts`; subsequent close projection must not debit it again. Close commission belongs to every actually projected close exactly once.

## 14. Result, terminal and reason contract

A level contains fingerprints, trigger prices, before/closed/after Far, four close-money results plus remaining-Far money, allocation/budget transitions, realized values, recovery-before/after-reopen, next basket, released/steady/peak/overlap margin and all invariant flags. Overall result contains independent `baseLevels[]`, `worstLevels[]`, final Base/Worst states and evaluated count.

Full-Far affordability routes to `CATCHUP_REQUIRES_FINAL_CLOSE_PREVIEW`; invalid residual to `CATCHUP_REJECT_INVALID_FAR_REMAINDER`; component min-volume to `CATCHUP_TERMINAL_MIN_VOLUME`. Other exact failures: `CATCHUP_STATE_INVALID`, `CATCHUP_TRIGGER_INVALID`, `CATCHUP_CURRENT_MONEY_FAILED`, `CATCHUP_ALLOCATION_FAILED`, `CATCHUP_PARTIAL_SOLVER_FAILED`, `CATCHUP_PARTIAL_BUDGET_FAILED`, `CATCHUP_REMAINING_FAR_MONEY_FAILED`, `CATCHUP_NEXT_BASKET_VOLUME_FAILED`, `CATCHUP_NEXT_BASKET_GEOMETRY_FAILED`, `CATCHUP_RECOVERY_FAILED`, `CATCHUP_MARGIN_FAILED`, `CATCHUP_WORST_FAILED`, `CATCHUP_TEMPORAL_INVARIANT_FAILED`, `NO_FINITE_CATCHUP_LEVEL`, `PASS`.

## 15. Worst per-leg adverse policy

Worst profile applies adverse close-side prices per leg: BUY close Bid moves down, SELL close Ask moves up. It does not rely on a shared price pair unless that pair is proven adverse for each role. Worst independently recomputes Harvest, allocation, Partial Far lot/cost, residual Far, next basket, margins, coverage and Recovery; only immutable identity/config is shared.

## 16. Margin fields

Each row retains MarginBeforeHarvest, ReleasedCore/Trend/Small/PartialFarMargin, RemainingFarMargin, NextCore/Trend/SmallMargin, SteadyStateMarginAfterReopen, PeakExecutionMargin and OverlapUpper. Close-before-open gives `Peak=max(MarginBefore,SteadyState)`; `OverlapUpper=MarginBefore+NextOrders` remains separate diagnostic evidence.

## Stage 1.2 typed outcomes, Worst execution and margin

Typed outcome/class and aggregation are normative in `HYBRID_SPLIT_BIG_CATCHUP_OUTCOME_TRUTH_TABLE.md`. Final Close routing is calculation-valid and is not a Catch-Up PASS.

Worst execution shock is non-cumulative: state retains `anchorMid`, `anchorBid/Ask` and `baselineSpread`; `lastExecutionBid/Ask` records stressed execution. Next geometric anchor is the unstressed base trigger. Profile contains independent bid/ask adverse points and `cumulativeSpreadStress=false`.

Margin uses current control side (`BUY→Ask`, `SELL→Bid`), never historical position open price merely because it is stored. `EstimatedReleasedMarginUpper` is diagnostic individual-margin sum, not actual hedging release. PASS uses `SteadyStateMarginUpper`; peak and overlap are separate.

## Stage 1.2.1 — состояние маршрута Final Close (`NORMATIVE`)

После CURRENT_LEG_MONEY, Harvest allocation и вычисления `PartialBudgetGross` выполняется `FULL_FAR_AFFORDABILITY`. Если `FullFarLoss <= PartialBudgetGross + MoneyCalculationTolerance`, обычная ветка немедленно прекращается и строится immutable `HybridFinalCloseRouteState`.

Route state сохраняет полный `FarLotBefore`, исходную цену Far, `RealizedPLBefore + HarvestNet`, полный нерасходованный `PartialBudgetGross`, `ReserveBefore + ReserveAdd`, `CarryBefore + CarryAdd`, execution Bid/Ask, full-Far money и Base/Worst provenance. Partial Far, residual Far, Next Basket, geometry, margin и RecoveryAfterReopen на route-пути не вычисляются. Route не означает Final Close PASS и не выполняет ledger или trade effects.
