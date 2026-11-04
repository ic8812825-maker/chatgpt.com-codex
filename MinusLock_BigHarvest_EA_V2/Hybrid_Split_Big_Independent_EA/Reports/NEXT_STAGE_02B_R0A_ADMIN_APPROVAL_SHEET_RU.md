# 02B-R0A — лист утверждения администратора

Проверенная база: `cb5e55cb38aa4f2eb5b58e5218462c6738f3097a`, ветка `work`, UTC проверки `2026-11-04T01:18:36Z`. Режим `NORMATIVE_FREEZE_PREPARATION / AUDIT_AND_TEST_ONLY`. Все новые экономические формулировки — **PROPOSED**, не утверждённый production-норматив. `STAGE_02B_R1_IMPLEMENTATION_ALLOWED=NO`.

Каждое решение независимо требует явного выбора. Дата создания документа не является датой утверждения. Отсутствие заполненных полей означает отсутствие решения, включая рекомендованные варианты. Нельзя заполнять их результатами тестов.

## D-01. Allocation conservation

**DecisionID:** D-01

**Problem:** Docs/04,08 требуют equality; Docs/32 допускает <= и складывает consumed с неуточнёнными grants.

**Alternatives:** Полное committed распределение; Частичное распределение с отдельной phase/Unallocated

**RecommendedOption:** Полные immutable grants; отдельные balances; промежуточный Unallocated недоступен.

**ExactNormativeText:** ActualDealNetRaw=Profit+Swap+Commission+Fee с исходными знаками и без повторного вычитания costs. PostedActualDealNet — одно преобразование суммы к известной валютной точности по явно утверждённой PrecisionPolicy. AllocatableActualDealNet=max(0,PostedActualDealNet) только для подтверждённого reconciled eligible closing source. Отрицательный/нулевой net даёт zero grant, сохраняя signed economic result. Для COMMITTED: Σ OriginalBucketGrant=AllocatableActualDealNet, Unallocated=0; для PREPARED: Σ Grant+Unallocated=AllocatableActualDealNet, расход запрещён. Для каждого bucket Remaining+Consumed=Grant, 0<=Reserved<=Remaining, Available=Remaining-Reserved. Consumed не является источником. Все суммы конечны, одной валюты и precision. Candidate PrecisionPolicy R0A-MONEY-1: decimal minor units, ROUND_HALF_EVEN один раз после суммы raw components; первые четыре shares округляются вниз, весь остаток — ResidualHeld. Policy должна быть утверждена и сверена с broker posting; несовпадение/неизвестная точность => UNAVAILABLE. ResidualHeld входит в сохранение денег, но не доступен потребителю; это не промежуточный Unallocated. Replay immutable grant сравнивает весь per-bucket vector, source, policy и schema. Balance меняется только отдельным consumption/reservation/release event.

**MathematicalConsequences:** Net100, grants60 и Unallocated40 допустимы только PREPARED; COMMITTED требует ResidualHeld40. Grant50, consumed10 => remaining40, не 60. Net .01 и две shares .5 дают ResidualHeld .01. Raw1.005 => posted1.00, raw1.015 =>1.02 по candidate half-even.

**ProductionImpact:** HSBI_EconomicLedgerTypes, HSBI_AllocationLedgerTypes, HSBI_ReserveAllocationTypes, MoneyState; Big harvest без скрытого remainder, Small — отдельный источник, Catch-Up/NewFar не тратят ResidualHeld.

**MigrationImpact:** Новая schema: OriginalGrant/Consumed/Reserved/Remaining различаются. Старое reserveAllocated нельзя автоматически объявить original/remaining. Legacy с неизвестной полнотой => reconciliation, без spend.

**Tests:** D01-signed-net, D01-components-sum-mismatch, D01-allocatable--15, D01-allocatable-0, D01-allocatable-1.005, D01-allocatable-1.015, D01-rounding-residual, D01-valid-balance, D01-no-double-count, D01-partial-committed, D01-partial-prepared, D01-prepared-no-consume, D01-negative-available, D01-missing-bucket, FINITE-nan, FINITE-inf, FINITE-NaN, FINITE-Infinity, FINITE-True, L02-bucket-digest.

**Risks:** Нужно подтвердить precision policy на целевом broker; no global tolerance для immutable equality. Нельзя прибавить consumed к original grants.

```text
AdministratorDecision:
ApprovalStatus: AWAITING_ADMIN_APPROVAL
ApprovalDate:
ApprovalIdentifier:
```

## D-02. Денежные типы и преобразования

**DecisionID:** D-02

**Problem:** Общее recoveryMoney может смешивать прогноз и доступный ресурс.

**Alternatives:** Один double с флагами; Раздельные DTO и явные conversion gates

**RecommendedOption:** Раздельные DTO, без неявного projected→actual/available.

**ExactNormativeText:** Ввести ProjectedBasketNet, ProjectedCloseNowNet, ActualRealizedDealNet, ReconciledEconomicNet, AllocationGrant, AvailableReserve. Все имеют amount/currency/precision/schema и provenance reference; projected имеют market/cost/position snapshots, actual — confirmed history source, reconciled — independent reconciliation receipt, grant — committed allocation, available — текущий balance revision. ProjectedBasketNet/ProjectedCloseNowNet никогда не конвертируются напрямую в actual/grant/available. Источником actual является независимо прочитанное экономическое событие broker history; opening commissions/fees учитываются в economic result один раз, но harvest conversion требует eligible closing deal; actual→reconciled требует сравнения signed components и ownership; reconciled→grant — утверждённой role/allocation policy; grant→available — проверенного остатка с reservations. ProjectedCatchUpMargin — только прогнозная проверка, не authorization. AuthorizedCatchUpMargin использует подтверждённый AvailableReserve и выбранную D-04 loss metric. Ни один planning PASS не создаёт settled ресурс и не означает commit.

**MathematicalConsequences:** ProjectedBasketNet100, confirmed closes0 => actual0, grant0, AvailableReserve0. RecoveryPL=realized+open close-now; buckets повторно к нему не прибавляются.

**ProductionImpact:** Новые Money DTO/конвертеры; Basket/FutureSmall/CatchUp/NewFar assembly. Big/Small прогнозы сохраняют planning-only статус; доступность NewFar отделена от прогнозного money proof.

**MigrationImpact:** Legacy projected без source receipt остаётся projected или UNAVAILABLE; никакой миграции через actual=true.

**Tests:** D02-no-implicit-ProjectedBasketNet, D02-no-implicit-ProjectedCloseNowNet, D02-no-implicit-ActualRealizedDealNet, D02-no-implicit-AllocationGrant, D02-no-implicit-AvailableReserve, D02-history-missing, D02-no-confirmed-closes, D02-projected100-available0.

**Risks:** Прогноз будущих уровней не доказывает наличие средств сегодня. Строгая типизация должна проверяться в вызывающем слое и при десериализации.

```text
AdministratorDecision:
ApprovalStatus: AWAITING_ADMIN_APPROVAL
ApprovalDate:
ApprovalIdentifier:
```

## D-03. Происхождение Reserve

**DecisionID:** D-03

**Problem:** Aggregate Core+Trend+Small ошибочно выглядит разрешённым Big Reserve.

**Alternatives:** Small участвует в BigReserve по новому разрешению; Small отдельно в ResidualHeld; Small в отдельном утверждённом spending bucket

**RecommendedOption:** Small positive net — ResidualHeld, не BigReserve; Core/Trend только confirmed eligible источники.

**ExactNormativeText:** Разделить AggregateBasketGain, ProjectedReserveCandidate, ActualEligibleReserveSource, CommittedReserveGrant и AvailableReserve. BigCore/BigTrend могут финансировать FinalReserve только положительным actual closing DealNet после reconciliation и утверждённой allocation policy. ProjectedReserveCandidate не является доступным ресурсом. Small участвует в actual economic ledger один раз; его положительный allocatable net по рекомендуемой политике целиком направляется в non-spendable ResidualHeld с исходным SourceDealKey/Role/Event. Negative Small net уменьшает actual economic result и не создаёт отрицательный grant. Распределение Small в иные buckets требует другого явного решения и versioned migration. Opening deals и InitialProfit не являются harvest sources. До утверждения production RHS не изменяется.

**MathematicalConsequences:** Core0+Trend0+Small10: AggregateBasketGain10; BigReserve contribution0; Small ResidualHeld10. Core10 даёт eligible contribution10 до policy shares. Экономические +10 Small не теряются и не прибавляются повторно.

**ProductionImpact:** HSBI_EvaluateBasketMoney / ReserveSourceProof / CatchUp; role-aware AllocationGrant. Big и Small не меняют geometry; NewFar не использует общий basket gain как authority.

**MigrationImpact:** Исторические Small allocations не переклассифицировать без подтверждённого source/consumption history; отдельная policyVersion.

**Tests:** D03-opening-no-grant-source, D03-small-not-reserve, D03-small-not-lost, D03-role-BigCore, D03-role-BigTrend.

**Risks:** ResidualHeld блокирует расход этой прибыли до отдельного решения; это осознанное ограничение, не исчезновение денег.

```text
AdministratorDecision:
ApprovalStatus: AWAITING_ADMIN_APPROVAL
ApprovalDate:
ApprovalIdentifier:
```

## D-04. Absolute и incremental Far loss

**DecisionID:** D-04

**Problem:** Название increase не определяет baseline и может ослаблять gate.

**Alternatives:** AbsoluteFarLoss для gate; IncrementalFarLoss с независимым baseline; Оба значения раздельно, metric в immutable policy

**RecommendedOption:** Хранить оба, для рекомендуемого рабочего gate выбрать ABSOLUTE; incremental — diagnostic до отдельного разрешения.

**ExactNormativeText:** AbsoluteFarLoss=max(0,-FarNetCurrent). IncrementalFarLoss=max(0,AbsoluteFarLossCurrent-AbsoluteFarLossBaseline). Candidate GateMetric=ABSOLUTE, зафиксированная в immutable CatchUpPolicy; переключение ради PASS запрещено. FarNetCurrent — типизированный fresh close-now broker-money proof по действующей стороне BUY/Bid, SELL/Ask и согласованным costs; он не создаёт Reserve. Incremental недоступен без independently verified baseline. Baseline включает account namespace, symbol, position, direction, volume, CycleID, PlanID, origin StateRevision, snapshot/time и costPolicy; текущее состояние требует проверенной lineage. В минимальной версии новая revision/plan/cycle/side/volume/costVersion инвалидирует baseline до явной reconciliation; stale либо невосстановленный после restart baseline => incremental UNAVAILABLE. Отсутствие baseline не мешает вычислять ABSOLUTE по подтверждённому current proof; metric не выбирается fallback-эвристикой.

**MathematicalConsequences:** Baseline40,current50,buffer5: Reserve20 => absolute -35, incremental +5; Reserve60 => +5/+45. Current30 при baseline40 => incremental0. Partial close меняет volume/basis: нельзя вычесть старый loss40 из нового loss20 автоматически.

**ProductionImpact:** BasketMoney/CatchUp/NewFar proof assembly и digests. Big/Small feasibility и время Catch-Up меняются только после утверждения; geometry неизменна.

**MigrationImpact:** Сохранять lossMetric/version, baseline origin и lineage. Старый baseline не угадывать; current absolute semantics до реализации остаётся прежней.

**Tests:** D04-margins-20, D04-margins-60, D04-missing-baseline, D04-stale-baseline, D04-baseline-unneeded-absolute, D04-loss-decrease, D04-BUY-Bid-cost, D04-SELL-Ask-cost, D04-baseline-control, D04-baseline-binding-side, D04-baseline-binding-volume, D04-baseline-binding-cycle, D04-baseline-binding-plan, D04-baseline-binding-revision, D04-baseline-binding-snapshot, D04-baseline-binding-costVersion, D04-restart-not-restored, D04-partial-close-rebase.

**Risks:** ABSOLUTE консервативнее данного примера, но не является доказательством полной recovery. Broker-specific расчёты NOT_RUN.

```text
AdministratorDecision:
ApprovalStatus: AWAITING_ADMIN_APPROVAL
ApprovalDate:
ApprovalIdentifier:
```

## D-05. ProjectedTransitionRisk и ActualTransitionLoss

**DecisionID:** D-05

**Problem:** Одна семантическая область для плановой оценки и фактического accounting.

**Alternatives:** Общий DTO с тегом; Раздельные projected/actual records

**RecommendedOption:** Раздельные типы и обязательная post-fill reconciliation.

**ExactNormativeText:** До исполнения ProjectedTransitionRisk сравнивается с плановым cap и сохраняет snapshot/cost basis. После исполнения ActualTransitionLoss=max(0,-Σunique confirmed closing deal signed net). Partial fills учитываются по уникальным account-scoped DealTicket/EventID с remainingVolume; неполный batch не становится completed. Under-cap partial => PENDING; observed actual loss>cap даже до завершения => SAFE_BLOCKED/accounting reconciliation. Unconfirmed history => UNAVAILABLE; duplicate/changed fill => CONFLICT. Slippage=разница observed и planned outcomes записывается как diagnostic delta; actual signed DealNet не уменьшается повторно на этот delta. Превышение не переписывает факт на planned10 и не разрешает новый переход/торговлю.

**MathematicalConsequences:** Projected10, actual15, cap12: плановое прохождение не отменяет превышение3; diagnostics actual-planned=5. Частичный actual10 остаётся PENDING; partial15 уже SAFE_BLOCKED.

**ProductionImpact:** HSBI_EvaluateFutureSmallLevel, NewFar gates, ActualClosingDeals DTO и accounting reconciliation. Small transition сохраняет partial completeness; Big harvest не подменяет actual прогнозом.

**MigrationImpact:** Хранить planned и actual separately, уникальные fills, remaining volume и over-cap reason; legacy с неизвестной completeness => UNAVAILABLE.

**Tests:** D05-overcap, D05-slippage-diagnostic-only, D05-partial-overcap, D05-partial-under-cap, D05-complete-under-cap, D05-duplicate-fill, D05-unconfirmed-fill.

**Risks:** Здесь SAFE_BLOCKED — контракт результата accounting, не реализованный торговый FSM transition.

```text
AdministratorDecision:
ApprovalStatus: AWAITING_ADMIN_APPROVAL
ApprovalDate:
ApprovalIdentifier:
```

## D-06. Costs и safety buffers

**DecisionID:** D-06

**Problem:** Не определено пересечение per-leg и Catch-Up deductions.

**Alternatives:** Единый общий budget с распределением; Независимые бюджеты с непересекающимися risk basis

**RecommendedOption:** Charge-once по документированным riskBasis/window, отдельные независимые risk budgets; unresolved overlap блокирует proof.

**ExactNormativeText:** Каждый cost/buffer содержит Name,Currency,Source,Purpose,CalculationStage,AlreadyIncludedInNet,MayOverlapWith,PolicyVersion,Amount,RiskBasis,Window и EvidenceDigest. Profit/Swap/Commission/Fee в actual net сохраняют signed broker значения; spread и slippage не вычитаются повторно из actual DealNet. Projected costs используют явно доказанный price/cost basis: spread, уже отражённый в open/close Bid/Ask, не повторяется как дополнительный charge. AlreadyIncludedInNet устанавливается reconciliation расчётного basis, не caller boolean. Одно покрытие RiskBasis/Window допускается ровно один раз; duplicate coverage => CONFLICT, неизвестный overlap/валюта/policy => UNAVAILABLE. Leg execution uncertainty, transition safety и Catch-Up safety складываются только при доказанной независимости рисков. До утверждения нельзя удалять существующие buffers или менять production формулу.

**MathematicalConsequences:** Четыре независимых leg buffer1 + иной CatchUpRisk1 =>5. Пятый charge того же risk basis =>CONFLICT, не молча4/5. Уже включённый charge1 даёт additional deduction0.

**ProductionImpact:** HSBI_CostModel/ProjectedProfit/LevelMoney/Basket/CatchUp и proof digests; Big/Small/последующие уровни используют одинаковую policy версии.

**MigrationImpact:** Новая cost coverage schema; старые combined buffers без basis требуют независимого rebuild projected proof, не изменения actual history.

**Tests:** D06-independent-five, D06-overlap-not-silent, D06-already-in-net, D06-currency, D06-negative.

**Risks:** Неподтверждённое разбиение может недоучесть риск; кандидат не отменяет текущую production защиту.

```text
AdministratorDecision:
ApprovalStatus: AWAITING_ADMIN_APPROVAL
ApprovalDate:
ApprovalIdentifier:
```

## D-07. Replay, eligibility и commit

**DecisionID:** D-07

**Problem:** Bool prior и key без amount не доказывают exactly-once.

**Alternatives:** Typed NO_OP; REJECT с доказанным NOOP reason

**RecommendedOption:** Typed outcomes; eligibility отдельно от commit, durable registry как prerequisite.

**ExactNormativeText:** EventIdentity=(broker,server,AccountLogin,ConsumptionEventID) в versioned namespace. Canonical payload включает source/allocation event/policy, bucket, currency/precision, amount, consumer purpose, cycle/plan/action/revision и immutable intent. Прочитать проверенный полный journal/authority scope; затем SameEvent+SameCanonicalPayload => NO_OP с delta balances/revision/actions=0, даже если исходная revision историческая и available уже нулевой. SameEvent+different payload => CONFLICT без mutation. Для нового события проверить current owner/source/plan/cycle/revision, COMMITTED allocation, known schema/policy, finite positive amount и sufficient available: результат ELIGIBLE_FOR_COMMIT, не списание. State revision compare-and-set и journal commit выполняются атомарно отдельным commit protocol; только подтверждённый commit меняет Consumed/Remaining и revision один раз. Missing/incomplete/stale authority или registry => UNAVAILABLE. hasPriorConsumption=false не является доказательством отсутствия событий. In-memory oracle не доказывает durable commit/restart correctness.

**MathematicalConsequences:** Reserve50; E1=10 =>remaining40; exact E1 =>40/revision unchanged; E1=11 =>CONFLICT; новый E2=41 =>REJECT. Новый E2=40 после CAS может исчерпать bucket; последующий новый debit отклоняется.

**ProductionImpact:** HSBI_ReserveConsumptionKey/duplicate/conflict/digest, CatchUp authorization, money state/restart interfaces. Replay Big/Small/NewFar не создаёт новый grant/action.

**MigrationImpact:** Старые events без amount/bucket/policy нельзя автоматически считать exact replay. Восстановить source payload или UNAVAILABLE/manual review.

**Tests:** D07-eligible-not-commit, D07-no-mutation-on-eligibility, D07-first10, D07-exact-noop, D07-altered11, D07-next41, D07-full-consumption, D07-full-replay-noop, D07-spent-bucket-new-event, D07-missing-registry, D07-reserved-not-available, D07-binding-plan, D07-binding-revision, D07-binding-cycle, D07-binding-policy, D07-binding-allocationEvent, D07-binding-source.

**Risks:** Гонки consumers и torn journals остаются UNPROVEN до отдельной durable реализации. Не считать ELIGIBLE совершённым денежным событием.

```text
AdministratorDecision:
ApprovalStatus: AWAITING_ADMIN_APPROVAL
ApprovalDate:
ApprovalIdentifier:
```

## D-08. Независимый economic authority

**DecisionID:** D-08

**Problem:** Флаги и self-copy expected не подтверждают existence/provenance.

**Alternatives:** Доверенные caller flags; Broker history + durable journal + independent reconciliation; Test-only fixture provider без production authorization

**RecommendedOption:** История брокера плюс durable журнал и независимая reconciliation; fixture только для тестов.

**ExactNormativeText:** SourceDealKey canonical namespace=(SchemaVersion,BrokerIdentity,ServerIdentity,AccountLogin,DealTicket); Symbol/Magic/Cycle/Plan/Action/Position/Order/Event/Role/Direction/EntryType и signed Profit/Swap/Commission/Fee/DealNet/Volume/Price/Time — immutable связанные поля Economic Record. Один DealTicket данного account namespace нельзя повторно легализовать изменением Magic/Cycle. Подтверждение — независимое чтение history и сверка journal/positions/immutable plan mapping, не valid/actual/fillsConfirmed/runtimeConfirmed и не comment. Reserve chain: BrokerHistory→ConfirmedDeal→EconomicReconciliation→ImmutableRecord→CommittedAllocation→ExpectedIdentity→ConsumptionAuthorization→CatchUp→NewFarEligibility. ExpectedIdentity строится из authority и immutable evaluation context; submitted proof/expected не являются источником. Проверяются canonical payload/digest, account/source/role, signed amounts, policy, available и revision. Полный history без сделки =>REJECT; недоступная/неполная authority =>UNAVAILABLE и все downstream authorizations NO. Far-loss отдельная ветвь: confirmed Far origin + observed owned position + fresh broker close-now calculation; отрицательный Far loss не требует фиктивного profit allocation и не становится ресурсом. Никакого auto-resume при unknown history/schema.

**MathematicalConsequences:** Deal999 отсутствует в полном history =>REJECT независимо от флагов. Тот же Deal11 у другого account/server — другой source; изменённые компоненты55-5 и60-10 при Net50 — CONFLICT.

**ProductionImpact:** EconomicLedgerTypes, authoritative lookup/reconciliation DTO, HSBI_NewFarProofIdentity/assembly, ReserveSourceProof/FarLossProof, consumption boundaries. Все остальные NewFar objective/geometry gates сохраняются.

**MigrationImpact:** Legacy source без account/server/полного payload нельзя восстановить по строке Symbol|Magic|Cycle|Deal. Нужна проверяемая миграция из history, иначе блокировка.

**Tests:** D08-proof-control, D08-missing-history, D08-authority-stale, D08-authority-incomplete, D08-invented-deal, D08-namespace-broker, D08-namespace-server, D08-namespace-account, D08-self-copy-owner, D08-self-copy-symbol, D08-self-copy-magic, D08-self-copy-deal, D08-self-copy-event, D08-self-copy-position, D08-self-copy-role, D08-self-copy-direction, D08-self-copy-cycle, D08-self-copy-action, D08-self-copy-plan, D08-self-copy-revision, D08-self-copy-snapshot, D08-wrong-digest, D08-stale, D08-wrong-net, D08-context-magic, D08-context-symbol, D08-forbidden-reserve-role, D08-allocation-reused, D08-allocation-owner, L01-component-digest, L01-same-record-digest.

**Risks:** Хеш обеспечивает integrity, не внешнюю подлинность. Доверие fixture flags и полная durable correctness не доказаны.

```text
AdministratorDecision:
ApprovalStatus: AWAITING_ADMIN_APPROVAL
ApprovalDate:
ApprovalIdentifier:
```

## CR-09. WORST_CASE Catch-Up

**DecisionID:** CR-09

**Problem:** Maximum TransitionLoss не обязан совпадать с minimum Catch-Up margin.

**Alternatives:** A: все обязательные уровни; B: один выбранный уровень без all-level guarantee

**RecommendedOption:** A; B допустим только явно ограниченным альтернативным решением.

**ExactNormativeText:** RequiredLevels определяется immutable proof depth/планом до расчёта margin и независимо от знака результата. EligibleLevels для all-level гарантии должен покрывать RequiredLevels полностью: отсутствие/неполнота/stale source, money, cost, risk, margin, Far projection или snapshot proof => UNAVAILABLE/UNPROVEN для всей гарантии, а не исключение неудобного уровня. Каждый обязательный уровень проходит lot gate Share*Bnet>F, независимый source/available proof и согласованную loss/buffer policy. Для варианта A WorstCatchUpMargin=min_i(AvailableReserve_i-FarLossMetric_i-SafetyBuffer_i); PASS только при строгом >0 и всех прочих gates. Tie-break — минимальный levelIndex среди минимумов; все уровни/metrics/proofs/policy входят в digest. Available_i не является суммой одинаковых средств по альтернативным сценариям; для последовательного пути нужен проверенный cumulative balance evolution. Projected future gain без source/available proof не даёт authority. Вариант B оценивает immutable выбранный control level и возвращает SINGLE_LEVEL_ONLY без all-level guarantee; maximum TransitionLoss не доказывает A. Политика и её scope требуют отдельного утверждения; production selector здесь не меняется.

**MathematicalConsequences:** L1:T100,Reserve50,FarLoss20,buffer1 =>+29; L2:T10,Reserve5 =>-16; A reject L2, B maxT positive L1. Эквивалентность требует дополнительных связей, например C_i=a-b*T_i, b>0. В общем случае их нет.

**ProductionImpact:** Отдельный последующий этап FutureSmall aggregate selector/digest и NewFar integration; Big/Small geometry не меняется.

**MigrationImpact:** Хранить selectionPolicy/scope/version, RequiredLevels и все source proof references. Старый max-loss proof не повышать автоматически до all-level.

**Tests:** CR09-A-negative-level, CR09-B-limited-positive, CR09-zero, CR09-tie, CR09-missing-complete, CR09-missing-fresh, CR09-missing-sourceProof, CR09-no-filter-bad-level, CR09-lot-failure, CR09-equivalence-sufficient.

**Risks:** Даже all-level положительные margins не доказывают реальную исполнимость trajectory, broker fill или конечность recovery.

```text
AdministratorDecision:
ApprovalStatus: AWAITING_ADMIN_APPROVAL
ApprovalDate:
ApprovalIdentifier:
```
