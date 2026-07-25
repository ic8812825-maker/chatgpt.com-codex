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
