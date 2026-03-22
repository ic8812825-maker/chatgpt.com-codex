# ALE_CONTROL_LYAPUNOV_AUDIT

## Control effect on tail-risk
- P(collapse) base: 0.9380
- P(collapse) control: 0.0010
- Δrisk (base-control): 0.9370
- trades_executed: 195.7830
- expansions_allowed: 46.0040
- expansions_blocked: 149.7790
- compressions_triggered: 159.1570

## Latency stress
| delay | P(collapse) | activity_ratio | control_intensity |
|---:|---:|---:|---:|
| 0 | 0.0044 | 0.1550 | 0.8450 |
| 2 | 0.0044 | 0.6232 | 0.3768 |
| 5 | 0.0089 | 0.7506 | 0.2494 |
| 8 | 0.0056 | 0.8129 | 0.1871 |
| 12 | 0.0044 | 0.8599 | 0.1401 |

## Interpretation
- If delay materially increases collapse risk, control loop is latency-sensitive.
- Overcontrol risk is flagged when activity_ratio falls while control_intensity saturates.
