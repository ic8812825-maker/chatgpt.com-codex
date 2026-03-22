# Test: TestProfitConstrainedControl

## Description
Hard activity/profit constraints for control.

## Input

## Execution
A/B baseline vs control in normal regime.
- timestamp_utc: 2026-03-22T09:14:32.115646+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: 13.688737863005608
- extra_metrics:
  - p_base: 0.4412
  - p_ctrl: 0.0
  - pnl_base: -45.73503018669821
  - pnl_ctrl: 13.688737863005608
  - activity_ratio: 0.457166654134686
  - trade_rate: 0.10639446153846155
  - control_intensity: 0.542833345865314
  - fake_safety: False

## Validation
Must cut risk without killing activity/profit.

## Conclusion
PASS
