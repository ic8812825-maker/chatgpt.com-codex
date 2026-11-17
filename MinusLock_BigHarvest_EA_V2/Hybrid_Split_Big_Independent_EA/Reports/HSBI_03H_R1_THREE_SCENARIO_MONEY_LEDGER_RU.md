# HSBI-03H-R1 — Три синтетических денежных сценария с физической lineage

DocumentVersion=HSBI-03H-R1-V1
SourceCommitSHA=70cc4c861b391a7916403106ff07f25729e602da
EvidenceClass=STATIC_REVIEWED; MATH_DERIVED; TEST_SPECIFIED_NOT_RUN
NormativeStatus=AUDIT_SPEC_ONLY_PROPOSED_AWAITING_OWNER_APPROVAL

Репозиторий: ic8812825-maker/chatgpt.com-codex; ветка work. Все пути относительно MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/. Режим GITHUB_MCP_REMOTE_ONLY, локальных файловых операций нет. SourceCommitSHA — исследованная база, не будущий commit отчётов.
D-06=A и NewFar=A/MINIMUM_SAFE_V1 сохраняются. Новых owner selections и approval receipts этот документ не создаёт. Все числовые торговые примеры синтетические; подтверждённых брокерских сделок в них нет.
PRODUCTION_CHANGED=NO; R11_IMPLEMENTATION_ALLOWED=NO; BROKER_DISPATCH_ALLOWED=NO; REAL_TRADING_ALLOWED=NO; NATIVE_MQL5_TESTS=NOT_RUN.
UNAVAILABLE — отсутствует доказательство, CONFLICT — противоречие, REJECT — доказанное нарушение. Ни один из этих результатов не разрешает новый финансовый эффект. Математическое ожидание не является фактическим PASS.

Scope=два зеркальных направления, недостаточное funding, same-position PartialFar, два projected promotions и разные extrema
Dependencies=Docs04/08/09/10/11/12/13/14; CostModel; BasketMoneyEvaluator; ReserveCatchUpEvaluator; physical ledger и semantics verdict этого пакета
OpenQuestions=actual broker parameters/receipts; разрешённые offsets/buckets/eligibility; gates физической рекурсии; provider/native evidence
AcceptanceCriteria=каждый lot и денежная сумма пересчитываются; closed volume не compression; ни одна projection не названа исполнением; расходы ровно один раз

## Область доказательства и модель

ВСЕ суммы и события ниже — SYNTHETIC_MATH_ONLY. Брокерские сделки, native вызовы, фактические fills и successful solver route отсутствуют. Строки close — условное раскрытие плана для проверки арифметики. Если gate не выполнен, это не означает, что сделки всё же выполнены. Реальный результат аудита во всех сценариях: торговых действий НЕТ.

Единый профиль SYN_LINEAR100_X3: Symbol=SYN_HSBI, ContractSize=100, TickSize=1, TickValue=100 XTEST3 за lot/tick (BUY/SELL симметричны), Point=1, Digits=0, LotStep=0.01, LotMin=0.01, LotMax=10, GridOrigin=0. Spread=0, Commission=0 на open/close, Swap=0, SlippageAssumption=0, Fee=0, physical remaining Costs=0. Это объявленная идеализированная zero-cost модель, не предположение о реальном брокере. Валюта XTEST3, расчёт в exact milli-units; все использованные результаты целые/десятичные точно.
BUY gross=100 v(P−open), SELL gross=100 v(open−P); Bid=Ask=P. Все цены кратны tick. Новые baskets в примерах имеют Rc=3,Rt=1,Rs=1.
CatchUpBuffer B=1 — отдельный математический safety headroom, не денежный расход; он не входит повторно в CyclePnL. ReserveShare=0.8 для Core-only projected preview; уже allocated Free повторно на share не умножается.
Compression guards модели: maximumNewFarRatio0.5, minimumCompressionLots0.01, minimumCompressionRatio0.5. Для F1,N0.4: compression0.6,ratio0.6. Для F0.4,N0.16:0.24,ratio0.6.

NetLot=ΣSELL−ΣBUY (положительный знак означает net SELL).
RealizedPnL=Σ уникальных closed net; UnrealizedPnL=Σ open close-now net.
CyclePnL=RealizedPnL+UnrealizedPnL−Costs, здесь Costs=0, потому что все затраты заданы нулём.
Для ненулевых costs в другой модели Net уже включает свои расходы; Costs содержит только ещё не включённые. B не cash expense.
Balance=InitialDeposit+RealizedPnL; Equity=Balance+UnrealizedPnL; allocations не прибавляются.

### Общее синтетическое начальное происхождение денег

InitialDeposit=89000. INITIAL BUY1@100/SELL1@100; в S1 цена90, закрыт INITIAL_SELL +1000, остаётся BUY1@100. В S2/S3 цена110, закрыт INITIAL_BUY +1000, остаётся SELL1@100. InitialProfitExcluded I=1000.
Далее независимо задан complete synthetic historical Core closing source H: BUY1@10→close110, net+10000, AccountMODEL/ServerMODEL/CycleMODEL/H. Это входной settled source пример, а НЕ доказательство достижимости всего предыдущего пути HSBI. Полная реальная history и actual association UNAVAILABLE.
Таким образом before scenarios R_all=11000, RecoveryRealized_A=10000, StartingBalance=100000. Opening deals не создают harvest grants. H — единственный eligible source budgets. Бюджеты S1/S2: Transition5000, FinalReserve4000, PartialFar100, Carry0, Residual900; сумма10000. S3: Transition500,FinalReserve4000,PartialFar100,Carry0,Residual5400; тоже10000.
Все grants — части уже учтённых10000, не дополнительная equity. Свободные Transition funds обозначим F_Tr, FinalReserve F_Final=4000. Разрешение их использовать остаётся математической premise, не owner approval.
Для FinalClose result illustration H_in=0, MinimumRecoveryProfit=20000, H_gate=1, tolerance=0, threshold20001. Поэтому positive equity/cycle result не создаёт successful recovery gate. Этот высокий threshold — явно выбранная fixture-константа, не параметр действующей стратегии.

## S1 — движение вверх: убыточная Far BUY, остаток SELL Core

StartingPositions: A1 FAR BUY1@100; A2 BIG_CORE SELL3@80; A3 BIG_TREND SELL1@80; A4 SMALL_BASE BUY1@80.
Начальная оценка при P80: U=−2000, StartingBalance100000, StartingEquity98000, NetLot=2.
Цена80→90. При P90 legs=(-1000,-3000,-1000,+1000), U=−4000, Equity96000, CyclePnL=7000. Именно Small выигрывает, а исходная Far всё ещё убыточна.

Условный SmallTransition: A4 full1, A1 full1, A3 full1, A2 partial2.6, затем A2 residual0.4→FAR SELL. Close-side для BUY/SELL совпадает с90 только из-за объявленного нулевого spread.

| Шаг | Позиции до → действие → позиции после (id:role direction lot@open) | ΔR | R_all | U_after | NetLot | Balance | Equity | CyclePnL |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| S1-0 | A1:F BUY1@100,A2:C SELL3@80,A3:T SELL1@80,A4:S BUY1@80; mark90 | 0 | 11000 | −4000 | 2 | 100000 | 96000 | 7000 |
| S1-1 | те же4 → close A4 BUY1@90 → A1,A2,A3 | +1000 | 12000 | −5000 | 3 | 101000 | 96000 | 7000 |
| S1-2 | A1,A2,A3 → close A1 BUY1@90 → A2,A3 | −1000 | 11000 | −4000 | 4 | 100000 | 96000 | 7000 |
| S1-3 | A2,A3 → close A3 SELL1@90 → A2 SELL3@80 | −1000 | 10000 | −3000 | 3 | 99000 | 96000 | 7000 |
| S1-4 | A2 SELL3@80 → close2.6@90 → A2 C SELL0.4@80 | −2600 | 7400 | −400 | 0.4 | 96400 | 96000 | 7000 |
| S1-5 | A2 C SELL0.4@80 → validate/promote, no deal → A2 FAR SELL0.4@80 | 0 | 7400 | −400 | 0.4 | 96400 | 96000 | 7000 |

В последней строке OldFar A1 residual=0; BigCore A2 physical residual=0.4; после promotion Role BIG_CORE больше нет, physical position A2 сохранена. Новая Far не A1 residual. F−N=0.6, закрыто old Far1, Core2.6.
Closing group net=1000−1000−1000−2600=−3600; TransitionLoss=3600.
Full-basket close-now net=−4000, basket loss4000. Разница400 — незакрытый отрицательный остаток Core, не потерянная комиссия.

### Funding и CatchUp S1

По action order negative outflows1000(Far)+1000(Trend)+2600(Core)=4600. Консервативная pre-reservation4600 из F_Tr5000 оставляет free400, reserved4600; после соответствующих условных settlements consumed4600,reserved0,free400. Small+1000 не считается новым eligible Core income; он остаётся экономическим результатом без автоматического grant. Если владелец в будущем разрешит netting этой положительной суммы внутри transition funding, минимальная net/prefix потребность3600; это ДРУГОЙ loss-consumption contract, здесь не выбран.
F_Final4000 не расходуется и не подменяет TransitionBudget. Копирование grants на каждом уровне запрещено.
Core-only projected G=0.8 max(−3000,0)=0; A=1000 для OLD Far BUY1; CatchUpMargin=0−1000−1=−1001. Уже allocated FinalReserve4000 дал бы диагностический headroom2999, но current validator требует positive projected Core proof; нельзя заменить этот провал финансовым разрешением.
Все projected closes в таблице — counterfactual reconciliation oracle; при failed CatchUp реальный план не запускается.


### Пооперационный остаток бюджета S1/S2

Это projected conservative reservation lifecycle, не actual registry. Перед plan F_Tr5000,Reserved0,Consumed0; reserve4600 →Free400,Reserved4600. F_Final4000 и F_Partial100 во всех строках неизменны. Положительный Small не вызывает grant.

| Action prefix S1/S2 | Δclosing net | cumulative closing net | net prefix loss | negative debit этого шага | Tr Consumed | Tr Reserved | Tr Free |
|---|---:|---:|---:|---:|---:|---:|---:|
| plan reserved |0|0|0|0|0|4600|400|
| Small full |+1000|1000|0|0|0|4600|400|
| OldFar full |−1000|0|0|1000|1000|3600|400|
| Trend full |−1000|−1000|1000|1000|2000|2600|400|
| Core partial |−2600|−3600|3600|2600|4600|0|400|
| promotion no-deal |0|−3600|3600|0|4600|0|400|

Каждая строка сохраняет Grant5000=Consumed+Reserved+Free. Объём old Far после Small1,после OldFar0; Core до последнего close3,после него0.4. Synthetic physical costs0 на всех actions. CatchUp −1001 относится к проверке всего планового перехода до actions, а не новому source grant после каждой строки. Изменение роли Core→Far не уменьшает funding и не меняет money.

## S2 — движение вниз: убыточная Far SELL, остаток BUY Core

StartingPositions: B1 FAR SELL1@100; B2 C BUY3@120; B3 T BUY1@120; B4 S SELL1@120.
Начальная оценка P120: U−2000, StartingBalance100000, StartingEquity98000, NetLot−2.
Цена120→110. Legs=(-1000,-3000,-1000,+1000), U−4000.

| Шаг | Позиции до → действие → позиции после | ΔR | R_all | U_after | NetLot | Balance | Equity | CyclePnL |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| S2-0 | B1:F SELL1@100,B2:C BUY3@120,B3:T BUY1@120,B4:S SELL1@120; mark110 | 0 | 11000 | −4000 | −2 | 100000 | 96000 | 7000 |
| S2-1 | B1,B2,B3,B4 → close B4 SELL1@110 → B1,B2,B3 | +1000 | 12000 | −5000 | −3 | 101000 | 96000 | 7000 |
| S2-2 | B1,B2,B3 → close B1 SELL1@110 → B2,B3 | −1000 | 11000 | −4000 | −4 | 100000 | 96000 | 7000 |
| S2-3 | B2,B3 → close B3 BUY1@110 → B2 BUY3@120 | −1000 | 10000 | −3000 | −3 | 99000 | 96000 | 7000 |
| S2-4 | B2 BUY3@120 → close2.6@110 → B2 C BUY0.4@120 | −2600 | 7400 | −400 | −0.4 | 96400 | 96000 | 7000 |
| S2-5 | B2 C BUY0.4@120 → validate/promote → B2 FAR BUY0.4@120 | 0 | 7400 | −400 | −0.4 | 96400 | 96000 | 7000 |

Old Far residual0; original Core residual0.4, new Far BUY@120. Funding4600 from5000, free400; F_Final4000 unchanged. TransitionLoss3600; full-basket loss4000; Core-only G0,A1000,B1,M−1001. Числовая симметрия обеспечена явно симметричным synthetic tick value; для реального брокера её предполагать нельзя.

## S3 — неблагоприятное движение вверх против Far SELL и недостаточный резерв

StartingPositions: D1 FAR SELL1@100; D2 C BUY3@120; D3 T BUY1@120; D4 S SELL1@120; StartingBalance100000,StartingEquity98000 при P120.
Цена120→130. Теперь legs=(-3000,+3000,+1000,-1000), U=0, Equity100000, CyclePnL11000. Far усугубилась, хотя basket money выросло.

F_Tr=500,F_Final=4000,PartialFar100; взаимозаменяемость запрещена. При S3-0 план блокируется ДО любых closes: первая Small уже требует1000>500. Следующие строки исключительно projected counterfactual; ФАКТИЧЕСКОЕ StateAfter_BLOCKED = D1,D2,D3,D4 без изменений, ΔR=0, R_all11000,U0,NetLot−2,F_Tr500.

| Projected step | Позиции до → действие → позиции после | ΔR | R_all | U_after | NetLot | Balance | Equity | CyclePnL | Накопленный closing net |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| S3-0 | D1:F SELL1@100,D2:C BUY3@120,D3:T BUY1@120,D4:S SELL1@120; mark130 | 0 | 11000 | 0 | −2 | 100000 | 100000 | 11000 | 0 |
| S3-1 | все4 → close D4 SELL1@130 → D1,D2,D3 | −1000 | 10000 | +1000 | −3 | 99000 | 100000 | 11000 | −1000 |
| S3-2 | D1,D2,D3 → close D1 SELL1@130 → D2,D3 | −3000 | 7000 | +4000 | −4 | 96000 | 100000 | 11000 | −4000 |
| S3-3 | D2,D3 → close D3 BUY1@130 → D2 BUY3@120 | +1000 | 8000 | +3000 | −3 | 97000 | 100000 | 11000 | −3000 |
| S3-4 | D2 BUY3@120 → close2.6@130 → D2 C BUY0.4@120 | +2600 | 10600 | +400 | −0.4 | 99600 | 100000 | 11000 | −400 |
| S3-5 | D2 C BUY0.4@120 → projected promotion → D2 FAR BUY0.4@120 | 0 | 10600 | +400 | −0.4 | 99600 | 100000 | 11000 | −400 |

Проверка NetLot S3-1: после закрытия Small SELL остаётся SELL1 против BUY4, то есть−3. После закрытия old Far остаются BUY4, то есть−4.

FundingPrefixNeed=max(0,−prefixClosingNet)=max(1000,4000,3000,400)=4000. Консервативная сумма negative cash outflows также4000. Даже при будущем offset итоговый убыток400 не отменяет пик4000. Shortfall=4000−500=3500; уже первый action shortfall500. FinalReserve4000 не TransitionBudget и не разрешённый substituting source.
Core-only full projected G=0.8×3000=2400; OldFar A3000; B1 →M−601. Если eligible только планово закрытая Core2.6, её projected gain2600, share→2080, M−921. Кроме разницы membership, обе суммы поступили бы ПОСЛЕ закрытия Far, не funding раннего prefix. Реальный Core income в S3 BLOCKED не возник.

## Проверки трёх сценариев

| Обязательный predicate | S1 | S2 | S3 |
|---|---|---|---|
| lot/tick grids; все volumes≥min | арифметически соблюдены | соблюдены | соблюдены |
| Geometry C3,T1,S1; slope C+T−S−F=2>0 | да в модели | да в модели | да в модели |
| quantity share×Bnet>FarClosed |0.8×3=2.4>1 |2.4>1 |2.4>1 |
| OldFar full close; Core residual physical lineage | условный ledger корректен | условный ledger корректен | условный ledger корректен, но BLOCKED |
| Compression0<N<F и limits |0.4<1,0.6/0.6 |то же |то же |
| Full old Far loss basis |1000 для1lot |1000 для1lot |3000 для1lot |
| Core-only CatchUp strict positive |нет,−1001 |нет,−1001 |нет,−601 full-Core preview |
| Transition cap, synthetic four caps5000 each |3600≤5000 |3600≤5000 |400≤5000, prefix4000 отдельно |
| Conservative prefix funding, без Small credit |4600≤5000 |4600≤5000 |4000>500; REJECT |
| Результат FinalClose D06 A ≥20001 |6000<20001 |6000<20001 |10000<20001 |
| Recovery monotonicity физической future chain |не доказана текущим template; на фиксированной цене R+U не растёт от closes |то же |рост basket при market move сам по себе не все gates |
| RiskNext/RiskOld, broker margin/free margin/drawdown, tail |UNAVAILABLE, synthetic lots не broker risk proof |UNAVAILABLE |UNAVAILABLE |
| Fresh authentic market/cost/source, plan/revision/ownership, durable reservations |только synthetic premises, actual UNAVAILABLE |то же |то же |
| Actual fills/reconcile/exactly one actual residual |NOT_RUN/UNAVAILABLE |NOT_RUN/UNAVAILABLE |NOT_RUN/UNAVAILABLE |
| Общий permission/dispatch |BLOCKED, projection only |BLOCKED, projection only |BLOCKED до S3-1 |

Риск по lots ограниченным не доказан как денежный bound. Эти модели не закрывают ERR038. Равенство экономического результата до/после closes — conservation на фиксированной цене без новых costs, не successful recovery. Устойчивый следующий basket не открывается в реальности.

## Отдельная ветвь: настоящий смысл same-position PartialFar

Не добавляется к S1/S2/S3. Synthetic Far SELL1@100, P110, R_all11000, U−1000, CyclePnL10000, F_Partial=100; FinalReserve4000.
LossPerLot1000 → floor_step(100/1000)=0.10. Close same Far0.10 net−100; same identifier residual0.90@100, U−900, R_all10900, CyclePnL10000. FinalReserve4000 остаётся. ReservedPF100→ConsumedPF100; freePF0. Residual0.9≥0.01. Role FAR сохраняется; новой Far из Core в этом действии нет. Actual matching требует реальных fills, здесь только math.
Partial fill0.04 не разрешил бы назвать action0.10 завершённой; остаётся pending0.06 и actual residual0.96. Денежный partial net−40; PF consumption40, unused reservation60 ещё bound до outcome/reconciliation, не автоматически released.

## Дополнительный witness: max TransitionLoss и min CatchUp на разных физических уровнях

Этот witness — отдельная projected chain на том же инструменте. Он соблюдает position lineage и action order, но НЕ допустимый successful solver path: CatchUp отрицателен, source production fixed-template не моделирует эту цепь.
L1 — S2 closing group: old B1 SELL1@100, Core B2 BUY3@120, T BUY1@120, S SELL1@120, P110. Full old Far−1000; close Core2.6−2600; Trend−1000; Small+1000; T_physical=3600. B2 residual BUY0.4@120 становится единственной новой Far.

L2 conditional expansion: сохранить B2 BUY0.4@120; при P80 открыть E2 Core SELL1.2@80,E3 Trend SELL0.4@80,E4 Small BUY0.4@80. Затем P90. Far B2 net−1200, full Core−1200, Trend−400, Small+400. Close E4 full0.4(+400), B2 full0.4(−1200), E3 full0.4(−400), E2 partial1.04(−1040), оставить E2 SELL0.16@80→новая Far.
L2 closing net=400−1200−400−1040=−2240; residual U−160. Full basket−2400, не−2240. F_before0.4,FarClosed0.4,N0.16,compression0.24; все lots на grid. После projected L1 R_all7400; после L2 R_all5160, U−160, CyclePnL5000. Между уровнями market movement меняет economy; при самих closes conservation соблюдается.
Core-only G1=G2=0 (обе Core отрицательны), B1=B2=1. M1=−1001,M2=−1201.
argmax T_physical=L1 (3600>2240), argmin M=L2 (−1201<−1001). Даже для full-basket T=(4000,2400) экстремум остаётсяL1.
Funding при прежних Transition5000: L1 conservative debit4600 →Free400; L2 negative outflows1200+400+1040=2640>400, continuation BLOCKED. Отдельная достаточная synthetic TransitionGrant8000 могла бы дать Free3400 послеL1 и760 послеL2; это не изменило бы отрицательный CatchUp и не разрешило путь.
Поэтому различие extrema доказано для корректного projected physical path. Положительный feasible/native witness НЕ доказан. Таблицы03G с неизменными направлениями/opens остаются историческими valuation fixtures; этот audit не превращает их в executed promotions.

## Независимая ручная арифметика

S1/S2: −1000−3000−1000+1000=−4000; CoreClosed(3−0.4)×(−10)×100=−2600; Closing−3600+Residual−400=−4000.
R_all7400+U−400=7000; Balance89000+7400=96400; Equity96400−400=96000; Recovery_A=7000−I1000=6000.
S3: −3000+3000+1000−1000=0; Closing−400+Residual400=0; R_all10600+U400=11000; Recovery_A10000.
Prefix S3: −1000,−4000,−3000,−400 →max loss4000, несмотря на terminal loss400.
Ненулевые costs oracle (отдельный component, не изменение трёх fixtures): profit10,commission−1,swap−2,fee−0.5 →DealNet6.5. Повторное вычитание1 комиссии запрещено. Если spread/slippage уже в fill/close price, второй same-window debit запрещён; неизвестное partial membership UNAVAILABLE.
