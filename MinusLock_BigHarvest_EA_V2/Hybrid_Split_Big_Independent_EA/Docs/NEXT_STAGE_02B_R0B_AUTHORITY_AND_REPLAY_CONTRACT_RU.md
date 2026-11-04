# 02B-R0B — authority, identities и replay

База `9b43c38afdb89c6b3b514b654c7fb9a936f9bf2b`, ветка work. Audit/test-only; production и historical evidence неизменны. Утверждение администратора отсутствует; все новые формулировки PROPOSED.

## Independent expected

Confirmed broker history → immutable economic record → committed allocation → independent expected identity → consumption eligibility → Catch-Up/NewFar gates. Ненулевой ID/positive value/valid/actual/runtimeConfirmed не доказывает source. ClientExpected не является authority. History unavailable/incomplete =>UNAVAILABLE; complete history без source =>REJECT. Новый oracle не строит history из предъявленного proof; mutation такого fallback поймана.

Broker/Server/Account — namespace; Symbol/Magic/Deal/Order/Position/Cycle — source binding; Plan/StateRevision/Snapshot — current context; AllocationEvent/PolicyVersion — authoritative grant. SourcePlan/SourceAction/OriginRevision неизменны, current consumption context связывается отдельным journal receipt. Magic — signed nonzero configured long, bool как ID запрещён.

По каждому из 14 полей выполнены positive control, изменение только одного поля и REJECT нового oracle. Все отказавшие apply сохраняют balances/journal/authority revision. После committed event изменённый payload даёт CONFLICT либо REJECT foreign namespace, никогда ложный NO_OP.

## Исполненная граница R0A

Таблица относится только к authorize/apply_for_test R0A. Unsupported extra fields не становятся поддержанными DTO; их игнорирование не доказывает обход полного verify_proof/NewFar pipeline. Для нового coupled oracle все single-field negatives отвергнуты без изменения state.

| Идентификатор | Positive R0A | Negative R0A | Balances/revision unchanged | Новый strict oracle |
|---|---|---|---|---|
| Broker | ELIGIBLE_FOR_COMMIT | REJECT | True/True | REJECT, unchanged |
| Server | ELIGIBLE_FOR_COMMIT | REJECT | True/True | REJECT, unchanged |
| Account | ELIGIBLE_FOR_COMMIT | REJECT | True/True | REJECT, unchanged |
| Symbol | ELIGIBLE_FOR_COMMIT | COMMITTED_IN_MEMORY | False/False | REJECT, unchanged |
| Magic | ELIGIBLE_FOR_COMMIT | COMMITTED_IN_MEMORY | False/False | REJECT, unchanged |
| Deal | ELIGIBLE_FOR_COMMIT | COMMITTED_IN_MEMORY | False/False | REJECT, unchanged |
| Order | ELIGIBLE_FOR_COMMIT | COMMITTED_IN_MEMORY | False/False | REJECT, unchanged |
| Position | ELIGIBLE_FOR_COMMIT | COMMITTED_IN_MEMORY | False/False | REJECT, unchanged |
| Cycle | ELIGIBLE_FOR_COMMIT | REJECT | True/True | REJECT, unchanged |
| Plan | ELIGIBLE_FOR_COMMIT | REJECT | True/True | REJECT, unchanged |
| StateRevision | ELIGIBLE_FOR_COMMIT | REJECT | True/True | REJECT, unchanged |
| AllocationEvent | ELIGIBLE_FOR_COMMIT | REJECT | True/True | REJECT, unchanged |
| PolicyVersion | ELIGIBLE_FOR_COMMIT | REJECT | True/True | REJECT, unchanged |
| SnapshotID | ELIGIBLE_FOR_COMMIT | COMMITTED_IN_MEMORY | False/False | REJECT, unchanged |

R0 legacy oracle отдельно дал ALLOW для Plan999 и Revision999; R0A и новый strict oracle их отвергают. На R0A authorize boundary шесть иных обязательных атрибутов не представлены/не проверяются. Это ограниченная reference API, не исполненная чужая сделка.

## Replay и применение

EventIdentity=(Broker,Server,Account,ConsumptionEvent). Canonical payload содержит amount/bucket/purpose/source/allocation/precision/policies/plan/action/revision/snapshot. Exact known event сравнивается с историческим committed payload до current revision/policy gate: NO_OP, zero deltas. Same event + changed payload: CONFLICT. Чужой namespace: REJECT, не ложный NO_OP.

Новое событие требует current context, sufficient available и independent source verification. ELIGIBLE_FOR_COMMIT не меняет ledger. Только отдельный verified commit меняет Remaining/Consumed/revision. In-memory apply не реализует durable CAS. ConsumptionPolicy и immutable AllocationPolicyVersion различаются. После advance policy exact старый event остаётся NO_OP; changed old payload — CONFLICT.

E1=10 из50 →40/revision2; exact E1 →40 без новой revision; E1=11 CONFLICT. E2=40 с current proof/revision2 исчерпывает source до0; replay E2 NO_OP; новый E3=1 REJECT. Consumed50 не становится available50.

## Проверенные функции R0A и границы

- reconciled_net — closing-source fixture helper с default USD/2 HALF_EVEN, без broker-posted API. Не равен universal reconciliation; opening fees учитываются отдельно в economic ledger.
- allocate — mathematical primitive с предполагаемым verified input. Kind label не подтверждает source; отсутствие history в API само по себе не дефект арифметики.
- valid_balance проверяет maps/суммы, не currency authority. Валюта/precision проверяются на обязательной внешней границе.
- authorize/apply не содержат все обязательные identity поля и не вызывают verify_proof обязательно. Обязательность полного production caller chain UNPROVEN.
- verify_proof не является balance/commit authorizer. Старые role/snapshot negatives маскировались другим guard: Small record имел Core identity, stale context менял digest. Новые причинные векторы согласуют identity/digest, оставляя один запрещённый признак.

New oracle проверяет независимые fixed history/allocations/context fixtures. Это не реальные broker receipts. Own-reservation settlement, global debit attribution, provider completeness, journal integrity и durable recovery требуют отдельного evidence. Scope consumption profile — unreserved debit. Для собственного verified reservation при commit R-=x,C+=x,V-=x; без ReservationOwner/Intent receipt нельзя расходовать чужой lock.

Источники: Tests/Reference/hsbi_02b_r0a_normative_model.py (шесть функций задания), production NewFar:119–125, MoneyProofIdentity:16, ReserveAllocationTypes:25; точные SourceFunction/SourceLine находятся в verification matrix.
