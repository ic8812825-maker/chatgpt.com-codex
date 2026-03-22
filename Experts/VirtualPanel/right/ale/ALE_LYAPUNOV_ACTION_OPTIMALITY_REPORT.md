# ALE_LYAPUNOV_ACTION_OPTIMALITY_REPORT

## Argmin objective(a) consistency
| scenario | argmin_match | target |
|---|---:|---:|
| trend | 1.0000 | >= 0.95 |
| adv_jump_cluster | 1.0000 | >= 0.95 |
| adv_liquidity_freeze | 1.0000 | >= 0.95 |

Prediction/realization aggregate match: **1.0000** (target >= 0.95).
Fallback activations: **227**, real-best replacements: **176**.
Worst mismatch |pred-real|: **0.492170**.

## Action distribution
| action | count |
|---|---:|
| HOLD | 0 |
| EXPAND | 0 |
| COMPRESS | 313 |
| PARTIAL_CLOSE | 118 |
| SAFE | 51 |
| MICRO_EXPAND | 31 |
| SOFT_COMPRESS | 27 |

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
