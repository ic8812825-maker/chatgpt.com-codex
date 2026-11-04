# 02B-R0A — рекомендации D-01–D-08 и CR-09

Проверенная база: `cb5e55cb38aa4f2eb5b58e5218462c6738f3097a`, ветка `work`, UTC проверки `2026-11-04T01:18:36Z`. Режим `NORMATIVE_FREEZE_PREPARATION / AUDIT_AND_TEST_ONLY`. Все новые экономические формулировки — **PROPOSED**, не утверждённый production-норматив. `STAGE_02B_R1_IMPLEMENTATION_ALLOWED=NO`.

Точные формулировки и поля утверждения: [лист администратора](NEXT_STAGE_02B_R0A_ADMIN_APPROVAL_SHEET_RU.md). Этот пакет не отменяет исторические нормы по дате публикации.

## D-01. Allocation conservation

**Проблема:** Docs/04,08 требуют equality; Docs/32 допускает <= и складывает consumed с неуточнёнными grants.

**Варианты:** Полное committed распределение; Частичное распределение с отдельной phase/Unallocated

**Рекомендация:** Полные immutable grants; отдельные balances; промежуточный Unallocated недоступен.

**Численные/математические последствия:** Net100, grants60 и Unallocated40 допустимы только PREPARED; COMMITTED требует ResidualHeld40. Grant50, consumed10 => remaining40, не 60. Net .01 и две shares .5 дают ResidualHeld .01. Raw1.005 => posted1.00, raw1.015 =>1.02 по candidate half-even.

**Риск и миграция:** Нужно подтвердить precision policy на целевом broker; no global tolerance для immutable equality. Нельзя прибавить consumed к original grants. Новая schema: OriginalGrant/Consumed/Reserved/Remaining различаются. Старое reserveAllocated нельзя автоматически объявить original/remaining. Legacy с неизвестной полнотой => reconciliation, без spend.

**Влияние на Big/Small/Catch-Up/NewFar/persistence:** HSBI_EconomicLedgerTypes, HSBI_AllocationLedgerTypes, HSBI_ReserveAllocationTypes, MoneyState; Big harvest без скрытого remainder, Small — отдельный источник, Catch-Up/NewFar не тратят ResidualHeld.

**Источники/статус:** Docs/04:Allocation conservation; Docs/08:Allocation Ledger; Docs/32; CR-01/04/07/08; предложение ожидает администратора.

**Выполненные test IDs:** D01-signed-net, D01-components-sum-mismatch, D01-allocatable--15, D01-allocatable-0, D01-allocatable-1.005, D01-allocatable-1.015, D01-rounding-residual, D01-valid-balance, D01-no-double-count, D01-partial-committed, D01-partial-prepared, D01-prepared-no-consume, D01-negative-available, D01-missing-bucket, FINITE-nan, FINITE-inf, FINITE-NaN, FINITE-Infinity, FINITE-True, L02-bucket-digest.

## D-02. Денежные типы и преобразования

**Проблема:** Общее recoveryMoney может смешивать прогноз и доступный ресурс.

**Варианты:** Один double с флагами; Раздельные DTO и явные conversion gates

**Рекомендация:** Раздельные DTO, без неявного projected→actual/available.

**Численные/математические последствия:** ProjectedBasketNet100, confirmed closes0 => actual0, grant0, AvailableReserve0. RecoveryPL=realized+open close-now; buckets повторно к нему не прибавляются.

**Риск и миграция:** Прогноз будущих уровней не доказывает наличие средств сегодня. Строгая типизация должна проверяться в вызывающем слое и при десериализации. Legacy projected без source receipt остаётся projected или UNAVAILABLE; никакой миграции через actual=true.

**Влияние на Big/Small/Catch-Up/NewFar/persistence:** Новые Money DTO/конвертеры; Basket/FutureSmall/CatchUp/NewFar assembly. Big/Small прогнозы сохраняют planning-only статус; доступность NewFar отделена от прогнозного money proof.

**Источники/статус:** Docs/04:RecoveryPL; Docs/24; Docs/27; Docs/31; CR-02/05/10; предложение ожидает администратора.

**Выполненные test IDs:** D02-no-implicit-ProjectedBasketNet, D02-no-implicit-ProjectedCloseNowNet, D02-no-implicit-ActualRealizedDealNet, D02-no-implicit-AllocationGrant, D02-no-implicit-AvailableReserve, D02-history-missing, D02-no-confirmed-closes, D02-projected100-available0.

## D-03. Происхождение Reserve

**Проблема:** Aggregate Core+Trend+Small ошибочно выглядит разрешённым Big Reserve.

**Варианты:** Small участвует в BigReserve по новому разрешению; Small отдельно в ResidualHeld; Small в отдельном утверждённом spending bucket

**Рекомендация:** Small positive net — ResidualHeld, не BigReserve; Core/Trend только confirmed eligible источники.

**Численные/математические последствия:** Core0+Trend0+Small10: AggregateBasketGain10; BigReserve contribution0; Small ResidualHeld10. Core10 даёт eligible contribution10 до policy shares. Экономические +10 Small не теряются и не прибавляются повторно.

**Риск и миграция:** ResidualHeld блокирует расход этой прибыли до отдельного решения; это осознанное ограничение, не исчезновение денег. Исторические Small allocations не переклассифицировать без подтверждённого source/consumption history; отдельная policyVersion.

**Влияние на Big/Small/Catch-Up/NewFar/persistence:** HSBI_EvaluateBasketMoney / ReserveSourceProof / CatchUp; role-aware AllocationGrant. Big и Small не меняют geometry; NewFar не использует общий basket gain как authority.

**Источники/статус:** Docs/08:Isolation; Docs/31; CR-10; M05-small-only; предложение ожидает администратора.

**Выполненные test IDs:** D03-opening-no-grant-source, D03-small-not-reserve, D03-small-not-lost, D03-role-BigCore, D03-role-BigTrend.

## D-04. Absolute и incremental Far loss

**Проблема:** Название increase не определяет baseline и может ослаблять gate.

**Варианты:** AbsoluteFarLoss для gate; IncrementalFarLoss с независимым baseline; Оба значения раздельно, metric в immutable policy

**Рекомендация:** Хранить оба, для рекомендуемого рабочего gate выбрать ABSOLUTE; incremental — diagnostic до отдельного разрешения.

**Численные/математические последствия:** Baseline40,current50,buffer5: Reserve20 => absolute -35, incremental +5; Reserve60 => +5/+45. Current30 при baseline40 => incremental0. Partial close меняет volume/basis: нельзя вычесть старый loss40 из нового loss20 автоматически.

**Риск и миграция:** ABSOLUTE консервативнее данного примера, но не является доказательством полной recovery. Broker-specific расчёты NOT_RUN. Сохранять lossMetric/version, baseline origin и lineage. Старый baseline не угадывать; current absolute semantics до реализации остаётся прежней.

**Влияние на Big/Small/Catch-Up/NewFar/persistence:** BasketMoney/CatchUp/NewFar proof assembly и digests. Big/Small feasibility и время Catch-Up меняются только после утверждения; geometry неизменна.

**Источники/статус:** Docs/04:Reserve Catch-Up; Docs/24; Docs/31; D-04 предыдущего пакета; предложение ожидает администратора.

**Выполненные test IDs:** D04-margins-20, D04-margins-60, D04-missing-baseline, D04-stale-baseline, D04-baseline-unneeded-absolute, D04-loss-decrease, D04-BUY-Bid-cost, D04-SELL-Ask-cost, D04-baseline-control, D04-baseline-binding-side, D04-baseline-binding-volume, D04-baseline-binding-cycle, D04-baseline-binding-plan, D04-baseline-binding-revision, D04-baseline-binding-snapshot, D04-baseline-binding-costVersion, D04-restart-not-restored, D04-partial-close-rebase.

## D-05. ProjectedTransitionRisk и ActualTransitionLoss

**Проблема:** Одна семантическая область для плановой оценки и фактического accounting.

**Варианты:** Общий DTO с тегом; Раздельные projected/actual records

**Рекомендация:** Раздельные типы и обязательная post-fill reconciliation.

**Численные/математические последствия:** Projected10, actual15, cap12: плановое прохождение не отменяет превышение3; diagnostics actual-planned=5. Частичный actual10 остаётся PENDING; partial15 уже SAFE_BLOCKED.

**Риск и миграция:** Здесь SAFE_BLOCKED — контракт результата accounting, не реализованный торговый FSM transition. Хранить planned и actual separately, уникальные fills, remaining volume и over-cap reason; legacy с неизвестной completeness => UNAVAILABLE.

**Влияние на Big/Small/Catch-Up/NewFar/persistence:** HSBI_EvaluateFutureSmallLevel, NewFar gates, ActualClosingDeals DTO и accounting reconciliation. Small transition сохраняет partial completeness; Big harvest не подменяет actual прогнозом.

**Источники/статус:** Docs/04:Transition Loss; Docs/08; Docs/27; R12A per-ticket fill/batch atomicity; предложение ожидает администратора.

**Выполненные test IDs:** D05-overcap, D05-slippage-diagnostic-only, D05-partial-overcap, D05-partial-under-cap, D05-complete-under-cap, D05-duplicate-fill, D05-unconfirmed-fill.

## D-06. Costs и safety buffers

**Проблема:** Не определено пересечение per-leg и Catch-Up deductions.

**Варианты:** Единый общий budget с распределением; Независимые бюджеты с непересекающимися risk basis

**Рекомендация:** Charge-once по документированным riskBasis/window, отдельные независимые risk budgets; unresolved overlap блокирует proof.

**Численные/математические последствия:** Четыре независимых leg buffer1 + иной CatchUpRisk1 =>5. Пятый charge того же risk basis =>CONFLICT, не молча4/5. Уже включённый charge1 даёт additional deduction0.

**Риск и миграция:** Неподтверждённое разбиение может недоучесть риск; кандидат не отменяет текущую production защиту. Новая cost coverage schema; старые combined buffers без basis требуют независимого rebuild projected proof, не изменения actual history.

**Влияние на Big/Small/Catch-Up/NewFar/persistence:** HSBI_CostModel/ProjectedProfit/LevelMoney/Basket/CatchUp и proof digests; Big/Small/последующие уровни используют одинаковую policy версии.

**Источники/статус:** Docs/24; Docs/04:Reserve Catch-Up; Include/Money/HSBI_CostModel.mqh:18; D-06 предыдущего пакета; предложение ожидает администратора.

**Выполненные test IDs:** D06-independent-five, D06-overlap-not-silent, D06-already-in-net, D06-currency, D06-negative.

## D-07. Replay, eligibility и commit

**Проблема:** Bool prior и key без amount не доказывают exactly-once.

**Варианты:** Typed NO_OP; REJECT с доказанным NOOP reason

**Рекомендация:** Typed outcomes; eligibility отдельно от commit, durable registry как prerequisite.

**Численные/математические последствия:** Reserve50; E1=10 =>remaining40; exact E1 =>40/revision unchanged; E1=11 =>CONFLICT; новый E2=41 =>REJECT. Новый E2=40 после CAS может исчерпать bucket; последующий новый debit отклоняется.

**Риск и миграция:** Гонки consumers и torn journals остаются UNPROVEN до отдельной durable реализации. Не считать ELIGIBLE совершённым денежным событием. Старые events без amount/bucket/policy нельзя автоматически считать exact replay. Восстановить source payload или UNAVAILABLE/manual review.

**Влияние на Big/Small/Catch-Up/NewFar/persistence:** HSBI_ReserveConsumptionKey/duplicate/conflict/digest, CatchUp authorization, money state/restart interfaces. Replay Big/Small/NewFar не создаёт новый grant/action.

**Источники/статус:** Docs/08:Keys/exactly-once; Docs/16; Docs/32; R10 replay binding; предложение ожидает администратора.

**Выполненные test IDs:** D07-eligible-not-commit, D07-no-mutation-on-eligibility, D07-first10, D07-exact-noop, D07-altered11, D07-next41, D07-full-consumption, D07-full-replay-noop, D07-spent-bucket-new-event, D07-missing-registry, D07-reserved-not-available, D07-binding-plan, D07-binding-revision, D07-binding-cycle, D07-binding-policy, D07-binding-allocationEvent, D07-binding-source.

## D-08. Независимый economic authority

**Проблема:** Флаги и self-copy expected не подтверждают existence/provenance.

**Варианты:** Доверенные caller flags; Broker history + durable journal + independent reconciliation; Test-only fixture provider без production authorization

**Рекомендация:** История брокера плюс durable журнал и независимая reconciliation; fixture только для тестов.

**Численные/математические последствия:** Deal999 отсутствует в полном history =>REJECT независимо от флагов. Тот же Deal11 у другого account/server — другой source; изменённые компоненты55-5 и60-10 при Net50 — CONFLICT.

**Риск и миграция:** Хеш обеспечивает integrity, не внешнюю подлинность. Доверие fixture flags и полная durable correctness не доказаны. Legacy source без account/server/полного payload нельзя восстановить по строке Symbol|Magic|Cycle|Deal. Нужна проверяемая миграция из history, иначе блокировка.

**Влияние на Big/Small/Catch-Up/NewFar/persistence:** EconomicLedgerTypes, authoritative lookup/reconciliation DTO, HSBI_NewFarProofIdentity/assembly, ReserveSourceProof/FarLossProof, consumption boundaries. Все остальные NewFar objective/geometry gates сохраняются.

**Источники/статус:** Docs/08; Docs/16; Docs/31; Docs/32; R10 proofBoundary; R12A scope boundary; предложение ожидает администратора.

**Выполненные test IDs:** D08-proof-control, D08-missing-history, D08-authority-stale, D08-authority-incomplete, D08-invented-deal, D08-namespace-broker, D08-namespace-server, D08-namespace-account, D08-self-copy-owner, D08-self-copy-symbol, D08-self-copy-magic, D08-self-copy-deal, D08-self-copy-event, D08-self-copy-position, D08-self-copy-role, D08-self-copy-direction, D08-self-copy-cycle, D08-self-copy-action, D08-self-copy-plan, D08-self-copy-revision, D08-self-copy-snapshot, D08-wrong-digest, D08-stale, D08-wrong-net, D08-context-magic, D08-context-symbol, D08-forbidden-reserve-role, D08-allocation-reused, D08-allocation-owner, L01-component-digest, L01-same-record-digest.

## CR-09. WORST_CASE Catch-Up

**Проблема:** Maximum TransitionLoss не обязан совпадать с minimum Catch-Up margin.

**Варианты:** A: все обязательные уровни; B: один выбранный уровень без all-level guarantee

**Рекомендация:** A; B допустим только явно ограниченным альтернативным решением.

**Численные/математические последствия:** L1:T100,Reserve50,FarLoss20,buffer1 =>+29; L2:T10,Reserve5 =>-16; A reject L2, B maxT positive L1. Эквивалентность требует дополнительных связей, например C_i=a-b*T_i, b>0. В общем случае их нет.

**Риск и миграция:** Даже all-level положительные margins не доказывают реальную исполнимость trajectory, broker fill или конечность recovery. Хранить selectionPolicy/scope/version, RequiredLevels и все source proof references. Старый max-loss proof не повышать автоматически до all-level.

**Влияние на Big/Small/Catch-Up/NewFar/persistence:** Отдельный последующий этап FutureSmall aggregate selector/digest и NewFar integration; Big/Small geometry не меняется.

**Источники/статус:** Docs/30; Docs/27; Include/Planning/HSBI_FutureSmallProofAggregator.mqh:50; CR-09 предыдущего пакета; предложение ожидает администратора.

**Выполненные test IDs:** CR09-A-negative-level, CR09-B-limited-positive, CR09-zero, CR09-tie, CR09-missing-complete, CR09-missing-fresh, CR09-missing-sourceProof, CR09-no-filter-bad-level, CR09-lot-failure, CR09-equivalence-sufficient.
