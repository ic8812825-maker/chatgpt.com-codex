# FAR100 — Порядок закрытий и единственный остаток Core

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

## Операции и запрет подмены actual

До отправки actions нужны revalidation, immutable persisted plan, repeated fresh touch/hold/retrace/debounce, funding и four caps. Actual deals отсутствуют. Для арифметики ниже N.40 — один из специально запрошенных diagnostic candidates, а не выбранный безопасный остаток. Ни одна строка не является разрешением сделки.

Брокерские ActualClosed/DealIDs/FillStatus UNAVAILABLE. В machine ledger отдельные SimulatedClosed и MODEL_* identity; simulated completed не становится broker completed. Таблица отражает counterfactual, который был бы заблокирован уже на preflight.

| Action | ID | Before lot | Close lot | After lot | Gross at simulated fill | Swap+commission expense | DealNet | EconomicCycleCloseNow | Mark Equity |
|---|---|---|---|---|---|---|---|---|---|
| MODEL_CLOSE_SMALL_BASE | MODEL_S0 | 0.5 | 0.5 | 0 | 114.5 | 2.25 | 112.25 | -534.7 | 99477.9 |
| MODEL_CLOSE_FAR | MODEL_F0 | 1 | 1 | 0 | -271 | 4.5 | -275.5 | -534.7 | 99473.4 |
| MODEL_CLOSE_BIG_TREND | MODEL_T0 | 0.6 | 0.6 | 0 | -150.6 | 2.7 | -153.3 | -534.7 | 99470.7 |
| MODEL_CLOSE_BIG_CORE | MODEL_C0 | 1.2 | 0.8 | 0.4 | -200.8 | 3.6 | -204.4 | -534.7 | 99467.1 |


FarClosed1.00;CoreClosed1.20−.40=.80;Far compression1−.4=.6. Small.5 иTrend.6 закрываются полностью. Единственный оставшийся ID MODEL_C0, BUY.4@1.10500, затем Role BIG_CORE→FAR. В зеркале тот же Core ID становится SELL.4@1.09500. Promotion no-deal не имеет commission/opening fee и не меняет money.

PhysicalClosingNet=112.25−275.50−153.30−204.40=−520.95;ResidualCoreNet−102.20;FullBasket−623.15. Physical TransitionLoss520.95≠FullBasketLoss623.15.

Conservative negative-outflow reservation275.50+153.30+204.40=633.20; positive Small112.25 не автоматически eligible Core income. С разрешённым netting minimum prefix520.95. Обе потребности выше main TransitionBudget0; FinalReserve0. Synthetic four caps1000 each дали бы cap520.95≤1000, но funding/CatchUp/source/future остаются blockers. Это демонстрирует различие cap и funding.

## Все18 checkpoint states каждого направления


### SELL→BUY (N.40 diagnostic, НЕ selected)

| Step | ActionID | PositionIdentifier | RoleBefore | RoleAfter | VolumeBefore | RequestedClose | ActualClosed | VolumeAfter | FillStatus | DealIDs | GrossMoney | Costs | DealNet | CyclePnL | Risk | Margin | State |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | MODEL_REVALIDATION | UNAVAILABLE | NONE | NONE | 0 | 0 | UNAVAILABLE | 0 | SYNTHETIC_CONTROL | MODEL_ONLY:MODEL_REVALIDATION | 0 | 0 | 0 | -534.7 | 300 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 2 | MODEL_IMMUTABLE_PLAN | UNAVAILABLE | NONE | NONE | 0 | 0 | UNAVAILABLE | 0 | SYNTHETIC_CONTROL | MODEL_ONLY:MODEL_IMMUTABLE_PLAN | 0 | 0 | 0 | -534.7 | 300 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 3 | MODEL_TRIGGER_HOLD_RETRACE_DEBOUNCE | UNAVAILABLE | NONE | NONE | 0 | 0 | UNAVAILABLE | 0 | SYNTHETIC_CONTROL | MODEL_ONLY:MODEL_TRIGGER_HOLD_RETRACE_DEBOUNCE | 0 | 0 | 0 | -534.7 | 300 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 4 | MODEL_FUNDING_AND_FOUR_CAPS | UNAVAILABLE | NONE | NONE | 0 | 0 | UNAVAILABLE | 0 | SYNTHETIC_CONTROL | MODEL_ONLY:MODEL_FUNDING_AND_FOUR_CAPS | 0 | 0 | 0 | -534.7 | 300 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 5 | MODEL_CLOSE_SMALL_BASE | MODEL_S0 | SMALL_BASE | CLOSED | 0.5 | 0.5 | UNAVAILABLE | 0 | SYNTHETIC_COMPLETED_MODEL | MODEL_ONLY:MODEL_CLOSE_SMALL_BASE | 114.5 | 2.25 | 112.25 | -534.7 | 800 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 6 | MODEL_CONFIRM_SMALL_BASE | MODEL_S0 | SMALL_BASE | SMALL_BASE | 0.5 | 0 | UNAVAILABLE | 0.5 | SYNTHETIC_CONFIRM_MODEL | MODEL_ONLY:MODEL_CONFIRM_SMALL_BASE | 0 | 0 | 0 | -534.7 | 800 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 7 | MODEL_CLOSE_FAR | MODEL_F0 | FAR | CLOSED | 1 | 1 | UNAVAILABLE | 0 | SYNTHETIC_COMPLETED_MODEL | MODEL_ONLY:MODEL_CLOSE_FAR | -271 | 4.5 | -275.5 | -534.7 | 1800 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 8 | MODEL_CONFIRM_FAR | MODEL_F0 | FAR | FAR | 1 | 0 | UNAVAILABLE | 1 | SYNTHETIC_CONFIRM_MODEL | MODEL_ONLY:MODEL_CONFIRM_FAR | 0 | 0 | 0 | -534.7 | 1800 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 9 | MODEL_CLOSE_BIG_TREND | MODEL_T0 | BIG_TREND | CLOSED | 0.6 | 0.6 | UNAVAILABLE | 0 | SYNTHETIC_COMPLETED_MODEL | MODEL_ONLY:MODEL_CLOSE_BIG_TREND | -150.6 | 2.7 | -153.3 | -534.7 | 1200 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 10 | MODEL_CONFIRM_BIG_TREND | MODEL_T0 | BIG_TREND | BIG_TREND | 0.6 | 0 | UNAVAILABLE | 0.6 | SYNTHETIC_CONFIRM_MODEL | MODEL_ONLY:MODEL_CONFIRM_BIG_TREND | 0 | 0 | 0 | -534.7 | 1200 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 11 | MODEL_CLOSE_BIG_CORE | MODEL_C0 | BIG_CORE | BIG_CORE | 1.2 | 0.8 | UNAVAILABLE | 0.4 | SYNTHETIC_COMPLETED_MODEL | MODEL_ONLY:MODEL_CLOSE_BIG_CORE | -200.8 | 3.6 | -204.4 | -534.7 | 400 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 12 | MODEL_CONFIRM_BIG_CORE | MODEL_C0 | BIG_CORE | BIG_CORE | 1.2 | 0 | UNAVAILABLE | 1.2 | SYNTHETIC_CONFIRM_MODEL | MODEL_ONLY:MODEL_CONFIRM_BIG_CORE | 0 | 0 | 0 | -534.7 | 400 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 13 | MODEL_READ_ACTUAL_RESIDUAL | MODEL_C0 | BIG_CORE | BIG_CORE | 0.4 | 0 | UNAVAILABLE | 0.4 | SYNTHETIC_COUNTERFACTUAL_CONTROL | MODEL_ONLY:MODEL_READ_ACTUAL_RESIDUAL | 0 | 0 | 0 | -534.7 | 400 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 14 | MODEL_NEWFAR_SOLVER | MODEL_C0 | BIG_CORE | BIG_CORE | 0.4 | 0 | UNAVAILABLE | 0.4 | SYNTHETIC_COUNTERFACTUAL_CONTROL | MODEL_ONLY:MODEL_NEWFAR_SOLVER | 0 | 0 | 0 | -534.7 | 400 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 15 | MODEL_PROMOTION | MODEL_C0 | BIG_CORE | FAR | 0.4 | 0 | UNAVAILABLE | 0.4 | SYNTHETIC_COUNTERFACTUAL_CONTROL | MODEL_ONLY:MODEL_PROMOTION | 0 | 0 | 0 | -534.7 | 400 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 16 | MODEL_PERSIST | MODEL_C0 | FAR | FAR | 0.4 | 0 | UNAVAILABLE | 0.4 | SYNTHETIC_COUNTERFACTUAL_CONTROL | MODEL_ONLY:MODEL_PERSIST | 0 | 0 | 0 | -534.7 | 400 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 17 | MODEL_RECONCILIATION | MODEL_C0 | FAR | FAR | 0.4 | 0 | UNAVAILABLE | 0.4 | SYNTHETIC_COUNTERFACTUAL_CONTROL | MODEL_ONLY:MODEL_RECONCILIATION | 0 | 0 | 0 | -534.7 | 400 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 18 | MODEL_NEXT_STATE | MODEL_C0 | FAR | FAR | 0.4 | 0 | UNAVAILABLE | 0.4 | SYNTHETIC_COUNTERFACTUAL_CONTROL | MODEL_ONLY:MODEL_NEXT_STATE | 0 | 0 | 0 | -534.7 | 400 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |


### BUY→SELL (N.40 diagnostic, НЕ selected)

| Step | ActionID | PositionIdentifier | RoleBefore | RoleAfter | VolumeBefore | RequestedClose | ActualClosed | VolumeAfter | FillStatus | DealIDs | GrossMoney | Costs | DealNet | CyclePnL | Risk | Margin | State |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | MODEL_REVALIDATION | UNAVAILABLE | NONE | NONE | 0 | 0 | UNAVAILABLE | 0 | SYNTHETIC_CONTROL | MODEL_ONLY:MODEL_REVALIDATION | 0 | 0 | 0 | -534.7 | 300 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 2 | MODEL_IMMUTABLE_PLAN | UNAVAILABLE | NONE | NONE | 0 | 0 | UNAVAILABLE | 0 | SYNTHETIC_CONTROL | MODEL_ONLY:MODEL_IMMUTABLE_PLAN | 0 | 0 | 0 | -534.7 | 300 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 3 | MODEL_TRIGGER_HOLD_RETRACE_DEBOUNCE | UNAVAILABLE | NONE | NONE | 0 | 0 | UNAVAILABLE | 0 | SYNTHETIC_CONTROL | MODEL_ONLY:MODEL_TRIGGER_HOLD_RETRACE_DEBOUNCE | 0 | 0 | 0 | -534.7 | 300 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 4 | MODEL_FUNDING_AND_FOUR_CAPS | UNAVAILABLE | NONE | NONE | 0 | 0 | UNAVAILABLE | 0 | SYNTHETIC_CONTROL | MODEL_ONLY:MODEL_FUNDING_AND_FOUR_CAPS | 0 | 0 | 0 | -534.7 | 300 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 5 | MODEL_CLOSE_SMALL_BASE | MODEL_S0 | SMALL_BASE | CLOSED | 0.5 | 0.5 | UNAVAILABLE | 0 | SYNTHETIC_COMPLETED_MODEL | MODEL_ONLY:MODEL_CLOSE_SMALL_BASE | 114.5 | 2.25 | 112.25 | -534.7 | 800 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 6 | MODEL_CONFIRM_SMALL_BASE | MODEL_S0 | SMALL_BASE | SMALL_BASE | 0.5 | 0 | UNAVAILABLE | 0.5 | SYNTHETIC_CONFIRM_MODEL | MODEL_ONLY:MODEL_CONFIRM_SMALL_BASE | 0 | 0 | 0 | -534.7 | 800 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 7 | MODEL_CLOSE_FAR | MODEL_F0 | FAR | CLOSED | 1 | 1 | UNAVAILABLE | 0 | SYNTHETIC_COMPLETED_MODEL | MODEL_ONLY:MODEL_CLOSE_FAR | -271 | 4.5 | -275.5 | -534.7 | 1800 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 8 | MODEL_CONFIRM_FAR | MODEL_F0 | FAR | FAR | 1 | 0 | UNAVAILABLE | 1 | SYNTHETIC_CONFIRM_MODEL | MODEL_ONLY:MODEL_CONFIRM_FAR | 0 | 0 | 0 | -534.7 | 1800 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 9 | MODEL_CLOSE_BIG_TREND | MODEL_T0 | BIG_TREND | CLOSED | 0.6 | 0.6 | UNAVAILABLE | 0 | SYNTHETIC_COMPLETED_MODEL | MODEL_ONLY:MODEL_CLOSE_BIG_TREND | -150.6 | 2.7 | -153.3 | -534.7 | 1200 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 10 | MODEL_CONFIRM_BIG_TREND | MODEL_T0 | BIG_TREND | BIG_TREND | 0.6 | 0 | UNAVAILABLE | 0.6 | SYNTHETIC_CONFIRM_MODEL | MODEL_ONLY:MODEL_CONFIRM_BIG_TREND | 0 | 0 | 0 | -534.7 | 1200 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 11 | MODEL_CLOSE_BIG_CORE | MODEL_C0 | BIG_CORE | BIG_CORE | 1.2 | 0.8 | UNAVAILABLE | 0.4 | SYNTHETIC_COMPLETED_MODEL | MODEL_ONLY:MODEL_CLOSE_BIG_CORE | -200.8 | 3.6 | -204.4 | -534.7 | 400 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 12 | MODEL_CONFIRM_BIG_CORE | MODEL_C0 | BIG_CORE | BIG_CORE | 1.2 | 0 | UNAVAILABLE | 1.2 | SYNTHETIC_CONFIRM_MODEL | MODEL_ONLY:MODEL_CONFIRM_BIG_CORE | 0 | 0 | 0 | -534.7 | 400 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 13 | MODEL_READ_ACTUAL_RESIDUAL | MODEL_C0 | BIG_CORE | BIG_CORE | 0.4 | 0 | UNAVAILABLE | 0.4 | SYNTHETIC_COUNTERFACTUAL_CONTROL | MODEL_ONLY:MODEL_READ_ACTUAL_RESIDUAL | 0 | 0 | 0 | -534.7 | 400 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 14 | MODEL_NEWFAR_SOLVER | MODEL_C0 | BIG_CORE | BIG_CORE | 0.4 | 0 | UNAVAILABLE | 0.4 | SYNTHETIC_COUNTERFACTUAL_CONTROL | MODEL_ONLY:MODEL_NEWFAR_SOLVER | 0 | 0 | 0 | -534.7 | 400 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 15 | MODEL_PROMOTION | MODEL_C0 | BIG_CORE | FAR | 0.4 | 0 | UNAVAILABLE | 0.4 | SYNTHETIC_COUNTERFACTUAL_CONTROL | MODEL_ONLY:MODEL_PROMOTION | 0 | 0 | 0 | -534.7 | 400 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 16 | MODEL_PERSIST | MODEL_C0 | FAR | FAR | 0.4 | 0 | UNAVAILABLE | 0.4 | SYNTHETIC_COUNTERFACTUAL_CONTROL | MODEL_ONLY:MODEL_PERSIST | 0 | 0 | 0 | -534.7 | 400 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 17 | MODEL_RECONCILIATION | MODEL_C0 | FAR | FAR | 0.4 | 0 | UNAVAILABLE | 0.4 | SYNTHETIC_COUNTERFACTUAL_CONTROL | MODEL_ONLY:MODEL_RECONCILIATION | 0 | 0 | 0 | -534.7 | 400 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |
| 18 | MODEL_NEXT_STATE | MODEL_C0 | FAR | FAR | 0.4 | 0 | UNAVAILABLE | 0.4 | SYNTHETIC_COUNTERFACTUAL_CONTROL | MODEL_ONLY:MODEL_NEXT_STATE | 0 | 0 | 0 | -534.7 | 400 | SYN profiles in JSON; broker UNAVAILABLE | PROJECTED_ONLY_NOT_AUTHORIZED |


Полные до/после Positions и все margin profiles — [physical_transitions.json](../Tests/Evidence/FAR100_R1/physical_transitions.json). Confirm rows с нулевым simulated close не новые deals; исторические original descriptors не заменяют observation. Финальный marked state контрфактический, фактический outcome всё время NOT_EXECUTED.

## Негативные события и restart

Reference barrier проверяет partial.20 из.50 →PENDING, следующий action запрещён; delayed.30 дополняет ту же Action до.50. Identical event replay→NO_OP, altered volume→CONFLICT. TIMEOUT/unknown оставляет barrier, wrong identifier/overfill/missing deal/core/twoFar/unreconciled volume блокируют continuation. Повтор ActionID не должен давать второй расход.
18 checkpoint JSON roundtrips сохраняют pending state; это **не** process crash, disk durability либо MQL5. Native/durable restart tests NOT_RUN. Requested.40 против observation.39 не допускает promotion до reconcile/replan. Нельзя открыть новую Far вместо исчезнувшего Core.

Status=PHYSICAL_ACCOUNTING_REFERENCE_VERIFIED; ACTUAL_EXECUTION_UNAVAILABLE; AUTHORIZED_TRANSITIONS0.

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
