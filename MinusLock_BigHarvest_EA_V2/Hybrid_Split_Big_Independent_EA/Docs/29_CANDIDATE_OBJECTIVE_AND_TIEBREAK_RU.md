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

## Коррекция HSB.2B-R2

До objective проверяется `HSBI_IsCompleteCandidateProof`: обязательны полные digests Future Small, money, margin, runtime risk, Catch-Up, allocation policy, control snapshots и cost snapshots. Candidate digest включает actual residual, old Far, compression/geometry и все перечисленные proof digests. Изменение любого level, policy share, market/cost/risk snapshot или Catch-Up result меняет plan/candidate digest.

Tie-break не рассматривает кандидатов с proxy/test-only risk, отсутствующим Reserve source или неполным digest.
