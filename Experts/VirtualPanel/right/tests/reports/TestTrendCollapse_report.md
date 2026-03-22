# Test: TestTrendCollapse

## Description
Trend should expose collapse risk.

## Input
- k: 1.45
- R: 90

## Execution
Run trend scenario.
- timestamp_utc: 2026-03-21T19:45:22.320715+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: 0.0
- extra_metrics:
  - p_collapse: 0.9994444444444445
  - p_lvl1: 0.9994444444444445
  - p_lvl2: 0.0
  - p_lvl3: 0.2827777777777778

## Validation
Collapse should be visible.

## Conclusion
PASS
