# Три главных закона Hybrid Split Big
## Полная математическая модель, денежные инварианты, алгоритмы Solver и требования к реализации в MQL5

**Статус документа:** нормативная спецификация для реализации. Все `PASS` принимаются только по уровню B (реальная денежная модель). Формулы уровня A не дают разрешения на торговлю сами по себе.

## Глава 1. Назначение системы
Hybrid Split Big — recovery-цикл для hedging-счёта. Initial Lock открывает встречные позиции; после закрытия стартовой плюсовой позиции остаётся убыточная позиция `Far`. Её стартовая прибыль **не входит** в бюджет Recovery: цикл начинается в момент назначения Far. Направление Big противоположно Far; SmallBase совпадает с Far. BigCore создаёт базовый наклон восстановления, BigTrend — отдельный закрываемый на переходе источник результата, SmallBase моделирует обратную ветвь.

`FinalReserveReal` — отмеченная часть уже реализированной прибыли только для Final Close Far; он не является новой прибылью и не финансирует Partial Far или Small Transition. Цикл завершён только при отсутствии управляемых позиций и `RecoveryPLCloseNow >= MinimumFinalRecoveryProfit`; иначе допускаются лишь `TERMINAL_SAFE_STATE` либо предварительный `HYBRID_CANDIDATE_REJECTED`.

```text
Initial Lock → initial plus close → Far → BuildHybridCandidate
→ Big/Small → Big Harvest или Small Transition
→ сжатый новый цикл / Final Close / Terminal Safe State
```

## Глава 2. Словарь, типы и размерности
| Символ [категория] | MQL5 имя | Тип / единица | Источник, знак и ошибка |
|---|---|---|---|
| `F` [LOTS] | `FarLot` | double, lots | фактическая позиция Far; `F>0`, иначе REJECT_POSITION |
| `C,T,S,N` [LOTS] | `BigCoreLot`, `BigTrendLot`, `SmallBaseLot`, `NewFarLot` | double, lots | нормализованные объёмы; все `>0`, `0<N<F` |
| `c,t,s,q,β` [RATIO] | `BigCoreRatio`, `BigTrendRatio`, `SmallBaseToFarRatio`, `CompressionRatio`, `FinalReserveShare` | double, ratio | `c=C/F`, `t=T/F`, `s=S/F`, `q=N/F`, `0<β<=1` |
| `P,Popen,Pclose` [PRICE] | prices | double, symbol price | Bid/Ask, направление определяет close price |
| `x,D` [POINTS] | points | double, points | нормированное движение к Big; `x>=0` |
| `V` [MONEY/POINT/LOT] | analytic only | double | только уровень A; не используется для финального PASS |
| `Rreal,Rproj` [MONEY] | `FinalReserveReal`, `FinalReserveProjected` | double, account currency | real — только deals; projected — сценарная оценка |
| `Hnet` [MONEY] | `HarvestNetActual/Projected` | double | net после всех включённых расходов |
| `Deficit` [MONEY] | `CoverageDeficit` | double | `FarCloseCost-FinalReserveReal`; покрыт при `<=0` |
| `RecoveryClose` [MONEY] | `RecoveryPLCloseNow` | double | результат закрытия всех управляемых leg сейчас |
| `TransitionNet` [MONEY] | `TransitionNet` | double | подписанный net Small-перехода |
| `Risk` [MONEY] | `OldRisk`, `NextRisk` | double | worst-case loss до контрольной цены; неотрицателен |
| `Mused,Mfree,Mlevel` [MONEY/MONEY/RATIO] | margin fields | double | только `OrderCalcMargin` и account values |
| `CycleID` [STATE] | `cycleId` | ulong | неизменен внутри цикла; mismatch = ERROR |

Все величины рассчитываются до открытия, перед каждым необратимым действием и после каждого deal. Raw lot никогда не используется после normalisation.

## Глава 3. Направления и симметрия
Нормируем ось `x>=0` в сторону Big. `dC=dT=+1`, `dF=dS=-1`. Для Far BUY: Far/SmallBase BUY, Core/Trend SELL, движение к Big — вниз. Для Far SELL: Far/SmallBase SELL, Core/Trend BUY, движение к Big — вверх. В обоих случаях `x` определён как прибыльное направление Big, поэтому все дальнейшие формулы одинаковы. Реальная модель вместо знака использует BUY-close=Bid, SELL-close=Ask.

## Глава 4. Абсолютный и относительный P/L — уровень A
`PLF(x)=PLF0-FVx`, `PLC(x)=PLC0+CVx`, `PLT(x)=PLT0+TVx`, `PLS(x)=PLS0-SVx` [MONEY]. Поэтому

`PLbasket(x)=PLbasket0+(C+T-S-F)Vx`, где `PLbasket0=PLF0+PLC0+PLT0+PLS0`.

Свободный член — состояние в начале рассматриваемого участка; наклон — изменение при движении. Положительный наклон не означает положительный P/L. При положительном знаменателе `xBE=-PLbasket0/((C+T-S-F)V)`. С расходами вместо `PLbasket` используется реальная функция главы 5.

## Глава 5. Реальная денежная функция MT5 — уровень B
Для каждой leg Solver обязан вызвать эквивалент `OrderCalcProfit(type,_Symbol,lot,open,close,money)`. `close=Bid` для BUY и `close=Ask` для SELL; в Worst Case close дополнительно ухудшается на slippage. Свойства `SYMBOL_POINT`, `SYMBOL_TRADE_TICK_SIZE`, `SYMBOL_TRADE_TICK_VALUE`, `..._PROFIT`, `..._LOSS` используются только для диагностики и сценарной сетки; итоговые деньги берутся из `OrderCalcProfit`, что учитывает symbol и валюту счёта. Ошибка вызова — `ERROR_ORDER_CALC_PROFIT`, действие запрещено.

## Глава 6. Ledger Recovery-цикла
`RealizedCyclePL = Σ(DEAL_PROFIT+DEAL_COMMISSION+DEAL_SWAP+DEAL_FEE)` [MONEY] только для текущих Symbol, Magic, CycleID и разрешённых identifiers. `FloatingManagedPL=Σ projected close net открытых leg`. `ExpectedExitCosts` содержит **только ещё не включённые** комиссии, slippage, spread impact и fee. Следовательно:

`RecoveryPLCloseNow=RealizedCyclePL+FloatingManagedPL-ExpectedExitCosts`.

Одна и та же комиссия может находиться либо в floating/deal net, либо в ExpectedExitCosts, но не в обоих. Final Close разрешён при `RecoveryPLCloseNow>=MinimumFinalRecoveryProfit` и нуле managed positions.

## Глава 7. Final Reserve и запрет двойного учёта
`Rreal` — подмножество `RealizedCyclePL`, а не добавка к нему. Запрещено `RecoveryPL=RealizedPL+Rreal`. Инварианты: `0<=Rreal<=EligibleRealizedProfit`; Reserve не дебетуется Partial Far или Small; каждый reserve event имеет `CycleID+HarvestID+eventKey`, применяется не более одного раза. Нарушение — `ERROR_RESERVE_LEDGER`/`ERROR_DOUBLE_COUNT_DETECTED`, дальнейшие открытия запрещены.

## Глава 8. Projected и Real Reserve
`HeligibleCloseNet=max(HcloseNet,0)` [MONEY]; комиссии и все close costs вычитаются **до** применения доли. `Rproj=Rreal+β*HeligibleCloseNet`. Отрицательный Harvest не уменьшает уже реализированный Rreal. После подтверждённого Harvest: `ReserveAddActual=β*max(HarvestNetActual,0)` и `Rreal,new=Rreal,old+ReserveAddActual`. Из того же net сначала создаются отдельные `PartialFarBudget` и `ReserveAdd`; их сумма с carry и unallocated remainder обязана равняться HarvestNetActual, без повторного кредита.

## Глава 9. Закон 1: Catch-Up Reserve
Уровень A: `dRproj/dx=β(C+T-S)V`, `dLF/dx=FV`; поэтому необходимое лотовое условие `β(C+T-S)>F`, или `KR=β(c+t-s)>1`. Это лишь асимптотический наклон, не гарантия terminal close.

Пусть `LF(x)=LF0+FVx+KF`, `Hnet(x)=H0+(C+T-S)Vx-KH`. При `a=β(C+T-S)-F`:

`xcatch=(LF0+KF-R0-βH0+βKH)/(V*a)`.

Если `a<=0`, конечного догоняния по этой модели нет. Если `a>0` и числитель `>0`, нужен проход `xcatch`; если числитель `<=0`, покрытие уже достигнуто. Реальный PASS: `Rproj(Pn)>=FarCloseCostProjected(Pn)+CoverageSafetyBuffer`, затем после deal — та же проверка с `Rreal` и actual cost.

## Глава 10. Дискретные Harvest-уровни и конечное покрытие
`Rreal(x)=R0+Σ(xk<=x)ΔRk`; `Deficitn=FarCloseCostn-Rreal,n`. `Deficit(n+1)<Deficitn` — только локальное улучшение, не доказательство конечности. До открытия строятся `n=1..MaxHarvestLevels`: real-price P/L C/T/S/F, net Harvest, reserve add, far close cost, deficit, RecoveryClose, worst costs и margin. Открытие разрешено только если существует `n*<=MaxHarvestLevels` с `Deficitn*<=0`, `RecoveryClose,n*>=MinimumFinalRecoveryProfit`, а ранее `Deficitn+1<=Deficitn-MinCoverageGainMoney`. Иначе `REJECT_NO_FINITE_HARVEST_LEVEL`.

## Глава 11. Закон 2: Recovery slope
Уровень A: `dRecovery/dx=(C+T-S-F)V`; необходимо `C+T-S-F>0`, то есть `c+t-s>1`. При `0<β<=1`, закон 1 строго влечёт закон 2: из `β(C+T-S)>F` следует `C+T-S>F/β>=F`. После normalisation проверяется `SlopeLots=C+T-S-F>=MinimumRecoverySlopeLots`, затем сценарно: `Recovery(P+ΔP)-Recovery(P)>=MinimumRecoverySlopeMoney`. Монотонность действует только при неизменном составе и фиксированной модели spread; после любого trade event пересчитываются slope, RecoveryClose, Deficit и Catch-Up.

## Глава 12. Big-сценарий и деньги
1. Получить актуальные Bid/Ask, позиции и Worst Case prices. 2. Пересчитать все gates. 3. Закрыть BigCore, BigTrend, SmallBase только по plan; при ошибке — reconciliation. 4. Собрать deal net: `HarvestNetActual=Σ(profit+commission+swap+fee)`. 5. При положительном net распределить `PartialFarBudget` и `FinalReserveAdd` по заранее сохранённым долям; Reserve не является источником Partial Far. 6. Выполнить partial Far только в пределах PartialFarBudget и сверить actual remaining lot. 7. Пересчитать ledger, Deficit, RecoveryClose и возможность Final Close. При любом deviation выше tolerance — `ERROR_PARTIAL_EXECUTION` или terminal safe state.

## Глава 13. Закон 3: меньший следующий цикл
`N=qF`, обязательно `0<N<F`. `BigGrossNext=Cnext+Tnext`; при постоянных ratio `BigGrossNext=(c+t)qF`, поэтому усиленное условие `q<1/(c+t)` даёт `BigGrossNext<F`. В реальной модели проверяются normalized lots напрямую: `Cnext+Tnext<Fold`. Также `GrossNext<N+Cnext+Tnext+Snext < GrossOld` и `RiskNext<RiskOld`, где риск — money loss до явно заданной control price, а не просто lot.

## Глава 14. Полная математика Small Transition
`CloseC=C-N=(c-q)F`; `CloseCoreShare=1-q/c`. Основная **знаковая** форма:

`TransitionNet(q)=NetF+NetS+NetT+NetCoreClosed(q)+TransitionBudget-OtherTransitionCosts`.

Каждый `Net` — `OrderCalcProfit` плюс только ещё не включённые worst-case expenses. Допустимый предел: `TransitionNet>=-MaximumAllowedTransitionLoss`; при строгом профиле параметр равен нулю. Любой допустимый убыток немедленно входит в `RealizedCyclePL`; он не исчезает и не компенсируется фиктивным Reserve.

## Глава 15. Источник Transition Budget
Допускаются только явно учтённые money: реализованный net текущих Small/OldFar/BigTrend/Core deals, отдельный `TransitionReserve`, либо разрешённая незарезервированная часть `RealizedCyclePL`. `FinalReserveReal` запрещён. Инвариант: `FinalReserveAfterSmall>=FinalReserveBeforeSmall`; при credit допускается только `SmallReserveAdd=SmallReserveShare*max(EligibleSmallNet,0)`.

## Глава 16. Solver q
`qmax=min(1-εq,(1-εB)/(cnext+tnext),qrisk,qmargin,qconfigured)`; `qmin=max(qmoney,qlot,qexecution,qconfiguredMin)`. Непрерывный кандидат существует лишь при `qmin<qmax`. Официальная цель — минимальный broker-valid `N`, но только если `TransitionNet>=TransitionSafetyBuffer-MaximumAllowedTransitionLoss` и пройдены все будущие gates. Реальный Solver перебирает `N=VolumeMin, VolumeMin+Step,...,Fold-Step`, а не raw q; первый PASS сохраняется с полным trace.

## Глава 17. Future Small до открытия
До открытия C/T/S на прогнозной Small-trigger цене выполняется `FutureSmallFeasibilityCheck`: все four close nets, перебор N, `TransitionNet`, Reserve preservation, NextBig, next risk, next margin, законы следующего Big и минимум один следующий Small feasibility check с recursion depth limit. Отсутствие N означает `REJECT_FUTURE_SMALL`; открывать текущую корзину запрещено.

## Глава 18. Нормализация объёмов
`Down(v)=floor(v/step)*step`, `Up(v)=ceil(v/step)*step`, `Nearest(v)=round(v/step)*step`, затем clamp range. NewFar использует `Down`; C/T/S используют политику, выбранную до проверки и записанную в log (рекомендуется Down, чтобы не увеличивать margin). После normalisation заново обязательны: volumes range, `β(C+T-S)>F`, slope, NextBig, risk, finite harvest, Future Small, margin и Worst Case. Raw PASS + normalized fail = `REJECT_ROUNDING`.

## Глава 19. Min lot и terminal state
Если `Nraw<VolumeMin`, `Nnorm<VolumeMin` или `Nnorm>=Fold`, новый Far запрещён. Если `RecoveryPLCloseNow` проходит final threshold — `FINAL_CLOSE`; иначе `TERMINAL_SAFE_STATE`: запрет новых открытий, сохранить tickets/ledger, отменить pending open, попытаться только разрешённые risk-reducing closes, запросить manual intervention. Запрещена цепочка `0.01→0.01`.

## Глава 20. Конечность разворотов
При постоянном q: минимальное число до `Fterminal` — `Nmin=ceil(ln(Fterminal/F0)/ln(q))`. При переменных `0<qn<=qmax<1`: `Fn<=F0*qmax^n`, значит верхняя граница `Nmax=ceil(ln(Fterminal/F0)/ln(qmax))`. Теорема применима лишь при каждом фактически принятом нетерминальном переходе, строгом уменьшении rounded Far и постоянном `qmax<1`; иначе запускается глава 19, а не новый цикл.

## Глава 21. Margin
Точная margin проверка только через `OrderCalcMargin` для каждого planned order и broker hedging model. Рассчитать `ProjectedUsedMargin`, `ProjectedFreeMargin=Equity-Used`, `ProjectedMarginLevel=Equity/Used*100`. PASS требует `UsagePercent<=MaxMarginPercent`, `MarginLevel>=MinimumMarginLevel`, `FreeMargin>0` в Base и Worst Case. Gross lots — только диагностическая оценка.

## Глава 22. Base и Worst Case costs
Base использует current Bid/Ask и expected commission. Worst: `SpreadWorst=CurrentSpread+SpreadBuffer`, close ухудшен на `MaxSlippagePoints`, commission/fee по максимуму, swap=`ProjectedSwapBuffer`. Необратимое действие требует `WORST_CASE_PASS`; невозможность вызвать money model — ERROR, а не optimistic PASS.

## Глава 23. Транзакционный Small порядок
До первого close: получить/сверить Symbol+Magic+CycleID+identifier+lot; re-solve on latest prices; check q, transition, margin, reserve; persist immutable plan. Порядок: SmallBase close → OldFar close → BigTrend close → partial BigCore → verify actual Core → preview next geometry → promote N. После каждого deal собрать actual net, сравнить fill lot, обновить ledger и повторно проверить continuation. Partial fill, reject, excess slippage, missing position, lot mismatch или lost mapping останавливают plan: no new leg; `ERROR_PARTIAL_EXECUTION`/`ERROR_POSITION_MISMATCH`; only reconciliation/terminal-safe actions.

## Глава 24. Коды решений
| Код | Условие | Разрешено / запрещено | Log |
|---|---|---|---|
| `PASS_ALL_LAWS` | все mandatory gates | исполнить следующий этап / не менять plan silently | all metrics |
| `REJECT_BIG_SLOPE`, `REJECT_RESERVE_CATCHUP` | slope/catch-up fail | no open | lots, prices, slopes |
| `REJECT_NO_FINITE_HARVEST_LEVEL` | нет n* | no open | level table, deficits |
| `REJECT_NO_VALID_Q`, `REJECT_FUTURE_SMALL` | q Solver fail | no open | q bounds, nets |
| `REJECT_MARGIN`, `REJECT_ROUNDING`, `REJECT_MIN_LOT_STALL` | margin/lot fail | no open/new Far | broker properties |
| `ERROR_ORDER_CALC_PROFIT/MARGIN` | API failure | no irreversible action | return code, inputs |
| `ERROR_RESERVE_LEDGER`, `ERROR_DOUBLE_COUNT_DETECTED` | ledger invariant fail | terminal safe | event keys, balances |
| `ERROR_PARTIAL_EXECUTION`, `ERROR_POSITION_MISMATCH` | actual differs | reconcile only | tickets, requested/filled |

## Глава 25. Инварианты
Identity: Symbol, Magic, CycleID and identifier must match. Reserve: nonnegative, within eligible realized profit, never double-counted, nondecreasing in Small. Big: normalized monetary Catch-Up and slope PASS. Small: `0<N<F`, `NextBigGross<OldFar`, `RiskNext<RiskOld`, `GrossNext<GrossOld`. Finiteness: each accepted nonterminal transition has `Fn+1<Fn` and bounded q. Execution: context volume equals broker volume within tolerance after every action.

## Глава 26. Полная последовательность Solver
```text
BuildHybridCandidate(context):
  Read symbol properties, account, positions; validate identity.
  Build raw C,T,S; normalize; reject invalid lots.
  Evaluate Base and Worst monetary basket at each point; require slopes.
  For level 1..MaxHarvestLevels: calculate close nets, reserve add,
    Far close cost, deficit, RecoveryClose and margin; find finite n*.
  If no n*: reject finite catch-up.
  FutureSmallSolver(triggerPrice, depth): enumerate normalized N ascending;
    compute all transition close nets; require TransitionNet threshold,
    reserve preservation, NextBig, gross/risk reduction, next laws,
    next margin, and recursively bounded future-small feasibility.
  If no N: reject future small.
  Require all Base and Worst gates; return immutable plan and PASS codes.
ExecuteSmallPlan(plan): revalidate; close legs in prescribed order;
  after each deal reconcile actual money/lot/context; abort safely on mismatch.
```
Inputs are actual broker snapshot plus config; outputs are `PASS plan` or one reject/error with full trace. No function has an implicit money source.

## Глава 27. Четыре тест-вектора
| Вектор | Вход | Ожидание |
|---|---|---|
| V1 valid | F=1,C=2,T=.8,S=.2,β=.9,N=.3; step=.01; V=1 | KR=2.34, slope=1.6, NextBig=.84; только если monetary/margin tables PASS |
| V2 money reject | та же geometry, но Core close net=-500, прочие transition nets=+100, limit=0 | q geometry PASS, `REJECT_TRANSITION_BUDGET` |
| V3 rounding reject | F=.03, step=.01, raw N=.011, raw Cnext+Tnext=.029 | normalize all; если strict NextBig/risk fails, `REJECT_ROUNDING` |
| V4 min lot | F=.01,q=.3,step=min=.01 | Nraw=.003; no NewFar, Final Close or TERMINAL_SAFE_STATE |

В production examples обязательно подставляются actual prices, `OrderCalcProfit` results, commission, swap, slippage and `OrderCalcMargin`; аналитический V=1 не является trade approval.

## Глава 28. Математические свойства для тестов
1. `β(C+T-S)>F` and `0<β<=1` implies positive ideal Recovery slope. 2. `0<q<1/(c+t)` implies `(c+t)qF<F`. 3. Every property repeats after rounding. 4. Reserve is not added to Recovery twice. 5. Small cannot debit FinalReserve. 6. Accepted nonterminal transition strictly reduces F. 7. bounded q proves finite count. 8. no finite harvest rejects pre-open. 9. no Future Small q rejects pre-open. 10. partial execution cannot complete plan before reconciliation.

## Глава 29. Журналирование
Each decision logs: Symbol, Magic, CycleID, State, Far ticket/lot/direction/open/current PL, raw and normalized C/T/S, Rreal/Rproj, RecoveryClose, CatchUpRatio, lot/money slope, level/Deficit, selected N/q, NextBigGross, old/next risk, Base/Worst TransitionNet, projected margin, decision and reason. Logs include price assumptions, costs, event keys, requested/filled lots and API errors.

## Глава 30. Критерии готовности и инженерный вывод
Мануал готов только при полном словаре, units, absolute/relative P/L separation, real/projected reserve separation, no double count, finite harvest table, pre-open Future Small, discrete q Solver, rounding reruns, terminal procedure, q theorem, OrderCalcProfit/Margin, Base/Worst costs, transaction rules, tests and codes.

**Строгий вывод.** Три закона совместимы; лотовые неравенства необходимы, но недостаточны. Разрешение равно только:

```text
GEOMETRY_PASS + MONEY_PASS + FUTURE_SMALL_PASS + FINITE_CATCHUP_PASS
+ ROUNDING_PASS + RISK_PASS + MARGIN_PASS + WORST_CASE_PASS
= HYBRID_CANDIDATE_ALLOWED
```

Отсутствие любого PASS означает `HYBRID_CANDIDATE_REJECTED`. После каждого irreversible action используются только actual deal results и reconciliation.
