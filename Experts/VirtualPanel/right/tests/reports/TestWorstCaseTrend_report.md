# Test: TestWorstCaseTrend

## Description
Deterministic one-way trend.

## Input
- trends: [1000, 3000, 5000, 10000, 20000]

## Execution
Compute safe deposits.
- timestamp_utc: 2026-03-21T19:45:41.748552+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: 0.0
- extra_metrics:
  - table: [(1000, 373.93175775916524), (3000, 116525.83827980765), (5000, 116804.497119855), (10000, 117501.14421997344), (20000, 118894.43842021027)]

## Validation
Safe deposit should rise with trend.

## Conclusion
PASS
