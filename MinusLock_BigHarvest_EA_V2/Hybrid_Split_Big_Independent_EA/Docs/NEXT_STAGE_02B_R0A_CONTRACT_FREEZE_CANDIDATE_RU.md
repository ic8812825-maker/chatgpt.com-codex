# 02B-R0A — кандидат фиксации денежных контрактов

Проверенная база: `cb5e55cb38aa4f2eb5b58e5218462c6738f3097a`, ветка `work`, UTC проверки `2026-11-04T01:18:36Z`. Режим `NORMATIVE_FREEZE_PREPARATION / AUDIT_AND_TEST_ONLY`. Все новые экономические формулировки — **PROPOSED**, не утверждённый production-норматив. `STAGE_02B_R1_IMPLEMENTATION_ALLOWED=NO`.

## Статус пакета

`CONTRACT_FREEZE_CANDIDATE=READY` означает полноту предложения для рассмотрения; `EFFECTIVE_NORMATIVE_FREEZE=NO`. Область утверждения — кандидат `R0A-CANDIDATE-1` и перечисленные policy/schema choices. Исторические документы не изменяются. При выборе альтернативы администратор должен указать точный текст/версию и повторить затронутые проверки до реализации.

## D-01. Allocation conservation

**Точный текст кандидата:** ActualDealNetRaw=Profit+Swap+Commission+Fee с исходными знаками и без повторного вычитания costs. PostedActualDealNet — одно преобразование суммы к известной валютной точности по явно утверждённой PrecisionPolicy. AllocatableActualDealNet=max(0,PostedActualDealNet) только для подтверждённого reconciled eligible closing source. Отрицательный/нулевой net даёт zero grant, сохраняя signed economic result. Для COMMITTED: Σ OriginalBucketGrant=AllocatableActualDealNet, Unallocated=0; для PREPARED: Σ Grant+Unallocated=AllocatableActualDealNet, расход запрещён. Для каждого bucket Remaining+Consumed=Grant, 0<=Reserved<=Remaining, Available=Remaining-Reserved. Consumed не является источником. Все суммы конечны, одной валюты и precision. Candidate PrecisionPolicy R0A-MONEY-1: decimal minor units, ROUND_HALF_EVEN один раз после суммы raw components; первые четыре shares округляются вниз, весь остаток — ResidualHeld. Policy должна быть утверждена и сверена с broker posting; несовпадение/неизвестная точность => UNAVAILABLE. ResidualHeld входит в сохранение денег, но не доступен потребителю; это не промежуточный Unallocated. Replay immutable grant сравнивает весь per-bucket vector, source, policy и schema. Balance меняется только отдельным consumption/reservation/release event.

**Примеры:** Net100, grants60 и Unallocated40 допустимы только PREPARED; COMMITTED требует ResidualHeld40. Grant50, consumed10 => remaining40, не 60. Net .01 и две shares .5 дают ResidualHeld .01. Raw1.005 => posted1.00, raw1.015 =>1.02 по candidate half-even.

**Решение администратора:** отсутствует.

## D-02. Денежные типы и преобразования

**Точный текст кандидата:** Ввести ProjectedBasketNet, ProjectedCloseNowNet, ActualRealizedDealNet, ReconciledEconomicNet, AllocationGrant, AvailableReserve. Все имеют amount/currency/precision/schema и provenance reference; projected имеют market/cost/position snapshots, actual — confirmed history source, reconciled — independent reconciliation receipt, grant — committed allocation, available — текущий balance revision. ProjectedBasketNet/ProjectedCloseNowNet никогда не конвертируются напрямую в actual/grant/available. Источником actual является независимо прочитанное экономическое событие broker history; opening commissions/fees учитываются в economic result один раз, но harvest conversion требует eligible closing deal; actual→reconciled требует сравнения signed components и ownership; reconciled→grant — утверждённой role/allocation policy; grant→available — проверенного остатка с reservations. ProjectedCatchUpMargin — только прогнозная проверка, не authorization. AuthorizedCatchUpMargin использует подтверждённый AvailableReserve и выбранную D-04 loss metric. Ни один planning PASS не создаёт settled ресурс и не означает commit.

**Примеры:** ProjectedBasketNet100, confirmed closes0 => actual0, grant0, AvailableReserve0. RecoveryPL=realized+open close-now; buckets повторно к нему не прибавляются.

**Решение администратора:** отсутствует.

## D-03. Происхождение Reserve

**Точный текст кандидата:** Разделить AggregateBasketGain, ProjectedReserveCandidate, ActualEligibleReserveSource, CommittedReserveGrant и AvailableReserve. BigCore/BigTrend могут финансировать FinalReserve только положительным actual closing DealNet после reconciliation и утверждённой allocation policy. ProjectedReserveCandidate не является доступным ресурсом. Small участвует в actual economic ledger один раз; его положительный allocatable net по рекомендуемой политике целиком направляется в non-spendable ResidualHeld с исходным SourceDealKey/Role/Event. Negative Small net уменьшает actual economic result и не создаёт отрицательный grant. Распределение Small в иные buckets требует другого явного решения и versioned migration. Opening deals и InitialProfit не являются harvest sources. До утверждения production RHS не изменяется.

**Примеры:** Core0+Trend0+Small10: AggregateBasketGain10; BigReserve contribution0; Small ResidualHeld10. Core10 даёт eligible contribution10 до policy shares. Экономические +10 Small не теряются и не прибавляются повторно.

**Решение администратора:** отсутствует.

## D-04. Absolute и incremental Far loss

**Точный текст кандидата:** AbsoluteFarLoss=max(0,-FarNetCurrent). IncrementalFarLoss=max(0,AbsoluteFarLossCurrent-AbsoluteFarLossBaseline). Candidate GateMetric=ABSOLUTE, зафиксированная в immutable CatchUpPolicy; переключение ради PASS запрещено. FarNetCurrent — типизированный fresh close-now broker-money proof по действующей стороне BUY/Bid, SELL/Ask и согласованным costs; он не создаёт Reserve. Incremental недоступен без independently verified baseline. Baseline включает account namespace, symbol, position, direction, volume, CycleID, PlanID, origin StateRevision, snapshot/time и costPolicy; текущее состояние требует проверенной lineage. В минимальной версии новая revision/plan/cycle/side/volume/costVersion инвалидирует baseline до явной reconciliation; stale либо невосстановленный после restart baseline => incremental UNAVAILABLE. Отсутствие baseline не мешает вычислять ABSOLUTE по подтверждённому current proof; metric не выбирается fallback-эвристикой.

**Примеры:** Baseline40,current50,buffer5: Reserve20 => absolute -35, incremental +5; Reserve60 => +5/+45. Current30 при baseline40 => incremental0. Partial close меняет volume/basis: нельзя вычесть старый loss40 из нового loss20 автоматически.

**Решение администратора:** отсутствует.

## D-05. ProjectedTransitionRisk и ActualTransitionLoss

**Точный текст кандидата:** До исполнения ProjectedTransitionRisk сравнивается с плановым cap и сохраняет snapshot/cost basis. После исполнения ActualTransitionLoss=max(0,-Σunique confirmed closing deal signed net). Partial fills учитываются по уникальным account-scoped DealTicket/EventID с remainingVolume; неполный batch не становится completed. Under-cap partial => PENDING; observed actual loss>cap даже до завершения => SAFE_BLOCKED/accounting reconciliation. Unconfirmed history => UNAVAILABLE; duplicate/changed fill => CONFLICT. Slippage=разница observed и planned outcomes записывается как diagnostic delta; actual signed DealNet не уменьшается повторно на этот delta. Превышение не переписывает факт на planned10 и не разрешает новый переход/торговлю.

**Примеры:** Projected10, actual15, cap12: плановое прохождение не отменяет превышение3; diagnostics actual-planned=5. Частичный actual10 остаётся PENDING; partial15 уже SAFE_BLOCKED.

**Решение администратора:** отсутствует.

## D-06. Costs и safety buffers

**Точный текст кандидата:** Каждый cost/buffer содержит Name,Currency,Source,Purpose,CalculationStage,AlreadyIncludedInNet,MayOverlapWith,PolicyVersion,Amount,RiskBasis,Window и EvidenceDigest. Profit/Swap/Commission/Fee в actual net сохраняют signed broker значения; spread и slippage не вычитаются повторно из actual DealNet. Projected costs используют явно доказанный price/cost basis: spread, уже отражённый в open/close Bid/Ask, не повторяется как дополнительный charge. AlreadyIncludedInNet устанавливается reconciliation расчётного basis, не caller boolean. Одно покрытие RiskBasis/Window допускается ровно один раз; duplicate coverage => CONFLICT, неизвестный overlap/валюта/policy => UNAVAILABLE. Leg execution uncertainty, transition safety и Catch-Up safety складываются только при доказанной независимости рисков. До утверждения нельзя удалять существующие buffers или менять production формулу.

**Примеры:** Четыре независимых leg buffer1 + иной CatchUpRisk1 =>5. Пятый charge того же risk basis =>CONFLICT, не молча4/5. Уже включённый charge1 даёт additional deduction0.

**Решение администратора:** отсутствует.

## D-07. Replay, eligibility и commit

**Точный текст кандидата:** EventIdentity=(broker,server,AccountLogin,ConsumptionEventID) в versioned namespace. Canonical payload включает source/allocation event/policy, bucket, currency/precision, amount, consumer purpose, cycle/plan/action/revision и immutable intent. Прочитать проверенный полный journal/authority scope; затем SameEvent+SameCanonicalPayload => NO_OP с delta balances/revision/actions=0, даже если исходная revision историческая и available уже нулевой. SameEvent+different payload => CONFLICT без mutation. Для нового события проверить current owner/source/plan/cycle/revision, COMMITTED allocation, known schema/policy, finite positive amount и sufficient available: результат ELIGIBLE_FOR_COMMIT, не списание. State revision compare-and-set и journal commit выполняются атомарно отдельным commit protocol; только подтверждённый commit меняет Consumed/Remaining и revision один раз. Missing/incomplete/stale authority или registry => UNAVAILABLE. hasPriorConsumption=false не является доказательством отсутствия событий. In-memory oracle не доказывает durable commit/restart correctness.

**Примеры:** Reserve50; E1=10 =>remaining40; exact E1 =>40/revision unchanged; E1=11 =>CONFLICT; новый E2=41 =>REJECT. Новый E2=40 после CAS может исчерпать bucket; последующий новый debit отклоняется.

**Решение администратора:** отсутствует.

## D-08. Независимый economic authority

**Точный текст кандидата:** SourceDealKey canonical namespace=(SchemaVersion,BrokerIdentity,ServerIdentity,AccountLogin,DealTicket); Symbol/Magic/Cycle/Plan/Action/Position/Order/Event/Role/Direction/EntryType и signed Profit/Swap/Commission/Fee/DealNet/Volume/Price/Time — immutable связанные поля Economic Record. Один DealTicket данного account namespace нельзя повторно легализовать изменением Magic/Cycle. Подтверждение — независимое чтение history и сверка journal/positions/immutable plan mapping, не valid/actual/fillsConfirmed/runtimeConfirmed и не comment. Reserve chain: BrokerHistory→ConfirmedDeal→EconomicReconciliation→ImmutableRecord→CommittedAllocation→ExpectedIdentity→ConsumptionAuthorization→CatchUp→NewFarEligibility. ExpectedIdentity строится из authority и immutable evaluation context; submitted proof/expected не являются источником. Проверяются canonical payload/digest, account/source/role, signed amounts, policy, available и revision. Полный history без сделки =>REJECT; недоступная/неполная authority =>UNAVAILABLE и все downstream authorizations NO. Far-loss отдельная ветвь: confirmed Far origin + observed owned position + fresh broker close-now calculation; отрицательный Far loss не требует фиктивного profit allocation и не становится ресурсом. Никакого auto-resume при unknown history/schema.

**Примеры:** Deal999 отсутствует в полном history =>REJECT независимо от флагов. Тот же Deal11 у другого account/server — другой source; изменённые компоненты55-5 и60-10 при Net50 — CONFLICT.

**Решение администратора:** отсутствует.

## CR-09. WORST_CASE Catch-Up

**Точный текст кандидата:** RequiredLevels определяется immutable proof depth/планом до расчёта margin и независимо от знака результата. EligibleLevels для all-level гарантии должен покрывать RequiredLevels полностью: отсутствие/неполнота/stale source, money, cost, risk, margin, Far projection или snapshot proof => UNAVAILABLE/UNPROVEN для всей гарантии, а не исключение неудобного уровня. Каждый обязательный уровень проходит lot gate Share*Bnet>F, независимый source/available proof и согласованную loss/buffer policy. Для варианта A WorstCatchUpMargin=min_i(AvailableReserve_i-FarLossMetric_i-SafetyBuffer_i); PASS только при строгом >0 и всех прочих gates. Tie-break — минимальный levelIndex среди минимумов; все уровни/metrics/proofs/policy входят в digest. Available_i не является суммой одинаковых средств по альтернативным сценариям; для последовательного пути нужен проверенный cumulative balance evolution. Projected future gain без source/available proof не даёт authority. Вариант B оценивает immutable выбранный control level и возвращает SINGLE_LEVEL_ONLY без all-level guarantee; maximum TransitionLoss не доказывает A. Политика и её scope требуют отдельного утверждения; production selector здесь не меняется.

**Примеры:** L1:T100,Reserve50,FarLoss20,buffer1 =>+29; L2:T10,Reserve5 =>-16; A reject L2, B maxT positive L1. Эквивалентность требует дополнительных связей, например C_i=a-b*T_i, b>0. В общем случае их нет.

**Решение администратора:** отсутствует.

## Типы DTO и единственные разрешённые преобразования

Общий MoneyAtom: SchemaVersion, Kind, AmountMinorUnits/CanonicalDecimal, Currency, CurrencyDigits, PrecisionPolicyVersion, SourceReceiptDigest. Денежные bool/float cast запрещены; NaN/Infinity, неизвестная валюта/precision/version блокируются. Максимум digits=8 — кандидат test profile, не произвольное утверждение о всех счетах. Raw signed broker components хранятся без утраты точности отдельно от posted minor units. RoundingAdjustment=PostedNet-RawNet — diagnostic, не новый source/grant. Candidate half-even требует подтверждения совместимости с broker posting; иначе UNAVAILABLE, не подмена broker numbers.

| DTO | Дополнительные обязательные поля | Статус и разрешённый выход |
|---|---|---|
| ProjectedBasketNet | четыре leg proofs, Market/Cost/Volume snapshots, price basis, timestamp/validUntil | PROJECTION_ONLY; никакого debit/credit |
| ProjectedCloseNowNet | position owner/identifier/direction/volume, Bid/Ask и broker calculation receipt | PROJECTION_ONLY; применяется к projected risk/RecoveryPL, не settled funds |
| ActualRealizedDealNet | account-scoped Deal/Order/Position, EntryType, signed components/raw net, actual history receipt; harvest только closing entry | OBSERVED; только независимая reconciliation |
| ReconciledEconomicNet | immutable EconomicRecordDigest, confirmed source, plan/role mapping receipt | RECONCILED; только allocation по утверждённой policy |
| AllocationGrant | account/source/currency, AllocationID/EventID/PolicyVersion, original bucket vector и source net | PREPARED либо COMMITTED; balances отдельно |
| AvailableReserve | AllocationReference, Remaining/Consumed/Reserved, purpose, BalanceRevision, authoritative snapshot | AVAILABLE_VERIFIED только после journal/history completeness; consumption eligibility отдельно |
| ProjectedTransitionRisk | план/snapshot/cost policy, projected cap comparison | PLANNING_ONLY, не actual loss |
| ActualTransitionLoss | unique actual fills, completeness/remaining volume, actual cap comparison | PENDING / RECONCILED / SAFE_BLOCKED / CONFLICT / UNAVAILABLE |
| ConsumptionIntent | EventIdentity, canonical full payload, amount/bucket/purpose, Plan/Action/Cycle/Revision, expected allocation version | ELIGIBLE_FOR_COMMIT не означает committed |

Запрещены неявные переходы между любыми monetary kinds. Новый фактический источник возникает из independently read history, а не из преобразования projected DTO. Role/Cycle/Plan/Action привязываются проверенным journal mapping; их нельзя вывести из одного comment. Currency conversion требует отдельного verified conversion receipt и policy; умножение arbitrary FX rate запрещено. TTL/maxAge/validUntil задаются immutable policy, неизвестные сроки означают UNAVAILABLE; fresh=true от caller не заменяет это доказательство.

## Цепочка authority: обязательные стрелки

| Переход | Вход и источник доверия | Обязательная проверка | Результат / ошибка / отказ |
|---|---|---|---|
| BrokerHistory → ConfirmedDeal | независимый account-scoped terminal history read с range/completeness receipt | Broker/Server/Login, DealTicket, Order/Position, existence, entry/time | FOUND_CONFIRMED; полный history без сделки REJECT; unavailable/truncated history UNAVAILABLE |
| ConfirmedDeal → EconomicReconciliation | signed broker fields + journal/immutable plan/observed positions | все components/net, ownership и role mapping; timestamps/clock domain сохранены | RECONCILED либо CONFLICT/REJECT; никаких исправлений факта из caller DTO |
| Reconciliation → ImmutableRecord | verified source receipt | canonical schema/precision, full immutable identity, account source uniqueness | RECORD_COMMITTED; изменённый existing payload CONFLICT |
| ImmutableRecord → CommittedAllocation | actual positive eligible source + approved policy | D-01 conservation, D-03 role, per-bucket immutable vector, replay event | GRANT_COMMITTED; PREPARED не расходуется; invalid REJECT, unknown policy UNAVAILABLE |
| Allocation → IndependentExpectedIdentity | source/allocation authority + immutable evaluation plan/current revision/market context | owner/source/event/policy/position/role; origin plan и consumption plan связаны journal binding | EXPECTED_READY; submitted expected игнорируется как authority; missing mapping UNAVAILABLE |
| ExpectedIdentity → ConsumptionAuthorization | submitted proof, full registry/current balance snapshot | independent equality/digest, available, replay classification, source/purpose/amount/currency/CAS | NO_OP/CONFLICT/REJECT/UNAVAILABLE/ELIGIBLE_FOR_COMMIT; eligibility read-only |
| Authorization → Catch-UpEvaluation | eligibility receipt + verified Far-loss proof, lot gate, chosen metric/buffer policy | Share×Bnet>F, positive money margin, all identities/freshness | CATCHUP_ELIGIBLE, либо отказ; не создаёт ConsumptionEvent и не меняет ledger |
| Catch-Up → NewFarEligibility | все предыдущие receipts + actual residual Core и остальные geometry/risk/margin/candidate gates | ни один источник не подменяется copied expected; snapshot/revision едины | PURE_CANDIDATE_ELIGIBLE; missing dependency BLOCKED/UNPROVEN; никакого dispatch |

Проверка источника и роли Far-loss отделена от allocation положительной прибыли Reserve: confirmed Far origin + observed position + fresh projected close-now broker calculation. Нельзя требовать allocation положительного net от убыточного Far либо прибавлять Far loss к Reserve. Полная money authorization требует обязательности всей цепочки; наличие отдельных helper функций её не доказывает.

Pure Catch-Up/NewFar calculation не является денежным расходом. Reservation и consumption — отдельные intent/journal события. После read-only eligibility другие потребители могут изменить balance: перед commit обязательны CAS/identity lock, проверка актуального receipt и подтверждённого экономического события. В R0A такой backend не реализуется. Partial success/unknown commit не угадывается; pending/reconciliation сохраняет запрет продолжения.

## Каноничность и immutable payload

Candidate canonicalization `R0A-CANDIDATE-1`: UTF-8 JSON, NFC strings, sorted unique keys, decimal plain strings с нормализацией -0 в 0, integer IDs без bool/float coercion, явные schema/units/currency/precision, без null/unknown identity. В metadata source key использовать канонический tuple/object, не неэкранированную склейку через `|`. Economic immutable fields: BrokerIdentity/ServerIdentity/AccountLogin, Symbol/Magic, Cycle/Plan/Action/Event, Deal/Order/PositionIdentifier, Role/Direction/EntryType, Volume/Price, raw Profit/Swap/Commission/Fee/Net, Timestamp/ClockDomain и reconciliation origin. Grants и balances имеют разные digests. Timestamp коррекции и broker correction events создают versioned reconciliation event, не переписывают silent duplicate. Validation flags mutable и не заменяют payload identity.

## CR-09: математическое доказательство и границы

Пусть T_i=TransitionLoss_i и C_i=R_i-F_i-B_i. Для конкретного j, выбранного argmax T, достаточность как argmin C эквивалентна проверке C_j<=C_i для всех обязательных i. Из одного неравенства T_j>=T_i это не следует: R/F/B имеют независимые источники.

Достаточное общее условие: C_i=a-bT_i, b>0, с одной policy/валютой и одинаковым tie scope. Тогда argmax T=argmin C; например R=100, B=1, F_i=T_i ⇒ C_i=99-T_i. Для полной эквивалентности порядка требуется обратный порядок C/T, включая согласование ties; просто одинаковый maximum T при разных R не определяет minimum C. Контрпример R1=50,R2=5,F1=F2=20,B=1: T1=100>T2=10, но C1=29>C2=-16.

Вариант A проверяет все required уровни, не фильтрует отрицательные/нулевые margins, missing source или lot failures. При неизвестном уровне all-level guarantee UNPROVEN. Вариант B может иметь positive single-level C1=29 при overall C2=-16 и обязан сообщать SINGLE_LEVEL_ONLY; его нельзя маркировать A. Tie-break для A — минимальный levelIndex среди минимальных margins; required set immutable и входит в digest. Суммировать один AvailableReserve по альтернативным уровням запрещено. Для sequential trajectory каждый available должен учитывать предыдущие grants/consumption/reservations; тестовые levels не доказывают реальный будущий path.

## Отдельная зависимость ZERO-CORE

Если BigCore обязателен: положительный raw Core, округлившийся ниже Vmin, отклоняет весь candidate. Пример F=.10, Rc=.01, Rt=3, Rs=.1, min=step=.01: rawCore=.001, Core=0, Trend=.30, Small=.01, NetLot=.29, slope=.19. Положительный slope не заменяет volume gate. Альтернатива поднять Core до .01 даёт NetLot=.30, slope=.20 и меняет money/margin/risk/exposure/RecoveryPL; она не разрешена автоматически. Рекомендация — reject, без ceil-normalization. RecoveryPL в money не выводится из .01 lot без broker profit/cost proof. Отдельный geometry этап; в R0A/R1.1–1.5 исправления geometry запрещены.

## Карта costs и buffers D-06

Все суммы в AccountCurrency; источник каждой строки — independent broker receipt либо утверждённая risk policy с EvidenceDigest. Одинаковые RiskBasis/Window не могут списываться повторно под разными Name. Поле MayOverlapWith означает необходимость проверки, не разрешение суммы или произвольного max().

| Name | Purpose | CalculationStage | AlreadyIncludedInNet | MayOverlapWith | PolicyVersion |
|---|---|---|---|---|---|
| spread | Bid/Ask price difference | PROJECTED_PRICE_BASIS | Если отражён open/close prices | price movement | R0A-COST-1 PROPOSED |
| commission | Брокерский signed commission | ACTUAL_COMPONENT/PROJECTED_COST | Actual signed component | execution uncertainty | R0A-COST-1 PROPOSED |
| swap | Брокерский signed overnight accrual | ACTUAL_COMPONENT/PROJECTED_COST | Actual signed component |  | R0A-COST-1 PROPOSED |
| fee | Брокерский signed fee | ACTUAL_COMPONENT/PROJECTED_COST | Actual signed component | commission | R0A-COST-1 PROPOSED |
| slippage | Execution-vs-plan price deviation | PROJECTED_BUFFER/ACTUAL_DIAGNOSTIC | Actual price already reflects slippage | price movement, execution uncertainty | R0A-COST-1 PROPOSED |
| price movement | Market movement during latency | PROJECTED_BUFFER | Только при доказанном existing coverage | spread, slippage, execution uncertainty | R0A-COST-1 PROPOSED |
| execution uncertainty | Execution residual risk | PROJECTED_LEG_BUFFER | Только при доказанном existing coverage | commission, slippage, price movement | R0A-COST-1 PROPOSED |
| transition safety | Residual transition uncertainty | TRANSITION_GATE | Не считать included без доказательства | execution uncertainty, Catch-Up safety | R0A-COST-1 PROPOSED |
| Catch-Up safety | Independent catch-up risk | CATCHUP_GATE | Не считать included без доказательства | transition safety, execution uncertainty | R0A-COST-1 PROPOSED |

Точные поля Name/Currency/Source/Purpose/CalculationStage/AlreadyIncludedInNet/MayOverlapWith/PolicyVersion присутствуют по каждой строке в machine matrix. Candidate не разрешает менять `HSBI_TryProjectedNetMoney` до утверждения и broker reconciliation.

## Связь с production исходниками (не изменены)

- [Include/Money/HSBI_EconomicLedgerTypes.mqh:9](../Include/Money/HSBI_EconomicLedgerTypes.mqh#L9) — `HSBI_SameEconomicRecord`
- [Include/Money/HSBI_EconomicLedgerTypes.mqh:10](../Include/Money/HSBI_EconomicLedgerTypes.mqh#L10) — `HSBI_ClassifyEconomicDuplicate`
- [Include/Money/HSBI_EconomicLedgerTypes.mqh:7](../Include/Money/HSBI_EconomicLedgerTypes.mqh#L7) — `HSBI_BuildSourceDealKey`
- [Include/Money/HSBI_AllocationLedgerTypes.mqh:8](../Include/Money/HSBI_AllocationLedgerTypes.mqh#L8) — `HSBI_ClassifyAllocationDuplicate`
- [Include/Money/HSBI_AllocationLedgerTypes.mqh:7](../Include/Money/HSBI_AllocationLedgerTypes.mqh#L7) — `HSBI_ValidateAllocationConservation`
- [Include/Money/HSBI_AllocationLedgerTypes.mqh:9](../Include/Money/HSBI_AllocationLedgerTypes.mqh#L9) — `HSBI_CanConsumeBucket`
- [Include/Money/HSBI_AllocationLedgerTypes.mqh:10](../Include/Money/HSBI_AllocationLedgerTypes.mqh#L10) — `HSBI_CanConsumeAmount`
- [Include/Money/HSBI_MoneyState.mqh:5](../Include/Money/HSBI_MoneyState.mqh#L5) — `HSBI_ValidateMoneyState`
- [Include/Money/HSBI_ReserveAllocationTypes.mqh:25](../Include/Money/HSBI_ReserveAllocationTypes.mqh#L25) — `HSBI_ValidateReserveConsumption`
- [Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:35](../Include/Money/HSBI_ReserveCatchUpEvaluator.mqh#L35) — `HSBI_EvaluateReserveCatchUp`
- [Include/Money/HSBI_MoneyProofIdentity.mqh:16](../Include/Money/HSBI_MoneyProofIdentity.mqh#L16) — `HSBI_IsSameMoneyProofIdentity`
- [Include/Planning/HSBI_NewFarSolver.mqh:94](../Include/Planning/HSBI_NewFarSolver.mqh#L94) — `HSBI_SolveNewFar`
- [Include/Planning/HSBI_GeometrySolver.mqh:21](../Include/Planning/HSBI_GeometrySolver.mqh#L21) — `HSBI_SolveBigGeometry`
- [Include/Money/HSBI_BasketMoneyEvaluator.mqh:11](../Include/Money/HSBI_BasketMoneyEvaluator.mqh#L11) — `HSBI_EvaluateBasketMoney`
- [Include/Planning/HSBI_FutureSmallProofAggregator.mqh:23](../Include/Planning/HSBI_FutureSmallProofAggregator.mqh#L23) — `HSBI_AggregateFutureSmallProof`
- [Include/Persistence/HSBI_PersistenceInterface.mqh:7](../Include/Persistence/HSBI_PersistenceInterface.mqh#L7) — `HSBI_PersistSnapshotStub`
