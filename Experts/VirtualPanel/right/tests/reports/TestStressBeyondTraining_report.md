# Test: TestStressBeyondTraining

## Description
Out-of-range stress (k=2.0, R=50, depth>50).

## Input

## Execution
Run adversarial monotonic.
- timestamp_utc: 2026-03-21T21:34:40.491663+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: -11.3321793638028
- extra_metrics:
  - p_collapse: 1.0
  - avg_depth: 12.0

## Validation
Model should expose non-zero failure beyond training.

## Conclusion
PASS
