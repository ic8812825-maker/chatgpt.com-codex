# ALE_MODEL_REALITY_DEEP

## Scenario gap
| scenario | mean_gap | bias | tail95 |
|---|---|---|---|
| trend | 0.001889 | -2e-06 | 0.007771 |
| jump | 0.000397 | -4e-06 | 0.001442 |
| freeze | 0.000684 | -3e-06 | 0.002603 |
| dual-flow | 0.003728 | -1.1e-05 | 0.017284 |

## Per-action gap
| action | gap |
|---|---|
| EXPAND | 0.001141 |
| SOFT | 0.001453 |
| COMPRESS | 0.002522 |
| PARTIAL | 0.002642 |
| SAFE | 0.001561 |

- global_bias_direction: -0.000005
- top5% tail_gap: 0.008770
- verdict: PASS
