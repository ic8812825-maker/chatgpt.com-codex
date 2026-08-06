# 14. Broker-valid deterministic minimum-safe NewFar Solver

Версия HSB.0R-C.15. Статус: нормативный source of truth.

## Входы
Actual OldFar F, actual remaining original BIG_CORE, broker Vmin/Vmax/Vstep, immutable market/control-price snapshot, risk/margin inputs, allocation state, Future Small policy, compression limits.

## Алгоритм
1. Построить ascending broker-valid grid `N∈{Vmin,Vmin+Vstep,...,<F}`.
2. Проверить `0<N<F`.
3. Проверить `F-N≥MinimumFarCompressionLots`.
4. Проверить `(F-N)/F≥MinimumFarCompressionRatio`.
5. Проверить `N≤MaximumNewFarRatio×F`.
6. Построить следующий C/T/S basket после broker rounding и проверить next-cycle feasibility.
7. Проверить RecoveryPL monotonicity point-by-point broker money.
8. Проверить Reserve Catch-Up money proof.
9. Проверить `RiskNext<RiskOld-RiskTolerance`.
10. Проверить MarginNext/free margin/drawdown/gross exposure.
11. Выполнить recursive Future Small exact preview и conservative bound.
12. Доказать finite catch-up после broker rounding.
13. Проверить operational terminal lot semantics.
14. Выбрать первый minimum-safe N.
15. При равных допустимых результатах tie-break: меньший RiskNext, меньший MarginNext, меньше transitions, больший safety buffer, меньший N.

Fixed TargetNewFarRatio запрещён как единственный solver и может быть только research hint. Все gates пересчитываются после rounding. Planned N никогда автоматически не становится FAR: после actual fills читается фактический BIG_CORE residual и повторно проходит validation.

Нет safe candidate, plateau на grid, stale snapshot, invalid money, failed recursion или actual residual mismatch→reject/TERMINAL_SAFE. Candidate proof и digest сохраняются. Owner Planning/NewFarSolver. Tests: 0.01/coarse step, min lot, both directions, tie, no candidate, two transitions, actual deviation.