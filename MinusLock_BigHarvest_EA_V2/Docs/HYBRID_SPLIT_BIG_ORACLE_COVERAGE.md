# Hybrid Split Big — Oracle Coverage

| Требование | Документ | Python функция | Vector | Pytest | Статус |
|---|---|---|---|---|---|
| Law 1 / Law 2 | Manual ch. 9/11 | `evaluate_vector` | TV-03/04 | 100-loop | PARTIALLY_COVERED |
| finite Catch-Up | ch. 10 | `find_finite_catchup_level` | TV-05/06 | vectors | PARTIALLY_COVERED |
| Reserve/allocation | ch. 7–8/12 | `Buckets.allocate_harvest` | TV-01/11 | vector + unit | PARTIALLY_COVERED |
| Final projected/actual | supplement A | final gates | TV-14 | vector | PARTIALLY_COVERED |
| Transition/cumulative | supplement D | `evaluate_vector` | TV-07/08 | vectors | PARTIALLY_COVERED |
| NewFar/rounding/min lot | ch. 16–20 | `apply_round` | TV-09/10 | vectors | PARTIALLY_COVERED |
| NextBig/risk/gross | ch. 13 | `evaluate_vector` | TV-01 | vectors | PARTIALLY_COVERED |
| Margin | supplement E | `evaluate_margin` | TV-15 | vector | PARTIALLY_COVERED |
| Worst Case | supplement E | `evaluate_worst_case` | TV-19 | vector | PARTIALLY_COVERED |
| Future Small | ch. 17 | `simulate_future_small` | extension tests | bounded recursion | PARTIALLY_COVERED |
| partial execution | ch. 23 | `reconcile` | TV-13 | vector | PARTIALLY_COVERED |
| restore | gaps/oracle | `restore_reconcile` | TV-20 | vector | PARTIALLY_COVERED |
| terminal state | ch. 19 | `evaluate_vector` | TV-10 | vector | PARTIALLY_COVERED |

Oracle is broker-agnostic; MT5 parity still requires a future adapter around `OrderCalcProfit` and `OrderCalcMargin`.

**MQL5 parity note:** ни одна строка не получает `FULLY_COVERED`, пока отсутствуют MQL5 parity fixture, MetaEditor compilation/run и broker adapter evidence. Python coverage и MQL5 parity являются разными доказательствами.
| Stage 1.1 sequential temporal Catch-Up | temporal model | source implementation pending audit | FT-01..FT-47 | pending | PARTIALLY_COVERED |
