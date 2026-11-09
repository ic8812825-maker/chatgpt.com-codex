# 02B-R0E — кандидат согласованных денежных контрактов

BASE_SHA=2d34c3378edc5f2df064282fa067bb4af2a1e3b0

Статус: PROPOSED / AWAITING_ADMIN_APPROVAL. Только audit/test-only; никаких production-изменений и торговли.

## Нормативная иерархия

Приоритет имеет текущее явное задание. Первичные Docs/04,08,16,24,27,30,31,32 объявляют спецификационные правила; наличие текста «source of truth» само по себе не доказывает подпись администратора. Доказательства административного утверждения новых D-01–D-08/CR-09/NUM/SNAP не найдены: APPROVAL_UNPROVEN для исторической подписи, AWAITING_ADMIN_APPROVAL для предложений. Исторические HSB.1V/HSB.2E статусы не разрешают новый dispatch.

Исторически утверждённое решение имеет силу только в своём scope и при проверяемой evidence утверждения. R0A–R0D — proposed review/reference packages, а не замена экономики. Production поведение описывает реализацию и возможные дефекты. Reference PASS доказывает ограниченный fixture contract. Ни то ни другое не выбирает норматив автоматически. При несовместимости — DECISION_REQUIRED.

## Доказательство D-01

Пусть G — immutable grant, C — consumed, V — owned reservation, F — free. Разбиение непересекающихся прав даёт G=C+V+F. Вводя Gross=V+F, получаем G=C+Gross и Available=Gross-V=F. Это эквивалентные представления, а не два независимых источника средств. Численный контроль: G50 C10 V15 Gross40 Free25. Трёхкомпонентная сумма с Gross равна65 и отвергается.

Consumption free переносит x из F в C; reservation переносит x из F в V; release — из V в F; consumption своего lock — из V в C. Каждая операция сохраняет G. Preconditions: x>0, достаточный собственный ресурс, одна валюта/grid, подтверждённый source, independent identity, complete journal, current revision. ResidualHeld и Unallocated не расходуемые buckets.

ActualDealNetRaw=Profit+Swap+Commission+Fee с исходными знаками. PostedActualDealNet — независимо переданный broker-posted факт, не результат локальной модели округления. EligiblePositiveNet=max(0,PostedActualDealNet) для разрешённой роли; отрицательная сделка сохраняется как debit и не порождает положительный grant. Нулевой источник имеет нулевой cap. Полное allocation положительного источника: ΣOriginalGrant=EligiblePositiveNet. PREPARED: ΣOriginalGrant+Unallocated=EligiblePositiveNet, расход запрещён. Доли округляются вниз в minor units, остаток явно ResidualHeld, сумма сохраняется точно. ResidualHeld — allocated nonspendable grant, не Unallocated.

## Типы и разрешённые преобразования

Все денежные DTO содержат currency, известные digits/grid, origin identity, schema/policy version; projected дополнительно snapshot и calculation basis. ProjectedBasketNet — прогноз корзины, provider planning evaluator. ProjectedCloseNowNet — прогноз закрытия по независимым котировкам/costs. ActualRealizedDealNet — подписанные компоненты подтверждённого deal, provider broker history. ReconciledEconomicNet — history+posted receipt+reconciliation. AllocationGrant — immutable allocation event по eligible reconciled source. AvailableReserve — проверенный Free разрешённого committed bucket, independent ledger/context/journal. Неявных преобразований нет.

Переход projection→actual запрещён. Broker history→Actual→Reconciled требует независимой сверки. Reconciled→Grant требует policy/source-cap. Grant→Available требует balance/ownership/reservations/replay/current context. Полная independently verified history без closing sources даёт known0; неполная/недоступная —UNAVAILABLE и запрет spending. Отдельные отрицательные debits требуют global attribution, поэтому source cap не равен account cash proof.

## Independent authority и replay

SourceKey=(Broker,Server,Account,Deal), изменение Magic/Cycle не создаёт новый deal budget. Source identity сохраняет Symbol/Magic/Cycle/Position/Order/Event/Role. Current Plan/Revision/Snapshot независимо поставляются evaluation context; historical SourcePlan не обязан равняться current plan. AllocationEvent и policy получаются из authoritative allocation. Request/proof не являются provider.

Exact confirmed replay допустим после shape/namespace/complete independent journal lookup и проверки payload digest; текущие spending gates не применяются повторно к уже совершённому событию. Но недоступная/неполная history/journal в этом fixture профиле даёт UNAVAILABLE и для replay: отсутствие prior=false не доказательство. Изменённый payload —CONFLICT. Новое событие требует current revision/policy/snapshot и доступного Free/owned lock. NO_OP/CONFLICT/REJECT/UNAVAILABLE не меняют balances, journal и revision. COMMITTED_IN_MEMORY — статус reference, не durable commit. ELIGIBLE_FOR_COMMIT — разрешение протокола, не trading permission.

## CR-09 и последовательная траектория

ALL_LEVEL оценивает точный min(EligibleReserve-AbsoluteFarLoss-SafetyBuffer) по полному RequiredLevels; minimum строго>0. Каждый уровень обязан иметь independently confirmed money/margin/risk/exposure/transition gates и свежие source/snapshot. Fixture complete — лишь внешняя attestation этих gates, не реализация broker proof. Missing/duplicate/stale levels →UNPROVEN; unknown transitionLoss →UNAVAILABLE; finite nonnegative TransitionLoss обязателен для A и B, у A для transition gate, у B также для selection. B выбирает maxTransitionLoss и возвращает SINGLE_LEVEL_POSITIVE, никогда ALL_LEVEL_POSITIVE.

Контрпример L1=(50,20,1,T10) margin29 и L2=(5,20,1,T1) margin-16: max T и min margin различны. Independent all-level snapshots являются альтернативными контрольными состояниями, а sequential путь расходует один остаток: 50→20 после30, второй30 отклонён; partial prefix явно сохранён, не успешная вся траектория.

## Неутверждённые решения

### D-01

Источник: Docs/08; Docs/32; R0D NUM-BALANCE.

Предложение: G=C+V+F; Gross=V+F; Available=F; COMMITTED ΣGrants=EligibleNet, PREPARED ΣGrants+Unallocated=EligibleNet и расход запрещён.

Контрпример: G50,C10,V15,Gross40,F25: 50=10+40=10+15+25, но 10+15+40=65.

Альтернативы и рекомендация: Сохранить Gross с отдельным Available либо перейти на Free. Рекомендуется явно версионированный Free-профиль, математический Gross-view для старых данных.

Migration: Миграция только при доказанной старой схеме, currency/grid и владельцах locks; неизвестные владельцы → quarantine/UNAVAILABLE.

Статус: AWAITING_ADMIN_APPROVAL; несовместимость до решения — DECISION_REQUIRED.

### D-02

Источник: Docs/04; Docs/08; Docs/31.

Предложение: Раздельные ProjectedBasketNet/ProjectedCloseNowNet/ActualRealizedDealNet/ReconciledEconomicNet/AllocationGrant/AvailableReserve. Только независимая reconciliation открывает путь к grant. Полная пустая history → известный0; неполная →UNAVAILABLE.

Контрпример: Projected100 и нет eligible закрытий →0; history отсутствует →UNAVAILABLE, а не доказанный0.

Альтернативы и рекомендация: Прогноз использовать для planning либо смешивать с actual; рекомендуется первый вариант с типизированными переходами.

Migration: Старый projected grant нельзя автоматически признать подтверждённым.

Статус: AWAITING_ADMIN_APPROVAL; несовместимость до решения — DECISION_REQUIRED.

### D-03

Источник: Docs/04; Docs/24; Docs/32.

Предложение: BigCore/BigTrend close sources после reconciliation и policy allocation; Small positive только ResidualHeld; opening costs в economic ledger без harvest grant; role/policy immutable.

Контрпример: Core0 Trend0 Small10 →BigReserve0, ResidualHeld10.

Альтернативы и рекомендация: Оставить раздельный Small residual либо разрешить трансфер отдельным будущим решением; рекомендуется изоляция.

Migration: Старые grants с неподтверждённой ролью блокируются, не переименовываются.

Статус: AWAITING_ADMIN_APPROVAL; несовместимость до решения — DECISION_REQUIRED.

### D-04

Источник: Docs/04; Docs/24; Docs/27; Docs/31.

Предложение: Рабочий gate использует AbsoluteFarLoss=max(0,-CloseNowNet); incremental=max(0,Absolute-baselineAbsolute) только diagnostic при совпадающем полном basis и свежем baseline.

Контрпример: Absolute50 baseline40 →incremental10; Reserve30 покрывает10, но не50.

Альтернативы и рекомендация: ABSOLUTE либо independently reconciled incremental с отдельной моделью; рекомендуется ABSOLUTE.

Migration: При partial close/volume/cycle/plan/revision change либо restart без basis lineage incremental UNAVAILABLE.

Статус: AWAITING_ADMIN_APPROVAL; несовместимость до решения — DECISION_REQUIRED.

### D-05

Источник: Docs/24; Docs/27; Docs/30.

Предложение: ProjectedTransitionRisk отдельно; ActualTransitionLoss=max(0,-Σunique confirmed net). PENDING/CONFIRMED/OVER_CAP/CONFLICT/UNAVAILABLE. Cap применяется и к неполному batch.

Контрпример: Projected10; fills -5 и -10; cap12 →OVER_CAP15.

Альтернативы и рекомендация: Плановый допуск без settlement контроля либо повторная actual reconciliation; рекомендуется второе.

Migration: Старые pending batches требуют order/position/deal/volume reconciliation, не признаются complete по флагу.

Статус: AWAITING_ADMIN_APPROVAL; несовместимость до решения — DECISION_REQUIRED.

### D-06

Источник: Docs/24; Docs/27; Docs/30.

Предложение: Каждая стоимость имеет CostID, Source, RiskBasis, Window, Currency, Amount, AlreadyIncluded, AdditionalDeduction, PolicyVersion, Evidence. Уже включённая стоимость не вычитается повторно; unknown overlap UNPROVEN.

Контрпример: Deal Profit10, Commission-2 →Net8. Ещё раз вычесть2 →6, неверная двойная стоимость.

Альтернативы и рекомендация: Общий buffer без basis либо отдельная cost coverage registry; рекомендуется registry с неизменным basis.

Migration: Непроверенные старые buffer assignments сохраняются как unknown, не обнуляются.

Статус: AWAITING_ADMIN_APPROVAL; несовместимость до решения — DECISION_REQUIRED.

### D-07

Источник: Docs/08; Docs/16; Docs/32.

Предложение: Eligibility →owner reservation →durable commit →confirmation →recovery. Exact confirmed payload NO_OP с zero deltas; changed payload CONFLICT. Source cap учитывает immutable grants один раз.

Контрпример: Source50, A50, B50 с другими event/allocation →второй funding отклонён. После C10 exact replay оставляет C10.

Альтернативы и рекомендация: In-memory demo либо durable journal/CAS/provider protocol; production разрешён только после доказательства второго.

Migration: При отсутствии complete journal/history UNAVAILABLE; history replay не восстанавливает потраченные деньги.

Статус: AWAITING_ADMIN_APPROVAL; несовместимость до решения — DECISION_REQUIRED.

### D-08

Источник: Docs/24; Docs/31; Docs/32.

Предложение: Broker/Server/Account/Symbol/Magic/Cycle/Position/Deal/Order/Event/Role — immutable source context; Plan/Revision/Snapshot — независимый текущий context; PolicyVersion/allocation event из authoritative allocation. Expected не создаётся из proof.

Контрпример: SourcePlan1 и ConsumptionPlan10 допустимы при независимом context; presentedMagic999 при sourceMagic7 отвергается.

Альтернативы и рекомендация: Независимый provider либо self-consistency; рекомендуется provider с reconciliation.

Migration: Account namespace обязателен; старые ключи без namespace не получают фиктивный AccountLogin.

Статус: AWAITING_ADMIN_APPROVAL; несовместимость до решения — DECISION_REQUIRED.

### CR-09

Источник: Docs/27; Docs/30; FutureSmallProofAggregator.

Предложение: ALL_LEVEL: min_i(EligibleReserve_i-AbsoluteFarLoss_i-Buffer_i)>0 при всех required gates; SINGLE_LEVEL отдельный scope. Required TransitionLoss конечен, >=0 и независимо подтверждён для обеих policies; unknown→UNAVAILABLE.

Контрпример: L1:Reserve50 Loss20 Buffer1 Transition10 →29; L2:Reserve5 Loss20 Buffer1 Transition1 →-16. MaxTransition выбирает L1; all-level должен отвергнуть.

Альтернативы и рекомендация: A all-level minimum либо B single-level maxTransition; рекомендуется A для all-level, B исключительно диагностический/явно single.

Migration: Старый selected-level proof нельзя повышать до all-level. Sequential proof использует остаток предыдущего шага.

Статус: AWAITING_ADMIN_APPROVAL; несовместимость до решения — DECISION_REQUIRED.

### NUM-EXACT-1

Источник: R0D NUM-EXACT-1; Docs/24.

Предложение: Сохранить R0D exact arithmetic; settled на известной currency/grid; projected subunit loss не округлять к нулю; ROUND_HALF_EVEN лишь candidate verified policy.

Контрпример: 1e28-.010-9999999999999999999999999999.995=-.005, gate REJECT.

Альтернативы и рекомендация: Integer settled + отдельные projected types; Decimal только с доказанным domain; рекомендуется точный fixture oracle и checked MQL boundaries.

Migration: Broker-posted values независимы от локального rounding.

Статус: AWAITING_ADMIN_APPROVAL; несовместимость до решения — DECISION_REQUIRED.

### NUM-DOMAIN-1

Источник: R0D NUM-DOMAIN-1.

Предложение: Fixture values кратны10^-64, abs<10^65; digits0..8; malformed→REJECT, supported format outside domain→UNAVAILABLE. MQL domain отдельно утверждается, без truncation.

Контрпример: 1e28 поддержан reference, но не int64 minor units; валюты USD/EUR нельзя суммировать без conversion authority.

Альтернативы и рекомендация: Расширить MQL checked representation либо ограничить домен с явным отказом; решение отдельно.

Migration: Данные вне нового domain quarantine; переполнение не исправляется clamp.

Статус: AWAITING_ADMIN_APPROVAL; несовместимость до решения — DECISION_REQUIRED.

### NUM-CODEC

Источник: R0D NUM-CODEC.

Предложение: Версионированное typed encoding; str/int/bool/number/tuple/list различаются; Decimal/Fraction одного numeric value эквивалентны. Digest не создаёт authority.

Контрпример: "1" != Decimal(1); int1 != boolTrue.

Альтернативы и рекомендация: Typed codec либо документированный ограниченный schema codec; рекомендуется сохранить fixture typed codec, production codec отдельным выбором.

Migration: Нельзя принимать старые digest как новые без schema version.

Статус: AWAITING_ADMIN_APPROVAL; несовместимость до решения — DECISION_REQUIRED.

### SNAP-FIXTURE-1

Источник: R0D SNAP-FIXTURE-1; R0C snapshot proposal.

Предложение: schema HSBI-SNAPSHOT-FIXTURE-1; id ulong; marketFingerprint nonempty opaque string; explicitNone unknown→UNAVAILABLE; missing malformed; independent content receipt; FIXTURE_MONOTONIC/tick.

Контрпример: Receipt от string"1" сохраняется до замены fingerprint на Decimal1; новый тип отвергается.

Альтернативы и рекомендация: Opaque string fixture либо новый broker schema; рекомендуется fixture только для tests, provider schema отдельно.

Migration: Неизвестная schema/version не принимается по умолчанию.

Статус: AWAITING_ADMIN_APPROVAL; несовместимость до решения — DECISION_REQUIRED.

### FUNDING-GLOBAL-ATTRIBUTION

Источник: Docs/08; Docs/16; R0D unproven boundaries.

Предложение: До отдельного ledger attribution contract +50 и -20 дают economic30, но ни доказанный available50, ни автоматический debit20 произвольного bucket; availability UNPROVEN, spending UNAVAILABLE.

Контрпример: Big+50 / отдельный Small-20: source cap50 корректен, глобальная доступность неизвестна.

Альтернативы и рекомендация: Account-wide pessimistic freeze; explicit debit waterfall; role/cycle funding pool. Рекомендуется freeze до отдельного утверждения attribution.

Migration: Нужно reconciliation всей выбранной funding domain, opening costs и historical consumed, не только positive grants.

Статус: AWAITING_ADMIN_APPROVAL; несовместимость до решения — DECISION_REQUIRED.

### MQL-DOMAIN

Источник: MQL5 signed long; NUM-DOMAIN-1.

Предложение: Settled signed64 minor units с prechecked operations; max positive money LONG_MAX/10^digits; projected отдельно; unsupported range UNAVAILABLE.

Контрпример: digits2: MAX=92233720368547758.07; LONG_MIN*-1 overflow; scale LONG_MAX*100 overflow.

Альтернативы и рекомендация: int64 minor + conservative intervals либо fixed/rational representation; рекомендуется сначала narrow settled domain, projected архитектура отдельно.

Migration: Диапазон уже fixture; импорт broker double требует независимой сверки conversion.

Статус: AWAITING_ADMIN_APPROVAL; несовместимость до решения — DECISION_REQUIRED.

### BALANCE-SCHEMA-MAPPING

Источник: R0D Gross; R0E Free.

Предложение: Версии Gross/Free различаются; Free=Gross-Reserved лишь проверяемый view; отсутствие owner provenance запрещает расход lock.

Контрпример: Gross40 Reserved15 →Free25; без owner нельзя расходовать15.

Альтернативы и рекомендация: Read-only conversion view либо schema migration с полной evidence; рекомендуется view до утверждения migration.

Migration: Никакой автоматической миграции сейчас; shadow comparison, durable backup и rollback plan обязательны.

Статус: AWAITING_ADMIN_APPROVAL; несовместимость до решения — DECISION_REQUIRED.

## D-06 — матрица покрытия расходов (PROPOSED fixture USD, policy1)

Amount сохраняет знаки реальных компонентов; positive risk buffers не являются actual deal costs. Числа ниже — иллюстративные fixture значения, не broker evidence.

| CostID | Source | RiskBasis | Window | Currency | Amount | AlreadyIncluded | AdditionalDeduction | PolicyVersion | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| SPREAD | CloseNow Bid/Ask provider | price-side spread | snapshot close-now | USD | 0.20 embedded | Да, если price provider именно closing side | Нет при включённой цене | 1 proposed | close_side fixture; broker valuation NOT_RUN |
| COMMISSION | Reconciled deal | signed commission | deal11 | USD | -2 signed | Да, в ActualNet | Нет | 1 proposed | D06-once/D06-double-cost; real receipt UNPROVEN |
| SWAP | Reconciled deal | signed swap | deal11 holding interval | USD | -0.30 signed | Да, в ActualNet | Нет | 1 proposed | Docs24; broker receipt UNPROVEN |
| FEE | Reconciled deal | signed fee | deal11 | USD | -0.10 signed | Да, в ActualNet | Нет | 1 proposed | signed raw sum; broker receipt UNPROVEN |
| SLIPPAGE_ACTUAL | Broker fill price | actual execution price difference | completed fill | USD | 0.10 embedded | Да, если included in actual price | Нет | 1 proposed | partial-fill fixture не доказывает реальную цену |
| EXECUTION_BUFFER | Risk policy provider | future execution uncertainty | pending intent execution | USD | 0.50 nonnegative risk | Нет | Только при independently known coverage | 1 proposed | D06 unknown overlap→UNPROVEN |
| CATCHUP_BUFFER | Risk policy provider | required Catch-Up safety | future control level | USD | 1.00 nonnegative risk | Неизвестно относительно execution buffer | Не назначать до overlap decision | 1 proposed | D06-unknown-overlap→UNPROVEN |

AlreadyIncluded определяется независимым расчётным basis, не названием. Future slippage risk может быть отдельным от actual slippage лишь при непересекающемся window/basis; неопределённое пересечение EXECUTION/CATCHUP →UNPROVEN/CONFLICT, не PASS. При смене provider/policy старый coverage receipt не переносится автоматически. Реализация costs_status проверяет fixture coverage registry; не рассчитывает цены, swaps или broker commission.

Точные функции/строки reference и literal expected: Tests/Contracts/NEXT_STAGE_02B_R0E_REQUIREMENT_MATRIX.json, cases. Production evidence отдельно в remediation plan; MQL5 runtime/broker/durable/CAS/NewFar — NOT_RUN/UNPROVEN.

## Граница композиции R0E

Registry fund/operate/recover — самостоятельная математическая модель funding, ownership и replay с независимой history fixture. operate не является полной production authorization: в её API нет полного proof DTO/market snapshot receipt/Plan, и она не вызывает verify_identity автоматически. verify_identity проверяется отдельным набором, R0D authorize — отдельными frozen регрессиями. Полная цепочка ProofVerification→live ConsumptionEligibility→durable commit и NewFar integration остаётся UNPROVEN; нельзя выдавать локальное COMMITTED_IN_MEMORY за прохождение этой цепочки. Нормативные preconditions независимой identity/snapshot обязательны для будущей production композиции и требуют отдельного интеграционного evidence.
