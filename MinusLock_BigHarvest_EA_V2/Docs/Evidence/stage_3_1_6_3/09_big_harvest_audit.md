# 3.1.6.3.9 — Big Harvest

Фактический Hybrid Big Harvest исполняется через Split states/functions в `StateMachine.mqh`. Roles BigCore, BigTrend и SmallBase закрываются отдельными фазами; history/position helpers затем формируют net и Reserve transaction.

## Выводы

- Actual history deal net местами используется, включая profit, commission, swap и fee через broker/history helpers.
- Reserve ledger имеет event hash, persisted transaction phases и duplicate protection для Reserve events.
- Это не общий Economic Ledger всех deals этапа 3.1.5.
- Close wrappers могут вернуть success до transaction-confirmed settlement.
- Immediate Final Close и Partial Far маршруты существуют, но связаны со Split state flow, а не единым Hybrid CandidatePlan execution.
- Far close выполняется по stored ticket; wrapper проверяет selected symbol+Magic, но CycleID/identifier ownership непосредственно в TradeEngine не проверяются.
- Следующий state может быть установлен после close wrapper до OnTradeTransaction, которого нет.

## Замечания

- `BIG-001 P1`: actual-deal lifecycle не является обязательным barrier перед allocation/state advance.
- `BIG-002 P1`: TradeEngine close ownership ограничен Symbol+Magic; CycleID+identifier проверяются не в одном атомарном месте.
- `BIG-003 P1`: Reserve event ledger не заменяет полный Economic/Allocation ledger.
- `BIG-004 P1`: Hybrid Harvest исполняется Split FSM и не связан с immutable full gate plan.
- `BIG-005 P2`: повторная проверка всех Base/Worst gates непосредственно перед каждым irreversible close не доказана.

Классификация: `SPLIT_ACTIVE + HYBRID_PARTIAL / UNSAFE`.
