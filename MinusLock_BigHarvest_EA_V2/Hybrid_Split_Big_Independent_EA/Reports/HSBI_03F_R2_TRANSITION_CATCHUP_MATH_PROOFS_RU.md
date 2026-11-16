# HSBI-03F-R2 — Математические доказательства Transition/CatchUp

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

Status=MATH_DERIVED_WITH_EXPLICIT_MODEL_BOUNDARY.
ModelVersion=R2-LINEAR-M3-V1. Это независимая синтетическая денежная модель, не broker evidence и не выполненный MQL5 test.

## 1. Источники формул

Include/Money/HSBI_CostModel.mqh:15–18, SourceBlobSHA=293a22c0ff14bc6d635e0cc50c79c8e3d4a7d5cd: gross+signedcomponents−spread−slippage−legbuffer.
HSBI_BasketMoneyEvaluator.mqh:7–17, SourceBlobSHA=4bea204e91a4719b4b24086304cb51051909a7de: четыре legs и basket loss.
Include/Planning/HSBI_GeometrySolver.mqh:21–35: floor/ceil grid и slope.
HSBI_FutureSmallSolver.mqh:63–91,120–147, SourceBlobSHA=be55c93f051f57ddffd189b9d2e8eee4c3ddaf9d: меняющийся Far, recovery monotonicity, terminal proof.
HSBI_NewFarSolver.mqh:118–141: Core-only projected reserve, share, control Far loss, fixed candidate lot.
Docs/04_MATHEMATICAL_MODEL_RU.md:15,21–36; Docs/24_BROKER_MONEY_MODEL_RU.md:3–11.
Проект all-level правила: Reports/HSBI_03E_NEWFAR_OBJECTIVE_RESOLUTION_RU.md:24–42 и pending CR09. Полный контракт ещё PROPOSED.

## 2. Полный математический профиль

CurrencyCode=XTEST3;CurrencyDigits=3;S=1000 minor/main. Эти значения только fixture; не универсальные broker constants.
Все суммы ниже вычислены в целых milli-units; размеры таблиц в main units. Это проверка арифметики в памяти, не test-run production.

Инструмент MODEL_LINEAR_1:
grossBUY(v,p_open,p_close)=v×(p_close−p_open);
grossSELL(v,p_open,p_close)=v×(p_open−p_close).
K=1 money/(lot×price); Point=TickSize=1;Digits=0;TickValueProfit=TickValueLoss=1 per lot/tick.
VolumeMin=VolumeStep=0.05,VolumeMax=10,GridOrigin=0.
Far SELL; Core/Trend BUY; Small SELL. Open prices всех legs100.
Bid=Ask=P_l,spread/slippage/swap/fee fields0. Signed commission Far=−f_l,Small=−s_l,Core/Trend0.
B_leg=1 вычитается в каждой leg; B_CU=1 — отдельный headroom в CatchUp predicate. Здесь воспроизводятся две явные стадии действующих формул. Наличие disjoint cost/headroom receipts в production НЕ доказано; CostBasisManifest остаётся обязательным. Ни один headroom не объявляется actual broker expense.

F_before=(0.4,0.2,0.1); C=3F,T=F,S=F;F_after=(0.2,0.1,0.05).
MaxNewFarRatio0.5;minimum compression lots0.05/ratio0.5;q0.5;maximumDepth3;counts3;terminal atVmin0.05.
NetBig=3F;recoverySlope=2F>0. Все активные lots на сетке и≥min.
Риск как отдельное условие fixture: initial100,tolerance1,level90/80/70. Margin model10 per lot даёт 24/12/6≤100. Initial gross exposure10 и priorBig10; последующие gross2.4/1.2/0.6 и netBig1.2/0.6/0.3 уменьшаются. Это допустимые численные premises, не независимый runtime risk/margin receipt.
Initial money recovery−20;future level cap20;outer min4caps=(12,12,12,12),H12. Values equity/oldFar caps здесь уже в money,не rawpercent.
Projection source EXPLICIT_MODEL, identifiers801/802/803,valid/projected/confirmed fixture flags; actual=false. Флаги не authentic broker authority.

Scope fixture:Broker B_MODEL,Server S_MODEL,Account1,SymbolMODEL_LINEAR_1,Magic7,Cycle7,Plan9,StateRevision5,PolicyVersion3.
MarketSnapshotIds1001/1002/1003,CostSnapshotIds2001/2002/2003,RiskSnapshotIds3001/3002/3003. Subleg cost IDs2011…2014,2021…2024,2031…2034.
Timestamp tick100;trusted fixtureNow100;TTL10;clock FIXTURE_MONOTONIC/tick;epochE1.
Producer/authority REAL instances=NONE. Полные поля quote/grid/volume/source задаются fixture, но финансовая авторизация всегда UNAVAILABLE без real evidence.

## 3. Вывод формул

x_l=F_l×(P_l−100).
FarNet_l=−x_l−f_l−1.
CoreNet_l=3x_l−1.
TrendNet_l=x_l−1.
SmallNet_l=−x_l−s_l−1.
BasketNet_l=2x_l−f_l−s_l−4.
T_l=max(0,−BasketNet_l).
A_l=max(0,−FarNet_l).
Preview eligible=CoreNet_l>0;share4/5.
G_l=(4/5)CoreNet_l.
Margin_l=G_l−A_l−1.

Допустимость costs: все f_l,s_l finite и nonnegative; signed commissions отрицательны, volume/price grids известны. Код не требует одинаковой fee rate между cost snapshots. Реальный брокер может иметь более узкий профиль — это отдельное evidence, здесь его не выдумываем.

## 4. Согласованный контрпример M_MINUS

P=(125,125,150);
Far commission magnitudes f=(2.2,8.2,2.2);
Small commission magnitudes s=(25.8,4.8,6.8).

| L | F | C | Trend | Small | FarNet | CoreNet | TrendNet | SmallNet | BasketNet | T | G | A | Margin |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.4 | 1.2 | 0.4 | 0.4 | -13.2 | 29 | 9 | -36.8 | -12 | 12 | 23.2 | 13.2 | 9 |
| 2 | 0.2 | 0.6 | 0.2 | 0.2 | -14.2 | 14 | 4 | -10.8 | -7 | 7 | 11.2 | 14.2 | -4 |
| 3 | 0.1 | 0.3 | 0.1 | 0.1 | -8.2 | 14 | 4 | -12.8 | -3 | 3 | 11.2 | 8.2 | 2 |

Проверки:
- basket recovery−12>−20,−7>−12,−3>−7: source monotonicity соблюдена.
- T=(12,7,3)≤H12.
- Все per-level lot inequalities0.8×3F>F проходят.
- minMargin−4 на L2;maxT12 на L1. Следовательно argmaxT НЕ argminMargin.
- WORST_CASE выбирает L1 и проверяет margin9. При all-required criterion требуется отказ из-за L2.

Это сильнее произвольной таблицы: числа согласованы с четырьмя legs, одной формулой broker profit, grid, cost signs и обязательной recovery monotonicity. Но это всё ещё математическая модель, не доказанная достижимость успешной ветки реального solver: символ/брокер/provider receipts/native execution отсутствуют.

## 5. Положительная и граничная модификации

Изменить только L2 fees, сохранив f2+s2=13:
| Model | f2 | s2 | Basket L2 | A2 | G2 | Margin2 | All margins |
|---|---:|---:|---:|---:|---:|---:|---|
| M_PLUS |3.2|9.8|−7|9.2|11.2|1|9,1,2 |
| M_ZERO |4.2|8.8|−7|10.2|11.2|0|9,0,2 |
| M_MINUS |8.2|4.8|−7|14.2|11.2|−4|9,−4,2 |

Strict>0 accepts только M_PLUS по CatchUp predicate,при остальных requirements. В native binary64 exact mathematicalzero может оказаться около 0; нельзя объявить native outcome заранее. Future numeric contract требует approved error bounds/точного oracle и запрещает округлять borderline до удобного PASS. Дополнительный native boundary case G12,A11,B1 даёт exact integer zero.

## 6. Почему worstL3 требует отдельной оговорки

При finite genuine producer:
B_(l+1)>B_l из FutureSmallSolver:89,143.
Функция max(0,−B) монотонно невозрастающая по B.
Следовательно T_(l+1)≤T_l. Aggregator strict> выбирает earliest maximum.
T=(3,7,12) с worstL3 противоречит этому producer invariant; его можно предъявить public aggregator как caller DTO с validflags,но нельзя объявлять genuine solver output без нарушения assumptions.
TL03 использует реальную для этой модели альтернативу: T=(12,7,3),EXPLICIT_CONTROL_LEVEL=L2,модель M_PLUS. WorstL1≠controlL2;оба lot checks controlL2 проходят. FINAL_LEVEL=L3 в текущем NewFar имеет отдельный quantity mismatch ниже.

## 7. Почему нельзя просто повторить текущий single-level call

NewFar:123 передаёт FarVolume=candidate0.4 во все возможные control choices.
0.8×NetBig=(0.96,0.48,0.24):
L1 и L2 больше 0.4;L3 не больше 0.4.
Сравнение с собственным FarBefore=(0.4,0.2,0.1) проходит всё.
Поэтому FINAL_LEVEL на M_MINUS может быть отклонён по lot predicate даже при margin2>0. Нельзя заявить, что все селективные политики принимают контрпример.
Proposed all-level contract должен связать volume/direction/position/snapshot конкретного уровня, а не клонировать scalar candidate. Это уточнение требует owner contract decision,не implementation в этом этапе.

## 8. Confirmed reserve и последовательное финансирование

Альтернативный proof той же независимости extrema:
actual source net18.125,share0.8→reserve14.5,residual3.625,остальные grants0;G18.125=14.5+3.625.
Reserved=Consumed0,Free14.5. При независимых оценках checkpoint из M_MINUS:
Margins=(14.5−13.2−1,14.5−14.2−1,14.5−8.2−1)=(0.3,−0.7,5.3).
Constant reserve не делает worstTworstMargin.

Это не три последовательных права потратить 14.5. Для последовательных расходов:
G_b=C_b+R_b+F_b,Free14500minor.
Event7001consume9000: C9000,F5500,revision5→6.
Event7002consume9000 с correctexpectedrevision6: REJECT insufficient,delta0. Новый AllocationKey того же physicalsource необновляет grant. Exact event7001replay→NO_OP,а не повторный расход.
Если checkpoints взаимоисключающие сценарии, один source можно оценивать многократно без mutation;нельзя затем суммировать permissions как независимые деньги. FutureSmall stages обычно последовательны, поэтому дополнительно нужен prefix funding trace,actual receipts и source inventory.
Предлагаемая minMargin проверка необходима, но недостаточна для globallyfunded execution.

## 9. TL001 и actual loss

Far−3,others−9→T12,A3;Far−12,others+9→T3,A12: это разные функции. В futuregate проверяется T_max,в return получается A_control.
ActualTransitionLoss=max(0,−Σ actual closingnet одного OperationID). Он отличается и от singleprojectedbasket,и от maximumdifferentfuturebaskets,и от historicsticky/peak D05.
Basket evaluator закрывает всю projectedCore;реальная Docs13operation сохраняет Core residual. Нужен отдельный close-membership proof;не выводить Actual из Projected посовпадениючисла.

## 10. Пределы/приёмка

Source-level conditional admissibility не native reachability. Даже M_PLUS не предоставляет authority/funding/dispatch. Top solver запрещает UNIT_TEST/injectedproofs;новый native harness должен честно разделять component fixtures и full broker-backed calls.
MATH_DERIVED проверено целочисленной арифметикой; NATIVE_NOT_RUN;новые casesTEST_SPECIFIED_NOT_RUN.
Unresolved:broker instrument/cost/risk/margin profiles,disjoint headrooms,source/clock/registry/journal,fullCR09,per-levelFarbinding,numerics/codec/native,tail risk ERR038.
Приёмка: recompute rows independently;все 3models сохраняют basketmonotonicity/grids/caps;проверены zero/negative margins;нет перехода от syntheticmodel к actualauthority.
Связи: [vectors](HSBI_03F_R2_TEST_VECTOR_SPECIFICATION_RU.md),[ERR018audit](HSBI_03F_R2_ERR018_SOURCE_LEVEL_AUDIT_RU.md),[futurecontract](HSBI_03F_R2_TRANSITION_CATCHUP_CONTRACT_V1_RU.md),[gates](HSBI_03F_R2_DEPENDENCY_AND_READINESS_MATRIX_RU.md).
