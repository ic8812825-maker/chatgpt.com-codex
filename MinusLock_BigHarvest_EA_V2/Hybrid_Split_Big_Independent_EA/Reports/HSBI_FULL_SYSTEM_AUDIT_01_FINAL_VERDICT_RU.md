# Независимый вердикт по всей системе HSBI

BASE_SHA=4185b84f7a6a8847f6a9c5796f07113907be447d

Режим READ-ONLY ANALYSIS + AUDIT/TEST-ONLY. Источники не изменены. **AUDIT_COMPLETENESS=PARTIAL.** Native MQL5/MT5/broker/durable execution NOT_RUN. Proposed R0A–R0H не становятся нормативом из-за тестовых PASS. Все административные разрешения остаются NO.

## 18.1. Общая характеристика

**FINAL_SYSTEM_VERDICT=SYSTEM_CRITICAL_CONTRADICTIONS_FOUND.** HSBI сейчас представляет собой неторгующий MQL5-каркас с библиотекой расчётных/проверочных прототипов, обширным нормативным дизайном и несколькими поколениями test-only моделей. Это не целостный реализованный recovery EA. Его главная идея: после Initial Lock оставить Far, открыть противоположные Core/Trend с Small на стороне Far, закрывать/распределять подтверждённые profits, частично уменьшать Far либо пройти SmallTransition и переназначить actual residual originalCore как новый Far.

Текущий production entry намеренно выключен: main:21 задаёт HSBI_RUNTIME_DISABLED, RuntimePolicy:25 всегда запрещает dispatch, OnTick:37 вызывает только неуспешный stub. Это подтверждает отсутствие текущего broker dispatch path в проверенных исходниках, но не математическую/экономическую безопасность будущей системы. В реальном счёте этот каркас не управляет уже открытыми позициями и не является защитным EA.

Аудит нельзя считать полным доказательством системы: **AUDIT_COMPLETENESS=PARTIAL**. Все74production modules статически рассмотрены, основной51-lineмануал прочитан целиком, но не вся историческая документация/279test scripts повторно проверена семантически,137expression sites не доказаны как отдельные атомарные формулы, native/broker/durable/full-cycle evidence отсутствуют. Это ограничивает полноту отрицательного/положительного вывода, но не отменяет воспроизведённые source-contract failures.

## 18.2. Полнота руководства

Основное руководство: `Docs/03_FULL_SYSTEM_MANUAL_RU.md:1–51`; owner-contracts00–32, в том числе два27. Найдены133 indexed Docs/root files.31owner-текст прочитан целиком;19/21/22 и многие historical/proposed appendices индексированы/выборочно сопоставлены. Полная карта headings/status locators и manual-section→code/evidence/verdict в DOCUMENTATION_MAP/REQUIREMENT_MATRIX.

Руководство описывает требуемую последовательность, но «self-contained/OPEN_P0=0» не current implementation acceptance. Нужно отдельно решить objective minN vs risk-first, FarLoss absolute/incremental, reserve/balance phase mapping, cost overlap/buffers, all-level Catch-Up, transition A/B/C, codec/native domain и legacy provider boundary. Отсутствуют доказанные production procedures для actual account model/retcodes/fills/journal/terminal affordability/restart. Формальные owners TransactionEngine/FillAccumulator/FinalCloseCalculator/SnapshotStore не реализованы как рабочие компоненты. Historical architecture closure остаётся историей, не разрешением на R1.1/торговлю.

## 18.3. Вердикт по математике

Базовая размерностная алгебра lot/price/money во многих формулах корректна при предпосылках. Signed DealNet сохраняет Profit+Swap+Commission+Fee; Bid/Ask close side и lot floor/ceil существуют в source. RecoveryPL=realized+open-net без повторного прибавления allocation buckets — правильное accounting identity, не стратегия заработка.

Но формальная связность системы не доказана. Из49semantic families24 проверены только в заявленном математическом/reference domain,11 имеют code/spec/предлагаемый-policy contradictions,14 остаются UNVERIFIED. Counts не проценты готовности и не49nativeформул. Существуют ложные локальные PASS и неразрешённые proof obligations.

**Геометрия.** Сlope=C+T−S−F>0 — лишь sensitivity filter. Actual source приF.1,Rc.01,Rt3,Rs.1 получает Core0,Trend.3,Small.01,slope.19 и geometryVALID, вопреки обязательному minimumCore. Core.01 приmin.05 тоже допускается. Напротив, Rt0 допускается геометрией/нормативом, но BasketMoney требует positive volume всех четырёх legs и отклоняет отсутствующий Trend. Такие локальные defects не объявляются working whole-solver обходом: другие money wrappers могут отклонить zeroCore.

**Gross/net.** FutureSmallSolver:90 сравнивает netBigVolume с priorBigGross. ПриC.6,T.6,S1,F.1 BigGross1.2>old1, net.2<1. Permitted UnitTestlevel с остальными synthetic gates проходит. Это неверный показатель для документированного NextBigGross<OldBigGross.

**Worst-case.** Source выбирает уровень argmax TransitionLoss, не минимум Catch-Up margin. (Trans10,Rsv100,FarLoss90,Buffer1)->+9 против (Trans5,Rsv10,FarLoss20,Buffer1)->−11. Положительный выбранный control не all-level proof. CR09 должен явно утвердить scope, не просто дать одинаковое POSITIVE двум политикам.

**Конечность.** Теорема F(k)<=q^kF0 условна при uniformq на каждом будущем успешном transition. Finite prefix.8,.64 и flags не доказывают tail: следующий.64 нарушаетq^3=.512. ДостижениеVmin не закрывает оставшуюся позицию; solver может вернуть valid/finite при terminalRouteAllowedfalse и remainingFar.01. Нет operational close affordability proof. Это пробел доказательства/реализации, а не опровержение правильной условной геометрической теоремы.

**Transition.** Signed batch[-15,+100] даёт currentloss0, peak15 и stickybreachcap12. Решение о A/B/C/reset/ordered partialfills не принято автоматически. Раннее нарушение cap не исчезает как исторический факт из-за последующей прибыли.

## 18.4. Вердикт по экономике

**PROFITABILITY_PROVEN=NO; LOSS_BOUND_PROVEN=NO.** Нет независимого empirical market protocol/backtest/demo/holdout или реализованного полного cycle. Успешная unit арифметика не доказывает positive expectancy.

Синтетический exact пример (не brokerdata): FarSELL1@100, CoreBUY1.2@101, TrendBUY1@101, SmallSELL.5@100, openingfees.37. На104/105 BigNet6.38, SmallNet−2.55; закрытие всех C/T/S даёт положительный Harvest3.83. Balance1003.46, remainingFar loss−5, Equity998.46. Стоимость окончательного Farclose.10 =>CyclePnL−1.64. Сценарий не утверждает разрешение actual HSBI gate; он математически доказывает, что positive Harvest/balance не означает прибыль всего цикла. FinalClose full recovery gate должен отклонить недостаточный результат.

Не закрытая Far liability может увеличиваться после закрытия выгодных ног. При оставшемся shortQ, без guaranteed hedge/exit, P→∞ даёт−Q(P−open), то есть модель не имеет unconditional lossbound. Реальные stop-out/negative-balance safeguards требуют отдельной broker account модели, не предполагаются. Flat/adverse path, отрицательный carry, отсутствие ликвидности/маржи/receipt или gap могут сорвать дальнейший recovery и потребовать капитал либо принятие убытка. Нет доказанной неизбежной убыточности каждой траектории; есть отсутствие доказательств заявляемых гарантий.

Allocation/source accounting критически неполон. Economic equality допускает изменённые компоненты при том жеNet, allocation equality перестановку buckets. Reserve key не связан с authoritative allocation, а exhausted source50 может получить новое projected Catch-Up permission45 через alreadyAllocatedfalse. Это не исполненное повторное списание: backendapply отсутствует. Но такой калькулятор нельзя сделать financial authority без исправления. Global economic funding/account debits across allocations не доказаны. Source-level positive receipt не автоматический discretionary accountsurplus после losses Small/Far/fees.

## 18.5. Вердикт по торговой логике

**Полный торговый цикл не реализован.** Source callback FSM фактически одно состояние DISABLED. Library topology имеет33enums и1089 observedpair results, но нормальные transitions заканчиваются openingCore; Core→Trend отсутствует. Нет engines initialrollback, stagedbasketopen, fillaccumulation, Harvestsettlement, PartialFar reservationconsumption, authoritative FinalClose, confirmation/debounce, stagedSmall/newFarcommit или cycle reset.

Pure topology допускает terminalSafe→reconciling→FarActive без admin argument. Это не текущий autoresume (main не вызываетhelper), но не готовое enforcement no-auto-resume. Реальный переход требует independent observed event+ownership+ledger+durable result; provided booleans не заменяют эти действия. Нет liveness/termination proof, полной error-state recovery, защиты от actual external intervention, account reconnect/retcodes/out-of-order fills. Статусы и outcome DTO не сами brokerexecution.

## 18.6. Вердикт по архитектуре

Безопасное полезное свойство текущего дизайна — явный no-trade runtime, изоляция расчётов от sends, typed roles/IDs, fail-unavailable broker calculation wrappers и часть pure validators. Но только16headers в mainincludeclosure и13projectfunctions консервативно entry-reachable. Большинство библиотек dormant. Концептуальный layered design не соответствует работающей end-to-end orchestration.

Independent providers/history/origin attribution отсутствуют. NewFar перезаписывает proof identity из входных descriptors/IDs, затем копирует expected=presented; helper equality корректно сравнит данные, но независимость expected не доказана caller. Без provider reconciliation nonzeroDeal/actualfillsConfirmed/runtimeConfirmed остаются предпосылками, не брокерскими фактами.

Durable backend/SHA256/lock/CAS/versioned commit/restart history loader не реализованы: PersistenceInterface:5–7 явноfalse/stub. Snapshot/journal DTO и prefix checks не durable exactly-once. Journal alteredpayload с сохранённымcurrentDigest получает NO_OP до validation (FSA-027). Main не использует этивалидации для реального цикла. Money/Planning dependency coupling и отсутствие готового input config/account mode требуют отдельного designgate, не скрытого расширения MinimalR1.1.

## 18.7. Вердикт по исходному коду

Выбранные source bodies выполнены в isolated C++ LP64 adapter с documented math/string wrappers и synthetic OrderCalcProfit/OrderCalcMargin. Это НЕ nativeMQL5. **54scoped source checks:27PASS/27FAIL**; числоFAIL не числоуникальныхвзломов. M02 coherent expected acceptance и conservative-prefix acceptance записаны как корректные локальные наблюдения: они не доказывают независимую authority или universal tail. Отдельные caller/global proof gaps оцениваются статически/математически, не ложным helperFAIL. Каждыйissue имеет evidence scope/контрпример/локатор в DEFECT_REGISTER/DEFECTS.json.

Дополнительно подтверждены:

- Risk gate допускает NaN projectedMargin; NewFar gate допускает unknown allowedMargin. Не все ограничения/диапазоны проверяются.
- TransactionBarrier/ExternalOutcome допускают NaN volumes/prices как completed при прочих заданных flags/IDs.
- Context validator пропускает второйFAR в initialBuy, а NoDualTail считает лишь четыре слота.
- MoneyState ignoresvalid/revision и принимает+Infinity; Allocation validator допускает отрицательный bucket при сохранённой общей сумме.
- Futuretimestamp принимается какfresh; universalclock/skew contract отсутствует. StateRevision+1 не имеетoverflowguard.
- Digest-loop maximumDepth используется до downstream<=128 validation; опасный OOB runtime не запускался, staticgap сохранён кактаковой.

Нет доказательства, что эти dormantlibrary flaws уже привели к реальным сделкам/списаниям. Но включать их в financial orchestration без исправления нельзя. Вывод «real trading отсутствует» не превращает формулы/контракты в корректные.

## 18.8. Вердикт по безопасности

**Использовать как реальный торговый/защитный советник нельзя. Включать broker dispatch нельзя.** Currentstatic scan не нашёл sendingpaths, guards/versionflagsdisabled подтверждены hashes. Это означает no-current-dispatch, а не completed execution safety.

MetaEditor/MT5/Wine не обнаружены; MQL5compile/native tests/StrategyTester NOT_RUN. No native profit/codec/ABI/runtime guarantee. Подготовленные R0H harness/goldens могут быть основой следующего isolated native test задания после предоставления среды; это не разрешение торговых операций. Ограниченное tradinglogic StrategyTester testing требует сначала monetary/provenance/persistence/FSM gates и отдельного административного задания. Нынешний audit ничего из этого не разрешает.

## 18.9. Критические проблемы P0/P1

| ID / severity | Source locator | Problem | Evidence / category |
|---|---|---|---|
| FSA-001 P0 | Include/Money/HSBI_EconomicLedgerTypes.mqh:9 | Equality ignores components/identity metadata and uses epsilon Net; legacy key partitions same deal by Magic/Cycle without account namespace | L01_COMPONENT_CONFLICT,KEY_MAGIC_PARTITION; CONFIRMED_DEFECT |
| FSA-002 P0 | Include/Money/HSBI_AllocationLedgerTypes.mqh:8 | Duplicate checks total only, not bucket vector/policy/immutable payload | L02_VECTOR_CONFLICT; CONFIRMED_DEFECT |
| FSA-003 P0 | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:44 | Consumption key only shape/plan/revision checked, not matching authoritative allocation keys | M01_FOREIGN_SOURCE_REJECT; CONFIRMED_DEFECT |
| FSA-004 P0 | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:63 | alreadyConsumed rejected only alreadyAllocated branch; eligible branch recreates gain from same exhausted source | RESERVE_SPENT_SOURCE_REJECT; CONFIRMED_DEFECT |
| FSA-005 P0 | Include/Risk/HSBI_RiskGateResult.mqh:6 | NaN comparisons are false, most fields/limits have no finite/domain checks | RISK_NAN_REJECT,NF_GATE_UNKNOWN_LIMIT_REJECT; CONFIRMED_DEFECT |
| FSA-006 P0 | Include/Execution/HSBI_TransactionTypes.mqh:15 | NaN accumulated volume or outcome price/volume bypass abs(diff)>tolerance | TX_NAN_VOLUME_REJECT,OUTCOME_NAN_VOLUME_REJECT,OUTCOME_NAN_PRICE_REJECT; CONFIRMED_DEFECT |
| FSA-007 P0 | Include/Money/HSBI_AllocationLedgerTypes.mqh:7 | No nonnegative/finite bucket validation; committed full equality not distinguished from partial inequality | ALLOC_NEGATIVE_BUCKET_REJECT,ALLOC_COMMITTED_UNALLOCATED; CONFIRMED_DEFECT |
| FSA-008 P0 | Include/Money/HSBI_MoneyState.mqh:5 | Only >=0 bucket tests, ignores valid/revision/finiteness | MONEY_INVALID_FLAG_REV,MONEY_INFINITY; CONFIRMED_DEFECT |
| FSA-009 P0 | Include/Core/HSBI_Context.mqh:48 | Far count and slot role validation cover only far/core/trend/small, omit initial and new candidate slots | CONTEXT_TWO_FAR_OTHER_SLOT_REJECT,INVARIANT_DUAL_FAR_OTHER_SLOT_REJECT; CONFIRMED_DEFECT |
| FSA-010 P0 | Include/Planning/HSBI_NewFarSolver.mqh:119 | Proof identity overwritten from input; expected then copied from same proof; no independent deal-reconciliation record | M02_COPIED_FOREIGN_EXPECTED; CONFIRMED_DEFECT |
| FSA-011 P1 | Include/Planning/HSBI_GeometrySolver.mqh:32 | Core0 accepted and positive Core/Trend omit volumeMin | ZERO_CORE_MINLOT,BELOW_MIN_CORE; CONFIRMED_DEFECT |
| FSA-012 P1 | Include/Core/HSBI_StateMachine.mqh:5 | Normal topology stops at openingCore; generic reconcile route lacks explicit resume authority | FSM_CORE_TO_TREND,FSM_AUTO_RESUME_UNGUARDED; UNIMPLEMENTED_ORCHESTRATION |
| FSA-013 P1 | Include/Persistence/HSBI_PersistenceInterface.mqh:5 | Production SHA256/storage stub; no durable lock/commit/CAS/history load | PROPERTY-SNAPSHOT_BINDING,PROPERTY-REPLAY_IDENTITY; UNIMPLEMENTED_COMPONENT |
| FSA-014 P1 | Hybrid_Split_Big_Independent_EA.mq5:35 | OnTick only SubmitActionStub; no OnTradeTransaction/planning/scenario ingress | STATIC-CALL-GRAPH; UNIMPLEMENTED_COMPONENT |
| FSA-015 P1 | Include/Planning/HSBI_FutureSmallProofAggregator.mqh:50 | Max transition-loss level need not minimize Catch-Up margin | AGGREGATE_POSITIVE_VALID,CR09-EXTREMA; NORMATIVE_CONFLICT |
| FSA-016 P1 | Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:22 | minimum-safeN vs global risk/margin-first selection have different order | OBJECTIVE-NON_EQUIVALENCE; NORMATIVE_CONFLICT |
| FSA-017 P1 | Include/Planning/HSBI_FutureSmallSolver.mqh:89 | compares netBigVolume with priorBigGross | FS_BIG_GROSS_GROWTH_REJECT; CONFIRMED_DEFECT |
| FSA-018 P1 | Include/Planning/HSBI_FutureSmallSolver.mqh:12 | Finite prefix checks and boolean flags do not establish a uniform infinite-tail q law | BOUND_FINITE_PREFIX_NOT_GLOBAL_PROOF,PREFIX-NOT-TAIL; UNPROVEN_PROOF_OBLIGATION |
| FSA-019 P1 | Include/Money/HSBI_CostModel.mqh:18 | No cost basis/window/coverage identity to establish spread/buffer nonoverlap | COST-OVERLAP; NORMATIVE_UNCERTAINTY |
| FSA-020 P1 | Docs/03_FULL_SYSTEM_MANUAL_RU.md:9 | Multiple simultaneous same-symbol opposite positions require hedging semantics or a virtual-position design | ACCOUNT-MODE-NETTING; UNSPECIFIED_DOMAIN |
| FSA-026 P1 | Tests/Reference/hsbi_02b_r0h_native_harness.mq5:1 | No MetaEditor/MT5 native logs; Python/C++ not MQL proof | NATIVE-DISCOVERY; MISSING_ACCEPTANCE_EVIDENCE |
| FSA-027 P1 | Include/Persistence/HSBI_ExecutionJournal.mqh:27 | Duplicate lookup occurs before validating candidate body/currentEntryDigest binding | JOURNAL_ALTERED_BODY_NOT_NOOP; CONFIRMED_DEFECT |
| FSA-028 P1 | Include/Planning/HSBI_FutureSmallSolver.mqh:144 | Terminal flag means Far<=Vmin, not actual closure/affordability; terminalRouteAllowed input is unused | FS_MISSING_TERMINAL_ROUTE_REJECT; UNIMPLEMENTED_TERMINAL_PROOF |
| FSA-029 P1 | Include/Money/HSBI_BasketMoneyEvaluator.mqh:15 | Geometry permits Trend0; basket always calls positive-volume money/margin wrapper for allfour legs | TREND_ZERO_GEOMETRY_ACCEPTED,TREND_ZERO_BASKET_ACCEPTED; CONFIRMED_DEFECT |


Порог severity описывает потенциальный ущерб при использовании соответствующего пути, не активный доступ к счёту. Реестр включает confirmed local defects, normative conflicts, unimplemented components и proof/evidenceblockers; count не подменяет proofseverity. Все29 issue scopes в DEFECT_REGISTER, отдельные9 unverifiedrisks в COVERAGE/DEFECTS.

## 18.10. Что исправлять и проверять дальше

1. Утвердить точные source/body/status/codec/legacy/provenance boundaries для MinimalR1.1; resolve policy prerequisites без overexpanding всейстратегии. Native toolchain/acceptance обязателен; не autoapprove16decisions.
2. Отдельным заданием исправить economic identity; затем allocation immutable vector/phase/state/conservation и authoritative source/bucket/consumer/replay binding, включая spentsource. Не смешивать projections и actualavailable.
3. Устранить finite/domain/cardinality/outcome/revision gaps во всех обязательных public paths, доказать mandatory callers и отсутствие bypass. Не считать наличие необязательного guard защитой.
4. Реализовать независимые account/history/EA-origin/risk/margin/cost providers. Утвердить supported accountmode, currency/precision/rounding/costbasis и current policy assumptions.
5. Затем durable storage/journal/CAS/globalfunding/reconciliation; validatealteredreplay и crash/restart/concurrent events на реальном backend.
6. Исправить geometry/optionalleg/grossmetric/objective/CR09/tail/terminalclose proofs и проверить в nativeMQL5 с реальными calculation-only broker contexts.
7. Только потом отдельные fullscenario/FSM simulation/nativeeventintegration, затем явно разрешённые StrategyTester/demoevidence и отдельный liveapprovalgate.

Полная пофазная таблица fileallowlists/dependencies/tests/stop/rollback в REMEDIATION_ROADMAP. Ни один этап не запускается текущей публикацией.

## 18.11. Итоговое заключение

**SYSTEM_CRITICAL_CONTRADICTIONS_FOUND** — подтверждены фундаментальные source/accounting/guard несоответствия, а непротиворечивость и экономическая состоятельность всей торговой системы не установлены. Одновременно **SYSTEM_NOT_FULLY_VERIFIABLE** описывает предел полноты из-за отсутствующих execution/backend/native/provider components, но не отменяет отрицательные конкретные находки. Положительный full-system status не обоснован.

Ответы администратора:

1. Математика целиком правильной не признана: есть корректные условные identity и ошибочные/неполные проверки/definitions.
2. Все части фактически не взаимодействуют end-to-end; main не запускает cycle.
3. Ошибки в денежных validators/equality/binding, риск nonfinite и lot/gross/terminal consistency подтверждены в scoped source evidence.
4. Работать как в руководстве текущий EA не может: ключевые engines/providers отсутствуют.
5. Реализованы skeleton/DTO/pure calculators/validators, а не полноценное исполнение.
6. Scenarios/backend/fullreconciliation/funding/terminalclose/ActualMarginRisk integration остаются преимущественно спецификацией/моделями.
7. Adverse trend/gaps/costs/margin shortage/noevent/nohistory и partial/unknown execution могут сорвать/зависить recovery; гарантии completion/lossbound не установлены.
8. Исправления начинаются с identity/conservation/provenance/finiteguards, не с отправки ордеров.
9. Доказаны лишь перечисленные local algebra/fixture properties при предпосылках. Ни прибыльность, ни реальная whole-account conservation/exactly-once/native execution ими не доказаны.
10. Дальнейшее продвижение требует конкретного approvedscope, native environment, provider/backend и доказательного fullcycle тестирования.

## 18.12. Readiness и полнота доказательств

| Readiness | Status | Reason / evidence |
|---|---|---|
| DOCUMENTATION_READY | PARTIAL | Mainmanual/ownertexts есть, но конфликты/current policy/provider/runbook gaps; DOCUMENTATION_MAP |
| MATHEMATICS_READY | NO_FULL_SYSTEM_PROOF | 49families/137sites; zeroCore,gross,worstcase/tail problems; MATHEMATICS |
| ECONOMIC_MODEL_READY | NO | No profitability/lossbound/globalfunding; ECONOMIC_MODEL |
| PRODUCTION_READY | NO | No event/scenario/storage/provider lifecycle; CODE_REVIEW |
| NATIVE_TESTING_READY | HARNESSES_PREPARED_TOOLCHAIN_MISSING | MQL5compile/runtimeNOT_RUN; NATIVE_ENVIRONMENT |
| TRADING_LOGIC_READY | NO | Full FSM/scenarios unimplemented; TRADING_CYCLE |
| BROKER_DISPATCH_READY | NO | Intentionallydisabled; no execution/risk/provider acceptance |
| REAL_TRADING_READY | NO | All necessary gates/admin approval absent |


Coverage:74staticallyreviewed productionfiles,199definitions,51linesmanualfullread,31ownertextsread,133docsindexed. All historicalqualification appendices and279test scripts не fullyreverified;14families unverified; no fullnative/broker/durable execution. Therefore AUDIT_COMPLETENESS=PARTIAL, STAGE_COMPLETE=NO_PARTIAL_AUDIT. Это опубликованный частичный независимый отчёт с конкретным отрицательным вердиктом, не ложное заявление полного выполнения аудита. PublicationSHA/parity фиксируются после commit в окончательном ответе, не self-embedded в собственный commit.

ADMIN_APPROVAL_COMPLETE=NO
PRODUCTION_REMEDIATION_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
BROKER_DISPATCH_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
