# HSBI-03F-R2 — Спецификация TL/CU test vectors

Version=**HSBI-03F-R2-V1**. SourceCommitSHA=`ae367ff2925da4d845a413326c840fe468ff451b`.
Repository=`ic8812825-maker/chatgpt.com-codex`; Branch=`work`.
Все относительные пути относятся к `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/`.

D-06 A и companion NewFar A выбраны владельцем в беседе. FormalApprovalReceipt=NOT_REGISTERED. Остальные 15 денежных решений остаются AWAITING/BLOCKED; CR09_FULL_APPROVAL=AWAITING.
EvidenceClass: CONFIRMED_STATIC/STATIC_CONFIRMED — чтение исходного кода; MATH_DERIVED — математический вывод при указанных предпосылках; TEST_SPECIFIED_NOT_RUN — заданный, но не выполненный тест; HISTORICAL_TEST_RESULT — прежний artifact.
Native, compile, runtime, mutation, crash и concurrency испытания на этом этапе не запускались.

EXECUTION_MODE=GITHUB_MCP_REMOTE_ONLY; LOCAL_FILE_OPERATIONS=0; NATIVE_MQL5_TESTS=NOT_RUN.
PRODUCTION_CHANGED=NO; IMPLEMENTATION_ALLOWED=NO; R11_IMPLEMENTATION_ALLOWED=NO; BROKER_DISPATCH_ALLOWED=NO; REAL_TRADING_ALLOWED=NO.
Новый contract с пометкой PROPOSED не считается утверждённым или реализованным. UNAVAILABLE означает отсутствие обязательного evidence, CONFLICT — противоречие, REJECT — известное нарушение. Все три результата запрещают новый финансовый эффект. NO_OP требует проверки полного прежнего body/receipt.

Критические SourceBlobSHA:
- `Include/Planning/HSBI_NewFarSolver.mqh`: `3d19eccd6cd318b9b4591e2bc0ccaa95f661930d`.
- `Include/Planning/HSBI_FutureSmallProofAggregator.mqh`: `4678ae152960e98b9f398b4497786061d7e8a524`.
- `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh`: `87a8b7e97727ce6e47c2a2f0abc3e237f6203204`.

Status=TEST_SPECIFIED_NOT_RUN.
VectorSetVersion=HSBI-03F-R2-VECTORS-V1.
Все expected — независимые математические либо source-derived ожидания. Ни один native runner, broker call, compile или mutation здесь не исполнялся.
Источники: NewFarSolver94–152;FutureSmallSolver57–149;Aggregator23–58;ReserveCatchUpEvaluator24–76;NewFarGateTypes6–16;Docs04:15,24;Docs30:3–7;selected objective03E:24–42;future R2 contract PROPOSED.
В каждом case источники и достижимость указаны отдельно; соответствие proposed ALL_REQUIRED_V1 не выдаётся за full CR09 approval.

## 1. Полные общие fixtures и правила наследования

Case input = именованный fixture + ТОЛЬКО перечисленные overrides. Неуказанные данные наследуются из fixture без угадывания. Значения amounts в main units, profileM3 S1000; внутренний expected oracle — целые minor units. Полные per-level legs/commissions приведены в [mathproofs](HSBI_03F_R2_TRANSITION_CATCHUP_MATH_PROOFS_RU.md).

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

## 2. TL cases — вход, expected,инвариант, достижимость

### TL-01

Input=TL_BASE1;independent component proofs предпосланы; all required levels2,controlL1,cap12.
Formula Tmax12,A_control3.
Expected new schema:MaximumProjectedTransitionLoss12,ControlLevelAbsoluteFarLoss3;cap equality passes.
Current source:при достижении SELECTED returntransitionLoss3,поскольку 151 копирует Farfield. Нельзя отображать его как checkedworst12.
Invariant:outputmetrickind и proofscope совпадают.
Source:Basket17,NewFar131/138/141/151.
Reachability:MODEL_ADMISSIBLE;successfulnativebranch не продемонстрирована; top injection запрещён 99.
EvidenceClass=MATH_DERIVED+STATIC_CONFIRMED;Execution=TEST_SPECIFIED_NOT_RUN.

### TL-02

Input=TL_BASE2;cap5,Tmax3,A_control12.
Expected transitioncap passes по 3,Far coverage отдельно по 12;newresult содержитоба числа. Treating12 astransitioncapmetric даст ложный отказ.
Source и invariant как TL01;scope двух levels.
Reachability:MODEL_ADMISSIBLE,fullsolverBLOCKED_BY_MISSING_EVIDENCE.
EvidenceClass=MATH_DERIVED+STATIC_CONFIRMED;Execution=TEST_SPECIFIED_NOT_RUN.

### TL-03

Input=M_PLUS,EXPLICIT_CONTROL_LEVEL2,requiredlevels1/2/3,H12.
Expected worstT=L1,Tmax12,controlL2,A2=9.2;newresultbinding хранитоба level IDs;minimum all margins1.
Current conditional control2margin1 и currentlot0.48>candidate0.4 проходят. Financial authority всёравнонет.
Source:Aggregator44,50–53;NewFar118–141.
Reachability:MODEL_ADMISSIBLE asfiniteproducer;nativeNOT_RUN.
Auxiliary TL03-INVALID:caller aggregateDTO T3/7/12 с recovery−3/−7/−12 и flagsvalid — publicaggregator можетструктурнорассматривать, но genuineproducer отвергает recoverydecrease;не fullsolvercounterexample.
EvidenceClass=MATH_DERIVED+STATIC_CONFIRMED;Execution=TEST_SPECIFIED_NOT_RUN.

### TL-04

Input=M_MINUS,WORST_CASE→L1,H12,required3.
Expected ALL_REQUIRED_V1 rejection,minMargin−4;currentcontrolmargin9 сам по себене all-levelproof.
Source:NewFar127onecall/138flag/140singlemargin;Aggregator без minfield.
Reachability:coherentmonetarymodel,controlrouteconditionallyadmissible;неутверждён fullnativefalsePASS.
EvidenceClass=MATH_DERIVED+STATIC_CONFIRMED;Execution=TEST_SPECIFIED_NOT_RUN.

### TL-05

Input=TL_BASE1,butouter4caps=(11,11,11,11),futurecap20;Tmax12,A3.
Expected candidate rejected before safe[];ifonlycandidate,noSELECTED;invaliddefault0notproof. Чтобы точно реализовать 13>12 вариант: raiseL1Smallcommission36→37→basket−13,Tmax13,H12;остальное TL_BASE1.
Source:NewFar131–146;NewFarGate15.
Invariant:Far scalar cannot bypass existing basketcap. Reachability:sourceconditionalrejection;realnativeNOT_RUN.
EvidenceClass=MATH_DERIVED+STATIC_CONFIRMED;Execution=TEST_SPECIFIED_NOT_RUN.

## 3. CU cases — все inputs наследуются точно из именованного fixture

| ID | Fixture+exactoverride/предусловие | Formula/expected | Invariant+source | Текущаядостижимость/EvidenceClass |
|---|---|---|---|---|
| CU-01 | M_PLUS,required3,ALL_REQUIRED_V1;othernecessaryproofs assumedvalid inreferenceonly | margins9/1/2,min1>0;CatchUpPredicateTRUE;ifothergatestrulyPASS,previewfeasible;financialauthorityNO | strictallquantifier;selectedobjective m(c),futurecontract§6 | MODELMATH;currentWORST_CASE seesonlyL1;MATH_DERIVED,NOT_RUN |
| CU-02 | M_ZERO,required3,H12 | margins9/0/2,min0→REJECT | strict>0 not≥0;ReserveEvaluator75 | exactmathzero;nativebinary64signunverified;MATH_DERIVED,NOT_RUN |
| CU-03 | M_MINUS,required3,H12 | margins9/−4/2→REJECT | sameallrequiredrule | coherentmodel;nofullnativePASSclaim;MATH_DERIVED,NOT_RUN |
| CU-04 | M_MINUS,WORST_CASE | argmaxT=L1,argminMargin=L2 | independentextrema;Aggregator44/50 vsmarginformula | MATH_DERIVED+STATIC_CONFIRMED;NOT_RUN |
| CU-05 | M_PLUS,L2 moneyproof absent,statusUNAVAILABLE,moneyIncludedfalse;requiredset unchanged | ProofCompletenessINCOMPLETE,UNAVAILABLE;no minfromremaininglevels | FS/aggregate31–39;newcontract§5 | currentproducer/aggregate blocks;solver maymap toNO_SAFE,необязательно returnUNAVAILABLE enum;STATIC_CONFIRMED,NOT_RUN |
| CU-06 | F-CASH,SEQUENTIAL;event7001 debit9,expectedrev5;event7002 debit9,expectedrev6 afterfirst | firstC9/F5.5/rev6;secondREJECTinsufficient,delta0 | Grant=C+R+F;no globalfundingrefresh | referencefixtureonly,backendnativeNOT_RUN;MATH_DERIVED |
| CU-07 | M_PLUS; L2 SnapshotId1002→2002; replacement authority receipt отсутствует; legacy expectedPlanDigest="" | UNAVAILABLE/CONFLICT по authority binding; требуется revalidation, не автоматический PASS | Snapshot/content/plan binding; NewFar35–59,106; D13 proposal | При пустом expected digest legacy mismatch check пропущен; независимый receipt обязателен. STATIC_CONFIRMED; NOT_RUN |
| CU-08 | M_PLUS,currentStateRevision6,proof/plan/consumptionrev5 unchanged | staleproofCONFLICT;financialdelta0 | expectedrevision/immutableplan;NewFar104–106 | currentplanidentitymismatchblocks;no claimCASnative;STATIC_CONFIRMED,NOT_RUN |
| CU-09 | M_PLUS,positiveprojectionnumbers,actualsource/providerreceiptsNONE | PREVIEW_ONLY/BLOCKEDforfunding,notactualreserve | D02/D13/D14;Reserveproof26 requiresprojected | mathreachablepreview;authoritycontractmissingnotfixedbyflags;STATIC_CONFIRMED+MATH_DERIVED,NOT_RUN |
| CU-10 | M_PLUS;VolumeMin=VolumeStep0.025;maximumDepth3;F_after0.2/0.1/0.05;RequiredIDs1,2,3,4;provided1,2,3;TailRequirement=EXACT_REQUIRED_4;L4dataUNKNOWN | UNAVAILABLE/UNPROVEN,nozeroL4/noinfiniteclaim | explicitrequiredset;Docs04:33–36,pendingCR09 | current provenDepth3/conservative bound не доказывает external requiredL4;STATIC_CONFIRMED,NOT_RUN |

Во всех CU execution status=TEST_SPECIFIED_NOT_RUN. Табличное NOT_RUN неисторический FAIL/PASS.

Дополнения, нужныенезависимойдоменнойприёмке:
- CU02-EXACT:allocatedG12,A11,B1→0 ровно; strictgate rejects evenwithoutdecimalrounding.
- CU06-REPLAY:event7001samebody/receipt→NO_OP,не debit;alteredamount8.999sameevent→CONFLICT.
- CU06-ALIAS:sameK/новый AllocationKeyA999 не grantrefresh;CONFLICT либо UNAVAILABLE если sourcecompletenessunknown.
- CU07-CONTENT:keepSnapshotId1002,changeFar/SmallfeesM_MINUS→M_PLUS,keepoldreceipt→CONFLICTeveniftotalbasketunchanged. Nativeproofmustbindfulloriginalcostcontent.
- CU-VOLUME:M_PLUS,controlFINAL_L3:current.8×netBig0.3=0.24≤candidate0.4rejects;proposedperlevelF0.1passeslotpredicate. Нельзя loop копироватьстарый ci без binding.
- CU-SOURCEORIGIN:historicalOriginPlan1,currentconsumePlan9validassociation—нет reject лишьиз-заразных IDs;нужнаявная causation,не guess.

CU10: min/step0.025 оставляет Far0.05 выше min; terminal=false, теоретическая q-depth4. Prefix3 может иметь conservative bound, но не доказывает точный required L4.
CU07: PLAN_DIGEST_MISMATCH от изменения ID доказуем только при отдельно frozen nonempty old digest. При пустом legacy expectedPlanDigest такой отказ не обещается; proposed authority rule требует новый receipt/revalidation.

## 4. Какготовить nativeacceptance,неподменяя scope

Component numeric/aggregator tests могут использовать отдельно утверждённые frozenfixtures и literalexpected. Их PASS не authenticbrokerfunding.
Currenttopsolver:runtimeUNIT_TEST/injectedproofsreject99,CandidateMoneyEvaluator14 также rejectsinjection. Нельзяэтот ранний отказвыдатьзапроверкууспешногопути 151.
Native integration должен получить реальные calculation-only brokerinstrument/cost/risk/margin/source/snapshot/profile receipts в разрешённом режиме; никакого dispatch. При fakeSymbolMODEL_LINEAR_1 nativeOrderCalcProfit можетбыть UNAVAILABLE;это EXPECTEDinfrastructureboundary,неположительный counterexample к selectedpath.
Futuretestartifact:sourceSHA,compiler/terminalbuild,fixture/vectorID,exactinputs,profile/receiptversions,expected/actual/status/log,whichbranchreached,financialstatebefore/after.
No source edits/testfiles/runners созданы. Native,crash,concurrency,providerqualification ещё NOT_RUN.
Приёмка спецификации: все TL01–05/CU01–10 имеютполные inheritedinputs,формулу, expected,scope/source/reachability;арифметикапересчитываетсянезависимо, не subjectencoder/evaluator.
Связи: [math](HSBI_03F_R2_TRANSITION_CATCHUP_MATH_PROOFS_RU.md),[ERR018](HSBI_03F_R2_ERR018_SOURCE_LEVEL_AUDIT_RU.md),[futurecontract](HSBI_03F_R2_TRANSITION_CATCHUP_CONTRACT_V1_RU.md),[readiness](HSBI_03F_R2_DEPENDENCY_AND_READINESS_MATRIX_RU.md).
