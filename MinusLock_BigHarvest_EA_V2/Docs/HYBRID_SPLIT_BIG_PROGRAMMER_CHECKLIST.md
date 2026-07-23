# Hybrid Split Big — чек-лист внедрения MQL5

1. Add immutable CycleID and role identifiers to every managed position/deal.
2. Implement one money adapter around `OrderCalcProfit` with directional Bid/Ask and explicit included-cost flags.
3. Implement `OrderCalcMargin` basket adapter including broker hedging behaviour.
4. Keep separate ledgers for realized P/L, Final Reserve, Partial Far budget and Transition Budget.
5. Enforce idempotent reserve event keys; never add reserve to Recovery P/L.
6. Normalize all volumes with explicit Down/Up/Nearest policies; rerun every gate afterwards.
7. Build every configured Harvest level and reject if no finite coverage level exists.
8. Build Future Small before any C/T/S open; enumerate broker-step NewFar candidates ascending.
9. Use `TransitionNet >= -MaximumAllowedTransitionLoss`; do not overload it with a minimum-profit parameter.
10. Require strict actual `NewFar<OldFar`, NextBig/gross/risk reductions and next-cycle validation.
11. Require Base and Worst Case PASS before an irreversible trade action.
12. Persist plan, prices, expected lots, event keys and version before first close.
13. Execute Small: SmallBase → OldFar → BigTrend → partial BigCore.
14. After each deal query actual history/position state, reconcile volume and money, then decide whether continuation is allowed.
15. On mismatch/error: do not open a compensating leg; enter terminal-safe/reconciliation path.
16. Log all fields from chapter 29 of the manual and add tester assertions for all vectors.
17. Compile in MetaEditor and validate real ticks, spread shocks, restart, partial fill and order rejection before live enablement.
