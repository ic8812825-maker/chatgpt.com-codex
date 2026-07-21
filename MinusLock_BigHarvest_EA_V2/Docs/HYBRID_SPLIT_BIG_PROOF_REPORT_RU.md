# Hybrid Split Big — инженерно-математический proof report

## Статусы доказательства

| Этап | Статус |
|---|---|
| MQL5_FORMULAS_EXTRACTED | PASS |
| CODE_MATCHES_DESIGN | CONDITIONAL_PASS |
| BEST_PARETO_SELECTED | PASS |
| LAW_1_ANALYTICALLY_PROVED | PASS в заявленной допустимой геометрии |
| LAW_1_NUMERICALLY_PROVED | CONDITIONAL_PASS: broker-model scenarios; MT5 pending |
| LAW_2_ANALYTICALLY_PROVED | PASS в заявленной допустимой геометрии |
| LAW_2_NUMERICALLY_PROVED | CONDITIONAL_PASS: MQL runtime gate added, MetaEditor pending |
| LAW_3_ANALYTICALLY_PROVED | CONDITIONAL_PASS |
| LAW_3_NUMERICALLY_PROVED | CONDITIONAL_PASS: valid-plan domain only |
| STRESS_TESTS_PASSED | CONDITIONAL_PASS: unsafe combinations are rejected by gate |
| BROKER_ROUNDING_PASSED | CONDITIONAL_PASS: modelled 0.001/0.01/0.10 |
| SMALL_SCENARIO_COMPLETION_PASSED | NOT_PROVED: requires terminal fills/restart |
| METAEDITOR_COMPILED | BLOCKED |
| MT5_STRATEGY_TESTED | BLOCKED |
| FINAL_PROOF_APPROVED | NOT_PROVED |

**Следствие:** окончательный manual не создаётся: это было бы ложным
утверждением полного PASS до MetaEditor и MT5 execution evidence.

## 1. Извлечённая фактическая математика

| Величина | MQL5 файл / функция | Фактическая формула и контроль |
|---|---|---|
| C,T,S | `StateMachine.mqh: PrepareSplitBigLevel`; `CalcBig*Lot` | broker `NormalizeLotDown(F*ratio)` |
| Net Big | `HybridGeometrySolver: SolveHybridGeometry` | `C+T-S-F`, затем `MinimumNetBigExposureLots` |
| Recovery | `EvaluateHybridProjectedRecoveryAtPrice` | sum broker projected net F/C/T/S at one Bid/Ask-aware mid price |
| Recovery trace | `ValidateHybridRecoveryMonotonicity` | every point `0..BigTarget+max(500,FarDistance)` |
| Reserve slope | `SolveHybridGeometry` | `β(C+T-S)V/FV`, separate from Recovery slope |
| Target / close C | `CalcTargetNewFarLot`; `BuildHybridReversePlan` | `N=floor(F*TargetNewFarRatio)`, `CloseC=floor(C-N)` |
| Transition net | `BuildHybridReversePlan` | actual broker-model nets S+F+T+closed C; Final Reserve excluded |
| next Big | `PreviewNextSplitGeometry` | floor ratios from actual N; `Gnext=Cnext+Tnext` |
| actual NewFar | `ProcessSplitSmallCloseCorePart` | terminal `GetActualPositionVolume`, then preview again |

MQL5 prices use `BrokerClosePriceAtMid` and the broker money functions, which
route BUY/Sell closes through the correct Bid/Ask. Net calculations include the
underlying commission/spread/slippage/swap/fee model; the proof harness is a
mirror only and cannot replace terminal fills.

## 2. Три закона: аналитика

Пусть `F>0`, `C=cF`, `T=tF`, `S=sF`, `β=ReserveShare`, `V>0`.

**Law 1.** Necessary and sufficient linear slope condition is
`β(c+t-s) >= r`, где `r=MinimumReserveCatchUpRatio>1`. Тогда
`ΔProjectedCoverage/ΔFarLoss=β(C+T-S)/F>=r`; fees are constant over a local
price step and are separately covered by the runtime broker-net trace. Actual
Reserve remains ledger-only after harvest; projected coverage never mutates it.

**Law 2.** The full-basket derivative is `V(C+T-S-F)`. Thus `C+T-S-F>0` is
necessary and sufficient absent discontinuous costs. The EA now evaluates the
same broker monetary close at **every point**, not merely at Big target, and
rejects a basket whose increment is below `MinimumRecoverySlopeMoneyPerPoint`.

**Law 3.** For actual residual `N`, `q=N/F`. Valid promotion requires `0<q<1`,
next recovery/catch-up/margin gates and `Gnext=Cnext+Tnext<F` when configured.
With `q<=qMax<1`, `Nreverse<=ceil(log(Fmin/F0)/log(qMax))+1`. For q=.30,
Fmin=.01: F=.05/.10/.50/1/2/5/10 requires 4/4/5/5/6/6/7 reverse steps before
rounding terminal close. `F=Fmin` is terminal, not a valid reverse candidate.

## 3. Выбранный кандидат и Pareto comparison

Выбран `core_target`: `c=2.00,t=.80,s=.20,β=.90,qTarget=.30`,
`r=1.10`, `Gnext limit=.99`, baseline F=1, step=.01. После rounding:
`C=2,T=.8,S=.2, Net=1.6, CatchUp=2.34, N=.3, Gnext=.84,
Enext=.48`. Он выбран не по одному score: одновременно даёт positive slope,
catch-up margin 1.24, 70% Far compression, gross next Big below F and positive
transition model. Полная таблица шести кандидатов находится в
`Reports/HYBRID_PARETO_COMPARISON.csv`.

## 4. Численная область и сценарии

`Tools/prove_hybrid_split_big.py` детерминированно генерирует:

* `HYBRID_BIG_100_SCENARIOS.csv`: 100 уникальных combinations Far, distance,
  lot step, expenses and six mandatory moves (600 rows).
* `HYBRID_SMALL_100_REVERSALS.csv`: 100 rounded reverse attempts.
* `HYBRID_STRESS_TEST.csv`: 60 combinations spread 1/2/3/5, commission 1/2/3,
  slippage 0..50.
* `HYBRID_COUNTEREXAMPLES.csv`: intentionally rejected geometry.

Counterexamples are not hidden: weak catch-up, excessive next Big and negative
transition are rejected with `RESERVE_CATCHUP`, `NEW_BIG_GROSS_EXPOSURE` or
`TRANSITION_LOSS`. For F equal to broker minimum, strict compression is
mathematically impossible; correct action is final-close/manual gate, never
promotion of an equal Far.

## 5. Stress and Small completion finding

The reports distinguish **PASS** from **safe rejection**. Elevated costs can
make a proposed transition net negative. The planner rejects it before OldFar
close; this preserves the three invariants but does not prove that every
requested transition completes. Therefore it is `CONDITIONAL_PASS`, not PASS.
The required terminal assertions — actual history nets, partial fills, pending
retry, restart recovery, no orphan and one-time promotion — remain impossible
to prove in this container.

## 6. Изменение после поиска контрпримеров

The prior implementation checked recovery only at coarse points. A local
counterexample could exist between those points. It was corrected by adding
`EvaluateHybridProjectedRecoveryAtPrice` and a per-point MQL5 loop through
`BigTarget+max(500,FarDistance)`. The next Big gross definition was also
corrected to `Core+Trend`, explicitly excluding SmallBase.

## 7. Итог

No claim of FINAL_APPROVED is made. Laws 1/2 are analytically established for
accepted rounded geometries; Law 3 is established only for successfully
executed plans, while execution/restart requires MT5. The safe operational
contract is: **reject geometry/plan on any missing proof condition; do not
trade hybrid live until MetaEditor and real-tick MT5 evidence upgrades all
conditional statuses to PASS.**
