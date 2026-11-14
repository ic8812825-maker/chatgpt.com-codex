# MONEY CONTRACT — 16 решений владельца

BASE_SHA=398da88424f3fb7b30e5315fbc3bf89219dd9ad2. Все рекомендации **PROPOSED**. ADMIN_APPROVAL_COMPLETE=NO. MONEY_CONTRACT_OWNER_APPROVED=NO.

| Display | Canonical DecisionId | Вопрос | Рекомендуемый вариант | OwnerApproval |
|---|---|---|---|---|
| D-01 | D-01 | Разделение денежных фаз | A | AWAITING_ADMIN_APPROVAL |
| D-02 | D-02 | Денежные типы / source status | A | AWAITING_ADMIN_APPROVAL |
| D-03 | D-03 | Reserve ownership / Small | A | AWAITING_ADMIN_APPROVAL |
| D-04 | D-04 | База Catch-Up loss | A | AWAITING_ADMIN_APPROVAL |
| D-05 | D-05 | Transition A/B/C | B | AWAITING_ADMIN_APPROVAL |
| D-06 | D-06 | Cost basis / FinalClose | A | AWAITING_ADMIN_APPROVAL |
| D-07 | D-07 | Execution / Journal / Restart | A | AWAITING_ADMIN_APPROVAL |
| D-08 | D-08 | Source identity / broker authority | A | AWAITING_ADMIN_APPROVAL |
| D-09 | CR-09 | All-level NewFar / FutureSmall | A | AWAITING_ADMIN_APPROVAL |
| D-10 | NUM-EXACT-1 | Settled precision | A | AWAITING_ADMIN_APPROVAL |
| D-11 | NUM-DOMAIN-1 | Currency / range / lot & price grids | A | AWAITING_ADMIN_APPROVAL |
| D-12 | NUM-CODEC | Schema / canonical codec | A | AWAITING_ADMIN_APPROVAL |
| D-13 | SNAP-FIXTURE-1 | Freshness / snapshot content | A | AWAITING_ADMIN_APPROVAL |
| D-14 | FUNDING-GLOBAL-ATTRIBUTION | Global source funding | A | AWAITING_ADMIN_APPROVAL |
| D-15 | MQL-DOMAIN | Native acceptance | A | AWAITING_ADMIN_APPROVAL |
| D-16 | BALANCE-SCHEMA-MAPPING | Legacy migration | A | AWAITING_ADMIN_APPROVAL |

Canonical IDs DG01/R0F сохранены. D-09…D-16 — только display labels. Источники: Docs/HSBI_DG01_CONTRACT_RESOLUTION_RU.md, Reports/HSBI_DG01_ADMIN_DECISION_BALLOT_RU.md, Reports/HSBI_FULL_SYSTEM_AUDIT_02_ADMIN_DECISIONS_RU.md, Reports/NEXT_STAGE_02B_R0F_ADMIN_APPROVAL_PACKAGE_RU.md и AUDIT03 ERR/IMP. Historical source/conflict поля извлечены из DG01, новые рекомендации ниже отделены. Полная authority precedence всех исторических материалов остаётся частью незавершённого AUDIT03.

## D-01 / D-01 — Разделение денежных фаз

**ExistingNorm:** Docs08/legacy Remaining и C3 Gross naming conflict.

**Conflict:** Bare Gross смешивает исходный grant и неиспользованный остаток.

**OptionA:** G=Consumed+Reserved+Free на каждом bucket; RemainingGross=Reserved+Free. Отдельно allocation C/P/T/K/R суммируется в исходный grant, это другая ось.

**OptionB:** Legacy RemainingGross остаётся read-only view; consumption использует только явно вычисленный Free.

**RecommendedOption:** A

**Rationale:** Исключает повторное включение already reserved/consumed money.

**Risk:** Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.

**Compatibility:** Новая schema/version; старые bytes неизменны. Unknown namespace/units/body → quarantine. Legacy не переименовывается в Free.

**Dependencies:** D-10/D-14/D-16

**RequiredTests:** UNDERALLOCATION, EXHAUSTED-VECTOR, COMPETING-B-STALE

**OwnerApproval:** AWAITING_ADMIN_APPROVAL

AdministratorDecision: ____________________
Approved wording/version/SHA: ____________________
Owner/date: ____________________

## D-02 / D-02 — Денежные типы / source status

**ExistingNorm:** Docs08 actual deals; C3 disjoint money types.

**Conflict:** Одинаковые числа и kind-флаги не подтверждают actual или spendable ресурс.

**OptionA:** Captured → Reconciled → Eligible → Allocated → Reserved → Consumed — разные состояния с подтверждёнными переходами. Projected существует отдельно и не fund.

**OptionB:** Только planning views до появления независимого provider; spending всегда UNAVAILABLE.

**RecommendedOption:** A

**Rationale:** Bool actual/valid в предъявленном DTO не является независимым фактом.

**Risk:** Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.

**Compatibility:** Новая schema/version; старые bytes неизменны. Unknown namespace/units/body → quarantine. Legacy не переименовывается в Free.

**Dependencies:** D-08/D-13/D-14

**RequiredTests:** P0-12, P0-03, projected source rejection

**OwnerApproval:** AWAITING_ADMIN_APPROVAL

AdministratorDecision: ____________________
Approved wording/version/SHA: ____________________
Owner/date: ____________________

## D-03 / D-03 — Reserve ownership / Small

**ExistingNorm:** Docs31 роли BigCore/BigTrend; production LevelMoney reserveGain включает Small.

**Conflict:** Small-only profit может ошибочно получить Big Reserve назначение.

**OptionA:** Small-only profit удерживается как ResidualHeld; BigReserve funding только от утверждённых BigCore/BigTrend closing sources.

**OptionB:** Small transfer допускается отдельным approved debit/credit event с исходным SourceKey и ownership.

**RecommendedOption:** A

**Rationale:** Смена роли не создаёт вторую прибыль; сохраняет существующее ограничение ролей.

**Risk:** Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.

**Compatibility:** Новая schema/version; старые bytes неизменны. Unknown namespace/units/body → quarantine. Legacy не переименовывается в Free.

**Dependencies:** D-02/D-14

**RequiredTests:** Core0 Trend0 Small10 → BigReserve0 Residual10; PLANNED

**OwnerApproval:** AWAITING_ADMIN_APPROVAL

AdministratorDecision: ____________________
Approved wording/version/SHA: ____________________
Owner/date: ____________________

## D-04 / D-04 — База Catch-Up loss

**ExistingNorm:** Far loss absolute/incremental proposals; historical baseline lineage не реализован.

**Conflict:** Incremental10 ошибочно покрывается Reserve30 при absolute50.

**OptionA:** AbsoluteFarLoss=max(0,−ProjectedCloseNowFarNet); projected preview не тратит confirmed reserve.

**OptionB:** IncrementalLoss только после утверждения baseline, lineage, currency и restart policy.

**RecommendedOption:** A

**Rationale:** Reserve30 не покрывает absolute loss50 при incremental10.

**Risk:** Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.

**Compatibility:** Новая schema/version; старые bytes неизменны. Unknown namespace/units/body → quarantine. Legacy не переименовывается в Free.

**Dependencies:** D-02/D-06/D-09

**RequiredTests:** proof50/eligible100 → REJECT; lossProof−50/loss0 → REJECT; PLANNED public

**OwnerApproval:** AWAITING_ADMIN_APPROVAL

AdministratorDecision: ____________________
Approved wording/version/SHA: ____________________
Owner/date: ____________________

## D-05 / D-05 — Transition A/B/C

**ExistingNorm:** Docs08 signed closing net; C2/C3 текущий batch assessment, без sticky журнала.

**Conflict:** Current final loss, историческое breach и peak loss неэквивалентны.

**OptionA:** A: current signed loss=max(0,−Σactual confirmed batch net); соответствует Docs/08:21 и Docs/13:9.

**OptionB:** B: current signed accounting плюс отдельный sticky safety breach до ручного reset.

**OptionC:** C: peak historical prefix loss=max_j max(0,−Σ_{i≤j}Net_i); хранить отдельно от current loss; reset и ordering policy обязательны.

**RecommendedOption:** B

**Rationale:** Сохраняет actual accounting A и не теряет нарушение cap на раннем prefix. Это изменение safety policy требует утверждения.

**Risk:** Final cumulative Net85 cannot reconstruct earlier breach15. Missing ordered history/reset journal => UNAVAILABLE for sticky/peak migration; do not infer no breach.

**Compatibility:** Новая schema/version; старые bytes неизменны. Unknown namespace/units/body → quarantine. Legacy не переименовывается в Free.

**Dependencies:** D-06/D-07/D-13

**RequiredTests:** Fills−15,+100 cap12: current0,sticky true,peak15; ordered history/restart PLANNED

**OwnerApproval:** AWAITING_ADMIN_APPROVAL

AdministratorDecision: ____________________
Approved wording/version/SHA: ____________________
Owner/date: ____________________

## D-06 / D-06 — Cost basis / FinalClose

**ExistingNorm:** Signed Profit/Swap/Commission/Fee и independent cost coverage; buffer headroom не actual debit.

**Conflict:** Неизвестное пересечение basis/window может дать двойное вычитание или скрытый ноль.

**OptionA:** Уникальный CostID+basis+window+includedIn компонентах; каждый применимый расход учтён ровно один раз; unknown → UNAVAILABLE.

**OptionB:** Сводный buffer допустим только с независимой полной coverage map и доказанным отсутствием overlap.

**RecommendedOption:** A

**Rationale:** Spread уже включён при open Ask/close Bid; повторное вычитание меняет PnL. FinalClose требует accounting И coverage/risk gates.

**Risk:** Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.

**Compatibility:** Новая schema/version; старые bytes неизменны. Unknown namespace/units/body → quarantine. Legacy не переименовывается в Free.

**Dependencies:** D-02/D-13

**RequiredTests:** SIGNED-DEAL, P0-14, SPREAD-EXPANSION, MARGIN-SHORTAGE

**OwnerApproval:** AWAITING_ADMIN_APPROVAL

AdministratorDecision: ____________________
Approved wording/version/SHA: ____________________
Owner/date: ____________________

## D-07 / D-07 — Execution / Journal / Restart

**ExistingNorm:** Docs08 exact NO_OP/changed CONFLICT; C3 in-memory != durable/concurrent.

**Conflict:** Replay ordering, durable commit и отсутствие истории смешивались.

**OptionA:** Атомарно фиксировать source balance, revision и immutable receipt; validate full body перед NO_OP; unknown outcome → block/reconcile, не redispatch.

**OptionB:** Оставить только чистые preview и in-memory model до готовности durable provider.

**RecommendedOption:** A

**Rationale:** Локальное сравнение revision не предотвращает два commit и не доказывает crash durability.

**Risk:** Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.

**Compatibility:** Новая schema/version; старые bytes неизменны. Unknown namespace/units/body → quarantine. Legacy не переименовывается в Free.

**Dependencies:** D-08/D-10/D-13/D-14

**RequiredTests:** P0-08/09/10/13; crash-between-write-and-ack PLANNED

**OwnerApproval:** AWAITING_ADMIN_APPROVAL

AdministratorDecision: ____________________
Approved wording/version/SHA: ____________________
Owner/date: ____________________

## D-08 / D-08 — Source identity / broker authority

**ExistingNorm:** Docs08/31/32 independent source; production source key без Account/Broker/Server.

**Conflict:** Expected из proof и key по symbol/magic/cycle/deal допускают самоподтверждение и namespace collisions.

**OptionA:** Абстрактная broker/server/account/deal identity; full immutable typed body и independent history provider. Wire format утверждается отдельно D-12.

**OptionB:** Совместимый legacy alias только для lookup после independent mapping в новый namespace, не источник funding.

**OptionC:** Legacy-only временно read-only; до однозначного broker namespace funding UNAVAILABLE.

**RecommendedOption:** A

**Rationale:** Magic/Cycle — attribution, не новая broker operation. Рекомендуется namespace, но спорный wire SourceKey здесь не выбран.

**Risk:** Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.

**Compatibility:** Новая schema/version; старые bytes неизменны. Unknown namespace/units/body → quarantine. Legacy не переименовывается в Free.

**Dependencies:** D-02/D-12/D-13/D-16

**RequiredTests:** P0-01, POSITION, ROLE, PRICE, DIFFERENT-account/server/deal, malformed key

**OwnerApproval:** AWAITING_ADMIN_APPROVAL

AdministratorDecision: ____________________
Approved wording/version/SHA: ____________________
Owner/date: ____________________

## D-09 / CR-09 — All-level NewFar / FutureSmall

**ExistingNorm:** Production worstTransitionLossLevel; C3 A all-level/B single-level.

**Conflict:** MaxTransition level не гарантирует минимальный CatchUpMargin; прогноз не actual resource.

**OptionA:** ALL_LEVEL: min CatchUpMargin_i>0 для каждого required level, отдельные доступность/margin/risk proof и quantified tail.

**OptionB:** SINGLE_LEVEL: только scope-labelled preview, без all-level claim и без spending authority.

**RecommendedOption:** A

**Rationale:** argmax TransitionLoss не равен argmin CatchUpMargin. Непроверенный tail не становится доказанным.

**Risk:** Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.

**Compatibility:** Новая schema/version; старые bytes неизменны. Unknown namespace/units/body → quarantine. Legacy не переименовывается в Free.

**Dependencies:** D-04/D-06/D-13/D-14

**RequiredTests:** margins9/−11 transitions10/5 → all-level REJECT; PLANNED

**OwnerApproval:** AWAITING_ADMIN_APPROVAL

AdministratorDecision: ____________________
Approved wording/version/SHA: ____________________
Owner/date: ____________________

## D-10 / NUM-EXACT-1 — Settled precision

**ExistingNorm:** R0D Fraction reference; raw double внешняя граница и неподтверждённый MQL domain.

**Conflict:** Округление projected потерь и потеря малых дебетов могут менять знак proof.

**OptionA:** Окончательные posted суммы в checked signed64 minor units; projected double только с finite/range/error bounds и консервативной оценкой расходов.

**OptionB:** Checked wider fixed point/rational adapter с отдельно доказанными intermediates.

**RecommendedOption:** A

**Rationale:** Exact debit1 должен изменять MAX на1; нельзя сливать financial posting и raw capture.

**Risk:** Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.

**Compatibility:** Новая schema/version; старые bytes неизменны. Unknown namespace/units/body → quarantine. Legacy не переименовывается в Free.

**Dependencies:** D-11/D-12/D-15

**RequiredTests:** CENTS, HALF-EVEN, NEGATIVE-COST, NUM-OVERFLOW; I64 intermediate native PLANNED

**OwnerApproval:** AWAITING_ADMIN_APPROVAL

AdministratorDecision: ____________________
Approved wording/version/SHA: ____________________
Owner/date: ____________________

## D-11 / NUM-DOMAIN-1 — Currency / range / lot & price grids

**ExistingNorm:** R0D lattice10^-64 abs<10^65; fixture money digits0..8.

**Conflict:** Reference-domain существенно шире int64 minor units и broker precision facts.

**OptionA:** Versioned profile: currency code, confirmed digits, minor scale, signed64 checked range; broker lot min/max/step и price tick проверяются отдельно. Unknown precision → UNAVAILABLE.

**OptionB:** Multiword adapter расширяет range после отдельной native qualification; не использовать unlimited Python как MQL proof.

**RecommendedOption:** A

**Rationale:** 1e28 money не помещается в cents64; отказ лучше ложного PASS. Digits0..8 — кандидат supported profile, не broker факт.

**Risk:** Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.

**Compatibility:** Новая schema/version; старые bytes неизменны. Unknown namespace/units/body → quarantine. Legacy не переименовывается в Free.

**Dependencies:** D-10/D-13/D-15

**RequiredTests:** VOLUME-OFFGRID, PRICE-GRID, MILLS, NUM-OVERFLOW, INF-CAP

**OwnerApproval:** AWAITING_ADMIN_APPROVAL

AdministratorDecision: ____________________
Approved wording/version/SHA: ____________________
Owner/date: ____________________

## D-12 / NUM-CODEC — Schema / canonical codec

**ExistingNorm:** R0D fixture typed codec, R1 raw64/NFC proposal, C3 native codec не проверен.

**Conflict:** Wire identity и financial rounding смешивались; MQL compatibility не доказана.

**OptionA:** F64Z как кандидат raw capture: typed length-prefixed UTF8/finite binary64; exact integer money как отдельный тип; schema/profile versions обязательны.

**OptionB:** T17Z typed length-prefixed UTF8/scientific17 с полным native roundtrip evidence.

**RecommendedOption:** A

**Rationale:** Raw capture и settled posting различны. Выбор wire SourceKey остаётся AWAITING; этот лист не freeze формата.

**Risk:** Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.

**Compatibility:** Новая schema/version; старые bytes неизменны. Unknown namespace/units/body → quarantine. Legacy не переименовывается в Free.

**Dependencies:** D-08/D-10/D-11/D-15

**RequiredTests:** 1 vs string1 vs bool1, delimiter injection, non-NFC, +0/−0, ulong2^53+1; native PLANNED

**OwnerApproval:** AWAITING_ADMIN_APPROVAL

AdministratorDecision: ____________________
Approved wording/version/SHA: ____________________
Owner/date: ____________________

## D-13 / SNAP-FIXTURE-1 — Freshness / snapshot content

**ExistingNorm:** R0D content receipt; C2 ID/fresh только provider fixture assertion.

**Conflict:** ID999+fresh не доказывают content/freshness полного snapshot.

**OptionA:** Content-bound provider receipt: account/symbol/currency/window, observation time, expiry, costs, full positions fingerprint; future clock skew только из профиля.

**OptionB:** Provider ID-only attestation допускается лишь диагностически, без full proof.

**RecommendedOption:** A

**Rationale:** Самоподписанный snapshot и fresh=true не подтверждают актуальные позиции или costs.

**Risk:** Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.

**Compatibility:** Новая schema/version; старые bytes неизменны. Unknown namespace/units/body → quarantine. Legacy не переименовывается в Free.

**Dependencies:** D-08/D-12/D-15

**RequiredTests:** SNAPSHOT-MISMATCH; same ID/altered content, future timestamp, gap PLANNED provider

**OwnerApproval:** AWAITING_ADMIN_APPROVAL

AdministratorDecision: ____________________
Approved wording/version/SHA: ____________________
Owner/date: ____________________

## D-14 / FUNDING-GLOBAL-ATTRIBUTION — Global source funding

**ExistingNorm:** C3 source-local cap доказан, глобальные account debit/credit и concurrency UNPROVEN.

**Conflict:** Сумма grants одного источника не равна доказанному свободному капиталу всего счёта.

**OptionA:** Единый source registry сквозь roles/allocations/restarts; source grant разбивается один раз, transfer/reversal — отдельные события, CAS source-level.

**OptionB:** Ограничить гарантии fixture-local и блокировать все production funding до provider.

**RecommendedOption:** A

**Rationale:** Новый allocationEvent не восстанавливает исчерпанный источник. Account equity не равно free source inventory.

**Risk:** Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.

**Compatibility:** Новая schema/version; старые bytes неизменны. Unknown namespace/units/body → quarantine. Legacy не переименовывается в Free.

**Dependencies:** D-01/D-02/D-07/D-08

**RequiredTests:** SECOND-ALLOCATION-EVENT, P0-03, COMPETING-B-STALE; real concurrency PLANNED

**OwnerApproval:** AWAITING_ADMIN_APPROVAL

AdministratorDecision: ____________________
Approved wording/version/SHA: ____________________
Owner/date: ____________________

## D-15 / MQL-DOMAIN — Native acceptance

**ExistingNorm:** C3 Python signed64 simulation и g++ subset; MetaEditor NOT_RUN.

**Conflict:** Математическая проверка не доказывает нативные ulong/long/double/UTF8 conversions.

**OptionA:** MetaEditor strict compile, long/ulong bounds, finite-only double, UTF8/codec goldens, revision overflow и actual logs обязательны.

**OptionB:** Сохранить только offline reference scope и запрет acceptance до готовности MT5.

**RecommendedOption:** A

**Rationale:** g++ shim и Python не устанавливают MQL5 runtime semantics.

**Risk:** Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.

**Compatibility:** Новая schema/version; старые bytes неизменны. Unknown namespace/units/body → quarantine. Legacy не переименовывается в Free.

**Dependencies:** D-10/D-11/D-12

**RequiredTests:** native_close.mq5 подготовлен; MQL5 tests NOT_RUN

**OwnerApproval:** AWAITING_ADMIN_APPROVAL

AdministratorDecision: ____________________
Approved wording/version/SHA: ____________________
Owner/date: ____________________

## D-16 / BALANCE-SCHEMA-MAPPING — Legacy migration

**ExistingNorm:** Legacy RemainingGross и новый Free profile.

**Conflict:** Silent rename возвращает reserved/consumed ресурс в available.

**OptionA:** Append-only migration по independent receipts с известными currency/scale/owner/grant/consumed/reserved/free; legacy bytes не переписывать. Unknown → quarantine.

**OptionB:** Legacy schema остаётся read-only; никакого автоматического funding/migration.

**RecommendedOption:** A

**Rationale:** Remaining40 и Reserved15 дают Free25, не40; неизвестная history не complete-empty.

**Risk:** Сохранить legacy bytes/schema/hash; неизвестные namespace, units, owners или policy → quarantine/UNAVAILABLE; current terminal facts не замещают историю.

**Compatibility:** Новая schema/version; старые bytes неизменны. Unknown namespace/units/body → quarantine. Legacy не переименовывается в Free.

**Dependencies:** D-01/D-07/D-08/D-10

**RequiredTests:** G50,C10,R15,F25; unknown owner/schema → UNAVAILABLE; PLANNED migration

**OwnerApproval:** AWAITING_ADMIN_APPROVAL

AdministratorDecision: ____________________
Approved wording/version/SHA: ____________________
Owner/date: ____________________

Решение каждого пункта должно однозначно указывать вариант и текст исключений. Утверждение этих контрактов не разрешает production implementation или trading; R1.1 нужен отдельный scoped task. D-05 B не считается уже действующей нормой: declared current loss A сохранён, sticky предлагается как отдельный safety gate.
