# 02B-R0C — контракт независимого test-only oracle

База: `8903f7ba5d376dc642024ac8ab4400b884466c55`, ветка `work`. Все изменения — новые Docs/Reports/Tests. Статус всех уточнений **PROPOSED / AWAITING_ADMIN_APPROVAL**. Нет разрешения менять production, выполнять R1.1 или торговать.

## Происхождение и граница

Новый `Tests/Reference/hsbi_02b_r0c_independent_oracle.py` произведён от R0B: математические примитивы allocate/balance/posted/sequential/geometry сохранены, authorization boundary и обработка DTO усилены, выход CR-09 получил явный scope. Импортов старых oracle и production в новой модели нет. История, allocations, snapshot receipts и journal — независимо заданные синтетические fixtures. Их подлинность у брокера не доказана.

Положительный контроль: source50, FinalReserve grant50, Remaining50, Consumed0, Reserved0, revision1; consumption10 даёт Remaining40, Consumed10, Reserved0, revision2 и одну запись journal. ELIGIBLE_FOR_COMMIT только проверяет возможность. COMMITTED_IN_MEMORY существует исключительно в памяти Python.

## R0C-ID — типизированные идентификаторы

`request_shape`, `identity_shape`, `source_shape`: bool не integer ID. Account — positive signed long (1..2^63-1); Magic — configured signed long (-2^63..2^63-1), nonzero; Deal/Order/Position/Cycle/Plan/StateRevision/AllocationEvent/PolicyVersion/SnapshotID/ConsumptionEvent — positive ulong (1..2^64-1). Broker/Server/Symbol — непустые строки. Данные не преобразуются из строк/float в IDs. Event1 и EventULONG_MAX допустимы; True, False, 0, -1, 1.5, "41", None и 2^64 отвергаются до journal lookup.

Новая операция при revision ULONG_MAX => UNAVAILABLE: следующая revision не представима. Exact исторический replay не требует её увеличения. Диапазоны — предлагаемое соответствие будущим MQL5 types, не изменение существующих DTO.

## R0C-SHAPE — ошибки входа и недоступность

Ожидаемая ошибка схемы поднимает только специальный `Malformed`; `authorize()` переводит только его в REJECT. Missing required field, неправильный container/type, invalid ID, unsupported serialization и nonfinite DTO money => REJECT. Корректный запрос при authority=None, journal=None, incomplete authority/journal, history=None или receipt=None => UNAVAILABLE. Complete history без source => REJECT. Record payload против account-scoped lookup key => CONFLICT. Отсутствующий required receipt.posted — malformed DTO; явно отсутствующий receipt=None — недоступный факт.

Неожиданные RuntimeError и внутренние ошибки реализации не преобразуются в REJECT/PASS. Harness отмечает INFRASTRUCTURE_ERROR; source mutation с exception не считается KILLED. Вектор INTERNAL-error-visible и fault после authorization до apply serialization проверяют видимость ошибки и неизменность исходных объектов.

Применяемый **fixture-only numeric profile**: DTO money — finite Decimal, exponent в [-64,64], adjusted exponent<=64 для nonzero; digits0..8. Локальный Decimal context256 исключает округление суммы/разности таких величин при проверке/списании. Это технический ограниченный домен oracle, не универсальная currency/broker policy. Примитивы с raw строками не подтверждают источник. Вне DTO-домена REJECT, без нормализации во "всё равно доступные" деньги. Decimal canonical encoding не использует context-rounded normalize().

## R0C-AUTH — независимое сопоставление

Цепочка: independent history record → authoritative allocation → independent evaluation context → expected identity → proof verification → eligibility. Предъявленный proof/presentedRecord не создаёт history или receipt.

Сопоставляются все14 полей запроса. Для economic origin проверяются Broker/Server/Account/Symbol/Magic/Deal/Order/Position/Cycle. Исторические origin Plan/Revision/Snapshot не обязаны равняться текущим consumption Plan/Revision/Snapshot; ORIGIN-context-distinct — положительный контроль. Production lineage/provider не реализуется.

Allocation dictionary key, внутренний allocation ID, event/policy, state allocation/source, per-bucket grant vector обязаны соответствовать. Один total при иной разбивке не identical replay. Policy allocation и consumption разделены. Global source→many-allocation uniqueness не следует из проверки одного state и остаётся UNPROVEN.

## R0C-SNAPSHOT — объект и независимый receipt

`SnapshotID(request)=SnapshotID(expected)=snapshot.id`. Объект snapshot содержит id/validUntil/clockDomain/timeUnit/marketFingerprint. Независимый fixture registry snapshotReceipts[id] хранит исходный canonical object, созданный тестом до отрицательного изменения. Неизвестный receipt => UNAVAILABLE; same ID + иной payload => CONFLICT; ID объекта против expected => REJECT. Receipt нельзя формировать из изменённого объекта как основание положительного результата отрицательного теста.

В причинных тестах ID/freshness зарегистрированный объект может быть согласован с receipt, чтобы изолировать именно ID/time gate; content-тест меняет только проверяемый объект и оставляет receipt прежним. В R0B независимого content registry нет: поведение по неизвестному extra content не доказывает проверку содержимого, статус UNPROVEN. В R0C это новый синтетический контракт, не доказательство broker authenticity.

## R0C-TIME — временной профиль

PROPOSED fixture profile: clockDomain=FIXTURE_MONOTONIC, timeUnit=tick, все timestamps integer>=0, допустимый future skew0. Требуется `0<=now-historyObservedAt<=historyMaxAge` и `now<=snapshot.validUntil`. Равенство границ допустимо. Future observation, stale history/snapshot, unknown/mismatched domain/unit => UNAVAILABLE; missing required field/invalid timestamp type => REJECT.

Нельзя переносить этот skew и endpoint на брокера без административного решения и evidence. В R0B metadata clockDomain/timeUnit не поддержаны; их игнорирование классифицировано UNPROVEN, а не исполнением брокерской операции.

## R0C-MONEY — четыре независимых защиты

1. ActualDealNetRaw = Profit + Swap + Commission + Fee со знаками; rawNet обязан совпасть (иначе CONFLICT).
2. Broker-posted fixture receipt проверяется отдельно; HALF_EVEN не подменяет posted факт. Posted net и state.net=max(0,posted) должны соответствовать (иначе CONFLICT).
3. Economic record identity сверяется с независимым expected context (REJECT/CONFLICT по указанной границе).
4. Предъявленный digest должен совпасть с independently encoded record/allocation/expected bundle (REJECT).

Оригинал отвергает четыре минимальных контрпримера; каждая weakened R0B copy принимает свой пример и при этом проходит141 старый тест. R0C имеет отдельные causal vectors и mutations для всех четырёх. Expected amounts заданы literal Decimal, не результатом subject evaluator.

Conservation: COMMITTED ΣGrant=AllocatableNet, Unallocated0; PREPARED ΣGrant+Unallocated=AllocatableNet, расход запрещён. Per bucket Remaining+Consumed=Grant; 0<=Reserved<=Remaining; Available=Remaining-Reserved. Для unreserved x: Remaining-=x,Consumed+=x,Reserved неизменен. ResidualHeld не выдаётся как резерв. Small не является разрешённой ролью расходуемого FinalReserve. Отрицательный источник не создаёт grant.

## R0C-REPLAY/APPLY — порядок и атомарность

Сначала проверить request shape/IDs, authority/journal shape/completeness и namespace. Затем account-scoped known event сравнивается с историческим canonical payload: exact=>NO_OP, changed=>CONFLICT, delta0. Текущие plan/revision/policy/snapshot freshness относятся к новому событию и не превращают exact known receipt в новое списание. Проверенная полнота journal в fixture — предпосылка; durable provenance этого boolean UNPROVEN.

Для нового события обязательны все context/source/balance/money gates. `apply_for_test` сериализует request до финансовых изменений и меняет только deep copies. Reject/Conflict/Unavailable/NoOp возвращают неизменные state/journal/authority; исходные аргументы не изменяются даже при успешном apply и при injected exception. Shared-state mutation и poison on rejection проверяются отдельно. Это не durable CAS/rollback/crash recovery.

## R0C-CR09 — явный scope

A: min_i(Available_i-Loss_i-Buffer_i) по всем RequiredLevels; только ALL_LEVEL_POSITIVE при строгом положительном минимуме и остальных gates. B: выбор max TransitionLoss; SINGLE_LEVEL_POSITIVE, не all-level guarantee. L1 T100,margin29; L2 T10,margin-16: A REJECT, B SINGLE_LEVEL_POSITIVE. Эти статусы не trading authorization. Sequential50 с расходами30+30 отвергается; неизвестные входы UNPROVEN. Zero Core остаётся production-дефектом; GEOMETRY_ONLY не разрешает dispatch.

## Непроверенные внешние зависимости

Global source-level funding/double-spend, durable restart/CAS/concurrency, receipts authenticity, real partial fills, full NewFar integration и broker margin/precision runtime не доказаны. Own-reservation settlement не реализован; проверен только unreserved debit. MQL5_COMPILE/MQL5_TESTS/STRATEGY_TESTER=NOT_RUN. No-trade static scan не заменяет runtime evidence.

Точные SourceFunction/SourceLine/TestID/MutationID указаны в `Tests/Contracts/NEXT_STAGE_02B_R0C_VERIFICATION_MATRIX.json`; evidence и команды — в новых R0C JSON. Источники: Docs/08:6–24, Docs/24:3–9, Docs/31:3–5, Docs/32:3–5; действующие противоречия D-01–D-08/CR-09 разрешает только администратор.
