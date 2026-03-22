# ALE_LYAPUNOV_ACTION_OPTIMALITY_REPORT

## Argmin objective(a) consistency
| scenario | argmin_match | target |
|---|---:|---:|
| trend | 1.0000 | >= 0.95 |
| adv_jump_cluster | 1.0000 | >= 0.95 |
| adv_liquidity_freeze | 1.0000 | >= 0.95 |

Prediction/realization aggregate match: **1.0000** (target >= 0.95).
Fallback activations: **514**, real-best replacements: **2**.
Worst mismatch |pred-real|: **0.492170**.

## Action distribution
| action | count |
|---|---:|
| HOLD | 0 |
| EXPAND | 0 |
| COMPRESS | 28 |
| PARTIAL_CLOSE | 0 |
| SAFE | 512 |
| MICRO_EXPAND | 0 |
| SOFT_COMPRESS | 0 |

## Action evaluation coverage (all actions must be evaluated in argmin set)
| action | evaluated_count |
|---|---:|
| HOLD | 540 |
| EXPAND | 540 |
| COMPRESS | 540 |
| PARTIAL_CLOSE | 540 |
| SAFE | 540 |
| MICRO_EXPAND | 540 |
| SOFT_COMPRESS | 540 |
