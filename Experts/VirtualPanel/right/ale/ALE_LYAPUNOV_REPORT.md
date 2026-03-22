# ALE_LYAPUNOV_REPORT

## Formula
V(state)=Σ w_i·x_i where x_i are normalized risk-state components (drawdown, exposure, margin, depth, distance-to-BE, unrealized-loss).

## Stability by scenario
| scenario | E[ΔV] | V_start | V_end | verdict |
|---|---:|---:|---:|---|
| random | 0.000218 | 0.0098 | 0.2711 | unstable |
| trend | 0.000318 | 0.0024 | 0.3842 | unstable |
| adv_monotonic | 0.000640 | 0.0024 | 0.7693 | unstable |
| adv_jump_cluster | 0.000819 | 0.0176 | 1.0000 | unstable |
| adv_liquidity_gap | 0.000820 | 0.0022 | 0.9860 | unstable |

## Graphs (generated)
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
