# HSBI-03F-R2 — Итоговое заключение

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

Status=ANALYSIS_COMPLETE_PUBLICATION_PENDING_VERIFICATION.
Этот файл формируется до commit/ref update. Фактические publication SHA,remote parity и readback сообщаются отдельно после операции; собственный SHA невстраиваетсявсебя.
Scope:owner policy selection+TL001 audit registration+independentERR018analysis+futurecontract/testspec,только 10 новых Reports.

## 1. Исходная база и remote-onlyattestation

ExpectedSourceSHA=ae367ff2925da4d845a413326c840fe468ff451b.
ActualBaseSHA=ae367ff2925da4d845a413326c840fe468ff451b.
Remote baseline checked2026-11-16 17:12:12 UTC.
BaseRootTree=79a4228c025296278a876dcfb6fbd704082f4ad8.
Reports298entries;все 10 целевых names отсутствовали; baseline безновых commits.
Только GitHubMCPremote reads/memoryanalysis иразрешённые Reportwrites. Localcheckout/search/filesystemoperations0. RulesetChatGPT1 не исследуется/не изменяется; PR/CodeQL/newbranches/force/bypass0.
Неизменность existingfiles подтверждается base-treeconstruction+последующим exact10addedfilesdiff,невыдуманнымлокальным cleantree.
Предыдущийнеопубликованный F-DRAFT1 не публикуетсяпод видомподписанногорешения.

## 2. Результаты

| Требование | Результат |
|---|---|
| D06A | точная D06-A/HSBI-03E-R1,owner selectionconfirmed;sourceblob39342ea57a83a8dcd2f8e22ff8b87747c371d0ca |
| NewFarA | MINIMUM_SAFE_V1,sourceblob a29b28fe806b7bd53cc49a34803b25b4b9b55543;objectiveinputminall,не control |
| Otherdecisions |15AWAITING/BLOCKED;fullCR09 не approved;formalreceipts0 |
| TL001 | audit-onlyregisteredFindingIdHSBI-03F-TL-001,P1_PROPOSED,CONFIRMED_STATIC,OfficialErrIdNOT_ASSIGNED |
| ERR018 | overallCONFIRMED_CONTRACT_GAP;all-requiredimplementationgapstaticconfirmed;fullruntimeevidenceblocked |
| Counterexample | coherent4legmodelT12/7/3,margin9/−4/2,recovery−12/−7/−3;exactmilli-unitarithmetic |
| Futurecontract | HSBI_TRANSITION_AND_CATCHUP_CONTRACT_V1 PROPOSED_AWAITING_CR09_AND_DEPENDENT_BUNDLES |
| Vectors | TL01–05/CU01–10+independentcontrols,TEST_SPECIFIED_NOT_RUN |
| Readiness | C/A/B/D/EallBLOCKED;implementationNO |
| Defects/trading |14P0open,0closed,ERR038OPEN,production/dispatch/tradingunchanged |

## 3. Что доказано непосредственно source

NewFarSolver131–134 проверяет aggregate.maximumTransitionLoss до safe[]146;151 возвращает controlFarLoss,не Tmax. Assignment не capbypass.
FutureSmallSolver/aggregator проверяютмного money/transitionproofs,но NewFar127 вызывает CatchUp0/1 разна candidate дляодного control;catchUpProofValid138 не all-requiredstatement.
WORST_CASE=argmaxTransition,FINAL=lastproven,EXPLICIT=callerindex в range.
Currentci.farVolume=candidate123,а futuregeometryF_l меняется; простая loop копияможетложноотвергатьдальниеуровни.
FutureSmallrecoverystrictgrow89/143⇒genuineprojectedTnonincreasing;«worstL3»сростом T невалидный genuineproducerfixture.
Sourceidentity119–124 переписаниз caller;allocated/free/historyvalidators не globalprovider/CAS;projectedproofflag не actualmoney.
AllsourceclaimspinnedSourceCommitSHA;точныефункции/строкив thematicreports.

## 4. Что доказано математически

CoherentM_MINUS использует validgrid,nonnegativefee magnitudes,signedcosts,четыре legs,уменьшающийся Far. Этоопровергает argmaxT⇒argminMargin безподменыпроизвольнойтаблицей.
M_PLUS даёт margins9/1/2;M_ZERO9/0/2;strict>0 разделяет accept/reject.
Constantreserve14.5 даёт 0.3/−0.7/5.3 дляальтернативных checkpoints;непоследовательныеправапотратить 14.5 трижды.
D06 инвариант E−H_in−Recovery_A=I приобщем scope/basis.
TL01T12/Far3 и TL02T3/Far12—разныефункции; ихнеравенствонеравносильно runtimebypass.
Проверкивпамяти—integerarithmetic,не MQL5runner. Матмодельнепредъявляетсякакреальный brokerinstrument,authenticatedsource или fullsuccessfulsolvercall.

## 5. Downstreamscope и severity

Повторнопрочитаны 74productionfiles и 11MQL/C++testsource. Comments/strings исключеныиз symbolsearch. Externalproductionreferences HSBI_SolveNewFar/HSBI_NewFarSolverResult NOT_FOUND_IN_SCANNED_SCOPE.
Mainincludeclosure16 файловбез NewFarSolver. Main19–43disabledpolicy/NoTradeStub/diagnostics.
RuntimeDecisionTypes11–17/Validator19–28 принимают candidate/aggregate отдельно; solverresultadapter NOT_FOUND_IN_SCANNED_SCOPE.
Safety/persistence/UIconsumer result.transitionLoss NOT_FOUND_IN_SCANNED_SCOPE;невозможностьвнешних consumers неутверждается.
Tests/MQL5/HSBI_Skeleton_Tests.mq5 имеет solvercalls,ноне assertresult.transitionLoss. Исторический 7PASS/16FAILC++artifact непокрываетновыесценарии.
P1_PROPOSEDTL001 обоснованденежным public output contract и latentfutureintegrationrisk;не P0 бездоказанного критического пути. Историческийреестрнеизменён.
Связи: ERR013sourceorigin,ERR018alllevel,ERR043absolutebasis,ERR045previewvsactualresidual;ERR038 отдельный lossboundOPEN.

## 6. Чтопредложено, нонеутверждено/не реализовано

Новый all-requiredtypedcontract;per-levelFarvolume/source/basisbinding;proof-completenessmanifest;Tmax/Far/Actual раздельныерезультаты; all-levelminimum/errorbounds;versionedresult/proof/Objective/numeric/legacycompatibility.
Requiredlevelset,eligibility,durablefundingprefix,CostBasis/snapshot/provider/numerics и fullCR09 ещёне approved. Selectedobjective не approval всегобандла.
FutureResultSchemaVersionHSBI-TC-RESULT-2 не разрешениеизменить DTO в production.
Все native/component/integration/crash/concurrency/providerqualificationtests ещёпредстоят.

## 7. Решения владельца и R1.1blockers

D06A/NewFarA повторновыбиратьне нужно: они recordedCONFIRMED_IN_CONVERSATION. Нужны оставшиеся 15decisions/CR09fullscope,EligibleReserveSourceSet,LevelSemantics/RequiredLevelIDs,per-levelFarobligation,TieID,CostBasis/H_in/H_gate/Initialmembership,actualcurrency/grid/codec/clock/trustprofiles,registry/journal/migration и nativeevidence.
FormalapprovalreceiptsNOT_REGISTERED,неподделаны. D05resetUNBOUND,D11EVIDENCE_BLOCKED,D12/D15nativeNOT_RUN,D13PROVIDER_BLOCKED.
CurrentR1allowlists неавтоматическипокрываютвсезатрагиваемые typed/runtimeinterfaces;нужныконкретный futuredesign/diff/scopeapproval. No backend/tradingactivation разрешение.
ERR038boundedlots не boundedmoney;все 14P0OPEN.

## 8. Историческое evidence

Tests/Close/production_subset_results.json,SourceBlobSHA=192fe577764407499c6334d8e07c55ad78afeed7:7PASS/16FAIL,exit1,HISTORICAL_TEST_RESULT. Не rerun;expected неизменны.
COMMITTED-UNDERALLOCATION-PROPOSED и P0-03-EXHAUSTED-PROPOSED сохраняют contract-dependentscope. Новыематематическиетаблицынеих replacementexpected.

## 9. Sourceinventory

Все 113 уникальных files прочитаны remote на SourceCommitSHA. 74production+11native/C++testsource прошлицелевой xrefscan;этоНЕновыйполный 74-moduleeconomicreview иНЕинвентаризация 1529baselinefiles.
Ниже blobs длявоспроизводимойпроверки; range/functionreferences в thematicdocuments.

| Source path | SourceBlobSHA |
|---|---|
| Docs/04_MATHEMATICAL_MODEL_RU.md | f290e753e62b004dbdc0c4f8ef24fda46b9b6d7c |
| Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md | 9bab98f4df7e162dd26fcf07f6e267bc079bd5ba |
| Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md | 0d9e9321bea27b83397e9eb3348434fbbed61970 |
| Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md | 1dc796cb19748ad7e70ac9bcac611e8e18dbdcdd |
| Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md | 4ecebeb09c9dcfbbf9d3927b980e44fd81289cf6 |
| Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md | f779a1a87ab2d0163c17d6c855c206047d970cec |
| Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md | f93a0cb48b7e1683883823ace9df9d6ede9697f3 |
| Docs/16_PERSISTENCE_AND_RESTART_RU.md | 5b1bd202c865828407eecdd8cffc04c4cae949f7 |
| Docs/24_BROKER_MONEY_MODEL_RU.md | fd4ca5dfb7835d22bde5d8971b7849226cc3b237 |
| Docs/25_BROKER_GRID_AND_ROUNDING_RU.md | 7e1357c5540bc92d7aaee142404aadc144f1a632 |
| Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md | 33796d41e5efa824fff32a38f4d09fefe90b5e0b |
| Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md | 0c4b5f9ea4aab1618a280a5c4510f89b76fb9646 |
| Docs/31_MONEY_PROOF_IDENTITY_RU.md | 95dfd5d807899d180632504dc01aa843b76ab1f5 |
| Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md | 77c9a05a0df23cb238dda71798bc2c158ffdbdbf |
| Hybrid_Split_Big_Independent_EA.mq5 | 3b306df062b5aabac16ee5874f9cf233c21d3e36 |
| Include/Core/HSBI_Context.mqh | 382be9e46dfc00a95393b79c2e2215cf0c0e62b4 |
| Include/Core/HSBI_Enums.mqh | 23ffdbc865932e8161d2f0eddd3627ca01640ef4 |
| Include/Core/HSBI_Identifiers.mqh | d05a05147f7641040dbf7261ebdd04832d643997 |
| Include/Core/HSBI_Invariants.mqh | 0c03a908e2887a4c19bf24829ba39769e05606b6 |
| Include/Core/HSBI_ReasonCodes.mqh | 3ffbe6a053ee574f607ca11161c049c990ef8128 |
| Include/Core/HSBI_Roles.mqh | 23d0bedac6e8852342638d7f16d121ad19124a11 |
| Include/Core/HSBI_RuntimeMode.mqh | 3c5eb19440572cae78eb2d042907ae13ffb10a44 |
| Include/Core/HSBI_RuntimePolicy.mqh | 657fe730c1a3df306848d1de00af87aa589be449 |
| Include/Core/HSBI_StateMachine.mqh | 836c2dcbe983caf7127cfcd2442dc0b740bf8479 |
| Include/Core/HSBI_StateValidator.mqh | b4c6ba061c33a6514f9eef9db2e8e885ff09008f |
| Include/Core/HSBI_Types.mqh | 9fd1c4bdf531665b50ba5ca6db38daba8f0d70d0 |
| Include/Core/HSBI_Version.mqh | d0eefae130ed96720b3f1962842d2a9c30168a00 |
| Include/Diagnostics/HSBI_Diagnostics.mqh | 6bde810e9fc5fe577744381a7ce0d52c3d6718ed |
| Include/Diagnostics/HSBI_Logger.mqh | 61471e52a9a98d465cb7ced3f6744ccd7678782e |
| Include/Diagnostics/HSBI_PanelModel.mqh | 2c878424c053e8c2b316c7e850c9df600dbdbc2d |
| Include/Execution/HSBI_ActionTypes.mqh | b592dac8bb8e862336e0a8da371ba76445c4da68 |
| Include/Execution/HSBI_EventTypes.mqh | 7dbdbb34a1e2eab4a3bf3bc0d649dbf30e45a13d |
| Include/Execution/HSBI_ExecutionIntent.mqh | 026b7c6d44b9dad83eb7d8de9bd0c567094a13ca |
| Include/Execution/HSBI_ExecutionPreflight.mqh | 2889fe50eb4690681f370d7be8613a887a81a05d |
| Include/Execution/HSBI_ExternalOutcome.mqh | 409e85b37268c2b7f4785a1b0d614423592b5ba7 |
| Include/Execution/HSBI_NoTradeExecution.mqh | 5c29fece82fe03a954fb345bf006de6a281705f9 |
| Include/Execution/HSBI_OwnershipGuardTypes.mqh | 4e6ca9ad75ef5ad37da4555feea44d451a6cb4c2 |
| Include/Execution/HSBI_TransactionTypes.mqh | bf82abf9b8aa212ce3c96f6c859e70000968b52d |
| Include/Money/HSBI_AllocationLedgerTypes.mqh | 87f86ec7498bd115f5a21da34d596c0ce0c2170a |
| Include/Money/HSBI_AllocationPolicyTypes.mqh | 720942a0049cacc76691e600efdef7018e91d482 |
| Include/Money/HSBI_BasketMoneyEvaluator.mqh | 4bea204e91a4719b4b24086304cb51051909a7de |
| Include/Money/HSBI_BrokerMarginModel.mqh | a8c0f43465785d7d6c82517124c3e3b028862337 |
| Include/Money/HSBI_BrokerMoneyModel.mqh | 4dbee633bceb914365e536acc00208955c01588f |
| Include/Money/HSBI_BrokerMoneyTypes.mqh | ebcd16b2a9ea770d9c8525f5ed3285f3a5129870 |
| Include/Money/HSBI_CandidateMoneyEvaluator.mqh | 5402799247ff948b2616306060764004b468abf2 |
| Include/Money/HSBI_CatchUpModel.mqh | 33a87589e8663ddf97b8c7495978b7462149d733 |
| Include/Money/HSBI_CatchUpTypes.mqh | 431dd7f52b9ee82f127d04d5db6a95e25545095c |
| Include/Money/HSBI_CostModel.mqh | 293a22c0ff14bc6d635e0cc50c79c8e3d4a7d5cd |
| Include/Money/HSBI_EconomicLedgerTypes.mqh | e589337d228323dba278b242d01e61fc0ee733fe |
| Include/Money/HSBI_LevelMarginEvaluator.mqh | 2227a0ef16caa44f4e4ffefcf860499773dbf471 |
| Include/Money/HSBI_LevelMoneyEvaluator.mqh | 3c89ae2355945ec7c75fac2694967ae5f1785967 |
| Include/Money/HSBI_MoneyProofIdentity.mqh | cb00b547b9f4d3d9eac7a473415b25627c3ac91d |
| Include/Money/HSBI_MoneyState.mqh | d318c28cc23ddaf19d22a9c7a47e9202800d1786 |
| Include/Money/HSBI_MoneyTypes.mqh | 2a3226fe19fdeb8053b618d2d7ca72ed111e6bb5 |
| Include/Money/HSBI_ReserveAllocationTypes.mqh | f1464320f1f853f12f8e3f3ddc3708bad2a0cd4d |
| Include/Money/HSBI_ReserveCatchUpEvaluator.mqh | 87a8b7e97727ce6e47c2a2f0abc3e237f6203204 |
| Include/Persistence/HSBI_ExecutionJournal.mqh | e65d6d9b0f04a3e236952ec577ea144bf57ee2b2 |
| Include/Persistence/HSBI_ExecutionStateSnapshot.mqh | 4fc1e37af6430d206bb2c7b480681473cd9c2bf2 |
| Include/Persistence/HSBI_JournalTypes.mqh | c2f007a44020dba1f5e0cb2c4f52342d1d0c9f8f |
| Include/Persistence/HSBI_PersistenceInterface.mqh | 36b7181f50fe4554d24f9ea6813906f9f4240d49 |
| Include/Persistence/HSBI_ReconciliationTypes.mqh | 1e79faeeef3b32aa5318f815f8308b67950ae3b2 |
| Include/Persistence/HSBI_SnapshotTypes.mqh | f3c7789f323657aee83c34544b0143165b454279 |
| Include/Planning/HSBI_BrokerGrid.mqh | 82a06297b2c98113f18d92ebf3cd7bdc615749a0 |
| Include/Planning/HSBI_CandidatePlan.mqh | f056148d2bccd020b01d6c8a7433fbba9e83f158 |
| Include/Planning/HSBI_ControlPrices.mqh | 2540db9d53533319319b698d999187f785f0815c |
| Include/Planning/HSBI_DecisionResult.mqh | 2847c1b1c61502ffa7cba9813e0a843afcf1a50b |
| Include/Planning/HSBI_FutureSmallProofAggregator.mqh | 4678ae152960e98b9f398b4497786061d7e8a524 |
| Include/Planning/HSBI_FutureSmallSolver.mqh | be55c93f051f57ddffd189b9d2e8eee4c3ddaf9d |
| Include/Planning/HSBI_FutureSmallTypes.mqh | ee962ed40a99b0d0a1fdd22f2ee071cc3fb6cbcc |
| Include/Planning/HSBI_GeometrySolver.mqh | 707cc1678ca4d98888b3acc2599838094fe13a78 |
| Include/Planning/HSBI_GeometryTypes.mqh | 3471f80349bdb20f8a13a99d11fd9b9244e93498 |
| Include/Planning/HSBI_NewFarCandidate.mqh | 758f1c89cf75701d3616dabec2fcb06413ee2d4a |
| Include/Planning/HSBI_NewFarSolver.mqh | 3d19eccd6cd318b9b4591e2bc0ccaa95f661930d |
| Include/Risk/HSBI_CalculationGateTypes.mqh | 06b75ded19b5c5d51e401066592dfc3ff1981e71 |
| Include/Risk/HSBI_FutureSmallRiskEvaluator.mqh | 870d84b3f49a85e7db5c6d5ead777efea1c9faa3 |
| Include/Risk/HSBI_NewFarGateTypes.mqh | 7d50669bda8ff2d000566ad7a38281140a77ae83 |
| Include/Risk/HSBI_RiskGateResult.mqh | f172bd2ab9cfc461ab403a8ce490a4b71ce3c8c4 |
| Include/Risk/HSBI_RiskTypes.mqh | 6f40356c18949a0465c1595b0229a67bbcd46dc7 |
| Include/Runtime/HSBI_RuntimeDecisionTypes.mqh | 0cc2619ed6ce7a93ea28c3c655a8d147e18a9231 |
| Include/Runtime/HSBI_RuntimeDecisionValidator.mqh | aecbf35e7ced9fd756d80803c63626b9b52c0846 |
| Include/Runtime/HSBI_RuntimeRestartValidator.mqh | 81001f9eadb42a2c8255f38392d1739064dc6749 |
| Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh | 2a5df55b4b5814eed26f684b8d86583cf2b53eb6 |
| Include/Scenarios/HSBI_BigHarvestTypes.mqh | 5be5c560ae6093281ad0f3f30cd7613514f675b1 |
| Include/Scenarios/HSBI_FinalCloseTypes.mqh | 319af55c5054e082582da0598c79ed0d319a1599 |
| Include/Scenarios/HSBI_InitialLockTypes.mqh | 79b6f2df50ea5c9b38bae46849bddb9f99de108b |
| Include/Scenarios/HSBI_PartialFarTypes.mqh | 19b41ac1061bee2cd5bd7412b94df2efcb0499c9 |
| Include/Scenarios/HSBI_ScenarioTypes.mqh | cd6598113b76dd2754c1ab7c5091c7e59b8d9a9c |
| Include/Scenarios/HSBI_SmallTransitionTypes.mqh | edbe990f0b0a6df2d4cba4368ad126764abad021 |
| Reports/HSBI_03D_MONEY_INVARIANTS_AND_COUNTEREXAMPLES_RU.md | cac37d61876fe1193d78791f4a09ef7aca8c486c |
| Reports/HSBI_03D_P0_REMEDIATION_CROSSWALK_RU.md | 6a72362e588506f310b31d6fb9437edaeb6ba7a6 |
| Reports/HSBI_03E_CONTRACT_DEPENDENCY_RECONCILIATION_RU.md | ceb6440e45dee9a67dab478dfbc48d4325e8db3f |
| Reports/HSBI_03E_D06_POLICY_RESOLUTION_RU.md | 39342ea57a83a8dcd2f8e22ff8b87747c371d0ca |
| Reports/HSBI_03E_FINAL_VERDICT_RU.md | d1f152fcda2ba66ef792e444c6b40185d2759ddc |
| Reports/HSBI_03E_NEWFAR_OBJECTIVE_RESOLUTION_RU.md | a29b28fe806b7bd53cc49a34803b25b4b9b55543 |
| Reports/HSBI_03E_NUMERIC_CONTRACT_MANIFEST_V1_RU.md | 6b9fcc61124e5d9d88f96cee420c3596fada0ff2 |
| Reports/HSBI_03E_OWNER_FINAL_DECISION_BALLOT_RU.md | 62472656ad4af5acba65144e30f36cbca05a5abd |
| Reports/HSBI_03E_R11_GATE_MATRIX_RU.md | 818bc9688f3d622f7bbfa8d804b29df1ba21a575 |
| Reports/HSBI_03E_SNAPSHOT_AUTHORITY_CONTRACT_RU.md | 31898e975924c9e54b94be06352e9f08fbfdcc3e |
| Reports/HSBI_AUDIT03_ALL_ERRORS_RU.md | a36d0fb1c37da7dcab02e54e9738e01befc16084 |
| Reports/HSBI_AUDIT03_CLOSE_FINDINGS_RECONCILIATION_RU.md | 2e883a8692fa94817bbde554646411b4f8cf6a5f |
| Reports/HSBI_R11_P0_DEPENDENCY_PLAN_RU.md | 8ac398a8dae93dbcbc28e2fbeddc70a7501b2f76 |
| Tests/Close/native_close.mq5 | efa32b21db4cbeaf1502fd5477583ad8c9019c03 |
| Tests/Close/production_subset.cpp | c15685bd47b64f5d1a66f5279553f40c5353905c |
| Tests/Close/production_subset_results.json | 192fe577764407499c6334d8e07c55ad78afeed7 |
| Tests/MQL5/HSBI_Skeleton_Tests.mq5 | 75052d49e55a5f43534143052b28c0b94ba2b516 |
| Tests/Native/HSBI_DG01_codec_cases.mqh | 3102e0aa6863704f41066b736d9a7542b38b6358 |
| Tests/Native/HSBI_DG01_goldens.mqh | cfacd88c155caa6e22cfe40ee5ab849291349449 |
| Tests/Native/HSBI_DG01_harness.mq5 | d7f5a8f88b7bf625e58af1e633cf526db372bb5e |
| Tests/Reference/HSBI_DG01_identity_candidate.mqh | 8c59dfe76dcf916c17774ddd63ce5ea6f1d61580 |
| Tests/Reference/HSBI_FULL_SYSTEM_AUDIT_02_native.mq5 | 114e026a38f7cf33633164de09ba5acb90239862 |
| Tests/Reference/hsbi_02b_r0h_native_codec.mqh | 91b8a09c2e7a2db31f0f917da105fff3260d6ffb |
| Tests/Reference/hsbi_02b_r0h_native_goldens.mqh | 31506f7b0a8932bdaf0ee7044c557100fd9dcc94 |
| Tests/Reference/hsbi_02b_r0h_native_harness.mq5 | 1bee48cf0ea949109b44274e4810c8ca4d26a01d |
## 10. Точный publicationmanifest

- [HSBI_03F_R2_OWNER_POLICY_SELECTION_RU.md](HSBI_03F_R2_OWNER_POLICY_SELECTION_RU.md)
- [HSBI_03F_R2_D06_A_NORMATIVE_LOCK_RU.md](HSBI_03F_R2_D06_A_NORMATIVE_LOCK_RU.md)
- [HSBI_03F_R2_NEWFAR_MINIMUM_SAFE_NORMATIVE_LOCK_RU.md](HSBI_03F_R2_NEWFAR_MINIMUM_SAFE_NORMATIVE_LOCK_RU.md)
- [HSBI_03F_R2_TL001_REGISTERED_FINDING_RU.md](HSBI_03F_R2_TL001_REGISTERED_FINDING_RU.md)
- [HSBI_03F_R2_ERR018_SOURCE_LEVEL_AUDIT_RU.md](HSBI_03F_R2_ERR018_SOURCE_LEVEL_AUDIT_RU.md)
- [HSBI_03F_R2_TRANSITION_CATCHUP_MATH_PROOFS_RU.md](HSBI_03F_R2_TRANSITION_CATCHUP_MATH_PROOFS_RU.md)
- [HSBI_03F_R2_TEST_VECTOR_SPECIFICATION_RU.md](HSBI_03F_R2_TEST_VECTOR_SPECIFICATION_RU.md)
- [HSBI_03F_R2_TRANSITION_CATCHUP_CONTRACT_V1_RU.md](HSBI_03F_R2_TRANSITION_CATCHUP_CONTRACT_V1_RU.md)
- [HSBI_03F_R2_DEPENDENCY_AND_READINESS_MATRIX_RU.md](HSBI_03F_R2_DEPENDENCY_AND_READINESS_MATRIX_RU.md)
- [HSBI_03F_R2_FINAL_VERDICT_RU.md](HSBI_03F_R2_FINAL_VERDICT_RU.md)

## Acceptancepublication

Проверить currentHEAD=base,10targetpathsnew,version/sourceblobs/links/16IDstatuses,mathinput/expectedconsistency,noinventedPASS.
Создать 10blobs,base-tree с 10explicitpaths,onecommit(singleparentbase),проверить exact10addedfilesdiff,nonforceupdatework expectedSHA. При HEADchange—stop/reconcile,не overwrite.
Послеуспеха readall10filesatwork,comparecontentandblobSHA,repeatcommitdiff/head. Фактический publishedSHA/parity сообщаетсяв finalreceipt,ане self-referentialbody.
Если writefailed,не COMPLETE. Если published и analysiscriteria выполнены, COMPLETE относитсяк audit/specdeliverable,ане tradingqualification.

P0_TOTAL=14;P0_CLOSED=0;ERR038_STATUS=OPEN
DECISIONS_TOTAL=16;DECISIONS_OWNER_SELECTED=1;DECISIONS_AWAITING=15
COMPANION_OBJECTIVE_SELECTED=1;REGISTERED_APPROVAL_RECEIPTS=0
NATIVE_MQL5_TESTS=NOT_RUN
PRODUCTION_CHANGED=NO
R11_IMPLEMENTATION_ALLOWED=NO
BROKER_DISPATCH_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
