# HSBI-03F-R2 — D06 A: lock выбранного опубликованного текста

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

Status=OWNER_SELECTED_A_TEXT_PINNED;FormalApprovalReceipt=NOT_REGISTERED.
LockId=HSBI_D06_A_SELECTION_LOCK_V1;LockVersion=HSBI-03F-R2-V1;SelectedPolicy=D06-A/HSBI-03E-R1. Это version pin выбранной политики, не новый изменённый D06-A.

## Источники и точный выбранный текст

SourceFile=Reports/HSBI_03E_D06_POLICY_RESOLUTION_RU.md;SourceBlobSHA=39342ea57a83a8dcd2f8e22ff8b87747c371d0ca.
Обязательная общая область: source29–50 (membership/cost/headroom/Initial/corrections),selectedA52–67;quote56. Ни один source paragraph не переписывается.

> RecoveryRealized_A=R_all−I; RecoveryResult_A=Q−I=R_all−I+O_phys−C_rem−H_in. EconomicCyclePnL=E хранится отдельно и не используется вместо RecoveryResult_A для ordinary FinalClose. Initial Profit остаётся вне recovery и harvest budgets согласно Docs09. Все отрицательные/rollback экономические факты сохраняются. FinalCloseResultGate_A: RecoveryResult_A≥Theta. Threshold и остальные gates Docs12 не ослабляются. Нельзя прибавлять allocation buckets к E/Q/RecoveryResult. Missing Initial/cost/basis evidence → UNAVAILABLE. Ordinary authorization требует одновременно result gate, independently confirmed allowed coverage, freshness/ownership/revision, no pending/unknown, complete costs и safety policy. CLOSED только после actual fills,actual zero managed positions,exactly-once ledger,durable result. Emergency отдельна.

Нормы для проверки: Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md:16–20,28;Docs/04_MATHEMATICAL_MODEL_RU.md:18,24,27,30;Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:6–24;Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md:5–17.
Production:Include/Money/HSBI_CostModel.mqh:11–18;HSBI_BasketMoneyEvaluator.mqh:7–18;HSBI_EconomicLedgerTypes.mqh:6–12. Это helper behaviour,не fullFinalClose implementation.

## Формулы без альтернативной подмены

R_all(t)=Σ уникальных independently associated actual net postings одного CycleScopeID.
E=R_all+O_phys−C_rem;Q=E−H_in.
RecoveryRealized_A=R_all−I.
RecoveryResult_A=R_all−I+O_phys−C_rem−H_in.
Theta=MinimumRecoveryProfitMoney+H_gate+MoneyTolerance.

Алгебра:
E−H_in−RecoveryResult_A
=(R_all+O_phys−C_rem)−H_in−(R_all−I+O_phys−C_rem−H_in)=I.
Это MATH_DERIVED при общем scope/basis/currency,не native arithmetic qualification.

## Каждый показатель и расходы

EconomicCyclePnL(E) включает реальные signed facts,не allocation buckets. RecoveryResult_A исключает именно independently confirmed positive InitialProfitExcludedNet I завершённой INITIAL_PLUS group. Rollback/negative/cost facts не исчезают.
I не сумма всех positive Initial deals;group,cost membership,complete receipt обязательны. Incompletegroup→UNAVAILABLE/ordinaryauthorityblocked.
CostFactID находится единожды в R_all/O_phys/C_rem;spread/slippage уже в executionprice не повторяются; headroom H_in/H_gate не actual broker expense.
Источником подтверждения membership и H_in/H_gate является CostBasisManifest с receipts,не scalar0. Correction chain append-only,не rewrite receipt/source grant. Валюта, profile и CycleScopeID проверяются до aggregation.

## Проверяемые cases

| Case | Полные monetary inputs | Expected/invariant |
|---|---|---|
| D6+ | R_all100,O_phys−8,C_rem2,I50,H_in4,min10,H_gate5,tol1 | E90,Q86,Recovery36≥Theta16;только resultgate |
| D6− | R_all40,O_phys−4,C_rem1,I50,H_in4,samethreshold | E35,Recovery−19;reject despite positiveE |
| Partial | beforeR20,O30,C2;aftergross12,cost1→R31,O18,C1;I/H unchanged | E48 before/after;не CLOSED whilepartial/pending |
| Double Initial | R_all уже включает I50;предложеноещё+50 | reject duplicateincome;формула не R_all+I |
| Duplicate expense | gross100,swap−1,commission−2,fee−1;net96;теже fees повторно 4 | actualnet96,not92 |
| Reserve addition | E35,FinalReserve20;предложено E55 | reject bucketdoublecount |
| Cross scope | R_all cycle7 + open cycle8 | CONFLICT,delta0 |
| Missing evidence | I или H_in/H_gate/profile unknown | UNAVAILABLE,не 0 |
| Projected posting | forecastprofit50 inserted inR_all | reject as actualposting/sourcegrant |

Все новые cases TEST_SPECIFIED_NOT_RUN;простая арифметика MATH_DERIVED.
Фактические fills/zero positions/exactly-once ledger/durable close — postconditions CLOSED;их нельзя требовать уже выполненными для самого preview или подменять preview фактическим закрытием. FinalClose authorization до actions требует result+coverage+freshness+ownership/revision+no pendingunknown+cost/safety gates;actual completion отдельно.

## Границы lock и будущая совместимость

Выбор A не меняет currentDocs09 Initial exclusion ине выбираетвариант B. Публичный scalar/helper не устанавливает actualauthority. CostBasisManifest,actualH values,Initialassociation,numerics,sourceinventory,snapshot,journal/native remainBLOCKED.
Нельзя менять oldexpected/планы, объявляя, что lock сам исправил moneycode. Будущие typedresult/membership changes толькос отдельным allowlist/permission/versionmapping.
Приёмка: quote byte-identical source56;формулы/инвариант совпадают; все cases имеют expected;unknown→unavailable;cost/grant/source uniqueness proof остаётся prerequisite.
Unresolved перечислены выше. Связи: [owner selection](HSBI_03F_R2_OWNER_POLICY_SELECTION_RU.md),[contract](HSBI_03F_R2_TRANSITION_CATCHUP_CONTRACT_V1_RU.md),[vectors](HSBI_03F_R2_TEST_VECTOR_SPECIFICATION_RU.md),[gates](HSBI_03F_R2_DEPENDENCY_AND_READINESS_MATRIX_RU.md).
