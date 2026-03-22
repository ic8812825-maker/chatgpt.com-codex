# Test: TestControlOverkill

## Description
Over-aggressive thresholds must be flagged.

## Input

## Execution
Run overkill config.
- timestamp_utc: 2026-03-22T09:15:01.333047+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: -0.013924692386694915
- extra_metrics:
  - p_ctrl: 0.0
  - activity_ratio: 0.0
  - control_intensity: 1.0

## Validation
Test passes if overkill is detected as bad regime.

## Conclusion
PASS
