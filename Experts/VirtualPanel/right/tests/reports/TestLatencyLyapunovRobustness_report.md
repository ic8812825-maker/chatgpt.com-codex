# Test: TestLatencyLyapunovRobustness

## Description
Latency degradation check for Lyapunov control.

## Input

## Execution
Delay sweep.
- timestamp_utc: 2026-03-22T15:10:25.771190+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: 0.0
- extra_metrics:
  - p0: 0.007142857142857143
  - pmax: 0.008571428571428572
  - rows: [(0, 0.007142857142857143), (2, 0.002857142857142857), (5, 0.008571428571428572), (8, 0.004285714285714286), (12, 0.0014285714285714286)]

## Validation
Collapse should not explode with delay.

## Conclusion
PASS
