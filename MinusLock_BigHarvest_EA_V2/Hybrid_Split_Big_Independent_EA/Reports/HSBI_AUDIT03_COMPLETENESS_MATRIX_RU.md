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
