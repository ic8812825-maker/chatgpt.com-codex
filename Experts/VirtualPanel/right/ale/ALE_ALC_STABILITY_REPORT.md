# ALE + ALC Stability Report

## Input parameters
- k: 1.3
- alpha: 0.5
- max_levels: 30
- leverage: 100.0
- l0: 0.01

## Core metrics
- n_max: 24
- P_collapse ≈ 1/n_max: 0.041666666666666664

## Required Deposit Table
| Trend | Required Deposit |
|---:|---:|
| 1000 | 52381.35 |
| 2000 | 52382.79 |
| 3000 | 52384.23 |
| 5000 | 52387.11 |
| 10000 | 52394.31 |

## Conclusion
ALC compression lowers margin pressure and stabilizes depth growth under configured alpha and max_levels constraints.