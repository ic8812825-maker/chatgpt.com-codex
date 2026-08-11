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
