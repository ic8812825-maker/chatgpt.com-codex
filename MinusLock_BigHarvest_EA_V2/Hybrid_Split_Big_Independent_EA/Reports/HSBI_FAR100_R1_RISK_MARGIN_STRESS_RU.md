# FAR100 — Risk, margin и девять сценариев A–I

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

## Общий adverse basis и ограничения риска

На Small-снимке GrossBUY1.8,GrossSELL1.5,netBUY.3,totalGross3.3. Для сравнения задаём два одинаковых для old/next immutable stress quotes: current Bid/Ask±0.01000 (100pip). Synthetic Risk=max(0,ValueNow−ValueAtEachStress). Исходная basketRisk300. На diagnostic N.4 новая basket имеет FarBUY.4,CSELL.48,TSELL.24,SBUY.20,totalGross1.32,netSELL.12,тот же symmetric stressRisk120. Таким образом120<300−tolerance1 на ограниченном stress basis, но это не проверка всех adverse/gap/holding сценариев и не broker RiskNext proof.
Если сравнивать лишь один adverse quote старой basket, он может быть благоприятным для новой: нельзя менять controlbasis с направлением и объявлять нулевой risk универсальным.

Уменьшение Far не гарантирует меньший account risk: до Far1 с stress100USD,после Far.4 соstress40USD плюс другая account position соstress10000USD →10040>100. Gross hedge margin тоже зависит от pairing/contract, не только net lots. Нужен независимый account-wide snapshot/ownership/foreign exposure policy. Модель не скрывает эти ограничения.

WorstCaseLoss на неограниченном рынке не доказан finite: для shortN>0 loss≈100000NΔP→∞. Ни q-compression, ни малое число позиций, ни finite stress tests/stopout не дают универсальной exit-price гарантии. ERR038 OPEN. Уровень Vmin не означает закрытый прибыльный цикл.

## Три margin profiles, каждый явно synthetic

Notional perlot=100000×mid, leverage100. Main mid1.10260. GROSS: charge(BUY+SELL)/100=3638.58; HEDGED_MAX:charge max(BUY,SELL)/100=1984.68; HEDGED20:charge[max+.2min]/100=2315.46USD. Actual broker calc mode/hedged-margin/account currency rules UNAVAILABLE.

| Profile | MarginUsed | FreeMarginAfter | MarginLevel% |
|---|---|---|---|
| SYN_GROSS_1_100 | 3638.58 | 95841.57 | 2734.03772900417195719209142 |
| SYN_HEDGED_MAX | 1984.68 | 97495.47 | 5012.402503174315254852167604 |
| SYN_HEDGED20 | 2315.46 | 97164.69 | 4296.34500272084164701614366 |


Main EquityMark99480.15; CycleDD.51985% от100000,AccountDD.619230769…% отpeak100100. Величины не из net lots. Каждый candidate JSON содержит свои profiles, risk, compression и nextgeometry; поле UNAVAILABLE при невозможной geometry, а не нулевая margin.

## Девять сценариев

A сильный Big: Bid1.13000/Ask1.13020, recovery190.30≥16. OrdinaryFinalClose RESULT gate выполнен на synthetic snapshot, поэтому сначала FinalClose preview, не ненужный переворот. Funding/ownership/freshness/etc требуют независимых receipts; actual authorization UNAVAILABLE.
B Small: Bid1.10250/Ask1.10270, recovery−634.70,CatchUp−280.50,TransitionBudget0; нет первого qualified flip. Trigger repeated snapshot/hold/debounce не доказан самим price touch.
C возврат после conditional flip: originalCore становится Far с inherited entry; возврат кстарой цене не ошибка автоматически. При diagnostic N.4 new basket recovery−630.46, predecessor blocked; см.multi report.
D колебания2–5: завершено0 допускаемых transitions, descendants NOT_REACHED. Независимо заданная geometric sequence не заменяет solver. Нет утверждения profitable mean reversion.
E длинный тренд: при Bid1.20000 old netBUY basket достигает recovery2290.30 и при valid final authority должна закрываться; но при противоположном тренде или после иных exposures убыток может расти без bound. Полагаться на возврат запрещено.
F gap: Bid1.08000/Ask1.08300,stale=true. Пропущенные уровни, changed fingerprint, slippage/fill uncertainty блокируют admission до revalidation. Старый plan не используется; actual equity/fill UNAVAILABLE, synthetic mark не гарантированный exit.
G spread.00200 и closingcommission50/lot: geometry.3 не меняется, quote money/fees ухудшаются. Основные Metrics в JSON используют baseline3.5; HighCommissionNet/HighCommissionRecoveryA и Legs отражают50. Эти scopes явно различены, не подставлены в один scalar. При SELL Bid1.10500/Ask1.10700 highcommission close net−971.60,RecoveryA−983.15. Swap−3.3 иslip−3.3 сохраняются; OpeningFees остаются ранее paid11.55, не заменены новой тарифной историей.
H grids: step.01 base geometry1.2/.6/.5,slope.3;step.10 то же;step.25 C1.00,T.50,S.50,Bnet1,slope0→reject. N.01 nextbasket impossible. Terminal min requires own guarded close; positive lot compression без next geometry не проходит.
I полный FinalClose: rootthreshold Bid1.12419/Ask1.12439 даёт ровно Recovery16.00; предыдущий tick1.12418 даёт15.70<threshold. Full close всех четырёх legs приводит кactualZero только после completed fills/reconciliation, а не расчёта. Emergency loss never SUCCESSFUL_RECOVERY.

| Scenario | Direction | RecoveryA | 100pip risk | Gross lots | Gross margin | Mark equity | Final result gate only |
|---|---|---|---|---|---|---|---|
| A_STRONG_BIG | -1 | 190.3 | 300 | 3.3 | 3729.33 | 100305.15 | True |
| A_STRONG_BIG | 1 | 190.3 | 300 | 3.3 | 3530.67 | 100305.15 | True |
| B_SMALL | -1 | -634.7 | 300 | 3.3 | 3638.58 | 99480.15 | False |
| B_SMALL | 1 | -634.7 | 300 | 3.3 | 3621.42 | 99480.15 | False |
| E_LONG_TREND | -1 | 2290.3 | 300 | 3.3 | 3960.33 | 102405.15 | True |
| E_LONG_TREND | 1 | 2290.3 | 300 | 3.3 | 3299.67 | 102405.15 | True |
| F_GAP | -1 | -1729.7 | 300 | 3.3 | 3568.95 | 98385.15 | False |
| F_GAP | 1 | -1729.7 | 300 | 3.3 | 3691.05 | 98385.15 | False |
| G_SPREAD_COMMISSION | -1 | -829.7 | 300 | 3.3 | 3649.8 | 99285.15 | False |
| G_SPREAD_COMMISSION | 1 | -829.7 | 300 | 3.3 | 3610.2 | 99285.15 | False |
| I_THRESHOLD | -1 | 16 | 300 | 3.3 | 3710.157 | 100130.85 | True |
| I_THRESHOLD | 1 | 16 | 300 | 3.3 | 3549.843 | 100130.85 | True |
| C_RETURN_AFTER_COUNTERFACTUAL_FLIP | -1 | -630.46 | 120 | 1.32 | 1452.132 | 99475.48 | PREDECESSOR_BLOCKED |
| C_RETURN_AFTER_COUNTERFACTUAL_FLIP | 1 | -630.46 | 120 | 1.32 | 1451.868 | 99475.48 | PREDECESSOR_BLOCKED |


Все сценарные prices — fixed test inputs, не реальные quotes. [scenarios.json](../Tests/Evidence/FAR100_R1/scenarios.json),[grid_boundaries.json](../Tests/Evidence/FAR100_R1/grid_boundaries.json). Asymmetric synthetic variant задаётся profit_tick1/loss_tick1.2 в reference leg; без реального payout/calculation-mode receipt она не broker EURUSD proof.

Status=RISK_MARGIN_SYNTHETIC_CALCULATED; BROKER_PROOF_UNAVAILABLE; UNBOUNDED_TAIL_UNPROVEN.

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
