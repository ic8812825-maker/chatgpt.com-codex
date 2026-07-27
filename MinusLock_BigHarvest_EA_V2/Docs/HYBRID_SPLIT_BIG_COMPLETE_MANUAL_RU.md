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
| MoneyTolerance | MONEY | absolute account money | money reconciliation/typed comparisons | lot/price/ratio | cannot turn negative into PASS |
| VolumeToleranceLots | LOT | absolute lot | actual/expected volume | money/price | cannot hide executable residual |
| PriceTolerance | PRICE | absolute symbol price | price snapshot/reconciliation | money/lot | snapshot freshness only as specified |
| PointTolerance | POINTS | absolute points | point distances | price without conversion | no implicit conversion |
| RatioTolerance | RATIO | absolute ratio | ratios/shares | money/lot | strict bounds remain strict |
| ComparisonEpsilon | typed | type-bound only | named diagnostic comparison | universal use | no business weakening |
| ReserveMismatchTolerance | MONEY | absolute | reserve ledger reconciliation | lot | mismatch detection only |
| GeometryTolerance | LOT | symbol-aware | strict compression after normalization | money | cannot make equality strict improvement |
| FingerprintTolerance | FINGERPRINT | exact semantic | serialized typed fields | numeric substitution | any semantic mismatch makes stale |

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
| Legacy | Legacy | Legacy | STATE | architecture/role | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | exact mode/role match | — | DOCUMENTED_NOT_APPROVED |
| LegacyMode | LegacyMode | Legacy | STATE | architecture/role | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | exact mode/role match | — | APPROVED_TERM |
| LegacyBig | LegacyBig | LegacyBig | ROLE_ID | architecture/role | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | exact mode/role match | — | APPROVED_TERM |
| LegacySmall | LegacySmall | LegacySmall | ROLE_ID | architecture/role | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | exact mode/role match | — | APPROVED_TERM |
| LegacyFar | LegacyFar | LegacyFar | ROLE_ID | architecture/role | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | exact mode/role match | — | APPROVED_TERM |
| MonolithicBig | MonolithicBig | MonolithicBig | ROLE_ID | architecture/role | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | exact mode/role match | — | APPROVED_TERM |
| Split | Split | Split | STATE | architecture/role | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | exact mode/role match | — | DOCUMENTED_NOT_APPROVED |
| SplitMode | SplitMode | Split | STATE | architecture/role | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | exact mode/role match | — | APPROVED_TERM |
| SplitBig | SplitBig | SplitBig | ROLE_ID | architecture/role | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | exact mode/role match | — | APPROVED_TERM |
| BigCore | BigCore | BigCore | ROLE_ID | architecture/role | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | exact mode/role match | Core | APPROVED_TERM |
| BigTrend | BigTrend | BigTrend | ROLE_ID | architecture/role | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | exact mode/role match | Trend | APPROVED_TERM |
| BigGross | BigGross | BigGross | ROLE_ID | architecture/role | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | exact mode/role match | — | APPROVED_TERM |
| SmallBase | SmallBase | SmallBase | ROLE_ID | architecture/role | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | exact mode/role match | Small | APPROVED_TERM |
| Hybrid | Hybrid | Hybrid | STATE | architecture/role | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | exact mode/role match | — | DOCUMENTED_NOT_APPROVED |
| HybridSplitBig | HybridSplitBig | HybridSplitBig | STATE | architecture/role | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | exact mode/role match | — | APPROVED_TERM |
| HybridMode | HybridMode | Hybrid | STATE | architecture/role | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | exact mode/role match | — | APPROVED_TERM |
| HybridPlan | HybridPlan | HybridPlan | STATE | architecture/role | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | exact mode/role match | — | APPROVED_TERM |
| HybridPreview | HybridPreview | HybridPreview | STATE | architecture/role | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | exact mode/role match | — | APPROVED_TERM |
| HybridExecution | HybridExecution | HybridExecution | STATE | architecture/role | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | exact mode/role match | — | APPROVED_TERM |
| InitialBuy | InitialBuy | Role-qualified architecture | ROLE_ID | role | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| InitialSell | InitialSell | Role-qualified architecture | ROLE_ID | role | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| InitialProfitLeg | InitialProfitLeg | Role-qualified architecture | ROLE_ID | role | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| InitialLosingLeg | InitialLosingLeg | Role-qualified architecture | ROLE_ID | role | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| InitialIgnoredProfit | InitialIgnoredProfit | Role-qualified architecture | MONEY_REALIZED | account money | >=0 diagnostic, excluded | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| OldFar | OldFar | Role-qualified architecture | ROLE_ID | role | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| CurrentFar | CurrentFar | Role-qualified architecture | ROLE_ID | role | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | Far | APPROVED_TERM |
| ResidualFar | ResidualFar | Role-qualified architecture | ROLE_ID | role | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| NewFar | NewFar | Role-qualified architecture | ROLE_ID | role | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| LegacyBigPosition | LegacyBigPosition | Role-qualified architecture | ROLE_ID | role | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| BigCorePosition | BigCorePosition | Role-qualified architecture | ROLE_ID | role | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| BigTrendPosition | BigTrendPosition | Role-qualified architecture | ROLE_ID | role | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| LegacySmallPosition | LegacySmallPosition | Role-qualified architecture | ROLE_ID | role | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| SmallBasePosition | SmallBasePosition | Role-qualified architecture | ROLE_ID | role | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| ManagedPosition | ManagedPosition | Role-qualified architecture | ROLE_ID | role | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| UnmanagedPosition | UnmanagedPosition | Role-qualified architecture | ROLE_ID | role | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| ForeignCyclePosition | ForeignCyclePosition | Role-qualified architecture | ROLE_ID | role | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| FarDirection | FarDirection | Role-qualified architecture | STATE | direction enum | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| OppositeFarDirection | OppositeFarDirection | Role-qualified architecture | STATE | direction enum | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| SameAsFarDirection | SameAsFarDirection | Role-qualified architecture | STATE | direction enum | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| BigDirection | BigDirection | Role-qualified architecture | STATE | direction enum | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| SmallDirection | SmallDirection | Role-qualified architecture | STATE | direction enum | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| TrendDirection | TrendDirection | Role-qualified architecture | STATE | direction enum | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| ReverseDirection | ReverseDirection | Role-qualified architecture | STATE | direction enum | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | exact role/identity; actual lot uses VolumeToleranceLots | — | APPROVED_TERM |
| RawLot | RawLot | Legacy/Split/Hybrid, role-qualified | LOT_RAW | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| CalculatedLot | CalculatedLot | Legacy/Split/Hybrid, role-qualified | LOT_CALCULATED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| NormalizedLot | NormalizedLot | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| RequestedLot | RequestedLot | Legacy/Split/Hybrid, role-qualified | LOT_REQUESTED | lot | >=0; active position >0 | REQUESTED | approved immutable plan | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| FilledLot | FilledLot | Legacy/Split/Hybrid, role-qualified | LOT_FILLED | lot | >=0; active position >0 | CONFIRMED | confirmed deals/trade result | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| ActualPositionLot | ActualPositionLot | Legacy/Split/Hybrid, role-qualified | LOT_POSITION_ACTUAL | lot | >=0; active position >0 | ACTUAL CURRENT | current MT5 position snapshot | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| ResidualLotProjected | ResidualLotProjected | Legacy/Split/Hybrid, role-qualified | LOT_RESIDUAL | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| ResidualLotActual | ResidualLotActual | Legacy/Split/Hybrid, role-qualified | LOT_POSITION_ACTUAL | lot | >=0; active position >0 | ACTUAL CURRENT | current MT5 position snapshot | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| FarLotRaw | FarLotRaw | Legacy/Split/Hybrid, role-qualified | LOT_RAW | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| FarLotCalculated | FarLotCalculated | Legacy/Split/Hybrid, role-qualified | LOT_CALCULATED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| FarLotNormalized | FarLotNormalized | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| FarLotRequested | FarLotRequested | Legacy/Split/Hybrid, role-qualified | LOT_REQUESTED | lot | >=0; active position >0 | REQUESTED | approved immutable plan | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| FarLotFilled | FarLotFilled | Legacy/Split/Hybrid, role-qualified | LOT_FILLED | lot | >=0; active position >0 | CONFIRMED | confirmed deals/trade result | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| FarLotActual | FarLotActual | Legacy/Split/Hybrid, role-qualified | LOT_POSITION_ACTUAL | lot | >=0; active position >0 | ACTUAL CURRENT | current MT5 position snapshot | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | FarLot, Ctx.farLot | APPROVED_TERM |
| BigCoreLotRaw | BigCoreLotRaw | Legacy/Split/Hybrid, role-qualified | LOT_RAW | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| BigCoreLotNormalized | BigCoreLotNormalized | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| BigCoreLotRequested | BigCoreLotRequested | Legacy/Split/Hybrid, role-qualified | LOT_REQUESTED | lot | >=0; active position >0 | REQUESTED | approved immutable plan | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| BigCoreLotFilled | BigCoreLotFilled | Legacy/Split/Hybrid, role-qualified | LOT_FILLED | lot | >=0; active position >0 | CONFIRMED | confirmed deals/trade result | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| BigCoreLotActual | BigCoreLotActual | Legacy/Split/Hybrid, role-qualified | LOT_POSITION_ACTUAL | lot | >=0; active position >0 | ACTUAL CURRENT | current MT5 position snapshot | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| BigTrendLotRaw | BigTrendLotRaw | Legacy/Split/Hybrid, role-qualified | LOT_RAW | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| BigTrendLotNormalized | BigTrendLotNormalized | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| SmallBaseLotRaw | SmallBaseLotRaw | Legacy/Split/Hybrid, role-qualified | LOT_RAW | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| SmallBaseLotNormalized | SmallBaseLotNormalized | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| PartialFarCloseLotCalculated | PartialFarCloseLotCalculated | Legacy/Split/Hybrid, role-qualified | LOT_CALCULATED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| PartialFarCloseLotNormalized | PartialFarCloseLotNormalized | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| PartialFarCloseLotRequested | PartialFarCloseLotRequested | Legacy/Split/Hybrid, role-qualified | LOT_REQUESTED | lot | >=0; active position >0 | REQUESTED | approved immutable plan | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| PartialFarCloseLotFilled | PartialFarCloseLotFilled | Legacy/Split/Hybrid, role-qualified | LOT_FILLED | lot | >=0; active position >0 | CONFIRMED | confirmed deals/trade result | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| FarResidualProjected | FarResidualProjected | Legacy/Split/Hybrid, role-qualified | LOT_RESIDUAL | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| FarResidualActual | FarResidualActual | Legacy/Split/Hybrid, role-qualified | LOT_POSITION_ACTUAL | lot | >=0; active position >0 | ACTUAL CURRENT | current MT5 position snapshot | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| NewFarCandidateLot | NewFarCandidateLot | Legacy/Split/Hybrid, role-qualified | LOT_CALCULATED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | UNRESOLVED_MODE_ROUTING |
| NewFarProjectedLot | NewFarProjectedLot | Legacy/Split/Hybrid, role-qualified | LOT_RAW | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | UNRESOLVED_MODE_ROUTING |
| NewFarNormalizedLot | NewFarNormalizedLot | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | UNRESOLVED_MODE_ROUTING |
| NewFarPromotedLot | NewFarPromotedLot | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | UNRESOLVED_MODE_ROUTING |
| NewFarActualLot | NewFarActualLot | Legacy/Split/Hybrid, role-qualified | LOT_POSITION_ACTUAL | lot | >=0; active position >0 | ACTUAL CURRENT | current MT5 position snapshot | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | UNRESOLVED_MODE_ROUTING |
| Point | Point | All profiles; Symbol-bound | PRICE_PROJECTED | price | >0 for absolute price; delta signed | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| TickSize | TickSize | All profiles; Symbol-bound | PRICE_PROJECTED | price | >0 for absolute price; delta signed | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| TickValue | TickValue | All profiles; Symbol-bound | PRICE_PROJECTED | price | >0 for absolute price; delta signed | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| MarketBidPrice | MarketBidPrice | All profiles; Symbol-bound | PRICE_BID | price | >0 for absolute price; delta signed | ACTUAL CURRENT | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| MarketAskPrice | MarketAskPrice | All profiles; Symbol-bound | PRICE_ASK | price | >0 for absolute price; delta signed | ACTUAL CURRENT | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| PositionOpenPrice | PositionOpenPrice | All profiles; Symbol-bound | PRICE_OPEN | price | >0 for absolute price; delta signed | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| TriggerPrice | TriggerPrice | All profiles; Symbol-bound | PRICE_PROJECTED | price | >0 for absolute price; delta signed | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| TargetPrice | TargetPrice | All profiles; Symbol-bound | PRICE_PROJECTED | price | >0 for absolute price; delta signed | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| ControlPrice | ControlPrice | All profiles; Symbol-bound | PRICE_PROJECTED | price | >0 for absolute price; delta signed | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| ProjectedExitPrice | ProjectedExitPrice | All profiles; Symbol-bound | PRICE_PROJECTED | price | >0 for absolute price; delta signed | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| ExecutedDealPrice | ExecutedDealPrice | All profiles; Symbol-bound | PRICE_EXECUTED | price | >0 for absolute price; delta signed | CONFIRMED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| PriceDelta | PriceDelta | All profiles; Symbol-bound | PRICE_DELTA | price | >0 for absolute price; delta signed | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| DistancePoints | DistancePoints | All profiles; Symbol-bound | POINTS | point | >0 for absolute price; delta signed | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PointTolerance | — | APPROVED_TERM |
| DistanceTicks | DistanceTicks | All profiles; Symbol-bound | TICKS | tick | >0 for absolute price; delta signed | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PointTolerance | — | APPROVED_TERM |
| BidAwareClosePrice | BidAwareClosePrice | All profiles; Symbol-bound | PRICE_BID | price | >0 for absolute price; delta signed | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| AskAwareClosePrice | AskAwareClosePrice | All profiles; Symbol-bound | PRICE_ASK | price | >0 for absolute price; delta signed | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| FarOpenPriceActual | FarOpenPriceActual | All profiles; Symbol-bound | PRICE_OPEN | price | >0 for absolute price; delta signed | ACTUAL CURRENT | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| BigCoreOpenPriceActual | BigCoreOpenPriceActual | All profiles; Symbol-bound | PRICE_OPEN | price | >0 for absolute price; delta signed | ACTUAL CURRENT | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| BigTrendOpenPriceActual | BigTrendOpenPriceActual | All profiles; Symbol-bound | PRICE_OPEN | price | >0 for absolute price; delta signed | ACTUAL CURRENT | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| SmallBaseOpenPriceActual | SmallBaseOpenPriceActual | All profiles; Symbol-bound | PRICE_OPEN | price | >0 for absolute price; delta signed | ACTUAL CURRENT | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| GrossProfit | GrossProfit | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed P/L | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| GrossLoss | GrossLoss | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| NetProfit | NetProfit | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed P/L | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| LegNet | LegNet | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed P/L | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| BasketNet | BasketNet | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed P/L | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| HarvestGross | HarvestGross | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| HarvestNet | HarvestNet | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed P/L | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| SmallReverseNet | SmallReverseNet | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed P/L | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | UNRESOLVED_BUSINESS_POLICY |
| TransitionNet | TransitionNet | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed P/L | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| RealizedCyclePL | RealizedCyclePL | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed P/L | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| FloatingManagedPL | FloatingManagedPL | Cycle/account as explicitly qualified | MONEY_FLOATING | account money | signed P/L | ACTUAL CURRENT | current position or broker-aware price model | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| ProjectedFloatingPL | ProjectedFloatingPL | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | signed P/L | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| RecoveryPLAnalytic | RecoveryPLAnalytic | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | signed P/L | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| RecoveryPLProjected | RecoveryPLProjected | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | signed P/L | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| RecoveryPLCloseNow | RecoveryPLCloseNow | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | signed P/L | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| RealRecoveryPL | RealRecoveryPL | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed P/L | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | realRecoveryPL | APPROVED_TERM |
| RecoverySlope | RecoverySlope | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | signed P/L | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| RecoveryMonotonicity | RecoveryMonotonicity | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | non-negative magnitude/bucket | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| ExpectedExitCosts | ExpectedExitCosts | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | non-negative magnitude/bucket | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| CommissionCost | CommissionCost | Cycle/account as explicitly qualified | MONEY_COST | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| SwapCost | SwapCost | Cycle/account as explicitly qualified | MONEY_COST | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| FeeCost | FeeCost | Cycle/account as explicitly qualified | MONEY_COST | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| SpreadCost | SpreadCost | Cycle/account as explicitly qualified | MONEY_COST | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| SlippageCost | SlippageCost | Cycle/account as explicitly qualified | MONEY_COST | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| PositionPLSigned | PositionPLSigned | Cycle/account as explicitly qualified | MONEY_FLOATING | account money | signed P/L | ACTUAL CURRENT | current position or broker-aware price model | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| FarLossSigned | FarLossSigned | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed P/L | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| FarLossMagnitude | FarLossMagnitude | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| PartialFarBudgetProjected | PartialFarBudgetProjected | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | non-negative magnitude/bucket | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| PartialFarBudgetReal | PartialFarBudgetReal | Cycle/account as explicitly qualified | MONEY_RESERVED | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| PartialFarBudgetAvailable | PartialFarBudgetAvailable | Cycle/account as explicitly qualified | MONEY_AVAILABLE | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| PartialFarBudgetConsumed | PartialFarBudgetConsumed | Cycle/account as explicitly qualified | MONEY_CONSUMED | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| PartialFarBudgetResidual | PartialFarBudgetResidual | Cycle/account as explicitly qualified | MONEY_RESIDUAL | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| FinalReserveProjected | FinalReserveProjected | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | non-negative magnitude/bucket | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| FinalReserveReal | FinalReserveReal | Cycle/account as explicitly qualified | MONEY_RESERVED | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | TotalReserve, finalReserveReal | APPROVED_TERM |
| ReserveAddProjected | ReserveAddProjected | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | non-negative magnitude/bucket | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| ReserveAddReal | ReserveAddReal | Cycle/account as explicitly qualified | MONEY_RESERVED | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| ReserveAvailable | ReserveAvailable | Cycle/account as explicitly qualified | MONEY_AVAILABLE | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| ReserveConsumed | ReserveConsumed | Cycle/account as explicitly qualified | MONEY_CONSUMED | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| ReserveResidual | ReserveResidual | Cycle/account as explicitly qualified | MONEY_RESIDUAL | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| CarryAvailable | CarryAvailable | Cycle/account as explicitly qualified | MONEY_AVAILABLE | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| CarryConsumed | CarryConsumed | Cycle/account as explicitly qualified | MONEY_CONSUMED | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| CarryResidual | CarryResidual | Cycle/account as explicitly qualified | MONEY_RESIDUAL | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| TransitionBudgetAvailable | TransitionBudgetAvailable | Cycle/account as explicitly qualified | MONEY_AVAILABLE | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| FinalCloseRequirement | FinalCloseRequirement | Cycle/account as explicitly qualified | MONEY_RESERVED | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| BasketRiskMoney | BasketRiskMoney | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | non-negative magnitude/bucket | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| AccountRiskMoney | AccountRiskMoney | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | non-negative magnitude/bucket | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| BigRatio | BigRatio | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | UNRESOLVED_PARAMETER_PROFILE |
| SmallRatio | SmallRatio | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | UNRESOLVED_PARAMETER_PROFILE |
| CloseBigOnSmallShare | CloseBigOnSmallShare | Profile-qualified; unresolved values not selected | SHARE | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | UNRESOLVED_PARAMETER_PROFILE |
| RemainBigOnSmallShare | RemainBigOnSmallShare | Profile-qualified; unresolved values not selected | SHARE | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | UNRESOLVED_PARAMETER_PROFILE |
| CloseFarShare | CloseFarShare | Profile-qualified; unresolved values not selected | SHARE | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | UNRESOLVED_PARAMETER_PROFILE |
| ReserveShare | ReserveShare | Profile-qualified; unresolved values not selected | SHARE | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | UNRESOLVED_PARAMETER_PROFILE |
| SmallReserveShare | SmallReserveShare | Profile-qualified; unresolved values not selected | SHARE | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| CompressionRatio | CompressionRatio | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| ReserveCoverageRatio | ReserveCoverageRatio | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| RecoveryCoverageRatio | RecoveryCoverageRatio | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| MaximumNewBigToOldFarRatio | MaximumNewBigToOldFarRatio | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | UNRESOLVED_BUSINESS_POLICY |
| MinimumReserveCatchUpRatio | MinimumReserveCatchUpRatio | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| PercentValue | PercentValue | Profile-qualified; unresolved values not selected | PERCENT | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| ScaleMultiplier | ScaleMultiplier | Profile-qualified; unresolved values not selected | MULTIPLIER | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| RiskThresholdRatio | RiskThresholdRatio | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| SymbolId | SymbolId | Symbol+Magic+CycleID+role scope | SYMBOL_ID | identifier | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | exact match; FingerprintTolerance permits no semantic drift | — | APPROVED_TERM |
| MagicId | MagicId | Symbol+Magic+CycleID+role scope | MAGIC_ID | identifier | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | exact match; FingerprintTolerance permits no semantic drift | MagicNumber | APPROVED_TERM |
| CycleId | CycleId | Symbol+Magic+CycleID+role scope | CYCLE_ID | identifier | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | exact match; FingerprintTolerance permits no semantic drift | CycleID, cycleId | APPROVED_TERM |
| RoleId | RoleId | Symbol+Magic+CycleID+role scope | ROLE_ID | identifier | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | exact match; FingerprintTolerance permits no semantic drift | — | APPROVED_TERM |
| PositionIdentifier | PositionIdentifier | Symbol+Magic+CycleID+role scope | POSITION_ID | identifier | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | exact match; FingerprintTolerance permits no semantic drift | POSITION_IDENTIFIER | APPROVED_TERM |
| PositionTicket | PositionTicket | Symbol+Magic+CycleID+role scope | POSITION_TICKET | identifier | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | exact match; FingerprintTolerance permits no semantic drift | ticket | APPROVED_TERM |
| OrderTicket | OrderTicket | Symbol+Magic+CycleID+role scope | ORDER_TICKET | identifier | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | exact match; FingerprintTolerance permits no semantic drift | — | APPROVED_TERM |
| DealTicket | DealTicket | Symbol+Magic+CycleID+role scope | DEAL_TICKET | identifier | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | exact match; FingerprintTolerance permits no semantic drift | — | APPROVED_TERM |
| EventId | EventId | Symbol+Magic+CycleID+role scope | EVENT_ID | identifier | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | exact match; FingerprintTolerance permits no semantic drift | — | APPROVED_TERM |
| EventKey | EventKey | Symbol+Magic+CycleID+role scope | EVENT_ID | identifier | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | exact match; FingerprintTolerance permits no semantic drift | — | APPROVED_TERM |
| SnapshotFingerprint | SnapshotFingerprint | Symbol+Magic+CycleID+role scope | FINGERPRINT | identifier | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | exact match; FingerprintTolerance permits no semantic drift | — | APPROVED_TERM |
| PlanFingerprint | PlanFingerprint | Symbol+Magic+CycleID+role scope | FINGERPRINT | identifier | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | exact match; FingerprintTolerance permits no semantic drift | — | APPROVED_TERM |
| PositionComment | PositionComment | Symbol+Magic+CycleID+role scope | ROLE_ID | identifier | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | exact match; FingerprintTolerance permits no semantic drift | — | APPROVED_TERM |
| SnapshotRevision | SnapshotRevision | Symbol+Magic+CycleID+role scope | ROLE_ID | identifier | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | exact match; FingerprintTolerance permits no semantic drift | — | APPROVED_TERM |
| StateRevision | StateRevision | Symbol+Magic+CycleID+role scope | EVENT_ID | identifier | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | exact match; FingerprintTolerance permits no semantic drift | — | APPROVED_TERM |
| State | State | Cycle lifecycle | STATE | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | exact enum; typed field tolerances inside snapshots | — | APPROVED_TERM |
| Phase | Phase | Cycle lifecycle | PHASE | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | exact enum; typed field tolerances inside snapshots | — | APPROVED_TERM |
| Event | Event | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | exact enum; typed field tolerances inside snapshots | — | APPROVED_TERM |
| Observation | Observation | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | exact enum; typed field tolerances inside snapshots | — | APPROVED_TERM |
| GateResult | GateResult | Cycle lifecycle | GATE_RESULT | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | exact enum; typed field tolerances inside snapshots | — | APPROVED_TERM |
| ExecutionResult | ExecutionResult | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | exact enum; typed field tolerances inside snapshots | — | APPROVED_TERM |
| Outcome | Outcome | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | exact enum; typed field tolerances inside snapshots | — | APPROVED_TERM |
| ReasonCode | ReasonCode | Cycle lifecycle | REASON_CODE | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | exact enum; typed field tolerances inside snapshots | — | APPROVED_TERM |
| ErrorCode | ErrorCode | Cycle lifecycle | REASON_CODE | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | exact enum; typed field tolerances inside snapshots | — | APPROVED_TERM |
| DiagnosticText | DiagnosticText | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | exact enum; typed field tolerances inside snapshots | — | APPROVED_TERM |
| CandidatePlan | CandidatePlan | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | PROJECTED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | exact enum; typed field tolerances inside snapshots | — | APPROVED_TERM |
| ApprovedImmutablePlan | ApprovedImmutablePlan | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | PROJECTED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | exact enum; typed field tolerances inside snapshots | — | APPROVED_TERM |
| ExecutionRequest | ExecutionRequest | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | exact enum; typed field tolerances inside snapshots | — | APPROVED_TERM |
| BrokerExecutionResult | BrokerExecutionResult | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | exact enum; typed field tolerances inside snapshots | — | APPROVED_TERM |
| ReconciledResult | ReconciledResult | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | exact enum; typed field tolerances inside snapshots | — | APPROVED_TERM |
| CommittedLedgerEvent | CommittedLedgerEvent | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | exact enum; typed field tolerances inside snapshots | — | APPROVED_TERM |
| BaseSnapshot | BaseSnapshot | Cycle lifecycle | STATE | enum/structured record | not numeric | PROJECTED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | exact enum; typed field tolerances inside snapshots | — | APPROVED_TERM |
| WorstSnapshot | WorstSnapshot | Cycle lifecycle | STATE | enum/structured record | not numeric | PROJECTED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | exact enum; typed field tolerances inside snapshots | — | APPROVED_TERM |
| ActualSnapshot | ActualSnapshot | Cycle lifecycle | STATE | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | exact enum; typed field tolerances inside snapshots | — | APPROVED_TERM |
| SnapshotStaleFlag | SnapshotStaleFlag | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | exact enum; typed field tolerances inside snapshots | — | APPROVED_TERM |
| FinalClosePreview | FinalClosePreview | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | PROJECTED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | exact enum; typed field tolerances inside snapshots | — | APPROVED_TERM |
| FinalCloseActualSuccess | FinalCloseActualSuccess | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | exact enum; typed field tolerances inside snapshots | — | APPROVED_TERM |
| MoneyTolerance | MoneyTolerance | Dimension-specific only | MONEY_AVAILABLE | same unit as compared operands | >=0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| VolumeToleranceLots | VolumeToleranceLots | Dimension-specific only | LOT_NORMALIZED | same unit as compared operands | >=0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| PriceTolerance | PriceTolerance | Dimension-specific only | PRICE_PROJECTED | same unit as compared operands | >=0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| PointTolerance | PointTolerance | Dimension-specific only | POINTS | same unit as compared operands | >=0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| RatioTolerance | RatioTolerance | Dimension-specific only | RATIO | same unit as compared operands | >=0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| ComparisonEpsilon | ComparisonEpsilon | Dimension-specific only | FINGERPRINT | same unit as compared operands | >=0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| ReserveMismatchTolerance | ReserveMismatchTolerance | Dimension-specific only | MONEY_AVAILABLE | same unit as compared operands | >=0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| GeometryTolerance | GeometryTolerance | Dimension-specific only | LOT_NORMALIZED | same unit as compared operands | >=0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| FingerprintTolerance | FingerprintTolerance | Dimension-specific only | FINGERPRINT | same unit as compared operands | >=0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| ProjectedData | ProjectedData | All | BOOLEAN_RESULT | data-state enum | not numeric | PROJECTED | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| RequestedData | RequestedData | All | BOOLEAN_RESULT | data-state enum | not numeric | REQUESTED | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| ExecutedData | ExecutedData | All | BOOLEAN_RESULT | data-state enum | not numeric | EXECUTED | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| ConfirmedData | ConfirmedData | All | BOOLEAN_RESULT | data-state enum | not numeric | CONFIRMED | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| ReconciledData | ReconciledData | All | BOOLEAN_RESULT | data-state enum | not numeric | RECONCILED | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| PersistedData | PersistedData | All | BOOLEAN_RESULT | data-state enum | not numeric | PERSISTED | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| StaleData | StaleData | All | BOOLEAN_RESULT | data-state enum | not numeric | STALE | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| InvalidData | InvalidData | All | BOOLEAN_RESULT | data-state enum | not numeric | INVALID | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| NotApplicableValue | NotApplicableValue | All | BOOLEAN_RESULT | data-state enum | not numeric | NOTAPPLICABLEVALUE | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| NotCalculatedValue | NotCalculatedValue | All | BOOLEAN_RESULT | data-state enum | not numeric | NOTCALCULATEDVALUE | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| NotAvailableValue | NotAvailableValue | All | BOOLEAN_RESULT | data-state enum | not numeric | NOTAVAILABLEVALUE | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
| UnknownValue | UnknownValue | All | BOOLEAN_RESULT | data-state enum | not numeric | UNKNOWNVALUE | lifecycle transition evidence | NO_ADDITIONAL_ROUNDING | exact state | — | APPROVED_TERM |
<!-- STAGE_3_1_3_CANONICAL_TABLE_END -->

<!-- STAGE_3_1_3_SECTION_END -->
