# FAR100 — P0/P1/P2, CR09 и отсутствующие доказательства

SourceCommitSHA=8640bf464eda220d9096adb99bc8bcb390ed68e7
CheckedAtUTC=2026-11-17T13:31:04.086505+00:00
ExecutionMode=LOCAL_RESEARCH_GIT_PLUS_GITHUB_MCP_PUBLICATION
DocumentVersion=HSBI-FAR100-R1-V1
NormativeStatus=RESEARCH_AUDIT_ONLY_NOT_OWNER_APPROVAL
EvidenceClass=SYNTHETIC_MATH_ONLY; STATIC_SOURCE_REVIEW; EXECUTED_PYTHON_REFERENCE_ONLY
DocumentationAudit=UNPROVEN_NOT_PASS_EXHAUSTIVE_SEMANTICS_NOT_CERTIFIED
BrokerProof=UNAVAILABLE
NativeMQL5=NOT_RUN_METAEDITOR_NOT_FOUND
PRODUCTION_CHANGED=NO; IMPLEMENTATION_ALLOWED=NO; BROKER_DISPATCH_ALLOWED=NO; REAL_TRADING_ALLOWED=NO.

Нормативные предпосылки: сохраняются D06=A и NewFar=A/MINIMUM_SAFE_V1, исходные роли и order Small→OldFar→Trend→Core part→actual residual→promotion. CR09 не утверждён, новых owner selections/receipts нет. Старые evidence не изменены. PASS далее относится только к фактически выполненной независимой Python-проверке конкретного synthetic predicate; он не authorizes strategy/runtime.

Синтетические предпосылки: EURUSD/счёт USD, contract100000, tick0.00001, point0.00001, pip0.0001, tick value1USD/lot симметрично; lot min/step0.01,max100,origin0. Spread0.00020 уже в Bid/Ask; opening commission3.5USD/lot учтена в realized, closing3.5USD/lot, accrued swap−1USD/lot, fee0, projected slippage1tick=1USD/lot. Это НЕ сведения реального брокера. Research money использует exact Decimal и не округляет каждый posting до цента; реальный currency/posting/partial-commission profile UNAVAILABLE. QuoteDigits5 не currency digits.

R_all=Initial100−opening fees11.55=88.45USD; excluded Initial I100; RecoveryRealized_A=−11.55. Deposit100000; Balance100088.45 после openings. Исторического eligible harvest в главной fixture нет: TransitionBudget=FinalReserve=PartialFarBudget=0. StartingEquityMark99555.15 при SELL Bid1.10500/Ask1.10520. Все Position/Deal/Action IDs с MODEL — исследовательские символы, не брокерские tickets.

Основные формулы: NetLot=SELL−BUY; DealNet=Profit+Swap+signed Commission+Fee; projected net содержит только ещё не включённые costs; RecoveryPLCloseNow_A=R_all−I+ΣOpenCloseNowNet−H_in, здесь H_in0; Economic=R_all+ΣOpenCloseNowNet. Threshold=10+5+1=16. Allocations не прибавляются к результату. Slippage, реализованная в simulated fill price, второй раз не списывается.

Полные данные, exact decimals и actual command exit codes: [run metadata](../Tests/Evidence/FAR100_R1/run_metadata.json), [команды](../Tests/Evidence/FAR100_R1/commands.json), [test results](../Tests/Evidence/FAR100_R1/test_results.json). Фактические брокерские fills отсутствуют; native/broker/durable tests не запускались.

## Сохранённый статус реестра

Исторический аудит содержит50 IDs: P014,P131,P25,TL001 дополнительно audit finding P1_PROPOSED без нового canonical ERR. Ни один P0 не закрыт новым reference test. ERR038OPEN,ERR018OPEN_CONTRACT_GAP,TL001CONFIRMED_STATIC/P1_PROPOSED. D06A/NewFarA сохраняются, formal receipts0. Doc03/23 исторические OPEN_P0=0 не актуальный closure этих later findings.

| ID | Severity | Historical scope excerpt | Current audit disposition |
|---|---|---|---|
| HSBI-A03-ERR-001 | P0 | IDENTITY / Economic source / replay / Include/Money/HSBI_EconomicLedgerTypes.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-002 | P0 | IDENTITY / Source discovery / Include/Money/HSBI_EconomicLedgerTypes.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-003 | P1 | IDENTITY / Serialization / Include/Money/HSBI_EconomicLedgerTypes.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-004 | P0 | IDENTITY / Allocation replay / Include/Money/HSBI_AllocationLedgerTypes.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-005 | P0 | MONEY_ACCOUNTING / Allocation / Include/Money/HSBI_AllocationLedgerTypes.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-006 | P1 | MONEY_ACCOUNTING / Allocation phases / Docs/04_MATHEMATICAL_MODEL_RU.md | OPEN; no production disposition here |
| HSBI-A03-ERR-007 | P0 | RESERVE / Reserve eligibility / Include/Money/HSBI_ReserveCatchUpEvaluator.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-008 | P0 | RESERVE / Reserve preview / Include/Money/HSBI_ReserveCatchUpEvaluator.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-009 | P0 | RISK / Risk preflight / Include/Risk/HSBI_RiskGateResult.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-010 | P0 | RISK / Fill confirmation / Include/Execution/HSBI_TransactionTypes.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-011 | P0 | MONEY_ACCOUNTING / Money state / Include/Money/HSBI_MoneyState.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-012 | P0 | IDENTITY / Position discovery / Include/Core/HSBI_Context.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-013 | P0 | NEW_FAR / NewFar provenance / Include/Planning/HSBI_NewFarSolver.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-014 | P1 | LOT_SIZING / Basket opening / Include/Planning/HSBI_GeometrySolver.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-015 | P1 | GEOMETRY / Basket planning / Docs/04_MATHEMATICAL_MODEL_RU.md | OPEN; no production disposition here |
| HSBI-A03-ERR-016 | P1 | FSM / Full cycle / Hybrid_Split_Big_Independent_EA.mq5 | OPEN; no production disposition here |
| HSBI-A03-ERR-017 | P1 | PERSISTENCE / Restart / Include/Persistence/HSBI_PersistenceInterface.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-018 | P1 | CATCH_UP / Future Catch-Up / Include/Planning/HSBI_FutureSmallProofAggregator.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-019 | P1 | NEW_FAR / NewFar selection / Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md | OPEN; no production disposition here |
| HSBI-A03-ERR-020 | P1 | GEOMETRY / Future geometry / Include/Planning/HSBI_FutureSmallSolver.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-021 | P1 | FUTURE_SMALL / Future Small / Include/Planning/HSBI_FutureSmallSolver.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-022 | P1 | MONEY_ACCOUNTING / Valuation / Harvest / Include/Money/HSBI_CostModel.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-023 | P1 | BROKER_MODEL / Initial Lock / Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md | OPEN; no production disposition here |
| HSBI-A03-ERR-024 | P2 | BROKER_MODEL / Market snapshots / Include/Planning/HSBI_ControlPrices.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-025 | P1 | FSM / All commits / Include/Core/HSBI_StateMachine.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-026 | P1 | STABILITY / Plan digest / Include/Planning/HSBI_NewFarSolver.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-027 | P2 | DOCUMENTATION / Evidence interpretation / Tests/Static/ | OPEN; no production disposition here |
| HSBI-A03-ERR-028 | P2 | DOCUMENTATION / Normative hierarchy / Docs/03_FULL_SYSTEM_MANUAL_RU.md | OPEN; no production disposition here |
| HSBI-A03-ERR-029 | P2 | IMPLEMENTATION_MISMATCH / Production acceptance / Docs/04_MATHEMATICAL_MODEL_RU.md | OPEN; no production disposition here |
| HSBI-A03-ERR-030 | P1 | IDENTITY / Journal replay / Include/Persistence/HSBI_ExecutionJournal.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-031 | P1 | TERMINATION / Terminal residual / Include/Planning/HSBI_FutureSmallSolver.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-032 | P1 | TERMINATION / Full recovery / Docs/04_MATHEMATICAL_MODEL_RU.md | OPEN; no production disposition here |
| HSBI-A03-ERR-033 | P0 | MONEY_ACCOUNTING / Funding / allocation / Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md | OPEN; no production disposition here |
| HSBI-A03-ERR-034 | P1 | MARGIN / All opens/closes / Include/Money/HSBI_BasketMoneyEvaluator.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-035 | P1 | RISK / Small Transition / Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md | OPEN; no production disposition here |
| HSBI-A03-ERR-036 | P1 | MONEY_ACCOUNTING / Initial / FinalClose / Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md | OPEN; no production disposition here |
| HSBI-A03-ERR-037 | P1 | FUTURE_SMALL / Price proof / Docs/05_GEOMETRY_MODEL_RU.md | OPEN; no production disposition here |
| HSBI-A03-ERR-038 | P0 | RISK / Open residual risk / Docs/04_MATHEMATICAL_MODEL_RU.md | OPEN; no production disposition here |
| HSBI-A03-ERR-039 | P2 | BROKER_MODEL / Broker lot admission / Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md | OPEN; no production disposition here |
| HSBI-A03-ERR-040 | P1 | MONEY_ACCOUNTING / Numeric boundaries / Include/Planning/HSBI_BrokerGrid.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-041 | P1 | RISK / Small Transition / Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md | OPEN; no production disposition here |
| HSBI-A03-ERR-042 | P1 | STABILITY / Full strategy / Docs/03_FULL_SYSTEM_MANUAL_RU.md | OPEN; no production disposition here |
| HSBI-A03-ERR-043 | P1 | CATCH_UP / Catch-Up basis / Include/Money/HSBI_CatchUpModel.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-044 | P1 | MONEY_ACCOUNTING / Final Close / Include/Money/HSBI_MoneyTypes.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-045 | P1 | NEW_FAR / NewFar commit boundary / Include/Planning/HSBI_NewFarSolver.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-046 | P1 | BUY_SELL_DIRECTION / Both directions / Docs/03_FULL_SYSTEM_MANUAL_RU.md | OPEN; no production disposition here |
| HSBI-A03-ERR-047 | P1 | MONEY_ACCOUNTING / Big/Small attribution / Include/Money/HSBI_BasketMoneyEvaluator.mqh | OPEN; no production disposition here |
| HSBI-A03-ERR-048 | P0 | ReserveCatchUp public value bindings / SOURCE_DEFECT / IMP-004/010 | OPEN; no production disposition here |
| HSBI-A03-ERR-049 | P1 | Closed enums intent/action/event/bucket / SOURCE_DEFECT / IMP-005/007/008 | OPEN; no production disposition here |
| HSBI-A03-ERR-050 | P1 | completedActionCount schema semantics / AMBIGUOUS_SPECIFICATION / IMP-009 | OPEN; no production disposition here |


Таблица сохраняет исторические severity, а не присваивает новые production errors. Full original rows/source excerpts есть в pinned Docs inventory; duplicate correction of withdrawn transitionShare hypothesis не восстанавливается как дефект. Current findings scope not exercised native.

## Критические source расхождения

| Source | Input/formula | Expected physical/selected contract | Static source observation | Severity/status | Future correction proposal, not implemented |
|---|---|---|---|---|---|
| [Include/Money/HSBI_BasketMoneyEvaluator.mqh:17](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Money/HSBI_BasketMoneyEvaluator.mqh#L17) | F1,C1.2,T.6,S.5,N.4 | closing−520.95,residual−102.20 | fullbasket−623.15→loss623.15 | membership gap; no new canonical ID | разделить full basket и action-closing metrics |
| [Include/Planning/HSBI_FutureSmallSolver.mqh:122](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_FutureSmallSolver.mqh#L122) | FarSELL→CoreBUYresidual | next FarBUY +Core inherited open | farDirection/openprices берутся сноваизx | physical lineage UNPROVEN | state-chain DTO/edge binding |
| [Include/Planning/HSBI_NewFarSolver.mqh:151](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_NewFarSolver.mqh#L151) | checked maxT versus selected FarA | typed T/A separate | returntransitionLoss=Far loss | TL001/P1_PROPOSED | versioned result fields,not relabellegacy |
| [Include/Planning/HSBI_NewFarSolver.mqh:118](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_NewFarSolver.mqh#L118) | all required margins | minAll predicate before objective | one control CatchUp/candidate | ERR018contractgap | approved manifest/per-level bindings |
| [Include/Planning/HSBI_NewFarSolver.mqh:123](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_NewFarSolver.mqh#L123) | ci.farVolume=candidate | physical full oldFar obligation1 | control NetBig versus original candidate | CR09-SUB04blocked | name obligation and volume/snapshot scope |
| [Include/Planning/HSBI_NewFarCandidate.mqh:33](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_NewFarCandidate.mqh#L33) | two feasible candidates N.2/.3,risk18/12 | MINIMUM_SAFE picks.2 | risk-first comparator picks.3 | existing normative conflict | align already selected A/versioned plans |
| [Include/Planning/HSBI_NewFarSolver.mqh:108](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_NewFarSolver.mqh#L108) | actual residual .4,candidate .2 | promotion actual residual equality independent | candidate≤actual upper does not assert final equality | ERR045OPEN | revalidate post-fill residual and actions |


Expected/current-observation в таблице — static formula reconstruction. Это не actual executed MQL outputs и не assertion об обходе существующего cap gate: cap действительно применяется до safe[]. Числа−520.95/−623.15 относятся к нашему synthetic cost profile.

## Owner-only вопросы

CR09-SUB01 all-requiredscope;02 level semantics;03 requiredIDs/terminal/tail;04 quantity/Far obligation;05 eligibility;06 preview/funding;07 prefix inventory;08 costmanifest;09 numericbound;10 authority/clock;11 legacy mapping. Все11 AWAITING. Не выбирать варианты за владельца. D06A иNewFarA не reopen.
Также нужны D01/02/03/04/05/07/08/10/11/12/13/14/15/16 approvals/receipts/profile/provider по published dependency plan. Результат review принципа не permission implementation.

## Конкретные блокирующие факторы

1. Нет утверждённого активного Rc/Rt/Rs/caps/trigger/terminal/runtime numeric profile; fixtures не defaults.
2. Нет real EURUSD/account margin/cost/asymmetrictick/history/positions/providerclock receipts.
3. Full semantic reading всех545 документов не certified; полный documentation PASS запрещён.
4. Current Small fixture mathematically fails Core-only money for everyN и funding0.
5. Physical future chain/requiredtail не доказана,currentfixedtemplate не наследует position lineage.
6. Нет native compiler/runtime/crash/concurrency evidence и independent durable funding authority.
7. Нет конечного market monetary risk theorem ERR038.

Status=OPEN_BLOCKERS_RECORDED; FULL_MATH_AUDIT_UNPROVEN; TRADING_FORBIDDEN.

## Точные исходные опоры и влияние на торговлю

- [Docs/04_MATHEMATICAL_MODEL_RU.md:9](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/04_MATHEMATICAL_MODEL_RU.md#L9)
- [Docs/05_GEOMETRY_MODEL_RU.md:21](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/05_GEOMETRY_MODEL_RU.md#L21)
- [Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:5](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md#L5)
- [Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md:7](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md#L7)
- [Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md:12](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md#L12)
- [Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:25](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md#L25)
- [Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:12](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md#L12)
- [Docs/24_BROKER_MONEY_MODEL_RU.md:5](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/24_BROKER_MONEY_MODEL_RU.md#L5)
- [Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md:3](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md#L3)
- [Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md:5](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md#L5)
- [Reports/HSBI_03F_R2_D06_A_NORMATIVE_LOCK_RU.md:30](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03F_R2_D06_A_NORMATIVE_LOCK_RU.md#L30)
- [Reports/HSBI_03F_R2_NEWFAR_MINIMUM_SAFE_NORMATIVE_LOCK_RU.md:30](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03F_R2_NEWFAR_MINIMUM_SAFE_NORMATIVE_LOCK_RU.md#L30)

Source blob SHA всех документов — в documentation_inventory.json, SHA25692 protected до/после — в protected_before/after.json. Конфликты source/Docs по full Core/closed Core, fixed template lineage, selective/minAll и objective не исправлены. Реальные risk/margin/provider/profile и full future proof UNAVAILABLE/UNPROVEN. Влияние: implementation, broker dispatch, real trading запрещены независимо от числа Python PASS.
