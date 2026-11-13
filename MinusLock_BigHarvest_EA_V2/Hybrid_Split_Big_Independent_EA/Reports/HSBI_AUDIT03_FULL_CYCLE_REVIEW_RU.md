# AUDIT03 — полный цикл, устойчивость и границы завершения

[Геометрия](HSBI_AUDIT03_GEOMETRY_REVIEW_RU.md), [деньги](HSBI_AUDIT03_MONEY_REVIEW_RU.md), [FSM](HSBI_AUDIT03_FSM_REVIEW_RU.md) задают отдельные proof scopes. Далее — ручная сквозная иллюстрация, **не симулятор и не результат теста**. Она не заменяет доказательство для всех admissible inputs.

## Начальный lock не создаёт прибыль

Предпосылки: один линейный symbol,K=1 money/(lot·price),spread1,нулевые дополнительные комиссии только для прозрачности алгебры. Initial BUY1 поAsk101 и SELL1 поBid100. При следующих Bid110/Ask111: BUY net+9,SELL net-11,сумма-2. Закрыв BUY, мы получаем Balance+9 и remaining FarSELL с floating-11, а не прирост Equity9. Источник F050, `Docs/09:6-20`; ERR-036/042; IMP-020/021.

Реальные commission/swap/fee в эту иллюстрацию не “доказаны равными нулю”; если они есть, добавляются signed и ухудшают/меняют итог. Источник прибыли в будущем зависит от направленного движения после изменения структуры, не от переименования remaining loser в Far.

## Basket и positive Harvest при отрицательном cycle

При Bid110/Ask111 открываются C1.2,T1 BUY по111, SmallSELL.5 по110; FarSELL1 остаётся со входом100. D=1.2+1-.5-1=.7. На Bid112/Ask113:

- Core+1.2,Trend+1,Small-1.5,закрываемые C/T/S дают Harvest+.7.
- Far net=-13.
- Полный EconomicCyclePnL от InitialLock: +9+.7-13=-3.3.
- Strategy RecoveryMetric, если InitialProfit исключён по Docs09: .7-13=-12.3.

Таким образом, положительный Harvest не означает положительный PnL или рост Equity. До Harvest at same quote CloseNow всех positions даёт тот же total при отсутствии новых fees; реализация меняет Balance/Floating, не сумму.

Allocation выполняется **по actual eligible источникам**, а не по forecast. Положительные Core1.2+Trend1 дают источники2.2; отрицательный Small-1.5 остаётся экономическим расходом, не отрицательным grant. Как условный candidate policy можно распределить source total2.2 на FinalReserve1.7 и PartialFar.5. Это не утверждённые shares и не разрешение реального расхода; индивидуальные source manifests всё равно обязательны. Сумма grants2.2 больше netHarvest.7, потому что расход Small не превращён в grant и не спрятан из CyclePnL. ERR-022/033/047; F007/012/018/035/060; IMP-003/004/014/020.

## Partial Far и сохранение цены ликвидации

При текущем loss13 money/lot, PartialBudget.5,lot step.01: raw=.5/13,между.03 и.04. Floor даёт.03,предполагаемый close cost.39<=.5,Far residual.97. Unused.11 возвращается тому же source reservation; не добавляется как новая прибыль. Без fees и изменений цены remaining Far loss12.61,realized full-cycle9+.7-.39=9.31,total9.31-12.61=-3.30. При начальном Balance1000 Balance1009.31,Equity996.70. Рост Balance совместим с падением Equity.

FarLots уменьшились, но экономическая потеря не исчезла; она перенесена из floating в realised. При настоящем slippage/fixed fee цена шага может превысить budget: линейный расчёт не гарантирует executable cost. Никакая цена/остаток здесь не получены от брокера. `Docs/11:5-13`; F040/F053–056; ERR-007/008/022/032; IMP-004/014/013.

FinalReserve1.7 не покрывает remaining loss12.61. Ни фактическая полная экономическая прибыль-3.30, ни strategy metric-12.30 не дают положительный FinalClose threshold. Catch-Up preview требует отдельной подходящей price-state/eligible resource, не сравнения lot slopes в одиночку. Максимум будущего TransitionLoss не определяет минимум будущего Margin (ERR-018/043; IMP-010).

## Small branch и actual residual

При альтернативном наступлении Small trigger требуются repeated fresh snapshot/hold/retrace/debounce и revision guard, а не один touch (`Docs/13:6`). Исходный план сохраняется. Small→OldFar→Trend→Core part закрываются только после complete prior outcomes. При наших объёмах Net может достичь2.2, несмотря на снижение Gross (F052). Модель risk/margin должна проверять каждый prefix и pause after partial, а не только final residual.

Actual residual original Core становится кандидатом NewFar лишь при same ticket/identifier, 0<N<F, exactly-one-position, пересчитанных risk/margin/cost/FutureSmall/Catch-Up gates. SelectedN=.2 при actual.6 — план дальнейшей обработки, не factual promotion .2. Independent expected identity отсутствует в одном лишь `expected=proof.identity`. ERR-013/019/041/045; IMP-001/011/022.

## Gap, ложный trigger и порядок событий

При level step5 и gap100→110 прохождение двух ценовых порогов не доказывает два actual Harvest или два открытых basket. Один persisted event/action, свежий plan/revision и pending barrier должны определить дальнейший маршрут. Нельзя ретроспективно исполнить два цикла по пропущенным ценам. Touch/retrace может отменить Small intent без actual close; altered replay/conflict блокирует новый расход. `Docs/05:19-25`, `Docs/07:6-25`, F045/F057, ERR-016/017/024/030; IMP-008/009/016.

## Signed loss и полный риск

Для batch[-15,+100],cap12: текущий signed-loss15→0,peak15→15,sticky breach true→true. После первого fill действие могло уже нарушить cap; второй положительный fill не отменяет исторического факта. Это сравнение математических альтернатив, а не выбор sticky вместо действующего current-net. Window/reset/restart/ordered membership требуют D-05 approval. Неизвестная history не даёт current-known zero. ERR-035, F024–026, IMP-019.

Снижение Far lot при новом price basis не обязательно снижает money risk. Снятие hedge при закрытии Small/Far может увеличить Net и account margin. Сумма standalone OrderCalcMargin не доказывает account headroom. RiskNext<RiskOld должно сравниваться на одной adverse модели/горизонте. ERR-034/037/041, F031–033/F052, IMP-015/021/022.

## Конечность, остаток и верхняя граница убытка

Условие forall k F(k+1)<=qF(k),0<q<1 даёт F(k)<=q^kF0 индукцией F058. Для достижения <=Vmin достаточное число **успешных** переходов удовлетворяет F037. Утверждение не гарантирует, что очередной safe candidate существует, хватает margin, придёт нужная цена, исполнится close или не возникнет timeout. Минимальный положительный lot остаётся открытым; при F=Vmin классического следующего N в(0,F) на той же сетке нет. Требуется terminal close с actual economic residual zero либо отдельно утверждённая остаточная policy, не фиктивное completed.

Конечное наблюдение F1=.8,F2=.64 при q=.8 не исключает plateauF3=.64. Uniform tail требует invariant admissible set и доказательства каждого будущего перехода, не набора bool flags. Источники Docs04:33-36,Docs27:5; ERR-021/031/032, F037/038/058; IMP-013.

Для незащищённого SELL F>0,K>0 и неограниченной adverse цены любая денежная граница B нарушается выбором P>Popen+B/(FK). Это F059: без дополнительной модели гарантированного exit, диапазона цены, ограниченной ликвидности/slippage/liability безусловный loss bound не следует. Stop-loss trigger не гарантирует fill price при gap. Для BUY с неотрицательной ценой и фиксированным K картина потери иная, но это не снимает short-case и account leverage/cost assumptions. Нельзя объявлять универсальный bounded loss из q-contraction. ERR-038/042; IMP-021.

## Идея, норматив и реальная реализация

HSBI описывает условную перенастройку экспозиции и раздельный учёт источников, а не алгебраическое создание прибыли. Математически корректны локальные signed sums, partition conservation и условная индукция. Недостаточно доказаны admitted market domain, global economic funding, prefix execution risk, uniform tail, terminal closure и final profitability. Нормативные противоречия direction/objective/optional-leg не исчезают от локальных совпадений.

Current main неторговый; полный цикл не запускается. Это надлежащая граница безопасности, а не evidence полной стратегии. Полноценная торговая логика допустима только после отдельных решений владельца, локальных remediation, независимого provider/ledger, нативных acceptance и сквозных execution/restart/risk доказательств. Текущее задание ни один из этих шагов не разрешает.
