# C1 — scope API и обязательная композиция

BASE_SHA=074165b38f1b6d6253a9629c7d2def988e8e286a

Статус: PROPOSED / AWAITING_ADMIN_APPROVAL. Контракт зафиксирован до реализации C1. Production/trading/dispatch запрещены.

## Архитектурное решение test-only

Сохраняется exact arithmetic R0D и математическое ядро registry R0E с документированными исправлениями. Private registry delta/replay helpers не являются authorization API. Публичный `apply_for_test(request, store, authority)` самостоятельно вызывает `authorize` при каждом новом событии. Он не принимает ранее возвращённый eligibility result как authority. Python private names не являются sandbox/security boundary: модель проверяет DTO на публичном API, не защищается от кода, произвольно изменяющего её память.

Store содержит core ledger и отдельные immutable composed receipts. Authority независимо поставляет economic history, core journal, commit receipts, allocation records, current evaluation context, batch context/fill history и cost policy set. Ни один expected record не строится из presented identity. Provider boundary здесь — независимо собранные fixtures, не доказательство broker authenticity.

## Публичные proof API

| API | InputContract / TrustedInputs | IndependentAuthority / MandatoryPreconditions | ValidatedProperties / OutcomeType | StateDelta / MandatoryCaller / UnvalidatedProperties |
|---|---|---|---|---|
| `available` | store/account, known typed economic history | complete external core journal и commit receipt journal; immutable source match; reconstructed ledger | verified fixture Free одной currency/grid; KNOWN_MODEL_AVAILABLE либо UNAVAILABLE/CONFLICT/UNPROVEN | Pure; authorize обязан вызвать после reconciliation; не account cash/broker/durable proof |
| `assess_batch` | collection of source references | independent expected account/broker/server/symbol/cycle/order/position/batch/currency/digits/volume/required deal set и fill history | membership перед netting; unique fills; exact volume/net; PENDING/CONFIRMED/OVER_CAP/CONFLICT/UNAVAILABLE | Pure; authorize требует CONFIRMED; signed-batch-net V1 — proposed profile, не утверждённая production cap/netting policy |
| `cost_coverage` | presented disposition rows | independent complete applicable cost set с applicability/amount/basis/window/currency/policy | required costs covered exactly once, unknown→UNAVAILABLE; COVERED и exact additional nonnegative risk total | Pure; authorize вычитает этот total при gate headroom; actual signed costs должны быть уже reconciled, новые signed costs не угадываются |
| `verify_allocation_identity` | presented typed identity | history source + authoritative allocation + independent current context/planned consumption event | distinct EconomicEventID/AllocationEventID/ConsumptionEventID; allocation-ID/event binding; money vector separately validated; PASS/REJECT/UNAVAILABLE | Pure; authorize обязан вызвать; не broker cryptographic proof |
| `authorize` | typed C1 request/store/authority | все предыдущие mandatory layers | ELIGIBLE_FOR_COMMIT/NO_OP/CONFLICT/REJECT/UNAVAILABLE; source/global-debit checks; exact DebitAmount/RequiredBalance/Free | Zero deltas; apply_for_test всегда вызывает сам; не durable commit |
| `apply_for_test` | те же входы, без eligibility token | повторная authorize; checked private delta; post-state validation | COMMITTED_IN_MEMORY либо прежний typed отказ/NO_OP | Deep-copy atomic apply, core revision+1 и receipt только после validation; durable CAS/concurrency не доказаны |
| `recover_store` | snapshots | независимые оба journals и economic history | checksum/schema + reconstruction + receipt bindings; RECONCILED_MODEL_ONLY/UNAVAILABLE/CONFLICT | Pure; не filesystem crash recovery |

## Математические primitives

`fund`, `balance`, `legacy_view`, `source_key`, `key`, `allocation_key`, `event_key`, `identity_shape`, `economic_record`, `funding_status`, `far_loss`, `snapshot`, `recover`, `new_registry`, `checked_add`, `checked_mul`, `close_side`, `assess_levels` сохраняют математический/валидационный scope ядра; их PASS/COMMITTED не является composed consumption authorization. Старый consumption entry переименован в private `_operate_for_registry_replay`, его delta — private `_apply_registry_delta`. Старые selected-fill/cost/source-context helpers также private. number/canonical/digest — frozen arithmetic/codec, не authority.

Неопределённые broker/provider facts не выводятся из kind/fresh/complete flags: в tests это явно trusted fixture assumptions. Неизвестная/неполная authority →UNAVAILABLE; некорректный внешний DTO→REJECT/CONFLICT согласно API; неожиданный programming exception остаётся видимым, blanket except Exception отсутствует.

## Proposed profile и replay

PrincipalAmount>0 и AdditionalRiskCost>=0; RequiredBalance=PrincipalAmount+AdditionalRiskCost; DebitAmount=PrincipalAmount. Публичная composed операция C1 ограничена CONSUME_FREE; это не реализация полного reservation/dispatch lifecycle. Математические reserve/release/owned-consume преобразования проверяются отдельно и не выдаются за публичную composed authorization.

Exact composed replay: сначала typed request, независимые complete journals и reconciliation immutable economic source. Изменённый immutable source →CONFLICT, missing history/journal→UNAVAILABLE; затем exact stored request receipt →NO_OP до новых current-policy/revision/snapshot gates. Changed request на том же event→CONFLICT. Это консервативный PROPOSED fixture choice D07, не автоматически утверждённый durable replay норматив.

Current Plan/Revision/Snapshot и planned ConsumptionEventID берутся из независимого evaluation context. Source EconomicEventID не приравнивается к allocation или consumption event. OriginPlan остаётся историческим source context. Allocation event/ID/policy/grants/currency берутся из независимого allocation provider и сверяются с immutable ledger allocation.

Partial fills: netting `PROPOSED_SIGNED_BATCH_NET_V1` по подтверждённым принадлежащим batch unique fills. Cap проверяется и на partial prefix; неизвестная policy→UNAVAILABLE. Это не решение о sticky historical breach/max-path loss; такой вариант требует отдельного административного выбора.

Safety risk buffers в C1 являются gate deductions: RequiredBalance<=Free. Они не становятся actual Consumed. Core journal списывает только independently planned PrincipalAmount. Поддержка иных дополнительных actual signed costs требует reconciliation и здесь UNAVAILABLE. Это fixture registry spending gate, не полный Catch-Up economic proof (lot/Far/broker guards не реализуются). Current context отдельно задаёт principal/bucket/purpose/intent; клиент не создаёт план своим request.




## Финальный inventory публичных функций

Private helpers с underscore не являются authorization entry points. Публичные математические helpers возвращают только локальные результаты; они не могут заменить composed store/authority schema. Импортированные number/canonical/digest — frozen R0D primitives. Полный scope identity helper: source/current/event/AllocationID binding; monetary vector/currency/ledger source проверяет обязательный _bind_allocation.

- `source_key` — MATHEMATICAL_OR_SHAPE_ONLY; SourceLine=21. Не spending authorization; типы/диапазоны задаёт exact R0D и локальная schema; ошибки формы Malformed/Unsupported видимы. Caller для spending — authorize/apply_for_test.
- `key` — MATHEMATICAL_OR_SHAPE_ONLY; SourceLine=25. Не spending authorization; типы/диапазоны задаёт exact R0D и локальная schema; ошибки формы Malformed/Unsupported видимы. Caller для spending — authorize/apply_for_test.
- `allocation_key` — MATHEMATICAL_OR_SHAPE_ONLY; SourceLine=26. Не spending authorization; типы/диапазоны задаёт exact R0D и локальная schema; ошибки формы Malformed/Unsupported видимы. Caller для spending — authorize/apply_for_test.
- `event_key` — MATHEMATICAL_OR_SHAPE_ONLY; SourceLine=27. Не spending authorization; типы/диапазоны задаёт exact R0D и локальная schema; ошибки формы Malformed/Unsupported видимы. Caller для spending — authorize/apply_for_test.
- `new_registry` — MATHEMATICAL_OR_SHAPE_ONLY; SourceLine=30. Не spending authorization; типы/диапазоны задаёт exact R0D и локальная schema; ошибки формы Malformed/Unsupported видимы. Caller для spending — authorize/apply_for_test.
- `identity_shape` — MATHEMATICAL_OR_SHAPE_ONLY; SourceLine=34. Не spending authorization; типы/диапазоны задаёт exact R0D и локальная schema; ошибки формы Malformed/Unsupported видимы. Caller для spending — authorize/apply_for_test.
- `economic_record` — MATHEMATICAL_OR_SHAPE_ONLY; SourceLine=43. Не spending authorization; типы/диапазоны задаёт exact R0D и локальная schema; ошибки формы Malformed/Unsupported видимы. Caller для spending — authorize/apply_for_test.
- `balance` — MATHEMATICAL_OR_SHAPE_ONLY; SourceLine=58. Не spending authorization; типы/диапазоны задаёт exact R0D и локальная schema; ошибки формы Malformed/Unsupported видимы. Caller для spending — authorize/apply_for_test.
- `legacy_view` — MATHEMATICAL_OR_SHAPE_ONLY; SourceLine=69. Не spending authorization; типы/диапазоны задаёт exact R0D и локальная schema; ошибки формы Malformed/Unsupported видимы. Caller для spending — authorize/apply_for_test.
- `fund` — MATHEMATICAL_OR_SHAPE_ONLY; SourceLine=118. Не spending authorization; типы/диапазоны задаёт exact R0D и локальная schema; ошибки формы Malformed/Unsupported видимы. Caller для spending — authorize/apply_for_test.
- `funding_status` — MATHEMATICAL_OR_SHAPE_ONLY; SourceLine=124. Не spending authorization; типы/диапазоны задаёт exact R0D и локальная schema; ошибки формы Malformed/Unsupported видимы. Caller для spending — authorize/apply_for_test.
- `far_loss` — MATHEMATICAL_OR_SHAPE_ONLY; SourceLine=229. Не spending authorization; типы/диапазоны задаёт exact R0D и локальная schema; ошибки формы Malformed/Unsupported видимы. Caller для spending — authorize/apply_for_test.
- `snapshot` — MATHEMATICAL_OR_SHAPE_ONLY; SourceLine=250. Не spending authorization; типы/диапазоны задаёт exact R0D и локальная schema; ошибки формы Malformed/Unsupported видимы. Caller для spending — authorize/apply_for_test.
- `recover` — MATHEMATICAL_OR_SHAPE_ONLY; SourceLine=253. Не spending authorization; типы/диапазоны задаёт exact R0D и локальная schema; ошибки формы Malformed/Unsupported видимы. Caller для spending — authorize/apply_for_test.
- `checked_add` — MATHEMATICAL_OR_SHAPE_ONLY; SourceLine=276. Не spending authorization; типы/диапазоны задаёт exact R0D и локальная schema; ошибки формы Malformed/Unsupported видимы. Caller для spending — authorize/apply_for_test.
- `checked_mul` — MATHEMATICAL_OR_SHAPE_ONLY; SourceLine=285. Не spending authorization; типы/диапазоны задаёт exact R0D и локальная schema; ошибки формы Malformed/Unsupported видимы. Caller для spending — authorize/apply_for_test.
- `close_side` — MATHEMATICAL_OR_SHAPE_ONLY; SourceLine=298. Не spending authorization; типы/диапазоны задаёт exact R0D и локальная schema; ошибки формы Malformed/Unsupported видимы. Caller для spending — authorize/apply_for_test.
- `assess_levels` — MATHEMATICAL_OR_SHAPE_ONLY; SourceLine=303. Не spending authorization; типы/диапазоны задаёт exact R0D и локальная schema; ошибки формы Malformed/Unsupported видимы. Caller для spending — authorize/apply_for_test.
- `request_shape` — MATHEMATICAL_OR_SHAPE_ONLY; SourceLine=325. Не spending authorization; типы/диапазоны задаёт exact R0D и локальная schema; ошибки формы Malformed/Unsupported видимы. Caller для spending — authorize/apply_for_test.
- `verify_allocation_identity` — COMPOSED_OR_PROOF; SourceLine=343. Zero deltas кроме apply_for_test; preconditions и authority приведены в таблице.
- `assess_batch` — COMPOSED_OR_PROOF; SourceLine=363. Zero deltas кроме apply_for_test; preconditions и authority приведены в таблице.
- `cost_coverage` — COMPOSED_OR_PROOF; SourceLine=395. Zero deltas кроме apply_for_test; preconditions и authority приведены в таблице.
- `new_store` — MATHEMATICAL_OR_SHAPE_ONLY; SourceLine=437. Не spending authorization; типы/диапазоны задаёт exact R0D и локальная schema; ошибки формы Malformed/Unsupported видимы. Caller для spending — authorize/apply_for_test.
- `available` — COMPOSED_OR_PROOF; SourceLine=493. Zero deltas кроме apply_for_test; preconditions и authority приведены в таблице.
- `authorize` — COMPOSED_OR_PROOF; SourceLine=514. Zero deltas кроме apply_for_test; preconditions и authority приведены в таблице.
- `apply_for_test` — COMPOSED_OR_PROOF; SourceLine=563. Zero deltas кроме apply_for_test; preconditions и authority приведены в таблице.
- `snapshot_store` — MATHEMATICAL_OR_SHAPE_ONLY; SourceLine=576. Не spending authorization; типы/диапазоны задаёт exact R0D и локальная schema; ошибки формы Malformed/Unsupported видимы. Caller для spending — authorize/apply_for_test.
- `recover_store` — COMPOSED_OR_PROOF; SourceLine=579. Zero deltas кроме apply_for_test; preconditions и authority приведены в таблице.

new_store создаёт пустой fixture store; snapshot_store только копирует/checksums store и не доказывает completeness; recover_store обязан независимо сверить оба journals. available возвращает account-scoped registry total одной валюты; authorize отдельно ограничивает debit allocation-local Free. assess_batch не отменяет реальные fills; будущий Economic Ledger обязан учитывать их независимо от cap. C1 store не является полным broker-economic ledger. Completeness относится к объявленному fixture domain, не доказывает полноту broker account history. Historical evaluationContext хранится как as-at-commit provider fact, не строится из предъявленной identity при восстановлении.

## Граница предварительного eligibility и core commit constraint

В fixture core R0E сохранён единый account-scoped ledger-event namespace для FUND и CONSUME_FREE. EconomicEventID имеет отдельный source domain. Равные numeric AllocationEventID/ConsumptionEventID не запрещены identity verifier сами по себе: это разные поля; однако reuse уже занятого core ledger key даёт CONFLICT. Это legacy fixture namespace, не утверждённый universal broker event codec. Выбор общего namespace либо typed compound event keys остаётся частью D07/D08 и будущей schema migration.

authorize даёт предварительную eligibility по заявленным source/context/batch/cost/availability gates. Последняя проверка generic core journal-key conflict принадлежит обязательной _event внутри private delta; apply_for_test всегда проверяет её status до публикации новой store. Поэтому ELIGIBLE_FOR_COMMIT не является commit guarantee и не принимается как готовый token. Проверенный scope probe: AllocationEventID=ConsumptionEventID=1 допустимы как independent identity values (PASS), preflight может быть ELIGIBLE, но existing FUND1 вызывает apply CONFLICT с zero deltas. Прямой публичный apply этот слой не обходит. Ни receipt replay, ни preflight не являются разрешением broker dispatch.
