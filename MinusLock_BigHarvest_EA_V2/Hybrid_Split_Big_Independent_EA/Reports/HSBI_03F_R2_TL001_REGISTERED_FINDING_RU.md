# HSBI-03F-R2 — TL001: audit-only зарегистрированная карточка

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

Status=AUDIT_ONLY_REGISTERED_FINDING_RECORD.
FindingId=HSBI-03F-TL-001
Classification=P1_PROPOSED
Evidence=CONFIRMED_STATIC
OfficialErrId=NOT_ASSIGNED
ProductionFix=NOT_IMPLEMENTED
NativeTests=NOT_RUN
RegistrationMode=NEW_REPORT_ONLY
RegistrationRecord=HSBI_03F_R2_TL001_REGISTERED_FINDING_RU.md

Слово REGISTERED относится только к этому новому audit package. Не меняетсяисторическийреестр, не присваивается ERR051,не подделывается ownerreceipt. Publication фактподтверждаетсяотдельным remote verification ответомпослезаписи.

## Подтверждённый defect и source

Include/Planning/HSBI_NewFarSolver.mqh:
-28–33:HSBI_NewFarSolverResult.transitionLoss.
-118–127:controllevel,cifarLoss=max(0,−control.farLossProof.netMoney),singleCatchUp.
-131–134:gate.transitionLoss=aggregate.maximumTransitionLoss;failedgate→continue.
-138:c.aggregateWorstTransitionLoss=aggregate.maximumTransitionLoss.
-141:c.farLossIncreaseMoney=catchResult.farLossIncreaseMoney.
-146:после gates candidate добавляется safe[].
-149–151:selectedsafe;result.transitionLoss=selected.farLossIncreaseMoney.

Фактические definitions:
T_l=max(0,−BasketNet_l).
T_max=max_l T_l.
A_c=max(0,−FarNet_c).
ReturnedtransitionLoss=A_c приуспешном selectedpath,не T_max.

Include/Money/HSBI_BasketMoneyEvaluator.mqh:17 (SourceBlobSHA=4bea204e91a4719b4b24086304cb51051909a7de) даётразныеформулы.
Include/Planning/HSBI_FutureSmallSolver.mqh:87,135 передаёт basketloss;aggregate:44 берёт maximum.
ReserveCatchUpEvaluator:39 сохраняет inputFarLoss;непревращаетегов basketloss.
CandidateSourceBlobSHA=758f1c89cf75701d3616dabec2fcb06413ee2d4a.
GateSourceBlobSHA=7d50669bda8ff2d000566ad7a38281140a77ae83;HSBI_EvaluateNewFarGates:11–15 проверяет cap.

## Математическоеопровержениеэквивалентности

FarNet−3,otherlegs−9→BasketNet−12,T12,A3.
FarNet−12,otherlegs+9→BasketNet−3,T3,A12.
Ни T=A,ниуниверсальныйпорядокмеждуниминеверны.
Болееполные grid/costfixturesTL01/TL02 в testspec;алгебраическаят a блицанерезультатполного solver/native.
Цепочка A_c→ci→catchResult→candidate→selected→result точнаповидимымприсваиваниям. Неверносчитать selectedFar и controlFar независимымитремянеизвестными; подменяетсяименно T_max.

## Downstreamcontract:факты, не предположения

Повторный remote symbolscan на SourceCommitSHA:74productionmodules и 11MQL/C++testsource;comments/strings исключеныиз symbolmatches. Scopedpath/blobmanifest в finalverdict.
HSBI_SolveNewFar/HSBI_NewFarSolverResult внешних productionrefs NOT_FOUND_IN_SCANNED_SCOPE.
Safetyconsumer result.transitionLoss:NOT_FOUND_IN_SCANNED_SCOPE.
Persistenceconsumer:NOT_FOUND_IN_SCANNED_SCOPE.
UI/diagnosticsconsumer:NOT_FOUND_IN_SCANNED_SCOPE.
SolverResult→RuntimeDecisionadapter:NOT_FOUND_IN_SCANNED_SCOPE.
Mainincludeclosure16files не containsNewFarSolver;main.mq5:19–43disabledpolicy,NoTradeStub,diagnostics.
RuntimeDecisionTypes:11–17 принимает candidate/aggregate отдельно; RuntimeDecisionValidator:19–28 возвращаетих, ноне принимает HSBI_NewFarSolverResult. Это не доказанный adapter.
Tests/MQL5/HSBI_Skeleton_Tests.mq5:180–195,226,484 вызывают solver;чтения result.transitionLoss не найдено. TestsT208:288 проверяет aggregate,неего returnmapping.
Не объявляетсяневозможностьвнешнегопотребителявне scannedscope;native/type-resolvedglobalgraph нестроился.

## Последствия и severity

Подмена можетзанижатьили завышать reportedworstloss ивбудущейинтеграцииввестивошибку safety/persistence/UI. Это P1_PROPOSED publicmonetaryoutputcontract,непросто cosmeticP2.
Прямой capbypass отстроки 151 НЕ ДОКАЗАН: gate использует T_max ДОпомещения safe[];T13,H12reject независимоот A3. Еслиединственный candidate отклонён, result.valid=false/defaultzero небезопасный loss0.
Длянового P0 нужно отдельно доказатьсоответствующийопасный productionpath/consumer/effect. Сейчасего нетв scannedscope;P0_TOTAL14unchanged.

## Связисисторическими ERR

Reports/HSBI_AUDIT03_ALL_ERRORS_RU.md:
ERR013205–216:expectedproof из caller/samepresentedidentity.
ERR018265–276:maxtransition≠minCatchUp;отдельная all-level проблема.
ERR043565–576:absolutevsincrementalFarLoss.
ERR045589–600:selectedNvsactualresidual.
TL001—отдельный outputmapping,связаннеравенэтимчетырём. ERR038505–516 остаётся OPEN;boundedlots не boundedmoney.

## Proposedfuturefixcontract

Для validselectedresult:
MaximumProjectedTransitionLoss=selected.aggregateWorstTransitionLoss,с levelset,capbasis,profile,revision и proofreceipt.
ControlLevelAbsoluteFarLoss=selected.farLossIncreaseMoney отдельноподдругимименем.
LegacytransitionLoss без schema непереосмыслятьмолча. ActualTransitionLoss —signedactualfills операции, отдельноотобоих projectionmetrics.
Failurevaluesinvalid,не proofzero. Body/receipt/digest/compatibilityversion проверять; all-levelCatchUp добавляетсяотдельнымутверждаемым contract,неодним mappingfix.
Полнаяспецификация: [HSBI_TRANSITION_AND_CATCHUP_CONTRACT_V1](HSBI_03F_R2_TRANSITION_CATCHUP_CONTRACT_V1_RU.md),StatusPROPOSED.

## Acceptance,unresolved

Нужны TL01…TL05,return/proofbinding,negativezero/nonfinite/schema/replaycases,allfutureadapters,strictcapguardpreservation,nativequalification. TEST_SPECIFIED_NOT_RUN.
Неисправлены production/API,не утверждены schema/provider/CR09/legacy. P1 карточказарегистрированатольковновом report.
Связи: [ERR018](HSBI_03F_R2_ERR018_SOURCE_LEVEL_AUDIT_RU.md),[proofs](HSBI_03F_R2_TRANSITION_CATCHUP_MATH_PROOFS_RU.md),[vectors](HSBI_03F_R2_TEST_VECTOR_SPECIFICATION_RU.md),[readiness](HSBI_03F_R2_DEPENDENCY_AND_READINESS_MATRIX_RU.md).
