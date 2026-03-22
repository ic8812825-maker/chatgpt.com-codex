# ALE_CONTROL_LYAPUNOV_AUDIT

## Control effect on ΔV and tail-risk
| scenario | improved E[ΔV] | Δrisk | trades_executed | expansions_allowed | expansions_blocked | compressions_triggered |
|---|---:|---:|---:|---:|---:|---:|
| random | 0.000251 | 0.7167 | 76.302 | 29.524 | 46.779 | 53.050 |
| trend | 0.000421 | 0.8022 | 98.181 | 32.638 | 65.544 | 72.361 |
| adv_monotonic | 0.000720 | 0.0067 | 22.000 | 21.000 | 1.000 | 1.000 |
| adv_jump_cluster | 0.000618 | 0.6722 | 349.570 | 22.910 | 326.660 | 331.217 |
| adv_liquidity_gap | 0.000730 | 0.9278 | 151.695 | 39.782 | 111.912 | 120.570 |
| adv_liquidity_freeze | 0.000679 | 0.9933 | 240.241 | 45.062 | 195.179 | 204.012 |

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
