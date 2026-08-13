# 30. Aggregate proof Future Small

`HSBI_AggregateFutureSmallProof` обрабатывает ровно `levels[0..provenDepth-1]`; `provenDepth < 2`, пропуск или неполный level отклоняются. Для каждого уровня обязательны exact status, money/margin/runtime-risk/transition-loss proofs, market/cost snapshots и Far projection.

Worst-case contract использует максимум margin, risk, gross exposure и transition loss, минимум recovery money и compression, а `finalFar` берёт из последнего подтверждённого уровня. Политика Catch-Up — `WORST_CASE`, `FINAL_LEVEL` либо immutable explicit control level — входит в aggregate и candidate digests. NewFar gates не читают молча только первый level.

Proxy/test-only risk делает aggregate invalid. Runtime risk и broker proof требуют проверки администратора.

```text
TRADE_EXECUTION=NOT_IMPLEMENTED
REAL_TRADING_ALLOWED=NO
METAEDITOR_COMPILE=USER_VERIFICATION_REQUIRED
MQL5_RUNTIME_TESTS=USER_VERIFICATION_REQUIRED
RISK_RUNTIME_PROOF=USER_VERIFICATION_REQUIRED
```
