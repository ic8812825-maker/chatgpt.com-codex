# 02B-R0E — административный лист утверждения

BASE_SHA=2d34c3378edc5f2df064282fa067bb4af2a1e3b0

Статус: PROPOSED / AWAITING_ADMIN_APPROVAL. Только audit/test-only; никаких production-изменений и торговли.

Каждое решение независимо. Пустые поля не означают согласие; READY означает пригодность к рассмотрению. Ни подписи, ни даты, ни идентификатора утверждения нет.

## Contract: D-01

Recommendation: Сохранить Gross с отдельным Available либо перейти на Free. Рекомендуется явно версионированный Free-профиль, математический Gross-view для старых данных.
ExactProposedContract: G=C+V+F; Gross=V+F; Available=F; COMMITTED ΣGrants=EligibleNet, PREPARED ΣGrants+Unallocated=EligibleNet и расход запрещён.
Alternatives: Сохранить Gross с отдельным Available либо перейти на Free. Рекомендуется явно версионированный Free-профиль, математический Gross-view для старых данных.
Counterexample: G50,C10,V15,Gross40,F25: 50=10+40=10+15+25, но 10+15+40=65.
MigrationImpact: Миграция только при доказанной старой схеме, currency/grid и владельцах locks; неизвестные владельцы → quarantine/UNAVAILABLE.
UnprovenDependencies: broker authenticity/precision, global debit attribution, durable journal/CAS, MQL5 runtime, complete NewFar integration; применимость зависит от scope решения.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: D-02

Recommendation: Прогноз использовать для planning либо смешивать с actual; рекомендуется первый вариант с типизированными переходами.
ExactProposedContract: Раздельные ProjectedBasketNet/ProjectedCloseNowNet/ActualRealizedDealNet/ReconciledEconomicNet/AllocationGrant/AvailableReserve. Только независимая reconciliation открывает путь к grant. Полная пустая history → известный0; неполная →UNAVAILABLE.
Alternatives: Прогноз использовать для planning либо смешивать с actual; рекомендуется первый вариант с типизированными переходами.
Counterexample: Projected100 и нет eligible закрытий →0; history отсутствует →UNAVAILABLE, а не доказанный0.
MigrationImpact: Старый projected grant нельзя автоматически признать подтверждённым.
UnprovenDependencies: broker authenticity/precision, global debit attribution, durable journal/CAS, MQL5 runtime, complete NewFar integration; применимость зависит от scope решения.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: D-03

Recommendation: Оставить раздельный Small residual либо разрешить трансфер отдельным будущим решением; рекомендуется изоляция.
ExactProposedContract: BigCore/BigTrend close sources после reconciliation и policy allocation; Small positive только ResidualHeld; opening costs в economic ledger без harvest grant; role/policy immutable.
Alternatives: Оставить раздельный Small residual либо разрешить трансфер отдельным будущим решением; рекомендуется изоляция.
Counterexample: Core0 Trend0 Small10 →BigReserve0, ResidualHeld10.
MigrationImpact: Старые grants с неподтверждённой ролью блокируются, не переименовываются.
UnprovenDependencies: broker authenticity/precision, global debit attribution, durable journal/CAS, MQL5 runtime, complete NewFar integration; применимость зависит от scope решения.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: D-04

Recommendation: ABSOLUTE либо independently reconciled incremental с отдельной моделью; рекомендуется ABSOLUTE.
ExactProposedContract: Рабочий gate использует AbsoluteFarLoss=max(0,-CloseNowNet); incremental=max(0,Absolute-baselineAbsolute) только diagnostic при совпадающем полном basis и свежем baseline.
Alternatives: ABSOLUTE либо independently reconciled incremental с отдельной моделью; рекомендуется ABSOLUTE.
Counterexample: Absolute50 baseline40 →incremental10; Reserve30 покрывает10, но не50.
MigrationImpact: При partial close/volume/cycle/plan/revision change либо restart без basis lineage incremental UNAVAILABLE.
UnprovenDependencies: broker authenticity/precision, global debit attribution, durable journal/CAS, MQL5 runtime, complete NewFar integration; применимость зависит от scope решения.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: D-05

Recommendation: Плановый допуск без settlement контроля либо повторная actual reconciliation; рекомендуется второе.
ExactProposedContract: ProjectedTransitionRisk отдельно; ActualTransitionLoss=max(0,-Σunique confirmed net). PENDING/CONFIRMED/OVER_CAP/CONFLICT/UNAVAILABLE. Cap применяется и к неполному batch.
Alternatives: Плановый допуск без settlement контроля либо повторная actual reconciliation; рекомендуется второе.
Counterexample: Projected10; fills -5 и -10; cap12 →OVER_CAP15.
MigrationImpact: Старые pending batches требуют order/position/deal/volume reconciliation, не признаются complete по флагу.
UnprovenDependencies: broker authenticity/precision, global debit attribution, durable journal/CAS, MQL5 runtime, complete NewFar integration; применимость зависит от scope решения.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: D-06

Recommendation: Общий buffer без basis либо отдельная cost coverage registry; рекомендуется registry с неизменным basis.
ExactProposedContract: Каждая стоимость имеет CostID, Source, RiskBasis, Window, Currency, Amount, AlreadyIncluded, AdditionalDeduction, PolicyVersion, Evidence. Уже включённая стоимость не вычитается повторно; unknown overlap UNPROVEN.
Alternatives: Общий buffer без basis либо отдельная cost coverage registry; рекомендуется registry с неизменным basis.
Counterexample: Deal Profit10, Commission-2 →Net8. Ещё раз вычесть2 →6, неверная двойная стоимость.
MigrationImpact: Непроверенные старые buffer assignments сохраняются как unknown, не обнуляются.
UnprovenDependencies: broker authenticity/precision, global debit attribution, durable journal/CAS, MQL5 runtime, complete NewFar integration; применимость зависит от scope решения.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: D-07

Recommendation: In-memory demo либо durable journal/CAS/provider protocol; production разрешён только после доказательства второго.
ExactProposedContract: Eligibility →owner reservation →durable commit →confirmation →recovery. Exact confirmed payload NO_OP с zero deltas; changed payload CONFLICT. Source cap учитывает immutable grants один раз.
Alternatives: In-memory demo либо durable journal/CAS/provider protocol; production разрешён только после доказательства второго.
Counterexample: Source50, A50, B50 с другими event/allocation →второй funding отклонён. После C10 exact replay оставляет C10.
MigrationImpact: При отсутствии complete journal/history UNAVAILABLE; history replay не восстанавливает потраченные деньги.
UnprovenDependencies: broker authenticity/precision, global debit attribution, durable journal/CAS, MQL5 runtime, complete NewFar integration; применимость зависит от scope решения.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: D-08

Recommendation: Независимый provider либо self-consistency; рекомендуется provider с reconciliation.
ExactProposedContract: Broker/Server/Account/Symbol/Magic/Cycle/Position/Deal/Order/Event/Role — immutable source context; Plan/Revision/Snapshot — независимый текущий context; PolicyVersion/allocation event из authoritative allocation. Expected не создаётся из proof.
Alternatives: Независимый provider либо self-consistency; рекомендуется provider с reconciliation.
Counterexample: SourcePlan1 и ConsumptionPlan10 допустимы при независимом context; presentedMagic999 при sourceMagic7 отвергается.
MigrationImpact: Account namespace обязателен; старые ключи без namespace не получают фиктивный AccountLogin.
UnprovenDependencies: broker authenticity/precision, global debit attribution, durable journal/CAS, MQL5 runtime, complete NewFar integration; применимость зависит от scope решения.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: CR-09

Recommendation: A all-level minimum либо B single-level maxTransition; рекомендуется A для all-level, B исключительно диагностический/явно single.
ExactProposedContract: ALL_LEVEL: min_i(EligibleReserve_i-AbsoluteFarLoss_i-Buffer_i)>0 при всех required gates; SINGLE_LEVEL отдельный scope. Required TransitionLoss конечен, >=0 и независимо подтверждён для обеих policies; unknown→UNAVAILABLE.
Alternatives: A all-level minimum либо B single-level maxTransition; рекомендуется A для all-level, B исключительно диагностический/явно single.
Counterexample: L1:Reserve50 Loss20 Buffer1 Transition10 →29; L2:Reserve5 Loss20 Buffer1 Transition1 →-16. MaxTransition выбирает L1; all-level должен отвергнуть.
MigrationImpact: Старый selected-level proof нельзя повышать до all-level. Sequential proof использует остаток предыдущего шага.
UnprovenDependencies: broker authenticity/precision, global debit attribution, durable journal/CAS, MQL5 runtime, complete NewFar integration; применимость зависит от scope решения.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: NUM-EXACT-1

Recommendation: Integer settled + отдельные projected types; Decimal только с доказанным domain; рекомендуется точный fixture oracle и checked MQL boundaries.
ExactProposedContract: Сохранить R0D exact arithmetic; settled на известной currency/grid; projected subunit loss не округлять к нулю; ROUND_HALF_EVEN лишь candidate verified policy.
Alternatives: Integer settled + отдельные projected types; Decimal только с доказанным domain; рекомендуется точный fixture oracle и checked MQL boundaries.
Counterexample: 1e28-.010-9999999999999999999999999999.995=-.005, gate REJECT.
MigrationImpact: Broker-posted values независимы от локального rounding.
UnprovenDependencies: broker authenticity/precision, global debit attribution, durable journal/CAS, MQL5 runtime, complete NewFar integration; применимость зависит от scope решения.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: NUM-DOMAIN-1

Recommendation: Расширить MQL checked representation либо ограничить домен с явным отказом; решение отдельно.
ExactProposedContract: Fixture values кратны10^-64, abs<10^65; digits0..8; malformed→REJECT, supported format outside domain→UNAVAILABLE. MQL domain отдельно утверждается, без truncation.
Alternatives: Расширить MQL checked representation либо ограничить домен с явным отказом; решение отдельно.
Counterexample: 1e28 поддержан reference, но не int64 minor units; валюты USD/EUR нельзя суммировать без conversion authority.
MigrationImpact: Данные вне нового domain quarantine; переполнение не исправляется clamp.
UnprovenDependencies: broker authenticity/precision, global debit attribution, durable journal/CAS, MQL5 runtime, complete NewFar integration; применимость зависит от scope решения.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: NUM-CODEC

Recommendation: Typed codec либо документированный ограниченный schema codec; рекомендуется сохранить fixture typed codec, production codec отдельным выбором.
ExactProposedContract: Версионированное typed encoding; str/int/bool/number/tuple/list различаются; Decimal/Fraction одного numeric value эквивалентны. Digest не создаёт authority.
Alternatives: Typed codec либо документированный ограниченный schema codec; рекомендуется сохранить fixture typed codec, production codec отдельным выбором.
Counterexample: "1" != Decimal(1); int1 != boolTrue.
MigrationImpact: Нельзя принимать старые digest как новые без schema version.
UnprovenDependencies: broker authenticity/precision, global debit attribution, durable journal/CAS, MQL5 runtime, complete NewFar integration; применимость зависит от scope решения.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: SNAP-FIXTURE-1

Recommendation: Opaque string fixture либо новый broker schema; рекомендуется fixture только для tests, provider schema отдельно.
ExactProposedContract: schema HSBI-SNAPSHOT-FIXTURE-1; id ulong; marketFingerprint nonempty opaque string; explicitNone unknown→UNAVAILABLE; missing malformed; independent content receipt; FIXTURE_MONOTONIC/tick.
Alternatives: Opaque string fixture либо новый broker schema; рекомендуется fixture только для tests, provider schema отдельно.
Counterexample: Receipt от string"1" сохраняется до замены fingerprint на Decimal1; новый тип отвергается.
MigrationImpact: Неизвестная schema/version не принимается по умолчанию.
UnprovenDependencies: broker authenticity/precision, global debit attribution, durable journal/CAS, MQL5 runtime, complete NewFar integration; применимость зависит от scope решения.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: FUNDING-GLOBAL-ATTRIBUTION

Recommendation: Account-wide pessimistic freeze; explicit debit waterfall; role/cycle funding pool. Рекомендуется freeze до отдельного утверждения attribution.
ExactProposedContract: До отдельного ledger attribution contract +50 и -20 дают economic30, но ни доказанный available50, ни автоматический debit20 произвольного bucket; availability UNPROVEN, spending UNAVAILABLE.
Alternatives: Account-wide pessimistic freeze; explicit debit waterfall; role/cycle funding pool. Рекомендуется freeze до отдельного утверждения attribution.
Counterexample: Big+50 / отдельный Small-20: source cap50 корректен, глобальная доступность неизвестна.
MigrationImpact: Нужно reconciliation всей выбранной funding domain, opening costs и historical consumed, не только positive grants.
UnprovenDependencies: broker authenticity/precision, global debit attribution, durable journal/CAS, MQL5 runtime, complete NewFar integration; применимость зависит от scope решения.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: MQL-DOMAIN

Recommendation: int64 minor + conservative intervals либо fixed/rational representation; рекомендуется сначала narrow settled domain, projected архитектура отдельно.
ExactProposedContract: Settled signed64 minor units с prechecked operations; max positive money LONG_MAX/10^digits; projected отдельно; unsupported range UNAVAILABLE.
Alternatives: int64 minor + conservative intervals либо fixed/rational representation; рекомендуется сначала narrow settled domain, projected архитектура отдельно.
Counterexample: digits2: MAX=92233720368547758.07; LONG_MIN*-1 overflow; scale LONG_MAX*100 overflow.
MigrationImpact: Диапазон уже fixture; импорт broker double требует независимой сверки conversion.
UnprovenDependencies: broker authenticity/precision, global debit attribution, durable journal/CAS, MQL5 runtime, complete NewFar integration; применимость зависит от scope решения.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: BALANCE-SCHEMA-MAPPING

Recommendation: Read-only conversion view либо schema migration с полной evidence; рекомендуется view до утверждения migration.
ExactProposedContract: Версии Gross/Free различаются; Free=Gross-Reserved лишь проверяемый view; отсутствие owner provenance запрещает расход lock.
Alternatives: Read-only conversion view либо schema migration с полной evidence; рекомендуется view до утверждения migration.
Counterexample: Gross40 Reserved15 →Free25; без owner нельзя расходовать15.
MigrationImpact: Никакой автоматической миграции сейчас; shadow comparison, durable backup и rollback plan обязательны.
UnprovenDependencies: broker authenticity/precision, global debit attribution, durable journal/CAS, MQL5 runtime, complete NewFar integration; применимость зависит от scope решения.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:
