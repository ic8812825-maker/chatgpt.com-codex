# Test: TestLyapunovRecoveryRelease

## Description
Feedback loop: when stress drops, control relaxes or activity recovers.

## Input

## Execution
Compare stressed vs recovery regime under control.
- timestamp_utc: 2026-03-22T13:55:03.655740+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: 9.7372985038457
- extra_metrics:
  - activity_stressed: 0.2658594463933025
  - activity_recovered: 0.6030736946056042
  - control_stressed: 0.7341405536066975
  - control_recovered: 0.3969263053943957

## Validation
Control should not stay locked at stressed intensity after recovery.

## Conclusion
PASS
