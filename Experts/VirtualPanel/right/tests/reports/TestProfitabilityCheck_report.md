# Test: TestProfitabilityCheck

## Description
PnL with/without control.

## Input

## Execution
Compare no-control vs control.
- timestamp_utc: 2026-03-21T21:34:06.952057+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: -0.0981671572876894
- extra_metrics:
  - pnl_no_control: -14.055650769321035
  - pnl_control: -0.0981671572876894
  - p_collapse_no_control: 0.031
  - p_collapse_control: 0.0

## Validation
Control should reduce risk without zeroing activity.

## Conclusion
PASS
