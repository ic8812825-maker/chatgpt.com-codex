# HSBI-03F-R2 — Зависимости и readiness matrix перед R1.1

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

Status=ALL_IMPLEMENTATION_GATES_BLOCKED.
GateManifestVersion=HSBI-03F-R2-READINESS-V1.

## Источники

Reports/HSBI_R11_P0_DEPENDENCY_PLAN_RU.md:20–223, SourceBlobSHA=8ac398a8dae93dbcbc28e2fbeddc70a7501b2f76: исходные allowlists/stopconditions A…E.
Reports/HSBI_03E_R11_GATE_MATRIX_RU.md:12–58,SourceBlobSHA=818bc9688f3d622f7bbfa8d804b29df1ba21a575.
Reports/HSBI_03E_CONTRACT_DEPENDENCY_RECONCILIATION_RU.md:versioned bundles,SourceBlobSHA=ceb6440e45dee9a67dab478dfbc48d4325e8db3f.
Reports/HSBI_03D_P0_REMEDIATION_CROSSWALK_RU.md:14 P0,SourceBlobSHA=6a72362e588506f310b31d6fb9437edaeb6ba7a6.
Production dependency roots: EconomicLedgerTypes6–12,AllocationLedgerTypes5–10,ReserveAllocationTypes15–30,CostModel11–18,FutureSmallSolver57–149,NewFarSolver94–152,NewFarCandidate26–40,Aggregator23–58,RuntimeDecisionTypes11–17/Validator19–28,ExecutionJournal18–43,PersistenceInterface5–7. Полные paths/blobSHA в [sourceinventory](HSBI_03F_R2_FINAL_VERDICT_RU.md).

## 1. Что изменил owner selection

D06SelectionGate=CONFIRMED_IN_CONVERSATION(A,точный sourceblob).
ObjectiveSelectionGate=CONFIRMED_IN_CONVERSATION(MINIMUM_SAFE_V1).
Other15MoneyDecisionGate=AWAITING/BLOCKED.
FormalApprovalReceipts=NOT_REGISTERED.
Нельзя ни игнорировать сделанный выбор, ни считатьегоавтоматическим approval остальных 15/native/providercontracts. Выбор A не устанавливает CostBasisManifest,Hvalues,Initialmembership или realSourceFacts.

## 2. Проверяемые gates

| Gate | Точный критерий PASS | Текущий статус |
|---|---|---|
| P-POLICY | selectedexactD06/objective + необходимые approvals всех зависимых CanonicalIDs и fullCR09/requiredlevelsemantics | Частично selected;остальные 15AWAITING→BLOCKED |
| N-NUMERIC | actualcurrency/posting/grid/profile,errorbounds,range,enumsets,codec/version/caps independently verified | EVIDENCE_BLOCKED;нет universalfixturedefaults |
| N-NATIVE | exactbuild/source native logs по zero/negative/overflow/codec/grids и TL/CUcausalbranches | NOT_RUN→BLOCKED |
| A-SOURCE | independent broker namespace/history+EAassociation,immutablebody,origin/currentcontext distinctions | PROVIDER_BLOCKED |
| S-SNAPSHOT | producer/verifiertrust,contentreceipt,clock/skew/expiry/restartepoch,consistentcut | PROVIDER_BLOCKED |
| B-REGISTRY | singlephysicalsourceinventory,exactgrants/C/R/F,aliases,perownerreserve,atomicreceipt/revision | BLOCKED:backend/completenessnotqualified |
| J-DURABLE | bodyvalidationbeforeNO_OP,atomicstate+receipt,unknown/partial/crash/restartreconciliation,sticky/resetpreservation | BLOCKED:productionstub/no nativecrashtests |
| C-ALLLEVEL | frozenrequiredIDset,perlevelreceipt,boundF_l/cost/source,minmargin>0,applicableprefixfunding | PROPOSEDcontract;notimplemented/qualified |
| T-RESULT | versionedTmaxvsA_controlvsActual;TL001mapping+legacyplancompatibility+consumerchecks | P1_PROPOSED;notfixed |
| I-SCOPE | конкретный futureallowlist/diff,mandatorycallergraph,independentreview,no-dispatch policy preserved | BLOCKED:noimplementationpermission |
| R-LOSSBOUND | ERR038 explicitboundedmarket/execution/costmodel+theorem,evidenceandlimitations | OPEN;deployment/activationBLOCKED |

Names/flags не evidence. Для нового eventexpectedrevision/sourceinventory должныпроверятьсяатомарно, а не callerbool. Если gate отсутствует, результат BLOCKED/UNAVAILABLE,не 0 и не«готовопосле публикации».

## 3. Матрица пакетов

| R1.1 | Нормативные зависимости | Source dependencies | Providers/journal | Native/tests | Open P0/P1 | Gate/переход |
|---|---|---|---|---|---|---|
| C Numeric guards | D10/D11/D12/D15,closedenums/grid/errorboundprofile | RiskGateResult,MoneyState,TransactionTypes,BrokerGrid,typedinputs/limits | independentprofile;guards сами не sourceauth | finiteinputs+limits+intermediates,overflow,grid,zero/errorbounds,nativecodec;CU02 | P0ERR009/010/011;adjacentdomainP1 | BLOCKED;profile/native/owner scope иотдельное implementationpermission |
| A Source identity | D02/D08/D12/D13/D16 +numeric | EconomicLedgerTypes,Identifiers,MoneyProofIdentity;actualoriginbindings | broker/history+EAoriginassociation,snapshotreceipts,migration | fullbody/keychanges,unknownauthority,CU05/07/08/09,exactreplay | P0ERR001/002/013;ERR043basisrelated | BLOCKED;independentprovider и legacyprofile required |
| B Allocation | D01/D02/D03/D07/D10/D11/D14/D16 | AllocationLedger/Policy,MoneyState,ReserveAllocationTypes | globalregistry+atomicdurablejournal;sourcealiases,grantphase,lifecycle | exactconservation,concurrentowners,CU06,restart/corrections | P0ERR004/005/007/008/011/033 | BLOCKED;realbackend/evidence не создаютсяданным R1scope |
| D Reserve binding | D02/D03/D04/D06A/CR09/D07/D08/D13/D14;selectedobjectiveinputm | ReserveCatchUp,NewFarSolver,Aggregator,CatchUpModel;proof DTO boundaries | eligibility/free/providerreceipts,levelscope/cost/quantitybinding,prefixinventory | TL01–05/CU01–10,perlevelFar,tamper,alllevelmin,native | P0ERR007/008/013/033/048;P1ERR018/043/045/TL001 | BLOCKED;полный contract+providers+scope/native,а не one-linefix |
| E Integration | Все dependentcontracts;D05reset,D06/objectiveversions,schemas | Context,StateMachine,TransactionTypes,Journal,Snapshot,Runtimevalidators/adapters | actualpositions/fills/unknownreconciliation,crashconsistentstore,atomicfunding | everycrashpoint,partial/delayed/restart,sticky/reset,alladapters,native | P0ERR010/012/013/033;ERR038activation;P1TL001/018+history | BLOCKED;allpriorevidence+mandatorypaths+separatepermit |

Каждаястрока: IMPLEMENTATION_ALLOWED=NO. Design/spec/read-onlyreview не равны разрешению изменять production.

## 4. Source closure и ограниченный allowlist

TL001localoutputmapping расположен в NewFarSolver,которыйестьвбудущем R1.1-Dallowlist. Это всёравнонеавтоматическоеразрешениеисправлятьего.
Полныйпредлагаемый typedall-levelcontract затрагивает interfaces FutureSmallTypes,NewFarCandidate,CandidateMoneyEvaluator,RuntimeDecisionTypes/Validator и schema/planbindings. Не всеонивключенывисходный allowlistD/E.
Нельзясамостоятельнорасширять scope. Конкретный futuredesign можетиспользовать additiveinterfaces иуменьшитьзатронутыепути, ноэтонадопоказатьв reviewableversioneddiff. Нельзяпредположить, чтолюбаяполнаяреализацияпомещаетсявстарый PoC.
NewFarA требуетсогласования Doc29/comparatororder и ObjectiveVersion. Source Doc29/comparator остаютсяпрежними; историческиетестынепереписываются.

## 5. Циклы и bundles сохраняются

Numeric(D10/D11/D12/D15),FundingAuthority(D01/D02/D03/D07/D08/D13/D14/D16),SafetyRestart(D05/D07/D13),RecoveryNewFar(D04/D06/CR09+companion)перекрываются.
В baselinegraph сохранены corecycle{D01,D02,D07,D08,D10,D11,D12,D13,D14,D15,D16}и{D04,CR09}. Новыеб inding обязанности не делают graphDAG.
SelectedD06/objective прикрепляютсяк versioned03Ebundles как choiceannotations,неменяютих pendingmemberapprovals. R2futurecontract имеет versionHSBI-03F-R2-V1 и requires полного CR09/provider/numeric/journalapproval.

## 6. Acceptance и unresolved

Длябудущего PASS нужныконкретныеквитанции/артефактыкаждогогейта, нефактналичия report. Testcoverage должнадоказать mandatorycalls,ветку SELECTED/отказ requirednegative,финансовую delta0,replay/crash/concurrency.
P0TOTAL14,CLOSED0:ERR001,002,004,005,007,008,009,010,011,012,013,033,038,048.
P1TL001auditregistered без officialERR-ID;ERR018 сохраняет OPEN. Нет severitypromotion по одной таблице.
Unresolved:15decisions/fullCR09,CostBasis,perlevelquantity/eligibility/levelsemantics,TieID,numeric/codec/native,snapshot/sourceauthority,registry/durability,legacy,ERR038theorem.
Связи: [selection](HSBI_03F_R2_OWNER_POLICY_SELECTION_RU.md),[ERR018](HSBI_03F_R2_ERR018_SOURCE_LEVEL_AUDIT_RU.md),[futurecontract](HSBI_03F_R2_TRANSITION_CATCHUP_CONTRACT_V1_RU.md),[vectors](HSBI_03F_R2_TEST_VECTOR_SPECIFICATION_RU.md),[TL001](HSBI_03F_R2_TL001_REGISTERED_FINDING_RU.md).
