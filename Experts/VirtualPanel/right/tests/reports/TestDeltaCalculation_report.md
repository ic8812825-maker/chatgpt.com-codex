# Test: TestDeltaCalculation

## Description
Delta formula check.

## Input
- positions: [(1, 0.3), (1, 0.2), (-1, 0.1)]

## Execution
Direct sum.
- timestamp_utc: 2026-03-21T21:31:48.581611+00:00

## Results
- levels_before: 3
- levels_after: 3
- delta_before: 0.4
- delta_after: 0.4
- margin_before: N/A
- margin_after: N/A
- pnl: 0.0
- extra_metrics:
  - distance_from_price: False

## Validation
Δ matches formula.

## Conclusion
PASS
