# ALE_CONTROL_LYAPUNOV_AUDIT

## Control effect on ΔV and tail-risk
| scenario | improved E[ΔV] | Δrisk | trades_executed | expansions_allowed | expansions_blocked | compressions_triggered |
|---|---:|---:|---:|---:|---:|---:|
| random | 0.000251 | 0.7167 | 79.961 | 30.477 | 49.484 | 56.060 |
| trend | 0.000421 | 0.8022 | 88.457 | 31.914 | 56.544 | 63.288 |
| adv_monotonic | 0.000720 | 0.0067 | 22.005 | 21.005 | 1.000 | 1.000 |
| adv_jump_cluster | 0.000618 | 0.6722 | 343.980 | 22.705 | 321.275 | 325.702 |
| adv_liquidity_gap | 0.000730 | 0.9278 | 148.155 | 39.938 | 108.218 | 116.825 |
| adv_liquidity_freeze | 0.000679 | 0.9933 | 246.765 | 45.400 | 201.365 | 210.039 |

## Latency/slippage stress
| delay | E[ΔV] | P(collapse) | activity_ratio | control_intensity |
|---:|---:|---:|---:|---:|
| 0 | 0.000916 | 0.0044 | 0.1550 | 0.8450 |
| 2 | 0.000975 | 0.0044 | 0.6232 | 0.3768 |
| 5 | 0.000937 | 0.0089 | 0.7506 | 0.2494 |
| 8 | 0.000965 | 0.0056 | 0.8129 | 0.1871 |
| 12 | 0.000944 | 0.0044 | 0.8599 | 0.1401 |

## Interpretation
- Overcontrol check: high control_intensity with low activity_ratio is flagged for tuning.
- Latency-sensitive growth in E[ΔV] is explicitly visible and not suppressed.
