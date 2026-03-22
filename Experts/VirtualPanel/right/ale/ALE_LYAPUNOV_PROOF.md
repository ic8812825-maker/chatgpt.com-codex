# ALE_LYAPUNOV_PROOF

## Baseline vs Improved V(state)
Baseline: V = Σ ai*xi (fixed normalization).
Improved: dynamic quantile normalization + log-compression + control/latency/compression terms + dd-margin coupling.

### Baseline coefficients
- {'drawdown': 0.3, 'exposure': 0.18, 'margin_usage': 0.18, 'depth': 0.12, 'distance_to_be': 0.12, 'unrealized_loss': 0.1}
### Improved coefficients
- {'drawdown': 0.22, 'exposure': 0.12, 'margin_usage': 0.18, 'depth': 0.1, 'distance_to_be': 0.08, 'unrealized_loss': 0.1, 'control_intensity': 0.08, 'latency': 0.04, 'compression': 0.04, 'corr_dd_margin': 0.04}

## ΔV analysis by mode
| mode | baseline E[ΔV] | improved E[ΔV] | worst ΔV | V_start | V_end | status |
|---|---:|---:|---:|---:|---:|---|
| random | 0.000428 | 0.000497 | 0.066632 | 0.0921 | 0.6878 | unstable |
| trend | 0.000377 | 0.000462 | 0.057575 | 0.0445 | 0.5979 | unstable |
| adv_monotonic | 0.000555 | 0.000721 | 0.028095 | 0.0540 | 0.9181 | unstable |
| adv_jump_cluster | 0.000820 | 0.000618 | 0.064242 | 0.1797 | 0.9210 | unstable |
| adv_liquidity_gap | 0.000482 | 0.000576 | 0.044046 | 0.1785 | 0.8695 | unstable |
| adv_liquidity_freeze | 0.000832 | 0.000728 | 0.061901 | 0.0486 | 0.9219 | unstable |

## V(t) text-graphs (improved)
### random
▁▁▂▁▂▂▂▂▂▂▂▂▂▃▃▃▂▃▃▃▃▃▃▃▃▃▃▃▃▂▃▃▃▂▃▂▃▃▃▃▃▃▃▃▄▄▄▄▄▅▅▆▆▆▆▆▆▆▆▆▆▆▆▆▆▇▆▆▆▇▇▇▇▇▇▇▇▇▇▇

### trend
▁▂▂▃▃▄▃▃▄▄▄▃▃▃▃▄▄▃▃▃▃▃▃▄▄▄▄▅▅▅▅▅▅▅▅▅▅▅▅▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇

### adv_monotonic
▁▁▁▂▂▂▂▂▂▂▂▂▂▃▃▃▃▃▃▃▃▃▄▄▄▄▄▄▄▄▄▄▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▆▆▆▆▆▆▆▆▆▆▆▆▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇

### adv_jump_cluster
▁▃▃▃▄▅▆▆▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇

### adv_liquidity_gap
▁▁▁▁▂▁▂▂▂▂▂▂▃▃▃▄▄▄▄▄▄▄▄▅▅▅▅▅▅▅▅▅▅▅▅▅▅▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇

### adv_liquidity_freeze
▁▂▂▂▂▃▃▃▃▄▄▄▄▄▄▄▄▅▅▅▅▅▅▆▆▆▆▆▆▆▆▆▆▆▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇

## Lyapunov result
- Modes with lower E[ΔV] vs baseline: 2/6
- Remaining unstable modes: 6/6
- Conclusion: instability is reduced but not fully eliminated in adversarial tails.
