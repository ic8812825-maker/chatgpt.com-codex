# Test: TestAdversarialScenarios

## Description
Adversarial market set.

## Input

## Execution
Run A/B per adversarial mode.
- timestamp_utc: 2026-03-22T09:15:46.923349+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: 0.0
- extra_metrics:
  - adv_monotonic_no: 0.008888888888888889
  - adv_monotonic_ctrl: 0.0
  - adv_regime_shift_no: 0.9966666666666667
  - adv_regime_shift_ctrl: 0.023333333333333334
  - adv_jump_cluster_no: 1.0
  - adv_jump_cluster_ctrl: 0.3022222222222222
  - adv_liquidity_gap_no: 0.9155555555555556
  - adv_liquidity_gap_ctrl: 0.0

## Validation
No-control adversarial risk must be non-zero.

## Conclusion
PASS
