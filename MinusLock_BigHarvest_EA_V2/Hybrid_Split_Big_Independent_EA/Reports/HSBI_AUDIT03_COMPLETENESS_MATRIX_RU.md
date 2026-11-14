# AUDIT03 COVERAGE-COMPLETION — прослеживаемость и незавершённые обязательства

База4761c66edc3343f353ca774df835eedb1787b818. Этот документ связывает результаты, но не создаёт конкурирующий реестр ошибок/улучшений. Единственные IDs — в ALL_ERRORS и ALL_IMPROVEMENTS. Детальная инвентаризация482 baseline-документов — [coverage](HSBI_AUDIT03_DOCUMENT_COVERAGE_RU.md),74 источника/199 lexical declarations — [source map](HSBI_AUDIT03_SOURCE_FUNCTION_MAP_RU.md).

## Contract → Formula → Source → Finding → Improvement → Approval

| Document / clause | Contract | Formula | Source implementation | Finding | Improvement | Approval dependency / remaining gap |
|---|---|---|---|---|---|---|
| Docs/04:9; Docs/25:5–17 | Active legs, floor/ceil, min/max/grid | F001–004/F048 | BrokerGrid:24–36; GeometrySolver:28–35; BasketMoneyEvaluator:15 | ERR-014/015/039/040 | IMP-002/007 | Optional Trend и grid origin требуют владельца |
| Docs/04:12; Docs/26:7 | Mirror favorable monetary slope | F005/F039/F051 | GeometrySolver:10–19 | ERR-037/046 | IMP-007/021 | Direction norm precedence; asymmetric valuation provider |
| Docs/04:21; Docs/27 | BigGross=C+T, не NetBig | F029/F030 | FutureSmallSolver:90 | ERR-020 | IMP-012 | Новая экономика не выбирается; проверить все relation callers |
| Docs/08:6; Docs/24 | Signed DealNet, disjoint projected costs | F007–009 | CostModel:13–18 | ERR-001/022 | IMP-001/014 | D-02/D-06, cost inventory/history |
| Docs/08:12–24; Docs/32 | Allocation conservation/vector | F012–016/F064 | AllocationLedgerTypes:6–10 | ERR-004/005/006 | IMP-003 | D-01/BALANCE mapping; committed exactness |
| Docs/08:15; Docs/31 | Immutable source and allocation | F017/F057 | EconomicLedgerTypes:6–12; AllocationLedgerTypes:8 | ERR-001–004 | IMP-001–003 | D-08, schema/codec/namespace/migration |
| Docs/32; R0F money contract | Source ledger + owner partition | F013–019/F053–056/F065 | ReserveAllocationTypes:15–35; ReserveCatchUpEvaluator:44–70 | ERR-007/008/033 | IMP-004/009 | D-07/global registry/durable/CAS |
| Docs/24:9; Docs/31; NEXT_STAGE02 money audit | Proof values bind evaluator scalars | F020–023/F060 | ReserveCatchUpEvaluator:24–74; NewFarSolver:121–127 | ERR-043/048 | IMP-004/010 | D-02/D-04; full NewFar caller injection не доказана |
| Docs/30:3–15 | Min all-level CatchUpMargin, scope | F023 | FutureSmallProofAggregator:44,50–52 | ERR-018 | IMP-010 | CR-09; one maxTransition index не all-level proof |
| Docs/13:9,20; R0F D-05 | Current/sticky/peak transition loss | F024–026 | Нет выбранного ordered-fill backend | ERR-035 | IMP-019 | Явный выбор D-05/reset/history |
| Docs/13:12–14 | Prefix exposure/margin/cap | F030/F052 | Scenarios DTO; полного handler нет | ERR-041 | IMP-022 | D-05/Margin provider; actual partials |
| Docs/14; Docs/28; Docs/29 | Selection ≠ actual promotion | F027/F028/F047/F060 | NewFarSolver:108–151; NewFarCandidate:35 | ERR-013/019/045 | IMP-001/011 | Objective priority и independent residual provider |
| Docs/04:33–36; Docs/27 | Uniform tail и terminal close | F037/F038/F058 | FutureSmallSolver:144–149 | ERR-021/031/032 | IMP-013 | Terminal policy; finite-prefix не uniform proof |
| Docs/15 | Finite risk/account margin | F026/F031–033/F036 | RiskGateResult:6; NewFarGateTypes; BrokerMarginModel | ERR-009/034/038 | IMP-005/015/021 | MQL/admitted account/risk domains |
| Docs/07; HSB.2C intent | Closed DTO enum and actual outcome | F036/F046/F062 | ExecutionIntent:28–40; OwnershipGuardTypes:8; ExternalOutcome:25–30 | ERR-010/024/049 | IMP-005/008/016 | Typed domain, mandatory caller и native future acceptance |
| Docs/16; HSB.2C journal | Immutable journal before replay status | F057/F065 | ExecutionJournal:21–29 | ERR-017/025/030 | IMP-009 | D-07 durable/concurrency не доказаны |
| Docs/16; HSB.2C snapshot | completed count/body meaning | F066 | ExecutionStateSnapshot:27–40 | ERR-050 | IMP-009 | SNAP schema semantics; условный defect не universal source claim |
| R12A normative decisions:19–31 | Full settlement conjunction | F062/F063 | Исторические qualification evaluators, не production backend | ERR-010/016/028 (scope links) | IMP-008/017 | Все caller/predicate implementations ещё не сопоставлены |
| Docs/09:20; Docs/12:7–15 | Economic cycle vs recovery metric | F010/F011/F034/F035/F050 | MoneyTypes:7–9; FinalCloseTypes DTO | ERR-036/044 | IMP-020 | Basis/threshold eligibility и actual zero proof |
| Docs/02; Context | Unique physical positions/one Far | F030/F061 | Context:19–24,48–53 | ERR-012/023 | IMP-006/015 | Hedging/account model и глобальный position registry |
| Docs/06; Docs/07; main | Normative lifecycle vs no-trade skeleton | F057/F060 | StateMachine:5–7; main:19–44 | ERR-016/028 | IMP-008/017 | Full Event×State coverage незавершено |
| R0D/R0F/R0G numeric proposals | Settled exact vs raw codec/domain | F041–043/F049 | Production double, native codec не принят | ERR-003/040 | IMP-002/018 | NUM-EXACT/DOMAIN/CODEC/MQL; тесты запрещены текущим scope |
| Full-cycle / market assertions | Bounded volume ≠ bounded loss/profit/time | F058/F059/F061/F065 | Полного торгового lifecycle нет | ERR-032/038/042 | IMP-013/021 | См. GLOBAL_PROPERTIES; guarantees не доказаны |

Короткие file names в Source колонке разрешаются однозначно в [полной source map](HSBI_AUDIT03_SOURCE_FUNCTION_MAP_RU.md), Documents — в [inventory](HSBI_AUDIT03_DOCUMENT_COVERAGE_RU.md). Числа после двоеточия — строки неизменного baseline source. Диапазоны семейств — навигация, не число исполненных assertions.

## Шестнадцать нерешённых решений

Все AWAITING_ADMIN_APPROVAL, AdministratorDecision не заполняется. Источники прочитаны целиком: Reports/NEXT_STAGE_02B_R0F_ADMIN_APPROVAL_PACKAGE_RU.md:1–314, HSBI_FULL_SYSTEM_AUDIT_02_ADMIN_DECISIONS_RU.md:1–243, HSBI_DG01_ADMIN_DECISION_BALLOT_RU.md:1–134; R0G/R0H ballots не подписаны. Readiness не approval.

| ID | Что именно решить | Главная зависимость / evidence | Связь с текущими findings |
|---|---|---|---|
| D-01 | OriginalGrant=C+R+Free, RemainingGross=R+Free | D-02 и versioned balance schema | ERR-006/033 |
| D-02 | Шесть денежных стадий, без implicit conversion | D-08 и independent history | ERR-022/033/048 |
| D-03 | Small held отдельно либо approved transfer | D-01/D-08, source attribution | ERR-047 |
| D-04 | Absolute vs separately based incremental | D-02, basis/volume/window | ERR-043/048 |
| D-05 | Current/sticky/peak, prefix/reset/restart | D-02/D-08, ordered fills | ERR-035/041 |
| D-06 | Каждый applicable CostID ровно один раз | D-02/D-08, broker costs/basis | ERR-022 |
| D-07 | Immutable replay и receipt/authority priority | D-08, journal/backend | ERR-017/030/033 |
| D-08 | Logical source namespace и immutable payload | Independent broker/EA-origin authorities | ERR-001/002/013 |
| CR-09 | All-required-level vs explicitly single preview | D-01/02/04/06/SNAP/global funding | ERR-018/043 |
| NUM-EXACT-1 | Settled minor units vs bounded fixed point | D-02, posting policy | ERR-003/040 |
| NUM-DOMAIN-1 | Допустимые scale/currency/ranges | NUM-EXACT/MQL, intermediate bounds | ERR-040 |
| NUM-CODEC | F64Z или T17Z, zero/version policy | Native golden acceptance; не financial rounding | ERR-003 |
| SNAP-FIXTURE-1 | Content receipt, clock и full schema | D-08, snapshot authority | ERR-017/024/050 |
| FUNDING-GLOBAL-ATTRIBUTION | Source/account-wide inventory и ordering | D-01/02/07/08, durable backend | ERR-033 |
| MQL-DOMAIN | Native long/ulong/double/UTF8 semantics | Реальные нативные evidence в отдельном разрешённом этапе | ERR-029/040 |
| BALANCE-SCHEMA-MAPPING | Explicit legacy Remaining adapter/quarantine | D-01/02/08, known units/owner/history | ERR-006/033 |

Историческая NUM-CODEC dependency на NUM-EXACT описывает общую архитектуру, но raw identity codec и settled арифметика не одно требование. Minimal R1.1 должен отдельно уточнять необходимое подмножество; ни это уточнение, ни source-local equality не устраняют весь global funding defect. No new approval generated.

## Незавершённый охват — точные критерии

1. Полный просмотр 306 строк inventory со статусом NOT_REVIEWED и двух PARTIAL файлов (точные paths уже приведены, не заменены общим «остальное»). Среди содержательно обязательных кандидатов: `Tests/Contracts/HSB_2E_R4_R9_R4A_R12_PREDICATE_CONTRACT.json`, `...R12_PREDICATE_REGISTRY.json`, `...R10_SCHEMA.json`, `...R9_SCHEMA.json`, `NEXT_STAGE_02B_R0E_C2_DTO_SCHEMAS.json`, ранние/поздние verification matrices; исторические Reports тоже требуют applicability classification.
2. Тематический index199 function declarations не является индивидуальным доказательством199 guards. Для каждого semantic clause надо завершить mandatory caller→normative field→proof boundary, включая составные guards и source-only helpers. FULL_SOURCE_TEXT_READ=YES, FULL_FUNCTION_CONTRACT_MAP=NO.
3. У старых60 formula cards ещё не заполнены все15 требуемых полей индивидуально. Групповые domain/direction/cost/partial уточнения помогают, но не закрывают это требование. Новые6 семейств не объявляются исчерпывающим итоговым каталогом всех применимых документов.
4. Фазовая FSM таблица не full Event×State×Partial×Timeout×Restart relation. Отсутствие executable handler установлено, полная нормативная relation с точными events ещё не закончена.
5. ERR-020/046 рассмотрены в primary Docs и source, но полный перечень повторов в непрочитанных historical Reports/oracles ещё не установлен.

Все эти gaps относятся к **полноте аудита**, в отличие от недоказанной прибыльности/брокерской подлинности, которые могут оставаться UNVERIFIED даже после будущего COMPLETE. Данные доступны; отсутствие MetaEditor не причина непрочитанной документации. Настоящий результат — существенное продолжение, **не выполнение критерия полного завершения задания**.

AUDIT_COMPLETENESS=PARTIAL
GLOBAL_MONEY_CONSERVATION_PROVEN=NO
GLOBAL_LOSS_BOUND_PROVEN=NO
FULL_FSM_VERIFIED=NO
FULL_TRADING_CYCLE_VERIFIED=NO
CYCLE_TERMINATION_PROVEN=NO
PROFITABILITY_GUARANTEED=NO
PRODUCTION_REMEDIATION_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
BROKER_DISPATCH_ALLOWED=NO
REAL_TRADING_ALLOWED=NO

## FINAL-CLOSURE — текущий незавершённый срез

| Обязательство | Фактический scope | Остаток |
|---|---|---|
| Baseline / preservation | exact base b4d8f1e; базовый inventory1528 | повторная финальная сверка перед публикацией |
| Documents | baseline485; FULL242; exact duplicate5; PARTIAL0; NOT_REVIEWED238 | все238 перечислены в текущем coverage table; authority UNKNOWN у ряда перенесённых FULL также требует индивидуального решения |
| Functions | 43 индивидуальные20-field cards из199; source body и static callsites |156 функций; полный atomic guard inventory |
| Formula cards |66 по15 полей; math47 valid/3 false/2 contradictory/6 unverified/8 undefined | полный authority/caller dependency crosswalk ещё не закрыт |
| FSM |9 normative rule cards,20 analytical cases,140 allowed source topology pairs | общий normative relation не определён; priority/phase/outcome mapping gaps; полного execution нет |
| Global properties |5 индивидуальных10-field analyses; conditional proofs/countermodels | global broker/runtime/concurrent guarantees не доказаны |
| Errors / improvements |50 ERR и22 IMP сохранены, ERR031 уточнён без нового ID | полная новая индивидуальная20/15-field нормализация ещё не завершена |
| Decisions |16 pending,0 approved | сквозная новая индивидуальная traceability для всех решений ещё не завершена |
| Quality | структурная сверка66 formula tables | полная link/line/field проверка всех обновлённых карточек ещё не завершена |
| Publication | commit/push текущего продолжения не выполнялись | только после условий задания и без branch-protection bypass |

AUDIT_COMPLETENESS=PARTIAL. Наличие всех названий выходных файлов не равно выполнению всех обязательств. Основной остаток — содержательное чтение и индивидуальный semantic crosswalk, не проблема доступа к файлам. Production и исторические evidence не исправлялись.

## R2 — индивидуальное рассмотрение16 административных решений

Источник proposals: Tests/Contracts/NEXT_STAGE_02B_R0F_ADMIN_DECISIONS.json:1–338, прочитан целиком. Это не присвоение normative authority. Все16 ниже AWAITING_ADMIN_APPROVAL, AdministratorDecision пуст; approvals0. Историческая D03 file привязка уточнена по actual BasketMoneyEvaluator:17.

### Decision D-01

| Поле | Индивидуальный вывод |
|---|---|
| Что решить | Grant/Consumed/Reserved/Free schema |
| Варианты | G=C+R+F,Remainder=R+F; alternativelegacyread-only |
| Математические последствия | 50=10+15+25, Remaining40неFree25 |
| ERR / IMP | ERR005/006/007/033/048; IMP003/004 |
| Будущие production модули | MoneyState/AllocationLedger/ReserveAllocation/ReserveCatchUp |
| Отсутствующие доказательства | Независимые grant/journal/owner/precision facts |
| Блокер | Без schema freeze нельзя silent rename Remaining в Free |
| ApprovalStatus | AWAITING_ADMIN_APPROVAL; отдельного решения владельца нет |

### Decision D-02

| Поле | Индивидуальный вывод |
|---|---|
| Что решить | Moneykind/authority boundary |
| Варианты | Запрет implicitprojected→actual→available; alternative planning-onlyviews |
| Математические последствия | Projected100 без закрытыхdealsнеgrant100; unknownhistoryне0 |
| ERR / IMP | ERR008/013/022/033/048; IMP001/004/014 |
| Будущие production модули | EconomicLedger/LevelMoney/ReserveCatchUp/RuntimeDecisionValidator |
| Отсутствующие доказательства | Actual brokerreceipts/completehistory/reconciliation |
| Блокер | Не generic boolruntimeConfirmed; required typedprovider |
| ApprovalStatus | AWAITING_ADMIN_APPROVAL; отдельного решения владельца нет |

### Decision D-03

| Поле | Индивидуальный вывод |
|---|---|
| Что решить | Big/Small attribution |
| Варианты | Small residualheld; alternative отдельноapproved debit/credit transfer |
| Математические последствия | Core0 Trend0 Small10→BigReserve0; переносне создаётприбыль |
| ERR / IMP | ERR022/033/047; IMP004/014 |
| Будущие production модули | BasketMoneyEvaluator:17 и downstream ReserveCatchUp; не LevelMoney scalarwrapper |
| Отсутствующие доказательства | Source role/cost attribution; immutable transfer receipts еслиB |
| Блокер | Решитьpolicyдоизменения reserveGain; текущийtransferне реализован |
| ApprovalStatus | AWAITING_ADMIN_APPROVAL; отдельного решения владельца нет |

### Decision D-04

| Поле | Индивидуальный вывод |
|---|---|
| Что решить | Far loss basis |
| Варианты | Absolute close-now; incremental separatediagnostic приprovedbaseline |
| Математические последствия | Abs50 baseline40 delta10 Reserve30 покрываетdelta,неabsolute |
| ERR / IMP | ERR018/043/048; IMP010 |
| Будущие production модули | BasketMoneyEvaluator/CatchUpModel/ReserveCatchUp/FutureSmallAggregator |
| Отсутствующие доказательства | Actual residual/quote/costbasis/lineage |
| Блокер | Выбратьbasis;не выдаватьprojectedcoverageзаfill guarantee |
| ApprovalStatus | AWAITING_ADMIN_APPROVAL; отдельного решения владельца нет |

### Decision D-05

| Поле | Индивидуальный вывод |
|---|---|
| Что решить | Current/sticky/peaktransitionpolicy |
| Варианты | A currentloss;B persistentbreach;C maxhistoricalLoss; choiceНЕСДЕЛАН |
| Математические последствия | -15,+100 cap12: послеfill1 A15/Btrue/C15;послеfill2 A0/Btrue/C15 |
| ERR / IMP | ERR010/035/041; IMP005/019/022 |
| Будущие production модули | TransactionTypes/transitionprovider/NewFarGates/scenarioSmallTransition |
| Отсутствующие доказательства | Independent orderedbatchfills; durablebreach/resethistoryдляB/C |
| Блокер | Нужныexplicitreset/restart/order/cap rules;автовыборзапрещён |
| ApprovalStatus | AWAITING_ADMIN_APPROVAL; отдельного решения владельца нет |

### Decision D-06

| Поле | Индивидуальный вывод |
|---|---|
| Что решить | Costcoverage/basis |
| Варианты | КаждыйrequiredCostID ровноодинраз;alternativebufferсprovedcoverage |
| Математические последствия | Commission−2 ужевNet50 не subtractagainдо48;unknownslippageне0 |
| ERR / IMP | ERR022/034/048; IMP014/015 |
| Будущие production модули | CostModel/BrokerMoneyModel/BasketMoneyEvaluator/CatchUp |
| Отсутствующие доказательства | Costinventory/basis/window/fees/spread/slippage brokerdata |
| Блокер | Размерыbuffersневыбиратьпоfixture; global overlap proof отсутствует |
| ApprovalStatus | AWAITING_ADMIN_APPROVAL; отдельного решения владельца нет |

### Decision D-07

| Поле | Индивидуальный вывод |
|---|---|
| Что решить | Replayauthority/durableexactlyonce |
| Варианты | Conflict-firstsource reconciliation versus separatelyapprovedreceipt-first |
| Математические последствия | Grant50 debit10→40;exactevent→40;changed11conflict |
| ERR / IMP | ERR007/017/025/030/033; IMP004/009 |
| Будущие production модули | ExecutionJournal/ExecutionStateSnapshot/ReserveAllocation/Persistencebackend |
| Отсутствующие доказательства | Immutablecompletejournal; atomiccommit/CAS/crash/concurrency evidence |
| Блокер | LocalNOOPнеdurable/concurrenttheorem;orderpolicyдолжнабытьявной |
| ApprovalStatus | AWAITING_ADMIN_APPROVAL; отдельного решения владельца нет |

### Decision D-08

| Поле | Индивидуальный вывод |
|---|---|
| Что решить | Logical source independent provenance |
| Варианты | Broker/Server/Account/Deal key +immutablebody;alternative independentverifiedreceipt |
| Математические последствия | Profit50/C0 vs60/C−10 sameNet50 differentpayload→CONFLICT |
| ERR / IMP | ERR001/002/013/026/033/049; IMP001/002 |
| Будущие production модули | EconomicLedger/Identifiers/MoneyProofIdentity/NewFar/Runtimevalidators |
| Отсутствующие доказательства | Brokerfacts+EA-origin journal association |
| Блокер | Copiedexpectedнеauthority; namespace/equalitylocalAPIнеfull fundingfix |
| ApprovalStatus | AWAITING_ADMIN_APPROVAL; отдельного решения владельца нет |

### Decision CR-09

| Поле | Индивидуальный вывод |
|---|---|
| Что решить | AllrequiredlevelCatchUp |
| Варианты | min_i Margin_i>0;alternativesingle-leveltypedresult |
| Математические последствия | MaxTransition level margin9, другойmargin−11: fullproofmustreject |
| ERR / IMP | ERR018/043/048; IMP010 |
| Будущие production модули | FutureSmallAggregator/NewFarSolver/ReserveCatchUp |
| Отсутствующие доказательства | Requiredlevelset +snapshots/reserve/risk/margin/realcosts |
| Блокер | Одинreserveдопустимвальтернативныхforecasts; последовательныйspendнуждаетсявdebit |
| ApprovalStatus | AWAITING_ADMIN_APPROVAL; отдельного решения владельца нет |

### Decision NUM-EXACT-1

| Поле | Индивидуальный вывод |
|---|---|
| Что решить | Settled representation |
| Варианты | Integer minorunits or checkedfixedpoint; referenceFractionseparate |
| Математические последствия | 1e28−.010−(1e28−.005)=−.005 точновreference;binary64можетскрыть |
| ERR / IMP | ERR003/040/051; IMP002/023 |
| Будущие production модули | MoneyTypes/AllocationLedger/codec/futuregridhelpers |
| Отсутствующие доказательства | Independentpostedcurrency/precisionnativevectors |
| Блокер | Нельзяперенестиreference-domainвMQL5автоматически |
| ApprovalStatus | AWAITING_ADMIN_APPROVAL; отдельного решения владельца нет |

### Decision NUM-DOMAIN-1

| Поле | Индивидуальный вывод |
|---|---|
| Что решить | Supported numeric range/intermediates |
| Варианты | Explicitboundednativeprofile or approvedwiderarithmetic |
| Математические последствия | 1e28dollars→1e30cents внеint64;final0не оправдываетintermediateoverflow |
| ERR / IMP | ERR025/040/051; IMP002/005/023 |
| Будущие production модули | BrokerGrid/NewFarSolver/moneycodec/revisionguards |
| Отсутствующие доказательства | Nativecheckedarithmeticandreceipt-domain facts |
| Блокер | НеиспользоватьширокиеPythonintsкакnativeproof;rejectunsupported |
| ApprovalStatus | AWAITING_ADMIN_APPROVAL; отдельного решения владельца нет |

### Decision NUM-CODEC

| Поле | Индивидуальный вывод |
|---|---|
| Что решить | Canonical immutable encoding |
| Варианты | F64Zfinitebinary64 or T17Zcanonical17text;noneapproved |
| Математические последствия | raw0.1 bits3fb999999999999a; bool/int/string различимы;±0policyexplicit |
| ERR / IMP | ERR003/026/040; IMP002/018 |
| Будущие production модули | EconomicLedger/identityserialization/approvedcodecfile |
| Отсутствующие доказательства | Independentgoldens/UTF8/long/ulong/nativecompile+runtime |
| Блокер | Recommendationнеapproval; codecrepresentationнеfinancialrounding |
| ApprovalStatus | AWAITING_ADMIN_APPROVAL; отдельного решения владельца нет |

### Decision SNAP-FIXTURE-1

| Поле | Индивидуальный вывод |
|---|---|
| Что решить | Independent snapshotcontentbinding |
| Варианты | Versionedcontentreceipt;alternativeID-onlylimitedattestation |
| Математические последствия | SameID3+changedfingerprint conflict; selfrecomputedreceipt неauthority |
| ERR / IMP | ERR013/017/024/026/050; IMP009/016/017 |
| Будущие production модули | ControlPrices/ExecutionStateSnapshot/RuntimeRestartValidator |
| Отсутствующие доказательства | Clockauthority/contentreceipts/journalbinding |
| Блокер | Freshflag/checksumнеactual brokertruth; recoveryненоваяauthorization |
| ApprovalStatus | AWAITING_ADMIN_APPROVAL; отдельного решения владельца нет |

### Decision FUNDING-GLOBAL-ATTRIBUTION

| Поле | Индивидуальный вывод |
|---|---|
| Что решить | Global economic source/debitregistry |
| Варианты | Globalcompleteattribution;currentlysource-localscopeonly |
| Математические последствия | source50 grants40+20 invalid;unseenaccountdebit30 breaksfree50claim |
| ERR / IMP | ERR007/008/017/033/047/048; IMP004/009 |
| Будущие production модули | Globalprovider/ledger/backend иconsumers;неonefilefix |
| Отсутствующие доказательства | Allaccountflows/manualdeals,atomicdurablereceipts |
| Блокер | Source-localbalanceнеaccountfree;backendещёUNPROVEN |
| ApprovalStatus | AWAITING_ADMIN_APPROVAL; отдельного решения владельца нет |

### Decision MQL-DOMAIN

| Поле | Индивидуальный вывод |
|---|---|
| Что решить | Actual long/ulong/double/stringdomain |
| Варианты | Checkednativeprofile or separatelyapprovedwideradapter |
| Математические последствия | LONG_MIN·−1/MAX+1 invalid;ulong>2^53 неserializeviadouble |
| ERR / IMP | ERR025/029/040/051; IMP002/018/023 |
| Будущие production модули | EconomicLedger/BrokerGrid/NewFarSolver/codec |
| Отсутствующие доказательства | MetaEditorcompile/nativevectors; сейчасNOT_RUNпоскоупу |
| Блокер | NativecompatibilityнеподменятьC++/Python; exactfieldlimitsrequired |
| ApprovalStatus | AWAITING_ADMIN_APPROVAL; отдельного решения владельца нет |

### Decision BALANCE-SCHEMA-MAPPING

| Поле | Индивидуальный вывод |
|---|---|
| Что решить | Legacy balance migration |
| Варианты | Versionedadapter iffactscomplete;elselegacyread-only/quarantine |
| Математические последствия | G50 C10 Remaining40 R15→Free25; unknownowner/currency→UNAVAILABLE |
| ERR / IMP | ERR005/006/007/033/048; IMP003/004/009 |
| Будущие production модули | MoneyState/AllocationLedger/ReserveAllocation/recoveryadapters |
| Отсутствующие доказательства | Oldschema/owner/currency/precision/historyreceipts |
| Блокер | Нельзяподставитьcurrentaccountкакmissinghistoricowner |
| ApprovalStatus | AWAITING_ADMIN_APPROVAL; отдельного решения владельца нет |

Порядок зависимости не разрешение implementation. Local Economic Identity может быть отдельно ограничен equality/namespace API, но full remediation требует migration/callers/provider/native acceptance. Положительная документационная готовность не R1_1_START_ALLOWED.

## R2 — текущий остаток и границы завершённого

| Обязательство | Фактический результат | Точный остаток |
|---|---|---|
| Исходные материалы |12 прежних изменений сохранены, SHA256 вR2_WIP;1515readonly+74production blob/mode match | Финальная повторная сверка передпубликацией |
| Документы |244FULL+5exactduplicate;0PARTIAL;236NOT_REVIEWED | Все236строк NOT_REVIEWED текущей485-rowтаблицы DOCUMENT_COVERAGE; UNKNOWN_AUTHORITY переносовтакженеодобрены |
| Функции |199declarations/199uniqueFunctionIDs/198names;43сохранённые+156новыекарты | Полнаяnative/dynamic reachability невыполнялась; нормативныйmandatoryguardinventory ещёнеполон |
| Формулы |66×15полей;66IDsсопоставленыbaseline, изменены толькоF039/F041 | Полнаясвязь со236непрочитаннымидокументаминеобъявлена завершённой |
| Critical recheck |ERR020/041/046/048/049/050 повторно scoped; новаяERR051 | У всех6ещёоткрытоhistoricalmachinecontract покрытие; этоявноуказановкарточках |
| Guards |16groups+10localTXrows; missingprogressguard ERR051 | Полныйнепересекающийсяnormativeinventory и все publicboundary proof, анеподсчётif |
| FSM |9rulecards22fields/20analyticalcases;140topologypairs | Normativephase/outcome/severity priorities ипереченьspecificgapsнеполны; handlersнеimplemented |
| Admin |16individual8fieldcards, всеAWAITING_ADMIN_APPROVAL | Решениевладельца отсутствует;нетавтоутверждения |
| Реестры |51ERR/23IMP, P0=14/P1=32/P2=5 | Полныйqualityaudit всехстарыхиновообновлённыхсвязейещёнезавершён |
| Публикация |CommitNO,PushNO,BypassNO | Критерииполногоаудитанедостигнуты; защитаGitHubнеобходится |

AUDIT_COMPLETENESS=PARTIAL. Чтение236конкретныхфайловнеподменяетсяновымиfunctioncards. Наличие199картнеproofполнойсистемы. НетзаявленияENVIRONMENT_BLOCKED: оставшиесяработысодержательные, неошибкаshell.


## R3 — конкретные новые цепочки прослеживаемости

| Document → Clause | Formula | Function | Guard | Caller | FSM transition | ERR → IMP | Decision / proof status |
|---|---|---|---|---|---|---|---|
| R0A_NORMATIVE_MATRIX.D08.SourceDealKey vsR0G_IDENTITY_MATRIX.SourceKey | F017/F041/F057/F060/F062 | Economic.BuildSourceDealKey/SameEconomicRecord | A03-G001..004;fullnamespaceproviderMISSING | NO_PRODUCTION_CALLER_FOUND дляfunding classifier | Newconfirmedsource→grant NOT_IMPLEMENTED | ERR001/002/033→IMP001/002/017/018 | D02/D08/NUM-CODEC/MQL;ADMIN_DECISION_REQUIRED; schema не новыйsource |
| AUDIT01_INVARIANT_MATRIX.NO_FALSE_NOOPnegative | F007/F017/F057/F060 | abstractpropertyoracle,productionSameEconomicRecord:9 отдельно | Component-sum иimmutableequalityразныеguards | HistoricalfixtureнеpublicEAcaller | NOT_APPLICABLE: fixtureнеFSMaction | ERR027→IMP017 | VERIFIED fixturemultiplecause; wholeproductionproofUNVERIFIED |
| Docs06:6,9,12,18,21+Docs07:15,18,21,24 | F024–026/F036/F053/F057 | StateMachine/Transaction/Runtimepurehelpers | TX01..10,GRD001..047,SG01..10 | 3admissionpureedgesmapped,financialorchestratorMISSING | Normative relation CONFLICTING/OPEN_DOMAIN | ERR013/016/017/028/030→IMP008/009/014/018 | ADMIN_DECISION_REQUIRED;140pairsне140handlers |
| Tests/Staticfsm/lifecycle/persistenceJSON | F036/F053/F057/F060 | Reference qualification;actualsourcecomparisonseparate | Historicalflagsnotauthoritativeprovider | NOT_IMPLEMENTED financialcaller | Historical16/18relationsнеclosedcurrentFSM | ERR017/027/028→IMP009/017/018 | SUPERSEDED/REFERENCE_ONLY;individualreadsrecorded |
| DocsHSB2DIntegration:3–5 | F007/F024–026/F036/F060 | ValidateRuntimeDecisionContext:6–29 |47individuallylocatedlocalconditions | Barrier7/Restart16/directhelper | requiredNextState=RECONCILING result,notFSMapply | ERR013/016/033/048/049→IMP005/009/014/018 | VERIFIED_LOCAL;independence/callerfinancialscopeINCOMPLETE |

Это добавленныеиндивидуальныецепочки,неполнаяматрицавсехnormclauses. Остатоктеперьсодержитточныепути(coverage+WIP),дополнительно46StaticJSON;AUDIT_COMPLETENESS=PARTIALдонезавершённогочтенияиcensus. Наличие199/66карточекнеубираетэтотостаток.

## R4 — промежуточный snapshot для audit-ветки

Текущее чтение:531 документов=463 FULL+5 exact duplicate+63 NOT_REVIEWED+0 PARTIAL. Увеличение denominator на46 обосновано дополнительными Tests/Static JSON в coverage; исходные485 сохранены. Функции199/199 и формулы66/66 сохраняются. Индивидуальные GRD001–073 не полный нормативный census; global mandatory caller denominator ещё не закрыт. FSM gaps10 зарегистрированы, но полный clause crosswalk остаётся незавершённым. AUDIT_COMPLETENESS=PARTIAL. Публикация audit snapshot не merge work и не разрешение production. См. [R4 publication checkpoint](HSBI_AUDIT03_R4_GITHUB_PUBLICATION_RU.md).

## R4 — проверенный remote snapshot и текущий остаток

Первый snapshot реально размещён в GitHub: commit `f3090a5aedd71510f38afd265ac6d7d9b56b63a2`, audit-ветка `audit/hsbi-audit03-github-closure-r4`; work неизменён. Проверены HTTP200 commit/compare/final verdict и SHA256 всех16 remote raw files. Draft PR и обязательная API verification заблокированы сетевым CONNECT403 к api.github.com; PR NOT_CREATED, protection/CI/CodeScanning NOT_VERIFIED. Поэтому строгий GITHUB_PUBLICATION_COMPLETE пока NO, несмотря на доказанный обычный push. Подробные URL, hashes и ошибки — [R4 publication report](HSBI_AUDIT03_R4_GITHUB_PUBLICATION_RU.md).

Текущее покрытие531=472 FULL+5duplicate+54NOT_REVIEWED+0PARTIAL;199 карт/66формул/73GRD/51ERR/23IMP/16pending approvals. Полнота document/guard/caller/FSM исследования не достигнута: AUDIT_COMPLETENESS=PARTIAL. TESTS_EXECUTED_BY_CODEX=NO; MQL5_COMPILE/MQL5_NATIVE_TESTS=NOT_RUN; все production/trading permissions=NO.

## R6 — реестр16 решений и прослеживаемость financial boundaries

Все16canonicalIDs сохранены; DG01DisplayOrdinalD09..16непереименование. Статус каждойстроки AWAITING_ADMIN_APPROVAL. Альтернативы здесь предложения; native/provider/backend доказательства отсутствуют,а не предполагаются. Приоритет1: identity/domain/authority доисточников;2: policy/metrics доscenariointegration;3: globalattribution/migration послеownerfreeze. Эти приоритеты неразрешениеimplementation. Полные варианты/математическиеоснования/миграционные риски в прочитанных R0F/DG01decision matrices и существующем ballot; историческая подписьAPPROVED безscope/provenance неapprovalэтихпредложений.

| Decision | Formula suffixes | Existing GRD suffixes | Caller/FSM boundary | ERR suffixes | IMP suffixes | Alternatives / conflict | Counterexample / risk | Priority | Status |
|---|---|---|---|---|---|---|---|---:|---|
| D-01 | F012–016/F053–056/F064 | 051/054/058 | R6-B02/B15; Allocation/SG07 | 006/033 | 003/004 | Grant vs Gross/Free; partialPREPARED vs fullCOMMITTED | G50,C10,R15,F25→Gross40,Free25; wrongFree40overspends15 | 1 | AWAITING_ADMIN_APPROVAL |
| D-02 | F007–010/F060 | 026/037/055/070 | B01/B07; FinalClose/SG07 | 022/033/044/048 | 004/020 | Six monetary domains; no implicit projected→actual | Projected100,nohistory→UNAVAILABLE;actual0 doesnotgrant100 | 1 | AWAITING_ADMIN_APPROVAL |
| D-03 | F007/F012/F018 | 055/062/070 | B01/B02; Allocation | 047 | 004/014 | Small residual vs separately approved transfer | Core0Trend0Small10→BigReserve0 candidate | 2 | AWAITING_ADMIN_APPROVAL |
| D-04 | F020–023 | 035/063/071/073 | B03; CatchUp | 018/043 | 010 | Absolute gate vs independently baselined incremental | loss50baseline40Reserve30:incremental10covered,absolute50not | 2 | AWAITING_ADMIN_APPROVAL |
| D-05 | F024–026/F052 | 028/039; TX01–10 aliases | B06/B16; SmallTransition/SG05/06/07 | 035/041 | 019/022 | Acurrent/Bsticky/Cpeak; ordered prefix/reset | fills−15,+100,cap12:A15→0,Btrue→true,C15→15 | 2 | AWAITING_ADMIN_APPROVAL |
| D-06 | F008/009/F011 | 012/026/037 | B07/B08; FinalClose/SG08 | 022/034 | 014/015 | Independent cost coverage vs shared budget map | Commission−2alreadyNet8,subtractagain→6doublecount | 2 | AWAITING_ADMIN_APPROVAL |
| D-07 | F015/F018/F057/F065 | 043/045/060/061/065/066 | B11/B12/B13/B18; SG07 | 017/030/033 | 004/009 | Authority/replay priority; durableCAS vs localidempotency | twoallocations30+30 source50; eachlocal30doesnotcapglobal60 | 1 | AWAITING_ADMIN_APPROVAL |
| D-08 | F017/F019/F060 | 003–008/018–021/034/035/044/049 | B01/B14; NewFar/SG07 | 001/002/013/048 | 001/006 | Independent source/history and EA-origin journal | profit50commission0 vs60/−10 samekey→CONFLICT | 1 | AWAITING_ADMIN_APPROVAL |
| CR-09 | F006/F022/F023 | 023/024/032/072/073 | B03/B04; CatchUp | 018 | 010 | ALL_LEVEL vs explicit SINGLE_LEVEL | T1=10,m1=9;T2=5,m2=−11:argmaxTnotminmargin | 2 | AWAITING_ADMIN_APPROVAL |
| NUM-EXACT-1 | F041/F043/F049/F064 | 056/068 and numericpublicAPIs not fullymapped | B19; allmoney | 040 | 002/005 | Settled minor units vs checkedwide/rational | 1e28−.01−.01 requires exact decrement.02 | 1 | AWAITING_ADMIN_APPROVAL |
| NUM-DOMAIN-1 | F036/F041/F043 | 056/068/071; domainextensionpending | B19; allnumeric | 009/025/026/040/051 | 002/005/023 | Bounded range/scale/intermediates vs widerrepresentation | MAX+MAX−MAX−MAX=0finaldoesnotlicenseoverflow | 1 | AWAITING_ADMIN_APPROVAL |
| NUM-CODEC | F017/F042/F057 | 046/047/049 | B14/B19; replay/recovery | 003/040 | 001/002 | F64Z candidate vs T17Z; nativeacceptance separate | ulong2^53+1 mustnotpassdouble; zeroZpolicy explicit | 1 | AWAITING_ADMIN_APPROVAL |
| SNAP-FIXTURE-1 | F036/F042/F066 | 009–012/046/047 | B10/B12; SG07 | 017/024/050 | 009/016 | Independent contentreceipt/clock vs scopedattestation | sameIDalteredcontent≠sameconfirmed snapshot | 1 | AWAITING_ADMIN_APPROVAL |
| FUNDING-GLOBAL-ATTRIBUTION | F018/F019/F034/F035 | 042/054/067/069 | B02/B15; Allocation/SG07 | 007/008/033/048 | 004/009 | Freeze vs debitwaterfall vs scopedpool | source50 plusunmappeddebit30 notfree50 | 3 | AWAITING_ADMIN_APPROVAL |
| MQL-DOMAIN | F036/F041/F042/F065 | 056/068/071; uncompletednativeboundary | B19; allnative | 009/010/025/040/051 | 002/005/018/023 | Native checkedlong/ulong/double/UTF8proof vs widerdomain | LONG_MINnegation/MAX+1/NaN/UTF8length unsupportedwithoutnativeproof | 1 | AWAITING_ADMIN_APPROVAL |
| BALANCE-SCHEMA-MAPPING | F013–015/F053–056 | 051/054/058/069 | B02/B15; restartSG07 | 006/017/033 | 003/004/009 | Read-only Gross view vs provedversionedmigration | Remaining40Reserved15→Free25,unknownowner→UNAVAILABLE | 3 | AWAITING_ADMIN_APPROVAL |

Document→Clause для20R6-B rows задан в GUARD_CALLER_CROSSWALK; FunctionID/Signature/Inputs/Guards/Callers/Dependencies длякаждогоsource — SOURCE_FUNCTION_MAP;FSMscenario/gap вFSM_COMPLETE_MATRIX. Связиотсутствующих financialcallersявноNOT_IMPLEMENTED,а не пустыеячейкииливыдуманныеfunctions. Текущийtraceabilityнеобъявленполным: необходимо завершить индивидуальное clause→GRD/alias→FunctionID→entry mapping,включая55C1proposedaliases безавтоматическогопревращениявcurrentnorm. AUDIT_COMPLETENESS=PARTIAL.

## R7_CURRENT_TRACEABILITY_BOUNDARY

Исторические срезы выше не являются текущим остатком. Подтверждены518 неизменяемых inventory identities,13 mutable checkpoint rows,6 exact duplicates,199 FunctionID,66 непустых таблиц1–15,51ERR/23IMP/73GRD ID без потерь. C1 proposed aliases сопоставлены55/55 в GUARD_CALLER_CROSSWALK; это тематические intersections, не approved predicates. R7-TR-01..18 в FSM_COMPLETE_MATRIX привязаны к clauses06/07, source и SG; это не полный transition census.

Точно незакрытые обязательства: (1) индивидуальная authority/precedence квалификация оставшихся137 UNKNOWN_AUTHORITY rows;40 PROPOSED и15 taxonomy labels уже адресно уточнены в R7_AUTHORITY_RECONCILIATION с сохранением истории; (2) атомарный clause inventory owner Docs00–32 и применимых поздних amendments против73GRD; (3) каждая нормативно обязательная caller relation и все public boundaries, не только три функции TransactionTypes/StateMachine; (4) clause-level scenario09–17 relation против SG01–10; (5) индивидуальная итоговая сверка51ERR/23IMP/66F со всеми полученными clauses,guards,callers,FSM и16decisions. Эти задачи доступны для дальнейшего статического анализа; отсутствие GitHub API не является причиной их содержательной незавершённости.

DOCUMENTARY_COMPLETENESS=READING_REGISTER_CONFIRMED_IDENTITY_AUTHORITY_RECONCILIATION_PARTIAL
AUDIT_RESEARCH_COMPLETE=NO
AUDIT_COMPLETENESS=PARTIAL
GITHUB_PUBLICATION_COMPLETE=NO
R7_OVERALL_STATUS=PARTIAL_AND_PUBLICATION_BLOCKED
