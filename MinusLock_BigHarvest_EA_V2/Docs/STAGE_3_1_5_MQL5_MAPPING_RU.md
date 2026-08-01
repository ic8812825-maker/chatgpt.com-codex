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
