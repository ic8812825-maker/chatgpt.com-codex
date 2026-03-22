# Test: TestLyapunovDominance

## Description
Disable-Lyapunov comparison: ON should dominate OFF in most regimes.

## Input

## Execution
Cross-mode A/B comparison.
- timestamp_utc: 2026-03-22T14:34:18.325931+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: 0.0
- extra_metrics:
  - improved_modes: 5
  - total_modes: 6
  - by_mode: {'random': {'off': 0.7242857142857143, 'on': 0.0}, 'trend': {'off': 0.8028571428571428, 'on': 0.0}, 'adv_monotonic': {'off': 0.0, 'on': 0.0}, 'adv_jump_cluster': {'off': 1.0, 'on': 0.3057142857142857}, 'adv_liquidity_gap': {'off': 0.8842857142857142, 'on': 0.0}, 'adv_liquidity_freeze': {'off': 0.98, 'on': 0.0014285714285714286}}

## Validation
Control ON must improve collapse risk in the majority of modes.

## Conclusion
PASS
