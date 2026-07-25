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
