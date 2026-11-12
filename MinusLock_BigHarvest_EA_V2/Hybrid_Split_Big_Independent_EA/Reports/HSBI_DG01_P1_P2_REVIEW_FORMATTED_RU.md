# AUDIT 02 — P1/P2: повторная классификация
Ни одна строка не означает native runtime доказательство. Отдельно различены source, normative conflict, unimplemented и UNVERIFIED.

## FSA-011 — P1 / CONFIRMED_SOURCE_DEFECT
- **Source**: {'File': 'Include/Planning/HSBI_GeometrySolver.mqh', 'SHA256': '62b3b4a8d7a374e15b96b46a380e3c2f8f0e74aa57ae8749c0261ebab27a11f9', 'Function': 'HSBI_SolveBigGeometry', 'Line': 21, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Docs/04:9; Docs/25:5; zeroCore
- **Actual**: coreGrid разрешает Core=0 и не требует Core>=volumeMin.
- **Expected**: Обязательный Core положителен и на broker grid/min/max.
- **Counterexample**: Far.1 Rc.01 Rt3 Rs.1: rawCore.001→0.
- **TestID**: FSA011_ZERO_CORE
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: Active-leg schema
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: HSBI_FULL_SYSTEM_AUDIT_02_SOURCE_TESTS_EXTENDED.json

## FSA-012 — P1 / UNIMPLEMENTED
- **Source**: {'File': 'Include/Core/HSBI_StateMachine.mqh', 'SHA256': '7ec9f9860ce9d72c7f7c119377c1b2bedda25001921b92ef3aa9c7d95a32e403', 'Function': 'HSBI_IsTransitionAllowed', 'Line': 5, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Docs/06 full transition lifecycle
- **Actual**: Таблица нормального пути обрывается после открытия Core; event orchestrator отсутствует.
- **Expected**: Полный event FSM и запрет auto-resume требуют orchestration/authority.
- **Counterexample**: CoreOpening→TrendOpening отсутствует; reconcile-путь не имеет admin resume аргумента.
- **TestID**: FSA012_CORE_TO_TREND
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: Lifecycle approval
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: HSBI_FULL_SYSTEM_AUDIT_02_SOURCE_TESTS_EXTENDED.json

## FSA-013 — P1 / UNIMPLEMENTED
- **Source**: {'File': 'Include/Persistence/HSBI_PersistenceInterface.mqh', 'SHA256': 'e72b591500db88e2596c498fcdf7dbfdbe3641eef91ebbee80ce59e3aeddab06', 'Function': 'HSBI_PersistSnapshotStub', 'Line': 7, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Docs/16:6,12,15
- **Actual**: Stub возвращает success=false; production SHA256=false.
- **Expected**: Durable commit/lock/CAS нельзя доказать stub.
- **Counterexample**: Restart без journal backend не восстанавливает подтверждённый funding.
- **TestID**: None
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: D-07
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: STATIC_SOURCE_AND_EXPLICIT_MATHEMATICAL_ARGUMENT; no fresh end-to-end execution

## FSA-014 — P1 / UNIMPLEMENTED
- **Source**: {'File': 'Hybrid_Split_Big_Independent_EA.mq5', 'SHA256': '71e511c620df5de7f1f9e0d865664efeaf4cf6edbcbb07f20efaf25c40e9bd62', 'Function': 'OnTick', 'Line': 35, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Docs/03:6,39; Docs/18:29
- **Actual**: EA вызывает только SubmitActionStub; OnTradeTransaction отсутствует.
- **Expected**: Полный lifecycle не реализован. Это не дефект работающего dispatch.
- **Counterexample**: Tick не запускает Harvest/PartialFar/NewFar.
- **TestID**: None
- **Reachability**: OnTick reachable: execution stub only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: Separate production task
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: STATIC_SOURCE_AND_EXPLICIT_MATHEMATICAL_ARGUMENT; no fresh end-to-end execution

## FSA-015 — P1 / CONFIRMED_CONTRACT_CONFLICT
- **Source**: {'File': 'Include/Planning/HSBI_FutureSmallProofAggregator.mqh', 'SHA256': '7bea2c75eec23825d5cbcca82fa72022b73f8c1626f5ffbce30ac79d722b03a0', 'Function': 'HSBI_AggregateFutureSmallProof', 'Line': 23, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Docs/30:5 vs proposed CR09/D04
- **Actual**: WORST_CASE выбирает worstTransitionLossLevel вместо minimum CatchUpMargin.
- **Expected**: ALL_LEVEL требует min margin>0; SINGLE_LEVEL должен иметь отдельный scope.
- **Counterexample**: T1=10,M1=9; T2=5,M2=-11. Выбран1.
- **TestID**: FSA015_MIN_MARGIN_LEVEL
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: CR-09
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: HSBI_FULL_SYSTEM_AUDIT_02_SOURCE_TESTS_EXTENDED.json

## FSA-016 — P1 / CONFIRMED_CONTRACT_CONFLICT
- **Source**: {'File': 'Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md', 'SHA256': 'cd8e312bc8d98519f42618b2ac3f316be546f178f4cc0b3168577bb365603dc1', 'Function': None, 'Line': 22}
- **Contract**: Docs/03:21; Docs/14:22 vs Docs/29:3
- **Actual**: Разные документы требуют minimum-safe-volume и risk-first ordering.
- **Expected**: Владелец выбирает lexicographic objective; тест не утверждает экономическую цель.
- **Counterexample**: Безопасный N.1 risk9 и N.2 risk1 дают разные optimum.
- **TestID**: None
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: NewFar objective policy
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: STATIC_SOURCE_AND_EXPLICIT_MATHEMATICAL_ARGUMENT; no fresh end-to-end execution

## FSA-017 — P1 / CONFIRMED_SOURCE_DEFECT
- **Source**: {'File': 'Include/Planning/HSBI_FutureSmallSolver.mqh', 'SHA256': 'c403bbad6089076500823219dac296e69100bed0e2cb950eb1f248749b868cf6', 'Function': 'HSBI_EvaluateFutureSmallLevel', 'Line': 57, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Docs/04:21 NextBigGross<OldBigGross
- **Actual**: netBigVolume сравнивается с priorBigGross, затем priorBig тоже хранит net.
- **Expected**: Сравнивать одинаковые gross величины; прочие gates независимы.
- **Counterexample**: Old gross4/net2; new gross8/net0 проходит одну net-проверку. Не весь solver.
- **TestID**: None
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: Gross schema
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: STATIC_SOURCE_AND_EXPLICIT_MATHEMATICAL_ARGUMENT; no fresh end-to-end execution

## FSA-018 — P1 / CONFIRMED_CONTRACT_CONFLICT
- **Source**: {'File': 'Include/Planning/HSBI_FutureSmallSolver.mqh', 'SHA256': 'c403bbad6089076500823219dac296e69100bed0e2cb950eb1f248749b868cf6', 'Function': 'HSBI_ValidateConservativeBound', 'Line': 12, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Docs/04:33,36; Docs/27:5
- **Actual**: Функция endpoint-bound не доказывает единый закон будущих переходов.
- **Expected**: Нужна предпосылка Fnext<=qF на каждом переходе; helper не ошибочен внутри scope.
- **Counterexample**: F=1,.8,.64 затем .64; первые два шага не задают третий.
- **TestID**: None
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: Tail/terminal contract
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: STATIC_SOURCE_AND_EXPLICIT_MATHEMATICAL_ARGUMENT; no fresh end-to-end execution

## FSA-019 — P1 / UNVERIFIED
- **Source**: {'File': 'Include/Money/HSBI_CostModel.mqh', 'SHA256': '4f19ebab853118d7946f99a5fed2b9d84cbfd16c83390df9f5721c53c207f590', 'Function': 'HSBI_TryProjectedNetMoney', 'Line': 15, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: D06; Docs/04:18; Docs/24:7
- **Actual**: Нет независимого basis/window/coverage для spread/buffer.
- **Expected**: Нельзя объявить любой spread двойным: provider basis неизвестен.
- **Counterexample**: BUY Ask101→Bid110 уже даёт9; вычет того же spread1 даёт8 только при доказанном overlap.
- **TestID**: None
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: D-06
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: STATIC_SOURCE_AND_EXPLICIT_MATHEMATICAL_ARGUMENT; no fresh end-to-end execution

## FSA-020 — P1 / UNVERIFIED
- **Source**: {'File': 'Docs/03_FULL_SYSTEM_MANUAL_RU.md', 'SHA256': '3d0bd17b2501d61d612d6ec982b215d52dbd92da8b174d4e425f4c477c7484d0', 'Function': None, 'Line': 9}
- **Contract**: Supported account/broker model admission
- **Actual**: Режим hedging/netting не закреплён независимым account admission.
- **Expected**: Нужен hedging contract либо виртуальный netting ledger; broker evidence отсутствует.
- **Counterexample**: BUY1+SELL1: hedging две позиции; netting net0.
- **TestID**: None
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: Account mode
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: STATIC_SOURCE_AND_EXPLICIT_MATHEMATICAL_ARGUMENT; no fresh end-to-end execution

## FSA-021 — P2 / CONFIRMED_CONTRACT_CONFLICT
- **Source**: {'File': 'Include/Planning/HSBI_ControlPrices.mqh', 'SHA256': '5bd35f0cc4b7ee1aac1a772b2932f13ba385922e26d5f2649bbda76837256a4b', 'Function': 'HSBI_IsSnapshotFresh', 'Line': 11, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Docs/05:6,13; freshness clock contract
- **Actual**: Нет нижней границы age; future timestamp принят.
- **Expected**: Для zero-skew fixture reject; универсальный clock skew требует выбора.
- **Counterexample**: now100,ts1000,maxAge10.
- **TestID**: FSA021_FUTURE_TIME_ZERO_SKEW
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: Clock-domain policy
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: HSBI_FULL_SYSTEM_AUDIT_02_SOURCE_TESTS_EXTENDED.json

## FSA-022 — P2 / CONFIRMED_SOURCE_DEFECT
- **Source**: {'File': 'Include/Core/HSBI_StateMachine.mqh', 'SHA256': '7ec9f9860ce9d72c7f7c119377c1b2bedda25001921b92ef3aa9c7d95a32e403', 'Function': 'HSBI_ProposeStateTransition', 'Line': 6, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Docs/01 StateRevision commit monotonicity
- **Actual**: Revision+1 не проверяет ULONG_MAX.
- **Expected**: Остановить переход до overflow; не обнулять revision.
- **Counterexample**: IDLE/revision 2^64-1→InitialPlanReady. C++ unsigned wrap; native NOT_RUN.
- **TestID**: FSA022_OVERFLOW
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: MQL-DOMAIN
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: HSBI_FULL_SYSTEM_AUDIT_02_SOURCE_TESTS_EXTENDED.json

## FSA-023 — P2 / CONFIRMED_SOURCE_DEFECT
- **Source**: {'File': 'Include/Planning/HSBI_NewFarSolver.mqh', 'SHA256': '9dcf60b6edc245a8a5ee3a05f35d4d8d26c12479f570a66aa5e4f0e703497cd2', 'Function': 'HSBI_FutureSmallTemplateDigest', 'Line': 35, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Array128/domain/proof digest
- **Actual**: Digest индексирует maximumDepth до downstream проверки <=128.
- **Expected**: Проверять shape/domain до digest. Нужен native checked test.
- **Counterexample**: maximumDepth129 при ранних валидных полях; static potential OOB, не исполнялся.
- **TestID**: None
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: DTO/domain
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: STATIC_SOURCE_AND_EXPLICIT_MATHEMATICAL_ARGUMENT; no fresh end-to-end execution

## FSA-024 — P2 / CONFIRMED_CONTRACT_CONFLICT
- **Source**: {'File': 'Tests/Static/accept_hsb_2e_r4_r9_r4a_r8.py', 'SHA256': '9a7d1d95f220038b4c68ad21518e3f8901b08398215556b59a7e96ffc28fe235', 'Function': 'run', 'Line': 7, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Historical frozen scope vs explicitly permitted R0H test harness
- **Actual**: Исторический scope запрещает MQL-файлы даже в разрешённых test harness.
- **Expected**: Разделить test-only MQL и production; frozen checker не менять.
- **Counterexample**: Три R0H .mq5/.mqh в Tests; свежие findings сохранены.
- **TestID**: None
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: Test scope
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: STATIC_SOURCE_AND_EXPLICIT_MATHEMATICAL_ARGUMENT; no fresh end-to-end execution

## FSA-025 — P2 / CONFIRMED_CONTRACT_CONFLICT
- **Source**: {'File': 'Docs/03_FULL_SYSTEM_MANUAL_RU.md', 'SHA256': '3d0bd17b2501d61d612d6ec982b215d52dbd92da8b174d4e425f4c477c7484d0', 'Function': None, 'Line': 50}
- **Contract**: Current evidence cannot inherit oldOPEN_P0=0
- **Actual**: Исторические closure/readiness statements не означают текущего source approval.
- **Expected**: Readiness версионировать по SHA/scope; исторические статусы не переписывать.
- **Counterexample**: OPEN_P0=0 прежнего этапа и новые source defects существуют одновременно.
- **TestID**: None
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: Normative hierarchy
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: STATIC_SOURCE_AND_EXPLICIT_MATHEMATICAL_ARGUMENT; no fresh end-to-end execution

## FSA-026 — P1 / UNVERIFIED
- **Source**: {'File': 'Tests/Reference/hsbi_02b_r0h_native_harness.mq5', 'SHA256': '4c4132f1899f9e6c7430c1b61df7c84d33391e2cee875cc3c3b996cec4dec41f', 'Function': 'OnStart', 'Line': 21, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Native acceptance R0G/R0H; MQL production readiness
- **Actual**: Native harness есть, выполнения MetaEditor/MT5 в этой среде нет.
- **Expected**: NOT_RUN; отсутствие evidence не является runtime bug.
- **Counterexample**: Python/C++ успешен без подтверждённых MQL compiler diagnostics.
- **TestID**: None
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: Native toolchain
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: STATIC_SOURCE_AND_EXPLICIT_MATHEMATICAL_ARGUMENT; no fresh end-to-end execution

## FSA-027 — P1 / CONFIRMED_SOURCE_DEFECT
- **Source**: {'File': 'Include/Persistence/HSBI_ExecutionJournal.mqh', 'SHA256': 'aeba6d8813c0079ae4f8e5c7484895e891e6acb91ae7aeacec751977adf1f76f', 'Function': 'HSBI_ClassifyJournalAppend', 'Line': 25, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Docs/16:append-only immutablejournal; Docs/17:14
- **Actual**: Duplicate lookup предшествует проверке digest/body candidate.
- **Expected**: Проверять immutable body binding до exact replay; durable backend отсутствует.
- **Counterexample**: payload A→ALTERED, currentEntryDigest оставлен старым → NO_OP.
- **TestID**: FSA027_ALTERED_BODY
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: D-07, D-08
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: HSBI_FULL_SYSTEM_AUDIT_02_SOURCE_TESTS_EXTENDED.json

## FSA-028 — P1 / CONFIRMED_CONTRACT_CONFLICT
- **Source**: {'File': 'Include/Planning/HSBI_FutureSmallSolver.mqh', 'SHA256': 'c403bbad6089076500823219dac296e69100bed0e2cb950eb1f248749b868cf6', 'Function': 'HSBI_SolveFutureSmall', 'Line': 113, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Docs/04:36 operationalterminalclose; Docs/27:5
- **Actual**: finiteSequence при Far<=volumeMin не означает full close; terminalRouteAllowed не используется.
- **Expected**: Отдельный терминальный маршрут, стоимость и фактическое закрытие.
- **Counterexample**: Far=.01>0, разрешение terminal route не проверено.
- **TestID**: None
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: Terminal policy
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: STATIC_SOURCE_AND_EXPLICIT_MATHEMATICAL_ARGUMENT; no fresh end-to-end execution

## FSA-029 — P1 / CONFIRMED_SOURCE_DEFECT
- **Source**: {'File': 'Include/Money/HSBI_BasketMoneyEvaluator.mqh', 'SHA256': 'f2038e34a8cc22d2e98cf870e479e6a3cbfe3d6edee64855ffb8784d1e5007fb', 'Function': 'HSBI_EvaluateBasketMoney', 'Line': 11, 'FullSourceReadBoundary': 'STATIC_SOURCE_NOT_NATIVE_RUNTIME'}
- **Contract**: Docs/04:9 Rt>=0; optional Trend
- **Actual**: Geometry разрешает Trend0, money/margin вызываются для четырёх положительных leg.
- **Expected**: Явный optional-leg contract; Core нельзя пропускать.
- **Counterexample**: Core=.3,Trend0,Small.01,Far.1; geometry valid, projected leg Trend0 invalid.
- **TestID**: None
- **Reachability**: NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only
- **FutureConsequence**: Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.
- **RequiredDecision**: Active-leg schema
- **Dependencies**: ['Separate admin approval', 'Native MQL acceptance', 'Independent provider/complete registry where applicable']
- **Evidence**: STATIC_SOURCE_AND_EXPLICIT_MATHEMATICAL_ARGUMENT; no fresh end-to-end execution
