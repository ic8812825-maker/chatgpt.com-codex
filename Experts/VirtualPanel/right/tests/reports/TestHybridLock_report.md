# Test: TestHybridLock

## Description
Hybrid lock should use brute-force for N<=12.

## Input
- N: 5

## Execution
Compare greedy/hybrid.
- timestamp_utc: 2026-03-21T21:31:48.581448+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: 0.20000000000000007
- delta_after: 0
- margin_before: N/A
- margin_after: N/A
- pnl: 0.0
- extra_metrics:
  - greedy_abs: 0.20000000000000004
  - mode: bruteforce

## Validation
Hybrid no worse than greedy.

## Conclusion
PASS
