# ALE_LYAPUNOV_PROOF

## V(state) formula
V = a1*drawdown + a2*|exposure| + a3*margin_usage + a4*depth + a5*distance_to_be + a6*unrealized_loss (normalized)

### Coefficients
- {'drawdown': 0.3, 'exposure': 0.18, 'margin_usage': 0.18, 'depth': 0.12, 'distance_to_be': 0.12, 'unrealized_loss': 0.1}

## ΔV analysis by mode
| mode | E[ΔV] | worst ΔV | V_start | V_end | status |
|---|---:|---:|---:|---:|---|
| random | 0.000433 | 0.049669 | 0.0035 | 0.5222 | unstable |
| trend | 0.000417 | 0.048157 | 0.0022 | 0.5017 | unstable |
| shock | 0.000092 | 0.020064 | 0.0022 | 0.1128 | borderline |
| adv_monotonic | 0.000640 | 0.048260 | 0.0024 | 0.7699 | unstable |
| adv_jump_cluster | 0.000819 | 0.090885 | 0.0176 | 1.0000 | unstable |
| adv_liquidity_gap | 0.000511 | 0.053425 | 0.0148 | 0.6280 | unstable |
| adv_liquidity_freeze | 0.000832 | 0.087198 | 0.0023 | 1.0000 | unstable |

## V(t) text-graphs
### random
▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▂▂▁▂▂▃▃▅▅▆▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇

### trend
▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▂▂▂▂▂▂▂▂▂▂▂▂▂▃▅▆▆▆▆▆▆▆▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇

### shock
▁▁▁▂▁▁▁▁▁▁▂▂▃▃▃▃▃▃▃▃▃▃▃▂▂▂▃▄▅▅▅▆▆▆▆▆▅▄▅▆▆▆▆▆▆▆▆▆▅▅▅▅▅▄▅▅▅▄▄▅▅▅▅▅▆▇▇▆▆▆▆▆▆▆▆▅▅▆▆▆

### adv_monotonic
▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▂▂▂▂▂▂▂▃▃▃▃▄▄▄▄▄▄▄▅▅▅▅▅▅▅▅▅▅▅▅▅▅▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▇▇▇▇▇▇▇▇

### adv_jump_cluster
▁▁▁▂▂▄▄▄▅▅▆▆▇▇▇▇▇▇▇▇▇▇▇▇▇▇██████████████████████████████████████████████████████

### adv_liquidity_gap
▁▁▁▁▁▁▁▁▁▁▁▂▂▂▃▄▅▅▅▅▅▅▅▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇

### adv_liquidity_freeze
▁▁▁▁▁▁▁▁▁▂▂▂▂▂▂▃▃▃▄▄▄▄▄▄▄▄▄▅▅▄▄▅▅▅▅▅▅▅▅▅▆▆▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇████████

## Lyapunov existence/result
- [x] Lyapunov exists
- [ ] Lyapunov does NOT exist
- Stability conclusion: UNSTABLE modes detected
