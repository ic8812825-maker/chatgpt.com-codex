# ALE_LYAPUNOV_CONTROL_RESPONSE

Monotonicity ΔV → control_strength and latency robustness.

Monotonicity pass ratio: **1.0000**.

## Latency sweep
| latency_ticks | control_quality | p_collapse | activity_ratio |
|---:|---:|---:|---:|
| 0 | 1.4500 | 0.0000 | 0.1650 |
| 2 | 1.4425 | 0.0025 | 0.6326 |
| 5 | 1.4375 | 0.0042 | 0.7615 |
| 8 | 1.4300 | 0.0067 | 0.8255 |
| 12 | 1.4425 | 0.0025 | 0.8710 |
| 15 | 1.4400 | 0.0033 | 0.8921 |
| 20 | 1.4300 | 0.0067 | 0.9100 |

## ApplyLyapunovControl signal routing
| signal | count |
|---|---:|
| LYAPUNOV_CRITICAL | 540 |
| LYAPUNOV_GUARD | 0 |
| PRICE_MOVE | 0 |
