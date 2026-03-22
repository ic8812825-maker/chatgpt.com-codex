# Test: TestLyapunovOptimization

## Description
Runtime action selection should improve collapse risk via non-binary control.

## Input

## Execution
Compare control OFF vs ON in jump-cluster stress.
- timestamp_utc: 2026-03-22T14:33:34.721894+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: -67.90371130135289
- extra_metrics:
  - p_off: 1.0
  - p_on: 0.3655555555555556
  - blocked: 342.92555555555555
  - compressions: 347.33444444444444

## Validation
Control ON must select protective actions and reduce collapse probability.

## Conclusion
PASS
