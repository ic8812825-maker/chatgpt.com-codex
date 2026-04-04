# ALE_MODEL_REALITY_GAP

Model-vs-real execution gap under matched seeds and stressed execution conditions.

## Scenario breakdown
| scenario | mean_gap | worst_gap | bias |
|---|---|---|---|
| trend | 0.002791 | 0.026826 | -5.7e-05 |
| jump | 0.002952 | 0.025296 | -5e-05 |
| freeze | 0.002167 | 0.024598 | -8.8e-05 |
| dual-flow | 0.00372 | 0.027016 | -1e-05 |

## KPI
- mean_gap: 0.002908 (target < 0.01)
- worst_gap: 0.027016 (target < 0.1)
- bias: -0.000051 (target ≈ 0)
- verdict: PASS
