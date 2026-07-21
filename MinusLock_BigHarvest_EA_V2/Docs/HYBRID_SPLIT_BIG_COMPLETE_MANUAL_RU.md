# Полный мануал Hybrid Split Big

## Область и назначение

Hybrid Split Big разруливает Far после Initial Lock. Initial Profit исключён;
Far является единственным хвостом. BigCore и BigTrend направлены против Far,
SmallBase — вместе с ним. Документ подтверждает математическую модель,
архитектуру исходного кода и Python-валидацию; работа терминала MT5 не входит
в данный этап.

## Термины и параметры

`C=BigCore`, `T=BigTrend`, `S=SmallBase`, `F=Far`, `N=ActualNewFar`.
`BigGross=C+T`; `NetRecoveryExposure=C+T-S-F`;
`NextDirectional=Cnext+Tnext-Snext-N`. Inputs: `BigCoreRatio`,
`BigTrendRatio`, `SmallBaseToFarRatio`, `ReserveShare`,
`TargetNewFarRatio`, `MaximumNewBigToOldFarRatio`,
`MinimumReserveCatchUpRatio`, `MinimumRecoverySlopeMoneyPerPoint`,
`MaximumTransitionLossMoney`, `MinimumReserveAfterTransition`.

## Big

Lots are rounded down to broker step. Before opening, the EA requires positive
net recovery exposure, `ReserveShare*(C+T-S)/F >= MinimumReserveCatchUpRatio`,
margin gate, and point-by-point projected broker-net RecoveryPL growth. The
trace includes F/C/T/S, Bid/Ask close price, commission, spread, swap, fee and
slippage. At Big harvest actual lifecycle net is split once between Final
Reserve and Partial Far budget; the same money cannot be credited twice.

## Small

Before OldFar close `HybridReversePlan` stores identities, projected leg money,
target and next geometry. It scans broker-rounded candidates from minimum lot
upward and chooses the **minimum safe** N. The order is SmallBase close →
OldFar close → BigTrend close → staged BigCore close. Actual remaining Core is
verified, previewed again, and only then promoted to the single NewFar.
BigTrend and Legacy ReverseSmall never become NewFar.

## Three laws

Law 1: projected coverage slope is `ReserveShare*(C+T-S)` and must exceed F.
Law 2: full slope is `C+T-S-F`; monetary close result is checked every point.
Law 3: `0<N<F`, NewFar risk decreases, `NextBigGross=Cnext+Tnext<F` when the
gate is enabled, and `N<=qMaxF` gives finite reverse bound. Invalid geometry,
expense or rounding conditions are rejected before an irreversible action.

## Profiles

| Profile | C | T | S | Reserve | Target cap | Purpose |
|---|---:|---:|---:|---:|---:|---|
| SAFE | 1.80 | .75 | .16 | .92 | .35 | lower gross/margin |
| BALANCED | 2.00 | .80 | .20 | .90 | .30 | selected proof candidate |
| STRONG_COMPRESSION | 2.36 | .99 | .20 | .93 | .20 | highest compression/margin |

The system is complex and sensitive to cost, lot step and TransitionNet; a
missing safe candidate is an intended no-trade/manual-safe outcome, not a
reason to weaken a law.

## Initial Lock и граница цикла

Initial Lock открывает встречные BUY и SELL. После срабатывания Trigger
плюсовая позиция закрывается и её `Initial Profit` не входит ни в RecoveryPL,
ни в Reserve, ни в Transition Budget. Оставшаяся убыточная позиция получает
роль `Far`; одновременно фиксируется `CycleStartBalance`. Таким образом,
Recovery измеряет только восстановление данного Far-цикла, а не смешивает его
с уже зафиксированной первоначальной прибылью.

## Полная геометрия и округление

До торгового действия вычисляются raw-объёмы `C=cF`, `T=tF`, `S=sF` и
`TargetNewFar=rF`. Каждый объём округляется вниз к `LotStep`, затем
проверяется против `MinLot`, максимального объёма, маржи и всех трёх законов.
`BigGross=C+T`; `DirectionalExposure=C+T-S`; полная текущая экспозиция
Recovery равна `C+T-S-F`. Для следующего цикла отдельно считаются
`NextBigGross=NextBigCore+NextBigTrend`,
`NextDirectionalExposure=NextBigCore+NextBigTrend-NextSmallBase` и
`NextNetRecoveryExposure=NextDirectionalExposure-NewFar`. SmallBase не
включается в `NextBigGross`.

| Параметр | Единица | Назначение и риск малого/большого значения |
|---|---|---|
| `BigCoreRatio` | лоты/Far | создаёт основной наклон; малый нарушает Recovery, большой увеличивает маржу |
| `BigTrendRatio` | лоты/Far | усиливает Harvest; ноль лишает план переходной прибыли |
| `SmallBaseToFarRatio` | лоты/Far | встречная часть; большой уменьшает наклон, малый меняет профиль Small |
| `ReserveShare` | доля 0..1 | доля Harvest в Final Reserve; малая не догоняет Far, чрезмерная уменьшает Partial Far |
| `TargetNewFarRatio` | доля Far | верхняя граница остатка; большая не сжимает цикл, малая может не пройти TransitionNet |
| `LotStep`, `MinLot` | лоты | после округления повторяются все gates; грубый шаг может безопасно отклонить план |
| spread/commission/slippage/swap | деньги/пункты | входят в цену закрытия и в консервативные расходы |

## Закон №1: Reserve и последовательные Harvest

Projected-часть закона проверяет отношение
`ReserveCatchUpRatio=ReserveShare*(C+T-S)/F`. Оно обязано быть больше единицы
и не меньше `MinimumReserveCatchUpRatio`; денежная проверка использует цену,
spread, комиссию, проскальзывание и swap. Одного наклона недостаточно: модель
`HYBRID_BIG_LEVEL_SEQUENCE.csv` рекурсивно передаёт остаток Far, Reserve и
PartialFarCarry от L1 к L7. На каждом уровне отдельно выполняются операции
`ReserveAdded`, `PartialFarBudget`, округлённое `PartialFarCloseLot`,
`PartialFarCarry` и новый `CoverageDeficit`. Пока дефицит положителен, он
строго уменьшается; после достижения нуля допустимо только сохранить ноль.

Денежный ledger Big не получает остаток алгебраически. Сначала отдельно
вычисляются `BigCoreCloseNet`, `BigTrendCloseNet`, `SmallBaseCloseNet` и
`HarvestExecutionCosts`; затем независимые операции кредитуют Reserve и
оплачивают фактический Partial Far. Проверяемое равенство:
`ActualHarvestNet=ReserveCredit+PartialFarBudgetUsed+PartialFarCarryAfter+
UnallocatedRemainder`. Одни и те же деньги не могут одновременно стать
Reserve и бюджетом Partial Far.

## Закон №2: RecoveryPL

В каждой точке движения к Big `RecoveryPL` содержит реализованный результат
цикла, плавающий net всех открытых leg, ожидаемые расходы закрытия и только
разрешённые уже зафиксированные эффекты Reserve/Partial Far. `Initial Profit`
исключён. Для FAR_BUY и FAR_SELL создаётся самостоятельный trace от point 0
до `BigTarget+max(500,FarDistance)`: `FarNet`, `BigCoreNet`, `BigTrendNet`,
`SmallBaseNet`, `BasketNet`, предыдущее значение и дельта. Проверяется
`RecoveryPL[n+1] >= RecoveryPL[n]+MinimumRequiredDelta-tolerance`.

Закрытия на Harvest — дискретные события, а не часть производной: их net и
execution cost записываются отдельными ledger-строками. В исходном коде
`ValidateHybridRecoveryMonotonicity` вызывается как pre-open preview:
неудачная геометрия не должна быть принята до необратимого закрытия. После
округления preview повторяется для тех же прогнозных open prices.

## Закон №3 и полный Small

Solver перебирает все broker-rounded `NewFar` от минимального лота до target
и выбирает первый прошедший кандидат: это `MinimumSafeNewFar`, а не просто
первый удобный target. `RequiredBigCoreClose=BigCoreBefore-TargetNewFar`.
Python state machine реально проходит `PLAN_CREATED`, `PLAN_VALIDATED`,
`SMALLBASE_CLOSED`, `OLDFAR_CLOSED`, `BIGTREND_CLOSED`,
`BIGCORE_COMPRESSED`, `ACTUAL_REMAIN_VERIFIED`,
`NEXT_GEOMETRY_PREVIEWED`, `NEWFAR_PROMOTED`, `FINAL_GATE_CHECKED` и
`NEXT_CYCLE_CREATED`. Каждая операция удаляет соответствующую старую позицию
из состояния; завершение запрещено при OldFar, OldBigTrend, OldSmallBase,
двух NewFar или неучтённом Core.

Следующий риск не сводится к NewFar: отчёт хранит `NextFarRiskMoney`, gross
четырёх leg, directional/net exposure, worst-case floating loss,
`NextTransitionRisk`, `NextRequiredMargin` и итоговый score. Проверяются
`NewFarRisk<OldFarRisk`, `NextCycleGross<OldCycleGross` и
`NextCycleRisk<OldCycleRisk`; маржа ограничена отдельным лимитом. При
`q=NewFar/OldFar` и `0<=q<1` округлённая цепочка F0,F1,... заканчивается на
`MinLot` либо финальным закрытием.

## Числовая шкала и профили

Для Far 0.01, 0.10, 1.00, 2.00 и 5.00 proof создаёт одинаковую формулу с
broker-округлением. Например у BALANCED для F=1: C=2.00, T=0.80, S=0.20,
BigGross=2.80, NetExposure=1.60, projected CatchUp=2.34, TargetNewFar=0.30,
NextBigGross=0.84. Для F=0.01 результат определяется MinLot: если
округление уничтожает безопасную геометрию, это корректный SAFE_REJECTED, а
не искусственный PASS. SAFE уменьшает gross и margin; BALANCED — базовый
доказательный профиль; STRONG_COMPRESSION сильнее уменьшает NewFar, но
требует большего gross, TransitionNet и запаса по расходам.

## Ограничения и улучшения

Сильные стороны системы — pre-open gate, point-by-point Recovery, раздельные
денежные корзины, рекурсивный Reserve и запрет невалидного перехода. Слабые
стороны — высокий gross, маржа, число операций, чувствительность к затратам,
LotStep и невозможность безопасного плана в плохих условиях. Обязательные
улучшения: сохранять ledger каждой сделки и повторять gates после каждого
округления. Желательные: расширять stress-профили брокера. Экспериментальные:
изменять коэффициенты только вместе с новым proof. Доказано в рамках
математики, исходного кода и Python-модели; работа терминала MT5 в этот этап
не входит.
