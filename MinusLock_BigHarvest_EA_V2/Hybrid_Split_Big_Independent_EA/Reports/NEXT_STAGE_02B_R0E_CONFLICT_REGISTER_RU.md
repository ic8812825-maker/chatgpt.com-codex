# 02B-R0E — реестр противоречий и решений

BASE_SHA=2d34c3378edc5f2df064282fa067bb4af2a1e3b0

Статус: PROPOSED / AWAITING_ADMIN_APPROVAL. Только audit/test-only; никаких production-изменений и торговли.

Проверено20 требований. Зарегистрировано18 записей: 9 SEMANTIC_CONFLICT, 6 ARCHITECTURE_DECISION, 1 MIGRATION_DECISION, 1 PROVENANCE_ERRATUM, 1 VERIFICATION_GAP. Последние9 не объявляются математическими противоречиями. Открыто16 административных решений.

## CF-01: D-01 — SEMANTIC_CONFLICT

ExistingRule / Conflict: R0D Remaining включает Reserved; простое трёхкомпонентное равенство с тем же полем повторно считает lock.

SourceAndApprovalEvidence: Docs/08; Docs/32; R0D NUM-BALANCE; историческая подпись APPROVAL_UNPROVEN.

ProposedRule: G=C+V+F; Gross=V+F; Available=F; COMMITTED ΣGrants=EligibleNet, PREPARED ΣGrants+Unallocated=EligibleNet и расход запрещён.

ProductionBehavior: см. DefectID в NEXT_STAGE_02B_R0E_PRODUCTION_REMEDIATION_PLAN_RU.md; Python не меняет MQL5.

MathematicalCounterexample: G50,C10,V15,Gross40,F25: 50=10+40=10+15+25, но 10+15+40=65.

RecommendedDecision: Сохранить Gross с отдельным Available либо перейти на Free. Рекомендуется явно версионированный Free-профиль, математический Gross-view для старых данных.

ApprovalStatus: AWAITING_ADMIN_APPROVAL / DECISION_REQUIRED.

## CF-02: D-02 — SEMANTIC_CONFLICT

ExistingRule / Conflict: Прогнозные proof допускаются историческим спецификационным слоем; они не доказывают фактический доступный ресурс.

SourceAndApprovalEvidence: Docs/04; Docs/08; Docs/31; историческая подпись APPROVAL_UNPROVEN.

ProposedRule: Раздельные ProjectedBasketNet/ProjectedCloseNowNet/ActualRealizedDealNet/ReconciledEconomicNet/AllocationGrant/AvailableReserve. Только независимая reconciliation открывает путь к grant. Полная пустая history → известный0; неполная →UNAVAILABLE.

ProductionBehavior: см. DefectID в NEXT_STAGE_02B_R0E_PRODUCTION_REMEDIATION_PLAN_RU.md; Python не меняет MQL5.

MathematicalCounterexample: Projected100 и нет eligible закрытий →0; history отсутствует →UNAVAILABLE, а не доказанный0.

RecommendedDecision: Прогноз использовать для planning либо смешивать с actual; рекомендуется первый вариант с типизированными переходами.

ApprovalStatus: AWAITING_ADMIN_APPROVAL / DECISION_REQUIRED.

## CF-03: D-03 — SEMANTIC_CONFLICT

ExistingRule / Conflict: Basket evaluator включает Small в reserveGainMoney. Значение projected не равно фактическому reserve posting.

SourceAndApprovalEvidence: Docs/04; Docs/24; Docs/32; историческая подпись APPROVAL_UNPROVEN.

ProposedRule: BigCore/BigTrend close sources после reconciliation и policy allocation; Small positive только ResidualHeld; opening costs в economic ledger без harvest grant; role/policy immutable.

ProductionBehavior: см. DefectID в NEXT_STAGE_02B_R0E_PRODUCTION_REMEDIATION_PLAN_RU.md; Python не меняет MQL5.

MathematicalCounterexample: Core0 Trend0 Small10 →BigReserve0, ResidualHeld10.

RecommendedDecision: Оставить раздельный Small residual либо разрешить трансфер отдельным будущим решением; рекомендуется изоляция.

ApprovalStatus: AWAITING_ADMIN_APPROVAL / DECISION_REQUIRED.

## CF-04: D-04 — SEMANTIC_CONFLICT

ExistingRule / Conflict: Absolute и incremental имеют разный basis; прежняя ссылка на baseline не доказывает lineage.

SourceAndApprovalEvidence: Docs/04; Docs/24; Docs/27; Docs/31; историческая подпись APPROVAL_UNPROVEN.

ProposedRule: Рабочий gate использует AbsoluteFarLoss=max(0,-CloseNowNet); incremental=max(0,Absolute-baselineAbsolute) только diagnostic при совпадающем полном basis и свежем baseline.

ProductionBehavior: см. DefectID в NEXT_STAGE_02B_R0E_PRODUCTION_REMEDIATION_PLAN_RU.md; Python не меняет MQL5.

MathematicalCounterexample: Absolute50 baseline40 →incremental10; Reserve30 покрывает10, но не50.

RecommendedDecision: ABSOLUTE либо independently reconciled incremental с отдельной моделью; рекомендуется ABSOLUTE.

ApprovalStatus: AWAITING_ADMIN_APPROVAL / DECISION_REQUIRED.

## CF-05: D-05 — SEMANTIC_CONFLICT

ExistingRule / Conflict: Projected loss не подтверждает actual partial executions.

SourceAndApprovalEvidence: Docs/24; Docs/27; Docs/30; историческая подпись APPROVAL_UNPROVEN.

ProposedRule: ProjectedTransitionRisk отдельно; ActualTransitionLoss=max(0,-Σunique confirmed net). PENDING/CONFIRMED/OVER_CAP/CONFLICT/UNAVAILABLE. Cap применяется и к неполному batch.

ProductionBehavior: см. DefectID в NEXT_STAGE_02B_R0E_PRODUCTION_REMEDIATION_PLAN_RU.md; Python не меняет MQL5.

MathematicalCounterexample: Projected10; fills -5 и -10; cap12 →OVER_CAP15.

RecommendedDecision: Плановый допуск без settlement контроля либо повторная actual reconciliation; рекомендуется второе.

ApprovalStatus: AWAITING_ADMIN_APPROVAL / DECISION_REQUIRED.

## CF-06: D-06 — SEMANTIC_CONFLICT

ExistingRule / Conflict: Имена safety buffers не доказывают независимость стоимостей; unknown overlap нельзя считать safe.

SourceAndApprovalEvidence: Docs/24; Docs/27; Docs/30; историческая подпись APPROVAL_UNPROVEN.

ProposedRule: Каждая стоимость имеет CostID, Source, RiskBasis, Window, Currency, Amount, AlreadyIncluded, AdditionalDeduction, PolicyVersion, Evidence. Уже включённая стоимость не вычитается повторно; unknown overlap UNPROVEN.

ProductionBehavior: см. DefectID в NEXT_STAGE_02B_R0E_PRODUCTION_REMEDIATION_PLAN_RU.md; Python не меняет MQL5.

MathematicalCounterexample: Deal Profit10, Commission-2 →Net8. Ещё раз вычесть2 →6, неверная двойная стоимость.

RecommendedDecision: Общий buffer без basis либо отдельная cost coverage registry; рекомендуется registry с неизменным basis.

ApprovalStatus: AWAITING_ADMIN_APPROVAL / DECISION_REQUIRED.

## CF-07: D-07 — SEMANTIC_CONFLICT

ExistingRule / Conflict: Boolean отсутствия prior consumption и память процесса не доказывают exactly-once; duplicate reject в production не типизированный NO_OP.

SourceAndApprovalEvidence: Docs/08; Docs/16; Docs/32; историческая подпись APPROVAL_UNPROVEN.

ProposedRule: Eligibility →owner reservation →durable commit →confirmation →recovery. Exact confirmed payload NO_OP с zero deltas; changed payload CONFLICT. Source cap учитывает immutable grants один раз.

ProductionBehavior: см. DefectID в NEXT_STAGE_02B_R0E_PRODUCTION_REMEDIATION_PLAN_RU.md; Python не меняет MQL5.

MathematicalCounterexample: Source50, A50, B50 с другими event/allocation →второй funding отклонён. После C10 exact replay оставляет C10.

RecommendedDecision: In-memory demo либо durable journal/CAS/provider protocol; production разрешён только после доказательства второго.

ApprovalStatus: AWAITING_ADMIN_APPROVAL / DECISION_REQUIRED.

## CF-08: D-08 — SEMANTIC_CONFLICT

ExistingRule / Conflict: NewFar копирует предъявленную identity в expected; nonzero DealID не доказывает сделку.

SourceAndApprovalEvidence: Docs/24; Docs/31; Docs/32; историческая подпись APPROVAL_UNPROVEN.

ProposedRule: Broker/Server/Account/Symbol/Magic/Cycle/Position/Deal/Order/Event/Role — immutable source context; Plan/Revision/Snapshot — независимый текущий context; PolicyVersion/allocation event из authoritative allocation. Expected не создаётся из proof.

ProductionBehavior: см. DefectID в NEXT_STAGE_02B_R0E_PRODUCTION_REMEDIATION_PLAN_RU.md; Python не меняет MQL5.

MathematicalCounterexample: SourcePlan1 и ConsumptionPlan10 допустимы при независимом context; presentedMagic999 при sourceMagic7 отвергается.

RecommendedDecision: Независимый provider либо self-consistency; рекомендуется provider с reconciliation.

ApprovalStatus: AWAITING_ADMIN_APPROVAL / DECISION_REQUIRED.

## CF-09: CR-09 — SEMANTIC_CONFLICT

ExistingRule / Conflict: Максимальный TransitionLoss не определяет минимальный Catch-Up margin.

SourceAndApprovalEvidence: Docs/27; Docs/30; FutureSmallProofAggregator; историческая подпись APPROVAL_UNPROVEN.

ProposedRule: ALL_LEVEL: min_i(EligibleReserve_i-AbsoluteFarLoss_i-Buffer_i)>0 при всех required gates; SINGLE_LEVEL отдельный scope. Required TransitionLoss конечен, >=0 и независимо подтверждён для обеих policies; unknown→UNAVAILABLE.

ProductionBehavior: см. DefectID в NEXT_STAGE_02B_R0E_PRODUCTION_REMEDIATION_PLAN_RU.md; Python не меняет MQL5.

MathematicalCounterexample: L1:Reserve50 Loss20 Buffer1 Transition10 →29; L2:Reserve5 Loss20 Buffer1 Transition1 →-16. MaxTransition выбирает L1; all-level должен отвергнуть.

RecommendedDecision: A all-level minimum либо B single-level maxTransition; рекомендуется A для all-level, B исключительно диагностический/явно single.

ApprovalStatus: AWAITING_ADMIN_APPROVAL / DECISION_REQUIRED.

## CF-10: NUM-EXACT-1 — ARCHITECTURE_DECISION

ExistingRule / Conflict: Fraction тестовый, не production MQL5 численный тип.

SourceAndApprovalEvidence: R0D NUM-EXACT-1; Docs/24; историческая подпись APPROVAL_UNPROVEN.

ProposedRule: Сохранить R0D exact arithmetic; settled на известной currency/grid; projected subunit loss не округлять к нулю; ROUND_HALF_EVEN лишь candidate verified policy.

ProductionBehavior: см. DefectID в NEXT_STAGE_02B_R0E_PRODUCTION_REMEDIATION_PLAN_RU.md; Python не меняет MQL5.

MathematicalCounterexample: 1e28-.010-9999999999999999999999999999.995=-.005, gate REJECT.

RecommendedDecision: Integer settled + отдельные projected types; Decimal только с доказанным domain; рекомендуется точный fixture oracle и checked MQL boundaries.

ApprovalStatus: AWAITING_ADMIN_APPROVAL / DECISION_REQUIRED.

## CF-11: NUM-DOMAIN-1 — ARCHITECTURE_DECISION

ExistingRule / Conflict: Reference domain шире MQL signed-long; currency precision неизвестна без provider.

SourceAndApprovalEvidence: R0D NUM-DOMAIN-1; историческая подпись APPROVAL_UNPROVEN.

ProposedRule: Fixture values кратны10^-64, abs<10^65; digits0..8; malformed→REJECT, supported format outside domain→UNAVAILABLE. MQL domain отдельно утверждается, без truncation.

ProductionBehavior: см. DefectID в NEXT_STAGE_02B_R0E_PRODUCTION_REMEDIATION_PLAN_RU.md; Python не меняет MQL5.

MathematicalCounterexample: 1e28 поддержан reference, но не int64 minor units; валюты USD/EUR нельзя суммировать без conversion authority.

RecommendedDecision: Расширить MQL checked representation либо ограничить домен с явным отказом; решение отдельно.

ApprovalStatus: AWAITING_ADMIN_APPROVAL / DECISION_REQUIRED.

## CF-12: NUM-CODEC — ARCHITECTURE_DECISION

ExistingRule / Conflict: Canonical fixture encoding не является broker-authentication или универсальным MQL wire format.

SourceAndApprovalEvidence: R0D NUM-CODEC; историческая подпись APPROVAL_UNPROVEN.

ProposedRule: Версионированное typed encoding; str/int/bool/number/tuple/list различаются; Decimal/Fraction одного numeric value эквивалентны. Digest не создаёт authority.

ProductionBehavior: см. DefectID в NEXT_STAGE_02B_R0E_PRODUCTION_REMEDIATION_PLAN_RU.md; Python не меняет MQL5.

MathematicalCounterexample: "1" != Decimal(1); int1 != boolTrue.

RecommendedDecision: Typed codec либо документированный ограниченный schema codec; рекомендуется сохранить fixture typed codec, production codec отдельным выбором.

ApprovalStatus: AWAITING_ADMIN_APPROVAL / DECISION_REQUIRED.

## CF-13: SNAP-FIXTURE-1 — ARCHITECTURE_DECISION

ExistingRule / Conflict: Независимый fixture receipt не доказывает broker authenticity; snapshot ID без content binding недостаточен.

SourceAndApprovalEvidence: R0D SNAP-FIXTURE-1; R0C snapshot proposal; историческая подпись APPROVAL_UNPROVEN.

ProposedRule: schema HSBI-SNAPSHOT-FIXTURE-1; id ulong; marketFingerprint nonempty opaque string; explicitNone unknown→UNAVAILABLE; missing malformed; independent content receipt; FIXTURE_MONOTONIC/tick.

ProductionBehavior: см. DefectID в NEXT_STAGE_02B_R0E_PRODUCTION_REMEDIATION_PLAN_RU.md; Python не меняет MQL5.

MathematicalCounterexample: Receipt от string"1" сохраняется до замены fingerprint на Decimal1; новый тип отвергается.

RecommendedDecision: Opaque string fixture либо новый broker schema; рекомендуется fixture только для tests, provider schema отдельно.

ApprovalStatus: AWAITING_ADMIN_APPROVAL / DECISION_REQUIRED.

## CF-14: FUNDING-GLOBAL-ATTRIBUTION — ARCHITECTURE_DECISION

ExistingRule / Conflict: Per-source cap не решает attribution иных фактических debits и конкуренцию.

SourceAndApprovalEvidence: Docs/08; Docs/16; R0D unproven boundaries; историческая подпись APPROVAL_UNPROVEN.

ProposedRule: До отдельного ledger attribution contract +50 и -20 дают economic30, но ни доказанный available50, ни автоматический debit20 произвольного bucket; availability UNPROVEN, spending UNAVAILABLE.

ProductionBehavior: см. DefectID в NEXT_STAGE_02B_R0E_PRODUCTION_REMEDIATION_PLAN_RU.md; Python не меняет MQL5.

MathematicalCounterexample: Big+50 / отдельный Small-20: source cap50 корректен, глобальная доступность неизвестна.

RecommendedDecision: Account-wide pessimistic freeze; explicit debit waterfall; role/cycle funding pool. Рекомендуется freeze до отдельного утверждения attribution.

ApprovalStatus: AWAITING_ADMIN_APPROVAL / DECISION_REQUIRED.

## CF-15: MQL-DOMAIN — ARCHITECTURE_DECISION

ExistingRule / Conflict: Нет утверждённого production представления exact projected values и scaling.

SourceAndApprovalEvidence: MQL5 signed long; NUM-DOMAIN-1; историческая подпись APPROVAL_UNPROVEN.

ProposedRule: Settled signed64 minor units с prechecked operations; max positive money LONG_MAX/10^digits; projected отдельно; unsupported range UNAVAILABLE.

ProductionBehavior: см. DefectID в NEXT_STAGE_02B_R0E_PRODUCTION_REMEDIATION_PLAN_RU.md; Python не меняет MQL5.

MathematicalCounterexample: digits2: MAX=92233720368547758.07; LONG_MIN*-1 overflow; scale LONG_MAX*100 overflow.

RecommendedDecision: int64 minor + conservative intervals либо fixed/rational representation; рекомендуется сначала narrow settled domain, projected архитектура отдельно.

ApprovalStatus: AWAITING_ADMIN_APPROVAL / DECISION_REQUIRED.

## CF-16: BALANCE-SCHEMA-MAPPING — MIGRATION_DECISION

ExistingRule / Conflict: Переименование Remaining не переносит reservation ownership.

SourceAndApprovalEvidence: R0D Gross; R0E Free; историческая подпись APPROVAL_UNPROVEN.

ProposedRule: Версии Gross/Free различаются; Free=Gross-Reserved лишь проверяемый view; отсутствие owner provenance запрещает расход lock.

ProductionBehavior: см. DefectID в NEXT_STAGE_02B_R0E_PRODUCTION_REMEDIATION_PLAN_RU.md; Python не меняет MQL5.

MathematicalCounterexample: Gross40 Reserved15 →Free25; без owner нельзя расходовать15.

RecommendedDecision: Read-only conversion view либо schema migration с полной evidence; рекомендуется view до утверждения migration.

ApprovalStatus: AWAITING_ADMIN_APPROVAL / DECISION_REQUIRED.

## CF-17 — PROVENANCE_ERRATUM

Два R0D отчёта содержат неправильный baseline SHA; см. отдельный errata с точными строками. Git objects и JSON evidence сохранены, публикация R0D не переписана.

## CF-18 — VERIFICATION_GAP

Исторический R0D package checker недостаточно связывает cases, context IDs, mutation source hashes и структурно пустые approval fields. Новый checker проверяет их независимо. Это дефект проверки доказательств, не новое экономическое правило. См. PACKAGE_RESULTS negative probes; исторический checker сохранён.
