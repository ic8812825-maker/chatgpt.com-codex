# Test: TestControlActivityAudit

## Description
Control activity metrics.

## Input

## Execution
Run controlled shock.
- timestamp_utc: 2026-03-21T21:33:41.259025+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: -0.5314334563576874
- extra_metrics:
  - trades_executed: 480.36
  - expansions_allowed: 1.764
  - expansions_blocked: 478.596
  - compressions_triggered: 2.002666666666667
  - time_in_CRITICAL: 0.014666666666666666

## Validation
System should both trade and control risk.

## Conclusion
PASS
