# R0G — узкие предпосылки Minimal R1.1

BASE_SHA=bcaa766568b9fe7eec0781a8c6efbb288cf16dae

PROPOSED / AWAITING_ADMIN_APPROVAL. Только подготовка Minimal R1.1; ни одного production изменения или утверждения.

Источники: `Include/Money/HSBI_EconomicLedgerTypes.mqh:6` struct, `:7` BuildSourceDealKey, `:8` ValidateEconomicRecord, `:9` SameEconomicRecord, `:10` ClassifyEconomicDuplicate, `:11` SerializeEconomicRecord, `:12` IsHarvestSourceEntry. R0F ECONOMIC_IDENTITY_SPEC/NUMERIC_CODEC_OPTIONS/R1_IMPLEMENTATION_SPEC; frozen `hsbi_02b_r0f_contract_candidate.py:record_shape/encode_record`; новые TestID в TEST_RESULTS.json.

| DecisionID | Minimal R1.1 dependency | Обоснование |
|---|---|---|
|D-01|DEFERRED_FOR_LOCAL_IDENTITY|Не блокирует локальную equality: нет allocate/consume или денег на выходе. Conservation остаётся обязательной при future funding.|
|D-02|DIRECT_BLOCKER|Обязательно: raw captured/source identity не является projected profit, reconciled posted net или available money. Equality не создаёт grant.|
|D-03|DEFERRED_FOR_LOCAL_IDENTITY|Не блокирует equality: Role immutable проверяется, но право harvest/перевода не определяется. IsHarvestSourceEntry нельзя использовать как полное разрешение funding.|
|D-04|DEFERRED_FOR_LOCAL_IDENTITY|Не блокирует: FarLoss отсутствует в pure source identity API.|
|D-05|DEFERRED_FOR_LOCAL_IDENTITY|Не блокирует: batch risk/reset не исполняются, A/B/C остаются невыбранными.|
|D-06|DEFERRED_FOR_LOCAL_IDENTITY|Не блокирует: компоненты фиксируются отдельно, размеры/coverage costs и buffers не вычисляются.|
|D-07|DEFERRED_FOR_LOCAL_IDENTITY|Не блокирует локальную classification: NO_OP является сравнением, не durable exactly-once. Backend/CAS отсутствуют.|
|D-08|DIRECT_BLOCKER|Обязательно: key/EA origin нельзя подтверждать предъявленным payload. Применяется только boundary independent provider inputs, не реализация брокерского provider.|
|CR-09|DEFERRED_FOR_LOCAL_IDENTITY|Не блокирует: level/Catch-Up proof не вызывается и не создаётся.|
|NUM-EXACT-1|NARROW_SUBSET_REQUIRED|Ограниченно обязательно: exact immutable raw comparison/no epsilon. Полная арифметика settled/projected money не используется в локальной equality.|
|NUM-DOMAIN-1|NARROW_SUBSET_REQUIRED|Ограниченно обязательно: профиль raw binary64 и точные ID bounds; account balance domain/aggregation остаются позже.|
|NUM-CODEC|DIRECT_BLOCKER|Обязательно для authoritative serializer в данном candidate ballot. При отказе от codec нужен другой явно урезанный ballot equality-only; нельзя молча считать diagnostic string authoritative.|
|SNAP-FIXTURE-1|DEFERRED_FOR_LOCAL_IDENTITY|Не требуется для pure equality/serialization: snapshot не часть economic body. Будущий provider receipt и current snapshot требуют отдельной интеграции.|
|FUNDING-GLOBAL-ATTRIBUTION|DEFERRED_FOR_LOCAL_IDENTITY|Не блокирует pure equality; глобальная уникальность funding НЕ доказана. NEW не разрешение credit, integration требует source-level unique index/CAS позже.|
|MQL-DOMAIN|DIRECT_BLOCKER|Обязательно: типы long/ulong/double, finite/UTF8/resource bounds и exact equality должны быть заданы до native implementation.|
|BALANCE-SCHEMA-MAPPING|DEFERRED_FOR_LOCAL_IDENTITY|Не блокирует: balance state не читается/не мигрирует. Economic legacy migration отдельно ограничена quarantine.|

Дополнительные обязательные approvals: ECONOMIC-SCHEMA-1 (29fields/key/provenance envelope), LEGACY-COMPAT-1 (old diagnostics vs V2 financial prohibition), NATIVE-ACCEPTANCE-1. Это технические уточнения R0F, не новая экономическая policy. Все16 прежних decisions остаются AWAITING, в R0G ничего автоматически не approved.

Есть разница между готовностью пакета решения и готовностью production приёмки. Native codec/API tests отсутствуют => production acceptance BLOCKED; администратор может рассмотреть conditional contract decision, но start всё равно NO до отдельного задания. Независимый broker/EA origin provider не реализуется в одном header; future classifier получает типизированные независимые view и доказывает только body/lookup binding. Полная provenance chain не доказана.

C3 cost status gap не блокирует local identity equality, потому cost API в этом scope не вызывается. R7/R0 historical FAIL остаются frozen; R0G не повторяет общий аудит/полную regression suite и не объявляет их исправленными. R0F16/package preservation проверяются новым read-only checker; отдельные нативные/runtime регрессии NOT_RUN.

One-file additive API технически описуем без новых helper headers. Однако если обязательная цель — переподключить действующий external financial consumer, заменить unsafe legacy classifier либо выполнить provider/durable funding, это другой scope и blocker. Нет скрытого объявления старого дефекта исправленным: production неизменён, новая Python модель не remediation.
