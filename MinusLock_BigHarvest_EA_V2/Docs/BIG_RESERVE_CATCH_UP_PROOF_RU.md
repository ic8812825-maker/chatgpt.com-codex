# Денежный шлюз догоняющего Reserve

Перед partial Far сохраняются worst-case Far loss и исходный coverage. После фактического partial close и exactly-once Reserve credit повторно рассчитывается remaining Far close loss через account-currency Broker Money Model.

```text
CoverageBefore = (ReserveBefore + CarryBefore) / FarLossBefore
CoverageAfter  = (ReserveBefore + ReserveAdd + CarryAfter) / FarLossAfter
```

Продолжение к следующему Split level запрещено, если `CoverageAfter <= CoverageBefore`. Тем самым учитываются и денежный Reserve add, и фактическое уменьшение Far. Проверка сохраняет baseline через restart.

MetaEditor/MT5 не запускались; runtime production proof остаётся NOT_CONFIRMED.
