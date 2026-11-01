# HSBI NEXT STAGE 02B — минимальный план исправлений

Этот документ является планом. Он не разрешает изменение production-кода, экономической модели или включение торговли.

## Входные решения

До реализации администратор утверждает D-01–D-08 из `Reports/NEXT_STAGE_02A_DECISIONS_REQUIRED_RU.md`: conservation, названия money states, допустимые Reserve roles, FarLossIncrease, TransitionLoss, buffers, replay outcome и authoritative provenance.

## Порядок реализации

### 1. Независимый authoritative ledger contract

Минимальный scope:

- расширить persistence contract append-only записями confirmed broker deals;
- связать deal ticket, order, position identifier, account, symbol, magic, cycle, action/event, role и DealNet components;
- вычислять immutable canonical digest;
- запретить caller-сформированные `actual=true` без reconciliation.

Риск: высокий; затрагивает все settled money. Тесты: nonexistent/foreign deal, altered DealNet, duplicate event, stale snapshot, restart replay.

### 2. Исправление M-01

Минимально затрагиваемые функции после решения:

- `HSBI_ValidateReserveConsumption` либо новая `HSBI_ValidateConsumptionAgainstAllocation`;
- `HSBI_EvaluateReserveCatchUp`;
- durable consumption registry/reconciliation;
- restart validator.

Обязательные equality/binding: sourceDealKey, sourceAllocationKey, sourceDealId, allocation event/policy version, account/symbol/magic/cycle, plan/revision и consumer purpose. Exact replay — утверждённый NO-OP; altered replay — conflict.

Риск: средний для validators, высокий для migration существующих snapshots. Success: M01-A–F проходят, foreign keys всегда fail, restart не восстанавливает spent Reserve.

### 3. Исправление M-02

New Far не должен строить expected identity из проверяемого proof. Expected identity загружается из reconciled ledger/allocation snapshot. Proof содержит ссылку и digest, которые проверяются против authoritative record.

Минимальный scope:

- `HSBI_NewFarProofIdentity`/caller assembly;
- `HSBI_ValidateReserveSourceProof`, `HSBI_ValidateFarLossProof`;
- source proof DTO;
- reconciliation lookup.

Риск: высокий; старые vectors могут быть self-confirming. Success: M02-01–14 имеют независимые expected outcomes, source mutations убиваются.

### 4. Денежная типизация M-03–M-08

После решений администратора:

- отделить projected basket metric от actual realized и allocated funds;
- удалить Small из Reserve source либо переименовать неавторитетную aggregate metric;
- ввести отдельные absolute/incremental Far loss types;
- разделить projected/actual TransitionLoss;
- сделать buffer components и aggregation явными;
- зафиксировать allocation equality или типизированный unallocated state.

Риск: высокий, потому что меняется контракт формул. Нельзя выполнять до решений.

### 5. Независимый oracle и mutation suite

Создать отдельную реализацию по утверждённым формулам без импорта production helpers. Численные vectors включают BUY/SELL, Bid/Ask, costs, grid, failed broker API, foreign IDs, replay/restart и десять mutations из Stage 02A matrix. Для broker instruments сравнивать с `OrderCalcProfit/OrderCalcMargin` в MetaTrader.

### 6. Runtime verification

Последовательность gate:

1. source/static tests;
2. MetaEditor compile main и harness;
3. MQL5 unit tests;
4. Strategy Tester dry run без broker dispatch;
5. restart/fault injection;
6. broker-money proof на утверждённых symbols/account modes;
7. независимый review evidence, привязанного к SHA.

## Критерии успешного 02B

- все решения D-01–D-08 зафиксированы;
- M-01/M-02 negative vectors и source mutations проходят;
- allocation conservation однозначен;
- projected не может попасть в actual/available buckets;
- durable replay даёт idempotent outcome после restart;
- MetaEditor/MQL5/broker checks имеют свежие результаты;
- no-trade guard и `brokerDispatchAllowed=false` сохранены;
- production trading остаётся запрещённым до отдельного этапа.
