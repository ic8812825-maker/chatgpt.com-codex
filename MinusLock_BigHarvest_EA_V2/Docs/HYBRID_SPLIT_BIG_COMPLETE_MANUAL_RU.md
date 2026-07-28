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

<!-- STAGE_3_1_3_SECTION_START -->
## Единый нормативный словарь, размерности, денежные знаки и источники данных

**Этап:** 3.1.3. **Граница:** терминологический/type contract; он не меняет формулы, коэффициенты, state transitions или runtime. Полный расширенный record каждого термина находится в `HYBRID_SPLIT_BIG_GLOSSARY_AND_DIMENSIONS_RU.md`; таблица ниже встроена полностью и обязана быть byte-equivalent таблице приложения. При расхождении validation FAIL. Приложение не является конкурирующим source of truth.

### Типовая система и lifecycle типов

| Family | Types | Meaning/source | Allowed | Forbidden | Created / stale / replacement |
|---|---|---|---|---|---|
| Volume | LOT_RAW, LOT_CALCULATED, LOT_NORMALIZED, LOT_REQUESTED, LOT_FILLED, LOT_POSITION_ACTUAL, LOT_RESIDUAL | formula → symbol constraints → request → deal → position | операции только с lot | MONEY/PRICE comparison | stale после execution; replacement — deal/position snapshot |
| Price | PRICE_BID, PRICE_ASK, PRICE_OPEN, PRICE_TRIGGER, PRICE_TARGET, PRICE_CONTROL, PRICE_PROJECTED, PRICE_EXECUTED | SymbolInfo/position/deal | price arithmetic and PriceTolerance | money/point tolerance | market price stale при move; actual deal price immutable |
| Distance | POINTS, PRICE_DELTA, TICKS | SYMBOL_POINT/TICK_SIZE | explicit conversion with Symbol | implicit Point=TickSize | stale with symbol change |
| Money | MONEY_PROJECTED, MONEY_REALIZED, MONEY_FLOATING, MONEY_RESERVED, MONEY_AVAILABLE, MONEY_CONSUMED, MONEY_RESIDUAL, MONEY_COST | OrderCalcProfit or confirmed deals/ledger | money-only sums with provenance | direct LOT conversion | projected replaced only by confirmed evidence |
| Dimensionless | RATIO, SHARE, PERCENT, MULTIPLIER | typed formula/profile | ratio/share operations | reinterpret numeric literal | policy revision invalidates |
| Identity | SYMBOL_ID, MAGIC_ID, CYCLE_ID, POSITION_ID, POSITION_TICKET, ORDER_TICKET, DEAL_TICKET, ROLE_ID, EVENT_ID, FINGERPRINT | terminal and reconciled namespace | exact identity comparison | Comment as identity | replacement only by reconciliation/new lifecycle |
| State | STATE, PHASE, OUTCOME, REASON_CODE, GATE_RESULT | FSM/gate contract | typed transitions | diagnostic text as enum | revision/state transition |
| Boolean | BOOLEAN_POLICY, BOOLEAN_OBSERVATION, BOOLEAN_RESULT | config/observation/gate | boolean logic | numeric money/lot use | new observation/policy revision |

### Детальный каталог нормативных типов

| Type | Смысл | Authoritative source | Допустимые операции | Запрещённые операции | Появление / stale / replacement |
|---|---|---|---|---|---|
| `BOOLEAN_RESULT` | typed structured value | named lifecycle authority | only operations declared by its family | implicit numeric/type conversion | new observation/reconciliation replaces |
| `CYCLE_ID` | identity/proof value | MT5 properties or reconciled namespace | exact identity match/hash validation | comment/numeric tolerance substitution | new lifecycle/revision replaces |
| `DEAL_TICKET` | identity/proof value | MT5 properties or reconciled namespace | exact identity match/hash validation | comment/numeric tolerance substitution | new lifecycle/revision replaces |
| `EVENT_ID` | identity/proof value | MT5 properties or reconciled namespace | exact identity match/hash validation | comment/numeric tolerance substitution | new lifecycle/revision replaces |
| `FINGERPRINT` | identity/proof value | MT5 properties or reconciled namespace | exact identity match/hash validation | comment/numeric tolerance substitution | new lifecycle/revision replaces |
| `GATE_RESULT` | typed lifecycle value | FSM/gate contract | typed transition/comparison | diagnostic text substitution | new transition/result replaces |
| `LOT_CALCULATED` | trade volume | formula/symbol constraints/request/deal/position | lot arithmetic and typed lot comparison | money/price substitution | created by named lifecycle stage; stale after execution; replaced by deal/position evidence |
| `LOT_FILLED` | trade volume | formula/symbol constraints/request/deal/position | lot arithmetic and typed lot comparison | money/price substitution | created by named lifecycle stage; stale after execution; replaced by deal/position evidence |
| `LOT_NORMALIZED` | trade volume | formula/symbol constraints/request/deal/position | lot arithmetic and typed lot comparison | money/price substitution | created by named lifecycle stage; stale after execution; replaced by deal/position evidence |
| `LOT_POSITION_ACTUAL` | trade volume | formula/symbol constraints/request/deal/position | lot arithmetic and typed lot comparison | money/price substitution | created by named lifecycle stage; stale after execution; replaced by deal/position evidence |
| `LOT_RAW` | trade volume | formula/symbol constraints/request/deal/position | lot arithmetic and typed lot comparison | money/price substitution | created by named lifecycle stage; stale after execution; replaced by deal/position evidence |
| `LOT_REQUESTED` | trade volume | formula/symbol constraints/request/deal/position | lot arithmetic and typed lot comparison | money/price substitution | created by named lifecycle stage; stale after execution; replaced by deal/position evidence |
| `LOT_RESIDUAL` | trade volume | formula/symbol constraints/request/deal/position | lot arithmetic and typed lot comparison | money/price substitution | created by named lifecycle stage; stale after execution; replaced by deal/position evidence |
| `MAGIC_ID` | identity/proof value | MT5 properties or reconciled namespace | exact identity match/hash validation | comment/numeric tolerance substitution | new lifecycle/revision replaces |
| `MONEY_AVAILABLE` | account-currency money | OrderCalcProfit for projected; confirmed deals/ledger for actual | money sums with explicit sign/provenance | lot/price comparison or projected ledger commit | stale on market/execution; actual replaces only through confirmation |
| `MONEY_CONSUMED` | account-currency money | OrderCalcProfit for projected; confirmed deals/ledger for actual | money sums with explicit sign/provenance | lot/price comparison or projected ledger commit | stale on market/execution; actual replaces only through confirmation |
| `MONEY_COST` | account-currency money | OrderCalcProfit for projected; confirmed deals/ledger for actual | money sums with explicit sign/provenance | lot/price comparison or projected ledger commit | stale on market/execution; actual replaces only through confirmation |
| `MONEY_FLOATING` | account-currency money | OrderCalcProfit for projected; confirmed deals/ledger for actual | money sums with explicit sign/provenance | lot/price comparison or projected ledger commit | stale on market/execution; actual replaces only through confirmation |
| `MONEY_PROJECTED` | account-currency money | OrderCalcProfit for projected; confirmed deals/ledger for actual | money sums with explicit sign/provenance | lot/price comparison or projected ledger commit | stale on market/execution; actual replaces only through confirmation |
| `MONEY_REALIZED` | account-currency money | OrderCalcProfit for projected; confirmed deals/ledger for actual | money sums with explicit sign/provenance | lot/price comparison or projected ledger commit | stale on market/execution; actual replaces only through confirmation |
| `MONEY_RESERVED` | account-currency money | OrderCalcProfit for projected; confirmed deals/ledger for actual | money sums with explicit sign/provenance | lot/price comparison or projected ledger commit | stale on market/execution; actual replaces only through confirmation |
| `MONEY_RESIDUAL` | account-currency money | OrderCalcProfit for projected; confirmed deals/ledger for actual | money sums with explicit sign/provenance | lot/price comparison or projected ledger commit | stale on market/execution; actual replaces only through confirmation |
| `MULTIPLIER` | dimensionless typed coefficient | approved profile or typed formula | dimensionless operations | reinterpretation as money/lot/points | policy revision invalidates |
| `ORDER_TICKET` | identity/proof value | MT5 properties or reconciled namespace | exact identity match/hash validation | comment/numeric tolerance substitution | new lifecycle/revision replaces |
| `OUTCOME` | typed lifecycle value | FSM/gate contract | typed transition/comparison | diagnostic text substitution | new transition/result replaces |
| `PERCENT` | dimensionless typed coefficient | approved profile or typed formula | dimensionless operations | reinterpretation as money/lot/points | policy revision invalidates |
| `PHASE` | typed lifecycle value | FSM/gate contract | typed transition/comparison | diagnostic text substitution | new transition/result replaces |
| `POINTS` | symbol distance | SYMBOL_POINT or SYMBOL_TRADE_TICK_SIZE | distance operations and explicit price conversion | implicit points=ticks or points→money | symbol/property revision invalidates |
| `POSITION_ID` | identity/proof value | MT5 properties or reconciled namespace | exact identity match/hash validation | comment/numeric tolerance substitution | new lifecycle/revision replaces |
| `POSITION_TICKET` | identity/proof value | MT5 properties or reconciled namespace | exact identity match/hash validation | comment/numeric tolerance substitution | new lifecycle/revision replaces |
| `PRICE_ASK` | symbol price | SymbolInfo/position/deal | price delta and price comparison | money/lot tolerance | market value stale on tick; executed deal price immutable |
| `PRICE_BID` | symbol price | SymbolInfo/position/deal | price delta and price comparison | money/lot tolerance | market value stale on tick; executed deal price immutable |
| `PRICE_DELTA` | symbol price | SymbolInfo/position/deal | price delta and price comparison | money/lot tolerance | market value stale on tick; executed deal price immutable |
| `PRICE_EXECUTED` | symbol price | SymbolInfo/position/deal | price delta and price comparison | money/lot tolerance | market value stale on tick; executed deal price immutable |
| `PRICE_OPEN` | symbol price | SymbolInfo/position/deal | price delta and price comparison | money/lot tolerance | market value stale on tick; executed deal price immutable |
| `PRICE_PROJECTED` | symbol price | SymbolInfo/position/deal | price delta and price comparison | money/lot tolerance | market value stale on tick; executed deal price immutable |
| `RATIO` | dimensionless typed coefficient | approved profile or typed formula | dimensionless operations | reinterpretation as money/lot/points | policy revision invalidates |
| `REASON_CODE` | typed lifecycle value | FSM/gate contract | typed transition/comparison | diagnostic text substitution | new transition/result replaces |
| `ROLE_ID` | identity/proof value | MT5 properties or reconciled namespace | exact identity match/hash validation | comment/numeric tolerance substitution | new lifecycle/revision replaces |
| `SHARE` | dimensionless typed coefficient | approved profile or typed formula | dimensionless operations | reinterpretation as money/lot/points | policy revision invalidates |
| `STATE` | typed lifecycle value | FSM/gate contract | typed transition/comparison | diagnostic text substitution | new transition/result replaces |
| `SYMBOL_ID` | identity/proof value | MT5 properties or reconciled namespace | exact identity match/hash validation | comment/numeric tolerance substitution | new lifecycle/revision replaces |
| `TICKS` | symbol distance | SYMBOL_POINT or SYMBOL_TRADE_TICK_SIZE | distance operations and explicit price conversion | implicit points=ticks or points→money | symbol/property revision invalidates |

### Архитектурные qualifiers и ambiguous-name ban

`Big`, `Small`, `Far`, `Reserve`, `Profit`, `RecoveryPL`, `Risk`, `Volume`, `Price`, `Close`, `State` без qualifier запрещены в новом нормативном тексте, если local definition не определяет canonical entity. Legacy, Split и Hybrid — разные architecture/mode scopes. Mapping не доказывает математическое соответствие кода.

| Far | SameAsFar | OppositeFar |
|---|---|---|
| BUY | BUY | SELL |
| SELL | SELL | BUY |

BUY/SELL — absolute direction; SameAsFar/OppositeFar — relative direction. BUY close preview uses Bid, SELL uses Ask. Actual deal price authoritative после execution и может отличаться из-за spread, slippage, fill mode и market movement.

### Lot lifecycle

`Raw → Calculated → Normalized → Requested → Filled → Actual Position`. Requested не равно Filled без broker result; ProjectedResidual не равно ActualResidual без reconciliation; actual position volume не нормализуется повторно.

### Projected/actual lifecycle

| Stage | Allowed class |
|---|---|
| Formula preview / pre-open gate | PROJECTED |
| Order request | REQUESTED |
| Broker response | EXECUTED / PARTIAL / REJECTED |
| Deal history / ledger commit | ACTUAL CONFIRMED |
| Position snapshot | ACTUAL CURRENT |
| Restart recovery | RECONCILED ACTUAL |

PROJECTED не превращается в ACTUAL присваиванием: нужны trade result, deal history, position snapshot и reconciliation.

### Money sign contract

Profit and signed favorable P/L >0; signed loss/cost <0; available/consumed/residual bucket and positive requirement >=0. `FarLossSigned=-1200 money`, `FarLossMagnitude=1200 money`, `FinalCloseRequirement=1200 money` — разные entities. `abs` допускается только при явном переходе Signed→Magnitude и новом canonical name.

### Source-of-truth priority

`actual terminal/deal state > reconciled persisted expected state > projected immutable plan`. Persisted cache не превосходит live reconciliation. Projected money: `OrderCalcProfit` + explicit projected costs. Actual realized: confirmed deal history filtered by Symbol+Magic+CycleID+position/deal+role/event. Actual volume/open price: current position properties or confirmed reconstruction after partial execution.

### Identity contract

PositionTicket != PositionIdentifier; OrderTicket != DealTicket != PositionTicket; Comment не identity; Magic без Symbol недостаточен; Symbol+Magic без CycleID недостаточен для concurrent cycles; EventID != trade ticket; Fingerprint не position. Scope hierarchy: `Position ⊂ Role ⊂ Cycle ⊂ Managed Account ⊆ Full Account`; Cycle PASS не означает Account PASS.

### State namespace

State, Phase, Event, Observation, GateResult, ExecutionResult, Outcome, ReasonCode, ErrorCode и DiagnosticText — разные types. `STATE_FINAL_CLOSE_PENDING` is STATE; `FINAL_CLOSE_PREVIEW` is PHASE; PASS is GATE_RESULT; PARTIAL_EXECUTION is OUTCOME; ERROR_PARTIAL_EXECUTION is REASON_CODE; free text is DiagnosticText.

### Null/sentinel contract

ZERO is a calculated numeric zero; NOT_APPLICABLE means contract branch excluded; NOT_CALCULATED means evaluator not run; NOT_AVAILABLE means source unavailable; INVALID means validation failed; STALE means revision/fingerprint invalidated; UNKNOWN means observation cannot be classified. Zero is never a universal missing marker. Ticket 0 is permitted only as type-specific absence sentinel.

### Rounding namespaces

| Entity | Raw type | Normalization | Rounding mode | Broker constraints | Zero policy | Profile |
|---|---|---|---|---|---|---|
| LegacyBig | LOT_RAW | volume step | ROUND_NEAREST | min/max/step | zero rejects open | Legacy DOCUMENTED_NOT_APPROVED |
| LegacySmall | LOT_RAW | volume step | ROUND_NEAREST | min/max/step | zero rejects open | Legacy DOCUMENTED_NOT_APPROVED |
| BigCore | LOT_RAW | volume step | ROUND_DOWN | min/max/step | zero rejects candidate | Hybrid DOCUMENTED_NOT_APPROVED |
| BigTrend | LOT_RAW | volume step | ROUND_DOWN | min/max/step | zero rejects candidate | Hybrid DOCUMENTED_NOT_APPROVED |
| SmallBase | LOT_RAW | volume step | ROUND_UP | min/max/step | zero rejects candidate | Hybrid DOCUMENTED_NOT_APPROVED |
| NewFar | LOT_RAW | volume step | ROUND_DOWN | min/max/step | zero routes terminal/final precheck | Hybrid MODE-DEPENDENT |
| Money ledger | MONEY_REALIZED | money digits at commit/display | ROUND_TO_MONEY_DIGITS | account currency | zero valid | All |
| Price | PRICE_PROJECTED | trade tick | ROUND_TO_PRICE_TICK | tick size | zero invalid | Symbol |
| Actual volume | LOT_POSITION_ACTUAL | none | NO_ADDITIONAL_ROUNDING | already broker state | zero means absent within lot tolerance | All |

DOCUMENTED does not select production profile. Point=SYMBOL_POINT; TickSize=SYMBOL_TRADE_TICK_SIZE; equality is not assumed.

### Tolerance matrix

| Tolerance | Type | Absolute/relative | Applied to | Forbidden for | Decision impact |
|---|---|---|---|---|---|
| MoneyTolerance | MONEY | absolute account money | MONEY_TOLERANCE | account money | >= 0 |
| VolumeToleranceLots | LOT | absolute lot | LOT_TOLERANCE | lot | >= 0 |
| PriceTolerance | PRICE | absolute symbol price | PRICE_TOLERANCE | price | >= 0 |
| PointTolerance | POINTS | absolute points | POINT_TOLERANCE | point | >= 0 |
| RatioTolerance | RATIO | absolute ratio | RATIO_TOLERANCE | dimensionless ratio | >= 0 |
| ComparisonEpsilon | typed | type-bound only | COMPARISON_EPSILON | dimensionless epsilon | >= 0 |
| ReserveMismatchTolerance | MONEY | absolute | MONEY_TOLERANCE | account money | >= 0 |
| GeometryTolerance | LOT | symbol-aware | LOT_TOLERANCE | lot | >= 0 |
| FingerprintTolerance | FINGERPRINT | exact semantic | IDENTITY_MATCH_POLICY | dimensionless policy | >= 0 |

### Source-of-truth matrix

| Data | Preview source | Requested source | Actual source | Persisted source | Restart authority |
|---|---|---|---|---|---|
| Far/BigCore/BigTrend/SmallBase volume | normalized CandidatePlan | request volume | current MT5 position + deals | expected state | reconciled MT5 position |
| opening price | planned entry | request | position properties / deal reconstruction | expected open price | live/rebuilt actual |
| close price | Bid/Ask/projected control | request price/deviation | confirmed deal price | diagnostic only | deal history |
| realized P/L, commission, swap, fee | projected estimate only | n/a | confirmed filtered deals | exactly-once ledger | deals + reconciliation |
| floating P/L | broker-aware preview | n/a | POSITION_PROFIT for display and broker-aware recalculation for proof, separately named | snapshot cache | fresh position + market |
| Reserve / PartialFarBudget | projected allocation | n/a | confirmed allocation event | ledger | reconciled exactly-once ledger |
| CycleID / role identity / state | frozen snapshot | request tags | reconciled positions/events/FSM | persisted state | terminal/deal truth then reconcile |
| snapshot revision | current frozen revision | plan revision | new post-execution revision | persisted revision | rebuilt revision/fingerprint |
| execution result / residual | expected result | requested volume | broker result + deals + position | pending record | actual terminal state |
| Final Close success | preview gate only | close requests | positions=0 + confirmed deals + actual threshold | pending state | reconciliation |

### Sign matrix

| Term | Positive meaning | Zero meaning | Negative meaning | Stored form |
|---|---|---|---|---|
| PositionPL / RealizedCyclePL / FloatingManagedPL / RecoveryPL / TransitionNet / HarvestNet | profit/favorable | break-even | loss | signed MONEY |
| FarLossSigned | impossible favorable under name; rename P/L | no loss | loss | signed MONEY |
| FarLossMagnitude / FinalCloseRequirement | positive obligation | none | invalid | non-negative MONEY |
| ReserveAvailable / PartialFarBudget | available bucket | empty | invalid | non-negative MONEY |
| Costs | refund only if broker-proven | none | cost | signed MONEY_COST |

### Architecture matrix

| Concept | Legacy | Split | Hybrid | Shared? | Mode discriminator required? |
|---|---|---|---|---|---|
| Big | monolithic LegacyBig | BigCore+BigTrend | Hybrid split roles | no | YES |
| Small | LegacySmall | SmallBase | SmallBase | role-qualified | YES |
| Far | LegacyFar | residual split Far | CurrentFar/NewFar | identity contract shared | YES |
| NewFar source | remaining monolithic Big | remaining component per plan | remaining BigCore only documented | conflict 020 | YES |
| rounding | nearest legacy | role-specific | role-specific | no | YES |
| open/close sequence | legacy FSM | split FSM | immutable Hybrid plan | no | YES |
| Reserve/RecoveryPL | legacy names | typed buckets | typed projected/actual | concepts shared | YES |
| compression/state/risk | legacy rules | split rules | Hybrid + Cycle/Account gates | no | YES |

### Mapping на существующие identifiers (без утверждения соответствия)

| Canonical group | Existing MQL5 identifiers | Existing Python identifiers | Documentation aliases | Mapping status |
|---|---|---|---|---|
| CurrentFar / OldFar | `Ctx.far*`, `oldFar*` | model `far` fields | Far, OldFar | PARTIAL_MATCH |
| BigCore / BigTrend / SmallBase | `Ctx.bigCore*`, `Ctx.bigTrend*`, `Ctx.smallBase*` | oracle role fields | Core, Trend, Small | SEMANTIC_MATCH |
| Raw/Normalized/Requested/Filled/Actual lots | various `*Lot`, request/result/position fields | vector stage fields | lot, volume | AMBIGUOUS |
| PartialFarBudget* | close-Far budget fields | ledger bucket fields | CloseFarBudget, PartialBudget | PARTIAL_MATCH |
| FinalReserve* | `totalReserve`, ledger fields | reserve model | Reserve, TotalReserve | AMBIGUOUS |
| Carry* / TransitionBudget* | Hybrid state fields where present | oracle buckets | Carry, TransitionBudget | PARTIAL_MATCH |
| RecoveryPL* | `realRecoveryPL`, projected fields | oracle P/L fields | RecoveryPL, RealRecoveryPL | AMBIGUOUS |
| TransitionNet | Small transition net fields | oracle TransitionNet | SmallReverseNet | PARTIAL_MATCH |
| FinalClosePreview / ActualSuccess | pending state/result fields | route model | Final Close | PARTIAL_MATCH |
| CycleId / EventId | `cycleId`, ledger event fields | namespace fields | CycleID, EventKey | SEMANTIC_MATCH |
| Snapshot / revision / fingerprint | Hybrid plan/snapshot structures | oracle snapshots | plan hash/revision | PARTIAL_MATCH |
| Cycle/Account Risk | not Stage-3.1.3 implementation target | model metrics where present | Risk | MISSING |

`EXACT_MATCH`, `SEMANTIC_MATCH`, `PARTIAL_MATCH`, `AMBIGUOUS`, `MISSING`, `LEGACY_ONLY`, `HYBRID_ONLY` describe mapping quality only. They do not prove code compliance.

### FORBIDDEN_CONVERSIONS

| From | Forbidden target | Required evidence/conversion |
|---|---|---|
| MONEY | LOT | broker-aware price path and symbol properties |
| LOT | MONEY | OrderCalcProfit or explicit broker-aware model |
| POINTS | MONEY | no universal constant; symbol/tick path required |
| PROJECTED | ACTUAL | broker result + deals + position + reconciliation |
| REQUESTED | FILLED | confirmed broker/deal result |
| FILLED | POSITION_ACTUAL | reconciled position snapshot |
| GROSS | NET | explicit commission/swap/fee/spread/slippage set |
| SIGNED_LOSS | LOSS_MAGNITUDE | explicit abs and renamed output |
| CYCLE_RISK | ACCOUNT_RISK | separate account aggregation/gate |
| COMMENT | UNIQUE_IDENTITY | Symbol+Magic+CycleID+identifier |
| TICKET | POSITION_IDENTIFIER | terminal identity properties |
| LEGACY_BIG | BIG_CORE | explicit mode migration/plan |
| BIG_TREND | NEW_FAR | forbidden by documented Hybrid role contract |
| RAW_LOT | REQUESTED_LOT | normalization and volume gates |

### Formula typing (type check only; no proof of laws)

| Formula ID | Formula | Left type | Right types | Dimension/sign | Projected/Actual | Status |
|---|---|---|---|---|---|---|
| TYPE-F-01 | BigLot=FarLot×BigRatio | LOT_CALCULATED | LOT×RATIO | LOT, >=0 | PROJECTED | DOCUMENTED_NOT_APPROVED/profile conflict |
| TYPE-F-02 | SmallLot=BigLot×SmallRatio | LOT_CALCULATED | LOT×RATIO | LOT, >=0 | PROJECTED | DOCUMENTED_NOT_APPROVED/profile conflict |
| TYPE-F-03 | CloseFarBudget=NetProfit×CloseFarShare | MONEY_PROJECTED/REALIZED by source | MONEY×SHARE | MONEY | class must be explicit | APPROVED_TERM |
| TYPE-F-04 | ReserveAdd=NetProfit×ReserveShare | MONEY_PROJECTED/REALIZED by source | MONEY×SHARE | MONEY | class must be explicit | APPROVED_TERM |
| TYPE-F-05 | RecoveryPLCloseNow=RealizedCyclePL+FloatingManagedPL−ExpectedExitCosts | MONEY_PROJECTED | MONEY+MONEY−MONEY | signed MONEY | PROJECTED | APPROVED_TERM |
| TYPE-F-06 | ReserveCoverage=ReserveAvailable/FinalCloseRequirement | RATIO | MONEY/MONEY | dimensionless >=0 | mixed actual requirement | APPROVED_TERM |
| TYPE-F-07 | TransitionNet=sum leg nets+budget−costs | MONEY_PROJECTED/REALIZED | MONEY terms | signed MONEY | suffix required | APPROVED_TERM |
| TYPE-F-08 | NewBigGross=NextCore+NextTrend | LOT_CALCULATED | LOT+LOT | LOT >=0 | PROJECTED | APPROVED_TERM |
| TYPE-F-09 | CompressionRatio=NewFar/OldFar | RATIO | LOT/LOT | dimensionless | PROJECTED or ACTUAL suffix | APPROVED_TERM |

### Unresolved conflict control

Parameters BigRatio, SmallRatio, CloseBigOnSmallShare, RemainBigOnSmallShare, CloseFarShare and ReserveShare have `UNRESOLVED_PARAMETER_PROFILE` and conflict IDs 001–006; no numeric production choice is made. NewFar terms have `UNRESOLVED_MODE_ROUTING`, conflict 020, resolution 3.1.6/3.1.8. MaximumNewBigToOldFarRatio references conflict 022; SmallReverseNet policy references 023; architecture mode routing references 031. Bare unresolved markers without conflict ID/resolution stage are forbidden.

### Canonical term table (216 terms)

<!-- STAGE_3_1_3_CANONICAL_TABLE_START -->
| Canonical term | Русское название | Profile | Type | Unit | Sign | Projected/Actual | Authoritative source | Rounding | Tolerance | Aliases | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Legacy | Устаревшая архитектура | Legacy | STATE | enum/structured record | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | DOCUMENTED_NOT_APPROVED |
| LegacyMode | Устаревшая архитектура режим | Legacy | STATE | enum/structured record | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| LegacyBig | Устаревшая архитектура компенсирующая позиция | LegacyBig | ROLE_ID | integer/string identity | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| LegacySmall | Устаревшая архитектура защитная позиция | LegacySmall | ROLE_ID | integer/string identity | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| LegacyFar | Устаревшая архитектура хвостовая позиция | LegacyFar | ROLE_ID | integer/string identity | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| MonolithicBig | Монолитный компенсирующая позиция | MonolithicBig | ROLE_ID | integer/string identity | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| Split | Разделённый | Split | STATE | enum/structured record | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | DOCUMENTED_NOT_APPROVED |
| SplitMode | Разделённый режим | Split | STATE | enum/structured record | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| SplitBig | Разделённый компенсирующая позиция | SplitBig | ROLE_ID | integer/string identity | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| BigCore | Компенсирующая позиция основная часть | BigCore | ROLE_ID | integer/string identity | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT | Core | APPROVED_TERM |
| BigTrend | Компенсирующая позиция трендовая часть | BigTrend | ROLE_ID | integer/string identity | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT | Trend | APPROVED_TERM |
| BigGross | совокупный расчётный объём частей Big | BigGross | LOT_CALCULATED | lot | >= 0 | PROJECTED | BigCoreLotProjected + BigTrendLotProjected из одного immutable plan | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | DOCUMENTED_NOT_APPROVED |
| SmallBase | Защитная позиция базовая | SmallBase | ROLE_ID | integer/string identity | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT | Small | APPROVED_TERM |
| Hybrid | Гибридный | Hybrid | STATE | enum/structured record | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | DOCUMENTED_NOT_APPROVED |
| HybridSplitBig | Гибридный разделённый компенсирующая позиция | HybridSplitBig | STATE | enum/structured record | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| HybridMode | Гибридный режим | Hybrid | STATE | enum/structured record | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| HybridPlan | Гибридный план | HybridPlan | PLAN_OBJECT | structured plan | not numeric | PROJECTED | immutable planner result bound to SnapshotFingerprint and PlanFingerprint | NO_ADDITIONAL_ROUNDING | EXACT STRUCTURE | — | APPROVED_TERM |
| HybridPreview | Гибридный preview | HybridPreview | PREVIEW_OBJECT | structured preview | not numeric | PROJECTED | preview calculator result bound to SnapshotFingerprint | NO_ADDITIONAL_ROUNDING | EXACT STRUCTURE | — | APPROVED_TERM |
| HybridExecution | Гибридный исполнение | HybridExecution | EXECUTION_OBJECT | structured execution object | not numeric | REQUESTED/EXECUTED | broker result + confirmed deal history + current position reconciliation scoped by ApprovedPlan fingerprint | NO_ADDITIONAL_ROUNDING | EXACT STRUCTURE | — | APPROVED_TERM |
| InitialBuy | Начальная покупка | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| InitialSell | Начальная продажа | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| InitialProfitLeg | Начальная прибыль leg | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| InitialLosingLeg | Начальная убыточная leg | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| InitialIgnoredProfit | Начальная исключённая прибыль | Role-qualified architecture | MONEY_REALIZED | account money | signed | ACTUAL CONFIRMED | confirmed closing deal aggregation of InitialProfitLeg filtered by Symbol+Magic+CycleID+position identity | ROUND_TO_MONEY_DIGITS at ledger/report boundary | MoneyTolerance | — | APPROVED_TERM |
| OldFar | Предыдущая хвостовая позиция | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| CurrentFar | Текущая хвостовая позиция | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | Far | APPROVED_TERM |
| ResidualFar | Остаточная хвостовая позиция | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| NewFar | Новая хвостовая позиция | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| LegacyBigPosition | Устаревшая архитектура компенсирующая позиция позиция | Role-qualified architecture | POSITION_ID | position reference identity | not numeric | ACTUAL CURRENT | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| BigCorePosition | Компенсирующая позиция основная часть позиция | Role-qualified architecture | POSITION_ID | position reference identity | not numeric | ACTUAL CURRENT | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| BigTrendPosition | Компенсирующая позиция трендовая часть позиция | Role-qualified architecture | POSITION_ID | position reference identity | not numeric | ACTUAL CURRENT | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| LegacySmallPosition | Устаревшая архитектура защитная позиция позиция | Role-qualified architecture | POSITION_ID | position reference identity | not numeric | ACTUAL CURRENT | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| SmallBasePosition | Защитная позиция базовая позиция | Role-qualified architecture | POSITION_ID | position reference identity | not numeric | ACTUAL CURRENT | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| ManagedPosition | Управляемая позиция | Role-qualified architecture | POSITION_ID | position reference identity | not numeric | ACTUAL CURRENT | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| UnmanagedPosition | Неуправляемая позиция | Role-qualified architecture | POSITION_ID | position reference identity | not numeric | ACTUAL CURRENT | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| ForeignCyclePosition | Чужая цикл позиция | Role-qualified architecture | POSITION_ID | position reference identity | not numeric | ACTUAL CURRENT | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| FarDirection | Хвостовая позиция направление | Role-qualified architecture | DIRECTION_ENUM | BUY/SELL enum | not numeric | ACTUAL CONFIRMED or POLICY DERIVED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| OppositeFarDirection | Противоположное хвостовая позиция направление | Role-qualified architecture | DIRECTION_ENUM | BUY/SELL enum | not numeric | ACTUAL CONFIRMED or POLICY DERIVED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| SameAsFarDirection | Совпадающее с хвостовая позиция направление | Role-qualified architecture | DIRECTION_ENUM | BUY/SELL enum | not numeric | ACTUAL CONFIRMED or POLICY DERIVED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| BigDirection | Компенсирующая позиция направление | Role-qualified architecture | DIRECTION_ENUM | BUY/SELL enum | not numeric | ACTUAL CONFIRMED or POLICY DERIVED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| SmallDirection | Защитная позиция направление | Role-qualified architecture | DIRECTION_ENUM | BUY/SELL enum | not numeric | ACTUAL CONFIRMED or POLICY DERIVED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| TrendDirection | Трендовая часть направление | Role-qualified architecture | DIRECTION_ENUM | BUY/SELL enum | not numeric | ACTUAL CONFIRMED or POLICY DERIVED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| ReverseDirection | Разворот направление | Role-qualified architecture | DIRECTION_ENUM | BUY/SELL enum | not numeric | ACTUAL CONFIRMED or POLICY DERIVED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| RawLot | Сырой объём в лотах | Legacy/Split/Hybrid, role-qualified | LOT_RAW | lot | >= 0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| CalculatedLot | Расчётный объём в лотах | Legacy/Split/Hybrid, role-qualified | LOT_CALCULATED | lot | >= 0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| NormalizedLot | Нормализованный объём в лотах | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >= 0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| RequestedLot | Запрошенный объём в лотах | Legacy/Split/Hybrid, role-qualified | LOT_REQUESTED | lot | >= 0 | REQUESTED | approved immutable plan | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| FilledLot | Исполненный объём в лотах | Legacy/Split/Hybrid, role-qualified | LOT_FILLED | lot | >= 0 | CONFIRMED | confirmed deals/trade result | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| ActualPositionLot | Фактический позиция объём в лотах | Legacy/Split/Hybrid, role-qualified | LOT_POSITION_ACTUAL | lot | >= 0 | ACTUAL CURRENT | current MT5 position snapshot | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| ResidualLotProjected | Остаточная объём в лотах прогнозный | Legacy/Split/Hybrid, role-qualified | LOT_RESIDUAL | lot | >= 0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| ResidualLotActual | Остаточная объём в лотах фактический | Legacy/Split/Hybrid, role-qualified | LOT_POSITION_ACTUAL | lot | >= 0 | ACTUAL CURRENT | current MT5 position snapshot | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| FarLotRaw | Хвостовая позиция объём в лотах сырой | Legacy/Split/Hybrid, role-qualified | LOT_RAW | lot | >= 0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| FarLotCalculated | Хвостовая позиция объём в лотах расчётный | Legacy/Split/Hybrid, role-qualified | LOT_CALCULATED | lot | >= 0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| FarLotNormalized | Хвостовая позиция объём в лотах нормализованный | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >= 0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| FarLotRequested | Хвостовая позиция объём в лотах запрошенный | Legacy/Split/Hybrid, role-qualified | LOT_REQUESTED | lot | >= 0 | REQUESTED | approved immutable plan | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| FarLotFilled | Хвостовая позиция объём в лотах исполненный | Legacy/Split/Hybrid, role-qualified | LOT_FILLED | lot | >= 0 | CONFIRMED | confirmed deals/trade result | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| FarLotActual | Хвостовая позиция объём в лотах фактический | Legacy/Split/Hybrid, role-qualified | LOT_POSITION_ACTUAL | lot | >= 0 | ACTUAL CURRENT | current MT5 position snapshot | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | FarLot, Ctx.farLot | APPROVED_TERM |
| BigCoreLotRaw | Компенсирующая позиция основная часть объём в лотах сырой | Legacy/Split/Hybrid, role-qualified | LOT_RAW | lot | >= 0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| BigCoreLotNormalized | Компенсирующая позиция основная часть объём в лотах нормализованный | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >= 0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| BigCoreLotRequested | Компенсирующая позиция основная часть объём в лотах запрошенный | Legacy/Split/Hybrid, role-qualified | LOT_REQUESTED | lot | >= 0 | REQUESTED | approved immutable plan | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| BigCoreLotFilled | Компенсирующая позиция основная часть объём в лотах исполненный | Legacy/Split/Hybrid, role-qualified | LOT_FILLED | lot | >= 0 | CONFIRMED | confirmed deals/trade result | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| BigCoreLotActual | Компенсирующая позиция основная часть объём в лотах фактический | Legacy/Split/Hybrid, role-qualified | LOT_POSITION_ACTUAL | lot | >= 0 | ACTUAL CURRENT | current MT5 position snapshot | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| BigTrendLotRaw | Компенсирующая позиция трендовая часть объём в лотах сырой | Legacy/Split/Hybrid, role-qualified | LOT_RAW | lot | >= 0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| BigTrendLotNormalized | Компенсирующая позиция трендовая часть объём в лотах нормализованный | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >= 0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| SmallBaseLotRaw | Защитная позиция базовая объём в лотах сырой | Legacy/Split/Hybrid, role-qualified | LOT_RAW | lot | >= 0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| SmallBaseLotNormalized | Защитная позиция базовая объём в лотах нормализованный | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >= 0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| PartialFarCloseLotCalculated | Частичный хвостовая позиция закрытие объём в лотах расчётный | Legacy/Split/Hybrid, role-qualified | LOT_CALCULATED | lot | >= 0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| PartialFarCloseLotNormalized | Частичный хвостовая позиция закрытие объём в лотах нормализованный | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >= 0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| PartialFarCloseLotRequested | Частичный хвостовая позиция закрытие объём в лотах запрошенный | Legacy/Split/Hybrid, role-qualified | LOT_REQUESTED | lot | >= 0 | REQUESTED | approved immutable plan | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| PartialFarCloseLotFilled | Частичный хвостовая позиция закрытие объём в лотах исполненный | Legacy/Split/Hybrid, role-qualified | LOT_FILLED | lot | >= 0 | CONFIRMED | confirmed deals/trade result | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| FarResidualProjected | Хвостовая позиция остаточная прогнозный | Legacy/Split/Hybrid, role-qualified | LOT_RESIDUAL | lot | >= 0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| FarResidualActual | Хвостовая позиция остаточная фактический | Legacy/Split/Hybrid, role-qualified | LOT_POSITION_ACTUAL | lot | >= 0 | ACTUAL CURRENT | current MT5 position snapshot | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| NewFarCandidateLot | Новая хвостовая позиция кандидат объём в лотах | Legacy/Split/Hybrid, role-qualified | LOT_CALCULATED | lot | >= 0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | UNRESOLVED_MODE_ROUTING |
| NewFarProjectedLot | Новая хвостовая позиция прогнозный объём в лотах | Legacy/Split/Hybrid, role-qualified | LOT_RAW | lot | >= 0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | UNRESOLVED_MODE_ROUTING |
| NewFarNormalizedLot | Новая хвостовая позиция нормализованный объём в лотах | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >= 0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | UNRESOLVED_MODE_ROUTING |
| NewFarPromotedLot | Новая хвостовая позиция назначенный объём в лотах | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >= 0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | UNRESOLVED_MODE_ROUTING |
| NewFarActualLot | Новая хвостовая позиция фактический объём в лотах | Legacy/Split/Hybrid, role-qualified | LOT_POSITION_ACTUAL | lot | >= 0 | ACTUAL CURRENT | current MT5 position snapshot | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | UNRESOLVED_MODE_ROUTING |
| Point | Размер пункта | All profiles; Symbol-bound | PRICE_POINT_SIZE | price per point | > 0 | SYMBOL PROPERTY | SymbolInfoDouble(symbol, SYMBOL_POINT) | NO_ADDITIONAL_ROUNDING | EXACT PROPERTY SNAPSHOT | — | APPROVED_TERM |
| TickSize | Тик размер | All profiles; Symbol-bound | PRICE_TICK_SIZE | price per tick | > 0 | SYMBOL PROPERTY | SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE) | NO_ADDITIONAL_ROUNDING | EXACT PROPERTY SNAPSHOT | — | APPROVED_TERM |
| TickValue | Тик стоимость | All profiles; Symbol-bound | PRICE_PROJECTED | price | > 0 | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| MarketBidPrice | Рыночная Bid цена | All profiles; Symbol-bound | PRICE_BID | price | > 0 | ACTUAL CURRENT | SymbolInfoDouble(symbol, SYMBOL_BID) | NO_ADDITIONAL_ROUNDING | PriceTolerance | — | APPROVED_TERM |
| MarketAskPrice | Рыночная Ask цена | All profiles; Symbol-bound | PRICE_ASK | price | > 0 | ACTUAL CURRENT | SymbolInfoDouble(symbol, SYMBOL_ASK) | NO_ADDITIONAL_ROUNDING | PriceTolerance | — | APPROVED_TERM |
| PositionOpenPrice | Позиция открытие цена | All profiles; Symbol-bound | PRICE_OPEN | price | > 0 | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| TriggerPrice | Триггер цена | All profiles; Symbol-bound | PRICE_PROJECTED | price | > 0 | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| TargetPrice | Целевая цена | All profiles; Symbol-bound | PRICE_PROJECTED | price | > 0 | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| ControlPrice | Контрольная цена | All profiles; Symbol-bound | PRICE_PROJECTED | price | > 0 | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| ProjectedExitPrice | Прогнозный выход цена | All profiles; Symbol-bound | PRICE_PROJECTED | price | > 0 | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| ExecutedDealPrice | Исполненная сделка цена | All profiles; Symbol-bound | PRICE_EXECUTED | price | > 0 | CONFIRMED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| PriceDelta | Цена дельта | All profiles; Symbol-bound | PRICE_DELTA | price | signed | PROJECTED | difference of two explicitly named prices | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| DistancePoints | Расстояние пункты | All profiles; Symbol-bound | DISTANCE_POINTS | points | non-negative distance | PROJECTED or ACTUAL MEASUREMENT | explicit price delta divided by SYMBOL_POINT | NO_ADDITIONAL_ROUNDING | PointTolerance | — | APPROVED_TERM |
| DistanceTicks | Расстояние тики | All profiles; Symbol-bound | DISTANCE_TICKS | ticks | non-negative distance | PROJECTED or ACTUAL MEASUREMENT | explicit price delta divided by SYMBOL_TRADE_TICK_SIZE | NO_ADDITIONAL_ROUNDING | PointTolerance | — | APPROVED_TERM |
| BidAwareClosePrice | Bid учитывающая сторону рынка закрытие цена | All profiles; Symbol-bound | PRICE_BID | price | > 0 | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| AskAwareClosePrice | Ask учитывающая сторону рынка закрытие цена | All profiles; Symbol-bound | PRICE_ASK | price | > 0 | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| FarOpenPriceActual | Хвостовая позиция открытие цена фактический | All profiles; Symbol-bound | PRICE_OPEN | price | > 0 | ACTUAL CURRENT | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| BigCoreOpenPriceActual | Компенсирующая позиция основная часть открытие цена фактический | All profiles; Symbol-bound | PRICE_OPEN | price | > 0 | ACTUAL CURRENT | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| BigTrendOpenPriceActual | Компенсирующая позиция трендовая часть открытие цена фактический | All profiles; Symbol-bound | PRICE_OPEN | price | > 0 | ACTUAL CURRENT | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| SmallBaseOpenPriceActual | Защитная позиция базовая открытие цена фактический | All profiles; Symbol-bound | PRICE_OPEN | price | > 0 | ACTUAL CURRENT | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| GrossProfit | Валовая прибыль | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| GrossLoss | Валовая убыток | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | >= 0 | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| NetProfit | Чистый результат прибыль | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| LegNet | Leg чистый результат | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| BasketNet | Корзина чистый результат | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| HarvestGross | Сбор прибыли валовая | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | >= 0 | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| HarvestNet | Сбор прибыли чистый результат | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| SmallReverseNet | Защитная позиция разворот чистый результат | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | UNRESOLVED_BUSINESS_POLICY |
| TransitionNet | Переход чистый результат | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| RealizedCyclePL | Реализованный цикл pl | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| FloatingManagedPL | Плавающий управляемая pl | Cycle/account as explicitly qualified | MONEY_FLOATING | account money | signed | ACTUAL CURRENT | current position or broker-aware price model | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| ProjectedFloatingPL | Прогнозный плавающий pl | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | signed | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| RecoveryPLAnalytic | Восстановление pl аналитический | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | signed | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| RecoveryPLProjected | Восстановление pl прогнозный | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | signed | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| RecoveryPLCloseNow | Восстановление pl закрытие сейчас | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | signed | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| RealRecoveryPL | Подтверждённый восстановление pl | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | realRecoveryPL | APPROVED_TERM |
| RecoverySlope | Восстановление наклон | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | signed | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| RecoveryMonotonicity | Восстановление монотонность | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | >= 0 | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| ExpectedExitCosts | Ожидаемые выход расходы | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | >= 0 | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| CommissionCost | Комиссия cost | Cycle/account as explicitly qualified | MONEY_COST | account money | >= 0 | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| SwapCost | Своп cost | Cycle/account as explicitly qualified | MONEY_COST | account money | >= 0 | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| FeeCost | Сбор cost | Cycle/account as explicitly qualified | MONEY_COST | account money | >= 0 | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| SpreadCost | Спред cost | Cycle/account as explicitly qualified | MONEY_COST | account money | >= 0 | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| SlippageCost | Проскальзывание cost | Cycle/account as explicitly qualified | MONEY_COST | account money | >= 0 | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| PositionPLSigned | Позиция pl со знаком | Cycle/account as explicitly qualified | MONEY_FLOATING | account money | signed | ACTUAL CURRENT | current position or broker-aware price model | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| FarLossSigned | Хвостовая позиция убыток со знаком | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| FarLossMagnitude | Хвостовая позиция убыток модуль | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | >= 0 | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| PartialFarBudgetProjected | Частичный хвостовая позиция бюджет прогнозный | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | >= 0 | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| PartialFarBudgetReal | Частичный хвостовая позиция бюджет подтверждённый | Cycle/account as explicitly qualified | MONEY_RESERVED | account money | >= 0 | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| PartialFarBudgetAvailable | Частичный хвостовая позиция бюджет доступный | Cycle/account as explicitly qualified | MONEY_AVAILABLE | account money | >= 0 | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| PartialFarBudgetConsumed | Частичный хвостовая позиция бюджет израсходованный | Cycle/account as explicitly qualified | MONEY_CONSUMED | account money | >= 0 | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| PartialFarBudgetResidual | Частичный хвостовая позиция бюджет остаточная | Cycle/account as explicitly qualified | MONEY_RESIDUAL | account money | >= 0 | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| FinalReserveProjected | Финальный резерв прогнозный | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | >= 0 | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| FinalReserveReal | Финальный резерв подтверждённый | Cycle/account as explicitly qualified | MONEY_RESERVED | account money | >= 0 | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | TotalReserve, finalReserveReal | APPROVED_TERM |
| ReserveAddProjected | Резерв начисление прогнозный | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | >= 0 | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| ReserveAddReal | Резерв начисление подтверждённый | Cycle/account as explicitly qualified | MONEY_RESERVED | account money | >= 0 | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| ReserveAvailable | Резерв доступный | Cycle/account as explicitly qualified | MONEY_AVAILABLE | account money | >= 0 | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| ReserveConsumed | Резерв израсходованный | Cycle/account as explicitly qualified | MONEY_CONSUMED | account money | >= 0 | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| ReserveResidual | Резерв остаточная | Cycle/account as explicitly qualified | MONEY_RESIDUAL | account money | >= 0 | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| CarryAvailable | Переносимый остаток доступный | Cycle/account as explicitly qualified | MONEY_AVAILABLE | account money | >= 0 | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| CarryConsumed | Переносимый остаток израсходованный | Cycle/account as explicitly qualified | MONEY_CONSUMED | account money | >= 0 | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| CarryResidual | Переносимый остаток остаточная | Cycle/account as explicitly qualified | MONEY_RESIDUAL | account money | >= 0 | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| TransitionBudgetAvailable | Переход бюджет доступный | Cycle/account as explicitly qualified | MONEY_AVAILABLE | account money | >= 0 | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| FinalCloseRequirement | Финальный закрытие требование | Cycle/account as explicitly qualified | MONEY_RESERVED | account money | >= 0 | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| BasketRiskMoney | Корзина риск денежный | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | >= 0 | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| AccountRiskMoney | Счёт риск денежный | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | >= 0 | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| BigRatio | Компенсирующая позиция отношение | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | >= 0 | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | UNRESOLVED_PARAMETER_PROFILE |
| SmallRatio | Защитная позиция отношение | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | >= 0 | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | UNRESOLVED_PARAMETER_PROFILE |
| CloseBigOnSmallShare | Закрытие компенсирующая позиция on защитная позиция доля | Profile-qualified; unresolved values not selected | SHARE | 1 (dimensionless) | >= 0 | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | UNRESOLVED_PARAMETER_PROFILE |
| RemainBigOnSmallShare | Remain компенсирующая позиция on защитная позиция доля | Profile-qualified; unresolved values not selected | SHARE | 1 (dimensionless) | >= 0 | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | UNRESOLVED_PARAMETER_PROFILE |
| CloseFarShare | Закрытие хвостовая позиция доля | Profile-qualified; unresolved values not selected | SHARE | 1 (dimensionless) | >= 0 | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | UNRESOLVED_PARAMETER_PROFILE |
| ReserveShare | Резерв доля | Profile-qualified; unresolved values not selected | SHARE | 1 (dimensionless) | >= 0 | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | UNRESOLVED_PARAMETER_PROFILE |
| SmallReserveShare | Защитная позиция резерв доля | Profile-qualified; unresolved values not selected | SHARE | 1 (dimensionless) | >= 0 | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| CompressionRatio | Сжатие отношение | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | >= 0 | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| ReserveCoverageRatio | Резерв покрытие отношение | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | >= 0 | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| RecoveryCoverageRatio | Восстановление покрытие отношение | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | >= 0 | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| MaximumNewBigToOldFarRatio | Максимальное новая компенсирующая позиция to предыдущая хвостовая позиция отношение | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | >= 0 | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | UNRESOLVED_BUSINESS_POLICY |
| MinimumReserveCatchUpRatio | Минимальное резерв catch up отношение | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | >= 0 | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| PercentValue | Процент стоимость | Profile-qualified; unresolved values not selected | PERCENT | 1 (dimensionless) | >= 0 | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| ScaleMultiplier | Масштаб множитель | Profile-qualified; unresolved values not selected | MULTIPLIER | 1 (dimensionless) | >= 0 | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| RiskThresholdRatio | Риск порог отношение | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | >= 0 | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| SymbolId | Символ идентификатор | Symbol+Magic+CycleID+role scope | SYMBOL_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| MagicId | Магический номер идентификатор | Symbol+Magic+CycleID+role scope | MAGIC_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | MagicNumber | APPROVED_TERM |
| CycleId | Цикл идентификатор | Symbol+Magic+CycleID+role scope | CYCLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | CycleID, cycleId | APPROVED_TERM |
| RoleId | Роль идентификатор | Symbol+Magic+CycleID+role scope | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| PositionIdentifier | Позиция идентификатор | Symbol+Magic+CycleID+role scope | POSITION_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | POSITION_IDENTIFIER | APPROVED_TERM |
| PositionTicket | Позиция тикет | Symbol+Magic+CycleID+role scope | POSITION_TICKET | integer/string identity | not numeric | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | ticket | APPROVED_TERM |
| OrderTicket | Ордер тикет | Symbol+Magic+CycleID+role scope | ORDER_TICKET | integer/string identity | not numeric | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| DealTicket | Сделка тикет | Symbol+Magic+CycleID+role scope | DEAL_TICKET | integer/string identity | not numeric | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| EventId | Событие идентификатор | Symbol+Magic+CycleID+role scope | EVENT_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| EventKey | Событие ключ | Symbol+Magic+CycleID+role scope | EVENT_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| SnapshotFingerprint | Снимок отпечаток | Symbol+Magic+CycleID+role scope | FINGERPRINT | integer/string identity | not numeric | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT HASH MATCH | — | APPROVED_TERM |
| PlanFingerprint | План отпечаток | Symbol+Magic+CycleID+role scope | FINGERPRINT | integer/string identity | not numeric | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT HASH MATCH | — | APPROVED_TERM |
| PositionComment | Позиция комментарий | Symbol+Magic+CycleID+role scope | DIAGNOSTIC_TEXT | diagnostic text | not numeric | ACTUAL OBSERVATION | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT STRUCTURE | — | APPROVED_TERM |
| SnapshotRevision | Снимок ревизия | Symbol+Magic+CycleID+role scope | EVENT_ID | integer revision identity | not numeric | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| StateRevision | Состояние ревизия | Symbol+Magic+CycleID+role scope | EVENT_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| State | Состояние | Cycle lifecycle | STATE | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| Phase | Фаза | Cycle lifecycle | PHASE | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| Event | Событие | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| Observation | Наблюдение | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| GateResult | Шлюз результат | Cycle lifecycle | GATE_RESULT | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| ExecutionResult | Исполнение результат | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| Outcome | Исход | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| ReasonCode | Причина код | Cycle lifecycle | REASON_CODE | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| ErrorCode | Ошибка код | Cycle lifecycle | REASON_CODE | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| DiagnosticText | Диагностический текст | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| CandidatePlan | Кандидат план | Cycle lifecycle | PLAN_OBJECT | structured plan | not numeric | PROJECTED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| ApprovedImmutablePlan | Утверждённый неизменяемый план | Cycle lifecycle | PLAN_OBJECT | structured plan | not numeric | PROJECTED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| ExecutionRequest | Исполнение запрос | Cycle lifecycle | EXECUTION_REQUEST | structured request | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| BrokerExecutionResult | Брокерский исполнение результат | Cycle lifecycle | EXECUTION_RESULT | structured result | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| ReconciledResult | Сверенный результат | Cycle lifecycle | RECONCILED_RESULT | structured result | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| CommittedLedgerEvent | Зафиксированный ledger событие | Cycle lifecycle | LEDGER_EVENT | structured event | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| BaseSnapshot | Базовая снимок | Cycle lifecycle | SNAPSHOT_PROJECTED | structured snapshot | not numeric | PROJECTED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| WorstSnapshot | Worst снимок | Cycle lifecycle | SNAPSHOT_WORST_CASE | structured snapshot | not numeric | PROJECTED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| ActualSnapshot | Фактический снимок | Cycle lifecycle | SNAPSHOT_ACTUAL | structured snapshot | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| SnapshotStaleFlag | Снимок устаревший признак | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| FinalClosePreview | Финальный закрытие preview | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | PROJECTED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| FinalCloseActualSuccess | Финальный закрытие фактический успех | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| MoneyTolerance | Денежный допуск | Dimension-specific only | MONEY_TOLERANCE | account money | >= 0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| VolumeToleranceLots | Объём допуск lots | Dimension-specific only | LOT_TOLERANCE | lot | >= 0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| PriceTolerance | Цена допуск | Dimension-specific only | PRICE_TOLERANCE | price | >= 0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| PointTolerance | Размер пункта допуск | Dimension-specific only | POINT_TOLERANCE | point | >= 0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| RatioTolerance | Отношение допуск | Dimension-specific only | RATIO_TOLERANCE | dimensionless ratio | >= 0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| ComparisonEpsilon | Comparison epsilon | Dimension-specific only | COMPARISON_EPSILON | dimensionless epsilon | >= 0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | EXACT HASH MATCH | — | APPROVED_TERM |
| ReserveMismatchTolerance | Резерв mismatch допуск | Dimension-specific only | MONEY_TOLERANCE | account money | >= 0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| GeometryTolerance | Геометрический допуск | Dimension-specific only | LOT_TOLERANCE | lot | >= 0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| FingerprintTolerance | Отпечаток допуск | Dimension-specific only | IDENTITY_MATCH_POLICY | dimensionless policy | >= 0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | EXACT HASH MATCH | — | APPROVED_TERM |
| ProjectedData | Прогнозный данные | All | BOOLEAN_RESULT | data-state enum | not numeric | PROJECTED | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| RequestedData | Запрошенный данные | All | BOOLEAN_RESULT | data-state enum | not numeric | REQUESTED | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| ExecutedData | Исполненная данные | All | BOOLEAN_RESULT | data-state enum | not numeric | EXECUTED | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| ConfirmedData | Подтверждённые данные | All | BOOLEAN_RESULT | data-state enum | not numeric | CONFIRMED | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| ReconciledData | Сверенный данные | All | BOOLEAN_RESULT | data-state enum | not numeric | RECONCILED | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| PersistedData | Сохранённые данные | All | BOOLEAN_RESULT | data-state enum | not numeric | PERSISTED | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| StaleData | Устаревший данные | All | BOOLEAN_RESULT | data-state enum | not numeric | STALE | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| InvalidData | Невалидные данные | All | BOOLEAN_RESULT | data-state enum | not numeric | INVALID | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| NotApplicableValue | Не применимо стоимость | All | BOOLEAN_RESULT | data-state enum | not numeric | NOTAPPLICABLEVALUE | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| NotCalculatedValue | Не расчётный стоимость | All | BOOLEAN_RESULT | data-state enum | not numeric | NOTCALCULATEDVALUE | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| NotAvailableValue | Не доступный стоимость | All | BOOLEAN_RESULT | data-state enum | not numeric | NOTAVAILABLEVALUE | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| UnknownValue | Неизвестное стоимость | All | BOOLEAN_RESULT | data-state enum | not numeric | UNKNOWNVALUE | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| CurrentBid | текущая цена Bid | All | PRICE_BID | price | > 0 | ACTUAL CURRENT | SymbolInfoDouble(symbol, SYMBOL_BID) | NO_ADDITIONAL_ROUNDING | PriceTolerance | — | APPROVED_TERM |
| CurrentAsk | текущая цена Ask | All | PRICE_ASK | price | > 0 | ACTUAL CURRENT | SymbolInfoDouble(symbol, SYMBOL_ASK) | NO_ADDITIONAL_ROUNDING | PriceTolerance | — | APPROVED_TERM |
| ReserveProjected | прогнозный резерв до подтверждения | All | MONEY_PROJECTED | account money | >= 0 | PROJECTED | OrderCalcProfit outputs plus explicit projected allocation model | NO_ADDITIONAL_ROUNDING | MoneyTolerance | — | APPROVED_TERM |
| ReserveCoverage | отношение доступного резерва к требованию закрытия | All | RATIO | dimensionless | >= 0 | PROJECTED or ACTUAL RATIO | ReserveAvailable divided by FinalCloseRequirement | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| Symbol | торговый символ цикла | All | SYMBOL_ID | string identity | not numeric | ACTUAL CONFIRMED | current chart/request symbol and reconciled position symbol | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| MagicNumber | магический номер стратегии | All | MAGIC_ID | integer identity | not numeric | POLICY/ACTUAL CONFIRMED | configured MagicNumber verified against position/deal properties | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| CycleID | идентификатор recovery-цикла | All | CYCLE_ID | integer identity | not numeric | ACTUAL CONFIRMED | persisted cycle creation event confirmed by reconciliation | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| EventID | идентификатор ledger-события | All | EVENT_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | exactly-once ledger event namespace | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| Fingerprint | типизированный отпечаток snapshot или plan | All | FINGERPRINT | hash identity | not numeric | PROJECTED or RECONCILED | canonical serialization of typed fields and revision | NO_ADDITIONAL_ROUNDING | EXACT HASH MATCH | — | APPROVED_TERM |
| Comment | комментарий торгового объекта | All | DIAGNOSTIC_TEXT | text | not numeric | ACTUAL OBSERVATION | MT5 position/order/deal comment property | NO_ADDITIONAL_ROUNDING | EXACT TEXT; never identity | — | APPROVED_TERM |
| Preview | read-only предварительная оценка | All | PREVIEW_OBJECT | structured preview | not numeric | PROJECTED | fresh immutable snapshot evaluator | NO_ADDITIONAL_ROUNDING | EXACT STRUCTURE | — | APPROVED_TERM |
| Candidate | кандидат плана до полного gate-chain | All | OUTCOME | structured record | not numeric | PROJECTED | solver output tied to source fingerprint | NO_ADDITIONAL_ROUNDING | EXACT STRUCTURE | — | APPROVED_TERM |
| Plan | расчётный набор действий и ожиданий | All | PLAN_OBJECT | structured plan | not numeric | PROJECTED | candidate planner output with revision | NO_ADDITIONAL_ROUNDING | EXACT STRUCTURE | — | APPROVED_TERM |
| ApprovedPlan | неизменяемый план после всех обязательных gates | All | PLAN_OBJECT | structured approved plan | not numeric | PROJECTED APPROVED | approved immutable plan and fingerprint | NO_ADDITIONAL_ROUNDING | EXACT STRUCTURE | — | APPROVED_TERM |<!-- STAGE_3_1_3_CANONICAL_TABLE_END -->

<!-- STAGE_3_1_3_SECTION_END -->

## Semantic category matrix (Этап 3.1.3, вторая коррекция)

Матрица типизирует смысл сущности независимо от совпадения слов в имени. Она является
machine-readable правилом validator, но не изменяет торговую математику.

| Semantic category | Разрешённые Type | Unit contract | Lifecycle class | Запрещённая подмена |
| --- | --- | --- | --- | --- |
| `ROLE` | `ROLE_ID` | role identity | `ROLE` | role ↛ lot/money/position object |
| `IDENTITY` | `*_ID`, `*_TICKET`, `FINGERPRINT` | typed identity/hash | `IDENTITY` | ticket ↛ position identifier |
| `LOT_VALUE` | `LOT_*` | lot | projected/requested/deal/actual-position | volume ↛ role identity |
| `MONEY_VALUE` | `MONEY_*` | account money | projected/deal/ledger/actual-position | projected money ↛ ledger money |
| `PRICE_OR_DISTANCE` | `PRICE_*`, `POINTS`, `TICKS`, `PRICE_DELTA`, `DISTANCE_*` | price/point/tick | symbol-property/projected/deal | Point ↛ TickSize; distance ↛ money |
| `POLICY` | `RATIO`, `SHARE`, `PERCENT`, `MULTIPLIER`, `BOOLEAN_POLICY` | dimensionless/boolean | `POLICY` | share ↛ money or lot |
| `STATE_OR_RESULT` | `STATE`, `PHASE`, `OUTCOME`, `REASON_CODE`, `GATE_RESULT` | enum/schema | `STATE` | diagnostic text ↛ state/reason |
| `STRUCTURED_OBJECT` | plan/snapshot/event/observation object types | typed structure | object-specific | preview ↛ execution result |

`Semantic exception: NOT_APPLICABLE` означает, что запись следует матрице без
исключения. Любое будущее исключение обязано содержать содержательное обоснование,
считаться validator и перечисляться в отчёте этапа.

## Candidate-to-entity mapping contract (третья коррекция 3.1.3)

Mapping обязан проходить цепочку `canonical term → generated candidates → declaration → use sites → semantic/lifecycle score → accepted/rejected → status`. `MISSING` допустим только после непустого candidate audit и документированного отклонения каждого найденного candidate. Полный `MISSING` для языка и менее 25 non-missing mappings являются blocking defects.

### Candidate score matrix

| Component | Evidence | Назначение |
| --- | --- | --- |
| name similarity | Camel/snake/Pascal tokens и aliases | поиск, но не доказательство эквивалентности |
| type/unit compatibility | declaration type и canonical family | отсечение money/lot/identity mismatch |
| semantic/source compatibility | declaration context и read/write sites | отличие runtime value от log/comment token |
| lifecycle compatibility | scope, cache/authoritative, projected/actual | выбор PARTIAL против SEMANTIC/EXACT |
| total score | 0–29 reject; 30–49 ambiguous; 50–69 partial; 70–89 semantic candidate; 90–100 exact candidate | EXACT всё равно требует отдельного proof |

### Sign, source and lifecycle validation matrix

| Family/class | Sign | Authoritative-source requirement | Lifecycle requirement |
| --- | --- | --- | --- |
| `LOT_REQUESTED` | `>= 0` | ApprovedPlan/request | immutable request, broker outcome replacement |
| `LOT_FILLED` | `>= 0` | confirmed deal/fill | immutable deal aggregation/history restart |
| `LOT_POSITION_ACTUAL` | `>= 0` | current position snapshot | stale after trade; terminal refresh |
| `MONEY_REALIZED` | signed or non-negative magnitude | confirmed deals/ledger | DEAL or exactly-once LEDGER |
| `PRICE_EXECUTED` | `> 0` | confirmed deal/execution | immutable deal evidence |
| `IDENTITY` / `STATE` | not numeric | owner/state-machine evidence | exact identity/event transition |
| `PROJECTED_VALUE` | family-specific | immutable input snapshot | stale on revision; never assignment-to-actual |
| `LEDGER` | money-specific | EventID + confirmed evidence | exactly-once persistence and restart reconciliation |
