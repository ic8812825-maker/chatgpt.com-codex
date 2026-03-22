# ALE_CONTROL_LATENCY_REPORT

Latency sensitivity under adversarial liquidity-freeze conditions.

| delay_ticks | P(collapse) | avg_drawdown | activity_ratio | control_intensity |
|---:|---:|---:|---:|---:|
| 0 | 0.0067 | 0.0026 | 0.1412 | 0.8588 |
| 2 | 0.0108 | 0.0028 | 0.6148 | 0.3852 |
| 5 | 0.0108 | 0.0029 | 0.7357 | 0.2643 |
| 8 | 0.0167 | 0.0029 | 0.7975 | 0.2025 |
| 12 | 0.0117 | 0.0028 | 0.8460 | 0.1540 |
| 16 | 0.0125 | 0.0029 | 0.8726 | 0.1274 |

## Baseline (no control)
- P(collapse): 0.9992
- avg_drawdown: 0.0022

## Conclusion
- Best delay by collapse-risk: 0 ticks (P=0.0067).
- Worst delay by collapse-risk: 8 ticks (P=0.0167).
- Non-monotonic behavior indicates latency interacts with spread/slippage shocks.
- Delays that materially increase P(collapse) are treated as unstable operation points.
