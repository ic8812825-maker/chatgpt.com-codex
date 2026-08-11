# HSB.2B — отчёт статической реализации

Реализованы pure Future Small exact recursion/conservative-bound/finite-grid proof и deterministic NewFar full-grid solver. Actual/projected residual разделены; source identity, immutable plan digest, risk, margin, gross exposure, transition loss, Future Small и second-Far gates fail-closed. Harness содержит непрерывные уникальные T01–T120.

Изменений FSM/roles/ledger/reconciliation state и торгового исполнения нет. MetaEditor, MQL5 runtime и broker-money proof проверяет администратор.

```text
HSB.2B=STATIC_IMPLEMENTED
FUTURE_SMALL=STATIC_IMPLEMENTED
NEW_FAR_SOLVER=STATIC_IMPLEMENTED
TRADE_EXECUTION=NOT_IMPLEMENTED
ON_TRADE_TRANSACTION=NOT_IMPLEMENTED
REAL_TRADING_ALLOWED=NO
METAEDITOR_COMPILE=USER_VERIFICATION_REQUIRED
MQL5_TESTS=USER_VERIFICATION_REQUIRED
HSB.2C=NOT_STARTED
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
