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

## Коррекция HSB.2B-R

Линейные per-level/per-lot коэффициенты не являются broker proof и удалены из production solver path. Каждый exact Future Small level заново строит geometry и четыре независимые legs, проверяет Bid/Ask, signed commission/swap/fee, spread/slippage/safety buffer, вызывает calculation-only money/margin wrappers, затем рассчитывает basket money, margin, exposure, basket-derived risk и transition loss. Любой unavailable leg делает уровень недоказанным.

Каждый NewFar candidate создаёт собственный Future Small input и собственные money/margin/risk/Catch-Up digests. Test-only approximation и injected proof без broker confirmation не могут дать VALID/SELECTED/EXACT_PROOF. Plan digest охватывает identity, grid/tick, Bid/Ask/control snapshot, cost snapshot IDs, money/margin/risk proofs и полный candidate-list digest. Fail-closed оставляет runtime проверку администратору.

```text
HSB.2B=STATIC_CORRECTED_IMPLEMENTATION
HSB.2C=NOT_STARTED
METAEDITOR_COMPILE=USER_VERIFICATION_REQUIRED
MQL5_RUNTIME_TESTS=USER_VERIFICATION_REQUIRED
BROKER_MONEY_RUNTIME_PROOF=USER_VERIFICATION_REQUIRED
TRADING_IMPLEMENTED=NO
REAL_TRADING_ALLOWED=NO
```
