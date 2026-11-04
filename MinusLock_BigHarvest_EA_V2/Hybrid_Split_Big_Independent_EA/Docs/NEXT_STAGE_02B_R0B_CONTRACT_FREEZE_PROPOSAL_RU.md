# 02B-R0B — окончательное предложение фиксации контрактов

База `9b43c38afdb89c6b3b514b654c7fb9a936f9bf2b`, ветка work. Audit/test-only; production и historical evidence неизменны. Утверждение администратора отсутствует; все новые формулировки PROPOSED.

`CONTRACT_FREEZE_STATUS=PROPOSED`. Ни один текст не вступил в силу автоматически; старые нормативы/решения/evidence не переписываются. Для реализации нужен отдельный approval и отдельное задание.

## D-01

ActualDealNetRaw=Profit+Swap+Commission+Fee с исходными знаками и без повторного вычитания costs. PostedActualDealNet — независимо подтверждённая posted сумма/сумма posted компонентов данного источника. Если брокерский posted факт неизвестен, локальный HALF_EVEN не создаёт actual resource. AllocatableActualDealNet=max(0,PostedActualDealNet) только для подтверждённого reconciled eligible closing source. Отрицательный/нулевой net даёт zero grant, сохраняя signed economic result. Для COMMITTED: Σ OriginalBucketGrant=AllocatableActualDealNet, Unallocated=0; для PREPARED: Σ Grant+Unallocated=AllocatableActualDealNet, расход запрещён. Для каждого bucket Remaining+Consumed=Grant, 0<=Reserved<=Remaining, Available=Remaining-Reserved. Consumed не является источником. Все суммы конечны, одной валюты и precision. Вариант B (не default), candidate PrecisionPolicy R0A-MONEY-1: decimal minor units, ROUND_HALF_EVEN один раз после суммы raw components; первые четыре shares округляются вниз, весь остаток — ResidualHeld. Policy должна быть утверждена и сверена с broker posting; несовпадение/неизвестная точность => UNAVAILABLE. ResidualHeld входит в сохранение денег, но не доступен потребителю; это не промежуточный Unallocated. Replay immutable grant сравнивает весь per-bucket vector, source, policy и schema. Balance меняется только отдельным consumption/reservation/release event. R0B рекомендует первичными broker-posted данные; local precision policy допустима только versioned, после source/account/currency-specific сверки с receipt. При mismatch либо неизвестной precision — UNAVAILABLE. Неатрибутированный actual debit/убыток требует независимой funding reconciliation: нельзя ни восстановить Consumed, ни списать случайный bucket; aggregate availability до сверки UNPROVEN/UNAVAILABLE.

**Рекомендуемое решение:** Broker-posted первично; approved local policy only after verification, otherwise UNAVAILABLE. Полные immutable grants; отдельные balances; промежуточный Unallocated недоступен.

**Альтернативы:** Allocation F: full COMMITTED equality, partial only PREPARED (recommended); Permanent partial COMMITTED: not supported without separate exact schema decision; A: broker-posted amounts/posted components with independent source receipt; B: versioned local precision policy after broker validation; C: UNAVAILABLE without sufficient data

**Утверждение:** AWAITING.

## D-02

Ввести ProjectedBasketNet, ProjectedCloseNowNet, ActualRealizedDealNet, ReconciledEconomicNet, AllocationGrant, AvailableReserve. Все имеют amount/currency/precision/schema и provenance reference; projected имеют market/cost/position snapshots, actual — confirmed history source, reconciled — independent reconciliation receipt, grant — committed allocation, available — текущий balance revision. ProjectedBasketNet/ProjectedCloseNowNet никогда не конвертируются напрямую в actual/grant/available. Источником actual является независимо прочитанное экономическое событие broker history; opening commissions/fees учитываются в economic result один раз, но harvest conversion требует eligible closing deal; actual→reconciled требует сравнения signed components и ownership; reconciled→grant — утверждённой role/allocation policy; grant→available — проверенного остатка с reservations. ProjectedCatchUpMargin — только прогнозная проверка, не authorization. AuthorizedCatchUpMargin использует подтверждённый AvailableReserve и выбранную D-04 loss metric. Ни один planning PASS не создаёт settled ресурс и не означает commit.

**Рекомендуемое решение:** Раздельные DTO, без неявного projected→actual/available.

**Альтернативы:** Один double с флагами; Раздельные DTO и явные conversion gates

**Утверждение:** AWAITING.

## D-03

Разделить AggregateBasketGain, ProjectedReserveCandidate, ActualEligibleReserveSource, CommittedReserveGrant и AvailableReserve. BigCore/BigTrend могут финансировать FinalReserve только положительным actual closing DealNet после reconciliation и утверждённой allocation policy. ProjectedReserveCandidate не является доступным ресурсом. Small участвует в actual economic ledger один раз; его положительный allocatable net по рекомендуемой политике целиком направляется в non-spendable ResidualHeld с исходным SourceDealKey/Role/Event. Negative Small net уменьшает actual economic result и не создаёт отрицательный grant. Распределение Small в иные buckets требует другого явного решения и versioned migration. Opening deals и InitialProfit не являются harvest sources. До утверждения production RHS не изменяется.

**Рекомендуемое решение:** Small positive net — ResidualHeld, не BigReserve; Core/Trend только confirmed eligible источники.

**Альтернативы:** Small участвует в BigReserve по новому разрешению; Small отдельно в ResidualHeld; Small в отдельном утверждённом spending bucket

**Утверждение:** AWAITING.

## D-04

AbsoluteFarLoss=max(0,-FarNetCurrent). IncrementalFarLoss=max(0,AbsoluteFarLossCurrent-AbsoluteFarLossBaseline). Candidate GateMetric=ABSOLUTE, зафиксированная в immutable CatchUpPolicy; переключение ради PASS запрещено. FarNetCurrent — типизированный fresh close-now broker-money proof по действующей стороне BUY/Bid, SELL/Ask и согласованным costs; он не создаёт Reserve. Incremental недоступен без independently verified baseline. Baseline включает account namespace, symbol, position, direction, volume, CycleID, PlanID, origin StateRevision, snapshot/time и costPolicy; текущее состояние требует проверенной lineage. В минимальной версии новая revision/plan/cycle/side/volume/costVersion инвалидирует baseline до явной reconciliation; stale либо невосстановленный после restart baseline => incremental UNAVAILABLE. Отсутствие baseline не мешает вычислять ABSOLUTE по подтверждённому current proof; metric не выбирается fallback-эвристикой.

**Рекомендуемое решение:** Хранить оба, для рекомендуемого рабочего gate выбрать ABSOLUTE; incremental — diagnostic до отдельного разрешения.

**Альтернативы:** AbsoluteFarLoss для gate; IncrementalFarLoss с независимым baseline; Оба значения раздельно, metric в immutable policy

**Утверждение:** AWAITING.

## D-05

До исполнения ProjectedTransitionRisk сравнивается с плановым cap и сохраняет snapshot/cost basis. После исполнения ActualTransitionLoss=max(0,-Σunique confirmed closing deal signed net). Partial fills учитываются по уникальным account-scoped DealTicket/EventID с remainingVolume; неполный batch не становится completed. Under-cap partial => PENDING; observed actual loss>cap даже до завершения => SAFE_BLOCKED/accounting reconciliation. Unconfirmed history => UNAVAILABLE; duplicate/changed fill => CONFLICT. Slippage=разница observed и planned outcomes записывается как diagnostic delta; actual signed DealNet не уменьшается повторно на этот delta. Превышение не переписывает факт на planned10 и не разрешает новый переход/торговлю.

**Рекомендуемое решение:** Раздельные типы и обязательная post-fill reconciliation.

**Альтернативы:** Общий DTO с тегом; Раздельные projected/actual records

**Утверждение:** AWAITING.

## D-06

Каждый cost/buffer содержит Name,Currency,Source,Purpose,CalculationStage,AlreadyIncludedInNet,MayOverlapWith,PolicyVersion,Amount,RiskBasis,Window и EvidenceDigest. Profit/Swap/Commission/Fee в actual net сохраняют signed broker значения; spread и slippage не вычитаются повторно из actual DealNet. Projected costs используют явно доказанный price/cost basis: spread, уже отражённый в open/close Bid/Ask, не повторяется как дополнительный charge. AlreadyIncludedInNet устанавливается reconciliation расчётного basis, не caller boolean. Одно покрытие RiskBasis/Window допускается ровно один раз; duplicate coverage => CONFLICT, неизвестный overlap/валюта/policy => UNAVAILABLE. Leg execution uncertainty, transition safety и Catch-Up safety складываются только при доказанной независимости рисков. До утверждения нельзя удалять существующие buffers или менять production формулу.

**Рекомендуемое решение:** Charge-once по документированным riskBasis/window, отдельные независимые risk budgets; unresolved overlap блокирует proof.

**Альтернативы:** Единый общий budget с распределением; Независимые бюджеты с непересекающимися risk basis

**Утверждение:** AWAITING.

## D-07

EventIdentity=(broker,server,AccountLogin,ConsumptionEventID) в versioned namespace. Canonical payload включает source/allocation event/policy, bucket, currency/precision, amount, consumer purpose, cycle/plan/action/revision и immutable intent. Прочитать проверенный полный journal/authority scope; затем SameEvent+SameCanonicalPayload => NO_OP с delta balances/revision/actions=0, даже если исходная revision историческая и available уже нулевой. SameEvent+different payload => CONFLICT без mutation. Для нового события проверить current owner/source/plan/cycle/revision, COMMITTED allocation, known schema/policy, finite positive amount и sufficient available: результат ELIGIBLE_FOR_COMMIT, не списание. State revision compare-and-set и journal commit выполняются атомарно отдельным commit protocol; только подтверждённый commit меняет Consumed/Remaining и revision один раз. Missing/incomplete/stale authority или registry => UNAVAILABLE. hasPriorConsumption=false не является доказательством отсутствия событий. In-memory oracle не доказывает durable commit/restart correctness. Разделить immutable AllocationPolicyVersion и current ConsumptionPolicyVersion. Exact historical event сравнивается с историческим canonical payload до текущей revision/policy проверки; изменённый payload — CONFLICT. Для own-reservation consumption одновременно Remaining-=x,Consumed+=x,Reserved-=x; для unreserved debit Reserved не меняется. Требуется независимый ReservationOwner/Intent binding; эта ветвь не реализована данным oracle.

**Рекомендуемое решение:** Typed outcomes; eligibility отдельно от commit, durable registry как prerequisite.

**Альтернативы:** Typed NO_OP; REJECT с доказанным NOOP reason

**Утверждение:** AWAITING.

## D-08

SourceDealKey canonical namespace=(SchemaVersion,BrokerIdentity,ServerIdentity,AccountLogin,DealTicket); Symbol/Magic/Cycle/Plan/Action/Position/Order/Event/Role/Direction/EntryType и signed Profit/Swap/Commission/Fee/DealNet/Volume/Price/Time — immutable связанные поля Economic Record. Один DealTicket данного account namespace нельзя повторно легализовать изменением Magic/Cycle. Подтверждение — независимое чтение history и сверка journal/positions/immutable plan mapping, не valid/actual/fillsConfirmed/runtimeConfirmed и не comment. Reserve chain: BrokerHistory→ConfirmedDeal→EconomicReconciliation→ImmutableRecord→CommittedAllocation→ExpectedIdentity→ConsumptionAuthorization→CatchUp→NewFarEligibility. ExpectedIdentity строится из authority и immutable evaluation context; submitted proof/expected не являются источником. Проверяются canonical payload/digest, account/source/role, signed amounts, policy, available и revision. Полный history без сделки =>REJECT; недоступная/неполная authority =>UNAVAILABLE и все downstream authorizations NO. Far-loss отдельная ветвь: confirmed Far origin + observed owned position + fresh broker close-now calculation; отрицательный Far loss не требует фиктивного profit allocation и не становится ресурсом. Никакого auto-resume при unknown history/schema. R0B предлагает codec HSBI-ECON-RAW64-1: source raw finite binary64 значения сохраняются canonical big-endian hex16, -0 нормализуется в +0; денежные вычисления/posted minor units хранятся отдельно. IDs типизированы без bool coercion, Magic — signed nonzero configured long. SourcePlan/SourceAction/OriginRevision неизменны; текущие ConsumptionPlan/Action/Revision/Snapshot привязываются отдельным journal receipt. Codec/миграция требуют явного утверждения; пять Python golden vectors не являются MQL5 acceptance.

**Рекомендуемое решение:** История брокера плюс durable журнал и независимая reconciliation; fixture только для тестов.

**Альтернативы:** Доверенные caller flags; Broker history + durable journal + independent reconciliation; Test-only fixture provider без production authorization

**Утверждение:** AWAITING.

## CR-09

RequiredLevels определяется immutable proof depth/планом до расчёта margin и независимо от знака результата. EligibleLevels для all-level гарантии должен покрывать RequiredLevels полностью: отсутствие/неполнота/stale source, money, cost, risk, margin, Far projection или snapshot proof => UNAVAILABLE/UNPROVEN для всей гарантии, а не исключение неудобного уровня. Каждый обязательный уровень проходит lot gate Share*Bnet>F, независимый source/available proof и согласованную loss/buffer policy. Для варианта A WorstCatchUpMargin=min_i(AvailableReserve_i-FarLossMetric_i-SafetyBuffer_i); PASS только при строгом >0 и всех прочих gates. Tie-break — минимальный levelIndex среди минимумов; все уровни/metrics/proofs/policy входят в digest. Available_i не является суммой одинаковых средств по альтернативным сценариям; для последовательного пути нужен проверенный cumulative balance evolution. Projected future gain без source/available proof не даёт authority. Вариант B оценивает immutable выбранный control level и возвращает SINGLE_LEVEL_ONLY без all-level guarantee; maximum TransitionLoss не доказывает A. Политика и её scope требуют отдельного утверждения; production selector здесь не меняется.

**Рекомендуемое решение:** A; B допустим только явно ограниченным альтернативным решением.

**Альтернативы:** A: все обязательные уровни; B: один выбранный уровень без all-level guarantee

**Утверждение:** AWAITING.

## Zero BigCore: Vmin необходим, но недостаточен

Reject candidate, если mandatory Core после rounding меньше Vmin/не на известном grid/выше Vmax. Дополнительно нужны Far/Small и optional Trend grid, maximum, positive Bnet/recovery slope, money/margin/risk/compression/source gates. Positive slope .19 при Core0 не заменяет volume gate. При Vmin=.015,Vstep=.01 нельзя произвольно предположить grid origin: zero-origin profile даёт UNPROVEN; другой broker grid требует evidence.

Выполнены zero/subminimum/equal/above minimum, nonstandard .025 step, inconsistent min/step, over-max и negative-slope cases. GEOMETRY_ONLY не является NewFar/trading readiness. Automatic ceil Core до Vmin меняет NetLot, slope, money/risk/margin; без отдельного решения запрещён. Production geometry не исправлена. Возможность Trend=0 при положительном raw Trend требует отдельного уточнения optional-leg semantics.

## CR-09: варианты и доказательство

A: min money margin всего immutable RequiredLevels, включая отрицательные/нулевые. Missing/duplicate/stale, RequiredSet mismatch и недостаточная depth не фильтруются и дают UNPROVEN. B: max TransitionLoss — SINGLE_LEVEL_ONLY. L1 T100,C29 против L2 T10,C-16 — контрпример эквивалентности. Выбранный j из argmax T является argmin C тогда и только тогда, когда Cj<=Ci для всех i. Sufficient связь C=a-bT,b>0 даёт равенство argsets при согласованных ties; из одного T этого не следует.

All-level positivity не доказывает sequential feasibility. Повторно подставив исходные50 при двух расходах30, получаем отдельные margins20; реально после первого шага осталось20, второй расход30 отклоняется. Sequential reference хранит Before/Consumption/After, missing input =>UNPROVEN. CONSERVATION_ONLY не означает broker-executable recovery.

## Оставшиеся обязательные зависимости

Реальный broker posting/history authenticity, durable commit/restart, own-reservation settlement, partial-fill execution, global debit attribution и полный NewFar остаются NOT_RUN/UNPROVEN. Нельзя опустить их из реализации из-за passing fixtures. Unknown provider/schema/precision/mapping блокирует authorization. Новые исходники — test-only reference; production remediation не выполнена.
