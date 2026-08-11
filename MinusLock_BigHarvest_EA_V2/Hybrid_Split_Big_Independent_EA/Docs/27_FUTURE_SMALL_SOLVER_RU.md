# 27. Future Small Solver HSB.2B

Pure solver строит immutable proof из snapshots без сделок и state mutation. Exact recursion на каждом уровне рассчитывает Core/Trend/Small через broker rounding, Bnet, recovery slope, следующий Far, compression, projected money/reserve/margin/risk/exposure и transition loss. Требуются `0<F(k+1)<F(k)`, ограничение MaximumNewFarRatio, minimum compression lots/ratio, снижение risk/exposure и margin/loss gates.

Conservative bound `F(k+j)≤q^jF(k)` допустим только при `0<q<1`, минимум двух exact уровнях и включённых rounding/cost/margin/risk/loss checks. Depth 1 не доказывает бесконечность. Теоретическая граница `ceil(ln(Vmin/F0)/ln(q))` дополняется broker-grid проверкой каждого уровня. Plateau, рост Far, invalid logarithm/step/q и отсутствие terminal route отклоняются.

Статусы различают EXACT_PROOF, CONSERVATIVE_BOUND, UNPROVEN, REJECTED. Tests: T71–T91.

```text
TRADE_EXECUTION=NOT_IMPLEMENTED
ON_TRADE_TRANSACTION=NOT_IMPLEMENTED
REAL_TRADING_ALLOWED=NO
METAEDITOR_COMPILE=USER_VERIFICATION_REQUIRED
MQL5_TESTS=USER_VERIFICATION_REQUIRED
```
