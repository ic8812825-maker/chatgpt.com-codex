# ALE_BASELINE_FULL

Re-baseline with action distribution, entropy, control-strength spread and ΔV tails.

## Scenario metrics
| scenario | E_dV | P_dV_le_0 | max_V | entropy | cvar_95 |
|---|---|---|---|---|---|
| trend | -0.002952 | 0.259091 | 0.975 | 0.484076 | 0.034247 |
| jump | -0.002733 | 0.25 | 0.975 | 0.485902 | 0.041819 |
| freeze | -0.003016 | 0.254545 | 0.975 | 0.491655 | 0.045772 |
| dual-flow | -0.0034 | 0.45 | 1.013538 | 0.509099 | 0.115677 |

## Global action distribution
- COMPRESS: 53 (0.0602)
- EXPAND: 623 (0.7080)
- PARTIAL: 128 (0.1455)
- SAFE: 52 (0.0591)
- SOFT: 24 (0.0273)

## Control-strength histogram (quantiles)
- q10: -1.0000
- q50: -1.0000
- q90: 0.8200

## ΔV tail
- p95: 0.049146
- p99: 0.109448

## KPI
- SAFE domination check (<0.55): 0.0591
- all key actions used: False
- flat control detected: False
