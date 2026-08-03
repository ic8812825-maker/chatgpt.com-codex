# Read-only mapping денежной модели в MQL5

Production `.mq5/.mqh` не изменялись. Статусы описывают лишь найденную статическую трассу.

| Правило | Фактическая трасса | Статус |
|---|---|---|
| Projected money / Bid-Ask | `BrokerMoneyModel.mqh`, Hybrid preview routes | PARTIAL |
| Symbol/Magic filtering | Position resolution/utility routes | IMPLEMENTED |
| CycleID | role comment `ML|...|C...`, `ParseRoleComment` | PARTIAL |
| Reserve ledger/transaction | `Types.mqh` ReserveLedgerEntry/ReserveTransaction | IMPLEMENTED |
| Pending reserve idempotency | `pendingReserveApplied` fields | PARTIAL |
| Realized DealNet incl. all costs | history recalculation routes | PARTIAL |
| Opening-cost allocation by partial fill | единый нормативный route не найден | MISSING |
| Economic/Allocation ledger separation | отдельная полная модель не найдена | MISSING |
| RecoveryPLCloseNow exact contract | `realCyclePL` и preview существуют, canonical aggregation не доказана | PARTIAL |
| TransitionBudget/Residual | единый persistent allocation ledger не найден | MISSING |
| Exactly-once composite EventKey | ticket/pending fields частичны | PARTIAL |
| Restart history reconciliation | reconciliation/persistence components существуют | PARTIAL |
| Final Close post-trade proof | preview/reconciliation routes частичны | PARTIAL |

`PRODUCTION_MQL5_MAPPING=PARTIAL`; runtime fills, dynamic spread, swap timing и deal replay данным
static audit не доказаны. Все MISSING/PARTIAL — требования будущей implementation/trace работы;
автоматическое исправление production на Этапе 3.1.5 запрещено.

## Correction mapping

Oracle capabilities не повышают MQL5 status: composite EventKey, unified allocation ledger,
serialized phase replay и ledger-derived Final Close остаются `MISSING/PARTIAL` и
`NOT_RUNTIME_PROVEN`; production implementation не менялась.

## Status after 3.1.5.58

Python normative proof is PASS; production MQL5 mapping remains PARTIAL and was not changed.
MetaEditor/Strategy Tester were not run; exact MT5 runtime execution remains unproven.

### Статус после третьей корректирующей приёмки (3.1.5.72)

```text
STAGE_3_1_5_VALIDATION=PASS
STAGE_3_1_5_STATUS=CLOSED
FRESH_CLONE_VERIFICATION=PASS
BLOCKING_COUNTERS=NONE
NEXT_ALLOWED_STAGE=3.1.6
STAGE_3_1_6_STARTED=NO
AWAITING_USER_APPROVAL=YES
REAL_TRADING_ALLOWED=NO
PRODUCTION_MQL5_IMPLEMENTATION=NOT_CHANGED
PRODUCTION_MQL5_MAPPING=PARTIAL
METAEDITOR_COMPILE=NOT_RUN
MT5_STRATEGY_TESTER=NOT_RUN
```
