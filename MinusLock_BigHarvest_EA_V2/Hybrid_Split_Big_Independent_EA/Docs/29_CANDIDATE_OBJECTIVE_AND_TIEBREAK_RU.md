# 29. Candidate objective и tie-break HSB.2B

Все допустимые кандидаты формируются до выбора. Детерминированный порядок: valid candidate; минимальный RiskNext; минимальный MarginNext; минимальное число будущих переходов; максимальный safety buffer; минимальный normalized N; лексикографически минимальный CandidateDigest. Время, ticket, hash-table order, randomness и weighted objective запрещены.

Immutable input digest включает identity scope, CycleID, StateRevision, PlanID, OldFar, original identifier, actual/projected residual, compression limits, broker grid, control price, Future Small proof и risk/margin snapshots. Изменение входа после persisted plan даёт PLAN_DIGEST_MISMATCH.

Tests T108, T118–T120 проверяют повторяемость, immutability и последний digest tie-break.

```text
TRADE_EXECUTION=NOT_IMPLEMENTED
ON_TRADE_TRANSACTION=NOT_IMPLEMENTED
REAL_TRADING_ALLOWED=NO
METAEDITOR_COMPILE=USER_VERIFICATION_REQUIRED
MQL5_TESTS=USER_VERIFICATION_REQUIRED
```
