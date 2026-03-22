# ALE_LYAPUNOV_REPORT

## Improved formula rationale
Dynamic quantile normalization + log compression + control/latency/compression terms + drawdown-margin coupling reduce shock sensitivity.

## Baseline vs improved
| scenario | baseline E[ΔV] | improved E[ΔV] | worst ΔV | V_start | V_end | verdict |
|---|---:|---:|---:|---:|---:|---|
| random | 0.000130 | 0.000251 | 0.055502 | 0.1553 | 0.4558 | unstable |
| trend | 0.000274 | 0.000421 | 0.057553 | 0.0544 | 0.5594 | unstable |
| adv_monotonic | 0.000555 | 0.000720 | 0.028037 | 0.0563 | 0.9195 | unstable |
| adv_jump_cluster | 0.000820 | 0.000618 | 0.053198 | 0.1801 | 0.9210 | unstable |
| adv_liquidity_gap | 0.000821 | 0.000730 | 0.066062 | 0.0456 | 0.9210 | unstable |
| adv_liquidity_freeze | 0.000831 | 0.000679 | 0.088587 | 0.1065 | 0.9210 | unstable |

## Tail-risk impact
| scenario | P(collapse) base | P(collapse) ctrl | Δrisk |
|---|---:|---:|---:|
| random | 0.7167 | 0.0000 | 0.7167 |
| trend | 0.8022 | 0.0000 | 0.8022 |
| adv_monotonic | 0.0067 | 0.0000 | 0.0067 |
| adv_jump_cluster | 1.0000 | 0.3278 | 0.6722 |
| adv_liquidity_gap | 0.9278 | 0.0000 | 0.9278 |
| adv_liquidity_freeze | 0.9933 | 0.0000 | 0.9933 |

## Additional metrics
| scenario | E[ΔV] | worst ΔV | ΔV variance | recovery speed |
|---|---:|---:|---:|---:|
| random | 0.000251 | 0.055502 | 0.000062 | -0.6059 |
| trend | 0.000421 | 0.057553 | 0.000035 | -0.6533 |
| adv_monotonic | 0.000720 | 0.028037 | 0.000012 | -0.0454 |
| adv_jump_cluster | 0.000618 | 0.053198 | 0.000028 | -0.9343 |
| adv_liquidity_gap | 0.000730 | 0.066062 | 0.000041 | -0.7407 |
| adv_liquidity_freeze | 0.000679 | 0.088587 | 0.000040 | -0.8099 |

## Graphs (generated)
- Heatmap: ![dV heatmap](ale/lyapunov/artifacts/dV_heatmap.png)
- random: ![random](ale/lyapunov/artifacts/V_random.png)
- random: ![random](ale/lyapunov/artifacts/dV_random.png)
- trend: ![trend](ale/lyapunov/artifacts/V_trend.png)
- trend: ![trend](ale/lyapunov/artifacts/dV_trend.png)
- adv_monotonic: ![adv_monotonic](ale/lyapunov/artifacts/V_adv_monotonic.png)
- adv_monotonic: ![adv_monotonic](ale/lyapunov/artifacts/dV_adv_monotonic.png)
- adv_jump_cluster: ![adv_jump_cluster](ale/lyapunov/artifacts/V_adv_jump_cluster.png)
- adv_jump_cluster: ![adv_jump_cluster](ale/lyapunov/artifacts/dV_adv_jump_cluster.png)
- adv_liquidity_gap: ![adv_liquidity_gap](ale/lyapunov/artifacts/V_adv_liquidity_gap.png)
- adv_liquidity_gap: ![adv_liquidity_gap](ale/lyapunov/artifacts/dV_adv_liquidity_gap.png)
- adv_liquidity_freeze: ![adv_liquidity_freeze](ale/lyapunov/artifacts/V_adv_liquidity_freeze.png)
- adv_liquidity_freeze: ![adv_liquidity_freeze](ale/lyapunov/artifacts/dV_adv_liquidity_freeze.png)
