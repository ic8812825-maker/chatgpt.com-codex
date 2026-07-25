# Hybrid Split Big — нормативные алгоритмы MQL5

**Статус:** нормативный контракт этапа 0. Торговая интеграция до завершения этапов 1–6 запрещена.

## 1. Нормативный `HybridCycleState`

Состояние строится как immutable snapshot. Числа должны быть конечными; деньги — валюта счёта, цены — цена символа, lot — broker volume, distances — points.

| Группа / поле | Тип | Источник и диапазон | Момент обновления | Persist | Ошибка mismatch |
|---|---|---|---|---|---|
| Symbol | string | runtime symbol, non-empty | создание цикла | да | `HYBRID_ERROR_INVALID_SNAPSHOT` |
| Magic | ulong | EA input, `>0` | создание цикла | да | `HYBRID_ERROR_INVALID_SNAPSHOT` |
| CycleID | ulong | monotonic cycle id, `>0` | новый цикл | да | `HYBRID_ERROR_RECONCILIATION` |
| StateRevision | ulong | monotonic, `>=1` | confirmed transition | да | `HYBRID_ERROR_RECONCILIATION` |
| SnapshotTime | datetime | server time | каждый freeze | да | `HYBRID_ERROR_STALE_SNAPSHOT` |
| PositionFingerprint | long | hash roles/identifiers/lots | каждый freeze | да | `HYBRID_ERROR_RECONCILIATION` |
| Far direction/ticket/identifier/lot/openPrice | enum/ulong/ulong/double/double | broker positions; identifiers and lot/price positive | confirmed deal/reconciliation | да | `HYBRID_ERROR_RECONCILIATION` |
| Core direction/ticket/identifier/lot/openPrice | same | broker; zero lot only when component absent by approved policy | confirmed open/close | да | `HYBRID_ERROR_RECONCILIATION` |
| Trend direction/ticket/identifier/lot/openPrice | same | broker | confirmed open/close | да | `HYBRID_ERROR_RECONCILIATION` |
| Small direction/ticket/identifier/lot/openPrice | same | broker | confirmed open/close | да | `HYBRID_ERROR_RECONCILIATION` |
| RealizedCyclePL | double money | confirmed deals only | after deal reconciliation | да | `HYBRID_ERROR_RESERVE_LEDGER` |
| FinalReserveReal | double money, `>=0` | confirmed allocation | harvest/final-Far debit | да | `HYBRID_ERROR_RESERVE_LEDGER` |
| PartialFarBudgetAvailable/Consumed | double money, `>=0` | partial bucket ledger | confirmed credit/debit | да | `HYBRID_ERROR_RESERVE_LEDGER` |
| TransitionBudgetAvailable/Consumed | double money, `>=0` | transition ledger | confirmed credit/debit | да | `HYBRID_ERROR_RESERVE_LEDGER` |
| CarryAvailable | double money, `>=0` | allocation plus residual | confirmed harvest | да | `HYBRID_ERROR_RESERVE_LEDGER` |
| CumulativeTransitionLoss | double money, `>=0` | `old+max(-TransitionNet,0)` | confirmed transition | да | `HYBRID_ERROR_RECONCILIATION` |
| HarvestLevel/ReverseCycle | int, `>=0` | state machine | confirmed level/transition | да | `HYBRID_ERROR_RECONCILIATION` |
| BigTriggerPrice/SmallTriggerPrice/FarControlPrice | double price, `>0` | geometry/market model | frozen plan | да | `HYBRID_ERROR_INVALID_SNAPSHOT` |
| OldRisk/NextRisk/WorstOldRisk/WorstNextRisk | double money, `>=0` | risk model | evaluation only | вместе с plan | `HYBRID_ERROR_ORDER_CALC_PROFIT` |
| CurrentMargin/ReleasedMargin/NewOrderMargin/ConservativeUpper | double money, `>=0` | account/OrderCalcMargin | evaluation/reconciliation | вместе с plan | `HYBRID_ERROR_ORDER_CALC_MARGIN` |

Ticket — routing handle, identifier — stable identity. Reconciliation всегда использует `Symbol+Magic+CycleID+identifier`, а не ticket отдельно.

## 2. Нормативная таблица Harvest level

Для каждого `n=1..MaxHarvestLevels` создаётся отдельная строка; денежные результаты другого уровня переиспользовать запрещено. `D_n=BigMoveStartPoints+(n-1)BigMoveStepPoints`. Для Big BUY: `Bid_n=Bid_0+D_n*Point`, `Ask_n=Bid_n+Spread_n`; для Big SELL: `Ask_n=Ask_0-D_n*Point`, `Bid_n=Ask_n-Spread_n`.

На каждой паре Bid/Ask заново вызывается broker money adapter для Far/Core/Trend/Small. Строка содержит: LevelIndex, LevelPriceBid/Ask; четыре CloseNet; HarvestGross/Costs/Net; EligibleHarvestNet; Partial/Reserve/Carry Add; три bucket After; FarCloseCost; CoverageDeficit; projected realized/floating/exit costs/RecoveryPL; base/worst margin and risk; BasePass/WorstPass/FiniteCatchUpPass.

`HarvestNet_n=CoreNet_n+TrendNet_n+SmallNet_n`; Far не входит, пока не закрывается. `E_n=max(HarvestNet_n,0)`. При утверждённых `alpha=.10,beta=.90,gamma=.00`: `PartialAdd=money_round(alpha*E)`, `ReserveAdd=money_round(beta*E)`, `CarryBase=money_round(gamma*E)`, residual и только residual добавляется в Carry. Conservation обязателен.

`FarCloseCost_n=max(-FarCloseNet_n,0)+CoverageSafetyBuffer`; использовать `-HarvestNet` вместо Far cost запрещено. `ReserveAfter_n=ReserveBefore+sum(ReserveAdd_k)` и `CoverageDeficit_n=FarCloseCost_n-ReserveAfter_n`. Для соседних уровней требуется `Deficit[n+1] <= Deficit[n]-MinimumCoverageGainMoney`.

`RecoveryPL_n=RealizedCyclePLProjected_n+FloatingManagedPL_n-ExpectedExitCosts_n`. PASS существует только при одном конечном уровне, где одновременно deficit `<=0`, RecoveryPL `>=MinimumRecoveryProfitMoney`, Base margin, Worst margin и Worst Case проходят.

## 3. Risk control price

`OldRiskControlPrice` — ближайший неблагоприятный обязательный trigger текущей корзины. `NextRiskControlPrice` — будущий Small trigger следующей корзины. `WorstRiskControlPrice` — тот же trigger, смещённый против позиции на spread-expansion, slippage и gap buffers.

Каждый leg считается `OrderCalcProfit`-совместимым adapter. `BasketRisk(Pc)=max(-sum(Net_i(Pc)),0)+UnincludedCosts`. В costs входят только ещё не включённые commission/swap/fee/buffers. Требуются `RiskNext+RiskSafetyBuffer<RiskOld` и аналогичное strict inequality для Worst Risk. Формула `nextRisk=oldRisk*q` запрещена.

## 4. Единый дискретный NewFar Solver

Один Solver используется Pre-open, Small Transition, Future Small и Restart reconciliation. Перебор идёт от `VolumeMin` вверх по `VolumeStep`, пока `N<OldFar`: NewFar DOWN; CoreNext DOWN; TrendNext DOWN; SmallNext UP. Для каждого кандидата заново считаются TransitionNet, cumulative loss, Law 1, Law 2, NextBig, GrossNext, RiskNext, MarginNext, finite Catch-Up, Worst Case и Future Small. Первый полный PASS побеждает.

`TargetNewFarRatio` — только preferred/upper search policy; fixed target не является решением. Нормативный порядок gate: Volume → Rounding → Transition → CumulativeLoss → Law1 → Law2 → NextBig → Gross → Risk → Margin → FiniteCatchUp → WorstCase → FutureSmall.

## 5. Future Small State Transition

На каждом depth создаётся новый state, старый vector/snapshot не мутируется и не переиспользуется: вычисляются trigger Bid/Ask и projected deals четырёх roles; TransitionNet; debit только TransitionBudget; cumulative loss; подтверждённый residual Core; новый Far; разворот Far/Big/Small directions; новые open prices и C/T/S; risk, margin, finite Catch-Up, Worst Case; новый fingerprint. FinalReserve переносится без debit.

Fingerprint включает direction, normalized lots, rounded trigger, reserve, transition budget, cumulative loss и depth. Повтор, `q>=1`, max depth или max nodes завершается точным reject/terminal code, а не PASS.

## 6. Final Close

`ProjectedFinalRecoveryPL=RealizedCyclePLBefore+ProjectedCloseNetAllManaged-UnincludedCosts`. Gate `FINAL_CLOSE_PREVIEW_PASS` возможен только при `ProjectedFinalRecoveryPL >= MinimumRecoveryProfitMoney+FinalCloseSafetyBuffer`.

`ActualFinalRecoveryPL=RealizedCyclePLAfterAllConfirmedDeals`. Финальное `CYCLE_CLOSED_PROFIT` возможно только при `ManagedPositions==0` и `ActualFinalRecoveryPL>=MinimumRecoveryProfitMoney-tolerance`. Иначе — mismatch/error/terminal. FinalReserve может оплатить только Final Far close и не добавляется повторно в RecoveryPL.

## 7. Money ledger transactions

| Bucket | Credit | Разрешённый debit | Запрещено | Event key / persistence |
|---|---|---|---|---|
| RealizedCyclePL | confirmed deal net | reset only | projected values | deal id; persisted |
| FinalReserveReal | confirmed Harvest reserve | Final Far close | Partial, Transition, margin, opens | cycle/harvest/reserve; persisted |
| PartialFarBudget | confirmed Harvest partial | confirmed Partial Far cost | Transition/opens | cycle/harvest/partial; persisted |
| TransitionBudget | approved credits | confirmed transition cost | FinalReserve source | cycle/reverse/transition; persisted |
| Carry | allocation base + residual | only approved carry policy | implicit reserve transfer | cycle/harvest/carry; persisted |
| CumulativeTransitionLoss | confirmed `max(-net,0)` | reset at closed cycle | decrement/reclassification | cycle/reverse/loss; persisted |

Порядок: PREPARED → EVENT_WRITTEN → CACHE_UPDATED → RECONCILED → COMPLETED. Event key уникален в namespace; replay не меняет balance. Для каждого bucket `opening+credits-debits=closing`.

## 8. State Machine mapping

| Событие | Preconditions / immutable plan | Pending / expected actual | Next | Error / terminal |
|---|---|---|---|---|
| Pre-open | reconciled Far, all gates pass, matching fingerprint | persist plan; C→T→S confirms | Hybrid active | partial basket → reconciliation/manual hold |
| Big Harvest | frozen identities/prices, Base+Worst pass | close Core→Trend→Small; confirmed deals | allocate buckets; Final Close or continuation | mismatch → terminal |
| Small Transition | full solver plan, Transition budget | close Small→Far→Trend→Core part; confirm residual | promote residual and atomic next basket | partial/mismatch → reconciliation |
| Final Close | projected gate pass | confirmed close for every managed identifier | closed profit | actual mismatch → terminal |
| Restart | persisted pending stage and ledger | rebuild by Symbol/Magic/CycleID/identifier | resume idempotently or active | no new opens until reconciled |
| Limited risk reduction | terminal, provable WorstRisk decrease | close-only action | re-run Final Close | unsafe/no action → Manual Hold |

До этапа 7 эта таблица является контрактом, но не разрешением подключать evaluator к торговому execution.

## Нормативные companion contracts

Неизменяемые требования вынесены в `HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`; допустимые переходы — в `HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md`; порядок gates — в `HYBRID_SPLIT_BIG_GATE_GRAPH.md`; разрешённые денежные рёбра — в `HYBRID_SPLIT_BIG_MONEY_FLOW.md`; формат воспроизводимого журнала — в `HYBRID_SPLIT_BIG_TRACE_SPEC.md`. Эти документы имеют такую же нормативную силу, как главы 1–8.
