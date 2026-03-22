# ALE_TAIL_EFFECTIVENESS_REPORT

Tail-risk effectiveness of control layer on stress-heavy regimes.

| mode | P(collapse) base | P(collapse) ctrl | Δrisk | pnl base | pnl ctrl |
|---|---:|---:|---:|---:|---:|
| shock | 0.8817 | 0.0000 | 0.8817 | -58.8848 | 15.1101 |
| adv_jump_cluster | 1.0000 | 0.4658 | 0.5342 | -111.3019 | -77.3770 |
| adv_liquidity_gap | 0.9475 | 0.0000 | 0.9475 | -54.3510 | 18.7198 |
| adv_liquidity_freeze | 0.9967 | 0.0008 | 0.9958 | -56.4299 | 10.8542 |

## Summary
- Modes with risk improvement: 4/4.
- A negative Δrisk means control worsened tail risk in that regime.
- Stability requires preserving positive activity while reducing collapse probability.
