# Hybrid Split Big — Oracle Coverage

| Требование | Документ | Python функция | Vector | Pytest | Статус |
|---|---|---|---|---|---|
| Law 1 / Law 2 | Manual ch. 9/11 | `evaluate_vector` | TV-03/04 | 100-loop | COVERED |
| finite Catch-Up | ch. 10 | `find_finite_catchup_level` | TV-05/06 | vectors | COVERED |
| Reserve/allocation | ch. 7–8/12 | `Buckets.allocate_harvest` | TV-01/11 | vector + unit | COVERED |
| Final projected/actual | supplement A | final gates | TV-14 | vector | COVERED |
| Transition/cumulative | supplement D | `evaluate_vector` | TV-07/08 | vectors | COVERED |
| NewFar/rounding/min lot | ch. 16–20 | `apply_round` | TV-09/10 | vectors | COVERED |
| NextBig/risk/gross | ch. 13 | `evaluate_vector` | TV-01 | vectors | COVERED |
| Margin | supplement E | `evaluate_margin` | TV-15 | vector | COVERED |
| Worst Case | supplement E | `evaluate_worst_case` | TV-19 | vector | COVERED |
| Future Small | ch. 17 | `evaluate_future_small` | TV-18 | vector | COVERED |
| partial execution | ch. 23 | `reconcile` | TV-13 | vector | COVERED |
| restore | gaps/oracle | `restore_reconcile` | TV-20 | vector | COVERED |
| terminal state | ch. 19 | `evaluate_vector` | TV-10 | vector | COVERED |

Oracle is broker-agnostic; MT5 parity still requires a future adapter around `OrderCalcProfit` and `OrderCalcMargin`.
