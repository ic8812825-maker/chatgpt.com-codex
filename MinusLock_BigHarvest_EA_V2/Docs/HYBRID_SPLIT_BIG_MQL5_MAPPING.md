# Hybrid Split Big — MQL5 mapping, этап 2

| Нормативное требование | MQL5 функция | Gate code | Test | Статус |
| --- | --- | --- | --- | --- |
| Hybrid opt-in без торговли при disabled | `EvaluateHybridCandidate` | `HYBRID_FINAL_NONE` / `HYBRID_DISABLED` | `HybridDecisionEngineTests.mq5` | PARTIALLY_COVERED |
| Identity snapshot validation | `ValidateHybridSnapshot` | `HYBRID_GATE_IDENTITY` | fixture invalid symbol/cycle | PARTIALLY_COVERED |
| Отдельные Hybrid allocation inputs | `ValidateHybridAllocationConfig` | `HYBRID_GATE_CONFIG` | allocation fixture | PARTIALLY_COVERED |
| SmallBase UP, Core/Trend/NewFar DOWN | `NormalizeHybridSmallLot`, `NormalizeHybridCoreLot`, `NormalizeHybridTrendLot`, `NormalizeHybridNewFarLot` | `HYBRID_GATE_ROUNDING` | rounding fixture | PARTIALLY_COVERED |
| Law 1 uses `HybridFinalReserveShare` | `EvaluateHybridCandidate` | `HYBRID_GATE_LAW1` | β=0.70 current geometry rejects | PARTIALLY_COVERED |
| Law 2 lot/money slope | `EvaluateHybridCandidate` | `HYBRID_GATE_LAW2` | slope fixture | PARTIALLY_COVERED |
| Base money preview via broker model | `EvaluateHybridBaseMoneyPreview` | `HYBRID_GATE_BASE_MONEY` | fixture | PARTIALLY_COVERED |
| Finite Catch-Up preview | `EvaluateHybridFiniteCatchUpPreview` | `HYBRID_GATE_FINITE_CATCHUP` | fixture | PARTIALLY_COVERED |
| NextBig and Gross compression | `EvaluateHybridCandidate` | `HYBRID_GATE_NEXT_BIG`, `HYBRID_GATE_GROSS` | fixtures | PARTIALLY_COVERED |
| Candidate margin preview | `EvaluateHybridCandidateMargin` | `HYBRID_GATE_MARGIN` | fixture | PARTIALLY_COVERED |
| Worst Case preview | `EvaluateHybridWorstCasePreview` | `HYBRID_GATE_WORST_CASE` | fixture | PARTIALLY_COVERED |
| Future Small depth-1 preview | `EvaluateHybridFutureSmallDepth1` | `HYBRID_GATE_FUTURE_SMALL` | fixture | PARTIALLY_COVERED |
| No execution integration in stage 2 | no StateMachine open/close call | n/a | scope diff | FULLY_COVERED |
| ADM-MQL5-05 allocation `.10/.90/.00` | `ValidateHybridAllocationConfig` / `EvaluateHybridCandidate` | `HYBRID_GATE_CONFIG`, `HYBRID_GATE_LAW1` | MQL5 parity pending | PARTIALLY_COVERED |
| Normative immutable cycle state | Stage 0 contract; implementation pending | identity/reconciliation | pending | NOT_COVERED |
| Level-by-level Harvest table | Stage 1 | finite Catch-Up | FC-01..FC-10 pending | NOT_COVERED |
| Money-based basket risk | Stage 2 | `HYBRID_GATE_RISK` | RK-01..RK-08 pending | NOT_COVERED |
| Unified NewFar Solver | Stage 3 | `HYBRID_GATE_NEW_FAR` | pending | NOT_COVERED |
| Recursive Future Small | Stage 4 | `HYBRID_GATE_FUTURE_SMALL` | pending | NOT_COVERED |
| Projected/actual Final Close | Stage 5 | final preview/actual | pending | NOT_COVERED |
| Persisted money ledger | Stage 6 | reconciliation | pending | NOT_COVERED |
