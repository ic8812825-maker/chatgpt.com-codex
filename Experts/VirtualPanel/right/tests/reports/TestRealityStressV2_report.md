# Test: TestRealityStressV2

## Description
Liquidity freeze + spread explosion + delayed control + slippage.

## Input

## Execution
Stress V2 comparison.
- timestamp_utc: 2026-03-22T09:15:27.075237+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: -55.6544811756367
- extra_metrics:
  - p_no_ctrl: 0.9991666666666666
  - p_ctrl: 0.024166666666666666
  - activity_ratio: 0.8207135316105346

## Validation
Preventive logic should not break under stress V2.

## Conclusion
PASS
