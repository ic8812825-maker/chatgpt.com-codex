# ALE_ADVERSARIAL_REPORT

| scenario | E_dV | collapse | max_V |
|---|---|---|---|
| flash_crash | -0.000316 | 0 | 0.975 |
| infinite_trend | 8.6e-05 | 1 | 0.992161 |
| spread_explosion | 5.8e-05 | 1 | 0.986425 |
| jump | 0.004115 | 0 | 1.880355 |
| margin_cascade | -0.000166 | 0 | 0.975 |
| dual-flow | -0.003911 | 0 | 1.254536 |

- E[ΔV]: -0.000022 (target < 0)
- collapse_rate: 0.333333 (target < 0.05)
- max(V): 1.880355 (bounded)
- verdict: FAIL
