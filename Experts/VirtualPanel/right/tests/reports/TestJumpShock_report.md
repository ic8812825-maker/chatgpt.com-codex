# Test: TestJumpShock

## Description
Shock should not be safer than random.

## Input
- mode: shock

## Execution
Compare random vs shock.
- timestamp_utc: 2026-03-21T19:45:28.561175+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: 0.0
- extra_metrics:
  - p_random: 0.8966666666666666
  - p_shock: 0.9727777777777777

## Validation
p_shock>=p_random

## Conclusion
PASS
