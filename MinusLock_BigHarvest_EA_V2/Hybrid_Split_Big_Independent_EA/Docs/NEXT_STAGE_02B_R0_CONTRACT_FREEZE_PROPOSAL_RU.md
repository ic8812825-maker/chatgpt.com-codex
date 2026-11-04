# 02B-R0 — предложение фиксации контрактов

Базовый SHA: `4e7d911002824a4a92e49b54f0f964afcf8cf703`; ветка `work`; дата 04.11.2026. Локальный HEAD и remote `refs/heads/work` совпали перед записью. Режим: только тесты, контракты-предложения и отчёты. Утверждения администратора не получены. Production-код и исторические evidence не изменяются.

## Статус и приоритет нормативов

`PROPOSAL_ONLY / AWAITING_ADMIN_APPROVAL`. Данный файл не заменяет Docs/04,08,16,24,27,30,31,32 и не утверждает D-01–D-08. Действующие ограничения no-trade сохраняются. Прочитаны все документы задания, Stage 02A matrix, Docs/28, R10 replay binding и R12A normative decisions. R12A определяет **static qualification**, не меняет production accounting и не доказывает брокерскую подлинность. Исторический `ADMIN_ACCEPTED` в README не является разрешением реализации 02B-R1.

## CR-01 — consumption против authoritative allocation

Authority возвращает типизированный результат `FOUND_RECONCILED`, `NOT_FOUND_COMPLETE`, `UNAVAILABLE`, `CONFLICT`. Только полный, проверенный registry позволяет доказать отсутствие prior consumption; `hasPriorConsumption=false` недостаточно. После рестарта отсутствие восстановленной записи означает `UNAVAILABLE`, пока полнота истории не доказана.

Проверяются независимо от входного proof: AccountLogin, Symbol, Magic, CycleID, DealID/SourceDealKey, AllocationID/SourceAllocationKey, AllocationEventID, policy version, bucket, consumer purpose, PlanID, ActionID, StateRevision, authoritative snapshot/schema/revision и сумма. AllocationEventID не равен ConsumptionEventID: это разные события, но оба должны ссылаться на один authoritative allocation. Нельзя извлекать owner только из непроверенной строки ключа.

Запрос имеет amount/currency и expected allocation revision. Порядок: восстановить authority → найти уже committed event → exact payload даёт NO_OP без проверки текущего available как нового расхода → altered payload даёт CONFLICT → новый event проходит ownership/source/purpose/remaining checks → атомарный journal commit уменьшает balance один раз. `ALLOW` означает допустимость в тестовом контракте, а не отправку сделки. Исходники: [Include/Money/HSBI_ReserveAllocationTypes.mqh:25](../Include/Money/HSBI_ReserveAllocationTypes.mqh#L25) — `HSBI_ValidateReserveConsumption`; [Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:35](../Include/Money/HSBI_ReserveCatchUpEvaluator.mqh#L35) — `HSBI_EvaluateReserveCatchUp`.

## CR-02 — независимая Money Proof Identity

`Confirmed Deal → Reconciled Economic Record → Authoritative Allocation → Expected Identity → Proof Verification`.

Confirmed означает успешное чтение конкретной сделки из broker deal history в требуемом account scope, а не `DealID>0`, `actual=true` или `fillsConfirmed=true`. Сверка journal ↔ history ↔ positions подтверждает Role/Cycle/Action/Plan, которые нельзя считать брокерскими полями по одному comment. Snapshot контекста PlanID/StateRevision/market/cost строится отдельно от submitted proof. Far-loss proof имеет отдельный source/role/direction и проходит независимую проверку.

Expected identity собирается из reconciled record + committed allocation + актуального immutable plan/snapshot. Proof только предъявляет identity, canonical payload digest и ссылку на authority. Проверяются весь immutable payload, Profit/Swap/Commission/Fee/DealNet, policy/bucket/remaining, digest, freshness, snapshot lineage. Неизвестный source/event или отсутствие history — REJECT при полном доступном registry; недоступный registry — UNAVAILABLE. Ненулевой вымышленный DealID=999 не проходит. Источники: [Include/Money/HSBI_MoneyProofIdentity.mqh:16](../Include/Money/HSBI_MoneyProofIdentity.mqh#L16) — `HSBI_IsSameMoneyProofIdentity`; [Include/Planning/HSBI_NewFarSolver.mqh:94](../Include/Planning/HSBI_NewFarSolver.mqh#L94) — `HSBI_SolveNewFar`, строки 119–125 (запись proof и self-copy expected).

## CR-03 — immutable Economic Record

Обязательные поля: schema/canonicalization version, AccountLogin, broker/server identity, Symbol, Magic, CycleID, PlanID, ActionID, EventID, DealTicket, OrderTicket, PositionIdentifier, Role, EntryType, Direction, Volume, Price, Profit, Swap, Commission, Fee, DealNet, Timestamp с исходной точностью, SourceDealKey, provenance/reconciliation reference. Отдельный mutable validation status не входит в экономическое содержимое; его доверенность не создаётся входным флагом.

SourceDealKey должен содержать account namespace (AccountLogin и broker/server) и DealTicket; Symbol/Magic/Cycle — обязательные связанные поля authority. Текущий ключ `Symbol|Magic|CycleID|DealTicket` может совпасть на двух счетах; в Economic DTO отсутствуют AccountLogin и PlanID. Нельзя дописать фиктивные значения миграцией: неизвестный account → UNAVAILABLE/manual reconciliation. Сохранять все компоненты signed DealNet и сверять их сумму. Source equality с изменением любого immutable поля → CONFLICT, exact canonical record → NO_OP. Числа нормализуются по версии precision/currency/grid, а не усечением до 8 знаков с потерей различий. Источник: [Include/Money/HSBI_EconomicLedgerTypes.mqh:7](../Include/Money/HSBI_EconomicLedgerTypes.mqh#L7) — `HSBI_BuildSourceDealKey`; [Include/Money/HSBI_EconomicLedgerTypes.mqh:9](../Include/Money/HSBI_EconomicLedgerTypes.mqh#L9) — `HSBI_SameEconomicRecord`; [Include/Money/HSBI_EconomicLedgerTypes.mqh:10](../Include/Money/HSBI_EconomicLedgerTypes.mqh#L10) — `HSBI_ClassifyEconomicDuplicate`.

## CR-04 — allocation и conservation (предложение D-01)

Разделить immutable `AllocationGrant` и mutable `BucketBalance`. Grant: owner/source/event/policy/schema, original per-bucket amounts, currency/precision, reconciled source digest. Для committed grant: `ΣOriginalGrant[b]=AllocatableActualDealNet`; отдельный `Unallocated=0`. Для каждого bucket: `Remaining[b]+Consumed[b]=OriginalGrant[b]`; при резервировании `Available[b]=Remaining[b]-Reserved[b]≥0`. Нельзя прибавлять consumed к original grants и тем самым считать деньги дважды. В intermediate состоянии нужны phase и явный Unallocated, который нельзя тратить.

Replay grant сравнивает **каждый bucket**, policy version, source net/digest и весь immutable payload. Balance changes разрешены только отдельным committed consumption/release event. Если replay-сообщение содержит balance snapshot, его изменение при том же event также CONFLICT; законное новое consumption не является altered replay исходного grant. Все money finite/nonnegative; negative actual DealNet учитывается в economic result, но не создаёт grant. Residual — учтённый bucket, не молча потерянный остаток. Источники: [Include/Money/HSBI_AllocationLedgerTypes.mqh:7](../Include/Money/HSBI_AllocationLedgerTypes.mqh#L7) — `HSBI_ValidateAllocationConservation`; [Include/Money/HSBI_AllocationLedgerTypes.mqh:8](../Include/Money/HSBI_AllocationLedgerTypes.mqh#L8) — `HSBI_ClassifyAllocationDuplicate`.

## CR-05 — слои проверки

Локальные DTO validators проверяют форму и арифметику; authority boundary проверяет owner/source/version/current revision и доступность registry; commit boundary — exactly-once. Нельзя требовать, чтобы простой bucket helper сам читал счёт, но нельзя использовать его bool как authorization. Все пути к Catch-Up/NewFar должны доминироваться полной проверкой authority.

Сейчас [Include/Money/HSBI_MoneyState.mqh:5](../Include/Money/HSBI_MoneyState.mqh#L5) — `HSBI_ValidateMoneyState` игнорирует valid/revision и допускает +infinity; [Include/Money/HSBI_AllocationLedgerTypes.mqh:7](../Include/Money/HSBI_AllocationLedgerTypes.mqh#L7) — `HSBI_ValidateAllocationConservation` пропускает отрицательные компенсирующие buckets и under-allocation; [Include/Money/HSBI_AllocationLedgerTypes.mqh:9](../Include/Money/HSBI_AllocationLedgerTypes.mqh#L9) — `HSBI_CanConsumeBucket` защищает FinalReserve от PartialFar, но допускает неизвестный enum; [Include/Money/HSBI_AllocationLedgerTypes.mqh:10](../Include/Money/HSBI_AllocationLedgerTypes.mqh#L10) — `HSBI_CanConsumeAmount` не проверяет valid/source. Поиск по всему production дереву не обнаружил их обязательных callers: это DTO helpers, не доказанный защищённый pipeline. Это **не доказательство выполненной торговой транзакции**; обязательность внешнего слоя UNPROVEN. Catch-Up напрямую вызывает другие validators и сохраняет разрывы CR-01/02. Пропущенный слой нельзя оправдать существованием runtime guards другого назначения.

## CR-06 — объём BigCore

По Docs/04 положительный raw Core после rounding обязан оставаться брокерски допустимым, либо весь кандидат отклоняется. F=0.10, Rc=0.01, Rt=3, Rs=0.1, min=step=0.01: rawCore=0.001 → Core=0; Trend=0.30; Small=0.01; slope=0.19. Текущий geometry возвращает valid. Исправление geometry на данном этапе запрещено; regression в matrix и harness. Источник: [Include/Planning/HSBI_GeometrySolver.mqh:21](../Include/Planning/HSBI_GeometrySolver.mqh#L21) — `HSBI_SolveBigGeometry`, строки 31–35.

## CR-07 — outcomes и exactly-once

`NO_OP`: exact committed event, delta buckets=0, revision unchanged, action count unchanged. `CONFLICT`: тот же event/key и иной payload, reconciliation, никаких balance changes. `REJECT`: известный чужой/недопустимый source, amount/purpose/geometry. `UNAVAILABLE`: authority/history/revision/freshness не доказаны; false prior не трактуется как clean start. Event identity и payload digest включают amount/bucket/currency/policy/owner/plan/revision. Нужен durable registry всех consumption, а не одного prior key. Миграция старой key без amount не может доказать replay equality.

## CR-08 — recovery и persistence

Доказать journal completeness, chain/checksum/schema, previous/current marker и history reconciliation до выдачи available money. Crash до/после prepare/commit, после consumption до snapshot и после snapshot до acknowledgement не должен ни восстанавливать spent bucket, ни терять подтверждённое событие. Сначала повтор committed event классифицируется NO_OP, затем новый event сверяется с текущими balances. При torn/unknown history → UNAVAILABLE/CONFLICT без auto-resume. [Include/Persistence/HSBI_PersistenceInterface.mqh:7](../Include/Persistence/HSBI_PersistenceInterface.mqh#L7) — `HSBI_PersistSnapshotStub` возвращает failure stub: production guarantee пока UNPROVEN. Полный durable IO — отдельный ограниченный этап после утверждения D-08, не фиктивный bool-fix.

## CR-09 — WORST_CASE (DECISION_REQUIRED)

Docs/30 задаёт экстремумы margin/risk/exposure/transition loss, но не определяет, что worst для Catch-Up — maximum TransitionLoss. Текущий aggregator выбирает именно этот уровень. Контрпример двух полных синтетических levels: L1 TransitionLoss=100, Reserve=50, FarLoss=20, buffer=1 → margin=29; L2 TransitionLoss=10, Reserve=5, FarLoss=20, buffer=1 → margin=-16. Обоим задаётся lot gate, например share=0.5, Bnet=4, F=1. Aggregate выбирает L1, хотя L2 недостаточен. Это проверка локального selector на предъявленных DTO, не брокерски достижимой траектории.

Варианты для администратора: минимум нормализованного Catch-Up margin по всем допустимым уровням с проверкой всех source proofs; либо явно оговорённый один maximum-loss control level с признанием отсутствия all-level гарантии. Рекомендуется первый вариант, с детерминированным tie-break и включением всех metrics/proofs в digest. Это дополнительное решение к D-01–D-08; самостоятельно политика не меняется. Источник: [Include/Planning/HSBI_FutureSmallProofAggregator.mqh:23](../Include/Planning/HSBI_FutureSmallProofAggregator.mqh#L23) — `HSBI_AggregateFutureSmallProof`, строка 50.

## CR-10 — роли Reserve и money typing

При Core=0, Trend=0, Small=10 точная production RHS даёт reserveGainMoney=10. При Core=10, Small=0 положительный контроль даёт 10. Это семантический дефект aggregate Reserve metric; прямой расход Small через NewFar не доказан: NewFar использует Core proof. Формула остаётся неизменной до D-03. Projected Small доход может стать actual доходом после подтверждённого close, но bucket назначения решает администратор. Источники: [Include/Money/HSBI_BasketMoneyEvaluator.mqh:11](../Include/Money/HSBI_BasketMoneyEvaluator.mqh#L11) — `HSBI_EvaluateBasketMoney`, строка 17; [Include/Planning/HSBI_FutureSmallSolver.mqh:140](../Include/Planning/HSBI_FutureSmallSolver.mqh#L140) (Core proof).

## Проверяемость и границы

Все CR имеют executable vectors в `Tests/Contracts/NEXT_STAGE_02B_R0_ADVERSARIAL_MATRIX.json`. Test-only oracle не импортирует production expected outcomes. C++ subset исполняет извлечённые тела MQL helpers и точные строки assembly/formula, но shim не является MQL5 компилятором, terminal или broker. MQL5 harness подготовлен, compile/runtime NOT_RUN. Source mutations применяются к отдельной копии Include внутри временного Tests-каталога, production не меняется. Принятие этих предложений не разрешает торговлю.

## Утверждение администратора

D-01…D-08: см. отдельные поля в `Reports/NEXT_STAGE_02B_R0_DECISIONS_REQUIRED_RU.md`.
CR-09 WORST_CASE: вариант ______; критерий ______; tie-break ______; администратор ______; дата ______; подпись/ID решения ______. До заполнения — DECISION_REQUIRED.
