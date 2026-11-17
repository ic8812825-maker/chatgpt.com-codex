# FAR100 — Последовательные потенциальные перевороты и точка остановки

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

## Основная последовательность обоих направлений

F0=1.00. На каждом разрешённом переходе должны заново строиться identity, executable entries, C/T/S, candidate grid, required control-price proofs, costs/funding/risk/margin и actual residual. Нельзя принять цепь1→.4→.16 автоматически.
Здесь первый переход уже не прошёл: для всех99 N moneyCatchUp−280.50 и availableTransition0; actual/source/required future отсутствуют. Поэтому **0 fully qualified transitions**, stop до первого irreversible action.

| Начальное направление | F0 | Potential1 | FullyQualified | Potential2…5 | Reason |
|---|---|---|---|---|---|
| SELL | 1 | NO_SAFE_NEW_FAR | 0 | NOT_REACHED; volumes/IDs UNAVAILABLE | Core-only margin−280.50; missing funding/proofs |
| BUY | 1 | NO_SAFE_NEW_FAR | 0 | NOT_REACHED; volumes/IDs UNAVAILABLE | mirror same money |


Это не пять искусственных FAIL-переворотов и не пять заданных остатков: descendants не оцениваются без admissible predecessor. Полный machine stop proof — [multi_transition.json](../Tests/Evidence/FAR100_R1/multi_transition.json). Текущее требование пяти успешно проверенных transitions выполнить на этих inputs нельзя; условие задания допускает доказанную более раннюю остановку.

## Контрфактический один переход и возврат цены (не основная цепь)

Чтобы проверить lineage отдельно от разрешения, diagnostic N.40 оставляет original Core BUY.40@1.10500 для SELL-start. При исходном Small-снимке1.10250/1.10270 следующий tentative basket: CoreSELL.48@1.10250,TrendSELL.24@1.10250,SmallBUY.20@1.10270. Новый Far не переоткрывается и opening commission за его.40 повторно не взимается. Новые legs платят opening.92×3.5=3.22.
Возврат к прежней Far-цене Bid1.10000/Ask1.10020: FarBUY gross−200,CoreSELL+110.40,TrendSELL+55.20,SmallBUY−54;Σgross−88.40. Старый residual сохраняет accrued swap−.40; у новых positions accrued swap0 на этом отдельном snapshot; closing commission−4.62,slippage−1.32 →U_close−94.74. Realized после conditional первого close и новых opens=88.45−520.95−3.22=−435.72; Economic−530.46,RecoveryA−630.46. Price return сам по себе не ошибка направления: Far законно BUY original Core entry1.10500, но никакого profitable exit не доказано.
В зеркальном BUY-start FarSELL.40@1.09500, следующие roles opposite; R/U совпадают при отражённом quote. Это synthetic counterfactual из [scenarios.json](../Tests/Evidence/FAR100_R1/scenarios.json), **не** второй пройденный solver cycle.

## Колебания, конечность и terminal

Для сетки step.01, F0=1 и каждого строго уменьшающегося положительного Far остаётся максимум99 reductions до.01: целочисленный индекс100 должен уменьшаться минимум на1. Это конечность **успешных сжатий**, не конечность времени, recovery или численности retry/events. На F=.01 нет grid N с0<N<.01; требуется отдельный operational terminal close, который может быть денежно недопустим.
При гарантированном q<1 можно оценить log depth, но rounding plateau обязан отвергаться. В этом эксперименте q-chain не установлена; требование strict risk/gross decrease/next basket и money может остановить намного раньше grid terminal — здесь до первого перехода.
Четыре разных утверждения: (1) conditional finite discrete compression доказана; (2) physical partial-close lineage показана для counterfactual; (3) существование допустимой следующей корзины не для всех N (.01fail); (4) profitable FinalClose после нескольких authorised reversals НЕ доказан.

Status=MULTI_TRANSITION_STOPPED_BEFORE_FIRST; FIVE_PASS_NOT_FABRICATED; CURRENT_TEMPLATE_PHYSICAL_CHAIN_UNPROVEN.

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
