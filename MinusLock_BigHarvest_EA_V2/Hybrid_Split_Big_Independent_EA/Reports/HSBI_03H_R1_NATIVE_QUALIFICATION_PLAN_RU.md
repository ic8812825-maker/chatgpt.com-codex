# HSBI-03H-R1 — План квалификации 67 спецификаций без торговых приказов

DocumentVersion=HSBI-03H-R1-V1
SourceCommitSHA=70cc4c861b391a7916403106ff07f25729e602da
EvidenceClass=STATIC_REVIEWED; MATH_DERIVED; TEST_SPECIFIED_NOT_RUN
NormativeStatus=AUDIT_SPEC_ONLY_PROPOSED_AWAITING_OWNER_APPROVAL

Репозиторий: ic8812825-maker/chatgpt.com-codex; ветка work. Все пути относительно MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/. Режим GITHUB_MCP_REMOTE_ONLY, локальных файловых операций нет. SourceCommitSHA — исследованная база, не будущий commit отчётов.
D-06=A и NewFar=A/MINIMUM_SAFE_V1 сохраняются. Новых owner selections и approval receipts этот документ не создаёт. Все числовые торговые примеры синтетические; подтверждённых брокерских сделок в них нет.
PRODUCTION_CHANGED=NO; R11_IMPLEMENTATION_ALLOWED=NO; BROKER_DISPATCH_ALLOWED=NO; REAL_TRADING_ALLOWED=NO; NATIVE_MQL5_TESTS=NOT_RUN.
UNAVAILABLE — отсутствует доказательство, CONFLICT — противоречие, REJECT — доказанное нарушение. Ни один из этих результатов не разрешает новый финансовый эффект. Математическое ожидание не является фактическим PASS.

Scope=15 inherited TL/CU и52 новых03G records; runnable qualification design, не запуск
Dependencies=03F-R2 vector blob0b74240e22fe0248977bb7448baac5039383452e;03G spec blob41f47c6bb8177fd7739babbb3e7a047a1c37a912; owner/profile/provider/native prerequisites
OpenQuestions=где/кем разрешён native запуск; конкретные provider/build/profiles; отсутствующие будущие API и durable backend
AcceptanceCriteria=67 unique TestID с target/fixture/oracle/expected/environment/dependencies/failure; manual exact oracles первой группы; каждый запуск отдельно доказывает достигнутую ветвь

## Статус и порядок исполнения

TEST_SPECS_REVIEWED=67; INHERITED=15; NEW_03G=52.
EXECUTION_STATUS_ALL=NOT_RUN; NATIVE_MQL5_TESTS=NOT_RUN.
Ручная арифметика и расчёт в памяти — MATH_DERIVED, не запущенные MQL5 тесты. Historical7PASS/16FAIL не редактируются и не считаются новым результатом.
Expected далее — proposed contract expectation, не обещание соответствия текущего production. Например, minimum-safe отличается от current risk-first; missing manifest API нельзя подменить другим early reject и поставить PASS.

Запускать по группам1→2→3/4→5→6 после выполнения dependencies. Для каждого case сначала validate fixture setup отдельно, затем subject call, затем независимый oracle и reached-branch trace. SETUP_UNAVAILABLE/NOT_IMPLEMENTED означает BLOCKED/NOT_RUN target, а не PASS negative test.
Тестовый harness обязан иметь неизменённые no-trade guards, недоступный dispatch backend и счётчик dispatch attempts=0. Реальные открывающие/закрывающие запросы не нужны ни одной группе.
Текущий top solver отвергает UNIT_TEST/injected proof; его early reject НЕ проверяет ветвь SELECTED. Для неё нужны реальные calculation-only broker inputs и квалифицированные source/cost/risk/market proofs.

## Шесть классов

### Группа 1 (19 tests)

ExecutionEnvironment=Независимый exact decimal/rational runner либо ручной oracle, вне production; будущий запуск отдельно разрешается.
Dependencies=Frozen fixture; утверждённый test-only exact profile; oracle не вызывает subject evaluator/encoder.

### Группа 2 (12 tests)

ExecutionEnvironment=MetaEditor+MQL5 terminal/build в изолированной calculation-only component среде; без trade backend.
Dependencies=R11-C numeric/codec domain; owner manifest/version; compilation baseline; tests для будущих API blocked до их появления.

### Группа 3 (3 tests)

ExecutionEnvironment=MQL5 terminal + доступный symbol/account для OrderCalcProfit/OrderCalcMargin ONLY; dispatch disabled.
Dependencies=Broker properties/calculation mode/currency/quote receipts; реальный instrument mapping; approved cost membership; R11-C.

### Группа 4 (13 tests)

ExecutionEnvironment=Квалифицированный read-only broker/history/market/cost/clock provider + native receipt decoder; без orders.
Dependencies=R11-C→R11-A; provider identity/account/server/snapshot content/revision/time; negative receipt fixtures.

### Группа 5 (11 tests)

ExecutionEnvironment=Native process + реальный durable journal/atomic registry test backend, controlled crash/restart и two-consumer scheduler; без trading.
Dependencies=C→A→B; approved loss-consumption/offset policy; unique source index/CAS; durable storage и reconciliation; funding никогда из projection.

### Группа 6 (9 tests)

ExecutionEnvironment=Нативная integration сборка с реальными calculation-only wrappers, original receipts, trace каждого branch, dispatch=false.
Dependencies=C→A→B→D и E prerequisites; selected semantics/required set; complete provider/profile/actual residual evidence; native branch instrumentation.

Группа1: Pure mathematical/deterministic. Группа2: MQL5 native component. Группа3: Broker calculation-only. Группа4: Provider/source identity. Группа5: Durable journal/crash/concurrency. Группа6: End-to-end без orders. Принадлежность — основной acceptance слой; например arithmetic reference funding можно считать отдельно, но funding acceptance остаётся в5.

## Полные общие fixtures

### F-PROJECTION (M_MINUS/M_PLUS/M_ZERO)

Все поля:
- Instrument MODEL_LINEAR_1,K1,TickSize=Point1,Digits0,TickValues1/1;volume min/step0.05,max10,origin0.
- Broker=B_MODEL,Server=S_MODEL,Account1,SymbolMODEL_LINEAR_1,Magic7,Cycle7,Plan9,StateRevision5,RegistryRevision5,PolicyVersion3.
- RuntimeMode candidate SHADOW;useInjectedProofs=false;testOnlyApproximation=false. Это декларация будущего integration input,не разрешение считать synthetic flags authentic.
- Far SELL,Core/Trend BUY,Small SELL;opens100;ratios3/1/1.
- Fbefore0.4/0.2/0.1,Fafter0.2/0.1/0.05;depth/counts3,q0.5,compression min0.05/ratio0.5,maxratio0.5.
- Quote Bid=Ask125/125/150,selectedPrice=Ask;timestamps100,fixtureNow100,TTL10,clockFIXTURE_MONOTONIC/tick,epochE1.
- Market IDs1001/1002/1003;cost IDs2001/2002/2003;subcost IDs2011…2014/2021…2024/2031…2034;risk IDs3001/3002/3003.
- Commission Far magnitudes(2.2,8.2,2.2),Small(25.8,4.8,6.8) для M_MINUS;Core/Trend commissions0;swap/fee/spread/slippage0;actual=false;legBuffer1/CatchBuffer1.
- M_PLUS меняет только f2=3.2,s2=9.8;M_ZERO только f2=4.2,s2=8.8.
- Initial recovery−20,priorBig10,exposure10,risk100/tolerance1→90/80/70;synthetic margin10perlot→24/12/6≤100;futurecap20;outer4caps12each.
- OuterOldFar0.8,actualCoreResidual0.4,originalCoreidentifier77/ticket88,directionBUY;oldFaridentifier10/ticket11,directionSELL;current candidate0.4. Проекции имеют IDs801/802/803 и explicitmodel kind,не actual deals.
- Preview eligibility Core-only;share0.8;ProjectedOriginRefs(Plan9,L1…3,BIG_CORE). Native DTO nominal sourceDealId101/sourceEventId501 и FarDealId102/FarEventId502 — symbols fixture дляизучения currentAPI,не выданныеброкеромфакты.
- Legacy shape allocation S101/A101,allocationEvent601,policy3,allocatableNet100,reserve0,PF0,Transition0,Carry0,Residual100,Consumed0;consumptionKey(S101,A101,plan9,rev5,event701,consumerNF),hasPrior=false. Все valid/fresh/confirmed booleans в component fixture true,но Origin/History/Provider receipts REAL=NONE.
- Frozen original fixture receipts FMR1001/1002/1003 содержат full declared quote/cost/identity bodies. Это независимые фиксированные test objects,не production authority.
- Legacy DTO expectedPlanDigest="" — точное значение в базовом fixture. Это не подтверждённая plan integrity. Отдельный frozen fixture object FMR описывает исходное содержимое; он не выдаётся за native digest.
- All other safety inputs имеют указанные numerical premises;доказательства реальных ownership/history/cost coverage/provider/native отсутствуют.
FinancialPermission=NO/UNAVAILABLE во всех этих synthetic previews. Positive CatchUp predicate не actual funding/dispatch.

Нативный codec и trusted plan receipt отсутствуют. Поэтому baseline задаёт expectedPlanDigest="", как допускает legacy source, но proposed authority contract не считает такой input достаточным для финансового разрешения. Component cases имеют полные numeric inputs; полноценный broker-backed integration case потребует отдельно полученных настоящих receipts, а не подставленного hash.

### F-CASH

Synthetic independently stipulated reference receipt R_AUTH,не реальная broker authority:
physicalK=(B_MODEL,S_MODEL,1,101),sourceEvent501,roleBIG_CORE,sourcepostednet18.125,profileM3;policy3/share0.8;
original grantsReserve14.5,PF0,Transition0,Carry0,Residual3.625;Reserve C0/R0/F14.5;revision5.
AllocationKeyA101,AllocationEvent601;all posted/source/history/registry facts полны только в reference fixture. Новый unknown actual provider не выдаётся за R_AUTH.
Stage semantics должны быть указаны: ALTERNATIVE_VALUATIONS (no debit) либо SEQUENTIAL_CONSUMPTIONS.
Exact same event replay→NO_OP. New event после exhaustion/insufficientfree→REJECT;newallocationalias не newsource.
Source of rule: Docs08:12–24,D01/D07/D14 proposals и R2 future contract;real provider/native unavailable.

### TL mathematical fixtures

TL_BASE1: depth2;Fbefore0.4/0.2,Fafter0.2/0.05;grid/profile/scopeIDs из F-PROJECTION first2;opensFar100,Core80,Trend100,Small100;quotes105/105;Farcommission0/0,Small36/12,othercosts0;leg/CUbuffer1;outercap12;controlWORST_CASE.
Leg netsL1=(−3,29,1,−39),L2=(−2,14,0,−14);
basket−12/−2;T12/2;G23.2/11.2;A3/2;margin19.2/8.2.
TL_BASE2: depth2,sameF sequence,allopens100,quotes125/125,Farcommission1/0,Small18/7,buffers1,outercap5;
netsL1=(−12,29,9,−29),L2=(−6,14,4,−13);
basket−3/−1;T3/1;G23.2/11.2;A12/6;margin10.2/4.2.
Both initialRecovery−20,futurecap20,other scope/risk/grid fields as above truncated2 (qtheoreticaldepth3 не requiredactualcount;terminal after2). Эти fixtures согласованы как денежная модель, не полный broker execution witness.


### Дополнения и несовместимые назначения

M_PLUS/M_MINUS/M_ZERO остаются projected fixed-template valuation fixtures, НЕ физической B-chain. Никакой case с ними не получает physical sequential certification из одних numeric flags.
R_AUTH — synthetic independent source, реальные provider receipts NONE. Для native positive funding будет нужен новый separately versioned fixture с настоящим read-only history binding; замена synthetic на real должна явно записать mapping и не изменить mathematical expected задним числом.
V1 quantity fixture: share0.5,NetBig1.2,FarBefore1,FarAfter0.4,OriginalCandidate0.8; SAME_POSITION_PARTIAL закрывает0.6, PROMOTION закрывает old position1.
NF_A_B: a(N0.2,Risk18,Margin40,count2,margins2/2), b(0.3,12,50,3,4/4); unsafe x(0.1,1,20,1,4/−1). NF_TIE: N0.2,Risk10,Margin40,count2,d margins10/1,e4/3.
INT64_EXACT — generic signed64 domain, не реальная currency policy. M3_EXACT — synthetic scale1000. D06_A и D05 полные inputs указаны в отдельных records.
Неподанные proof clauses NF fixtures — component premises MODEL_ONLY, не real authority. Inputs денежных records ниже literal decimal strings; нельзя случайно заменить их binary64 parsing до независимого exact oracle.

## Независимые оракулы и ручная арифметика группы1

Оракул использует arbitrary precision integers/rationals, set/tuple rules и literal expected. Он не импортирует subject money/identity/codec functions. Для double inputs fixed decimal → exact rational; float error qualification отдельно. Выполненная здесь ручная проверка не является отдельным test run.

- CU-04: M_MINUS: T=(12,7,3),M=(9,−4,2);12>7>3,−4<2<9, поэтому разные IDs1 и2. Это valuation oracle03G, не физическая promotion history; physical witness отдельно в03H money report.

- VOLUME-01: 0.5×1.2=0.6; сравнения строгие:0.6>1 false,>0.4 true,>0.6 false,>0.8 false.

- VOLUME-03: 0.8×(1.2,0.6,0.3)=(0.96,0.48,0.24); все>(0.4,0.2,0.1),но последнее0.24>0.4 false.

- VOLUME-05: 0.43/0.05=8.6 не целое, off-grid; min/max alone недостаточно.

- MONEY-01: 12000−11000−1000=0 milli-units; strict>0 false.

- MONEY-02: nominal12001−11000−1000=1 milli-unit; lower11999−11001−1001=−3; positive nominal недостаточен.

- MONEY-04: −INT64_MIN=9223372036854775808>9223372036854775807; вычислить математически arbitrary precision, subject обязан UNAVAILABLE, а не wrap.

- MONEY-05: 9223372036854775807+1=9223372036854775808, на1 выше максимума signed64; overflow.

- COST-01: 10000−1000−2000−500=6500 milli-units; комиссия не вычитается второй раз.

- OBJECTIVE-01: Оба feasible по component premises; minimum tuple N:0.2<0.3 →a; legacy Risk12<18 →b. Это две разные policy versions.

- OBJECTIVE-02: x margin min(4,−1)=−1≤0: исключить; a min(2,2)=2>0, N0.2 среди доказанных допустимых.

- OBJECTIVE-03: m(d)=min(10,1)=1,m(e)=min(4,3)=3; равные N/risk/margin/count →−3<−1, выбираетсяe.

- OBJECTIVE-04: ASCII bytes a=97,b=98,97<98 при обеих permutations. MODEL_ASCII_TOTAL_1 не утверждает реальный codec.

- OBJECTIVE-05: N0.1 unknown,N0.2 feasible: невозможно доказать отсутствие меньшего допустимого; qualified minimum UNAVAILABLE.

- OBJECTIVE-06: Feasible set пуст и полностью rejected: selection NO_SAFE_CANDIDATE; unknown≠полностью rejected.

- OBJECTIVE-07: min(9,0,2)=0; strict>0 false, reject.

- OBJECTIVE-08: R из3,1 marginUNKNOWN: известные9/2 не дают min всего R; UNAVAILABLE.

- SAFETY-01: E=40−4−1=35; RecoveryA=35−4−50=−19; threshold10+5+1=16; −19<16.

- SAFETY-03: short loss(v,K,ΔP)=0.1×1×ΔP; при ΔP→∞ loss→∞. Конечный native sample это не опровергает.

Дополнительная арифметика для native funding oracle: source18.125×0.8=14.5,residual3.625;9 debit оставляет5.5; второй9 невозможен. Reservation9 из14.5 даётF5.5/R9/C0; commit4 даётF5.5/R5/C4; release5 даётF10.5/R0/C4, сумма14.5. Correction grant14.5−10=4.5<Consumed9 даёт reconciliation debt/conflict, не отрицательный Free. Два commits с одной expected revision5: максимум один; невозможен C18 при grant14.5. SAFETY-02:−15<−12 breach,−15+100=85,lossNow0,sticky сохраняется.

## Полный реестр 67 тестов

В каждой записи ExecutionEnvironment и Dependencies включают общие требования указанной группы целиком. TargetFunction с NOT_IMPLEMENTED — будущий компонент, не существующий API. Native expected status разрешено отображать на legacy enum только явно documented adapter; смысл unknown/proof completeness не теряется. Для каждого отрицательного/unknown case новый финансовый delta=0; позитивный component result не grants/dispatch.

### TL-01

TestID=TL-01
QualificationGroup=2
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_SolveNewFar/result mapping
RequiredFixture=TL_BASE1,cap12
IndependentOracle=frozen exact fixture + независимый component predicate; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult=Tmax12,Acontrol3; хранить оба вида; cap equality valid
ExecutionEnvironment=MetaEditor+MQL5 terminal/build в изолированной calculation-only component среде; без trade backend.
Dependencies=R11-C numeric/codec domain; owner manifest/version; compilation baseline; tests для будущих API blocked до их появления. Полный fixture из раздела выше; исходные TL/CU expected version03G не переписывают03F. 
FailureClass=METRIC_KIND_MISMATCH

### TL-02

TestID=TL-02
QualificationGroup=3
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_EvaluateBasketMoney; HSBI_EvaluateNewFarGates
RequiredFixture=TL_BASE2,cap5
IndependentOracle=frozen exact fixture + независимый component predicate; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult=Tmax3,Acontrol12; cap сравнивает3, coverage12
ExecutionEnvironment=MQL5 terminal + доступный symbol/account для OrderCalcProfit/OrderCalcMargin ONLY; dispatch disabled.
Dependencies=Broker properties/calculation mode/currency/quote receipts; реальный instrument mapping; approved cost membership; R11-C. Полный fixture из раздела выше; исходные TL/CU expected version03G не переписывают03F. 
FailureClass=METRIC_SCOPE

### TL-03

TestID=TL-03
QualificationGroup=6
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_SolveNewFar; HSBI_AggregateFutureSmallProof
RequiredFixture=M_PLUS,explicit controlL2
IndependentOracle=frozen exact fixture + независимый component predicate; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult=Tmax12@L1,A9.2@L2,minM1
ExecutionEnvironment=Нативная integration сборка с реальными calculation-only wrappers, original receipts, trace каждого branch, dispatch=false.
Dependencies=C→A→B→D и E prerequisites; selected semantics/required set; complete provider/profile/actual residual evidence; native branch instrumentation. Полный fixture из раздела выше; исходные TL/CU expected version03G не переписывают03F. 
FailureClass=LEVEL_SCOPE_MISMATCH

### TL-04

TestID=TL-04
QualificationGroup=6
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_SolveNewFar/all-required future gate
RequiredFixture=M_MINUS,controlL1,cap12
IndependentOracle=frozen exact fixture + независимый component predicate; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult=REJECT,required L2 margin−4
ExecutionEnvironment=Нативная integration сборка с реальными calculation-only wrappers, original receipts, trace каждого branch, dispatch=false.
Dependencies=C→A→B→D и E prerequisites; selected semantics/required set; complete provider/profile/actual residual evidence; native branch instrumentation. Полный fixture из раздела выше; исходные TL/CU expected version03G не переписывают03F. 
FailureClass=REQUIRED_MARGIN_NEGATIVE

### TL-05

TestID=TL-05
QualificationGroup=6
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_EvaluateNewFarGates→safe[]
RequiredFixture=TL_BASE1,Small commissionL1=37,cap12
IndependentOracle=frozen exact fixture + независимый component predicate; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult=Tmax13>12; REJECT до safe[]
ExecutionEnvironment=Нативная integration сборка с реальными calculation-only wrappers, original receipts, trace каждого branch, dispatch=false.
Dependencies=C→A→B→D и E prerequisites; selected semantics/required set; complete provider/profile/actual residual evidence; native branch instrumentation. Полный fixture из раздела выше; исходные TL/CU expected version03G не переписывают03F. 
FailureClass=TRANSITION_CAP_EXCEEDED

### CU-01

TestID=CU-01
QualificationGroup=6
ExecutionStatus=NOT_RUN
TargetFunction=future all-required CatchUp→HSBI_SolveNewFar
RequiredFixture=M_PLUS,required3
IndependentOracle=frozen exact fixture + независимый component predicate; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult=minM1; component true; authority NO
ExecutionEnvironment=Нативная integration сборка с реальными calculation-only wrappers, original receipts, trace каждого branch, dispatch=false.
Dependencies=C→A→B→D и E prerequisites; selected semantics/required set; complete provider/profile/actual residual evidence; native branch instrumentation. Полный fixture из раздела выше; исходные TL/CU expected version03G не переписывают03F. 
FailureClass=FALSE_ALL_LEVEL_PERMISSION

### CU-02

TestID=CU-02
QualificationGroup=2
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_EvaluateReserveCatchUp/strict zero
RequiredFixture=M_ZERO,required3
IndependentOracle=frozen exact fixture + независимый component predicate; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult=minM0; REJECT
ExecutionEnvironment=MetaEditor+MQL5 terminal/build в изолированной calculation-only component среде; без trade backend.
Dependencies=R11-C numeric/codec domain; owner manifest/version; compilation baseline; tests для будущих API blocked до их появления. Полный fixture из раздела выше; исходные TL/CU expected version03G не переписывают03F. 
FailureClass=NONPOSITIVE_CATCHUP_MARGIN

### CU-03

TestID=CU-03
QualificationGroup=6
ExecutionStatus=NOT_RUN
TargetFunction=future per-level CatchUp
RequiredFixture=M_MINUS,required3
IndependentOracle=frozen exact fixture + независимый component predicate; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult=minM−4; REJECT
ExecutionEnvironment=Нативная integration сборка с реальными calculation-only wrappers, original receipts, trace каждого branch, dispatch=false.
Dependencies=C→A→B→D и E prerequisites; selected semantics/required set; complete provider/profile/actual residual evidence; native branch instrumentation. Полный fixture из раздела выше; исходные TL/CU expected version03G не переписывают03F. 
FailureClass=REQUIRED_MARGIN_NEGATIVE

### CU-04

TestID=CU-04
QualificationGroup=1
ExecutionStatus=NOT_RUN
TargetFunction=independent extrema oracle
RequiredFixture=M_MINUS
IndependentOracle=frozen exact fixture + независимый component predicate; M_MINUS: T=(12,7,3),M=(9,−4,2);12>7>3,−4<2<9, поэтому разные IDs1 и2. Это valuation oracle03G, не физическая promotion history; physical witness отдельно в03H money report.
ExpectedResult=argmaxT=L1,argminM=L2
ExecutionEnvironment=Независимый exact decimal/rational runner либо ручной oracle, вне production; будущий запуск отдельно разрешается.
Dependencies=Frozen fixture; утверждённый test-only exact profile; oracle не вызывает subject evaluator/encoder. Полный fixture из раздела выше; исходные TL/CU expected version03G не переписывают03F. 
FailureClass=EXTREMA_CONFLATION

### CU-05

TestID=CU-05
QualificationGroup=6
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_SolveFutureSmall→aggregator→caller
RequiredFixture=M_PLUS,L2 moneyIncluded=false/statusUNAVAILABLE
IndependentOracle=frozen exact fixture + независимый component predicate; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult=INCOMPLETE/UNAVAILABLE; no qualified min
ExecutionEnvironment=Нативная integration сборка с реальными calculation-only wrappers, original receipts, trace каждого branch, dispatch=false.
Dependencies=C→A→B→D и E prerequisites; selected semantics/required set; complete provider/profile/actual residual evidence; native branch instrumentation. Полный fixture из раздела выше; исходные TL/CU expected version03G не переписывают03F. 
FailureClass=REQUIRED_MONEY_PROOF_MISSING

### CU-06

TestID=CU-06
QualificationGroup=5
ExecutionStatus=NOT_RUN
TargetFunction=future atomic inventory reserve/consume (NOT_IMPLEMENTED)
RequiredFixture=R_AUTH,9@rev5,9@rev6
IndependentOracle=frozen exact fixture + независимый component predicate; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult=after1 C9/F5.5/rev6; second REJECT delta0
ExecutionEnvironment=Native process + реальный durable journal/atomic registry test backend, controlled crash/restart и two-consumer scheduler; без trading.
Dependencies=C→A→B; approved loss-consumption/offset policy; unique source index/CAS; durable storage и reconciliation; funding никогда из projection. Полный fixture из раздела выше; исходные TL/CU expected version03G не переписывают03F. 
FailureClass=INSUFFICIENT_FREE

### CU-07

TestID=CU-07
QualificationGroup=4
ExecutionStatus=NOT_RUN
TargetFunction=future original snapshot receipt validator (NOT_IMPLEMENTED)
RequiredFixture=M_PLUS,market1002→2002,replacement receiptNONE,expectedPlanDigest empty
IndependentOracle=frozen exact fixture + независимый component predicate; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult=UNAVAILABLE/authority mismatch; не обещать legacy digest reject
ExecutionEnvironment=Квалифицированный read-only broker/history/market/cost/clock provider + native receipt decoder; без orders.
Dependencies=R11-C→R11-A; provider identity/account/server/snapshot content/revision/time; negative receipt fixtures. Полный fixture из раздела выше; исходные TL/CU expected version03G не переписывают03F. 
FailureClass=SNAPSHOT_AUTHORITY_MISSING

### CU-08

TestID=CU-08
QualificationGroup=4
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_SolveNewFar/plan identity; future independent revision binding
RequiredFixture=M_PLUS,currentRevision6,plan/proof/consumption5
IndependentOracle=frozen exact fixture + независимый component predicate; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult=CONFLICT,delta0
ExecutionEnvironment=Квалифицированный read-only broker/history/market/cost/clock provider + native receipt decoder; без orders.
Dependencies=R11-C→R11-A; provider identity/account/server/snapshot content/revision/time; negative receipt fixtures. Полный fixture из раздела выше; исходные TL/CU expected version03G не переписывают03F. 
FailureClass=STATE_REVISION_MISMATCH

### CU-09

TestID=CU-09
QualificationGroup=4
ExecutionStatus=NOT_RUN
TargetFunction=future preview/funding type and authority gate (NOT_IMPLEMENTED)
RequiredFixture=positive projected Core,actual receiptsNONE
IndependentOracle=frozen exact fixture + независимый component predicate; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult=PREVIEW_ONLY, fundingBLOCKED
ExecutionEnvironment=Квалифицированный read-only broker/history/market/cost/clock provider + native receipt decoder; без orders.
Dependencies=R11-C→R11-A; provider identity/account/server/snapshot content/revision/time; negative receipt fixtures. Полный fixture из раздела выше; исходные TL/CU expected version03G не переписывают03F. 
FailureClass=SOURCE_AUTHORITY_MISSING

### CU-10

TestID=CU-10
QualificationGroup=6
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_SolveFutureSmall→future manifest completeness
RequiredFixture=M_PLUS,min/step0.025,depth3,R=L1…L4,L4UNKNOWN
IndependentOracle=frozen exact fixture + независимый component predicate; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult=UNAVAILABLE; prefix/bound не required tail
ExecutionEnvironment=Нативная integration сборка с реальными calculation-only wrappers, original receipts, trace каждого branch, dispatch=false.
Dependencies=C→A→B→D и E prerequisites; selected semantics/required set; complete provider/profile/actual residual evidence; native branch instrumentation. Полный fixture из раздела выше; исходные TL/CU expected version03G не переписывают03F. 
FailureClass=TAIL_MONEY_NOT_PROVEN

### LEVEL-01

TestID=LEVEL-01
QualificationGroup=2
ExecutionStatus=NOT_RUN
TargetFunction=future frozen manifest/state-chain validator (NOT_IMPLEMENTED); HSBI_SolveFutureSmall/HSBI_AggregateFutureSmallProof downstream
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","R":["L1","L2","L3"],"P":["L1","L2","L3"],"semantics":"ALTERNATIVE_SCENARIOS","terminal":"approved fixture guard at L3"}
IndependentOracle=set coverage component; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"completeness":"COMPLETE_FOR_DECLARED_FIXTURE_SCOPE","financialPermission":"NO"}
ExecutionEnvironment=MetaEditor+MQL5 terminal/build в изолированной calculation-only component среде; без trade backend.
Dependencies=R11-C numeric/codec domain; owner manifest/version; compilation baseline; tests для будущих API blocked до их появления. Frozen level manifest + independent per-level original receipts NativeIntegrationRequired=owner-selected model + real provider/native
FailureClass=NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED

### LEVEL-02

TestID=LEVEL-02
QualificationGroup=2
ExecutionStatus=NOT_RUN
TargetFunction=future frozen manifest/state-chain validator (NOT_IMPLEMENTED); HSBI_SolveFutureSmall/HSBI_AggregateFutureSmallProof downstream
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","R":["L1","L2","L3","L4"],"P":["L1","L2","L3"],"L4":"MISSING"}
IndependentOracle=set coverage component; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"completeness":"INCOMPLETE","reason":"REQUIRED_LEVEL_MISSING","delta":0}
ExecutionEnvironment=MetaEditor+MQL5 terminal/build в изолированной calculation-only component среде; без trade backend.
Dependencies=R11-C numeric/codec domain; owner manifest/version; compilation baseline; tests для будущих API blocked до их появления. External frozen R, no L4 receipt NativeIntegrationRequired=native missing-level propagation
FailureClass=REQUIRED_LEVEL_MISSING

### LEVEL-03

TestID=LEVEL-03
QualificationGroup=2
ExecutionStatus=NOT_RUN
TargetFunction=future frozen manifest/state-chain validator (NOT_IMPLEMENTED); HSBI_SolveFutureSmall/HSBI_AggregateFutureSmallProof downstream
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","IDs":["L1","L2","L2"],"bodies":["body1","body2","alteredBody2"]}
IndependentOracle=manifest/receipt comparison; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"CONFLICT","reason":"DUPLICATE_LEVEL_ALTERED_BODY","delta":0}
ExecutionEnvironment=MetaEditor+MQL5 terminal/build в изолированной calculation-only component среде; без trade backend.
Dependencies=R11-C numeric/codec domain; owner manifest/version; compilation baseline; tests для будущих API blocked до их появления. Original receipts for L2 and altered body NativeIntegrationRequired=authority-backed content validation
FailureClass=DUPLICATE_LEVEL_ALTERED_BODY

### LEVEL-04

TestID=LEVEL-04
QualificationGroup=2
ExecutionStatus=NOT_RUN
TargetFunction=future frozen manifest/state-chain validator (NOT_IMPLEMENTED); HSBI_SolveFutureSmall/HSBI_AggregateFutureSmallProof downstream
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","requiredOrder":["L1","L2","L3"],"providedOrder":["L2","L1","L3"],"semantics":"SEQUENTIAL_TRANSITIONS","edges":[["L1","L2"],["L2","L3"]]}
IndependentOracle=graph validator; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"REJECT","reason":"STATE_CHAIN_ORDER_MISMATCH","delta":0}
ExecutionEnvironment=MetaEditor+MQL5 terminal/build в изолированной calculation-only component среде; без trade backend.
Dependencies=R11-C numeric/codec domain; owner manifest/version; compilation baseline; tests для будущих API blocked до их появления. Ordered state before/after receipts NativeIntegrationRequired=native execution-prefix/restart
FailureClass=STATE_CHAIN_ORDER_MISMATCH

### LEVEL-05

TestID=LEVEL-05
QualificationGroup=2
ExecutionStatus=NOT_RUN
TargetFunction=future frozen manifest/state-chain validator (NOT_IMPLEMENTED); HSBI_SolveFutureSmall/HSBI_AggregateFutureSmallProof downstream
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","volumeMin":"0.025","volumeStep":"0.025","maximumDepth":3,"FarAfter":["0.2","0.1","0.05"],"R":["L1","L2","L3","L4"],"tail":"EXACT_REQUIRED_4","L4":"UNKNOWN"}
IndependentOracle=bound versus coverage component; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"UNAVAILABLE","reason":"TAIL_MONEY_NOT_PROVEN","delta":0}
ExecutionEnvironment=MetaEditor+MQL5 terminal/build в изолированной calculation-only component среде; без trade backend.
Dependencies=R11-C numeric/codec domain; owner manifest/version; compilation baseline; tests для будущих API blocked до их появления. Tail manifest; L4 money proof absent NativeIntegrationRequired=native producer with conservative prefix
FailureClass=TAIL_MONEY_NOT_PROVEN

### LEVEL-06

TestID=LEVEL-06
QualificationGroup=2
ExecutionStatus=NOT_RUN
TargetFunction=future frozen manifest/state-chain validator (NOT_IMPLEMENTED); HSBI_SolveFutureSmall/HSBI_AggregateFutureSmallProof downstream
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","LevelSemantics":"UNKNOWN_SCHEMA_V99"}
IndependentOracle=schema validator; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"UNSUPPORTED","reason":"LEVEL_SEMANTICS_UNSUPPORTED","delta":0}
ExecutionEnvironment=MetaEditor+MQL5 terminal/build в изолированной calculation-only component среде; без trade backend.
Dependencies=R11-C numeric/codec domain; owner manifest/version; compilation baseline; tests для будущих API blocked до их появления. Version allowlist receipt NativeIntegrationRequired=native codec/restart
FailureClass=LEVEL_SEMANTICS_UNSUPPORTED

### VOLUME-01

TestID=VOLUME-01
QualificationGroup=1
ExecutionStatus=NOT_RUN
TargetFunction=quantity oracle; HSBI_ValidateVolume; future action/volume binding (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"V1","share":"0.5","NetBig":"1.2","FarBefore":"1","FarAfter":"0.4","OriginalCandidate":"0.8","mode":"SAME_POSITION_PARTIAL","FarClosed":"0.6"}
IndependentOracle=exact quantity predicates; 0.5×1.2=0.6; сравнения строгие:0.6>1 false,>0.4 true,>0.6 false,>0.8 false.
ExpectedResult={"lhs":"0.6","FarBefore":false,"FarAfter":true,"FarClosed":false,"OriginalCandidate":false}
ExecutionEnvironment=Независимый exact decimal/rational runner либо ручной oracle, вне production; будущий запуск отдельно разрешается.
Dependencies=Frozen fixture; утверждённый test-only exact profile; oracle не вызывает subject evaluator/encoder. One position/action partial-fill lineage NativeIntegrationRequired=native grid + fills
FailureClass=NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED

### VOLUME-02

TestID=VOLUME-02
QualificationGroup=6
ExecutionStatus=NOT_RUN
TargetFunction=quantity oracle; HSBI_ValidateVolume; future action/volume binding (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"V1","share":"0.5","NetBig":"1.2","FarBefore":"1","FarAfter":"0.4","oldPosition":"SELL:P1","newPosition":"BUY:P2","mode":"PROMOTION","FarClosed":"1"}
IndependentOracle=lineage semantics; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"compression":"0.6","physicalClosed":"1","reason":"COMPRESSION_NOT_PHYSICAL_CLOSED"}
ExecutionEnvironment=Нативная integration сборка с реальными calculation-only wrappers, original receipts, trace каждого branch, dispatch=false.
Dependencies=C→A→B→D и E prerequisites; selected semantics/required set; complete provider/profile/actual residual evidence; native branch instrumentation. OldFar full-close and originalCore residual receipts NativeIntegrationRequired=actual-fill integration, no dispatch in qualification
FailureClass=COMPRESSION_NOT_PHYSICAL_CLOSED

### VOLUME-03

TestID=VOLUME-03
QualificationGroup=1
ExecutionStatus=NOT_RUN
TargetFunction=quantity oracle; HSBI_ValidateVolume; future action/volume binding (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","policy":"FarBefore","share":"0.8","NetBig":["1.2","0.6","0.3"],"FarBefore":["0.4","0.2","0.1"],"legacyN":"0.4"}
IndependentOracle=quantity model; 0.8×(1.2,0.6,0.3)=(0.96,0.48,0.24); все>(0.4,0.2,0.1),но последнее0.24>0.4 false.
ExpectedResult={"lhs":["0.96","0.48","0.24"],"perLevel":[true,true,true],"legacy":[true,true,false]}
ExecutionEnvironment=Независимый exact decimal/rational runner либо ручной oracle, вне production; будущий запуск отдельно разрешается.
Dependencies=Frozen fixture; утверждённый test-only exact profile; oracle не вызывает subject evaluator/encoder. Volume proof and frozen obligation policy NativeIntegrationRequired=owner policy + native producer
FailureClass=NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED

### VOLUME-04

TestID=VOLUME-04
QualificationGroup=3
ExecutionStatus=NOT_RUN
TargetFunction=quantity oracle; HSBI_ValidateVolume; future action/volume binding (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"V1","share":"0.5","NetBig":"1.2","FarBefore":"1","FarLossProofVolume":"0.4","Obligation":"FULL_CLOSE_OLD_FAR"}
IndependentOracle=typed binding validator; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"CONFLICT","reason":"LOSS_VOLUME_SCOPE_MISMATCH","delta":0}
ExecutionEnvironment=MQL5 terminal + доступный symbol/account для OrderCalcProfit/OrderCalcMargin ONLY; dispatch disabled.
Dependencies=Broker properties/calculation mode/currency/quote receipts; реальный instrument mapping; approved cost membership; R11-C. Far money receipt with volume+identifier NativeIntegrationRequired=real broker money wrapper
FailureClass=LOSS_VOLUME_SCOPE_MISMATCH

### VOLUME-05

TestID=VOLUME-05
QualificationGroup=1
ExecutionStatus=NOT_RUN
TargetFunction=quantity oracle; HSBI_ValidateVolume; future action/volume binding (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"V1","VolumeMin":"0.05","VolumeMax":"10","VolumeStep":"0.05","GridOrigin":"0","FarBefore":"0.43"}
IndependentOracle=grid validator; 0.43/0.05=8.6 не целое, off-grid; min/max alone недостаточно.
ExpectedResult={"status":"REJECT","reason":"OFF_GRID_VOLUME","delta":0}
ExecutionEnvironment=Независимый exact decimal/rational runner либо ручной oracle, вне production; будущий запуск отдельно разрешается.
Dependencies=Frozen fixture; утверждённый test-only exact profile; oracle не вызывает subject evaluator/encoder. Broker grid receipt version NativeIntegrationRequired=native boundary/grid qualification
FailureClass=OFF_GRID_VOLUME

### MONEY-01

TestID=MONEY-01
QualificationGroup=1
ExecutionStatus=NOT_RUN
TargetFunction=exact/interval oracle; HSBI_EvaluateReserveCatchUp; future checked arithmetic (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","G":"12","A":"11","B":"1","profile":"M3_EXACT"}
IndependentOracle=exact margin component; 12000−11000−1000=0 milli-units; strict>0 false.
ExpectedResult={"M":"0","feasible":false,"reason":"NONPOSITIVE_CATCHUP_MARGIN","delta":0}
ExecutionEnvironment=Независимый exact decimal/rational runner либо ручной oracle, вне production; будущий запуск отдельно разрешается.
Dependencies=Frozen fixture; утверждённый test-only exact profile; oracle не вызывает subject evaluator/encoder. Cost/source amount receipts NativeIntegrationRequired=native strict boundary
FailureClass=NONPOSITIVE_CATCHUP_MARGIN

### MONEY-02

TestID=MONEY-02
QualificationGroup=1
ExecutionStatus=NOT_RUN
TargetFunction=exact/interval oracle; HSBI_EvaluateReserveCatchUp; future checked arithmetic (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","G":"12.001","A":"11","B":"1","Ginterval":["11.999","12.003"],"Ainterval":["10.999","11.001"],"Binterval":["1","1.001"]}
IndependentOracle=interval arithmetic; nominal12001−11000−1000=1 milli-unit; lower11999−11001−1001=−3; positive nominal недостаточен.
ExpectedResult={"nominal":"0.001","lower":"-0.003","feasible":false,"reason":"LOWER_BOUND_NOT_POSITIVE","delta":0}
ExecutionEnvironment=Независимый exact decimal/rational runner либо ручной oracle, вне production; будущий запуск отдельно разрешается.
Dependencies=Frozen fixture; утверждённый test-only exact profile; oracle не вызывает subject evaluator/encoder. Approved independent error-bound profile NativeIntegrationRequired=native rounding/error qualification
FailureClass=LOWER_BOUND_NOT_POSITIVE

### MONEY-03

TestID=MONEY-03
QualificationGroup=2
ExecutionStatus=NOT_RUN
TargetFunction=exact/interval oracle; HSBI_EvaluateReserveCatchUp; future checked arithmetic (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","G":"NaN","A":"1","B":"1"}
IndependentOracle=domain guard; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"REJECT","reason":"NONFINITE_MONEY","delta":0}
ExecutionEnvironment=MetaEditor+MQL5 terminal/build в изолированной calculation-only component среде; без trade backend.
Dependencies=R11-C numeric/codec domain; owner manifest/version; compilation baseline; tests для будущих API blocked до их появления. Numeric profile finite-domain rule NativeIntegrationRequired=native NaN/Infinity representation
FailureClass=NONFINITE_MONEY

### MONEY-04

TestID=MONEY-04
QualificationGroup=1
ExecutionStatus=NOT_RUN
TargetFunction=exact/interval oracle; HSBI_EvaluateReserveCatchUp; future checked arithmetic (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"INT64_EXACT","currency":"XTEST3","scale":1000,"postedMinor":"-9223372036854775808","operation":"max(0,-postedMinor)"}
IndependentOracle=checked arithmetic boundary; −INT64_MIN=9223372036854775808>9223372036854775807; вычислить математически arbitrary precision, subject обязан UNAVAILABLE, а не wrap.
ExpectedResult={"status":"UNAVAILABLE","reason":"INT64_NEGATION_OVERFLOW","delta":0}
ExecutionEnvironment=Независимый exact decimal/rational runner либо ручной oracle, вне production; будущий запуск отдельно разрешается.
Dependencies=Frozen fixture; утверждённый test-only exact profile; oracle не вызывает subject evaluator/encoder. Approved exact type/range profile NativeIntegrationRequired=native signed64 boundary
FailureClass=INT64_NEGATION_OVERFLOW

### MONEY-05

TestID=MONEY-05
QualificationGroup=1
ExecutionStatus=NOT_RUN
TargetFunction=exact/interval oracle; HSBI_EvaluateReserveCatchUp; future checked arithmetic (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"INT64_EXACT","left":"9223372036854775807","right":"1","operation":"add"}
IndependentOracle=checked arithmetic; 9223372036854775807+1=9223372036854775808, на1 выше максимума signed64; overflow.
ExpectedResult={"status":"UNAVAILABLE","reason":"INT64_ADDITION_OVERFLOW","delta":0}
ExecutionEnvironment=Независимый exact decimal/rational runner либо ручной oracle, вне production; будущий запуск отдельно разрешается.
Dependencies=Frozen fixture; утверждённый test-only exact profile; oracle не вызывает subject evaluator/encoder. Exact numeric manifest NativeIntegrationRequired=native overflow/cast qualification
FailureClass=INT64_ADDITION_OVERFLOW

### COST-01

TestID=COST-01
QualificationGroup=1
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_TryActualDealNet/HSBI_TryProjectedNetMoney; future CostFact inclusion validator (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","ActualDeal":{"profit":"10","commission":"-1","swap":"-2","fee":"-0.5"},"duplicateDeduction":false}
IndependentOracle=cost inclusion component; 10000−1000−2000−500=6500 milli-units; комиссия не вычитается второй раз.
ExpectedResult={"actualNet":"6.5","inclusionCountPerFact":1}
ExecutionEnvironment=Независимый exact decimal/rational runner либо ручной oracle, вне production; будущий запуск отдельно разрешается.
Dependencies=Frozen fixture; утверждённый test-only exact profile; oracle не вызывает subject evaluator/encoder. Actual deal and cost coverage receipts NativeIntegrationRequired=broker association+native
FailureClass=NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED

### COST-02

TestID=COST-02
QualificationGroup=4
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_TryActualDealNet/HSBI_TryProjectedNetMoney; future CostFact inclusion validator (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","actualNet":"6.5","CommissionIncludedInNet":"-1","requestedExtraCommissionDeduction":"1","sameCostFactID":"CF1"}
IndependentOracle=cost coverage validator; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"CONFLICT","reason":"DUPLICATE_COST_FACT","delta":0}
ExecutionEnvironment=Квалифицированный read-only broker/history/market/cost/clock provider + native receipt decoder; без orders.
Dependencies=R11-C→R11-A; provider identity/account/server/snapshot content/revision/time; negative receipt fixtures. CF1 includedIn mapping NativeIntegrationRequired=provider-backed facts
FailureClass=DUPLICATE_COST_FACT

### COST-03

TestID=COST-03
QualificationGroup=4
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_TryActualDealNet/HSBI_TryProjectedNetMoney; future CostFact inclusion validator (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","legBuffer":["1","1","1","1"],"extraCatchUpBuffer":"1","extraPurpose":"UNKNOWN"}
IndependentOracle=coverage completeness; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"UNAVAILABLE","reason":"COST_BASIS_UNBOUND","delta":0}
ExecutionEnvironment=Квалифицированный read-only broker/history/market/cost/clock provider + native receipt decoder; без orders.
Dependencies=R11-C→R11-A; provider identity/account/server/snapshot content/revision/time; negative receipt fixtures. CostBasisManifest missing buffer purpose NativeIntegrationRequired=authority/native cost integration
FailureClass=COST_BASIS_UNBOUND

### COST-04

TestID=COST-04
QualificationGroup=3
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_TryActualDealNet/HSBI_TryProjectedNetMoney; future CostFact inclusion validator (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","quoteSpreadAlreadyInCloseSide":true,"additionalSpreadSameWindow":"0.2"}
IndependentOracle=cost ownership; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"CONFLICT","reason":"SPREAD_ALREADY_INCLUDED","delta":0}
ExecutionEnvironment=MQL5 terminal + доступный symbol/account для OrderCalcProfit/OrderCalcMargin ONLY; dispatch disabled.
Dependencies=Broker properties/calculation mode/currency/quote receipts; реальный instrument mapping; approved cost membership; R11-C. Price/cost window receipt NativeIntegrationRequired=native BUY/SELL bid/ask
FailureClass=SPREAD_ALREADY_INCLUDED

### SOURCE-01

TestID=SOURCE-01
QualificationGroup=4
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_ClassifyEconomicDuplicate/HSBI_ValidateMoneyProofIdentity; future qualified provider (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"R_AUTH","physicalK":["B_MODEL","S_MODEL","1","101","DEAL_NET"],"deliveryEvents":["501","999"],"body":"same full body"}
IndependentOracle=source dedup; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"physicalSources":1,"newGrant":"0","reason":"REIMPORT_SAME_ECONOMIC_FACT"}
ExecutionEnvironment=Квалифицированный read-only broker/history/market/cost/clock provider + native receipt decoder; без orders.
Dependencies=R11-C→R11-A; provider identity/account/server/snapshot content/revision/time; negative receipt fixtures. Independent broker/server/account/deal mapping NativeIntegrationRequired=provider reconciliation
FailureClass=REIMPORT_SAME_ECONOMIC_FACT

### SOURCE-02

TestID=SOURCE-02
QualificationGroup=4
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_ClassifyEconomicDuplicate/HSBI_ValidateMoneyProofIdentity; future qualified provider (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"R_AUTH","event":"501","oldComponents":{"profit":"20","commission":"-1.875"},"newComponents":{"profit":"21","commission":"-2.875"},"sameNet":"18.125"}
IndependentOracle=body comparison; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"CONFLICT","reason":"ALTERED_COMPONENT_SAME_NET","delta":0}
ExecutionEnvironment=Квалифицированный read-only broker/history/market/cost/clock provider + native receipt decoder; без orders.
Dependencies=R11-C→R11-A; provider identity/account/server/snapshot content/revision/time; negative receipt fixtures. Original full component receipt NativeIntegrationRequired=real source provider
FailureClass=ALTERED_COMPONENT_SAME_NET

### SOURCE-03

TestID=SOURCE-03
QualificationGroup=4
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_ClassifyEconomicDuplicate/HSBI_ValidateMoneyProofIdentity; future qualified provider (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"R_AUTH","oldK":["B_MODEL","S_MODEL","1","101"],"newK":["B_MODEL","S_MODEL","2","101"],"ConsumerAccount":"1"}
IndependentOracle=identity validator; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"REJECT","reason":"WRONG_ACCOUNT_SOURCE","delta":0}
ExecutionEnvironment=Квалифицированный read-only broker/history/market/cost/clock provider + native receipt decoder; без orders.
Dependencies=R11-C→R11-A; provider identity/account/server/snapshot content/revision/time; negative receipt fixtures. Account/server receipt NativeIntegrationRequired=broker multi-account negative qualification
FailureClass=WRONG_ACCOUNT_SOURCE

### SOURCE-04

TestID=SOURCE-04
QualificationGroup=4
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_ClassifyEconomicDuplicate/HSBI_ValidateMoneyProofIdentity; future qualified provider (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"R_AUTH","SourceHistory":"MISSING","net":"18.125","runtimeConfirmed":true}
IndependentOracle=authority validator; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"UNAVAILABLE","reason":"SOURCE_AUTHORITY_MISSING","delta":0}
ExecutionEnvironment=Квалифицированный read-only broker/history/market/cost/clock provider + native receipt decoder; без orders.
Dependencies=R11-C→R11-A; provider identity/account/server/snapshot content/revision/time; negative receipt fixtures. History/association receipt absent NativeIntegrationRequired=provider unavailable path
FailureClass=SOURCE_AUTHORITY_MISSING

### FUNDING-01

TestID=FUNDING-01
QualificationGroup=5
ExecutionStatus=NOT_RUN
TargetFunction=future atomic source registry/CAS/reserve/consume/release (NOT_IMPLEMENTED); HSBI_ReserveAllocationTypes shape only
RequiredFixture={"Fixture":"R_AUTH","semantics":"SEQUENTIAL_TRANSITIONS","Free":"14.5","events":[{"id":"7001","debit":"9","expectedRevision":5},{"id":"7002","debit":"9","expectedRevision":6}]}
IndependentOracle=reference inventory component; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"afterFirst":{"C":"9","R":"0","F":"5.5","revision":6},"second":"REJECT","reason":"INSUFFICIENT_FREE","secondDelta":"0"}
ExecutionEnvironment=Native process + реальный durable journal/atomic registry test backend, controlled crash/restart и two-consumer scheduler; без trading.
Dependencies=C→A→B; approved loss-consumption/offset policy; unique source index/CAS; durable storage и reconciliation; funding никогда из projection. Registry initial receipt and durable first outcome NativeIntegrationRequired=atomic provider+journal/crash
FailureClass=INSUFFICIENT_FREE

### FUNDING-02

TestID=FUNDING-02
QualificationGroup=5
ExecutionStatus=NOT_RUN
TargetFunction=future atomic source registry/CAS/reserve/consume/release (NOT_IMPLEMENTED); HSBI_ReserveAllocationTypes shape only
RequiredFixture={"Fixture":"R_AUTH","Grant":"14.5","C":"0","R":"0","F":"14.5","reserve":"9","commitReserved":"4","releaseRemaining":"5"}
IndependentOracle=exact lifecycle component; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"C":"4","R":"0","F":"10.5","sum":"14.5"}
ExecutionEnvironment=Native process + реальный durable journal/atomic registry test backend, controlled crash/restart и two-consumer scheduler; без trading.
Dependencies=C→A→B; approved loss-consumption/offset policy; unique source index/CAS; durable storage и reconciliation; funding никогда из projection. Reservation/action/outcome receipts NativeIntegrationRequired=durable concurrency/crash
FailureClass=NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED

### FUNDING-03

TestID=FUNDING-03
QualificationGroup=5
ExecutionStatus=NOT_RUN
TargetFunction=future atomic source registry/CAS/reserve/consume/release (NOT_IMPLEMENTED); HSBI_ReserveAllocationTypes shape only
RequiredFixture={"Fixture":"R_AUTH","sameSource":true,"oldAllocation":"A101","newAllocation":"A999","newGrantRequest":"14.5"}
IndependentOracle=source/global allocation model; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"CONFLICT","reason":"ALLOCATION_ALIAS_NOT_NEW_SOURCE","delta":0}
ExecutionEnvironment=Native process + реальный durable journal/atomic registry test backend, controlled crash/restart и two-consumer scheduler; без trading.
Dependencies=C→A→B; approved loss-consumption/offset policy; unique source index/CAS; durable storage и reconciliation; funding никогда из projection. Registry physical-source index NativeIntegrationRequired=atomic multi-consumer integration
FailureClass=ALLOCATION_ALIAS_NOT_NEW_SOURCE

### FUNDING-04

TestID=FUNDING-04
QualificationGroup=5
ExecutionStatus=NOT_RUN
TargetFunction=future atomic source registry/CAS/reserve/consume/release (NOT_IMPLEMENTED); HSBI_ReserveAllocationTypes shape only
RequiredFixture={"Fixture":"R_AUTH","e1":{"amount":"9","expectedRevision":5},"e2":{"amount":"9","expectedRevision":5},"interleaving":"both read Free14.5 before commit"}
IndependentOracle=reference interleaving model; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"committedCount":1,"loser":"REVISION_CONFLICT","maxConsumed":"9"}
ExecutionEnvironment=Native process + реальный durable journal/atomic registry test backend, controlled crash/restart и two-consumer scheduler; без trading.
Dependencies=C→A→B; approved loss-consumption/offset policy; unique source index/CAS; durable storage и reconciliation; funding никогда из projection. Two durable registry outcomes NativeIntegrationRequired=native provider concurrency stress
FailureClass=NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED

### FUNDING-05

TestID=FUNDING-05
QualificationGroup=5
ExecutionStatus=NOT_RUN
TargetFunction=future atomic source registry/CAS/reserve/consume/release (NOT_IMPLEMENTED); HSBI_ReserveAllocationTypes shape only
RequiredFixture={"Fixture":"R_AUTH","oldEvent":"7001","oldBody":{"amount":"9","source":"K1"},"replayBody":{"amount":"9","source":"K1"},"oldOutcome":"COMMITTED"}
IndependentOracle=idempotency comparison; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"NO_OP","delta":"0"}
ExecutionEnvironment=Native process + реальный durable journal/atomic registry test backend, controlled crash/restart и two-consumer scheduler; без trading.
Dependencies=C→A→B; approved loss-consumption/offset policy; unique source index/CAS; durable storage и reconciliation; funding никогда из projection. Authentic original body+outcome NativeIntegrationRequired=journal replay/restart
FailureClass=NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED

### FUNDING-06

TestID=FUNDING-06
QualificationGroup=5
ExecutionStatus=NOT_RUN
TargetFunction=future atomic source registry/CAS/reserve/consume/release (NOT_IMPLEMENTED); HSBI_ReserveAllocationTypes shape only
RequiredFixture={"Fixture":"R_AUTH","oldEvent":"7001","oldAmount":"9","newAmount":"8.999"}
IndependentOracle=idempotency comparison; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"CONFLICT","reason":"EVENT_BODY_CHANGED","delta":0}
ExecutionEnvironment=Native process + реальный durable journal/atomic registry test backend, controlled crash/restart и two-consumer scheduler; без trading.
Dependencies=C→A→B; approved loss-consumption/offset policy; unique source index/CAS; durable storage и reconciliation; funding никогда из projection. Original full event receipt NativeIntegrationRequired=native codec/body binding
FailureClass=EVENT_BODY_CHANGED

### FUNDING-07

TestID=FUNDING-07
QualificationGroup=5
ExecutionStatus=NOT_RUN
TargetFunction=future atomic source registry/CAS/reserve/consume/release (NOT_IMPLEMENTED); HSBI_ReserveAllocationTypes shape only
RequiredFixture={"Fixture":"R_AUTH","Grant":"14.5","Consumed":"9","correction":"-10","newGrant":"4.5"}
IndependentOracle=reconciliation model; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"CONFLICT","reason":"CORRECTION_BELOW_COMMITTED_OBLIGATION","Free":"NOT_NEGATIVE_RECOMPUTED","delta":0}
ExecutionEnvironment=Native process + реальный durable journal/atomic registry test backend, controlled crash/restart и two-consumer scheduler; без trading.
Dependencies=C→A→B; approved loss-consumption/offset policy; unique source index/CAS; durable storage и reconciliation; funding никогда из projection. Append-only correction causation NativeIntegrationRequired=provider/journal recovery
FailureClass=CORRECTION_BELOW_COMMITTED_OBLIGATION

### FUNDING-08

TestID=FUNDING-08
QualificationGroup=5
ExecutionStatus=NOT_RUN
TargetFunction=future atomic source registry/CAS/reserve/consume/release (NOT_IMPLEMENTED); HSBI_ReserveAllocationTypes shape only
RequiredFixture={"Fixture":"R_AUTH","journalOutcome":"UNKNOWN_AFTER_CRASH","registryRevision":"UNRECONCILED","retryDebit":"9"}
IndependentOracle=recovery state validator; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"UNAVAILABLE","reason":"RESTART_RECONCILIATION_REQUIRED","delta":0}
ExecutionEnvironment=Native process + реальный durable journal/atomic registry test backend, controlled crash/restart и two-consumer scheduler; без trading.
Dependencies=C→A→B; approved loss-consumption/offset policy; unique source index/CAS; durable storage и reconciliation; funding никогда из projection. Durable intent/outcome and broker reconciliation NativeIntegrationRequired=crash at every commit boundary
FailureClass=RESTART_RECONCILIATION_REQUIRED

### SNAPSHOT-01

TestID=SNAPSHOT-01
QualificationGroup=4
ExecutionStatus=NOT_RUN
TargetFunction=future independent receipt/clock/epoch validator (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","fresh":true,"AuthorityReceipt":"NONE"}
IndependentOracle=receipt validator; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"UNAVAILABLE","reason":"SNAPSHOT_AUTHORITY_MISSING","delta":0}
ExecutionEnvironment=Квалифицированный read-only broker/history/market/cost/clock provider + native receipt decoder; без orders.
Dependencies=R11-C→R11-A; provider identity/account/server/snapshot content/revision/time; negative receipt fixtures. Independent authority receipt absent NativeIntegrationRequired=provider qualification
FailureClass=SNAPSHOT_AUTHORITY_MISSING

### SNAPSHOT-02

TestID=SNAPSHOT-02
QualificationGroup=4
ExecutionStatus=NOT_RUN
TargetFunction=future independent receipt/clock/epoch validator (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","SnapshotId":1002,"oldContent":"M_MINUS L2","newContent":"M_PLUS L2","oldReceipt":"UNCHANGED"}
IndependentOracle=content binding; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"CONFLICT","reason":"SNAPSHOT_CONTENT_CHANGED","delta":0}
ExecutionEnvironment=Квалифицированный read-only broker/history/market/cost/clock provider + native receipt decoder; без orders.
Dependencies=R11-C→R11-A; provider identity/account/server/snapshot content/revision/time; negative receipt fixtures. Full original cost/quote receipt NativeIntegrationRequired=native serialization+authority
FailureClass=SNAPSHOT_CONTENT_CHANGED

### SNAPSHOT-03

TestID=SNAPSHOT-03
QualificationGroup=4
ExecutionStatus=NOT_RUN
TargetFunction=future independent receipt/clock/epoch validator (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","clockEpoch":"E1","now":100,"issued":120,"skewMax":2,"expiry":130}
IndependentOracle=freshness component; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"REJECT","reason":"FUTURE_TIMESTAMP_OUTSIDE_SKEW","delta":0}
ExecutionEnvironment=Квалифицированный read-only broker/history/market/cost/clock provider + native receipt decoder; без orders.
Dependencies=R11-C→R11-A; provider identity/account/server/snapshot content/revision/time; negative receipt fixtures. Trusted monotonic epoch+skew policy NativeIntegrationRequired=native clock/restart/skew
FailureClass=FUTURE_TIMESTAMP_OUTSIDE_SKEW

### SNAPSHOT-04

TestID=SNAPSHOT-04
QualificationGroup=4
ExecutionStatus=NOT_RUN
TargetFunction=future independent receipt/clock/epoch validator (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","currentAccount":"1","snapshotAccount":"2","snapshotPosition":"MISSING"}
IndependentOracle=identity validator; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"REJECT","reason":"SNAPSHOT_ACCOUNT_POSITION_MISMATCH","delta":0}
ExecutionEnvironment=Квалифицированный read-only broker/history/market/cost/clock provider + native receipt decoder; без orders.
Dependencies=R11-C→R11-A; provider identity/account/server/snapshot content/revision/time; negative receipt fixtures. Position membership receipt NativeIntegrationRequired=provider actual inventory
FailureClass=SNAPSHOT_ACCOUNT_POSITION_MISMATCH

### SNAPSHOT-05

TestID=SNAPSHOT-05
QualificationGroup=5
ExecutionStatus=NOT_RUN
TargetFunction=future independent receipt/clock/epoch validator (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","restart":true,"oldEpoch":"E1","newEpoch":"E2","reconciliation":"NONE"}
IndependentOracle=epoch validator; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"UNAVAILABLE","reason":"SNAPSHOT_RESTART_UNRECONCILED","delta":0}
ExecutionEnvironment=Native process + реальный durable journal/atomic registry test backend, controlled crash/restart и two-consumer scheduler; без trading.
Dependencies=C→A→B; approved loss-consumption/offset policy; unique source index/CAS; durable storage и reconciliation; funding никогда из projection. Restart/reconciliation receipt NativeIntegrationRequired=native terminal restart
FailureClass=SNAPSHOT_RESTART_UNRECONCILED

### OBJECTIVE-01

TestID=OBJECTIVE-01
QualificationGroup=1
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_CompareCandidateTieBreak/HSBI_SolveNewFar; future MINIMUM_SAFE_V1/all-required rank
RequiredFixture={"Fixture":"NF_A_B","candidates":[["a","0.2",18,40,2,[2,2]],["b","0.3",12,50,3,[4,4]]],"allOtherGates":"MODEL_VALID"}
IndependentOracle=tuple comparator model; Оба feasible по component premises; minimum tuple N:0.2<0.3 →a; legacy Risk12<18 →b. Это две разные policy versions.
ExpectedResult={"MINIMUM_SAFE_V1":"a","legacyRiskFirst":"b"}
ExecutionEnvironment=Независимый exact decimal/rational runner либо ручной oracle, вне production; будущий запуск отдельно разрешается.
Dependencies=Frozen fixture; утверждённый test-only exact profile; oracle не вызывает subject evaluator/encoder. Frozen candidates+required proofs NativeIntegrationRequired=native qualified candidates
FailureClass=NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED

### OBJECTIVE-02

TestID=OBJECTIVE-02
QualificationGroup=1
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_CompareCandidateTieBreak/HSBI_SolveNewFar; future MINIMUM_SAFE_V1/all-required rank
RequiredFixture={"Fixture":"NF_A_B","candidates":[["x","0.1",1,20,1,[4,-1]],["a","0.2",18,40,2,[2,2]]],"cap":12}
IndependentOracle=feasibility before rank; x margin min(4,−1)=−1≤0: исключить; a min(2,2)=2>0, N0.2 среди доказанных допустимых.
ExpectedResult={"selected":"a","excluded":"x","reason":"REQUIRED_MARGIN_NEGATIVE"}
ExecutionEnvironment=Независимый exact decimal/rational runner либо ручной oracle, вне production; будущий запуск отдельно разрешается.
Dependencies=Frozen fixture; утверждённый test-only exact profile; oracle не вызывает subject evaluator/encoder. All level margin receipts NativeIntegrationRequired=native full path
FailureClass=REQUIRED_MARGIN_NEGATIVE

### OBJECTIVE-03

TestID=OBJECTIVE-03
QualificationGroup=1
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_CompareCandidateTieBreak/HSBI_SolveNewFar; future MINIMUM_SAFE_V1/all-required rank
RequiredFixture={"Fixture":"NF_TIE","N":"0.2","Risk":10,"Margin":40,"Transitions":2,"candidates":{"d":[10,1],"e":[4,3]}}
IndependentOracle=min/tuple model; m(d)=min(10,1)=1,m(e)=min(4,3)=3; равные N/risk/margin/count →−3<−1, выбираетсяe.
ExpectedResult={"selected":"e","minimumMargins":{"d":1,"e":3}}
ExecutionEnvironment=Независимый exact decimal/rational runner либо ручной oracle, вне production; будущий запуск отдельно разрешается.
Dependencies=Frozen fixture; утверждённый test-only exact profile; oracle не вызывает subject evaluator/encoder. Frozen R and exact margins NativeIntegrationRequired=native aggregator/output binding
FailureClass=NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED

### OBJECTIVE-04

TestID=OBJECTIVE-04
QualificationGroup=1
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_CompareCandidateTieBreak/HSBI_SolveNewFar; future MINIMUM_SAFE_V1/all-required rank
RequiredFixture={"Fixture":"NF_TIE","numericTuplesEqual":true,"tieProfile":"MODEL_ASCII_TOTAL_1","TieIDs":["a","b"],"orders":[["a","b"],["b","a"]]}
IndependentOracle=tie comparator component; ASCII bytes a=97,b=98,97<98 при обеих permutations. MODEL_ASCII_TOTAL_1 не утверждает реальный codec.
ExpectedResult={"selectedEachOrder":["a","a"]}
ExecutionEnvironment=Независимый exact decimal/rational runner либо ручной oracle, вне production; будущий запуск отдельно разрешается.
Dependencies=Frozen fixture; утверждённый test-only exact profile; oracle не вызывает subject evaluator/encoder. Fixture-only total order; real codec pending NativeIntegrationRequired=native UTF-8/roundtrip/version
FailureClass=NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED

### OBJECTIVE-05

TestID=OBJECTIVE-05
QualificationGroup=1
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_CompareCandidateTieBreak/HSBI_SolveNewFar; future MINIMUM_SAFE_V1/all-required rank
RequiredFixture={"Fixture":"NF_A_B","smallerCandidate":{"N":"0.1","evidence":"MISSING"},"largerCandidate":{"N":"0.2","feasible":"MODEL_TRUE"}}
IndependentOracle=search completeness; N0.1 unknown,N0.2 feasible: невозможно доказать отсутствие меньшего допустимого; qualified minimum UNAVAILABLE.
ExpectedResult={"qualifiedMinimum":"UNAVAILABLE","reason":"SMALLER_CANDIDATE_UNPROVEN","delta":0}
ExecutionEnvironment=Независимый exact decimal/rational runner либо ручной oracle, вне production; будущий запуск отдельно разрешается.
Dependencies=Frozen fixture; утверждённый test-only exact profile; oracle не вызывает subject evaluator/encoder. Complete candidate-set receipt NativeIntegrationRequired=native candidate enumeration
FailureClass=SMALLER_CANDIDATE_UNPROVEN

### OBJECTIVE-06

TestID=OBJECTIVE-06
QualificationGroup=1
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_CompareCandidateTieBreak/HSBI_SolveNewFar; future MINIMUM_SAFE_V1/all-required rank
RequiredFixture={"Fixture":"NF_A_B","allCandidates":"NO_PROVEN_FEASIBLE","requiredProofs":"COMPLETE_REJECTED"}
IndependentOracle=selection component; Feasible set пуст и полностью rejected: selection NO_SAFE_CANDIDATE; unknown≠полностью rejected.
ExpectedResult={"status":"NO_SAFE_CANDIDATE","delta":0}
ExecutionEnvironment=Независимый exact decimal/rational runner либо ручной oracle, вне production; будущий запуск отдельно разрешается.
Dependencies=Frozen fixture; утверждённый test-only exact profile; oracle не вызывает subject evaluator/encoder. Complete rejection proofs NativeIntegrationRequired=native reject propagation
FailureClass=NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED

### OBJECTIVE-07

TestID=OBJECTIVE-07
QualificationGroup=1
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_CompareCandidateTieBreak/HSBI_SolveNewFar; future MINIMUM_SAFE_V1/all-required rank
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","margins":["9","0","2"],"allOtherNumericPredicates":true}
IndependentOracle=feasibility component; min(9,0,2)=0; strict>0 false, reject.
ExpectedResult={"status":"REJECT","reason":"NONPOSITIVE_CATCHUP_MARGIN","delta":0}
ExecutionEnvironment=Независимый exact decimal/rational runner либо ручной oracle, вне production; будущий запуск отдельно разрешается.
Dependencies=Frozen fixture; утверждённый test-only exact profile; oracle не вызывает subject evaluator/encoder. Exact per-level margin fixture NativeIntegrationRequired=native boundary
FailureClass=NONPOSITIVE_CATCHUP_MARGIN

### OBJECTIVE-08

TestID=OBJECTIVE-08
QualificationGroup=1
ExecutionStatus=NOT_RUN
TargetFunction=HSBI_CompareCandidateTieBreak/HSBI_SolveNewFar; future MINIMUM_SAFE_V1/all-required rank
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","margins":["9","UNKNOWN","2"],"providedMinimum":"2"}
IndependentOracle=completeness before minimum; R из3,1 marginUNKNOWN: известные9/2 не дают min всего R; UNAVAILABLE.
ExpectedResult={"status":"UNAVAILABLE","reason":"MARGIN_SET_INCOMPLETE","delta":0}
ExecutionEnvironment=Независимый exact decimal/rational runner либо ручной oracle, вне production; будущий запуск отдельно разрешается.
Dependencies=Frozen fixture; утверждённый test-only exact profile; oracle не вызывает subject evaluator/encoder. Frozen R and missing receipt NativeIntegrationRequired=native output contract
FailureClass=MARGIN_SET_INCOMPLETE

### COMPATIBILITY-01

TestID=COMPATIBILITY-01
QualificationGroup=2
ExecutionStatus=NOT_RUN
TargetFunction=future result/plan versioned decoder/adapter (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"LEGACY_RESULT","legacySchema":"HSBI_BASE_e68","returnTransitionLoss":"3","aggregateMaximum":"12","kindDeclared":false}
IndependentOracle=adapter validation; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"qualifiedWorst":"UNAVAILABLE","reason":"LEGACY_METRIC_KIND_UNBOUND"}
ExecutionEnvironment=MetaEditor+MQL5 terminal/build в изолированной calculation-only component среде; без trade backend.
Dependencies=R11-C numeric/codec domain; owner manifest/version; compilation baseline; tests для будущих API blocked до их появления. Pinned source/schema proof NativeIntegrationRequired=native persistence/adapters
FailureClass=LEGACY_METRIC_KIND_UNBOUND

### COMPATIBILITY-02

TestID=COMPATIBILITY-02
QualificationGroup=2
ExecutionStatus=NOT_RUN
TargetFunction=future result/plan versioned decoder/adapter (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"LEGACY_PLAN","oldObjective":"RISK_FIRST","requestedObjective":"MINIMUM_SAFE_V1","planReceipt":"OLD_UNCHANGED"}
IndependentOracle=version gate; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"UNSUPPORTED","reason":"PLAN_OBJECTIVE_VERSION_MISMATCH","delta":0}
ExecutionEnvironment=MetaEditor+MQL5 terminal/build в изолированной calculation-only component среде; без trade backend.
Dependencies=R11-C numeric/codec domain; owner manifest/version; compilation baseline; tests для будущих API blocked до их появления. Old immutable plan receipt NativeIntegrationRequired=native restart/migration
FailureClass=PLAN_OBJECTIVE_VERSION_MISMATCH

### COMPATIBILITY-03

TestID=COMPATIBILITY-03
QualificationGroup=2
ExecutionStatus=NOT_RUN
TargetFunction=future result/plan versioned decoder/adapter (NOT_IMPLEMENTED)
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","ResultSchemaVersion":"V99","ProofSchemaVersion":"CR09_PROOF_V1"}
IndependentOracle=schema decoder; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"UNSUPPORTED","reason":"UNKNOWN_RESULT_SCHEMA","delta":0}
ExecutionEnvironment=MetaEditor+MQL5 terminal/build в изолированной calculation-only component среде; без trade backend.
Dependencies=R11-C numeric/codec domain; owner manifest/version; compilation baseline; tests для будущих API blocked до их появления. Approved version manifest NativeIntegrationRequired=native codec compatibility
FailureClass=UNKNOWN_RESULT_SCHEMA

### SAFETY-01

TestID=SAFETY-01
QualificationGroup=1
ExecutionStatus=NOT_RUN
TargetFunction=D06-A arithmetic/future FinalClose authority; sticky journal model; HSBI_EvaluateNewFarGates
RequiredFixture={"Fixture":"D06_A","R_all":"40","O_phys":"-4","C_rem":"1","I":"50","H_in":"4","MinimumProfit":"10","H_gate":"5","Tolerance":"1"}
IndependentOracle=exact formula model; E=40−4−1=35; RecoveryA=35−4−50=−19; threshold10+5+1=16; −19<16.
ExpectedResult={"E":"35","RecoveryResultA":"-19","threshold":"16","ordinaryFinalClose":false,"reason":"RECOVERY_RESULT_BELOW_THRESHOLD"}
ExecutionEnvironment=Независимый exact decimal/rational runner либо ручной oracle, вне production; будущий запуск отдельно разрешается.
Dependencies=Frozen fixture; утверждённый test-only exact profile; oracle не вызывает subject evaluator/encoder. Initial group/cost/headroom receipts NativeIntegrationRequired=native FinalClose/source integration
FailureClass=RECOVERY_RESULT_BELOW_THRESHOLD

### SAFETY-02

TestID=SAFETY-02
QualificationGroup=5
ExecutionStatus=NOT_RUN
TargetFunction=D06-A arithmetic/future FinalClose authority; sticky journal model; HSBI_EvaluateNewFarGates
RequiredFixture={"Fixture":"D05","orderedFills":["-15","100"],"cap":"12","priorSticky":false,"reset":"NONE"}
IndependentOracle=sticky history reference model; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"currentNet":"85","currentLoss":"0","historicalBreach":true,"sticky":true,"continuation":"BLOCKED"}
ExecutionEnvironment=Native process + реальный durable journal/atomic registry test backend, controlled crash/restart и two-consumer scheduler; без trading.
Dependencies=C→A→B; approved loss-consumption/offset policy; unique source index/CAS; durable storage и reconciliation; funding никогда из projection. Independent ordered history; reset authority unbound NativeIntegrationRequired=journal/restart authority/native
FailureClass=NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED

### SAFETY-03

TestID=SAFETY-03
QualificationGroup=1
ExecutionStatus=NOT_RUN
TargetFunction=D06-A arithmetic/future FinalClose authority; sticky journal model; HSBI_EvaluateNewFarGates
RequiredFixture={"Fixture":"ERR038","shortLots":"0.1","multiplier":"1","priceMoveAdverse":"UNBOUNDED","positions":1}
IndependentOracle=symbolic loss formula; short loss(v,K,ΔP)=0.1×1×ΔP; при ΔP→∞ loss→∞. Конечный native sample это не опровергает.
ExpectedResult={"moneyLossBound":"NOT_PROVEN","reason":"UNBOUNDED_PRICE_MOVE"}
ExecutionEnvironment=Независимый exact decimal/rational runner либо ручной oracle, вне production; будущий запуск отдельно разрешается.
Dependencies=Frozen fixture; утверждённый test-only exact profile; oracle не вызывает subject evaluator/encoder. Explicit bounded-market/execution assumptions absent NativeIntegrationRequired=separate risk proof, not native sufficient
FailureClass=UNBOUNDED_PRICE_MOVE

### SAFETY-04

TestID=SAFETY-04
QualificationGroup=6
ExecutionStatus=NOT_RUN
TargetFunction=D06-A arithmetic/future FinalClose authority; sticky journal model; HSBI_EvaluateNewFarGates
RequiredFixture={"Fixture":"R2-F-PROJECTION/M_PLUS","allMarginsPositive":true,"Tmax":"13","cap":"12","controlFarLoss":"3"}
IndependentOracle=gate component; Полный original input/body и независимый reference predicate; subject flags/digest не oracle. Expected literal ниже.
ExpectedResult={"status":"REJECT","reason":"TRANSITION_CAP_EXCEEDED","delta":0}
ExecutionEnvironment=Нативная integration сборка с реальными calculation-only wrappers, original receipts, trace каждого branch, dispatch=false.
Dependencies=C→A→B→D и E prerequisites; selected semantics/required set; complete provider/profile/actual residual evidence; native branch instrumentation. Complete basket maximum proof NativeIntegrationRequired=native rejection before safe array
FailureClass=TRANSITION_CAP_EXCEEDED

## Зависимости отсутствующих компонентов и реальные acceptance probes

Группа2 LEVEL: current producer может дать valid prefix без frozen required manifest. Сначала нужен approved manifest validator; затем tests cover пустой R, duplicates/body conflict/order/tail, unknown schema. Нативные NaN/Infinity отдельно проверяются на ABI/compiler build; NaN constructor/repr документируется, не вставляется как обычная строка в double.

Группа3: capture actual instrument properties/calculation mode/quote sides/account currency. Independent broker oracle — отдельный validated invocation OrderCalcProfit/OrderCalcMargin с literal volume/opens/close-side и signed costs, плюс ручная проверка для символов, где payout формула доказана. Это calculation-only, не history fill. Реальный symbol должен позволять fixture либо case BLOCKED_SYMBOL_MAPPING; невозможные synthetic broker inputs не дают failed subject arithmetic.
VOLUME-04 обязателен negative mismatch: obligation full old Far1, proof volume0.4 →CONFLICT до money permission. COST-04 требует доказать quote spread уже включён в price, затем повторный same-window spread receipt отвергается.

Группа4: source K содержит broker/server/account/immutable posting/component kind, original full body, position/action/cycle association. SOURCE-01 два delivery events для одного K не два grants; SOURCE-02 profit20/commission−1.875 и profit21/commission−2.875 оба net18.125, но разные bodies →CONFLICT.
Snapshot identity/content/time/epoch проверяет независимая authority, не reconstructed expected из самого caller. Clock now100,issued120,skew2 не fresh:20>2. Unknown account/provider/restart state не заменять0/true.

Группа5: WAL/intent/outcome durability, source registry revisions и полные bytes before/after. Crash до persist intent, после intent, до/после CAS, после effect до receipt, при release и replay. После unknown outcome новый debit запрещён до reconciliation. Два независимых consumers одновременно читают rev5/free14.5 и пытаются debit9; расписания read-read-commit-commit и перезапуск проигравшего обязаны дать≤1commit. Atomicity/durability нельзя доказать in-memory bool fixture.
Sticky D05 breach после первого−15 не стирается поздней+100; reset authority не назначена. EpochE1→E2 без reconciliation блокирует freshness. Настоящий backend отсутствует: эти зависимости BLOCKED, не выполненные тесты.

Группа6: записать фактический call graph и достигнутые guards/branches. Для TL001 successful return требуется trace selected safe candidate с aggregate loss и Far loss отдельно. Пустой safe[] из missing provider не проверяет return151. Для all-required отказа доказать, что отказ вызван конкретным required negative margin, а не setup stale.
VOLUME-02 проверяет oldFar ID исчез, CoreID сохранён, closedOldFar1≠compression0.6. Дополнительно обязательны physical ledger S1/S2/S3, два promotions с чередованием direction/open basis, actual residual≠requested, partial/delayed completion и zero managed positions при final completion. Эти probes расширяют execution prerequisites, не увеличивают заявленные67 исторических спецификаций.

## Формат будущего artifact и критерий остановки

Каждый результат сохраняет TestID, source/tree/blob SHA, compiler/terminal/build/OS, contract/fixture/numeric/codec/provider versions, полный input receipt, independent expected, observed output, reached branch, statuses/log, states before/after, dispatch attempts0 и financial delta. PASS возможен только после фактического запуска нужного target branch и oracle comparison; здесь все67 NOT_RUN.

STOP при изменении базы, source mapping, неподписанном concrete contract, unknown costs/provider/profile, nondeterministic codec, mutation survivor, несогласованном physical lineage, no-trade guard change либо attempted dispatch. Не менять frozen historical expected ради зелёного результата. Нужна новая versioned suite при изменении semantics.
