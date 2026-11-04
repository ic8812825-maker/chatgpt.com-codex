# 02B-R0B — финальный лист административного утверждения

База `9b43c38afdb89c6b3b514b654c7fb9a936f9bf2b`. Только audit/test-only. Все D-01–D-08/CR-09 ожидают администратора. Новые документы не заменяют старые нормативы автоматически.

Документ содержит точный текст предложения и последствия. Поля решения/даты/идентификатора намеренно пусты. Никакой результат тестов их не заполняет. Перед отдельным R1.1 заданием нужны exact approved versions, codec/precision choice, migration policy и allowlist. Нельзя написать общую отметку PASS вместо выбранного нормативного текста.

## D-01

**DecisionID:** D-01

**Problem:** Docs/04,08 требуют equality; Docs/32 допускает <= и складывает consumed с неуточнёнными grants. Дополнительные R0B gaps и пределы доказательств перечислены в Findings.

**Alternatives:** Allocation F: full COMMITTED equality, partial only PREPARED (recommended); Permanent partial COMMITTED: not supported without separate exact schema decision; A: broker-posted amounts/posted components with independent source receipt; B: versioned local precision policy after broker validation; C: UNAVAILABLE without sufficient data

**RecommendedOption:** Broker-posted первично; approved local policy only after verification, otherwise UNAVAILABLE. Полные immutable grants; отдельные balances; промежуточный Unallocated недоступен.

**ExactNormativeText:** ActualDealNetRaw=Profit+Swap+Commission+Fee с исходными знаками и без повторного вычитания costs. PostedActualDealNet — независимо подтверждённая posted сумма/сумма posted компонентов данного источника. Если брокерский posted факт неизвестен, локальный HALF_EVEN не создаёт actual resource. AllocatableActualDealNet=max(0,PostedActualDealNet) только для подтверждённого reconciled eligible closing source. Отрицательный/нулевой net даёт zero grant, сохраняя signed economic result. Для COMMITTED: Σ OriginalBucketGrant=AllocatableActualDealNet, Unallocated=0; для PREPARED: Σ Grant+Unallocated=AllocatableActualDealNet, расход запрещён. Для каждого bucket Remaining+Consumed=Grant, 0<=Reserved<=Remaining, Available=Remaining-Reserved. Consumed не является источником. Все суммы конечны, одной валюты и precision. Вариант B (не default), candidate PrecisionPolicy R0A-MONEY-1: decimal minor units, ROUND_HALF_EVEN один раз после суммы raw components; первые четыре shares округляются вниз, весь остаток — ResidualHeld. Policy должна быть утверждена и сверена с broker posting; несовпадение/неизвестная точность => UNAVAILABLE. ResidualHeld входит в сохранение денег, но не доступен потребителю; это не промежуточный Unallocated. Replay immutable grant сравнивает весь per-bucket vector, source, policy и schema. Balance меняется только отдельным consumption/reservation/release event. R0B рекомендует первичными broker-posted данные; local precision policy допустима только versioned, после source/account/currency-specific сверки с receipt. При mismatch либо неизвестной precision — UNAVAILABLE. Неатрибутированный actual debit/убыток требует независимой funding reconciliation: нельзя ни восстановить Consumed, ни списать случайный bucket; aggregate availability до сверки UNPROVEN/UNAVAILABLE.

**MathematicalConsequences:** При debit x: Remaining-=x, Consumed+=x, поэтому их сумма сохраняется. Reservation отдельно уменьшает Available, не Grant. Equality по каждому source не доказывает общесчётную solvency. Grant50, remaining40, consumed10; reserved5 => available35. Нераспределённые10 допустимы PREPARED, не COMMITTED.

**ProductionImpact:** AllocationLedger conservation использует <= и consumed<=available; ReserveAllocationSource имеет finite/nonnegative guard, но original/remaining semantics не разделены. Изменения только будущим утверждённым scope; R0B production unchanged.

**MigrationImpact:** Новая schema: OriginalGrant/Consumed/Reserved/Remaining различаются. Старое reserveAllocated нельзя автоматически объявить original/remaining. Legacy с неизвестной полнотой => reconciliation, без spend.

**Tests:** EVENT-first; EVENT-full-consumed; GRANT-replay; GRANT-bucket-permutation; GRANT-altered-event; GRANT-altered-policyVersion; ALLOC-net-0; ALLOC-net--15; ALLOC-net-50; ALLOC-residual-cent; BALANCE-prepared; BALANCE-committed-unallocated

**Risks:** Broker authenticity/precision, durable IO/CAS, mandatory full caller chain, MQL5 runtime; никакой PASS из fixtures не закрывает эти зависимости.

```text
AdministratorDecision:
ApprovalStatus: AWAITING_ADMIN_APPROVAL
ApprovalDate:
ApprovalIdentifier:
```

Дополнительный выбор (не заполнен): AllocationVariant ______; PrecisionMode A/B/C ______; broker compatibility evidence ______.

## D-02

**DecisionID:** D-02

**Problem:** Общее recoveryMoney может смешивать прогноз и доступный ресурс. Дополнительные R0B gaps и пределы доказательств перечислены в Findings.

**Alternatives:** Один double с флагами; Раздельные DTO и явные conversion gates

**RecommendedOption:** Раздельные DTO, без неявного projected→actual/available.

**ExactNormativeText:** Ввести ProjectedBasketNet, ProjectedCloseNowNet, ActualRealizedDealNet, ReconciledEconomicNet, AllocationGrant, AvailableReserve. Все имеют amount/currency/precision/schema и provenance reference; projected имеют market/cost/position snapshots, actual — confirmed history source, reconciled — independent reconciliation receipt, grant — committed allocation, available — текущий balance revision. ProjectedBasketNet/ProjectedCloseNowNet никогда не конвертируются напрямую в actual/grant/available. Источником actual является независимо прочитанное экономическое событие broker history; opening commissions/fees учитываются в economic result один раз, но harvest conversion требует eligible closing deal; actual→reconciled требует сравнения signed components и ownership; reconciled→grant — утверждённой role/allocation policy; grant→available — проверенного остатка с reservations. ProjectedCatchUpMargin — только прогнозная проверка, не authorization. AuthorizedCatchUpMargin использует подтверждённый AvailableReserve и выбранную D-04 loss metric. Ни один planning PASS не создаёт settled ресурс и не означает commit.

**MathematicalConsequences:** Нет разрешённого перехода Projected→Grant: обязательное actual event/reconciliation отсутствует. Поэтому projected100 и actual0 не дают Available100. ProjectedBasketNet100, confirmed sources0 => allocated0/available0.

**ProductionImpact:** Basket.recoveryMoney=basketNetMoney — projected; MoneyState.valid/revision не проверяются локальным validator. Полного actual→authority pipeline нет. Изменения только будущим утверждённым scope; R0B production unchanged.

**MigrationImpact:** Legacy projected без source receipt остаётся projected или UNAVAILABLE; никакой миграции через actual=true.

**Tests:** ID-control-Broker; ID-foreign-Broker; ID-control-Server; ID-foreign-Server; ID-control-Account; ID-foreign-Account; ID-control-Symbol; ID-foreign-Symbol; ID-control-Magic; ID-foreign-Magic; ID-control-Deal; ID-foreign-Deal; ID-control-Order; ID-foreign-Order; ID-control-Position; ID-foreign-Position; ID-control-Cycle; ID-foreign-Cycle; ID-control-Plan; ID-foreign-Plan; ID-control-StateRevision; ID-foreign-StateRevision; ID-control-AllocationEvent; ID-foreign-AllocationEvent; ID-control-PolicyVersion; ID-foreign-PolicyVersion; ID-control-SnapshotID; ID-foreign-SnapshotID; ID-bool-Account; ID-bool-Deal; ID-signed-Magic-control; EVENT-exact-revision-advanced; EVENT-altered-amount; EVENT-exact-policy-advanced; EVENT-altered-policy; EVENT-altered-Broker; EVENT-altered-Server; EVENT-altered-Account; EVENT-altered-Symbol; EVENT-altered-Magic; EVENT-altered-Deal; EVENT-altered-Order; EVENT-altered-Position; EVENT-altered-Cycle; EVENT-altered-Plan; EVENT-altered-StateRevision; EVENT-altered-AllocationEvent; EVENT-altered-PolicyVersion; EVENT-altered-SnapshotID; EVENT-full-replay; EVENT-spent-new; GUARD-state-revision; GUARD-state-source; GUARD-state-allocation; GUARD-amount-precision; GUARD-currency; GUARD-precision-metadata; GUARD-source-unconfirmed; GUARD-source-role; GUARD-snapshot-stale; GUARD-source-stale; GUARD-history-missing; GUARD-history-unavailable; GUARD-grant-vector; GUARD-reserved-other-bucket; GUARD-consumed-other-bucket; GUARD-sum-grants; GUARD-negative-remaining; GUARD-amount-NaN; GUARD-amount-Infinity; GUARD-incomplete-authority; GUARD-missing-registry; SOURCE-signed-components; GUARD-prepared-no-spend

**Risks:** Broker authenticity/precision, durable IO/CAS, mandatory full caller chain, MQL5 runtime; никакой PASS из fixtures не закрывает эти зависимости.

```text
AdministratorDecision:
ApprovalStatus: AWAITING_ADMIN_APPROVAL
ApprovalDate:
ApprovalIdentifier:
```

## D-03

**DecisionID:** D-03

**Problem:** Aggregate Core+Trend+Small ошибочно выглядит разрешённым Big Reserve. Дополнительные R0B gaps и пределы доказательств перечислены в Findings.

**Alternatives:** Small участвует в BigReserve по новому разрешению; Small отдельно в ResidualHeld; Small в отдельном утверждённом spending bucket

**RecommendedOption:** Small positive net — ResidualHeld, не BigReserve; Core/Trend только confirmed eligible источники.

**ExactNormativeText:** Разделить AggregateBasketGain, ProjectedReserveCandidate, ActualEligibleReserveSource, CommittedReserveGrant и AvailableReserve. BigCore/BigTrend могут финансировать FinalReserve только положительным actual closing DealNet после reconciliation и утверждённой allocation policy. ProjectedReserveCandidate не является доступным ресурсом. Small участвует в actual economic ledger один раз; его положительный allocatable net по рекомендуемой политике целиком направляется в non-spendable ResidualHeld с исходным SourceDealKey/Role/Event. Negative Small net уменьшает actual economic result и не создаёт отрицательный grant. Распределение Small в иные buckets требует другого явного решения и versioned migration. Opening deals и InitialProfit не являются harvest sources. До утверждения production RHS не изменяется.

**MathematicalConsequences:** Small10 сохраняется как EconomicNet10 и ResidualHeld10; FinalReserve0. Повторно прибавить buckets к actual net нельзя. Core0 Trend0 Small10 => aggregate10, permitted BigReserve0.

**ProductionImpact:** Basket.reserveGainMoney=max(0,Core+Trend+Small); ReserveSourceProof отдельно разрешает Core/Trend. Actual Small funding через full NewFar не доказан. Изменения только будущим утверждённым scope; R0B production unchanged.

**MigrationImpact:** Исторические Small allocations не переклассифицировать без подтверждённого source/consumption history; отдельная policyVersion.

**Tests:** ID-control-Broker; ID-foreign-Broker; ID-control-Server; ID-foreign-Server; ID-control-Account; ID-foreign-Account; ID-control-Symbol; ID-foreign-Symbol; ID-control-Magic; ID-foreign-Magic; ID-control-Deal; ID-foreign-Deal; ID-control-Order; ID-foreign-Order; ID-control-Position; ID-foreign-Position; ID-control-Cycle; ID-foreign-Cycle; ID-control-Plan; ID-foreign-Plan; ID-control-StateRevision; ID-foreign-StateRevision; ID-control-AllocationEvent; ID-foreign-AllocationEvent; ID-control-PolicyVersion; ID-foreign-PolicyVersion; ID-control-SnapshotID; ID-foreign-SnapshotID; ID-bool-Account; ID-bool-Deal; ID-signed-Magic-control; EVENT-exact-revision-advanced; EVENT-altered-amount; EVENT-exact-policy-advanced; EVENT-altered-policy; EVENT-altered-Broker; EVENT-altered-Server; EVENT-altered-Account; EVENT-altered-Symbol; EVENT-altered-Magic; EVENT-altered-Deal; EVENT-altered-Order; EVENT-altered-Position; EVENT-altered-Cycle; EVENT-altered-Plan; EVENT-altered-StateRevision; EVENT-altered-AllocationEvent; EVENT-altered-PolicyVersion; EVENT-altered-SnapshotID; EVENT-full-replay; EVENT-spent-new; GUARD-state-revision; GUARD-state-source; GUARD-state-allocation; GUARD-amount-precision; GUARD-currency; GUARD-precision-metadata; GUARD-source-unconfirmed; GUARD-source-role; GUARD-snapshot-stale; GUARD-source-stale; GUARD-history-missing; GUARD-history-unavailable; GUARD-grant-vector; GUARD-reserved-other-bucket; GUARD-consumed-other-bucket; GUARD-sum-grants; GUARD-negative-remaining; GUARD-amount-NaN; GUARD-amount-Infinity; GUARD-incomplete-authority; GUARD-missing-registry; SOURCE-signed-components; GUARD-prepared-no-spend

**Risks:** Broker authenticity/precision, durable IO/CAS, mandatory full caller chain, MQL5 runtime; никакой PASS из fixtures не закрывает эти зависимости.

```text
AdministratorDecision:
ApprovalStatus: AWAITING_ADMIN_APPROVAL
ApprovalDate:
ApprovalIdentifier:
```

## D-04

**DecisionID:** D-04

**Problem:** Название increase не определяет baseline и может ослаблять gate. Дополнительные R0B gaps и пределы доказательств перечислены в Findings.

**Alternatives:** AbsoluteFarLoss для gate; IncrementalFarLoss с независимым baseline; Оба значения раздельно, metric в immutable policy

**RecommendedOption:** Хранить оба, для рекомендуемого рабочего gate выбрать ABSOLUTE; incremental — diagnostic до отдельного разрешения.

**ExactNormativeText:** AbsoluteFarLoss=max(0,-FarNetCurrent). IncrementalFarLoss=max(0,AbsoluteFarLossCurrent-AbsoluteFarLossBaseline). Candidate GateMetric=ABSOLUTE, зафиксированная в immutable CatchUpPolicy; переключение ради PASS запрещено. FarNetCurrent — типизированный fresh close-now broker-money proof по действующей стороне BUY/Bid, SELL/Ask и согласованным costs; он не создаёт Reserve. Incremental недоступен без independently verified baseline. Baseline включает account namespace, symbol, position, direction, volume, CycleID, PlanID, origin StateRevision, snapshot/time и costPolicy; текущее состояние требует проверенной lineage. В минимальной версии новая revision/plan/cycle/side/volume/costVersion инвалидирует baseline до явной reconciliation; stale либо невосстановленный после restart baseline => incremental UNAVAILABLE. Отсутствие baseline не мешает вычислять ABSOLUTE по подтверждённому current proof; metric не выбирается fallback-эвристикой.

**MathematicalConsequences:** При loss50/baseline40/buffer5 margins R20: -35/+5; R60: +5/+45. Различие делает выбор метрики нормативным. Baseline40/current50/Reserve20/buffer5: absolute rejects, incremental passes.

**ProductionImpact:** Basket/NewFar используют absolute max(0,-FarNetCurrent); независимый baseline/incremental contract отсутствует. Изменения только будущим утверждённым scope; R0B production unchanged.

**MigrationImpact:** Сохранять lossMetric/version, baseline origin и lineage. Старый baseline не угадывать; current absolute semantics до реализации остаётся прежней.

**Tests:** R0A unchanged 128: D-04 numeric vectors; broker runtime NOT_RUN

**Risks:** Broker authenticity/precision, durable IO/CAS, mandatory full caller chain, MQL5 runtime; никакой PASS из fixtures не закрывает эти зависимости.

```text
AdministratorDecision:
ApprovalStatus: AWAITING_ADMIN_APPROVAL
ApprovalDate:
ApprovalIdentifier:
```

## D-05

**DecisionID:** D-05

**Problem:** Одна семантическая область для плановой оценки и фактического accounting. Дополнительные R0B gaps и пределы доказательств перечислены в Findings.

**Alternatives:** Общий DTO с тегом; Раздельные projected/actual records

**RecommendedOption:** Раздельные типы и обязательная post-fill reconciliation.

**ExactNormativeText:** До исполнения ProjectedTransitionRisk сравнивается с плановым cap и сохраняет snapshot/cost basis. После исполнения ActualTransitionLoss=max(0,-Σunique confirmed closing deal signed net). Partial fills учитываются по уникальным account-scoped DealTicket/EventID с remainingVolume; неполный batch не становится completed. Under-cap partial => PENDING; observed actual loss>cap даже до завершения => SAFE_BLOCKED/accounting reconciliation. Unconfirmed history => UNAVAILABLE; duplicate/changed fill => CONFLICT. Slippage=разница observed и planned outcomes записывается как diagnostic delta; actual signed DealNet не уменьшается повторно на этот delta. Превышение не переписывает факт на planned10 и не разрешает новый переход/торговлю.

**MathematicalConsequences:** Observed net -15 даёт loss15 независимо от plan10; partial status не уменьшает известное превышение cap12. Projected10/actual15/cap12: SAFE_BLOCKED; actual не переписывается на10.

**ProductionImpact:** Future Small и NewFar используют projected transition metrics; actual closing deal reconciliation не реализована end-to-end. Изменения только будущим утверждённым scope; R0B production unchanged.

**MigrationImpact:** Хранить planned и actual separately, уникальные fills, remaining volume и over-cap reason; legacy с неизвестной completeness => UNAVAILABLE.

**Tests:** R0A unchanged 128: D-05 numeric vectors; broker runtime NOT_RUN

**Risks:** Broker authenticity/precision, durable IO/CAS, mandatory full caller chain, MQL5 runtime; никакой PASS из fixtures не закрывает эти зависимости.

```text
AdministratorDecision:
ApprovalStatus: AWAITING_ADMIN_APPROVAL
ApprovalDate:
ApprovalIdentifier:
```

## D-06

**DecisionID:** D-06

**Problem:** Не определено пересечение per-leg и Catch-Up deductions. Дополнительные R0B gaps и пределы доказательств перечислены в Findings.

**Alternatives:** Единый общий budget с распределением; Независимые бюджеты с непересекающимися risk basis

**RecommendedOption:** Charge-once по документированным riskBasis/window, отдельные независимые risk budgets; unresolved overlap блокирует proof.

**ExactNormativeText:** Каждый cost/buffer содержит Name,Currency,Source,Purpose,CalculationStage,AlreadyIncludedInNet,MayOverlapWith,PolicyVersion,Amount,RiskBasis,Window и EvidenceDigest. Profit/Swap/Commission/Fee в actual net сохраняют signed broker значения; spread и slippage не вычитаются повторно из actual DealNet. Projected costs используют явно доказанный price/cost basis: spread, уже отражённый в open/close Bid/Ask, не повторяется как дополнительный charge. AlreadyIncludedInNet устанавливается reconciliation расчётного basis, не caller boolean. Одно покрытие RiskBasis/Window допускается ровно один раз; duplicate coverage => CONFLICT, неизвестный overlap/валюта/policy => UNAVAILABLE. Leg execution uncertainty, transition safety и Catch-Up safety складываются только при доказанной независимости рисков. До утверждения нельзя удалять существующие buffers или менять production формулу.

**MathematicalConsequences:** Сумма5 корректна лишь для пяти независимых покрытий. При одном RiskBasis/Window два charge являются double deduction; удаление одного без evidence может недоучесть риск. Four leg1 + Catch-Up1: 5 при независимых risks; CONFLICT при повторе leg0 coverage.

**ProductionImpact:** ProjectedNet=gross+swap+commission+fee-spread-slippage-buffer; четыре leg buffer и отдельный Catch-Up buffer не имеют доказанной risk coverage карты. Изменения только будущим утверждённым scope; R0B production unchanged.

**MigrationImpact:** Новая cost coverage schema; старые combined buffers без basis требуют независимого rebuild projected proof, не изменения actual history.

**Tests:** R0A unchanged 128: D-06 numeric vectors; broker runtime NOT_RUN

**Risks:** Broker authenticity/precision, durable IO/CAS, mandatory full caller chain, MQL5 runtime; никакой PASS из fixtures не закрывает эти зависимости.

```text
AdministratorDecision:
ApprovalStatus: AWAITING_ADMIN_APPROVAL
ApprovalDate:
ApprovalIdentifier:
```

## D-07

**DecisionID:** D-07

**Problem:** Bool prior и key без amount не доказывают exactly-once. Дополнительные R0B gaps и пределы доказательств перечислены в Findings.

**Alternatives:** Typed NO_OP; REJECT с доказанным NOOP reason

**RecommendedOption:** Typed outcomes; eligibility отдельно от commit, durable registry как prerequisite.

**ExactNormativeText:** EventIdentity=(broker,server,AccountLogin,ConsumptionEventID) в versioned namespace. Canonical payload включает source/allocation event/policy, bucket, currency/precision, amount, consumer purpose, cycle/plan/action/revision и immutable intent. Прочитать проверенный полный journal/authority scope; затем SameEvent+SameCanonicalPayload => NO_OP с delta balances/revision/actions=0, даже если исходная revision историческая и available уже нулевой. SameEvent+different payload => CONFLICT без mutation. Для нового события проверить current owner/source/plan/cycle/revision, COMMITTED allocation, known schema/policy, finite positive amount и sufficient available: результат ELIGIBLE_FOR_COMMIT, не списание. State revision compare-and-set и journal commit выполняются атомарно отдельным commit protocol; только подтверждённый commit меняет Consumed/Remaining и revision один раз. Missing/incomplete/stale authority или registry => UNAVAILABLE. hasPriorConsumption=false не является доказательством отсутствия событий. In-memory oracle не доказывает durable commit/restart correctness. Разделить immutable AllocationPolicyVersion и current ConsumptionPolicyVersion. Exact historical event сравнивается с историческим canonical payload до текущей revision/policy проверки; изменённый payload — CONFLICT. Для own-reservation consumption одновременно Remaining-=x,Consumed+=x,Reserved-=x; для unreserved debit Reserved не меняется. Требуется независимый ReservationOwner/Intent binding; эта ветвь не реализована данным oracle.

**MathematicalConsequences:** После E1=10 из50 Remaining40; exact E1 не меняет state/revision. Changed payload не эквивалентен первому событию и даёт CONFLICT. E1=10 повторён с amount11 или policy2: CONFLICT, даже если текущая revision уже2.

**ProductionImpact:** Exact local duplicate блокируется как CALC_REJECT/NOOP reason; hasPrior=false обходит проверку knowledge прошлого; durable registry отсутствует. Изменения только будущим утверждённым scope; R0B production unchanged.

**MigrationImpact:** Старые events без amount/bucket/policy нельзя автоматически считать exact replay. Восстановить source payload или UNAVAILABLE/manual review.

**Tests:** EVENT-first; EVENT-full-consumed

**Risks:** Broker authenticity/precision, durable IO/CAS, mandatory full caller chain, MQL5 runtime; никакой PASS из fixtures не закрывает эти зависимости.

```text
AdministratorDecision:
ApprovalStatus: AWAITING_ADMIN_APPROVAL
ApprovalDate:
ApprovalIdentifier:
```

## D-08

**DecisionID:** D-08

**Problem:** Флаги и self-copy expected не подтверждают existence/provenance. Дополнительные R0B gaps и пределы доказательств перечислены в Findings.

**Alternatives:** Доверенные caller flags; Broker history + durable journal + independent reconciliation; Test-only fixture provider без production authorization

**RecommendedOption:** История брокера плюс durable журнал и независимая reconciliation; fixture только для тестов.

**ExactNormativeText:** SourceDealKey canonical namespace=(SchemaVersion,BrokerIdentity,ServerIdentity,AccountLogin,DealTicket); Symbol/Magic/Cycle/Plan/Action/Position/Order/Event/Role/Direction/EntryType и signed Profit/Swap/Commission/Fee/DealNet/Volume/Price/Time — immutable связанные поля Economic Record. Один DealTicket данного account namespace нельзя повторно легализовать изменением Magic/Cycle. Подтверждение — независимое чтение history и сверка journal/positions/immutable plan mapping, не valid/actual/fillsConfirmed/runtimeConfirmed и не comment. Reserve chain: BrokerHistory→ConfirmedDeal→EconomicReconciliation→ImmutableRecord→CommittedAllocation→ExpectedIdentity→ConsumptionAuthorization→CatchUp→NewFarEligibility. ExpectedIdentity строится из authority и immutable evaluation context; submitted proof/expected не являются источником. Проверяются canonical payload/digest, account/source/role, signed amounts, policy, available и revision. Полный history без сделки =>REJECT; недоступная/неполная authority =>UNAVAILABLE и все downstream authorizations NO. Far-loss отдельная ветвь: confirmed Far origin + observed owned position + fresh broker close-now calculation; отрицательный Far loss не требует фиктивного profit allocation и не становится ресурсом. Никакого auto-resume при unknown history/schema. R0B предлагает codec HSBI-ECON-RAW64-1: source raw finite binary64 значения сохраняются canonical big-endian hex16, -0 нормализуется в +0; денежные вычисления/posted minor units хранятся отдельно. IDs типизированы без bool coercion, Magic — signed nonzero configured long. SourcePlan/SourceAction/OriginRevision неизменны; текущие ConsumptionPlan/Action/Revision/Snapshot привязываются отдельным journal receipt. Codec/миграция требуют явного утверждения; пять Python golden vectors не являются MQL5 acceptance.

**MathematicalConsequences:** Нет логического вывода existence из DealID>0 или proof==copiedExpected. Фиксированный independent history отсутствующий deal отвергает независимо от caller flags. Order/Position/Snapshot неизвестны authorize R0A; добавленный чужой атрибут может быть проигнорирован. Это gap локальной API, не доказательство обхода полного verify_proof pipeline.

**ProductionImpact:** SourceDealKey=Symbol|Magic|Cycle|Deal без account/server; NewFar копирует expected из проверяемого proof. Caller flags не подтверждены broker lookup. Изменения только будущим утверждённым scope; R0B production unchanged.

**MigrationImpact:** Legacy source без account/server/полного payload нельзя восстановить по строке Symbol|Magic|Cycle|Deal. Нужна проверяемая миграция из history, иначе блокировка.

**Tests:** ID-control-Broker; ID-foreign-Broker; ID-control-Server; ID-foreign-Server; ID-control-Account; ID-foreign-Account; ID-control-Symbol; ID-foreign-Symbol; ID-control-Magic; ID-foreign-Magic; ID-control-Deal; ID-foreign-Deal; ID-control-Order; ID-foreign-Order; ID-control-Position; ID-foreign-Position; ID-control-Cycle; ID-foreign-Cycle; ID-control-Plan; ID-foreign-Plan; ID-control-StateRevision; ID-foreign-StateRevision; ID-control-AllocationEvent; ID-foreign-AllocationEvent; ID-control-PolicyVersion; ID-foreign-PolicyVersion; ID-control-SnapshotID; ID-foreign-SnapshotID; ID-bool-Account; ID-bool-Deal; ID-signed-Magic-control; EVENT-exact-revision-advanced; EVENT-altered-amount; EVENT-exact-policy-advanced; EVENT-altered-policy; EVENT-altered-Broker; EVENT-altered-Server; EVENT-altered-Account; EVENT-altered-Symbol; EVENT-altered-Magic; EVENT-altered-Deal; EVENT-altered-Order; EVENT-altered-Position; EVENT-altered-Cycle; EVENT-altered-Plan; EVENT-altered-StateRevision; EVENT-altered-AllocationEvent; EVENT-altered-PolicyVersion; EVENT-altered-SnapshotID; EVENT-full-replay; EVENT-spent-new; GUARD-state-revision; GUARD-state-source; GUARD-state-allocation; GUARD-amount-precision; GUARD-currency; GUARD-precision-metadata; GUARD-source-unconfirmed; GUARD-source-role; GUARD-snapshot-stale; GUARD-source-stale; GUARD-history-missing; GUARD-history-unavailable; GUARD-grant-vector; GUARD-reserved-other-bucket; GUARD-consumed-other-bucket; GUARD-sum-grants; GUARD-negative-remaining; GUARD-amount-NaN; GUARD-amount-Infinity; GUARD-incomplete-authority; GUARD-missing-registry; SOURCE-signed-components; GUARD-prepared-no-spend; CODEC-raw64-0.0; CODEC-raw64--0.0; CODEC-raw64-1.0; CODEC-raw64--5.0; CODEC-raw64-0.1

**Risks:** Broker authenticity/precision, durable IO/CAS, mandatory full caller chain, MQL5 runtime; никакой PASS из fixtures не закрывает эти зависимости.

```text
AdministratorDecision:
ApprovalStatus: AWAITING_ADMIN_APPROVAL
ApprovalDate:
ApprovalIdentifier:
```

Дополнительный выбор (не заполнен): CanonicalCodecVersion ______; Origin/Consumption binding policy ______; MigrationVersion ______.

## CR-09

**DecisionID:** CR-09

**Problem:** Maximum TransitionLoss не обязан совпадать с minimum Catch-Up margin. Дополнительные R0B gaps и пределы доказательств перечислены в Findings.

**Alternatives:** A: все обязательные уровни; B: один выбранный уровень без all-level guarantee

**RecommendedOption:** A; B допустим только явно ограниченным альтернативным решением.

**ExactNormativeText:** RequiredLevels определяется immutable proof depth/планом до расчёта margin и независимо от знака результата. EligibleLevels для all-level гарантии должен покрывать RequiredLevels полностью: отсутствие/неполнота/stale source, money, cost, risk, margin, Far projection или snapshot proof => UNAVAILABLE/UNPROVEN для всей гарантии, а не исключение неудобного уровня. Каждый обязательный уровень проходит lot gate Share*Bnet>F, независимый source/available proof и согласованную loss/buffer policy. Для варианта A WorstCatchUpMargin=min_i(AvailableReserve_i-FarLossMetric_i-SafetyBuffer_i); PASS только при строгом >0 и всех прочих gates. Tie-break — минимальный levelIndex среди минимумов; все уровни/metrics/proofs/policy входят в digest. Available_i не является суммой одинаковых средств по альтернативным сценариям; для последовательного пути нужен проверенный cumulative balance evolution. Projected future gain без source/available proof не даёт authority. Вариант B оценивает immutable выбранный control level и возвращает SINGLE_LEVEL_ONLY без all-level guarantee; maximum TransitionLoss не доказывает A. Политика и её scope требуют отдельного утверждения; production selector здесь не меняется.

**MathematicalConsequences:** T1=100>T2=10, но C1=29>C2=-16. Equivalence требует дополнительной antitone зависимости, например C=a-bT,b>0, с согласованными ties. A выбирает L2=-16 и reject; B выбирает L1=+29, но только SINGLE_LEVEL_ONLY.

**ProductionImpact:** Aggregator WORST_CASE выбирает worstTransitionLossLevel, а не минимальный денежный margin. Сам production не менялся. Изменения только будущим утверждённым scope; R0B production unchanged.

**MigrationImpact:** Хранить selectionPolicy/scope/version, RequiredLevels и все source proof references. Старый max-loss proof не повышать автоматически до all-level.

**Tests:** CR09-A-negative; CR09-B-positive-limited; CR09-all-positive; CR09-zero; CR09-missing-level; CR09-single-depth; CR09-duplicate-level; CR09-required-mismatch; CR09-sourceFresh; CR09-snapshotFresh; CR09-complete; CR09-currency; CR09-lot-gate; CR09-negative-loss-invalid; CR09-tie-different-loss; SEQUENTIAL-conserve; SEQUENTIAL-no-reuse; SEQUENTIAL-missing

**Risks:** Broker authenticity/precision, durable IO/CAS, mandatory full caller chain, MQL5 runtime; никакой PASS из fixtures не закрывает эти зависимости.

```text
AdministratorDecision:
ApprovalStatus: AWAITING_ADMIN_APPROVAL
ApprovalDate:
ApprovalIdentifier:
```

Дополнительный выбор (не заполнен): A all-level / B single-level ______; RequiredLevels policy ______; tie-break/version ______.
