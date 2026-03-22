# Test: TestAdaptiveKStability

## Description
Adaptive-k should have distribution, not constant min.

## Input

## Execution
Inspect k_eff stats.
- timestamp_utc: 2026-03-22T09:15:11.066850+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: 16.065338333371248
- extra_metrics:
  - k_eff_min: 1.1
  - k_eff_max: 1.25
  - k_eff_unique: 3

## Validation
k_eff must vary across risk zones.

## Conclusion
PASS
