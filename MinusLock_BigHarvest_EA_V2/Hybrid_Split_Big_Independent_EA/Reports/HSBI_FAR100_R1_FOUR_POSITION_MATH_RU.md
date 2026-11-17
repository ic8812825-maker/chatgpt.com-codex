# FAR100 — Четыре позиции, направления, размеры и деньги

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

## Исходные позиции и текущий снимок

Набор пользователя исследуется как один candidate geometry: F1SELL@1.10000,C1.20BUY@1.10500,T0.60BUY@1.10500,S0.50SELL@1.10500. При ненулевом spread одинаковые BUY/SELL entry1.10500 трактуются как fills на разных synthetic ticks, не одновременно один Bid=Ask. Actual entry quote history UNAVAILABLE.
На Small-снимке Bid1.10250,Ask1.10270:

| PositionID | Role | Direction | OpenPrice | OpenVolume | ClosedVolume | ResidualVolume | Bid | Ask | GrossPnL | Swap | Commission | Fee | Slippage | NetPnL |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MODEL_F0 | FAR | SELL | 1.1 | 1 | 1 | 0 | 1.1025 | 1.1027 | -270 | -1 | -3.5 | 0 | -1 | -275.5 |
| MODEL_C0 | BIG_CORE | BUY | 1.105 | 1.2 | 1.2 | 0 | 1.1025 | 1.1027 | -300 | -1.2 | -4.2 | 0 | -1.2 | -306.6 |
| MODEL_T0 | BIG_TREND | BUY | 1.105 | 0.6 | 0.6 | 0 | 1.1025 | 1.1027 | -150 | -0.6 | -2.1 | 0 | -0.6 | -153.3 |
| MODEL_S0 | SMALL_BASE | SELL | 1.105 | 0.5 | 0.5 | 0 | 1.1025 | 1.1027 | 115 | -0.5 | -1.75 | 0 | -0.5 | 112.25 |


ClosedVolume в этой valuation-таблице — гипотетический полный close-now каждой leg; это не утверждение actual close и не membership SmallTransition. При partial Core следующая таблица изменяет CoreClosed на C−N.

Σgross=−605;Σswap=−3.30;closing commission−11.55;slippage−3.30;FullBasketCloseNowNet=−623.15.
R_all88.45+U−623.15=Economic−534.70; D06 A исключает I100, Recovery=−634.70. Mark-to-market U=−608.30 (без ещё не оплаченных closing commission/slippage), MarkEquity99480.15. CloseNowEquity99465.30. Это два разных economic basis, не ошибка conservation.

## Нормативная геометрия и утверждённые параметры

C=floor(F Rc),T=floor(F Rt),S=ceil(F Rs). При исследовательских1.2/.6/.5 получаем C1.2,T.6,S.5,Bnet1.3,slope.3. GrossBUY1.8,GrossSELL1.5,NetLot−.3,totalGross3.3.
Утверждённые production Rc/Rt/Rs и reserveShare НЕ найдены как активная конфигурация: main EA — disabled skeleton без input-профиля. Tests/MQL5/HSBI_Skeleton_Tests.mq5:49/55 задаёт test-only share.6 и ratios2/1/.5. На F1 этот альтернативный fixture дал бы C2,T1,S.5,Bnet2.5,slope1.5,gross4.5; это не production default.
Docs23 устанавливает ranges Rc>0,Rt≥0,Rs>0, но не назначает активные числовые defaults. Поэтому параллельная **нормативная** геометрия остаётся параметрической; UNKNOWN profile не заменён демонстрационным3/1/1 из03H.

## Зеркальность

Для BUY отражаем price p→2.2−p и меняем BUY↔SELL; quote sides меняются местами: oldFar BUY1@1.10000,Core SELL1.2@1.09500,Trend SELL.6@1.09500,Small BUY.5@1.09500; Bid1.09730/Ask1.09750. PnL всех четырёх legs совпадают с SELL-таблицей; NetLot+.3. Симметрия проверена отдельно на101 market snapshots (tick cost симметричен по явной synthetic premise). Реального asymmetric broker proof это не даёт.

## Slope не гарантия

Research share.8×Bnet1.3=1.04>1, но fullCoreNet−306.60 →eligibleCore0, fullOldFarLoss275.50, disjoint buffer5 →CatchUp−280.50. Geometry проходит, money отказывает независимо от N. При test share.6 lot condition уже .78≤1. Возможность восстановления зависит от цены/fees/sources/funding/risk и FinalClose, не только положительной производной.

Status: exact four-position arithmetic PASS_REFERENCE; real broker parameters UNAVAILABLE; all-gate strategy admissibility UNPROVEN.

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
