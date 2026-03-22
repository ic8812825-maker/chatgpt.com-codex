# Test: TestLyapunovDeltaFeedback

## Description
Feedback loop: worsening regime increases control intensity/blocks.

## Input

## Execution
Compare benign vs adversarial regime under control.
- timestamp_utc: 2026-03-22T13:54:54.439030+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: 10.84028588999769
- extra_metrics:
  - control_intensity_low: 0.45990022537921954
  - control_intensity_high: 0.8123698516539205
  - blocked_low: 20.17888888888889
  - blocked_high: 195.92555555555555

## Validation
High-stress regime should trigger stronger control.

## Conclusion
PASS
