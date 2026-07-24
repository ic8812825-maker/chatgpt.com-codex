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
