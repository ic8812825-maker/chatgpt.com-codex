# Test: TestRiskReturnEfficiency

## Description
Pareto-like comparison ALE vs ALC vs CONTROL.

## Input

## Execution
3-way comparison.
- timestamp_utc: 2026-03-22T09:14:53.242694+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: 11.492797901307368
- extra_metrics:
  - p_ale: 0.6377777777777778
  - p_alc: 0.48388888888888887
  - p_ctrl: 0.0
  - pnl_ale: -52.05909224135212
  - pnl_alc: -57.99349878605694
  - pnl_ctrl: 11.492797901307368

## Validation
Control should improve risk-return efficiency.

## Conclusion
PASS
