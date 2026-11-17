# FAR100 — Полный broker-grid search без искусственного безопасного N

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

## Полная область поиска

99 values N=.01,.02,…,.99 для каждого направления. Исследовательский профиль RESEARCH_ALPHA50: maxNewFarRatio.5,minCompressionLots.01,minCompressionRatio.5. Отдельный HISTORICAL_TEST_ALPHA60: .6/.2/.2 из native fixture, не production approval. Всего396 rows (99×2directions×2policies) сохранены в [полной сетке](../Tests/Evidence/FAR100_R1/new_far_candidates.json).
Grid synthetic EURUSD min/step.01,max100,origin0. Все99 на grid и0<N<1; physical possible residual≤C1.2, но actual residual и source proof UNAVAILABLE. Значения≥.51 не проходят profile50 compression; profile60 допускает до.60 по этому фильтру.

## Специально запрошенные N (SELL; BUY зеркален)

| N | Compression | Grid | RecoveryMoney | CatchUp | PhysicalTransitionLoss | RiskOld/Next | Next slope | Margin gross USD | FutureSmall | FinalStatus |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.01 | 0.99 | synthetic valid | -634.7 | -280.5 | 620.595 | 300.0000000/UNAVAILABLE | -0.01 | UNAVAILABLE | UNPROVEN | REJECT |
| 0.05 | 0.95 | synthetic valid | -634.7 | -280.5 | 610.375 | 300.0000000/10.0000000 | 0.01 | 187.442 | UNPROVEN | REJECT |
| 0.1 | 0.9 | synthetic valid | -634.7 | -280.5 | 597.6 | 300.0000000/30.0000000 | 0.03 | 363.858 | UNPROVEN | REJECT |
| 0.2 | 0.8 | synthetic valid | -634.7 | -280.5 | 572.05 | 300.0000000/60.0000000 | 0.06 | 727.716 | UNPROVEN | REJECT |
| 0.3 | 0.7 | synthetic valid | -634.7 | -280.5 | 546.5 | 300.0000000/90.0000000 | 0.09 | 1091.574 | UNPROVEN | REJECT |
| 0.4 | 0.6 | synthetic valid | -634.7 | -280.5 | 520.95 | 300.0000000/120.0000000 | 0.12 | 1455.432 | UNPROVEN | REJECT |
| 0.5 | 0.5 | synthetic valid | -634.7 | -280.5 | 495.4 | 300.0000000/150.0000000 | 0.15 | 1819.29 | UNPROVEN | REJECT |


Каждая machine row содержит следующие required fields: CandidateN,Compression,BrokerGrid,RecoveryMoney,CatchUp,TransitionLoss,RiskOld/RiskNext,Margin,FutureSmall,FinalStatus и полный RejectReasons. Risk/Margin — только synthetic profiles; native broker counterpart UNAVAILABLE. Next C/T/S пересчитываются floor/floor/ceil по каждому N.
N.01→C.01,T0,S.01,Bnet0,slope−.01, geometry fail; никакое уменьшение объёма не исправляет next-cycle feasibility. N.05→C.06,T.03,S.03,slope.01, но CatchUp всё равно−280.50. N.4→next volumes.48/.24/.20, slope.12,gross1.32; контрольный stress risk120 против300, однако это не all-required proof.

## Доказательство отсутствия safe candidate на этом снимке

Для ЛЮБОГО N∈grid fullCoreCloseNowNet=−306.60, eligible=max(0,−306.60)=0. OldFar полностью1lot, его close-net−275.50. Потому M(N)=.8×0−275.50−5=−280.50<0, независимо от compression и output ranking. На этих входах нет безопасного кандидата в принятой conditional Core-only интерпретации: **NO_SAFE_NEW_FAR**. Actual current MQL solver не запускался; его observed result НЕ заявляется как NO_SAFE_CANDIDATE.
Более общая стратегия может иметь другие facts/sources/prices; impossibility не переносится на все HSBI states. До CR09 concrete obligations/eligibility/profile/source/future утверждение полной production feasibility остаётся UNPROVEN.

RecoveryMoney=−634.70 на одном снимке для всех N: перераспределение realized/open без изменения цены не создаёт восстановление. PhysicalClosingNet(N)=−623.15+255.50N;ResidualNet(N)=−255.50N; сумма неизменна. Funding в full machine ledger не подменено closing loss.

## Полный declared control range

Дополнительно рассчитаны2501 tick от Bid1.10500 до1.13000 приspread.00020, включая оба конца. В control_price_curve.json сохранены RecoveryA,Core-only CatchUp,closed-Core(.8lot) CatchUp и условный Core+Trend CatchUp. Core-only margin отрицательна во всех2501 точках; точка FinalClose result gate не становится funding authority. Этот declared finite range не заменяет неутверждённый CR09 required manifest/tail.

## Выбор и source различия

SelectedNewFar=NONE, потому что feasible set пуст, а не потому что.40 неудобен. Minimum-safe выбирал бы первый полностью qualified N, но здесь такого нет. Подстановка convenient N запрещена. Owner NewFar A не пересматривается. Source NewFarSolver108–151 допускает поисковые candidates меньше имеющегося actual residual; selectedVolume не является доказанным final residual. Equality requested/actual нужно проверять после fills независимо. Identity/refunding/future unknown не дают valid.

Status=GRID_ENUMERATION_COMPLETE_REFERENCE; CONDITIONAL_NO_SAFE_NEW_FAR; NATIVE_SOLVER_NOT_RUN.

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
