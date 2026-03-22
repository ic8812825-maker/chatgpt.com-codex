# Test: TestLockCompression

## Description
Greedy lock monotonicity.

## Input
- positions: [(1, 0.4), (1, 0.2), (1, 0.1), (-1, 0.3), (-1, 0.2)]

## Execution
Compute d0/d1.
- timestamp_utc: 2026-03-22T09:13:17.040106+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: 0.20000000000000007
- delta_after: 0.20000000000000004
- margin_before: N/A
- margin_after: N/A
- pnl: 0.0

## Validation
|Δ_new|<=|Δ_old|

## Conclusion
PASS
