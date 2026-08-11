# 28. NewFar Solver HSB.2B

Источник — только actual residual исходного BIG_CORE после confirmed fills. Проверяются Account, Symbol, Magic, CycleID, PositionIdentifier, Role, Direction, Ticket, actual volume/grid, source deal, PlanID, StateRevision и freshness. ProjectedNewFar остаётся планом и не становится actual role; mismatch ведёт в reconciliation/terminal-safe contract.

Solver детерминированно перечисляет весь broker grid от VolumeMin до фактического residual/upper bound. Для каждого N проверяются `0<N<OldFar`, max ratio, compression, Future Small proof, broker money availability, margin, risk reduction, gross exposure и transition loss. AllowedTransitionLoss — минимум absolute/equity/old-Far/cumulative caps; неизвестное значение fail-closed.

Result содержит counts, selected/projected/actual volumes, compression, risk/margin/loss, source IDs, plan/revision, candidate/proof digests и typed solver status. Второй Far отклоняется. Tests: T92–T119.

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
