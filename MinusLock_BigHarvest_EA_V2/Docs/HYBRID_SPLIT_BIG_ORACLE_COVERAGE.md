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
| Stage 1.1 source audit | sequential MQL5 source | `EvaluateHybridCatchUpLevel` | FT-01..FT-47 | Python/static | PARTIALLY_COVERED — runtime parity absent |
| Stage 1.2 typed outcomes | outcome truth table | `classify/combine` | FO-01..FO-12 | Python + MQL5 runner source | PARTIALLY_COVERED — MQL5 runtime absent |
| Stage 1.2 non-cumulative Worst | temporal/outcome contracts | `trigger` | WP-01..WP-08 | Python + MQL5 runner source | PARTIALLY_COVERED — MQL5 runtime absent |
| Stage 1.2 margin controls | temporal contract | `margin_price/margins` | MG-01..MG-10 | Python + MQL5 runner source | PARTIALLY_COVERED — MQL5 runtime absent |
| Stage 1.2.1 Final Close route state | temporal/outcome contracts | route-state oracle | ROUTE-01..12, ADV-01..05 | source tests pending | PARTIALLY_COVERED — MQL5 runtime absent |
| Stage 1.2.1 route preservation source | immutable pre-Partial route state | `test_catchup_route_state` | ROUTE-01..12, ADV-01..05 | Python numeric/static + MQL5 source | PARTIALLY_COVERED — runtime absent |
| Stage 1.2.2 route hardening | strict validator/fingerprint/revisions | `test_catchup_route_hardening` | RV-01..15, FP-01..08, CV-01..07 | Python/source parity | PARTIALLY_COVERED — Administrator MT5 validation required |
