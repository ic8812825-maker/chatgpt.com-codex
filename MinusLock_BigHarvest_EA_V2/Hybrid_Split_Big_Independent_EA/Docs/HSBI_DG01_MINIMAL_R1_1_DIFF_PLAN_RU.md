# DG01 — точный неприменённый проект Minimal R1.1

ONE_FILE_LOCAL_API_FEASIBLE=YES_STATIC_CONDITIONAL
ONE_FILE_COMPLETE_REMEDIATION_NOT_FEASIBLE=YES
R1_1_START_ALLOWED=NO

## Что именно подготовлено

`Tests/Reference/HSBI_DG01_MINIMAL_R1_1_CANDIDATE.patch` — точный unified diff к baseline `92a55371299439f2ff33494497cde2aa78013d77`, только `Include/Money/HSBI_EconomicLedgerTypes.mqh`. Выполнен лишь `git apply --check`, код не применён. Test-only `HSBI_DG01_identity_candidate.mqh` содержит тот же добавляемый body, но включает старый header из Tests; package checker сверяет body и diff. Проект не является production helper.

Не меняются старый struct, имена, сигнатуры, equality/classifier/serializer и фактическое legacy поведение. Добавляются отдельная V2 struct29 immutable fields, известность facts mask как envelope metadata, enum NEW/NO_OP/CONFLICT/REJECT/UNAVAILABLE, shape validator, logical source-key equality, full immutable payload equality и pure classifier с независимыми authority+complete registry входами. Это не legacy migration и не новый funding path.

## Контракт API кандидата

EconomicEventID, AllocationEventID и ConsumptionEventID — разные namespaces: первое принадлежит immutable origin, второе allocation vector, третье consumption journal. Произвольное равенство между ними не требуется.

SourceKey=(Broker,Server,AccountLogin,DealTicket). Magic/Cycle/Symbol/Role входят в immutable body, а не создают новый источник. При одном key изменённые Profit/Swap/Commission/Fee/Net и прочие поля — CONFLICT; одинаковый Net не заменяет components. NEW означает только independently confirmed identity observation и отсутствие key в complete registry, не доступные деньги.

Captured finite binary64 equality точная, без epsilon; +0/-0 эквивалентны только в proposed Z profile. В reference journal event IDs уникальны в своих namespaces, а порядок применения задаётся expected revision, не численным возрастанием EventID. Это отличается от fresh transaction event sequence и требует явного mapping, не подменяет OnTradeTransaction порядок. Integer IDs никогда не проходят через double; long/ulong типы не требуют суммирования для comparator. Malformed/nonfinite → REJECT, unknown facts/schema/provider/registry → UNAVAILABLE. Никакого UNAVAILABLE→NEW. Декодер обязан проверять wire types до приведения: после преобразования bool→long MQL struct уже не хранит исходный wire tag.

`knownFieldsMask` нужен для missing/unknown facts, чтобы false/0 в initialized struct не означали доказанный факт. sourcePlanApplicable=false требует sourcePlan0; аналогично policy. Currency/precision — независимый account/provider fact, не SYMBOL_DIGITS. Digits0..8 и positive price/volume — **proposed supported profile**, не универсальные broker limits. Все29 field-equality probes подготовлены в native harness. Typed role/entry fields V2 ещё не имеют утверждённого mapping в string wire fields F64Z; это отдельный schema/codec вопрос. Codec сериализация в этом локальном API **не реализована**: pure equality не объявляется полным NUM-CODEC или broker reconciliation. F64Z/T17Z проверяются отдельным test-only subject; выбор и native реализация потребуют owner решения.

Validate проверяет shape/captured domain, не выполняет арифметическую брокерскую reconciliation DealNet из компонентов. Её выполняет независимый provider с declared posted/raw policy. Входной bool independentSourceConfirmed и registryComplete сами по себе не удостоверяют receipt; это обязательная граница caller/provider, не новый доказанный источник истины.

## Почему полного исправления в одном файле нет

Старый classifier намеренно остаётся с прежней небезопасной семантикой. Additive V2 не устраняет FSA-001 во всех возможных путях. В74 текущих production sources lexical scan нашёл старые economic symbols только в исходном header; external/future consumers не проверены. Чтобы объявить полное remediation, надо утвердить diagnostic-only legacy policy, проверить всех consumers и подключить independent namespace/origin provider + registry reconciliation. Глобальные funding/restart/durable/CAS невозможно получить из equality header. Каждый дополнительный production-модуль требует отдельного расширенного allowlist, не разрешён здесь.

## Acceptance, stop и rollback

До первого production изменения: явный ballot по D-02/D-08/MQL-DOMAIN/schema+compatibility; NUM-CODEC для serialization части; отдельное задание с новым baseline/allowlist. До acceptance: MetaEditor strict compile полного EA и isolated harness, full-field changes, signed components, namespace, unknown legacy, nonfinite, zero policy, overflow/UTF8/codecs goldens, zero deltas и caller review. Одна successful compilation не означает native runtime PASS.

Legacy без Broker/Server/Account/origin/currency/precision — quarantine/UNAVAILABLE; нельзя достраивать текущими terminal facts или умножать timestamp до миллисекунд без источника. Minimal не пишет migration files. Rollback — отдельный обратимый remediation commit без on-disk преобразований; исходные bytes/schema сохраняются. Stop: unapproved contract, native incompatibility, новая зависимость/financial callsite вне allowlist, changed remote или необходимость dispatch/persistence.
