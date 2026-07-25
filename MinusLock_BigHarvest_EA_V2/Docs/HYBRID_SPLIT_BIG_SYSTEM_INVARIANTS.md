# Hybrid Split Big — System Invariants

Нарушение любого `MUST` запрещает необратимое действие и переводит результат в reject/error/reconciliation. Safe default не заменяет failed invariant.

## Geometry

| ID | Инвариант |
|---|---|
| GEO-01 | `0 < NewFar < OldFar`. |
| GEO-02 | `NextCore + NextTrend < OldFar * MaximumNewBigToOldFarRatio`. |
| GEO-03 | В strict profile `Core > Trend` и `Core > Small`. |
| GEO-04 | После rounding повторяются volume, Law 1/2/3, gross, risk, margin, Worst Case и Future Small gates. |
| GEO-05 | Core/Trend/NewFar нормализуются DOWN; Small нормализуется UP. |

## Money

| ID | Инвариант |
|---|---|
| MONEY-01 | `FinalReserveReal >= 0`; Reserve уменьшается только подтверждённым Final Far Close. |
| MONEY-02 | PartialFarBudget не финансирует Final Close, Transition, margin или opens. |
| MONEY-03 | TransitionBudget не финансирует opens и не получает средства из FinalReserve. |
| MONEY-04 | `PartialAdd + ReserveAdd + CarryAdd = EligibleHarvest` в money tolerance. |
| MONEY-05 | Negative Harvest не создаёт Partial/Reserve/Carry credits. |
| MONEY-06 | Reserve уже входит в RealizedCyclePL и никогда не добавляется к RecoveryPL повторно. |
| MONEY-07 | Opening + confirmed credits − confirmed debits = closing для каждого bucket. |

## Identity and logic

| ID | Инвариант |
|---|---|
| LOGIC-01 | Snapshot immutable после freeze; mismatch fingerprint делает plan stale. |
| LOGIC-02 | CandidatePlan immutable после persist; execution не меняет plan silently. |
| LOGIC-03 | Ledger event idempotent в namespace и имеет ровно один commit outcome. |
| LOGIC-04 | CycleID уникален; roles идентифицируются Symbol+Magic+CycleID+identifier. |
| LOGIC-05 | Projected result никогда не подменяет confirmed actual result. |
| LOGIC-06 | Любой partial fill/reject требует reconciliation до следующего open. |

## Recovery and safety

| ID | Инвариант |
|---|---|
| REC-01 | В level model ReserveAfter не уменьшается. |
| REC-02 | CoverageDeficit не ухудшается из-за внутренней allocation/math; ухудшение обязано иметь market/cost provenance. |
| REC-03 | RecoveryPL не уменьшается из-за внутреннего double count/rounding; допустимое ухудшение имеет market, commission, swap, fee или slippage provenance. |
| SAFE-01 | Base PASS без Worst PASS не разрешает действие. |
| SAFE-02 | Terminal state запрещает opens, NewFar promotion и Reserve transfer. |

## Temporal and Far invariants

| ID | Инвариант |
|---|---|
| TIME-01 | Полностью закрытая позиция не рассчитывается и не закрывается повторно. |
| TIME-02 | Каждый Harvest использует lots/open prices только текущего `StateBefore[n]`. |
| TIME-03 | `StateBefore[n+1]` создаётся только из `StateAfter[n]`. |
| TIME-04 | Cumulative Harvest — сумма непересекающихся deals `Open[k]→Close[k]`. |
| FAR-01 | `PartialFarNet` входит в `RealizedCyclePL`. |
| FAR-02 | Partial budget consumption равен projected/actual Far loss в tolerance. |
| FAR-03 | FinalReserve отсутствует во входах Partial Far solver. |
| FAR-04 | Residual Far равен 0 либо `>=VolumeMin`. |
| FAR-05 | Следующие Core/Trend/Small рассчитываются от residual Far. |
| TIME-05 | Следующий trigger строится от anchor следующего состояния. |
| TIME-06 | Base и Worst имеют независимые последовательности states и fingerprints. |
| FAR-06 | Remaining Far close cost пересчитывается после каждого partial close. |
| FAR-07 | Full Far candidate маршрутизируется в Final Close preview, не в Partial Far completion. |
| ACC-01 | Каждый HarvestNet учитывается ровно один раз. |
| ACC-02 | Каждый PartialFarNet учитывается ровно один раз. |
| ACC-03 | Open commission каждого projected leg учитывается ровно один раз. |
| ACC-04 | Partial budget conservation выполняется на каждом level. |
| ACC-05 | Allocation conservation выполняется на каждом level. |

Temporal authority: `HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`.
| OUTCOME-01 | Route outcome is calculation-valid, not an error. |
| OUTCOME-02 | FINITE_PASS requires Base and Worst FINITE_PASS. |
| OUTCOME-03 | ERROR and TERMINAL dominate per outcome truth table. |
| OUTCOME-04 | ReasonCode is a stable typed code, not free text. |
| WORST-01 | Execution adverse spread never changes baseline spread. |
| WORST-02 | With cumulativeSpreadStress=false shock applies once per level. |
| WORST-03 | Worst leg net cannot improve over Base without provenance. |
| MARGIN-01 | Margin control price uses current market side. |
| MARGIN-02 | Historical open price is not automatic margin control price. |
| MARGIN-03 | EstimatedReleasedMarginUpper is not actual release. |
| MARGIN-04 | PASS uses conservative state-after margin upper bound. |

## Final Close route invariants — Stage 1.2.1

- **ROUTE-INV-01:** full-affordability route не выполняет Partial Far.
- **ROUTE-INV-02:** `FarLotForFinalClosePreview == FarLotBefore`.
- **ROUTE-INV-03:** `PartialBudgetConsumed == 0`.
- **ROUTE-INV-04:** route budget равен `PartialBudgetBefore + PartialAdd`.
- **ROUTE-INV-05:** route RealizedPL включает Harvest и не включает PartialFarNet.
- **ROUTE-INV-06:** Next Basket при route не строится.
- **ROUTE-INV-07:** geometry, margin и reopen Recovery не участвуют в route outcome.
- **ROUTE-INV-08:** aggregate route требует Base route и Worst route.
- **ROUTE-INV-09:** mixed Route/Continue и Route/Success являются divergence.
- **ROUTE-INV-10:** Worst adverse validation выполняется только для полностью рассчитанных current legs.

## Route hardening invariants — Stage 1.2.2
- **ROUTE-VALID-01:** route state проходит отдельную строгую валидацию.
- **ROUTE-VALID-02:** builder успешен только после validator PASS.
- **ROUTE-VALID-03:** fingerprint охватывает Far, money, allocation, Carry и обе revisions.
- **ROUTE-VALID-04:** gross budget берётся из `partial.budgetGross`.
- **ROUTE-VALID-05:** route не имеет valid continuation state.
- **ROUTE-VALID-06:** aggregate route хранит две valid Base/Worst route states.
- **ROUTE-VALID-07:** source и route revision различаются ровно на один.
- **ROUTE-VALID-08:** Full Far adverse check имеет evaluated/pass status.
- **ROUTE-FP-01…08:** одинаковое состояние даёт тот же hash; Far, execution price, gross budget, Reserve, Carry, full-Far commission или route revision меняют hash.
- **ROUTE-REV-01…04:** source revision равна before revision; route revision равна source+1; обе входят в fingerprint.

## Dimension-safe route invariants — Stage 1.2.3
- **ROUTE-TOL-01:** money tolerance не применяется к lot или price.
- **ROUTE-TOL-02:** изменение Far на один volume step отклоняется.
- **ROUTE-TOL-03:** изменение price на один broker point отклоняется.
- **ROUTE-TOL-04:** floating representation noise меньше typed tolerance допускается.
- **ROUTE-TOL-05:** `routeCandidate=true` обязателен и включён в fingerprint.
- **ROUTE-TOL-06:** Full-Far adverse flags равны false/false при NOT_APPLICABLE.

## Full Catch-Up dimensions — Stage 1.2.4
- **DIM-INV-01:** `MoneyCalculationTolerance` применяется только к account money.
- **DIM-INV-02:** lot comparisons используют symbol-aware lot tolerance.
- **DIM-INV-03:** price comparisons используют symbol-aware price tolerance.
- **DIM-INV-04:** ratio comparisons используют ratio tolerance.
- **DIM-INV-05:** margin level/usage используют percent tolerance.
- **DIM-INV-06:** points не сравниваются money/price tolerance.
- **DIM-INV-07:** Far ниже `SYMBOL_VOLUME_MIN` не продолжает Catch-Up.
- **DIM-INV-08:** строгая Far compression превышает lot tolerance.
- **DIM-INV-09:** New Big на лимите отклоняется.
- **DIM-INV-10:** Worst helpers получают symbol из обязательного source context.

## Stage 1.2.4.1 money/Partial clarification

- `HybridMoneyEqual(a,b)` проверяет ledger-normalized значения: `abs(Round2(a)-Round2(b)) <= MoneyCalculationTolerance`.
- `HybridMoneyGreater`, `HybridMoneyGreaterOrEqual`, `HybridMoneyLessOrEqual` применяются к raw projected money без предварительного округления и реализуют консервативные boundary inequalities.
- Partial margin существует только при `HybridLotGreater(symbol,partialLot,0.0)`; noise внутри lot tolerance не вызывает Partial margin calculation.
