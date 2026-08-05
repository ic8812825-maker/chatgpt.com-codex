# 3.1.6.3.10 — Partial Far и Immediate Final Close

## Partial Far

- Budget формируется из положительного harvest allocation; Reserve isolation декларируется и частично обеспечивается отдельными fields/ledger events.
- Close lot округляется вниз; остаток после close перечитывается из actual position в новых путях.
- Однако request/deal/consume не образуют единую transaction с общим EventKey.
- Retry/persistence существуют, но отсутствие OnTradeTransaction не доказывает exactly-once actual budget consumption.

## Final Close

В проекте одновременно существуют несколько семантик:

1. Legacy/старые проверки Reserve/Far loss.
2. Split Final Close safety functions.
3. Hybrid preview/gates.
4. Real cycle P/L history recalculation.

Единого централизованного Final Close gate, который всегда использует нормативный `RecoveryPLCloseNow`, immutable snapshot, FinalReserve coverage и actual state reconciliation, не доказано. `HybridDecisionEngine` помечает Final Close preview gate PASS без расчёта и оставляет `finalCloseAvailable=false`.

## Замечания

- `PF-001 P1`: Budget debit и actual Far deal не объединены в exactly-once transaction.
- `PF-002 P1`: Несколько Final Close gates/формул создают competing authority.
- `PF-003 P1`: Нельзя доказать, что отрицательный RecoveryPL исключён на каждом legacy/split route.
- `PF-004 P1`: FinalReserve subset может быть корректно persisted, но общий double-count prevention RecoveryPL runtime неполон.
- `PF-005 P2`: Retry после partial execution опирается на polling/history, а не parent event reconciliation.

Классификация: Partial Far `MAPPED_PARTIAL`; Final Close `CONFLICTING / PARTIAL / UNSAFE`.
