# Test: TestFSMDelay

## Description
Delay worsens risk.

## Input
- fast: 1
- slow: 25

## Execution
Compare delays.
- timestamp_utc: 2026-03-21T19:45:44.726619+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: 0.0
- extra_metrics:
  - p_fast: 0.99875
  - p_slow: 0.9975
  - ttc_fast: 167.129375
  - ttc_slow: 161.895625

## Validation
Slow delay should reduce time-to-collapse.

## Conclusion
PASS
