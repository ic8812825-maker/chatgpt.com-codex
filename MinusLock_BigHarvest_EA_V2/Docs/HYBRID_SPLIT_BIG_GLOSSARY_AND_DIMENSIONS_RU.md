# Hybrid Split Big — расширенный glossary и dimensions appendix

Статус: `SUPPORTING_TYPED_APPENDIX`. Нормативная таблица встроена также в Complete Manual. Это приложение не является конкурирующим source of truth.

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

## Расширенные records canonical terms

### Legacy
CanonicalName: `Legacy`
Русское название: Устаревшая архитектура
Краткое определение: Legacy — typed `STATE` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Устаревшая архитектура»; его authoritative provenance — «explicit mode discriminator + plan role».
Архитектурный профиль: Legacy
Торговая роль: Legacy
Размерность: `STATE`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `STATE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: POLICY stage для Legacy.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: Legacy создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение Legacy историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Устаревшая архитектура» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение Legacy историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: Legacy нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Legacy, тип STATE, class POLICY.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `HSB-DOC-CONFLICT-031`
Resolution stage: `3.1.8`
Статус определения: `DOCUMENTED_NOT_APPROVED`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: Legacy создаётся соответствующим transition, gate или observation event.
Validation event: Legacy проверяется точным enum/schema сравнением.
Freeze/confirmation event: Legacy фиксируется вместе с CycleID и EventID.
Mutation events: Изменяется только явно разрешённым событием своего класса.
Stale triggers: Новая state revision делает прежнее current значение Legacy историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: Legacy отличается от sibling-терминов источником `explicit mode discriminator + plan role`, классом `POLICY` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `Legacy` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `Legacy` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### LegacyMode
CanonicalName: `LegacyMode`
Русское название: Устаревшая архитектура режим
Краткое определение: LegacyMode — typed `STATE` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Устаревшая архитектура режим»; его authoritative provenance — «explicit mode discriminator + plan role».
Архитектурный профиль: Legacy
Торговая роль: LegacyMode
Размерность: `STATE`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `STATE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: POLICY stage для LegacyMode.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: LegacyMode создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение LegacyMode историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Устаревшая архитектура режим» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение LegacyMode историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: LegacyMode нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: LegacyMode, тип STATE, class POLICY.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: LegacyMode создаётся соответствующим transition, gate или observation event.
Validation event: LegacyMode проверяется точным enum/schema сравнением.
Freeze/confirmation event: LegacyMode фиксируется вместе с CycleID и EventID.
Mutation events: Изменяется только явно разрешённым событием своего класса.
Stale triggers: Новая state revision делает прежнее current значение LegacyMode историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: LegacyMode отличается от sibling-терминов источником `explicit mode discriminator + plan role`, классом `POLICY` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `LegacyMode` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `LegacyMode` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### LegacyBig
CanonicalName: `LegacyBig`
Русское название: Устаревшая архитектура компенсирующая позиция
Краткое определение: LegacyBig — Монолитная компенсирующая позиция Legacy mode; не является BigCore и требует явного LegacyMode qualifier. Отличительный объект записи: «Устаревшая архитектура компенсирующая позиция»; его authoritative provenance — «explicit mode discriminator + plan role».
Архитектурный профиль: LegacyBig
Торговая роль: LegacyBig
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: POLICY stage для LegacyBig.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: LegacyBig назначается approved role rule и связывается с position identity. LegacyBig меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку LegacyBig stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Устаревшая архитектура компенсирующая позиция» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку LegacyBig stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: LegacyBig нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: LegacyBig, тип ROLE_ID, class POLICY.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: ROLE
Lifecycle class: ROLE
Creation event: LegacyBig назначается approved role rule и связывается с position identity.
Validation event: Связка LegacyBig проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: LegacyBig меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку LegacyBig stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: LegacyBig отличается от sibling-терминов источником `explicit mode discriminator + plan role`, классом `POLICY` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ROLE`; запись `LegacyBig` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `LegacyBig` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### LegacySmall
CanonicalName: `LegacySmall`
Русское название: Устаревшая архитектура защитная позиция
Краткое определение: LegacySmall — Монолитная защитная позиция Legacy mode; не является SmallBase без mode mapping. Отличительный объект записи: «Устаревшая архитектура защитная позиция»; его authoritative provenance — «explicit mode discriminator + plan role».
Архитектурный профиль: LegacySmall
Торговая роль: LegacySmall
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: POLICY stage для LegacySmall.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: LegacySmall назначается approved role rule и связывается с position identity. LegacySmall меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку LegacySmall stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Устаревшая архитектура защитная позиция» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку LegacySmall stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: LegacySmall нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: LegacySmall, тип ROLE_ID, class POLICY.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: ROLE
Lifecycle class: ROLE
Creation event: LegacySmall назначается approved role rule и связывается с position identity.
Validation event: Связка LegacySmall проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: LegacySmall меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку LegacySmall stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: LegacySmall отличается от sibling-терминов источником `explicit mode discriminator + plan role`, классом `POLICY` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ROLE`; запись `LegacySmall` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `LegacySmall` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### LegacyFar
CanonicalName: `LegacyFar`
Русское название: Устаревшая архитектура хвостовая позиция
Краткое определение: LegacyFar — Хвостовая позиция Legacy cycle; роль не переносится в Hybrid plan без explicit mode routing. Отличительный объект записи: «Устаревшая архитектура хвостовая позиция»; его authoritative provenance — «explicit mode discriminator + plan role».
Архитектурный профиль: LegacyFar
Торговая роль: LegacyFar
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: POLICY stage для LegacyFar.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: LegacyFar назначается approved role rule и связывается с position identity. LegacyFar меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку LegacyFar stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Устаревшая архитектура хвостовая позиция» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку LegacyFar stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: LegacyFar нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: LegacyFar, тип ROLE_ID, class POLICY.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: ROLE
Lifecycle class: ROLE
Creation event: LegacyFar назначается approved role rule и связывается с position identity.
Validation event: Связка LegacyFar проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: LegacyFar меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку LegacyFar stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: LegacyFar отличается от sibling-терминов источником `explicit mode discriminator + plan role`, классом `POLICY` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ROLE`; запись `LegacyFar` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `LegacyFar` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### MonolithicBig
CanonicalName: `MonolithicBig`
Русское название: Монолитный компенсирующая позиция
Краткое определение: MonolithicBig — Расчётно и идентификационно единый LegacyBig без Core/Trend split; отличается от BigGross, который является суммой двух ролей. Отличительный объект записи: «Монолитный компенсирующая позиция»; его authoritative provenance — «explicit mode discriminator + plan role».
Архитектурный профиль: MonolithicBig
Торговая роль: MonolithicBig
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: POLICY stage для MonolithicBig.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: MonolithicBig назначается approved role rule и связывается с position identity. MonolithicBig меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку MonolithicBig stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Монолитный компенсирующая позиция» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку MonolithicBig stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: MonolithicBig нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: MonolithicBig, тип ROLE_ID, class POLICY.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: ROLE
Lifecycle class: ROLE
Creation event: MonolithicBig назначается approved role rule и связывается с position identity.
Validation event: Связка MonolithicBig проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: MonolithicBig меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку MonolithicBig stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: MonolithicBig отличается от sibling-терминов источником `explicit mode discriminator + plan role`, классом `POLICY` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ROLE`; запись `MonolithicBig` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `MonolithicBig` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### Split
CanonicalName: `Split`
Русское название: Разделённый
Краткое определение: Split — Архитектурное поколение, разделяющее компенсирующий Big на BigCore и BigTrend; это не runtime state и не numeric profile. Отличительный объект записи: «Разделённый»; его authoritative provenance — «explicit mode discriminator + plan role».
Архитектурный профиль: Split
Торговая роль: Split
Размерность: `STATE`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `STATE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: POLICY stage для Split.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: Split создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение Split историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Разделённый» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение Split историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: Split нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Split, тип STATE, class POLICY.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `HSB-DOC-CONFLICT-031`
Resolution stage: `3.1.8`
Статус определения: `DOCUMENTED_NOT_APPROVED`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: Split создаётся соответствующим transition, gate или observation event.
Validation event: Split проверяется точным enum/schema сравнением.
Freeze/confirmation event: Split фиксируется вместе с CycleID и EventID.
Mutation events: Изменяется только явно разрешённым событием своего класса.
Stale triggers: Новая state revision делает прежнее current значение Split историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: Split отличается от sibling-терминов источником `explicit mode discriminator + plan role`, классом `POLICY` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `Split` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `Split` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### SplitMode
CanonicalName: `SplitMode`
Русское название: Разделённый режим
Краткое определение: SplitMode — Явный runtime/config discriminator выбора Split role graph; не подменяется фактом наличия поля BigCore. Отличительный объект записи: «Разделённый режим»; его authoritative provenance — «explicit mode discriminator + plan role».
Архитектурный профиль: Split
Торговая роль: SplitMode
Размерность: `STATE`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `STATE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: POLICY stage для SplitMode.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: SplitMode создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение SplitMode историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Разделённый режим» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение SplitMode историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: SplitMode нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SplitMode, тип STATE, class POLICY.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: SplitMode создаётся соответствующим transition, gate или observation event.
Validation event: SplitMode проверяется точным enum/schema сравнением.
Freeze/confirmation event: SplitMode фиксируется вместе с CycleID и EventID.
Mutation events: Изменяется только явно разрешённым событием своего класса.
Stale triggers: Новая state revision делает прежнее current значение SplitMode историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: SplitMode отличается от sibling-терминов источником `explicit mode discriminator + plan role`, классом `POLICY` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `SplitMode` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `SplitMode` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### SplitBig
CanonicalName: `SplitBig`
Русское название: Разделённый компенсирующая позиция
Краткое определение: SplitBig — Совокупность BigCore и BigTrend в Split mode; термин обозначает role group, а не самостоятельный position identifier. Отличительный объект записи: «Разделённый компенсирующая позиция»; его authoritative provenance — «explicit mode discriminator + plan role».
Архитектурный профиль: SplitBig
Торговая роль: SplitBig
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: POLICY stage для SplitBig.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: SplitBig назначается approved role rule и связывается с position identity. SplitBig меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку SplitBig stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Разделённый компенсирующая позиция» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку SplitBig stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: SplitBig нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SplitBig, тип ROLE_ID, class POLICY.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: ROLE
Lifecycle class: ROLE
Creation event: SplitBig назначается approved role rule и связывается с position identity.
Validation event: Связка SplitBig проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: SplitBig меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку SplitBig stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: SplitBig отличается от sibling-терминов источником `explicit mode discriminator + plan role`, классом `POLICY` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ROLE`; запись `SplitBig` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `SplitBig` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### BigCore
CanonicalName: `BigCore`
Русское название: Компенсирующая позиция основная часть
Краткое определение: BigCore — Основная компенсирующая роль Split/Hybrid basket, направленная против CurrentFar и учитываемая отдельно от BigTrend; возможное использование её остатка как NewFar остаётся mode-dependent по конфликту 020. Отличительный объект записи: «Компенсирующая позиция основная часть»; его authoritative provenance — «explicit mode discriminator + plan role».
Архитектурный профиль: BigCore
Торговая роль: BigCore
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: POLICY stage для BigCore.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: BigCore назначается approved role rule и связывается с position identity. BigCore меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку BigCore stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Компенсирующая позиция основная часть» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку BigCore stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: BigCore нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigCore, тип ROLE_ID, class POLICY.
Legacy aliases: Core
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: ROLE
Lifecycle class: ROLE
Creation event: BigCore назначается approved role rule и связывается с position identity.
Validation event: Связка BigCore проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: BigCore меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку BigCore stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: BigCore отличается от sibling-терминов источником `explicit mode discriminator + plan role`, классом `POLICY` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ROLE`; запись `BigCore` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `BigCore` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### BigTrend
CanonicalName: `BigTrend`
Русское название: Компенсирующая позиция трендовая часть
Краткое определение: BigTrend — Дополнительная трендовая роль Split/Hybrid basket против CurrentFar; она не объединяется с BigCore в identity и не может молча быть назначена NewFar. Отличительный объект записи: «Компенсирующая позиция трендовая часть»; его authoritative provenance — «explicit mode discriminator + plan role».
Архитектурный профиль: BigTrend
Торговая роль: BigTrend
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: POLICY stage для BigTrend.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: BigTrend назначается approved role rule и связывается с position identity. BigTrend меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку BigTrend stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Компенсирующая позиция трендовая часть» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку BigTrend stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: BigTrend нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigTrend, тип ROLE_ID, class POLICY.
Legacy aliases: Trend
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: ROLE
Lifecycle class: ROLE
Creation event: BigTrend назначается approved role rule и связывается с position identity.
Validation event: Связка BigTrend проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: BigTrend меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку BigTrend stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: BigTrend отличается от sibling-терминов источником `explicit mode discriminator + plan role`, классом `POLICY` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ROLE`; запись `BigTrend` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `BigTrend` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### BigGross
CanonicalName: `BigGross`
Русское название: совокупный расчётный объём частей Big
Краткое определение: BigGross — projected сумма BigCoreLotProjected и BigTrendLotProjected из одного immutable plan; отличается от каждой role и от actual суммарного объёма открытых позиций. Отличительный объект записи: «совокупный расчётный объём частей Big»; его authoritative provenance — «BigCoreLotProjected + BigTrendLotProjected из одного immutable plan».
Архитектурный профиль: BigGross
Торговая роль: BigGross
Размерность: `LOT_CALCULATED`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: от 0 до суммы допустимых projected объёмов BigCore и BigTrend; NaN и infinity запрещены.
Источник возникновения: арифметика BigCoreLotProjected + BigTrendLotProjected внутри одного plan snapshot.
Authoritative source: BigCoreLotProjected + BigTrendLotProjected из одного immutable plan
Время фиксации: после расчёта обеих частей и до broker request.
Projected/Actual class: `PROJECTED`
Normalization: сам BigGross не нормализуется; складываются уже явно типизированные projected компоненты.
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: BigGross вычисляется из snapshot inputs: BigCoreLotProjected + BigTrendLotProjected из одного immutable plan. Не мутирует; изменение inputs создаёт новую revision BigGross. Market, symbol, config или snapshot revision делает BigGross stale. пересчёт BigGross на новом immutable snapshot. После execution projected BigGross завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «совокупный расчётный объём частей Big» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает BigGross stale.
Authoritative replacement: пересчёт BigGross на новом immutable snapshot.
Допустимые операции: сложение только совместимых projected lot components; lot-сравнения выполняются с `VolumeToleranceLots`.
Запрещённые подмены: BigGross нельзя подменять BigCore/BigTrend role identity, actual position volume, requested/filled lot или stale plan.
Связанные сущности: BigCoreLotProjected, BigTrendLotProjected; тип LOT_CALCULATED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::nextBigGross
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `DOCUMENTED_NOT_APPROVED`
Semantic category: LOT_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: BigGross вычисляется из snapshot inputs: BigCoreLotProjected + BigTrendLotProjected из одного immutable plan.
Validation event: BigGross валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: BigGross замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision BigGross.
Stale triggers: Market, symbol, config или snapshot revision делает BigGross stale.
Replacement source: пересчёт BigGross на новом immutable snapshot.
Terminal condition: После execution projected BigGross завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: BigGross отличается от sibling-терминов источником `BigCoreLotProjected + BigTrendLotProjected из одного immutable plan`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `BigGross` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `BigGross` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### SmallBase
CanonicalName: `SmallBase`
Русское название: Защитная позиция базовая
Краткое определение: SmallBase — Защитная роль Split/Hybrid basket в направлении CurrentFar; её volume, P/L и identity ведутся отдельно от LegacySmall. Отличительный объект записи: «Защитная позиция базовая»; его authoritative provenance — «explicit mode discriminator + plan role».
Архитектурный профиль: SmallBase
Торговая роль: SmallBase
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: POLICY stage для SmallBase.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: SmallBase назначается approved role rule и связывается с position identity. SmallBase меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку SmallBase stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Защитная позиция базовая» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку SmallBase stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: SmallBase нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SmallBase, тип ROLE_ID, class POLICY.
Legacy aliases: Small
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: ROLE
Lifecycle class: ROLE
Creation event: SmallBase назначается approved role rule и связывается с position identity.
Validation event: Связка SmallBase проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: SmallBase меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку SmallBase stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: SmallBase отличается от sibling-терминов источником `explicit mode discriminator + plan role`, классом `POLICY` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ROLE`; запись `SmallBase` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `SmallBase` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### Hybrid
CanonicalName: `Hybrid`
Русское название: Гибридный
Краткое определение: Hybrid — Архитектурный scope, объединяющий split roles с immutable preview/plan/gates; conflict 031 запрещает считать его alias Legacy. Отличительный объект записи: «Гибридный»; его authoritative provenance — «explicit mode discriminator + plan role».
Архитектурный профиль: Hybrid
Торговая роль: Hybrid
Размерность: `STATE`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `STATE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: POLICY stage для Hybrid.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: Hybrid создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение Hybrid историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Гибридный» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение Hybrid историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: Hybrid нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Hybrid, тип STATE, class POLICY.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `HSB-DOC-CONFLICT-031`
Resolution stage: `3.1.8`
Статус определения: `DOCUMENTED_NOT_APPROVED`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: Hybrid создаётся соответствующим transition, gate или observation event.
Validation event: Hybrid проверяется точным enum/schema сравнением.
Freeze/confirmation event: Hybrid фиксируется вместе с CycleID и EventID.
Mutation events: Изменяется только явно разрешённым событием своего класса.
Stale triggers: Новая state revision делает прежнее current значение Hybrid историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: Hybrid отличается от sibling-терминов источником `explicit mode discriminator + plan role`, классом `POLICY` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `Hybrid` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `Hybrid` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### HybridSplitBig
CanonicalName: `HybridSplitBig`
Русское название: Гибридный разделённый компенсирующая позиция
Краткое определение: HybridSplitBig — Полное имя Hybrid basket с BigCore, BigTrend и SmallBase; определяет vocabulary scope, но не выбирает coefficients. Отличительный объект записи: «Гибридный разделённый компенсирующая позиция»; его authoritative provenance — «explicit mode discriminator + plan role».
Архитектурный профиль: HybridSplitBig
Торговая роль: HybridSplitBig
Размерность: `STATE`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `STATE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: POLICY stage для HybridSplitBig.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: HybridSplitBig создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение HybridSplitBig историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Гибридный разделённый компенсирующая позиция» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение HybridSplitBig историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: HybridSplitBig нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: HybridSplitBig, тип STATE, class POLICY.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: HybridSplitBig создаётся соответствующим transition, gate или observation event.
Validation event: HybridSplitBig проверяется точным enum/schema сравнением.
Freeze/confirmation event: HybridSplitBig фиксируется вместе с CycleID и EventID.
Mutation events: Изменяется только явно разрешённым событием своего класса.
Stale triggers: Новая state revision делает прежнее current значение HybridSplitBig историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: HybridSplitBig отличается от sibling-терминов источником `explicit mode discriminator + plan role`, классом `POLICY` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `HybridSplitBig` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `HybridSplitBig` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### HybridMode
CanonicalName: `HybridMode`
Русское название: Гибридный режим
Краткое определение: HybridMode — Mode discriminator для Hybrid plan/execution contracts; его наличие должно подтверждаться config/plan, а не comment. Отличительный объект записи: «Гибридный режим»; его authoritative provenance — «explicit mode discriminator + plan role».
Архитектурный профиль: Hybrid
Торговая роль: HybridMode
Размерность: `STATE`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `STATE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: POLICY stage для HybridMode.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: HybridMode создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение HybridMode историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Гибридный режим» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение HybridMode историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: HybridMode нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: HybridMode, тип STATE, class POLICY.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: HybridMode создаётся соответствующим transition, gate или observation event.
Validation event: HybridMode проверяется точным enum/schema сравнением.
Freeze/confirmation event: HybridMode фиксируется вместе с CycleID и EventID.
Mutation events: Изменяется только явно разрешённым событием своего класса.
Stale triggers: Новая state revision делает прежнее current значение HybridMode историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: HybridMode отличается от sibling-терминов источником `explicit mode discriminator + plan role`, классом `POLICY` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `HybridMode` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `HybridMode` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### HybridPlan
CanonicalName: `HybridPlan`
Русское название: Гибридный план
Краткое определение: HybridPlan — типизированный projected набор ролей, объёмов, цен и ожидаемых действий Hybrid mode, построенный на одном immutable snapshot; он не является runtime State или доказательством исполнения.
Архитектурный профиль: HybridPlan
Торговая роль: HybridPlan
Размерность: `PLAN_OBJECT`
Unit: `structured plan`
Знак: not numeric
Допустимый диапазон: валидная PLAN_OBJECT schema с согласованными CycleID, SnapshotFingerprint и PlanFingerprint; отсутствие обязательного поля означает INVALID.
Источник возникновения: Hybrid planner output from immutable Base/Worst snapshot and explicit mode discriminator
Authoritative source: immutable planner result bound to SnapshotFingerprint and PlanFingerprint
Время фиксации: после candidate validation и до approval/execution.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT STRUCTURE`
Lifecycle: HybridPlan создаётся из immutable snapshot; stale при input revision; заменяется пересчётом и никогда не становится actual присваиванием.
Условия stale: изменение input, market, symbol-property или snapshot revision делает HybridPlan stale.
Authoritative replacement: новый HybridPlan, пересчитанный и validated на новом immutable snapshot.
Допустимые операции: schema validation, fingerprint comparison и immutable freeze в ApprovedPlan; state-transition операции неприменимы.
Запрещённые подмены: HybridPlan нельзя подменять Preview, runtime State, ExecutionRequest либо actual ExecutionResult.
Связанные сущности: Candidate, ApprovedPlan, PlanFingerprint; тип PLAN_OBJECT, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: PROJECTED_VALUE
Creation event: HybridPlan создаётся из immutable calculation snapshot.
Validation event: HybridPlan проверяется по PLAN_OBJECT schema, dimensions, CycleID и fingerprint.
Freeze/confirmation event: После gates HybridPlan может быть скопирован в immutable ApprovedPlan; сам plan не становится actual.
Mutation events: Не мутирует; новая revision создаёт новый object.
Stale triggers: input or snapshot revision делает object stale.
Replacement source: пересчёт на новом immutable snapshot.
Terminal condition: завершается перед execution либо freeze approved plan.
Persistence behavior: plan/audit evidence, не actual ledger commit.
Restart behavior: после restart сверяется fingerprint и пересчитывается.
Отличие от: HybridPlan отличается от HybridPreview наличием сформированного набора действий, а от ApprovedPlan — отсутствием approval freeze.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие projected-plan lifecycle clauses разделяются с Plan; HybridPlan дополнительно фиксирует Hybrid mode roles и explicit mode discriminator.
Evidence: mapping record `HybridPlan` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### HybridPreview
CanonicalName: `HybridPreview`
Русское название: Гибридный preview
Краткое определение: HybridPreview — Read-only расчёт Base/Worst candidate до approval; PASS не является broker execution success. Отличительный объект записи: «Гибридный preview»; его authoritative provenance — «explicit mode discriminator + plan role».
Архитектурный профиль: HybridPreview
Торговая роль: HybridPreview
Размерность: `PREVIEW_OBJECT`
Unit: `structured preview`
Знак: not numeric
Допустимый диапазон: валидная PREVIEW_OBJECT schema для Base/Worst snapshot; broker outcome и actual deal evidence в preview запрещены.
Источник возникновения: read-only Hybrid calculation over immutable Base/Worst snapshot
Authoritative source: preview calculator result bound to SnapshotFingerprint
Время фиксации: при завершении read-only formula preview до Candidate approval.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT STRUCTURE`
Lifecycle: HybridPreview создаётся из immutable snapshot; stale при input revision; заменяется пересчётом и никогда не становится actual присваиванием.
Условия stale: изменение input, market, symbol properties или snapshot revision делает HybridPreview stale.
Authoritative replacement: новый read-only HybridPreview на новом immutable snapshot.
Допустимые операции: read-only inspection, schema validation и сравнение snapshot fingerprint; исполнение и state transition запрещены.
Запрещённые подмены: HybridPreview нельзя подменять ApprovedPlan, ExecutionRequest, broker result или current State.
Связанные сущности: Preview, Candidate, BaseSnapshot; тип PREVIEW_OBJECT, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: PROJECTED_VALUE
Creation event: HybridPreview создаётся из immutable calculation snapshot.
Validation event: HybridPreview проверяется по PREVIEW_OBJECT schema, dimensions и SnapshotFingerprint.
Freeze/confirmation event: NOT_APPLICABLE: preview не approved и не execution request; validated данные передаются отдельному Candidate.
Mutation events: Не мутирует; новая revision создаёт новый object.
Stale triggers: input or snapshot revision делает object stale.
Replacement source: пересчёт на новом immutable snapshot.
Terminal condition: завершается перед execution либо freeze approved plan.
Persistence behavior: plan/audit evidence, не actual ledger commit.
Restart behavior: после restart сверяется fingerprint и пересчитывается.
Отличие от: HybridPreview отличается от HybridPlan отсутствием утверждаемого набора действий и от ExecutionResult отсутствием broker evidence.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие lifecycle clauses класса PROJECTED_VALUE разделяются с Preview; HybridPreview отличается source-контекстом Hybrid Base/Worst calculation.
Evidence: mapping record `HybridPreview` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### HybridExecution
CanonicalName: `HybridExecution`
Русское название: Гибридный исполнение
Краткое определение: HybridExecution — Исполнение ApprovedPlan с broker result, deals и reconciliation; отличается от preview фактическими evidence и возможным partial outcome. Отличительный объект записи: «Гибридный исполнение»; его authoritative provenance — «explicit mode discriminator + plan role».
Архитектурный профиль: HybridExecution
Торговая роль: HybridExecution
Размерность: `EXECUTION_OBJECT`
Unit: `structured execution object`
Знак: not numeric
Допустимый диапазон: валидная EXECUTION_OBJECT schema, связывающая ApprovedPlan, request identity, broker outcomes, deals и reconciliation revision.
Источник возникновения: ExecutionRequest plus broker response, confirmed deal events and reconciliation snapshot
Authoritative source: broker result + confirmed deal history + current position reconciliation scoped by ApprovedPlan fingerprint
Время фиксации: создаётся при request submission и финализируется только после reconciliation.
Projected/Actual class: `REQUESTED/EXECUTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT STRUCTURE`
Lifecycle: HybridExecution создаётся из ApprovedPlan и ExecutionRequest; broker results и deal events дополняют execution aggregate, после reconciliation он заменяется ReconciledResult и сохраняется как audit evidence. Этот lifecycle относится именно к объекту «Гибридный исполнение» и его собственному type/source contract.
Условия stale: новый broker result, partial fill, deal-history revision или reconciliation revision делает прежний execution aggregate stale.
Authoritative replacement: ReconciledResult, построенный из broker result, confirmed deals и current position snapshot.
Допустимые операции: агрегирование broker outcomes, привязка OrderTicket/DealTicket, reconciliation и формирование ExecutionResult.
Запрещённые подмены: HybridExecution нельзя подменять ApprovedPlan, request acceptance, отдельный DealTicket либо диагностический State.
Связанные сущности: ApprovedPlan, ExecutionRequest, ExecutionResult, ReconciledResult; тип EXECUTION_OBJECT, class REQUESTED/EXECUTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: OBJECT
Creation event: HybridExecution создаётся при отправке ExecutionRequest из ApprovedPlan.
Validation event: HybridExecution проверяется по EXECUTION_OBJECT schema, PlanFingerprint, tickets, deal identity и cycle scope.
Freeze/confirmation event: submitted ExecutionRequest immutable; confirmed deals immutable; aggregate финализируется ReconciledResult.
Mutation events: broker response, partial fills и confirmed deal aggregation создают новые execution revisions.
Stale triggers: broker/deal/position revision после зафиксированного execution snapshot.
Replacement source: ReconciledResult из broker result, deal history и current position snapshot.
Terminal condition: full reconciliation подтверждает complete/partial/rejected outcome.
Persistence behavior: request, broker result и deal identities сохраняются как audit evidence; projected plan не записывается как actual ledger.
Restart behavior: после restart execution восстанавливается по order/deal history и current position reconciliation.
Отличие от: HybridExecution отличается от ApprovedPlan наличием broker/deal evidence, а от ExecutionResult — объединением request, outcomes и reconciliation lifecycle.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Execution lifecycle clauses разделяются с ExecutionRequest/Result; HybridExecution является aggregate полного Hybrid execution scope.
Evidence: mapping record `HybridExecution` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### InitialBuy
CanonicalName: `InitialBuy`
Русское название: Начальная покупка
Краткое определение: InitialBuy — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Начальная покупка»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: InitialBuy
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для InitialBuy.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: InitialBuy назначается approved role rule и связывается с position identity. InitialBuy меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку InitialBuy stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Начальная покупка» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку InitialBuy stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: InitialBuy нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: InitialBuy, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: ROLE
Lifecycle class: ROLE
Creation event: InitialBuy назначается approved role rule и связывается с position identity.
Validation event: Связка InitialBuy проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: InitialBuy меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку InitialBuy stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: InitialBuy отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ROLE`; запись `InitialBuy` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `InitialBuy` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### InitialSell
CanonicalName: `InitialSell`
Русское название: Начальная продажа
Краткое определение: InitialSell — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Начальная продажа»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: InitialSell
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для InitialSell.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: InitialSell назначается approved role rule и связывается с position identity. InitialSell меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку InitialSell stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Начальная продажа» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку InitialSell stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: InitialSell нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: InitialSell, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: ROLE
Lifecycle class: ROLE
Creation event: InitialSell назначается approved role rule и связывается с position identity.
Validation event: Связка InitialSell проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: InitialSell меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку InitialSell stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: InitialSell отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ROLE`; запись `InitialSell` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `InitialSell` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### InitialProfitLeg
CanonicalName: `InitialProfitLeg`
Русское название: Начальная прибыль leg
Краткое определение: InitialProfitLeg — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Начальная прибыль leg»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: InitialProfitLeg
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для InitialProfitLeg.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: InitialProfitLeg назначается approved role rule и связывается с position identity. InitialProfitLeg меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку InitialProfitLeg stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Начальная прибыль leg» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку InitialProfitLeg stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: InitialProfitLeg нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: InitialProfitLeg, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: ROLE
Lifecycle class: ROLE
Creation event: InitialProfitLeg назначается approved role rule и связывается с position identity.
Validation event: Связка InitialProfitLeg проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: InitialProfitLeg меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку InitialProfitLeg stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: InitialProfitLeg отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ROLE`; запись `InitialProfitLeg` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `InitialProfitLeg` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### InitialLosingLeg
CanonicalName: `InitialLosingLeg`
Русское название: Начальная убыточная leg
Краткое определение: InitialLosingLeg — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Начальная убыточная leg»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: InitialLosingLeg
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для InitialLosingLeg.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: InitialLosingLeg назначается approved role rule и связывается с position identity. InitialLosingLeg меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку InitialLosingLeg stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Начальная убыточная leg» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку InitialLosingLeg stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: InitialLosingLeg нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: InitialLosingLeg, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: ROLE
Lifecycle class: ROLE
Creation event: InitialLosingLeg назначается approved role rule и связывается с position identity.
Validation event: Связка InitialLosingLeg проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: InitialLosingLeg меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку InitialLosingLeg stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: InitialLosingLeg отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ROLE`; запись `InitialLosingLeg` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `InitialLosingLeg` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### InitialIgnoredProfit
CanonicalName: `InitialIgnoredProfit`
Русское название: Начальная исключённая прибыль
Краткое определение: InitialIgnoredProfit — Подтверждённый signed net закрытия прибыльной initial leg, сохранённый только как диагностика и исключённый из Reserve и RecoveryPL decision money. Отличительный объект записи: «Начальная исключённая прибыль»; его authoritative provenance — «confirmed closing deal aggregation of InitialProfitLeg filtered by Symbol+Magic+CycleID+position identity».
Архитектурный профиль: Role-qualified architecture
Торговая роль: InitialIgnoredProfit
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: signed
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed closing deal aggregation of InitialProfitLeg filtered by Symbol+Magic+CycleID+position identity
Authoritative source: confirmed closing deal aggregation of InitialProfitLeg filtered by Symbol+Magic+CycleID+position identity
Время фиксации: ACTUAL CONFIRMED stage для InitialIgnoredProfit.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS at ledger/report boundary
Rounding: ROUND_TO_MONEY_DIGITS at ledger/report boundary
Tolerance: `MoneyTolerance`
Lifecycle: InitialIgnoredProfit создаётся confirmed allocation/deal event с уникальным EventID. InitialIgnoredProfit меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Начальная исключённая прибыль» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: InitialIgnoredProfit нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: InitialIgnoredProfit, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::initialIgnoredProfit
Python mapping: Tests/real_recovery_examples_check.py::initial_ignored_profit
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: InitialIgnoredProfit создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: InitialIgnoredProfit проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: InitialIgnoredProfit меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: InitialIgnoredProfit отличается от sibling-терминов источником `confirmed closing deal aggregation of InitialProfitLeg filtered by Symbol+Magic+CycleID+position identity`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `InitialIgnoredProfit` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `InitialIgnoredProfit` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### OldFar
CanonicalName: `OldFar`
Русское название: Предыдущая хвостовая позиция
Краткое определение: OldFar — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Предыдущая хвостовая позиция»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: OldFar
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для OldFar.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: OldFar назначается approved role rule и связывается с position identity. OldFar меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку OldFar stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Предыдущая хвостовая позиция» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку OldFar stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: OldFar нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: OldFar, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: ROLE
Lifecycle class: ROLE
Creation event: OldFar назначается approved role rule и связывается с position identity.
Validation event: Связка OldFar проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: OldFar меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку OldFar stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: OldFar отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ROLE`; запись `OldFar` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `OldFar` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### CurrentFar
CanonicalName: `CurrentFar`
Русское название: Текущая хвостовая позиция
Краткое определение: CurrentFar — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Текущая хвостовая позиция»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: CurrentFar
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для CurrentFar.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: CurrentFar назначается approved role rule и связывается с position identity. CurrentFar меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку CurrentFar stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Текущая хвостовая позиция» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку CurrentFar stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: CurrentFar нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CurrentFar, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: Far
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: ROLE
Lifecycle class: ROLE
Creation event: CurrentFar назначается approved role rule и связывается с position identity.
Validation event: Связка CurrentFar проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: CurrentFar меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку CurrentFar stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: CurrentFar отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ROLE`; запись `CurrentFar` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `CurrentFar` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### ResidualFar
CanonicalName: `ResidualFar`
Русское название: Остаточная хвостовая позиция
Краткое определение: ResidualFar — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Остаточная хвостовая позиция»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: ResidualFar
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для ResidualFar.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: ResidualFar назначается approved role rule и связывается с position identity. ResidualFar меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку ResidualFar stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Остаточная хвостовая позиция» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку ResidualFar stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: ResidualFar нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ResidualFar, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: ROLE
Lifecycle class: ROLE
Creation event: ResidualFar назначается approved role rule и связывается с position identity.
Validation event: Связка ResidualFar проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: ResidualFar меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку ResidualFar stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: ResidualFar отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ROLE`; запись `ResidualFar` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ResidualFar` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### NewFar
CanonicalName: `NewFar`
Русское название: Новая хвостовая позиция
Краткое определение: NewFar — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Новая хвостовая позиция»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: NewFar
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для NewFar.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: NewFar назначается approved role rule и связывается с position identity. NewFar меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку NewFar stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Новая хвостовая позиция» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку NewFar stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: NewFar нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: NewFar, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: ROLE
Lifecycle class: ROLE
Creation event: NewFar назначается approved role rule и связывается с position identity.
Validation event: Связка NewFar проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: NewFar меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку NewFar stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: NewFar отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ROLE`; запись `NewFar` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `NewFar` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### LegacyBigPosition
CanonicalName: `LegacyBigPosition`
Русское название: Устаревшая архитектура компенсирующая позиция позиция
Краткое определение: LegacyBigPosition — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Устаревшая архитектура компенсирующая позиция позиция»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: LegacyBig
Размерность: `POSITION_ID`
Unit: `position reference identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для LegacyBigPosition.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: LegacyBigPosition назначается approved role rule и связывается с position identity. LegacyBigPosition меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку LegacyBigPosition stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Устаревшая архитектура компенсирующая позиция позиция» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку LegacyBigPosition stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: LegacyBigPosition нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: LegacyBig, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/StateMachine.mqh::bigPositionId
Python mapping: NONE_FOUND
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: LegacyBigPosition назначается approved role rule и связывается с position identity.
Validation event: Связка LegacyBigPosition проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: LegacyBigPosition меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку LegacyBigPosition stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: LegacyBigPosition отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `LegacyBigPosition` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `LegacyBigPosition` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### BigCorePosition
CanonicalName: `BigCorePosition`
Русское название: Компенсирующая позиция основная часть позиция
Краткое определение: BigCorePosition — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Компенсирующая позиция основная часть позиция»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: BigCore
Размерность: `POSITION_ID`
Unit: `position reference identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для BigCorePosition.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: BigCorePosition назначается approved role rule и связывается с position identity. BigCorePosition меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку BigCorePosition stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Компенсирующая позиция основная часть позиция» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку BigCorePosition stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: BigCorePosition нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigCore, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/ReconciliationEngine.mqh::ValidateBigCorePosition
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: BigCorePosition назначается approved role rule и связывается с position identity.
Validation event: Связка BigCorePosition проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: BigCorePosition меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку BigCorePosition stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: BigCorePosition отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `BigCorePosition` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `BigCorePosition` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### BigTrendPosition
CanonicalName: `BigTrendPosition`
Русское название: Компенсирующая позиция трендовая часть позиция
Краткое определение: BigTrendPosition — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Компенсирующая позиция трендовая часть позиция»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: BigTrend
Размерность: `POSITION_ID`
Unit: `position reference identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для BigTrendPosition.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: BigTrendPosition назначается approved role rule и связывается с position identity. BigTrendPosition меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку BigTrendPosition stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Компенсирующая позиция трендовая часть позиция» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку BigTrendPosition stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: BigTrendPosition нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigTrend, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/ReconciliationEngine.mqh::ValidateBigTrendPosition
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: BigTrendPosition назначается approved role rule и связывается с position identity.
Validation event: Связка BigTrendPosition проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: BigTrendPosition меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку BigTrendPosition stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: BigTrendPosition отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `BigTrendPosition` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `BigTrendPosition` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### LegacySmallPosition
CanonicalName: `LegacySmallPosition`
Русское название: Устаревшая архитектура защитная позиция позиция
Краткое определение: LegacySmallPosition — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Устаревшая архитектура защитная позиция позиция»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: LegacySmall
Размерность: `POSITION_ID`
Unit: `position reference identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для LegacySmallPosition.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: LegacySmallPosition назначается approved role rule и связывается с position identity. LegacySmallPosition меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку LegacySmallPosition stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Устаревшая архитектура защитная позиция позиция» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку LegacySmallPosition stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: LegacySmallPosition нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: LegacySmall, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/StateMachine.mqh::smallPositionId
Python mapping: NONE_FOUND
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: LegacySmallPosition назначается approved role rule и связывается с position identity.
Validation event: Связка LegacySmallPosition проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: LegacySmallPosition меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку LegacySmallPosition stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: LegacySmallPosition отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `LegacySmallPosition` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `LegacySmallPosition` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### SmallBasePosition
CanonicalName: `SmallBasePosition`
Русское название: Защитная позиция базовая позиция
Краткое определение: SmallBasePosition — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Защитная позиция базовая позиция»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: SmallBase
Размерность: `POSITION_ID`
Unit: `position reference identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для SmallBasePosition.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: SmallBasePosition назначается approved role rule и связывается с position identity. SmallBasePosition меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку SmallBasePosition stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Защитная позиция базовая позиция» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку SmallBasePosition stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: SmallBasePosition нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SmallBase, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/ReconciliationEngine.mqh::ValidateSmallBasePosition
Python mapping: Tests/unit/test_split_exact_persistence_model.py::small_base_id
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: SmallBasePosition назначается approved role rule и связывается с position identity.
Validation event: Связка SmallBasePosition проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: SmallBasePosition меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку SmallBasePosition stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: SmallBasePosition отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `SmallBasePosition` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `SmallBasePosition` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### ManagedPosition
CanonicalName: `ManagedPosition`
Русское название: Управляемая позиция
Краткое определение: ManagedPosition — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Управляемая позиция»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: ManagedPosition
Размерность: `POSITION_ID`
Unit: `position reference identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для ManagedPosition.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: ManagedPosition назначается approved role rule и связывается с position identity. ManagedPosition меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку ManagedPosition stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Управляемая позиция» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку ManagedPosition stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: ManagedPosition нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ManagedPosition, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/PositionUtils.mqh::IsManagedPositionForMagic
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: ManagedPosition назначается approved role rule и связывается с position identity.
Validation event: Связка ManagedPosition проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: ManagedPosition меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку ManagedPosition stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: ManagedPosition отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `ManagedPosition` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ManagedPosition` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### UnmanagedPosition
CanonicalName: `UnmanagedPosition`
Русское название: Неуправляемая позиция
Краткое определение: UnmanagedPosition — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Неуправляемая позиция»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: UnmanagedPosition
Размерность: `POSITION_ID`
Unit: `position reference identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для UnmanagedPosition.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: UnmanagedPosition назначается approved role rule и связывается с position identity. UnmanagedPosition меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку UnmanagedPosition stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Неуправляемая позиция» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку UnmanagedPosition stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: UnmanagedPosition нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: UnmanagedPosition, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: UnmanagedPosition назначается approved role rule и связывается с position identity.
Validation event: Связка UnmanagedPosition проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: UnmanagedPosition меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку UnmanagedPosition stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: UnmanagedPosition отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `UnmanagedPosition` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `UnmanagedPosition` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### ForeignCyclePosition
CanonicalName: `ForeignCyclePosition`
Русское название: Чужая цикл позиция
Краткое определение: ForeignCyclePosition — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Чужая цикл позиция»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: ForeignCyclePosition
Размерность: `POSITION_ID`
Unit: `position reference identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для ForeignCyclePosition.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: ForeignCyclePosition назначается approved role rule и связывается с position identity. ForeignCyclePosition меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку ForeignCyclePosition stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Чужая цикл позиция» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку ForeignCyclePosition stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: ForeignCyclePosition нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ForeignCyclePosition, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: ForeignCyclePosition назначается approved role rule и связывается с position identity.
Validation event: Связка ForeignCyclePosition проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: ForeignCyclePosition меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку ForeignCyclePosition stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: ForeignCyclePosition отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `ForeignCyclePosition` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ForeignCyclePosition` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### FarDirection
CanonicalName: `FarDirection`
Русское название: Хвостовая позиция направление
Краткое определение: FarDirection — Абсолютный BUY/SELL type текущей подтверждённой Far position, считанный из reconciled position snapshot. Отличительный объект записи: «Хвостовая позиция направление»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: Far
Размерность: `DIRECTION_ENUM`
Unit: `BUY/SELL enum`
Знак: not numeric
Допустимый диапазон: соответствует типу `DIRECTION_ENUM`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED or POLICY DERIVED stage для FarDirection.
Projected/Actual class: `ACTUAL CONFIRMED or POLICY DERIVED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: FarDirection вычисляется из snapshot inputs: reconciled MT5 position identity and role mapping. Не мутирует; изменение inputs создаёт новую revision FarDirection. Market, symbol, config или snapshot revision делает FarDirection stale. пересчёт FarDirection на новом immutable snapshot. После execution projected FarDirection завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Хвостовая позиция направление» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает FarDirection stale.
Authoritative replacement: пересчёт FarDirection на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `DIRECTION_ENUM` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: FarDirection нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Far, тип DIRECTION_ENUM, class ACTUAL CONFIRMED or POLICY DERIVED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::farDirection
Python mapping: Tools/hybrid_small_state_machine.py::direction
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: OBJECT
Creation event: FarDirection вычисляется из snapshot inputs: reconciled MT5 position identity and role mapping.
Validation event: FarDirection валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: FarDirection замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision FarDirection.
Stale triggers: Market, symbol, config или snapshot revision делает FarDirection stale.
Replacement source: пересчёт FarDirection на новом immutable snapshot.
Terminal condition: После execution projected FarDirection завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: FarDirection отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED or POLICY DERIVED` и стадией lifecycle `OBJECT`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `OBJECT`; запись `FarDirection` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `FarDirection` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### OppositeFarDirection
CanonicalName: `OppositeFarDirection`
Русское название: Противоположное хвостовая позиция направление
Краткое определение: OppositeFarDirection — Детерминированная инверсия FarDirection по таблице BUY→SELL и SELL→BUY. Отличительный объект записи: «Противоположное хвостовая позиция направление»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: OppositeFarDirection
Размерность: `DIRECTION_ENUM`
Unit: `BUY/SELL enum`
Знак: not numeric
Допустимый диапазон: соответствует типу `DIRECTION_ENUM`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED or POLICY DERIVED stage для OppositeFarDirection.
Projected/Actual class: `ACTUAL CONFIRMED or POLICY DERIVED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: OppositeFarDirection вычисляется из snapshot inputs: reconciled MT5 position identity and role mapping. Не мутирует; изменение inputs создаёт новую revision OppositeFarDirection. Market, symbol, config или snapshot revision делает OppositeFarDirection stale. пересчёт OppositeFarDirection на новом immutable snapshot. После execution projected OppositeFarDirection завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Противоположное хвостовая позиция направление» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает OppositeFarDirection stale.
Authoritative replacement: пересчёт OppositeFarDirection на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `DIRECTION_ENUM` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: OppositeFarDirection нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: OppositeFarDirection, тип DIRECTION_ENUM, class ACTUAL CONFIRMED or POLICY DERIVED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::farDirection
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: OBJECT
Creation event: OppositeFarDirection вычисляется из snapshot inputs: reconciled MT5 position identity and role mapping.
Validation event: OppositeFarDirection валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: OppositeFarDirection замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision OppositeFarDirection.
Stale triggers: Market, symbol, config или snapshot revision делает OppositeFarDirection stale.
Replacement source: пересчёт OppositeFarDirection на новом immutable snapshot.
Terminal condition: После execution projected OppositeFarDirection завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: OppositeFarDirection отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED or POLICY DERIVED` и стадией lifecycle `OBJECT`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `OBJECT`; запись `OppositeFarDirection` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `OppositeFarDirection` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### SameAsFarDirection
CanonicalName: `SameAsFarDirection`
Русское название: Совпадающее с хвостовая позиция направление
Краткое определение: SameAsFarDirection — Детерминированное относительное направление, равное FarDirection; не требует чтения отдельной позиции. Отличительный объект записи: «Совпадающее с хвостовая позиция направление»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: SameAsFarDirection
Размерность: `DIRECTION_ENUM`
Unit: `BUY/SELL enum`
Знак: not numeric
Допустимый диапазон: соответствует типу `DIRECTION_ENUM`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED or POLICY DERIVED stage для SameAsFarDirection.
Projected/Actual class: `ACTUAL CONFIRMED or POLICY DERIVED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: SameAsFarDirection вычисляется из snapshot inputs: reconciled MT5 position identity and role mapping. Не мутирует; изменение inputs создаёт новую revision SameAsFarDirection. Market, symbol, config или snapshot revision делает SameAsFarDirection stale. пересчёт SameAsFarDirection на новом immutable snapshot. После execution projected SameAsFarDirection завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Совпадающее с хвостовая позиция направление» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает SameAsFarDirection stale.
Authoritative replacement: пересчёт SameAsFarDirection на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `DIRECTION_ENUM` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: SameAsFarDirection нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SameAsFarDirection, тип DIRECTION_ENUM, class ACTUAL CONFIRMED or POLICY DERIVED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::farDirection
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: OBJECT
Creation event: SameAsFarDirection вычисляется из snapshot inputs: reconciled MT5 position identity and role mapping.
Validation event: SameAsFarDirection валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: SameAsFarDirection замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision SameAsFarDirection.
Stale triggers: Market, symbol, config или snapshot revision делает SameAsFarDirection stale.
Replacement source: пересчёт SameAsFarDirection на новом immutable snapshot.
Terminal condition: После execution projected SameAsFarDirection завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: SameAsFarDirection отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED or POLICY DERIVED` и стадией lifecycle `OBJECT`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `OBJECT`; запись `SameAsFarDirection` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `SameAsFarDirection` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### BigDirection
CanonicalName: `BigDirection`
Русское название: Компенсирующая позиция направление
Краткое определение: BigDirection — Role-policy direction для LegacyBig или Hybrid BigCore/BigTrend относительно Far; требует architecture qualifier. Отличительный объект записи: «Компенсирующая позиция направление»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: BigDirection
Размерность: `DIRECTION_ENUM`
Unit: `BUY/SELL enum`
Знак: not numeric
Допустимый диапазон: соответствует типу `DIRECTION_ENUM`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED or POLICY DERIVED stage для BigDirection.
Projected/Actual class: `ACTUAL CONFIRMED or POLICY DERIVED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: BigDirection вычисляется из snapshot inputs: reconciled MT5 position identity and role mapping. Не мутирует; изменение inputs создаёт новую revision BigDirection. Market, symbol, config или snapshot revision делает BigDirection stale. пересчёт BigDirection на новом immutable snapshot. После execution projected BigDirection завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Компенсирующая позиция направление» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает BigDirection stale.
Authoritative replacement: пересчёт BigDirection на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `DIRECTION_ENUM` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: BigDirection нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigDirection, тип DIRECTION_ENUM, class ACTUAL CONFIRMED or POLICY DERIVED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::bigDirection
Python mapping: Tools/hybrid_small_state_machine.py::direction
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: OBJECT
Creation event: BigDirection вычисляется из snapshot inputs: reconciled MT5 position identity and role mapping.
Validation event: BigDirection валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: BigDirection замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision BigDirection.
Stale triggers: Market, symbol, config или snapshot revision делает BigDirection stale.
Replacement source: пересчёт BigDirection на новом immutable snapshot.
Terminal condition: После execution projected BigDirection завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: BigDirection отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED or POLICY DERIVED` и стадией lifecycle `OBJECT`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `OBJECT`; запись `BigDirection` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `BigDirection` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### SmallDirection
CanonicalName: `SmallDirection`
Русское название: Защитная позиция направление
Краткое определение: SmallDirection — Role-policy direction LegacySmall/SmallBase относительно Far; требует architecture qualifier. Отличительный объект записи: «Защитная позиция направление»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: SmallDirection
Размерность: `DIRECTION_ENUM`
Unit: `BUY/SELL enum`
Знак: not numeric
Допустимый диапазон: соответствует типу `DIRECTION_ENUM`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED or POLICY DERIVED stage для SmallDirection.
Projected/Actual class: `ACTUAL CONFIRMED or POLICY DERIVED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: SmallDirection вычисляется из snapshot inputs: reconciled MT5 position identity and role mapping. Не мутирует; изменение inputs создаёт новую revision SmallDirection. Market, symbol, config или snapshot revision делает SmallDirection stale. пересчёт SmallDirection на новом immutable snapshot. После execution projected SmallDirection завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Защитная позиция направление» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает SmallDirection stale.
Authoritative replacement: пересчёт SmallDirection на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `DIRECTION_ENUM` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: SmallDirection нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SmallDirection, тип DIRECTION_ENUM, class ACTUAL CONFIRMED or POLICY DERIVED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::smallDirection
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: OBJECT
Creation event: SmallDirection вычисляется из snapshot inputs: reconciled MT5 position identity and role mapping.
Validation event: SmallDirection валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: SmallDirection замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision SmallDirection.
Stale triggers: Market, symbol, config или snapshot revision делает SmallDirection stale.
Replacement source: пересчёт SmallDirection на новом immutable snapshot.
Terminal condition: После execution projected SmallDirection завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: SmallDirection отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED or POLICY DERIVED` и стадией lifecycle `OBJECT`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `OBJECT`; запись `SmallDirection` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `SmallDirection` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### TrendDirection
CanonicalName: `TrendDirection`
Русское название: Трендовая часть направление
Краткое определение: TrendDirection — Направление BigTrend, вычисленное из FarDirection и утверждённого Hybrid role rule; не берётся из comment. Отличительный объект записи: «Трендовая часть направление»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: TrendDirection
Размерность: `DIRECTION_ENUM`
Unit: `BUY/SELL enum`
Знак: not numeric
Допустимый диапазон: соответствует типу `DIRECTION_ENUM`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED or POLICY DERIVED stage для TrendDirection.
Projected/Actual class: `ACTUAL CONFIRMED or POLICY DERIVED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: TrendDirection вычисляется из snapshot inputs: reconciled MT5 position identity and role mapping. Не мутирует; изменение inputs создаёт новую revision TrendDirection. Market, symbol, config или snapshot revision делает TrendDirection stale. пересчёт TrendDirection на новом immutable snapshot. После execution projected TrendDirection завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Трендовая часть направление» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает TrendDirection stale.
Authoritative replacement: пересчёт TrendDirection на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `DIRECTION_ENUM` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: TrendDirection нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: TrendDirection, тип DIRECTION_ENUM, class ACTUAL CONFIRMED or POLICY DERIVED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: OBJECT
Creation event: TrendDirection вычисляется из snapshot inputs: reconciled MT5 position identity and role mapping.
Validation event: TrendDirection валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: TrendDirection замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision TrendDirection.
Stale triggers: Market, symbol, config или snapshot revision делает TrendDirection stale.
Replacement source: пересчёт TrendDirection на новом immutable snapshot.
Terminal condition: После execution projected TrendDirection завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: TrendDirection отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED or POLICY DERIVED` и стадией lifecycle `OBJECT`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `OBJECT`; запись `TrendDirection` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `TrendDirection` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### ReverseDirection
CanonicalName: `ReverseDirection`
Русское название: Разворот направление
Краткое определение: ReverseDirection — Направление следующего reversal role, полученное из подтверждённого transition plan; до approval остаётся projected. Отличительный объект записи: «Разворот направление»; его authoritative provenance — «reconciled MT5 position identity and role mapping».
Архитектурный профиль: Role-qualified architecture
Торговая роль: ReverseDirection
Размерность: `DIRECTION_ENUM`
Unit: `BUY/SELL enum`
Знак: not numeric
Допустимый диапазон: соответствует типу `DIRECTION_ENUM`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED or POLICY DERIVED stage для ReverseDirection.
Projected/Actual class: `ACTUAL CONFIRMED or POLICY DERIVED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: ReverseDirection вычисляется из snapshot inputs: reconciled MT5 position identity and role mapping. Не мутирует; изменение inputs создаёт новую revision ReverseDirection. Market, symbol, config или snapshot revision делает ReverseDirection stale. пересчёт ReverseDirection на новом immutable snapshot. После execution projected ReverseDirection завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Разворот направление» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает ReverseDirection stale.
Authoritative replacement: пересчёт ReverseDirection на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `DIRECTION_ENUM` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: ReverseDirection нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ReverseDirection, тип DIRECTION_ENUM, class ACTUAL CONFIRMED or POLICY DERIVED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: Tests/test_dynamic_reverse_small_direction.py::reverse_direction
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: OBJECT
Creation event: ReverseDirection вычисляется из snapshot inputs: reconciled MT5 position identity and role mapping.
Validation event: ReverseDirection валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: ReverseDirection замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision ReverseDirection.
Stale triggers: Market, symbol, config или snapshot revision делает ReverseDirection stale.
Replacement source: пересчёт ReverseDirection на новом immutable snapshot.
Terminal condition: После execution projected ReverseDirection завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: ReverseDirection отличается от sibling-терминов источником `reconciled MT5 position identity and role mapping`, классом `ACTUAL CONFIRMED or POLICY DERIVED` и стадией lifecycle `OBJECT`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `OBJECT`; запись `ReverseDirection` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ReverseDirection` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=PARTIAL_MATCH.

### RawLot
CanonicalName: `RawLot`
Русское название: Сырой объём в лотах
Краткое определение: RawLot — Ненормализованный объём, непосредственно полученный из исходной математической формулы; отличается от CalculatedLot отсутствием terminal constraints. Отличительный объект записи: «Сырой объём в лотах»; его authoritative provenance — «typed formula + SymbolInfo volume constraints».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: RawLot
Размерность: `LOT_RAW`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_RAW`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для RawLot.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: RawLot вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints. Не мутирует; изменение inputs создаёт новую revision RawLot. Market, symbol, config или snapshot revision делает RawLot stale. пересчёт RawLot на новом immutable snapshot. После execution projected RawLot завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Сырой объём в лотах» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает RawLot stale.
Authoritative replacement: пересчёт RawLot на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_RAW` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: RawLot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RawLot, тип LOT_RAW, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/RecoveryMath.mqh::rawLot
Python mapping: Tests/normalize_volume_to_step_check.py::lot
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: RawLot вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints.
Validation event: RawLot валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: RawLot замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision RawLot.
Stale triggers: Market, symbol, config или snapshot revision делает RawLot stale.
Replacement source: пересчёт RawLot на новом immutable snapshot.
Terminal condition: После execution projected RawLot завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: RawLot отличается от sibling-терминов источником `typed formula + SymbolInfo volume constraints`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `RawLot` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `RawLot` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### CalculatedLot
CanonicalName: `CalculatedLot`
Русское название: Расчётный объём в лотах
Краткое определение: CalculatedLot — Результат role formula до broker volume constraints; отличается от RawLot применёнными formula rules и от NormalizedLot отсутствием min/max/step. Отличительный объект записи: «Расчётный объём в лотах»; его authoritative provenance — «typed formula + SymbolInfo volume constraints».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: CalculatedLot
Размерность: `LOT_CALCULATED`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_CALCULATED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для CalculatedLot.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: CalculatedLot вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints. Не мутирует; изменение inputs создаёт новую revision CalculatedLot. Market, symbol, config или snapshot revision делает CalculatedLot stale. пересчёт CalculatedLot на новом immutable snapshot. После execution projected CalculatedLot завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Расчётный объём в лотах» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает CalculatedLot stale.
Authoritative replacement: пересчёт CalculatedLot на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_CALCULATED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: CalculatedLot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CalculatedLot, тип LOT_CALCULATED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: CalculatedLot вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints.
Validation event: CalculatedLot валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: CalculatedLot замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision CalculatedLot.
Stale triggers: Market, symbol, config или snapshot revision делает CalculatedLot stale.
Replacement source: пересчёт CalculatedLot на новом immutable snapshot.
Terminal condition: После execution projected CalculatedLot завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: CalculatedLot отличается от sibling-терминов источником `typed formula + SymbolInfo volume constraints`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `CalculatedLot` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `CalculatedLot` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### NormalizedLot
CanonicalName: `NormalizedLot`
Русское название: Нормализованный объём в лотах
Краткое определение: NormalizedLot — CalculatedLot после Symbol volume min/max/step и named rounding policy; ещё не является requested или filled volume. Отличительный объект записи: «Нормализованный объём в лотах»; его authoritative provenance — «typed formula + SymbolInfo volume constraints».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: NormalizedLot
Размерность: `LOT_NORMALIZED`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_NORMALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для NormalizedLot.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: NormalizedLot вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints. Не мутирует; изменение inputs создаёт новую revision NormalizedLot. Market, symbol, config или snapshot revision делает NormalizedLot stale. пересчёт NormalizedLot на новом immutable snapshot. После execution projected NormalizedLot завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Нормализованный объём в лотах» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает NormalizedLot stale.
Authoritative replacement: пересчёт NormalizedLot на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_NORMALIZED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: NormalizedLot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: NormalizedLot, тип LOT_NORMALIZED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/ReconciliationEngine.mqh::normalizedCtxLot
Python mapping: NONE_FOUND
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: NormalizedLot вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints.
Validation event: NormalizedLot валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: NormalizedLot замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision NormalizedLot.
Stale triggers: Market, symbol, config или snapshot revision делает NormalizedLot stale.
Replacement source: пересчёт NormalizedLot на новом immutable snapshot.
Terminal condition: После execution projected NormalizedLot завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: NormalizedLot отличается от sibling-терминов источником `typed formula + SymbolInfo volume constraints`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `NormalizedLot` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `NormalizedLot` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### RequestedLot
CanonicalName: `RequestedLot`
Русское название: Запрошенный объём в лотах
Краткое определение: RequestedLot — Frozen NormalizedLot, помещённый в один trade request; не доказывает FilledLot. Отличительный объект записи: «Запрошенный объём в лотах»; его authoritative provenance — «approved immutable plan».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: RequestedLot
Размерность: `LOT_REQUESTED`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_REQUESTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved immutable plan
Authoritative source: approved immutable plan
Время фиксации: REQUESTED stage для RequestedLot.
Projected/Actual class: `REQUESTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: RequestedLot создаётся из ApprovedPlan непосредственно перед отправкой request. Не мутирует; broker создаёт отдельное execution evidence. PlanFingerprint mismatch, reject или новый request делает RequestedLot непригодным. FilledLot/ExecutionResult, затем reconciled actual state. Завершается broker outcome: fill, partial fill или reject. Этот lifecycle относится именно к объекту «Запрошенный объём в лотах» и его собственному type/source contract.
Условия stale: PlanFingerprint mismatch, reject или новый request делает RequestedLot непригодным.
Authoritative replacement: FilledLot/ExecutionResult, затем reconciled actual state.
Допустимые операции: сравнение и преобразование только по `LOT_REQUESTED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: RequestedLot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RequestedLot, тип LOT_REQUESTED, class REQUESTED.
Legacy aliases: —
MQL5 mapping: Include/SimulationEngine.mqh::requestedLot
Python mapping: Tests/unit/test_money_completion_behavior.py::requested
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: REQUESTED
Creation event: RequestedLot создаётся из ApprovedPlan непосредственно перед отправкой request.
Validation event: RequestedLot сверяется с plan fingerprint и broker constraints.
Freeze/confirmation event: Отправленное значение RequestedLot неизменно для данного request identity.
Mutation events: Не мутирует; broker создаёт отдельное execution evidence.
Stale triggers: PlanFingerprint mismatch, reject или новый request делает RequestedLot непригодным.
Replacement source: FilledLot/ExecutionResult, затем reconciled actual state.
Terminal condition: Завершается broker outcome: fill, partial fill или reject.
Persistence behavior: Сохраняется только как audit evidence request, не как actual.
Restart behavior: После restart подтверждается по order/deal history.
Отличие от: RequestedLot отличается от sibling-терминов источником `approved immutable plan`, классом `REQUESTED` и стадией lifecycle `REQUESTED`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `REQUESTED`; запись `RequestedLot` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `RequestedLot` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### FilledLot
CanonicalName: `FilledLot`
Русское название: Исполненный объём в лотах
Краткое определение: FilledLot — Сумма подтверждённых deal volumes данного request/event; не равна ActualPositionLot без position reconciliation. Отличительный объект записи: «Исполненный объём в лотах»; его authoritative provenance — «confirmed deals/trade result».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: FilledLot
Размерность: `LOT_FILLED`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_FILLED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deals/trade result
Authoritative source: confirmed deals/trade result
Время фиксации: CONFIRMED stage для FilledLot.
Projected/Actual class: `CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: FilledLot возникает только из подтверждённого deal event. Несколько partial fills агрегируются без изменения исходных deals. Новая выборка history делает прежний aggregate FilledLot stale, но не отдельный deal. повторно построенный aggregate confirmed deal history. Финализируется после полного сбора fills для execution scope. Этот lifecycle относится именно к объекту «Исполненный объём в лотах» и его собственному type/source contract.
Условия stale: Новая выборка history делает прежний aggregate FilledLot stale, но не отдельный deal.
Authoritative replacement: повторно построенный aggregate confirmed deal history.
Допустимые операции: сравнение и преобразование только по `LOT_FILLED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: FilledLot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: FilledLot, тип LOT_FILLED, class CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/SimulationEngine.mqh::filledLot
Python mapping: Tests/unit/test_big_small_behavior.py::filled
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: DEAL
Creation event: FilledLot возникает только из подтверждённого deal event.
Validation event: FilledLot проверяется фильтрами Symbol, MagicNumber, CycleID и deal/position identity.
Freeze/confirmation event: Deal evidence для FilledLot неизменно после подтверждения истории.
Mutation events: Несколько partial fills агрегируются без изменения исходных deals.
Stale triggers: Новая выборка history делает прежний aggregate FilledLot stale, но не отдельный deal.
Replacement source: повторно построенный aggregate confirmed deal history.
Terminal condition: Финализируется после полного сбора fills для execution scope.
Persistence behavior: Persisted audit ссылается на DealTicket/EventID exactly once.
Restart behavior: После restart реконструируется из confirmed deal history.
Отличие от: FilledLot отличается от sibling-терминов источником `confirmed deals/trade result`, классом `CONFIRMED` и стадией lifecycle `DEAL`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `DEAL`; запись `FilledLot` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `FilledLot` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### ActualPositionLot
CanonicalName: `ActualPositionLot`
Русское название: Фактический позиция объём в лотах
Краткое определение: ActualPositionLot — Текущий terminal position volume после reconciliation; повторная normalization запрещена. Отличительный объект записи: «Фактический позиция объём в лотах»; его authoritative provenance — «current MT5 position snapshot».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: ActualPositionLot
Размерность: `LOT_POSITION_ACTUAL`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_POSITION_ACTUAL`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: current MT5 position snapshot
Authoritative source: current MT5 position snapshot
Время фиксации: ACTUAL CURRENT stage для ActualPositionLot.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: ActualPositionLot появляется при чтении текущего MT5 position snapshot. Любое исполнение, partial close или position merge изменяет ActualPositionLot. Любой trade event после snapshot немедленно делает ActualPositionLot stale. новый current MT5 position snapshot. После полного закрытия становится ZERO либо NOT_APPLICABLE согласно типу. Этот lifecycle относится именно к объекту «Фактический позиция объём в лотах» и его собственному type/source contract.
Условия stale: Любой trade event после snapshot немедленно делает ActualPositionLot stale.
Authoritative replacement: новый current MT5 position snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_POSITION_ACTUAL` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: ActualPositionLot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ActualPositionLot, тип LOT_POSITION_ACTUAL, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::actualPositionLot
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: ACTUAL_POSITION
Creation event: ActualPositionLot появляется при чтении текущего MT5 position snapshot.
Validation event: ActualPositionLot валидируется по managed identity и revision снимка.
Freeze/confirmation event: Фиксация относится только к конкретному snapshot revision.
Mutation events: Любое исполнение, partial close или position merge изменяет ActualPositionLot.
Stale triggers: Любой trade event после snapshot немедленно делает ActualPositionLot stale.
Replacement source: новый current MT5 position snapshot.
Terminal condition: После полного закрытия становится ZERO либо NOT_APPLICABLE согласно типу.
Persistence behavior: Live значение не заменяется persisted cache.
Restart behavior: После restart обязательно перечитывается из terminal state.
Отличие от: ActualPositionLot отличается от sibling-терминов источником `current MT5 position snapshot`, классом `ACTUAL CURRENT` и стадией lifecycle `ACTUAL_POSITION`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ACTUAL_POSITION`; запись `ActualPositionLot` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ActualPositionLot` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### ResidualLotProjected
CanonicalName: `ResidualLotProjected`
Русское название: Остаточная объём в лотах прогнозный
Краткое определение: ResidualLotProjected — Плановый остаток до execution, вычисленный из requested close; не может назначать actual role. Отличительный объект записи: «Остаточная объём в лотах прогнозный»; его authoritative provenance — «typed formula + SymbolInfo volume constraints».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: ResidualLotProjected
Размерность: `LOT_RESIDUAL`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_RESIDUAL`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для ResidualLotProjected.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: ResidualLotProjected вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints. Не мутирует; изменение inputs создаёт новую revision ResidualLotProjected. Market, symbol, config или snapshot revision делает ResidualLotProjected stale. пересчёт ResidualLotProjected на новом immutable snapshot. После execution projected ResidualLotProjected завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Остаточная объём в лотах прогнозный» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает ResidualLotProjected stale.
Authoritative replacement: пересчёт ResidualLotProjected на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_RESIDUAL` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: ResidualLotProjected нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ResidualLotProjected, тип LOT_RESIDUAL, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: ResidualLotProjected вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints.
Validation event: ResidualLotProjected валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: ResidualLotProjected замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision ResidualLotProjected.
Stale triggers: Market, symbol, config или snapshot revision делает ResidualLotProjected stale.
Replacement source: пересчёт ResidualLotProjected на новом immutable snapshot.
Terminal condition: После execution projected ResidualLotProjected завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: ResidualLotProjected отличается от sibling-терминов источником `typed formula + SymbolInfo volume constraints`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `ResidualLotProjected` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ResidualLotProjected` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### ResidualLotActual
CanonicalName: `ResidualLotActual`
Русское название: Остаточная объём в лотах фактический
Краткое определение: ResidualLotActual — Остаток текущей позиции после confirmed fills и reconciliation; заменяет projected residual. Отличительный объект записи: «Остаточная объём в лотах фактический»; его authoritative provenance — «current MT5 position snapshot».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: ResidualLotActual
Размерность: `LOT_POSITION_ACTUAL`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_POSITION_ACTUAL`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: current MT5 position snapshot
Authoritative source: current MT5 position snapshot
Время фиксации: ACTUAL CURRENT stage для ResidualLotActual.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: ResidualLotActual появляется при чтении текущего MT5 position snapshot. Любое исполнение, partial close или position merge изменяет ResidualLotActual. Любой trade event после snapshot немедленно делает ResidualLotActual stale. новый current MT5 position snapshot. После полного закрытия становится ZERO либо NOT_APPLICABLE согласно типу. Этот lifecycle относится именно к объекту «Остаточная объём в лотах фактический» и его собственному type/source contract.
Условия stale: Любой trade event после snapshot немедленно делает ResidualLotActual stale.
Authoritative replacement: новый current MT5 position snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_POSITION_ACTUAL` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: ResidualLotActual нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ResidualLotActual, тип LOT_POSITION_ACTUAL, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: ACTUAL_POSITION
Creation event: ResidualLotActual появляется при чтении текущего MT5 position snapshot.
Validation event: ResidualLotActual валидируется по managed identity и revision снимка.
Freeze/confirmation event: Фиксация относится только к конкретному snapshot revision.
Mutation events: Любое исполнение, partial close или position merge изменяет ResidualLotActual.
Stale triggers: Любой trade event после snapshot немедленно делает ResidualLotActual stale.
Replacement source: новый current MT5 position snapshot.
Terminal condition: После полного закрытия становится ZERO либо NOT_APPLICABLE согласно типу.
Persistence behavior: Live значение не заменяется persisted cache.
Restart behavior: После restart обязательно перечитывается из terminal state.
Отличие от: ResidualLotActual отличается от sibling-терминов источником `current MT5 position snapshot`, классом `ACTUAL CURRENT` и стадией lifecycle `ACTUAL_POSITION`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ACTUAL_POSITION`; запись `ResidualLotActual` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ResidualLotActual` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### FarLotRaw
CanonicalName: `FarLotRaw`
Русское название: Хвостовая позиция объём в лотах сырой
Краткое определение: FarLotRaw — объём `Far` на стадии до broker normalization; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence. Отличительный объект записи: «Хвостовая позиция объём в лотах сырой»; его authoritative provenance — «typed formula + SymbolInfo volume constraints».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: Far
Размерность: `LOT_RAW`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_RAW`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для FarLotRaw.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: FarLotRaw вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints. Не мутирует; изменение inputs создаёт новую revision FarLotRaw. Market, symbol, config или snapshot revision делает FarLotRaw stale. пересчёт FarLotRaw на новом immutable snapshot. После execution projected FarLotRaw завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Хвостовая позиция объём в лотах сырой» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает FarLotRaw stale.
Authoritative replacement: пересчёт FarLotRaw на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_RAW` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: FarLotRaw нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Far, тип LOT_RAW, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Logger.mqh::closeFarLotRaw
Python mapping: Tools/optimize_big_scenario_min_levels.py::close_far_lot_raw
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: FarLotRaw вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints.
Validation event: FarLotRaw валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: FarLotRaw замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision FarLotRaw.
Stale triggers: Market, symbol, config или snapshot revision делает FarLotRaw stale.
Replacement source: пересчёт FarLotRaw на новом immutable snapshot.
Terminal condition: После execution projected FarLotRaw завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: FarLotRaw отличается от sibling-терминов источником `typed formula + SymbolInfo volume constraints`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `FarLotRaw` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `FarLotRaw` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### FarLotCalculated
CanonicalName: `FarLotCalculated`
Русское название: Хвостовая позиция объём в лотах расчётный
Краткое определение: FarLotCalculated — объём `Far` на стадии после роли/formula до terminal constraints; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence. Отличительный объект записи: «Хвостовая позиция объём в лотах расчётный»; его authoritative provenance — «typed formula + SymbolInfo volume constraints».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: Far
Размерность: `LOT_CALCULATED`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_CALCULATED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для FarLotCalculated.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: FarLotCalculated вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints. Не мутирует; изменение inputs создаёт новую revision FarLotCalculated. Market, symbol, config или snapshot revision делает FarLotCalculated stale. пересчёт FarLotCalculated на новом immutable snapshot. После execution projected FarLotCalculated завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Хвостовая позиция объём в лотах расчётный» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает FarLotCalculated stale.
Authoritative replacement: пересчёт FarLotCalculated на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_CALCULATED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: FarLotCalculated нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Far, тип LOT_CALCULATED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::farLotAfter
Python mapping: Tools/optimize_big_scenario_min_levels.py::FarLotAfter
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: FarLotCalculated вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints.
Validation event: FarLotCalculated валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: FarLotCalculated замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision FarLotCalculated.
Stale triggers: Market, symbol, config или snapshot revision делает FarLotCalculated stale.
Replacement source: пересчёт FarLotCalculated на новом immutable snapshot.
Terminal condition: После execution projected FarLotCalculated завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: FarLotCalculated отличается от sibling-терминов источником `typed formula + SymbolInfo volume constraints`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `FarLotCalculated` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `FarLotCalculated` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### FarLotNormalized
CanonicalName: `FarLotNormalized`
Русское название: Хвостовая позиция объём в лотах нормализованный
Краткое определение: FarLotNormalized — объём `Far` на стадии после min/max/step и profile rounding; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence. Отличительный объект записи: «Хвостовая позиция объём в лотах нормализованный»; его authoritative provenance — «typed formula + SymbolInfo volume constraints».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: Far
Размерность: `LOT_NORMALIZED`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_NORMALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для FarLotNormalized.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: FarLotNormalized вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints. Не мутирует; изменение inputs создаёт новую revision FarLotNormalized. Market, symbol, config или snapshot revision делает FarLotNormalized stale. пересчёт FarLotNormalized на новом immutable snapshot. После execution projected FarLotNormalized завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Хвостовая позиция объём в лотах нормализованный» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает FarLotNormalized stale.
Authoritative replacement: пересчёт FarLotNormalized на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_NORMALIZED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: FarLotNormalized нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Far, тип LOT_NORMALIZED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: FarLotNormalized вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints.
Validation event: FarLotNormalized валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: FarLotNormalized замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision FarLotNormalized.
Stale triggers: Market, symbol, config или snapshot revision делает FarLotNormalized stale.
Replacement source: пересчёт FarLotNormalized на новом immutable snapshot.
Terminal condition: После execution projected FarLotNormalized завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: FarLotNormalized отличается от sibling-терминов источником `typed formula + SymbolInfo volume constraints`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `FarLotNormalized` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `FarLotNormalized` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### FarLotRequested
CanonicalName: `FarLotRequested`
Русское название: Хвостовая позиция объём в лотах запрошенный
Краткое определение: FarLotRequested — объём `Far` на стадии после freeze approved plan и отправки request; он отличается от соседних lot stages источником `approved immutable plan` и не может использоваться как их evidence. Отличительный объект записи: «Хвостовая позиция объём в лотах запрошенный»; его authoritative provenance — «approved immutable plan».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: Far
Размерность: `LOT_REQUESTED`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_REQUESTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved immutable plan
Authoritative source: approved immutable plan
Время фиксации: REQUESTED stage для FarLotRequested.
Projected/Actual class: `REQUESTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: FarLotRequested создаётся из ApprovedPlan непосредственно перед отправкой request. Не мутирует; broker создаёт отдельное execution evidence. PlanFingerprint mismatch, reject или новый request делает FarLotRequested непригодным. FilledLot/ExecutionResult, затем reconciled actual state. Завершается broker outcome: fill, partial fill или reject. Этот lifecycle относится именно к объекту «Хвостовая позиция объём в лотах запрошенный» и его собственному type/source contract.
Условия stale: PlanFingerprint mismatch, reject или новый request делает FarLotRequested непригодным.
Authoritative replacement: FilledLot/ExecutionResult, затем reconciled actual state.
Допустимые операции: сравнение и преобразование только по `LOT_REQUESTED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: FarLotRequested нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Far, тип LOT_REQUESTED, class REQUESTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: Tools/hybrid_geometry_model.py::far_lot
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: REQUESTED
Creation event: FarLotRequested создаётся из ApprovedPlan непосредственно перед отправкой request.
Validation event: FarLotRequested сверяется с plan fingerprint и broker constraints.
Freeze/confirmation event: Отправленное значение FarLotRequested неизменно для данного request identity.
Mutation events: Не мутирует; broker создаёт отдельное execution evidence.
Stale triggers: PlanFingerprint mismatch, reject или новый request делает FarLotRequested непригодным.
Replacement source: FilledLot/ExecutionResult, затем reconciled actual state.
Terminal condition: Завершается broker outcome: fill, partial fill или reject.
Persistence behavior: Сохраняется только как audit evidence request, не как actual.
Restart behavior: После restart подтверждается по order/deal history.
Отличие от: FarLotRequested отличается от sibling-терминов источником `approved immutable plan`, классом `REQUESTED` и стадией lifecycle `REQUESTED`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `REQUESTED`; запись `FarLotRequested` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `FarLotRequested` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=PARTIAL_MATCH.

### FarLotFilled
CanonicalName: `FarLotFilled`
Русское название: Хвостовая позиция объём в лотах исполненный
Краткое определение: FarLotFilled — объём `Far` на стадии после aggregation подтверждённых deals; он отличается от соседних lot stages источником `confirmed deals/trade result` и не может использоваться как их evidence. Отличительный объект записи: «Хвостовая позиция объём в лотах исполненный»; его authoritative provenance — «confirmed deals/trade result».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: Far
Размерность: `LOT_FILLED`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_FILLED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deals/trade result
Authoritative source: confirmed deals/trade result
Время фиксации: CONFIRMED stage для FarLotFilled.
Projected/Actual class: `CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: FarLotFilled возникает только из подтверждённого deal event. Несколько partial fills агрегируются без изменения исходных deals. Новая выборка history делает прежний aggregate FarLotFilled stale, но не отдельный deal. повторно построенный aggregate confirmed deal history. Финализируется после полного сбора fills для execution scope. Этот lifecycle относится именно к объекту «Хвостовая позиция объём в лотах исполненный» и его собственному type/source contract.
Условия stale: Новая выборка history делает прежний aggregate FarLotFilled stale, но не отдельный deal.
Authoritative replacement: повторно построенный aggregate confirmed deal history.
Допустимые операции: сравнение и преобразование только по `LOT_FILLED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: FarLotFilled нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Far, тип LOT_FILLED, class CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::farLot
Python mapping: Tools/hybrid_geometry_model.py::far_lot
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: DEAL
Creation event: FarLotFilled возникает только из подтверждённого deal event.
Validation event: FarLotFilled проверяется фильтрами Symbol, MagicNumber, CycleID и deal/position identity.
Freeze/confirmation event: Deal evidence для FarLotFilled неизменно после подтверждения истории.
Mutation events: Несколько partial fills агрегируются без изменения исходных deals.
Stale triggers: Новая выборка history делает прежний aggregate FarLotFilled stale, но не отдельный deal.
Replacement source: повторно построенный aggregate confirmed deal history.
Terminal condition: Финализируется после полного сбора fills для execution scope.
Persistence behavior: Persisted audit ссылается на DealTicket/EventID exactly once.
Restart behavior: После restart реконструируется из confirmed deal history.
Отличие от: FarLotFilled отличается от sibling-терминов источником `confirmed deals/trade result`, классом `CONFIRMED` и стадией lifecycle `DEAL`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `DEAL`; запись `FarLotFilled` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `FarLotFilled` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### FarLotActual
CanonicalName: `FarLotActual`
Русское название: Хвостовая позиция объём в лотах фактический
Краткое определение: FarLotActual — объём `Far` на стадии из текущего reconciled position/deal snapshot; он отличается от соседних lot stages источником `current MT5 position snapshot` и не может использоваться как их evidence. Отличительный объект записи: «Хвостовая позиция объём в лотах фактический»; его authoritative provenance — «current MT5 position snapshot».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: Far
Размерность: `LOT_POSITION_ACTUAL`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_POSITION_ACTUAL`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: current MT5 position snapshot
Authoritative source: current MT5 position snapshot
Время фиксации: ACTUAL CURRENT stage для FarLotActual.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: FarLotActual появляется при чтении текущего MT5 position snapshot. Любое исполнение, partial close или position merge изменяет FarLotActual. Любой trade event после snapshot немедленно делает FarLotActual stale. новый current MT5 position snapshot. После полного закрытия становится ZERO либо NOT_APPLICABLE согласно типу. Этот lifecycle относится именно к объекту «Хвостовая позиция объём в лотах фактический» и его собственному type/source contract.
Условия stale: Любой trade event после snapshot немедленно делает FarLotActual stale.
Authoritative replacement: новый current MT5 position snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_POSITION_ACTUAL` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: FarLotActual нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Far, тип LOT_POSITION_ACTUAL, class ACTUAL CURRENT.
Legacy aliases: FarLot, Ctx.farLot
MQL5 mapping: Include/Types.mqh::farLot
Python mapping: Tools/hybrid_geometry_model.py::far_lot
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: ACTUAL_POSITION
Creation event: FarLotActual появляется при чтении текущего MT5 position snapshot.
Validation event: FarLotActual валидируется по managed identity и revision снимка.
Freeze/confirmation event: Фиксация относится только к конкретному snapshot revision.
Mutation events: Любое исполнение, partial close или position merge изменяет FarLotActual.
Stale triggers: Любой trade event после snapshot немедленно делает FarLotActual stale.
Replacement source: новый current MT5 position snapshot.
Terminal condition: После полного закрытия становится ZERO либо NOT_APPLICABLE согласно типу.
Persistence behavior: Live значение не заменяется persisted cache.
Restart behavior: После restart обязательно перечитывается из terminal state.
Отличие от: FarLotActual отличается от sibling-терминов источником `current MT5 position snapshot`, классом `ACTUAL CURRENT` и стадией lifecycle `ACTUAL_POSITION`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ACTUAL_POSITION`; запись `FarLotActual` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `FarLotActual` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### BigCoreLotRaw
CanonicalName: `BigCoreLotRaw`
Русское название: Компенсирующая позиция основная часть объём в лотах сырой
Краткое определение: BigCoreLotRaw — объём `BigCore` на стадии до broker normalization; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence. Отличительный объект записи: «Компенсирующая позиция основная часть объём в лотах сырой»; его authoritative provenance — «typed formula + SymbolInfo volume constraints».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: BigCore
Размерность: `LOT_RAW`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_RAW`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для BigCoreLotRaw.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: BigCoreLotRaw вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints. Не мутирует; изменение inputs создаёт новую revision BigCoreLotRaw. Market, symbol, config или snapshot revision делает BigCoreLotRaw stale. пересчёт BigCoreLotRaw на новом immutable snapshot. После execution projected BigCoreLotRaw завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Компенсирующая позиция основная часть объём в лотах сырой» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает BigCoreLotRaw stale.
Authoritative replacement: пересчёт BigCoreLotRaw на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_RAW` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: BigCoreLotRaw нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigCore, тип LOT_RAW, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Logger.mqh::closeBigLotRaw
Python mapping: Tools/hybrid_geometry_model.py::core_lot
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: BigCoreLotRaw вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints.
Validation event: BigCoreLotRaw валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: BigCoreLotRaw замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision BigCoreLotRaw.
Stale triggers: Market, symbol, config или snapshot revision делает BigCoreLotRaw stale.
Replacement source: пересчёт BigCoreLotRaw на новом immutable snapshot.
Terminal condition: После execution projected BigCoreLotRaw завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: BigCoreLotRaw отличается от sibling-терминов источником `typed formula + SymbolInfo volume constraints`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `BigCoreLotRaw` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `BigCoreLotRaw` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### BigCoreLotNormalized
CanonicalName: `BigCoreLotNormalized`
Русское название: Компенсирующая позиция основная часть объём в лотах нормализованный
Краткое определение: BigCoreLotNormalized — объём `BigCore` на стадии после min/max/step и profile rounding; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence. Отличительный объект записи: «Компенсирующая позиция основная часть объём в лотах нормализованный»; его authoritative provenance — «typed formula + SymbolInfo volume constraints».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: BigCore
Размерность: `LOT_NORMALIZED`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_NORMALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для BigCoreLotNormalized.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: BigCoreLotNormalized вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints. Не мутирует; изменение inputs создаёт новую revision BigCoreLotNormalized. Market, symbol, config или snapshot revision делает BigCoreLotNormalized stale. пересчёт BigCoreLotNormalized на новом immutable snapshot. После execution projected BigCoreLotNormalized завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Компенсирующая позиция основная часть объём в лотах нормализованный» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает BigCoreLotNormalized stale.
Authoritative replacement: пересчёт BigCoreLotNormalized на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_NORMALIZED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: BigCoreLotNormalized нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigCore, тип LOT_NORMALIZED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: BigCoreLotNormalized вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints.
Validation event: BigCoreLotNormalized валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: BigCoreLotNormalized замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision BigCoreLotNormalized.
Stale triggers: Market, symbol, config или snapshot revision делает BigCoreLotNormalized stale.
Replacement source: пересчёт BigCoreLotNormalized на новом immutable snapshot.
Terminal condition: После execution projected BigCoreLotNormalized завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: BigCoreLotNormalized отличается от sibling-терминов источником `typed formula + SymbolInfo volume constraints`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `BigCoreLotNormalized` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `BigCoreLotNormalized` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### BigCoreLotRequested
CanonicalName: `BigCoreLotRequested`
Русское название: Компенсирующая позиция основная часть объём в лотах запрошенный
Краткое определение: BigCoreLotRequested — объём `BigCore` на стадии после freeze approved plan и отправки request; он отличается от соседних lot stages источником `approved immutable plan` и не может использоваться как их evidence. Отличительный объект записи: «Компенсирующая позиция основная часть объём в лотах запрошенный»; его authoritative provenance — «approved immutable plan».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: BigCore
Размерность: `LOT_REQUESTED`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_REQUESTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved immutable plan
Authoritative source: approved immutable plan
Время фиксации: REQUESTED stage для BigCoreLotRequested.
Projected/Actual class: `REQUESTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: BigCoreLotRequested создаётся из ApprovedPlan непосредственно перед отправкой request. Не мутирует; broker создаёт отдельное execution evidence. PlanFingerprint mismatch, reject или новый request делает BigCoreLotRequested непригодным. FilledLot/ExecutionResult, затем reconciled actual state. Завершается broker outcome: fill, partial fill или reject. Этот lifecycle относится именно к объекту «Компенсирующая позиция основная часть объём в лотах запрошенный» и его собственному type/source contract.
Условия stale: PlanFingerprint mismatch, reject или новый request делает BigCoreLotRequested непригодным.
Authoritative replacement: FilledLot/ExecutionResult, затем reconciled actual state.
Допустимые операции: сравнение и преобразование только по `LOT_REQUESTED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: BigCoreLotRequested нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigCore, тип LOT_REQUESTED, class REQUESTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: REQUESTED
Creation event: BigCoreLotRequested создаётся из ApprovedPlan непосредственно перед отправкой request.
Validation event: BigCoreLotRequested сверяется с plan fingerprint и broker constraints.
Freeze/confirmation event: Отправленное значение BigCoreLotRequested неизменно для данного request identity.
Mutation events: Не мутирует; broker создаёт отдельное execution evidence.
Stale triggers: PlanFingerprint mismatch, reject или новый request делает BigCoreLotRequested непригодным.
Replacement source: FilledLot/ExecutionResult, затем reconciled actual state.
Terminal condition: Завершается broker outcome: fill, partial fill или reject.
Persistence behavior: Сохраняется только как audit evidence request, не как actual.
Restart behavior: После restart подтверждается по order/deal history.
Отличие от: BigCoreLotRequested отличается от sibling-терминов источником `approved immutable plan`, классом `REQUESTED` и стадией lifecycle `REQUESTED`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `REQUESTED`; запись `BigCoreLotRequested` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `BigCoreLotRequested` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### BigCoreLotFilled
CanonicalName: `BigCoreLotFilled`
Русское название: Компенсирующая позиция основная часть объём в лотах исполненный
Краткое определение: BigCoreLotFilled — объём `BigCore` на стадии после aggregation подтверждённых deals; он отличается от соседних lot stages источником `confirmed deals/trade result` и не может использоваться как их evidence. Отличительный объект записи: «Компенсирующая позиция основная часть объём в лотах исполненный»; его authoritative provenance — «confirmed deals/trade result».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: BigCore
Размерность: `LOT_FILLED`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_FILLED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deals/trade result
Authoritative source: confirmed deals/trade result
Время фиксации: CONFIRMED stage для BigCoreLotFilled.
Projected/Actual class: `CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: BigCoreLotFilled возникает только из подтверждённого deal event. Несколько partial fills агрегируются без изменения исходных deals. Новая выборка history делает прежний aggregate BigCoreLotFilled stale, но не отдельный deal. повторно построенный aggregate confirmed deal history. Финализируется после полного сбора fills для execution scope. Этот lifecycle относится именно к объекту «Компенсирующая позиция основная часть объём в лотах исполненный» и его собственному type/source contract.
Условия stale: Новая выборка history делает прежний aggregate BigCoreLotFilled stale, но не отдельный deal.
Authoritative replacement: повторно построенный aggregate confirmed deal history.
Допустимые операции: сравнение и преобразование только по `LOT_FILLED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: BigCoreLotFilled нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigCore, тип LOT_FILLED, class CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: DEAL
Creation event: BigCoreLotFilled возникает только из подтверждённого deal event.
Validation event: BigCoreLotFilled проверяется фильтрами Symbol, MagicNumber, CycleID и deal/position identity.
Freeze/confirmation event: Deal evidence для BigCoreLotFilled неизменно после подтверждения истории.
Mutation events: Несколько partial fills агрегируются без изменения исходных deals.
Stale triggers: Новая выборка history делает прежний aggregate BigCoreLotFilled stale, но не отдельный deal.
Replacement source: повторно построенный aggregate confirmed deal history.
Terminal condition: Финализируется после полного сбора fills для execution scope.
Persistence behavior: Persisted audit ссылается на DealTicket/EventID exactly once.
Restart behavior: После restart реконструируется из confirmed deal history.
Отличие от: BigCoreLotFilled отличается от sibling-терминов источником `confirmed deals/trade result`, классом `CONFIRMED` и стадией lifecycle `DEAL`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `DEAL`; запись `BigCoreLotFilled` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `BigCoreLotFilled` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### BigCoreLotActual
CanonicalName: `BigCoreLotActual`
Русское название: Компенсирующая позиция основная часть объём в лотах фактический
Краткое определение: BigCoreLotActual — объём `BigCore` на стадии из текущего reconciled position/deal snapshot; он отличается от соседних lot stages источником `current MT5 position snapshot` и не может использоваться как их evidence. Отличительный объект записи: «Компенсирующая позиция основная часть объём в лотах фактический»; его authoritative provenance — «current MT5 position snapshot».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: BigCore
Размерность: `LOT_POSITION_ACTUAL`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_POSITION_ACTUAL`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: current MT5 position snapshot
Authoritative source: current MT5 position snapshot
Время фиксации: ACTUAL CURRENT stage для BigCoreLotActual.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: BigCoreLotActual появляется при чтении текущего MT5 position snapshot. Любое исполнение, partial close или position merge изменяет BigCoreLotActual. Любой trade event после snapshot немедленно делает BigCoreLotActual stale. новый current MT5 position snapshot. После полного закрытия становится ZERO либо NOT_APPLICABLE согласно типу. Этот lifecycle относится именно к объекту «Компенсирующая позиция основная часть объём в лотах фактический» и его собственному type/source contract.
Условия stale: Любой trade event после snapshot немедленно делает BigCoreLotActual stale.
Authoritative replacement: новый current MT5 position snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_POSITION_ACTUAL` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: BigCoreLotActual нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigCore, тип LOT_POSITION_ACTUAL, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: ACTUAL_POSITION
Creation event: BigCoreLotActual появляется при чтении текущего MT5 position snapshot.
Validation event: BigCoreLotActual валидируется по managed identity и revision снимка.
Freeze/confirmation event: Фиксация относится только к конкретному snapshot revision.
Mutation events: Любое исполнение, partial close или position merge изменяет BigCoreLotActual.
Stale triggers: Любой trade event после snapshot немедленно делает BigCoreLotActual stale.
Replacement source: новый current MT5 position snapshot.
Terminal condition: После полного закрытия становится ZERO либо NOT_APPLICABLE согласно типу.
Persistence behavior: Live значение не заменяется persisted cache.
Restart behavior: После restart обязательно перечитывается из terminal state.
Отличие от: BigCoreLotActual отличается от sibling-терминов источником `current MT5 position snapshot`, классом `ACTUAL CURRENT` и стадией lifecycle `ACTUAL_POSITION`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ACTUAL_POSITION`; запись `BigCoreLotActual` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `BigCoreLotActual` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### BigTrendLotRaw
CanonicalName: `BigTrendLotRaw`
Русское название: Компенсирующая позиция трендовая часть объём в лотах сырой
Краткое определение: BigTrendLotRaw — объём `BigTrend` на стадии до broker normalization; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence. Отличительный объект записи: «Компенсирующая позиция трендовая часть объём в лотах сырой»; его authoritative provenance — «typed formula + SymbolInfo volume constraints».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: BigTrend
Размерность: `LOT_RAW`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_RAW`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для BigTrendLotRaw.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: BigTrendLotRaw вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints. Не мутирует; изменение inputs создаёт новую revision BigTrendLotRaw. Market, symbol, config или snapshot revision делает BigTrendLotRaw stale. пересчёт BigTrendLotRaw на новом immutable snapshot. После execution projected BigTrendLotRaw завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Компенсирующая позиция трендовая часть объём в лотах сырой» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает BigTrendLotRaw stale.
Authoritative replacement: пересчёт BigTrendLotRaw на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_RAW` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: BigTrendLotRaw нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigTrend, тип LOT_RAW, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::trendLot
Python mapping: Tools/hybrid_geometry_model.py::trend_lot
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: BigTrendLotRaw вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints.
Validation event: BigTrendLotRaw валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: BigTrendLotRaw замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision BigTrendLotRaw.
Stale triggers: Market, symbol, config или snapshot revision делает BigTrendLotRaw stale.
Replacement source: пересчёт BigTrendLotRaw на новом immutable snapshot.
Terminal condition: После execution projected BigTrendLotRaw завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: BigTrendLotRaw отличается от sibling-терминов источником `typed formula + SymbolInfo volume constraints`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `BigTrendLotRaw` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `BigTrendLotRaw` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### BigTrendLotNormalized
CanonicalName: `BigTrendLotNormalized`
Русское название: Компенсирующая позиция трендовая часть объём в лотах нормализованный
Краткое определение: BigTrendLotNormalized — объём `BigTrend` на стадии после min/max/step и profile rounding; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence. Отличительный объект записи: «Компенсирующая позиция трендовая часть объём в лотах нормализованный»; его authoritative provenance — «typed formula + SymbolInfo volume constraints».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: BigTrend
Размерность: `LOT_NORMALIZED`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_NORMALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для BigTrendLotNormalized.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: BigTrendLotNormalized вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints. Не мутирует; изменение inputs создаёт новую revision BigTrendLotNormalized. Market, symbol, config или snapshot revision делает BigTrendLotNormalized stale. пересчёт BigTrendLotNormalized на новом immutable snapshot. После execution projected BigTrendLotNormalized завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Компенсирующая позиция трендовая часть объём в лотах нормализованный» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает BigTrendLotNormalized stale.
Authoritative replacement: пересчёт BigTrendLotNormalized на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_NORMALIZED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: BigTrendLotNormalized нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigTrend, тип LOT_NORMALIZED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: BigTrendLotNormalized вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints.
Validation event: BigTrendLotNormalized валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: BigTrendLotNormalized замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision BigTrendLotNormalized.
Stale triggers: Market, symbol, config или snapshot revision делает BigTrendLotNormalized stale.
Replacement source: пересчёт BigTrendLotNormalized на новом immutable snapshot.
Terminal condition: После execution projected BigTrendLotNormalized завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: BigTrendLotNormalized отличается от sibling-терминов источником `typed formula + SymbolInfo volume constraints`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `BigTrendLotNormalized` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `BigTrendLotNormalized` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### SmallBaseLotRaw
CanonicalName: `SmallBaseLotRaw`
Русское название: Защитная позиция базовая объём в лотах сырой
Краткое определение: SmallBaseLotRaw — объём `SmallBase` на стадии до broker normalization; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence. Отличительный объект записи: «Защитная позиция базовая объём в лотах сырой»; его authoritative provenance — «typed formula + SymbolInfo volume constraints».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: SmallBase
Размерность: `LOT_RAW`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_RAW`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для SmallBaseLotRaw.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: SmallBaseLotRaw вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints. Не мутирует; изменение inputs создаёт новую revision SmallBaseLotRaw. Market, symbol, config или snapshot revision делает SmallBaseLotRaw stale. пересчёт SmallBaseLotRaw на новом immutable snapshot. После execution projected SmallBaseLotRaw завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Защитная позиция базовая объём в лотах сырой» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает SmallBaseLotRaw stale.
Authoritative replacement: пересчёт SmallBaseLotRaw на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_RAW` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: SmallBaseLotRaw нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SmallBase, тип LOT_RAW, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::smallLot
Python mapping: Tools/hybrid_geometry_model.py::small_lot
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: SmallBaseLotRaw вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints.
Validation event: SmallBaseLotRaw валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: SmallBaseLotRaw замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision SmallBaseLotRaw.
Stale triggers: Market, symbol, config или snapshot revision делает SmallBaseLotRaw stale.
Replacement source: пересчёт SmallBaseLotRaw на новом immutable snapshot.
Terminal condition: После execution projected SmallBaseLotRaw завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: SmallBaseLotRaw отличается от sibling-терминов источником `typed formula + SymbolInfo volume constraints`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `SmallBaseLotRaw` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `SmallBaseLotRaw` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### SmallBaseLotNormalized
CanonicalName: `SmallBaseLotNormalized`
Русское название: Защитная позиция базовая объём в лотах нормализованный
Краткое определение: SmallBaseLotNormalized — объём `SmallBase` на стадии после min/max/step и profile rounding; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence. Отличительный объект записи: «Защитная позиция базовая объём в лотах нормализованный»; его authoritative provenance — «typed formula + SymbolInfo volume constraints».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: SmallBase
Размерность: `LOT_NORMALIZED`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_NORMALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для SmallBaseLotNormalized.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: SmallBaseLotNormalized вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints. Не мутирует; изменение inputs создаёт новую revision SmallBaseLotNormalized. Market, symbol, config или snapshot revision делает SmallBaseLotNormalized stale. пересчёт SmallBaseLotNormalized на новом immutable snapshot. После execution projected SmallBaseLotNormalized завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Защитная позиция базовая объём в лотах нормализованный» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает SmallBaseLotNormalized stale.
Authoritative replacement: пересчёт SmallBaseLotNormalized на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_NORMALIZED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: SmallBaseLotNormalized нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SmallBase, тип LOT_NORMALIZED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: SmallBaseLotNormalized вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints.
Validation event: SmallBaseLotNormalized валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: SmallBaseLotNormalized замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision SmallBaseLotNormalized.
Stale triggers: Market, symbol, config или snapshot revision делает SmallBaseLotNormalized stale.
Replacement source: пересчёт SmallBaseLotNormalized на новом immutable snapshot.
Terminal condition: После execution projected SmallBaseLotNormalized завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: SmallBaseLotNormalized отличается от sibling-терминов источником `typed formula + SymbolInfo volume constraints`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `SmallBaseLotNormalized` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `SmallBaseLotNormalized` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### PartialFarCloseLotCalculated
CanonicalName: `PartialFarCloseLotCalculated`
Русское название: Частичный хвостовая позиция закрытие объём в лотах расчётный
Краткое определение: PartialFarCloseLotCalculated — объём `PartialFarClose` на стадии после роли/formula до terminal constraints; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence. Отличительный объект записи: «Частичный хвостовая позиция закрытие объём в лотах расчётный»; его authoritative provenance — «typed formula + SymbolInfo volume constraints».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: PartialFarClose
Размерность: `LOT_CALCULATED`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_CALCULATED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для PartialFarCloseLotCalculated.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: PartialFarCloseLotCalculated вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints. Не мутирует; изменение inputs создаёт новую revision PartialFarCloseLotCalculated. Market, symbol, config или snapshot revision делает PartialFarCloseLotCalculated stale. пересчёт PartialFarCloseLotCalculated на новом immutable snapshot. После execution projected PartialFarCloseLotCalculated завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Частичный хвостовая позиция закрытие объём в лотах расчётный» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает PartialFarCloseLotCalculated stale.
Authoritative replacement: пересчёт PartialFarCloseLotCalculated на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_CALCULATED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: PartialFarCloseLotCalculated нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PartialFarClose, тип LOT_CALCULATED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: PartialFarCloseLotCalculated вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints.
Validation event: PartialFarCloseLotCalculated валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: PartialFarCloseLotCalculated замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision PartialFarCloseLotCalculated.
Stale triggers: Market, symbol, config или snapshot revision делает PartialFarCloseLotCalculated stale.
Replacement source: пересчёт PartialFarCloseLotCalculated на новом immutable snapshot.
Terminal condition: После execution projected PartialFarCloseLotCalculated завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: PartialFarCloseLotCalculated отличается от sibling-терминов источником `typed formula + SymbolInfo volume constraints`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `PartialFarCloseLotCalculated` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `PartialFarCloseLotCalculated` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### PartialFarCloseLotNormalized
CanonicalName: `PartialFarCloseLotNormalized`
Русское название: Частичный хвостовая позиция закрытие объём в лотах нормализованный
Краткое определение: PartialFarCloseLotNormalized — объём `PartialFarClose` на стадии после min/max/step и profile rounding; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence. Отличительный объект записи: «Частичный хвостовая позиция закрытие объём в лотах нормализованный»; его authoritative provenance — «typed formula + SymbolInfo volume constraints».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: PartialFarClose
Размерность: `LOT_NORMALIZED`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_NORMALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для PartialFarCloseLotNormalized.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: PartialFarCloseLotNormalized вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints. Не мутирует; изменение inputs создаёт новую revision PartialFarCloseLotNormalized. Market, symbol, config или snapshot revision делает PartialFarCloseLotNormalized stale. пересчёт PartialFarCloseLotNormalized на новом immutable snapshot. После execution projected PartialFarCloseLotNormalized завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Частичный хвостовая позиция закрытие объём в лотах нормализованный» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает PartialFarCloseLotNormalized stale.
Authoritative replacement: пересчёт PartialFarCloseLotNormalized на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_NORMALIZED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: PartialFarCloseLotNormalized нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PartialFarClose, тип LOT_NORMALIZED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: PartialFarCloseLotNormalized вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints.
Validation event: PartialFarCloseLotNormalized валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: PartialFarCloseLotNormalized замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision PartialFarCloseLotNormalized.
Stale triggers: Market, symbol, config или snapshot revision делает PartialFarCloseLotNormalized stale.
Replacement source: пересчёт PartialFarCloseLotNormalized на новом immutable snapshot.
Terminal condition: После execution projected PartialFarCloseLotNormalized завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: PartialFarCloseLotNormalized отличается от sibling-терминов источником `typed formula + SymbolInfo volume constraints`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `PartialFarCloseLotNormalized` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `PartialFarCloseLotNormalized` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### PartialFarCloseLotRequested
CanonicalName: `PartialFarCloseLotRequested`
Русское название: Частичный хвостовая позиция закрытие объём в лотах запрошенный
Краткое определение: PartialFarCloseLotRequested — объём `PartialFarClose` на стадии после freeze approved plan и отправки request; он отличается от соседних lot stages источником `approved immutable plan` и не может использоваться как их evidence. Отличительный объект записи: «Частичный хвостовая позиция закрытие объём в лотах запрошенный»; его authoritative provenance — «approved immutable plan».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: PartialFarClose
Размерность: `LOT_REQUESTED`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_REQUESTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved immutable plan
Authoritative source: approved immutable plan
Время фиксации: REQUESTED stage для PartialFarCloseLotRequested.
Projected/Actual class: `REQUESTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: PartialFarCloseLotRequested создаётся из ApprovedPlan непосредственно перед отправкой request. Не мутирует; broker создаёт отдельное execution evidence. PlanFingerprint mismatch, reject или новый request делает PartialFarCloseLotRequested непригодным. FilledLot/ExecutionResult, затем reconciled actual state. Завершается broker outcome: fill, partial fill или reject. Этот lifecycle относится именно к объекту «Частичный хвостовая позиция закрытие объём в лотах запрошенный» и его собственному type/source contract.
Условия stale: PlanFingerprint mismatch, reject или новый request делает PartialFarCloseLotRequested непригодным.
Authoritative replacement: FilledLot/ExecutionResult, затем reconciled actual state.
Допустимые операции: сравнение и преобразование только по `LOT_REQUESTED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: PartialFarCloseLotRequested нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PartialFarClose, тип LOT_REQUESTED, class REQUESTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: REQUESTED
Creation event: PartialFarCloseLotRequested создаётся из ApprovedPlan непосредственно перед отправкой request.
Validation event: PartialFarCloseLotRequested сверяется с plan fingerprint и broker constraints.
Freeze/confirmation event: Отправленное значение PartialFarCloseLotRequested неизменно для данного request identity.
Mutation events: Не мутирует; broker создаёт отдельное execution evidence.
Stale triggers: PlanFingerprint mismatch, reject или новый request делает PartialFarCloseLotRequested непригодным.
Replacement source: FilledLot/ExecutionResult, затем reconciled actual state.
Terminal condition: Завершается broker outcome: fill, partial fill или reject.
Persistence behavior: Сохраняется только как audit evidence request, не как actual.
Restart behavior: После restart подтверждается по order/deal history.
Отличие от: PartialFarCloseLotRequested отличается от sibling-терминов источником `approved immutable plan`, классом `REQUESTED` и стадией lifecycle `REQUESTED`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `REQUESTED`; запись `PartialFarCloseLotRequested` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `PartialFarCloseLotRequested` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### PartialFarCloseLotFilled
CanonicalName: `PartialFarCloseLotFilled`
Русское название: Частичный хвостовая позиция закрытие объём в лотах исполненный
Краткое определение: PartialFarCloseLotFilled — объём `PartialFarClose` на стадии после aggregation подтверждённых deals; он отличается от соседних lot stages источником `confirmed deals/trade result` и не может использоваться как их evidence. Отличительный объект записи: «Частичный хвостовая позиция закрытие объём в лотах исполненный»; его authoritative provenance — «confirmed deals/trade result».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: PartialFarClose
Размерность: `LOT_FILLED`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_FILLED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deals/trade result
Authoritative source: confirmed deals/trade result
Время фиксации: CONFIRMED stage для PartialFarCloseLotFilled.
Projected/Actual class: `CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: PartialFarCloseLotFilled возникает только из подтверждённого deal event. Несколько partial fills агрегируются без изменения исходных deals. Новая выборка history делает прежний aggregate PartialFarCloseLotFilled stale, но не отдельный deal. повторно построенный aggregate confirmed deal history. Финализируется после полного сбора fills для execution scope. Этот lifecycle относится именно к объекту «Частичный хвостовая позиция закрытие объём в лотах исполненный» и его собственному type/source contract.
Условия stale: Новая выборка history делает прежний aggregate PartialFarCloseLotFilled stale, но не отдельный deal.
Authoritative replacement: повторно построенный aggregate confirmed deal history.
Допустимые операции: сравнение и преобразование только по `LOT_FILLED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: PartialFarCloseLotFilled нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PartialFarClose, тип LOT_FILLED, class CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: DEAL
Creation event: PartialFarCloseLotFilled возникает только из подтверждённого deal event.
Validation event: PartialFarCloseLotFilled проверяется фильтрами Symbol, MagicNumber, CycleID и deal/position identity.
Freeze/confirmation event: Deal evidence для PartialFarCloseLotFilled неизменно после подтверждения истории.
Mutation events: Несколько partial fills агрегируются без изменения исходных deals.
Stale triggers: Новая выборка history делает прежний aggregate PartialFarCloseLotFilled stale, но не отдельный deal.
Replacement source: повторно построенный aggregate confirmed deal history.
Terminal condition: Финализируется после полного сбора fills для execution scope.
Persistence behavior: Persisted audit ссылается на DealTicket/EventID exactly once.
Restart behavior: После restart реконструируется из confirmed deal history.
Отличие от: PartialFarCloseLotFilled отличается от sibling-терминов источником `confirmed deals/trade result`, классом `CONFIRMED` и стадией lifecycle `DEAL`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `DEAL`; запись `PartialFarCloseLotFilled` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `PartialFarCloseLotFilled` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### FarResidualProjected
CanonicalName: `FarResidualProjected`
Русское название: Хвостовая позиция остаточная прогнозный
Краткое определение: FarResidualProjected — объём `FarResidual` на стадии в read-only preview; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence. Отличительный объект записи: «Хвостовая позиция остаточная прогнозный»; его authoritative provenance — «typed formula + SymbolInfo volume constraints».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: FarResidual
Размерность: `LOT_RESIDUAL`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_RESIDUAL`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для FarResidualProjected.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: FarResidualProjected вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints. Не мутирует; изменение inputs создаёт новую revision FarResidualProjected. Market, symbol, config или snapshot revision делает FarResidualProjected stale. пересчёт FarResidualProjected на новом immutable snapshot. После execution projected FarResidualProjected завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Хвостовая позиция остаточная прогнозный» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает FarResidualProjected stale.
Authoritative replacement: пересчёт FarResidualProjected на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_RESIDUAL` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: FarResidualProjected нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: FarResidual, тип LOT_RESIDUAL, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: FarResidualProjected вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints.
Validation event: FarResidualProjected валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: FarResidualProjected замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision FarResidualProjected.
Stale triggers: Market, symbol, config или snapshot revision делает FarResidualProjected stale.
Replacement source: пересчёт FarResidualProjected на новом immutable snapshot.
Terminal condition: После execution projected FarResidualProjected завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: FarResidualProjected отличается от sibling-терминов источником `typed formula + SymbolInfo volume constraints`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `FarResidualProjected` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `FarResidualProjected` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### FarResidualActual
CanonicalName: `FarResidualActual`
Русское название: Хвостовая позиция остаточная фактический
Краткое определение: FarResidualActual — объём `FarResidual` на стадии из текущего reconciled position/deal snapshot; он отличается от соседних lot stages источником `current MT5 position snapshot` и не может использоваться как их evidence. Отличительный объект записи: «Хвостовая позиция остаточная фактический»; его authoritative provenance — «current MT5 position snapshot».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: FarResidual
Размерность: `LOT_POSITION_ACTUAL`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_POSITION_ACTUAL`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: current MT5 position snapshot
Authoritative source: current MT5 position snapshot
Время фиксации: ACTUAL CURRENT stage для FarResidualActual.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: FarResidualActual появляется при чтении текущего MT5 position snapshot. Любое исполнение, partial close или position merge изменяет FarResidualActual. Любой trade event после snapshot немедленно делает FarResidualActual stale. новый current MT5 position snapshot. После полного закрытия становится ZERO либо NOT_APPLICABLE согласно типу. Этот lifecycle относится именно к объекту «Хвостовая позиция остаточная фактический» и его собственному type/source contract.
Условия stale: Любой trade event после snapshot немедленно делает FarResidualActual stale.
Authoritative replacement: новый current MT5 position snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_POSITION_ACTUAL` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: FarResidualActual нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: FarResidual, тип LOT_POSITION_ACTUAL, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: LOT_VALUE
Lifecycle class: ACTUAL_POSITION
Creation event: FarResidualActual появляется при чтении текущего MT5 position snapshot.
Validation event: FarResidualActual валидируется по managed identity и revision снимка.
Freeze/confirmation event: Фиксация относится только к конкретному snapshot revision.
Mutation events: Любое исполнение, partial close или position merge изменяет FarResidualActual.
Stale triggers: Любой trade event после snapshot немедленно делает FarResidualActual stale.
Replacement source: новый current MT5 position snapshot.
Terminal condition: После полного закрытия становится ZERO либо NOT_APPLICABLE согласно типу.
Persistence behavior: Live значение не заменяется persisted cache.
Restart behavior: После restart обязательно перечитывается из terminal state.
Отличие от: FarResidualActual отличается от sibling-терминов источником `current MT5 position snapshot`, классом `ACTUAL CURRENT` и стадией lifecycle `ACTUAL_POSITION`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ACTUAL_POSITION`; запись `FarResidualActual` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `FarResidualActual` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### NewFarCandidateLot
CanonicalName: `NewFarCandidateLot`
Русское название: Новая хвостовая позиция кандидат объём в лотах
Краткое определение: NewFarCandidateLot — объём `NewFar` на стадии до approval и execution; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence. Отличительный объект записи: «Новая хвостовая позиция кандидат объём в лотах»; его authoritative provenance — «typed formula + SymbolInfo volume constraints».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: NewFar
Размерность: `LOT_CALCULATED`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_CALCULATED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для NewFarCandidateLot.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: NewFarCandidateLot вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints. Не мутирует; изменение inputs создаёт новую revision NewFarCandidateLot. Market, symbol, config или snapshot revision делает NewFarCandidateLot stale. пересчёт NewFarCandidateLot на новом immutable snapshot. После execution projected NewFarCandidateLot завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Новая хвостовая позиция кандидат объём в лотах» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает NewFarCandidateLot stale.
Authoritative replacement: пересчёт NewFarCandidateLot на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_CALCULATED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: NewFarCandidateLot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: NewFar, тип LOT_CALCULATED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `HSB-DOC-CONFLICT-020`
Resolution stage: `3.1.6 / 3.1.8`
Статус определения: `UNRESOLVED_MODE_ROUTING`
Semantic category: LOT_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: NewFarCandidateLot вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints.
Validation event: NewFarCandidateLot валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: NewFarCandidateLot замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision NewFarCandidateLot.
Stale triggers: Market, symbol, config или snapshot revision делает NewFarCandidateLot stale.
Replacement source: пересчёт NewFarCandidateLot на новом immutable snapshot.
Terminal condition: После execution projected NewFarCandidateLot завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: NewFarCandidateLot отличается от sibling-терминов источником `typed formula + SymbolInfo volume constraints`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `NewFarCandidateLot` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `NewFarCandidateLot` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### NewFarProjectedLot
CanonicalName: `NewFarProjectedLot`
Русское название: Новая хвостовая позиция прогнозный объём в лотах
Краткое определение: NewFarProjectedLot — объём `NewFar` на стадии в read-only preview; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence. Отличительный объект записи: «Новая хвостовая позиция прогнозный объём в лотах»; его authoritative provenance — «typed formula + SymbolInfo volume constraints».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: NewFar
Размерность: `LOT_RAW`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_RAW`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для NewFarProjectedLot.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: NewFarProjectedLot вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints. Не мутирует; изменение inputs создаёт новую revision NewFarProjectedLot. Market, symbol, config или snapshot revision делает NewFarProjectedLot stale. пересчёт NewFarProjectedLot на новом immutable snapshot. После execution projected NewFarProjectedLot завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Новая хвостовая позиция прогнозный объём в лотах» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает NewFarProjectedLot stale.
Authoritative replacement: пересчёт NewFarProjectedLot на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_RAW` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: NewFarProjectedLot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: NewFar, тип LOT_RAW, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::projectedNewFarLot
Python mapping: NONE_FOUND
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`MISSING`
Conflict: `HSB-DOC-CONFLICT-020`
Resolution stage: `3.1.6 / 3.1.8`
Статус определения: `UNRESOLVED_MODE_ROUTING`
Semantic category: LOT_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: NewFarProjectedLot вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints.
Validation event: NewFarProjectedLot валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: NewFarProjectedLot замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision NewFarProjectedLot.
Stale triggers: Market, symbol, config или snapshot revision делает NewFarProjectedLot stale.
Replacement source: пересчёт NewFarProjectedLot на новом immutable snapshot.
Terminal condition: После execution projected NewFarProjectedLot завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: NewFarProjectedLot отличается от sibling-терминов источником `typed formula + SymbolInfo volume constraints`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `NewFarProjectedLot` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `NewFarProjectedLot` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### NewFarNormalizedLot
CanonicalName: `NewFarNormalizedLot`
Русское название: Новая хвостовая позиция нормализованный объём в лотах
Краткое определение: NewFarNormalizedLot — объём `NewFar` на стадии после min/max/step и profile rounding; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence. Отличительный объект записи: «Новая хвостовая позиция нормализованный объём в лотах»; его authoritative provenance — «typed formula + SymbolInfo volume constraints».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: NewFar
Размерность: `LOT_NORMALIZED`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_NORMALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для NewFarNormalizedLot.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: NewFarNormalizedLot вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints. Не мутирует; изменение inputs создаёт новую revision NewFarNormalizedLot. Market, symbol, config или snapshot revision делает NewFarNormalizedLot stale. пересчёт NewFarNormalizedLot на новом immutable snapshot. После execution projected NewFarNormalizedLot завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Новая хвостовая позиция нормализованный объём в лотах» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает NewFarNormalizedLot stale.
Authoritative replacement: пересчёт NewFarNormalizedLot на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_NORMALIZED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: NewFarNormalizedLot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: NewFar, тип LOT_NORMALIZED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `HSB-DOC-CONFLICT-020`
Resolution stage: `3.1.6 / 3.1.8`
Статус определения: `UNRESOLVED_MODE_ROUTING`
Semantic category: LOT_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: NewFarNormalizedLot вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints.
Validation event: NewFarNormalizedLot валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: NewFarNormalizedLot замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision NewFarNormalizedLot.
Stale triggers: Market, symbol, config или snapshot revision делает NewFarNormalizedLot stale.
Replacement source: пересчёт NewFarNormalizedLot на новом immutable snapshot.
Terminal condition: После execution projected NewFarNormalizedLot завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: NewFarNormalizedLot отличается от sibling-терминов источником `typed formula + SymbolInfo volume constraints`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `NewFarNormalizedLot` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `NewFarNormalizedLot` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### NewFarPromotedLot
CanonicalName: `NewFarPromotedLot`
Русское название: Новая хвостовая позиция назначенный объём в лотах
Краткое определение: NewFarPromotedLot — объём `NewFar` на стадии после role validation и persistence; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence. Отличительный объект записи: «Новая хвостовая позиция назначенный объём в лотах»; его authoritative provenance — «typed formula + SymbolInfo volume constraints».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: NewFar
Размерность: `LOT_NORMALIZED`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_NORMALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для NewFarPromotedLot.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: NewFarPromotedLot вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints. Не мутирует; изменение inputs создаёт новую revision NewFarPromotedLot. Market, symbol, config или snapshot revision делает NewFarPromotedLot stale. пересчёт NewFarPromotedLot на новом immutable snapshot. После execution projected NewFarPromotedLot завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Новая хвостовая позиция назначенный объём в лотах» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает NewFarPromotedLot stale.
Authoritative replacement: пересчёт NewFarPromotedLot на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_NORMALIZED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: NewFarPromotedLot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: NewFar, тип LOT_NORMALIZED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `HSB-DOC-CONFLICT-020`
Resolution stage: `3.1.6 / 3.1.8`
Статус определения: `UNRESOLVED_MODE_ROUTING`
Semantic category: LOT_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: NewFarPromotedLot вычисляется из snapshot inputs: typed formula + SymbolInfo volume constraints.
Validation event: NewFarPromotedLot валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: NewFarPromotedLot замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision NewFarPromotedLot.
Stale triggers: Market, symbol, config или snapshot revision делает NewFarPromotedLot stale.
Replacement source: пересчёт NewFarPromotedLot на новом immutable snapshot.
Terminal condition: После execution projected NewFarPromotedLot завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: NewFarPromotedLot отличается от sibling-терминов источником `typed formula + SymbolInfo volume constraints`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `NewFarPromotedLot` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `NewFarPromotedLot` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### NewFarActualLot
CanonicalName: `NewFarActualLot`
Русское название: Новая хвостовая позиция фактический объём в лотах
Краткое определение: NewFarActualLot — объём `NewFar` на стадии из текущего reconciled position/deal snapshot; он отличается от соседних lot stages источником `current MT5 position snapshot` и не может использоваться как их evidence. Отличительный объект записи: «Новая хвостовая позиция фактический объём в лотах»; его authoritative provenance — «current MT5 position snapshot».
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: NewFar
Размерность: `LOT_POSITION_ACTUAL`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_POSITION_ACTUAL`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: current MT5 position snapshot
Authoritative source: current MT5 position snapshot
Время фиксации: ACTUAL CURRENT stage для NewFarActualLot.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: NewFarActualLot появляется при чтении текущего MT5 position snapshot. Любое исполнение, partial close или position merge изменяет NewFarActualLot. Любой trade event после snapshot немедленно делает NewFarActualLot stale. новый current MT5 position snapshot. После полного закрытия становится ZERO либо NOT_APPLICABLE согласно типу. Этот lifecycle относится именно к объекту «Новая хвостовая позиция фактический объём в лотах» и его собственному type/source contract.
Условия stale: Любой trade event после snapshot немедленно делает NewFarActualLot stale.
Authoritative replacement: новый current MT5 position snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_POSITION_ACTUAL` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: NewFarActualLot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: NewFar, тип LOT_POSITION_ACTUAL, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: Include/StateMachine.mqh::actualNewFarLot
Python mapping: Tools/hybrid_small_state_machine.py::actual_new_far_lot
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `HSB-DOC-CONFLICT-020`
Resolution stage: `3.1.6 / 3.1.8`
Статус определения: `UNRESOLVED_MODE_ROUTING`
Semantic category: LOT_VALUE
Lifecycle class: ACTUAL_POSITION
Creation event: NewFarActualLot появляется при чтении текущего MT5 position snapshot.
Validation event: NewFarActualLot валидируется по managed identity и revision снимка.
Freeze/confirmation event: Фиксация относится только к конкретному snapshot revision.
Mutation events: Любое исполнение, partial close или position merge изменяет NewFarActualLot.
Stale triggers: Любой trade event после snapshot немедленно делает NewFarActualLot stale.
Replacement source: новый current MT5 position snapshot.
Terminal condition: После полного закрытия становится ZERO либо NOT_APPLICABLE согласно типу.
Persistence behavior: Live значение не заменяется persisted cache.
Restart behavior: После restart обязательно перечитывается из terminal state.
Отличие от: NewFarActualLot отличается от sibling-терминов источником `current MT5 position snapshot`, классом `ACTUAL CURRENT` и стадией lifecycle `ACTUAL_POSITION`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ACTUAL_POSITION`; запись `NewFarActualLot` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `NewFarActualLot` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### Point
CanonicalName: `Point`
Русское название: Размер пункта
Краткое определение: Point — Размер одного terminal point для конкретного Symbol (`SYMBOL_POINT`); symbol property, а не projected market price и не TickSize. Отличительный объект записи: «Размер пункта»; его authoritative provenance — «SymbolInfoDouble(symbol, SYMBOL_POINT)».
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: Point
Размерность: `PRICE_POINT_SIZE`
Unit: `price per point`
Знак: > 0
Допустимый диапазон: соответствует типу `PRICE_POINT_SIZE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfoDouble(symbol, SYMBOL_POINT)
Authoritative source: SymbolInfoDouble(symbol, SYMBOL_POINT)
Время фиксации: SYMBOL PROPERTY stage для Point.
Projected/Actual class: `SYMBOL PROPERTY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT PROPERTY SNAPSHOT`
Lifecycle: Point считывается вызовом SymbolInfo* при refresh свойств символа. Рыночный tick не изменяет Point; меняет только broker property refresh. Изменение свойств символа делает старый Point stale. новый SymbolInfo* property snapshot. NOT_APPLICABLE: действует пока symbol доступен. Этот lifecycle относится именно к объекту «Размер пункта» и его собственному type/source contract.
Условия stale: Изменение свойств символа делает старый Point stale.
Authoritative replacement: новый SymbolInfo* property snapshot.
Допустимые операции: сравнение и преобразование только по `PRICE_POINT_SIZE` с `EXACT PROPERTY SNAPSHOT` и explicit provenance.
Запрещённые подмены: Point нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Point, тип PRICE_POINT_SIZE, class SYMBOL PROPERTY.
Legacy aliases: —
MQL5 mapping: Include/HybridFutureSmallSolver.mqh::point
Python mapping: Tests/small_at_far_scenario_log.py::point
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: PRICE_OR_DISTANCE
Lifecycle class: SYMBOL_PROPERTY
Creation event: Point считывается вызовом SymbolInfo* при refresh свойств символа.
Validation event: Point проверяется на положительность и согласованность symbol snapshot.
Freeze/confirmation event: Значение фиксируется в symbol-property revision.
Mutation events: Рыночный tick не изменяет Point; меняет только broker property refresh.
Stale triggers: Изменение свойств символа делает старый Point stale.
Replacement source: новый SymbolInfo* property snapshot.
Terminal condition: NOT_APPLICABLE: действует пока symbol доступен.
Persistence behavior: Можно хранить только с symbol/property revision.
Restart behavior: После restart перечитывается из терминала.
Отличие от: Point отличается от sibling-терминов источником `SymbolInfoDouble(symbol, SYMBOL_POINT)`, классом `SYMBOL PROPERTY` и стадией lifecycle `SYMBOL_PROPERTY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `SYMBOL_PROPERTY`; запись `Point` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `Point` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### TickSize
CanonicalName: `TickSize`
Русское название: Тик размер
Краткое определение: TickSize — Минимальный trade tick price increment (`SYMBOL_TRADE_TICK_SIZE`); не считается равным Point без проверки symbol properties. Отличительный объект записи: «Тик размер»; его authoritative provenance — «SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE)».
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: TickSize
Размерность: `PRICE_TICK_SIZE`
Unit: `price per tick`
Знак: > 0
Допустимый диапазон: соответствует типу `PRICE_TICK_SIZE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE)
Authoritative source: SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE)
Время фиксации: SYMBOL PROPERTY stage для TickSize.
Projected/Actual class: `SYMBOL PROPERTY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT PROPERTY SNAPSHOT`
Lifecycle: TickSize считывается вызовом SymbolInfo* при refresh свойств символа. Рыночный tick не изменяет TickSize; меняет только broker property refresh. Изменение свойств символа делает старый TickSize stale. новый SymbolInfo* property snapshot. NOT_APPLICABLE: действует пока symbol доступен. Этот lifecycle относится именно к объекту «Тик размер» и его собственному type/source contract.
Условия stale: Изменение свойств символа делает старый TickSize stale.
Authoritative replacement: новый SymbolInfo* property snapshot.
Допустимые операции: сравнение и преобразование только по `PRICE_TICK_SIZE` с `EXACT PROPERTY SNAPSHOT` и explicit provenance.
Запрещённые подмены: TickSize нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: TickSize, тип PRICE_TICK_SIZE, class SYMBOL PROPERTY.
Legacy aliases: —
MQL5 mapping: Include/SimulationEngine.mqh::tickSize
Python mapping: NONE_FOUND
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: PRICE_OR_DISTANCE
Lifecycle class: SYMBOL_PROPERTY
Creation event: TickSize считывается вызовом SymbolInfo* при refresh свойств символа.
Validation event: TickSize проверяется на положительность и согласованность symbol snapshot.
Freeze/confirmation event: Значение фиксируется в symbol-property revision.
Mutation events: Рыночный tick не изменяет TickSize; меняет только broker property refresh.
Stale triggers: Изменение свойств символа делает старый TickSize stale.
Replacement source: новый SymbolInfo* property snapshot.
Terminal condition: NOT_APPLICABLE: действует пока symbol доступен.
Persistence behavior: Можно хранить только с symbol/property revision.
Restart behavior: После restart перечитывается из терминала.
Отличие от: TickSize отличается от sibling-терминов источником `SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE)`, классом `SYMBOL PROPERTY` и стадией lifecycle `SYMBOL_PROPERTY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `SYMBOL_PROPERTY`; запись `TickSize` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `TickSize` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### TickValue
CanonicalName: `TickValue`
Русское название: Тик стоимость
Краткое определение: TickValue — symbol-bound величина `TickValue` типа `PRICE_PROJECTED`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance. Отличительный объект записи: «Тик стоимость»; его authoritative provenance — «SymbolInfo tick/current position/deal properties».
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: TickValue
Размерность: `PRICE_PROJECTED`
Unit: `price`
Знак: > 0
Допустимый диапазон: соответствует типу `PRICE_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: PROJECTED stage для TickValue.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: TickValue вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties. Не мутирует; изменение inputs создаёт новую revision TickValue. Market, symbol, config или snapshot revision делает TickValue stale. пересчёт TickValue на новом immutable snapshot. После execution projected TickValue завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Тик стоимость» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает TickValue stale.
Authoritative replacement: пересчёт TickValue на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `PRICE_PROJECTED` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: TickValue нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: TickValue, тип PRICE_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/SimulationEngine.mqh::tickValue
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: PRICE_OR_DISTANCE
Lifecycle class: PROJECTED_VALUE
Creation event: TickValue вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties.
Validation event: TickValue валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: TickValue замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision TickValue.
Stale triggers: Market, symbol, config или snapshot revision делает TickValue stale.
Replacement source: пересчёт TickValue на новом immutable snapshot.
Terminal condition: После execution projected TickValue завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: TickValue отличается от sibling-терминов источником `SymbolInfo tick/current position/deal properties`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `TickValue` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `TickValue` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### MarketBidPrice
CanonicalName: `MarketBidPrice`
Русское название: Рыночная Bid цена
Краткое определение: MarketBidPrice — symbol-bound величина `MarketBidPrice` типа `PRICE_BID`, получаемая из SymbolInfoDouble(symbol, SYMBOL_BID); она не является money или lot и не использует их tolerance. Отличительный объект записи: «Рыночная Bid цена»; его authoritative provenance — «SymbolInfoDouble(symbol, SYMBOL_BID)».
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: MarketBidPrice
Размерность: `PRICE_BID`
Unit: `price`
Знак: > 0
Допустимый диапазон: соответствует типу `PRICE_BID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfoDouble(symbol, SYMBOL_BID)
Authoritative source: SymbolInfoDouble(symbol, SYMBOL_BID)
Время фиксации: ACTUAL CURRENT stage для MarketBidPrice.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `PriceTolerance`
Lifecycle: MarketBidPrice вычисляется из snapshot inputs: SymbolInfoDouble(symbol, SYMBOL_BID). Не мутирует; изменение inputs создаёт новую revision MarketBidPrice. Market, symbol, config или snapshot revision делает MarketBidPrice stale. пересчёт MarketBidPrice на новом immutable snapshot. После execution projected MarketBidPrice завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Рыночная Bid цена» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает MarketBidPrice stale.
Authoritative replacement: пересчёт MarketBidPrice на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `PRICE_BID` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: MarketBidPrice нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: MarketBidPrice, тип PRICE_BID, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: PRICE_OR_DISTANCE
Lifecycle class: PROJECTED_VALUE
Creation event: MarketBidPrice вычисляется из snapshot inputs: SymbolInfoDouble(symbol, SYMBOL_BID).
Validation event: MarketBidPrice валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: MarketBidPrice замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision MarketBidPrice.
Stale triggers: Market, symbol, config или snapshot revision делает MarketBidPrice stale.
Replacement source: пересчёт MarketBidPrice на новом immutable snapshot.
Terminal condition: После execution projected MarketBidPrice завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: MarketBidPrice отличается от sibling-терминов источником `SymbolInfoDouble(symbol, SYMBOL_BID)`, классом `ACTUAL CURRENT` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `MarketBidPrice` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `MarketBidPrice` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### MarketAskPrice
CanonicalName: `MarketAskPrice`
Русское название: Рыночная Ask цена
Краткое определение: MarketAskPrice — symbol-bound величина `MarketAskPrice` типа `PRICE_ASK`, получаемая из SymbolInfoDouble(symbol, SYMBOL_ASK); она не является money или lot и не использует их tolerance. Отличительный объект записи: «Рыночная Ask цена»; его authoritative provenance — «SymbolInfoDouble(symbol, SYMBOL_ASK)».
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: MarketAskPrice
Размерность: `PRICE_ASK`
Unit: `price`
Знак: > 0
Допустимый диапазон: соответствует типу `PRICE_ASK`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfoDouble(symbol, SYMBOL_ASK)
Authoritative source: SymbolInfoDouble(symbol, SYMBOL_ASK)
Время фиксации: ACTUAL CURRENT stage для MarketAskPrice.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `PriceTolerance`
Lifecycle: MarketAskPrice вычисляется из snapshot inputs: SymbolInfoDouble(symbol, SYMBOL_ASK). Не мутирует; изменение inputs создаёт новую revision MarketAskPrice. Market, symbol, config или snapshot revision делает MarketAskPrice stale. пересчёт MarketAskPrice на новом immutable snapshot. После execution projected MarketAskPrice завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Рыночная Ask цена» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает MarketAskPrice stale.
Authoritative replacement: пересчёт MarketAskPrice на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `PRICE_ASK` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: MarketAskPrice нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: MarketAskPrice, тип PRICE_ASK, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: PRICE_OR_DISTANCE
Lifecycle class: PROJECTED_VALUE
Creation event: MarketAskPrice вычисляется из snapshot inputs: SymbolInfoDouble(symbol, SYMBOL_ASK).
Validation event: MarketAskPrice валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: MarketAskPrice замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision MarketAskPrice.
Stale triggers: Market, symbol, config или snapshot revision делает MarketAskPrice stale.
Replacement source: пересчёт MarketAskPrice на новом immutable snapshot.
Terminal condition: После execution projected MarketAskPrice завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: MarketAskPrice отличается от sibling-терминов источником `SymbolInfoDouble(symbol, SYMBOL_ASK)`, классом `ACTUAL CURRENT` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `MarketAskPrice` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `MarketAskPrice` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### PositionOpenPrice
CanonicalName: `PositionOpenPrice`
Русское название: Позиция открытие цена
Краткое определение: PositionOpenPrice — symbol-bound величина `Position` типа `PRICE_OPEN`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance. Отличительный объект записи: «Позиция открытие цена»; его authoritative provenance — «SymbolInfo tick/current position/deal properties».
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: Position
Размерность: `PRICE_OPEN`
Unit: `price`
Знак: > 0
Допустимый диапазон: соответствует типу `PRICE_OPEN`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: PROJECTED stage для PositionOpenPrice.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: PositionOpenPrice вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties. Не мутирует; изменение inputs создаёт новую revision PositionOpenPrice. Market, symbol, config или snapshot revision делает PositionOpenPrice stale. пересчёт PositionOpenPrice на новом immutable snapshot. После execution projected PositionOpenPrice завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Позиция открытие цена» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает PositionOpenPrice stale.
Authoritative replacement: пересчёт PositionOpenPrice на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `PRICE_OPEN` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: PositionOpenPrice нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Position, тип PRICE_OPEN, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/SimulationEngine.mqh::positionOpenPrice
Python mapping: NONE_FOUND
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: PRICE_OR_DISTANCE
Lifecycle class: PROJECTED_VALUE
Creation event: PositionOpenPrice вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties.
Validation event: PositionOpenPrice валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: PositionOpenPrice замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision PositionOpenPrice.
Stale triggers: Market, symbol, config или snapshot revision делает PositionOpenPrice stale.
Replacement source: пересчёт PositionOpenPrice на новом immutable snapshot.
Terminal condition: После execution projected PositionOpenPrice завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: PositionOpenPrice отличается от sibling-терминов источником `SymbolInfo tick/current position/deal properties`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `PositionOpenPrice` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `PositionOpenPrice` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### TriggerPrice
CanonicalName: `TriggerPrice`
Русское название: Триггер цена
Краткое определение: TriggerPrice — symbol-bound величина `TriggerPrice` типа `PRICE_PROJECTED`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance. Отличительный объект записи: «Триггер цена»; его authoritative provenance — «SymbolInfo tick/current position/deal properties».
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: TriggerPrice
Размерность: `PRICE_PROJECTED`
Unit: `price`
Знак: > 0
Допустимый диапазон: соответствует типу `PRICE_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: PROJECTED stage для TriggerPrice.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: TriggerPrice вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties. Не мутирует; изменение inputs создаёт новую revision TriggerPrice. Market, symbol, config или snapshot revision делает TriggerPrice stale. пересчёт TriggerPrice на новом immutable snapshot. После execution projected TriggerPrice завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Триггер цена» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает TriggerPrice stale.
Authoritative replacement: пересчёт TriggerPrice на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `PRICE_PROJECTED` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: TriggerPrice нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: TriggerPrice, тип PRICE_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: PRICE_OR_DISTANCE
Lifecycle class: PROJECTED_VALUE
Creation event: TriggerPrice вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties.
Validation event: TriggerPrice валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: TriggerPrice замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision TriggerPrice.
Stale triggers: Market, symbol, config или snapshot revision делает TriggerPrice stale.
Replacement source: пересчёт TriggerPrice на новом immutable snapshot.
Terminal condition: После execution projected TriggerPrice завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: TriggerPrice отличается от sibling-терминов источником `SymbolInfo tick/current position/deal properties`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `TriggerPrice` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `TriggerPrice` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### TargetPrice
CanonicalName: `TargetPrice`
Русское название: Целевая цена
Краткое определение: TargetPrice — symbol-bound величина `TargetPrice` типа `PRICE_PROJECTED`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance. Отличительный объект записи: «Целевая цена»; его authoritative provenance — «SymbolInfo tick/current position/deal properties».
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: TargetPrice
Размерность: `PRICE_PROJECTED`
Unit: `price`
Знак: > 0
Допустимый диапазон: соответствует типу `PRICE_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: PROJECTED stage для TargetPrice.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: TargetPrice вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties. Не мутирует; изменение inputs создаёт новую revision TargetPrice. Market, symbol, config или snapshot revision делает TargetPrice stale. пересчёт TargetPrice на новом immutable snapshot. После execution projected TargetPrice завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Целевая цена» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает TargetPrice stale.
Authoritative replacement: пересчёт TargetPrice на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `PRICE_PROJECTED` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: TargetPrice нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: TargetPrice, тип PRICE_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: PRICE_OR_DISTANCE
Lifecycle class: PROJECTED_VALUE
Creation event: TargetPrice вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties.
Validation event: TargetPrice валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: TargetPrice замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision TargetPrice.
Stale triggers: Market, symbol, config или snapshot revision делает TargetPrice stale.
Replacement source: пересчёт TargetPrice на новом immutable snapshot.
Terminal condition: После execution projected TargetPrice завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: TargetPrice отличается от sibling-терминов источником `SymbolInfo tick/current position/deal properties`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `TargetPrice` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `TargetPrice` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### ControlPrice
CanonicalName: `ControlPrice`
Русское название: Контрольная цена
Краткое определение: ControlPrice — symbol-bound величина `ControlPrice` типа `PRICE_PROJECTED`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance. Отличительный объект записи: «Контрольная цена»; его authoritative provenance — «SymbolInfo tick/current position/deal properties».
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: ControlPrice
Размерность: `PRICE_PROJECTED`
Unit: `price`
Знак: > 0
Допустимый диапазон: соответствует типу `PRICE_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: PROJECTED stage для ControlPrice.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: ControlPrice вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties. Не мутирует; изменение inputs создаёт новую revision ControlPrice. Market, symbol, config или snapshot revision делает ControlPrice stale. пересчёт ControlPrice на новом immutable snapshot. После execution projected ControlPrice завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Контрольная цена» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает ControlPrice stale.
Authoritative replacement: пересчёт ControlPrice на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `PRICE_PROJECTED` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: ControlPrice нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ControlPrice, тип PRICE_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: PRICE_OR_DISTANCE
Lifecycle class: PROJECTED_VALUE
Creation event: ControlPrice вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties.
Validation event: ControlPrice валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: ControlPrice замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision ControlPrice.
Stale triggers: Market, symbol, config или snapshot revision делает ControlPrice stale.
Replacement source: пересчёт ControlPrice на новом immutable snapshot.
Terminal condition: После execution projected ControlPrice завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: ControlPrice отличается от sibling-терминов источником `SymbolInfo tick/current position/deal properties`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `ControlPrice` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ControlPrice` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### ProjectedExitPrice
CanonicalName: `ProjectedExitPrice`
Русское название: Прогнозный выход цена
Краткое определение: ProjectedExitPrice — symbol-bound величина `ProjectedExitPrice` типа `PRICE_PROJECTED`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance. Отличительный объект записи: «Прогнозный выход цена»; его authoritative provenance — «SymbolInfo tick/current position/deal properties».
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: ProjectedExitPrice
Размерность: `PRICE_PROJECTED`
Unit: `price`
Знак: > 0
Допустимый диапазон: соответствует типу `PRICE_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: PROJECTED stage для ProjectedExitPrice.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: ProjectedExitPrice вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties. Не мутирует; изменение inputs создаёт новую revision ProjectedExitPrice. Market, symbol, config или snapshot revision делает ProjectedExitPrice stale. пересчёт ProjectedExitPrice на новом immutable snapshot. После execution projected ProjectedExitPrice завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Прогнозный выход цена» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает ProjectedExitPrice stale.
Authoritative replacement: пересчёт ProjectedExitPrice на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `PRICE_PROJECTED` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: ProjectedExitPrice нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ProjectedExitPrice, тип PRICE_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: PRICE_OR_DISTANCE
Lifecycle class: PROJECTED_VALUE
Creation event: ProjectedExitPrice вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties.
Validation event: ProjectedExitPrice валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: ProjectedExitPrice замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision ProjectedExitPrice.
Stale triggers: Market, symbol, config или snapshot revision делает ProjectedExitPrice stale.
Replacement source: пересчёт ProjectedExitPrice на новом immutable snapshot.
Terminal condition: После execution projected ProjectedExitPrice завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: ProjectedExitPrice отличается от sibling-терминов источником `SymbolInfo tick/current position/deal properties`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `ProjectedExitPrice` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ProjectedExitPrice` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### ExecutedDealPrice
CanonicalName: `ExecutedDealPrice`
Русское название: Исполненная сделка цена
Краткое определение: ExecutedDealPrice — symbol-bound величина `ExecutedDealPrice` типа `PRICE_EXECUTED`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance. Отличительный объект записи: «Исполненная сделка цена»; его authoritative provenance — «SymbolInfo tick/current position/deal properties».
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: ExecutedDealPrice
Размерность: `PRICE_EXECUTED`
Unit: `price`
Знак: > 0
Допустимый диапазон: соответствует типу `PRICE_EXECUTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: CONFIRMED stage для ExecutedDealPrice.
Projected/Actual class: `CONFIRMED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: ExecutedDealPrice возникает только из подтверждённого deal event. Несколько partial fills агрегируются без изменения исходных deals. Новая выборка history делает прежний aggregate ExecutedDealPrice stale, но не отдельный deal. повторно построенный aggregate confirmed deal history. Финализируется после полного сбора fills для execution scope. Этот lifecycle относится именно к объекту «Исполненная сделка цена» и его собственному type/source contract.
Условия stale: Новая выборка history делает прежний aggregate ExecutedDealPrice stale, но не отдельный deal.
Authoritative replacement: повторно построенный aggregate confirmed deal history.
Допустимые операции: сравнение и преобразование только по `PRICE_EXECUTED` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: ExecutedDealPrice нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ExecutedDealPrice, тип PRICE_EXECUTED, class CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: PRICE_OR_DISTANCE
Lifecycle class: DEAL
Creation event: ExecutedDealPrice возникает только из подтверждённого deal event.
Validation event: ExecutedDealPrice проверяется фильтрами Symbol, MagicNumber, CycleID и deal/position identity.
Freeze/confirmation event: Deal evidence для ExecutedDealPrice неизменно после подтверждения истории.
Mutation events: Несколько partial fills агрегируются без изменения исходных deals.
Stale triggers: Новая выборка history делает прежний aggregate ExecutedDealPrice stale, но не отдельный deal.
Replacement source: повторно построенный aggregate confirmed deal history.
Terminal condition: Финализируется после полного сбора fills для execution scope.
Persistence behavior: Persisted audit ссылается на DealTicket/EventID exactly once.
Restart behavior: После restart реконструируется из confirmed deal history.
Отличие от: ExecutedDealPrice отличается от sibling-терминов источником `SymbolInfo tick/current position/deal properties`, классом `CONFIRMED` и стадией lifecycle `DEAL`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `DEAL`; запись `ExecutedDealPrice` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ExecutedDealPrice` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### PriceDelta
CanonicalName: `PriceDelta`
Русское название: Цена дельта
Краткое определение: PriceDelta — symbol-bound величина `PriceDelta` типа `PRICE_DELTA`, получаемая из difference of two explicitly named prices; она не является money или lot и не использует их tolerance. Отличительный объект записи: «Цена дельта»; его authoritative provenance — «difference of two explicitly named prices».
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: PriceDelta
Размерность: `PRICE_DELTA`
Unit: `price`
Знак: signed
Допустимый диапазон: соответствует типу `PRICE_DELTA`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: difference of two explicitly named prices
Authoritative source: difference of two explicitly named prices
Время фиксации: PROJECTED stage для PriceDelta.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: PriceDelta вычисляется из snapshot inputs: difference of two explicitly named prices. Не мутирует; изменение inputs создаёт новую revision PriceDelta. Market, symbol, config или snapshot revision делает PriceDelta stale. пересчёт PriceDelta на новом immutable snapshot. После execution projected PriceDelta завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Цена дельта» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает PriceDelta stale.
Authoritative replacement: пересчёт PriceDelta на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `PRICE_DELTA` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: PriceDelta нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PriceDelta, тип PRICE_DELTA, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: PRICE_OR_DISTANCE
Lifecycle class: PROJECTED_VALUE
Creation event: PriceDelta вычисляется из snapshot inputs: difference of two explicitly named prices.
Validation event: PriceDelta валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: PriceDelta замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision PriceDelta.
Stale triggers: Market, symbol, config или snapshot revision делает PriceDelta stale.
Replacement source: пересчёт PriceDelta на новом immutable snapshot.
Terminal condition: После execution projected PriceDelta завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: PriceDelta отличается от sibling-терминов источником `difference of two explicitly named prices`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `PriceDelta` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `PriceDelta` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### DistancePoints
CanonicalName: `DistancePoints`
Русское название: Расстояние пункты
Краткое определение: DistancePoints — symbol-bound величина `DistancePoints` типа `DISTANCE_POINTS`, получаемая из explicit price delta divided by SYMBOL_POINT; она не является money или lot и не использует их tolerance. Отличительный объект записи: «Расстояние пункты»; его authoritative provenance — «explicit price delta divided by SYMBOL_POINT».
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: DistancePoints
Размерность: `DISTANCE_POINTS`
Unit: `points`
Знак: non-negative distance
Допустимый диапазон: соответствует типу `DISTANCE_POINTS`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: explicit price delta divided by SYMBOL_POINT
Authoritative source: explicit price delta divided by SYMBOL_POINT
Время фиксации: PROJECTED or ACTUAL MEASUREMENT stage для DistancePoints.
Projected/Actual class: `PROJECTED or ACTUAL MEASUREMENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `PointTolerance`
Lifecycle: DistancePoints вычисляется из snapshot inputs: explicit price delta divided by SYMBOL_POINT. Не мутирует; изменение inputs создаёт новую revision DistancePoints. Market, symbol, config или snapshot revision делает DistancePoints stale. пересчёт DistancePoints на новом immutable snapshot. После execution projected DistancePoints завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Расстояние пункты» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает DistancePoints stale.
Authoritative replacement: пересчёт DistancePoints на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `DISTANCE_POINTS` с `PointTolerance` и explicit provenance.
Запрещённые подмены: DistancePoints нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: DistancePoints, тип DISTANCE_POINTS, class PROJECTED or ACTUAL MEASUREMENT.
Legacy aliases: —
MQL5 mapping: Include/HybridCatchUpModel.mqh::distancePoints
Python mapping: Tools/mql5_like_big_scenario_parameter_search.py::distance_points
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: PRICE_OR_DISTANCE
Lifecycle class: PROJECTED_VALUE
Creation event: DistancePoints вычисляется из snapshot inputs: explicit price delta divided by SYMBOL_POINT.
Validation event: DistancePoints валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: DistancePoints замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision DistancePoints.
Stale triggers: Market, symbol, config или snapshot revision делает DistancePoints stale.
Replacement source: пересчёт DistancePoints на новом immutable snapshot.
Terminal condition: После execution projected DistancePoints завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: DistancePoints отличается от sibling-терминов источником `explicit price delta divided by SYMBOL_POINT`, классом `PROJECTED or ACTUAL MEASUREMENT` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `DistancePoints` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `DistancePoints` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### DistanceTicks
CanonicalName: `DistanceTicks`
Русское название: Расстояние тики
Краткое определение: DistanceTicks — symbol-bound величина `DistanceTicks` типа `DISTANCE_TICKS`, получаемая из explicit price delta divided by SYMBOL_TRADE_TICK_SIZE; она не является money или lot и не использует их tolerance. Отличительный объект записи: «Расстояние тики»; его authoritative provenance — «explicit price delta divided by SYMBOL_TRADE_TICK_SIZE».
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: DistanceTicks
Размерность: `DISTANCE_TICKS`
Unit: `ticks`
Знак: non-negative distance
Допустимый диапазон: соответствует типу `DISTANCE_TICKS`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: explicit price delta divided by SYMBOL_TRADE_TICK_SIZE
Authoritative source: explicit price delta divided by SYMBOL_TRADE_TICK_SIZE
Время фиксации: PROJECTED or ACTUAL MEASUREMENT stage для DistanceTicks.
Projected/Actual class: `PROJECTED or ACTUAL MEASUREMENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `PointTolerance`
Lifecycle: DistanceTicks вычисляется из snapshot inputs: explicit price delta divided by SYMBOL_TRADE_TICK_SIZE. Не мутирует; изменение inputs создаёт новую revision DistanceTicks. Market, symbol, config или snapshot revision делает DistanceTicks stale. пересчёт DistanceTicks на новом immutable snapshot. После execution projected DistanceTicks завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Расстояние тики» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает DistanceTicks stale.
Authoritative replacement: пересчёт DistanceTicks на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `DISTANCE_TICKS` с `PointTolerance` и explicit provenance.
Запрещённые подмены: DistanceTicks нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: DistanceTicks, тип DISTANCE_TICKS, class PROJECTED or ACTUAL MEASUREMENT.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: PRICE_OR_DISTANCE
Lifecycle class: PROJECTED_VALUE
Creation event: DistanceTicks вычисляется из snapshot inputs: explicit price delta divided by SYMBOL_TRADE_TICK_SIZE.
Validation event: DistanceTicks валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: DistanceTicks замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision DistanceTicks.
Stale triggers: Market, symbol, config или snapshot revision делает DistanceTicks stale.
Replacement source: пересчёт DistanceTicks на новом immutable snapshot.
Terminal condition: После execution projected DistanceTicks завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: DistanceTicks отличается от sibling-терминов источником `explicit price delta divided by SYMBOL_TRADE_TICK_SIZE`, классом `PROJECTED or ACTUAL MEASUREMENT` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `DistanceTicks` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `DistanceTicks` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### BidAwareClosePrice
CanonicalName: `BidAwareClosePrice`
Русское название: Bid учитывающая сторону рынка закрытие цена
Краткое определение: BidAwareClosePrice — symbol-bound величина `BidAwareClosePrice` типа `PRICE_BID`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance. Отличительный объект записи: «Bid учитывающая сторону рынка закрытие цена»; его authoritative provenance — «SymbolInfo tick/current position/deal properties».
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: BidAwareClosePrice
Размерность: `PRICE_BID`
Unit: `price`
Знак: > 0
Допустимый диапазон: соответствует типу `PRICE_BID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: PROJECTED stage для BidAwareClosePrice.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: BidAwareClosePrice вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties. Не мутирует; изменение inputs создаёт новую revision BidAwareClosePrice. Market, symbol, config или snapshot revision делает BidAwareClosePrice stale. пересчёт BidAwareClosePrice на новом immutable snapshot. После execution projected BidAwareClosePrice завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Bid учитывающая сторону рынка закрытие цена» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает BidAwareClosePrice stale.
Authoritative replacement: пересчёт BidAwareClosePrice на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `PRICE_BID` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: BidAwareClosePrice нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BidAwareClosePrice, тип PRICE_BID, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: PRICE_OR_DISTANCE
Lifecycle class: PROJECTED_VALUE
Creation event: BidAwareClosePrice вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties.
Validation event: BidAwareClosePrice валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: BidAwareClosePrice замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision BidAwareClosePrice.
Stale triggers: Market, symbol, config или snapshot revision делает BidAwareClosePrice stale.
Replacement source: пересчёт BidAwareClosePrice на новом immutable snapshot.
Terminal condition: После execution projected BidAwareClosePrice завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: BidAwareClosePrice отличается от sibling-терминов источником `SymbolInfo tick/current position/deal properties`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `BidAwareClosePrice` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `BidAwareClosePrice` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### AskAwareClosePrice
CanonicalName: `AskAwareClosePrice`
Русское название: Ask учитывающая сторону рынка закрытие цена
Краткое определение: AskAwareClosePrice — symbol-bound величина `AskAwareClosePrice` типа `PRICE_ASK`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance. Отличительный объект записи: «Ask учитывающая сторону рынка закрытие цена»; его authoritative provenance — «SymbolInfo tick/current position/deal properties».
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: AskAwareClosePrice
Размерность: `PRICE_ASK`
Unit: `price`
Знак: > 0
Допустимый диапазон: соответствует типу `PRICE_ASK`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: PROJECTED stage для AskAwareClosePrice.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: AskAwareClosePrice вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties. Не мутирует; изменение inputs создаёт новую revision AskAwareClosePrice. Market, symbol, config или snapshot revision делает AskAwareClosePrice stale. пересчёт AskAwareClosePrice на новом immutable snapshot. После execution projected AskAwareClosePrice завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Ask учитывающая сторону рынка закрытие цена» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает AskAwareClosePrice stale.
Authoritative replacement: пересчёт AskAwareClosePrice на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `PRICE_ASK` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: AskAwareClosePrice нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: AskAwareClosePrice, тип PRICE_ASK, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: PRICE_OR_DISTANCE
Lifecycle class: PROJECTED_VALUE
Creation event: AskAwareClosePrice вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties.
Validation event: AskAwareClosePrice валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: AskAwareClosePrice замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision AskAwareClosePrice.
Stale triggers: Market, symbol, config или snapshot revision делает AskAwareClosePrice stale.
Replacement source: пересчёт AskAwareClosePrice на новом immutable snapshot.
Terminal condition: После execution projected AskAwareClosePrice завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: AskAwareClosePrice отличается от sibling-терминов источником `SymbolInfo tick/current position/deal properties`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `AskAwareClosePrice` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `AskAwareClosePrice` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### FarOpenPriceActual
CanonicalName: `FarOpenPriceActual`
Русское название: Хвостовая позиция открытие цена фактический
Краткое определение: FarOpenPriceActual — symbol-bound величина `Far` типа `PRICE_OPEN`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance. Отличительный объект записи: «Хвостовая позиция открытие цена фактический»; его authoritative provenance — «SymbolInfo tick/current position/deal properties».
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: Far
Размерность: `PRICE_OPEN`
Unit: `price`
Знак: > 0
Допустимый диапазон: соответствует типу `PRICE_OPEN`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: ACTUAL CURRENT stage для FarOpenPriceActual.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: FarOpenPriceActual вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties. Не мутирует; изменение inputs создаёт новую revision FarOpenPriceActual. Market, symbol, config или snapshot revision делает FarOpenPriceActual stale. пересчёт FarOpenPriceActual на новом immutable snapshot. После execution projected FarOpenPriceActual завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Хвостовая позиция открытие цена фактический» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает FarOpenPriceActual stale.
Authoritative replacement: пересчёт FarOpenPriceActual на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `PRICE_OPEN` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: FarOpenPriceActual нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Far, тип PRICE_OPEN, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::farOpenPrice
Python mapping: Tests/small_at_far_scenario_log.py::far_open_price
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: PRICE_OR_DISTANCE
Lifecycle class: PROJECTED_VALUE
Creation event: FarOpenPriceActual вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties.
Validation event: FarOpenPriceActual валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: FarOpenPriceActual замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision FarOpenPriceActual.
Stale triggers: Market, symbol, config или snapshot revision делает FarOpenPriceActual stale.
Replacement source: пересчёт FarOpenPriceActual на новом immutable snapshot.
Terminal condition: После execution projected FarOpenPriceActual завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: FarOpenPriceActual отличается от sibling-терминов источником `SymbolInfo tick/current position/deal properties`, классом `ACTUAL CURRENT` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `FarOpenPriceActual` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `FarOpenPriceActual` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### BigCoreOpenPriceActual
CanonicalName: `BigCoreOpenPriceActual`
Русское название: Компенсирующая позиция основная часть открытие цена фактический
Краткое определение: BigCoreOpenPriceActual — symbol-bound величина `BigCore` типа `PRICE_OPEN`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance. Отличительный объект записи: «Компенсирующая позиция основная часть открытие цена фактический»; его authoritative provenance — «SymbolInfo tick/current position/deal properties».
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: BigCore
Размерность: `PRICE_OPEN`
Unit: `price`
Знак: > 0
Допустимый диапазон: соответствует типу `PRICE_OPEN`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: ACTUAL CURRENT stage для BigCoreOpenPriceActual.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: BigCoreOpenPriceActual вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties. Не мутирует; изменение inputs создаёт новую revision BigCoreOpenPriceActual. Market, symbol, config или snapshot revision делает BigCoreOpenPriceActual stale. пересчёт BigCoreOpenPriceActual на новом immutable snapshot. После execution projected BigCoreOpenPriceActual завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Компенсирующая позиция основная часть открытие цена фактический» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает BigCoreOpenPriceActual stale.
Authoritative replacement: пересчёт BigCoreOpenPriceActual на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `PRICE_OPEN` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: BigCoreOpenPriceActual нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigCore, тип PRICE_OPEN, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::coreOpenPrice
Python mapping: NONE_FOUND
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: PRICE_OR_DISTANCE
Lifecycle class: PROJECTED_VALUE
Creation event: BigCoreOpenPriceActual вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties.
Validation event: BigCoreOpenPriceActual валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: BigCoreOpenPriceActual замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision BigCoreOpenPriceActual.
Stale triggers: Market, symbol, config или snapshot revision делает BigCoreOpenPriceActual stale.
Replacement source: пересчёт BigCoreOpenPriceActual на новом immutable snapshot.
Terminal condition: После execution projected BigCoreOpenPriceActual завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: BigCoreOpenPriceActual отличается от sibling-терминов источником `SymbolInfo tick/current position/deal properties`, классом `ACTUAL CURRENT` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `BigCoreOpenPriceActual` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `BigCoreOpenPriceActual` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### BigTrendOpenPriceActual
CanonicalName: `BigTrendOpenPriceActual`
Русское название: Компенсирующая позиция трендовая часть открытие цена фактический
Краткое определение: BigTrendOpenPriceActual — symbol-bound величина `BigTrend` типа `PRICE_OPEN`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance. Отличительный объект записи: «Компенсирующая позиция трендовая часть открытие цена фактический»; его authoritative provenance — «SymbolInfo tick/current position/deal properties».
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: BigTrend
Размерность: `PRICE_OPEN`
Unit: `price`
Знак: > 0
Допустимый диапазон: соответствует типу `PRICE_OPEN`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: ACTUAL CURRENT stage для BigTrendOpenPriceActual.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: BigTrendOpenPriceActual вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties. Не мутирует; изменение inputs создаёт новую revision BigTrendOpenPriceActual. Market, symbol, config или snapshot revision делает BigTrendOpenPriceActual stale. пересчёт BigTrendOpenPriceActual на новом immutable snapshot. После execution projected BigTrendOpenPriceActual завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Компенсирующая позиция трендовая часть открытие цена фактический» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает BigTrendOpenPriceActual stale.
Authoritative replacement: пересчёт BigTrendOpenPriceActual на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `PRICE_OPEN` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: BigTrendOpenPriceActual нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigTrend, тип PRICE_OPEN, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::trendOpenPrice
Python mapping: NONE_FOUND
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: PRICE_OR_DISTANCE
Lifecycle class: PROJECTED_VALUE
Creation event: BigTrendOpenPriceActual вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties.
Validation event: BigTrendOpenPriceActual валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: BigTrendOpenPriceActual замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision BigTrendOpenPriceActual.
Stale triggers: Market, symbol, config или snapshot revision делает BigTrendOpenPriceActual stale.
Replacement source: пересчёт BigTrendOpenPriceActual на новом immutable snapshot.
Terminal condition: После execution projected BigTrendOpenPriceActual завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: BigTrendOpenPriceActual отличается от sibling-терминов источником `SymbolInfo tick/current position/deal properties`, классом `ACTUAL CURRENT` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `BigTrendOpenPriceActual` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `BigTrendOpenPriceActual` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### SmallBaseOpenPriceActual
CanonicalName: `SmallBaseOpenPriceActual`
Русское название: Защитная позиция базовая открытие цена фактический
Краткое определение: SmallBaseOpenPriceActual — symbol-bound величина `SmallBase` типа `PRICE_OPEN`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance. Отличительный объект записи: «Защитная позиция базовая открытие цена фактический»; его authoritative provenance — «SymbolInfo tick/current position/deal properties».
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: SmallBase
Размерность: `PRICE_OPEN`
Unit: `price`
Знак: > 0
Допустимый диапазон: соответствует типу `PRICE_OPEN`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: ACTUAL CURRENT stage для SmallBaseOpenPriceActual.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: SmallBaseOpenPriceActual вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties. Не мутирует; изменение inputs создаёт новую revision SmallBaseOpenPriceActual. Market, symbol, config или snapshot revision делает SmallBaseOpenPriceActual stale. пересчёт SmallBaseOpenPriceActual на новом immutable snapshot. После execution projected SmallBaseOpenPriceActual завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Защитная позиция базовая открытие цена фактический» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает SmallBaseOpenPriceActual stale.
Authoritative replacement: пересчёт SmallBaseOpenPriceActual на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `PRICE_OPEN` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: SmallBaseOpenPriceActual нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SmallBase, тип PRICE_OPEN, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::smallOpenPrice
Python mapping: NONE_FOUND
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: PRICE_OR_DISTANCE
Lifecycle class: PROJECTED_VALUE
Creation event: SmallBaseOpenPriceActual вычисляется из snapshot inputs: SymbolInfo tick/current position/deal properties.
Validation event: SmallBaseOpenPriceActual валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: SmallBaseOpenPriceActual замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision SmallBaseOpenPriceActual.
Stale triggers: Market, symbol, config или snapshot revision делает SmallBaseOpenPriceActual stale.
Replacement source: пересчёт SmallBaseOpenPriceActual на новом immutable snapshot.
Terminal condition: После execution projected SmallBaseOpenPriceActual завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: SmallBaseOpenPriceActual отличается от sibling-терминов источником `SymbolInfo tick/current position/deal properties`, классом `ACTUAL CURRENT` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `SmallBaseOpenPriceActual` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `SmallBaseOpenPriceActual` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### GrossProfit
CanonicalName: `GrossProfit`
Русское название: Валовая прибыль
Краткое определение: GrossProfit — денежная величина `GrossProfit` класса `ACTUAL CONFIRMED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Валовая прибыль»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: GrossProfit
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: signed
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для GrossProfit.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: GrossProfit создаётся confirmed allocation/deal event с уникальным EventID. GrossProfit меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Валовая прибыль» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: GrossProfit нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: GrossProfit, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/StateMachine.mqh::projectedGrossProfit
Python mapping: Tools/offline_optimizer.py::gross_profit
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: GrossProfit создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: GrossProfit проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: GrossProfit меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: GrossProfit отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `GrossProfit` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `GrossProfit` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### GrossLoss
CanonicalName: `GrossLoss`
Русское название: Валовая убыток
Краткое определение: GrossLoss — денежная величина `GrossLoss` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Валовая убыток»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: GrossLoss
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для GrossLoss.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: GrossLoss создаётся confirmed allocation/deal event с уникальным EventID. GrossLoss меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Валовая убыток» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: GrossLoss нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: GrossLoss, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: Tools/offline_optimizer.py::gross_loss
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: GrossLoss создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: GrossLoss проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: GrossLoss меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: GrossLoss отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `GrossLoss` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `GrossLoss` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=PARTIAL_MATCH.

### NetProfit
CanonicalName: `NetProfit`
Русское название: Чистый результат прибыль
Краткое определение: NetProfit — денежная величина `NetProfit` класса `ACTUAL CONFIRMED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Чистый результат прибыль»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: NetProfit
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: signed
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для NetProfit.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: NetProfit создаётся confirmed allocation/deal event с уникальным EventID. NetProfit меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Чистый результат прибыль» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: NetProfit нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: NetProfit, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/Logger.mqh::netProfit
Python mapping: Tools/run_full_parameter_optimization_study.py::net_profit
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: NetProfit создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: NetProfit проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: NetProfit меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: NetProfit отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `NetProfit` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `NetProfit` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### LegNet
CanonicalName: `LegNet`
Русское название: Leg чистый результат
Краткое определение: LegNet — денежная величина `LegNet` класса `ACTUAL CONFIRMED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Leg чистый результат»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: LegNet
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: signed
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для LegNet.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: LegNet создаётся confirmed allocation/deal event с уникальным EventID. LegNet меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Leg чистый результат» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: LegNet нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: LegNet, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/StateMachine.mqh::legNet
Python mapping: NONE_FOUND
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: LegNet создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: LegNet проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: LegNet меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: LegNet отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `LegNet` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `LegNet` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### BasketNet
CanonicalName: `BasketNet`
Русское название: Корзина чистый результат
Краткое определение: BasketNet — денежная величина `BasketNet` класса `ACTUAL CONFIRMED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Корзина чистый результат»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: BasketNet
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: signed
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для BasketNet.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: BasketNet создаётся confirmed allocation/deal event с уникальным EventID. BasketNet меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Корзина чистый результат» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: BasketNet нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BasketNet, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::basket
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: BasketNet создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: BasketNet проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: BasketNet меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: BasketNet отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `BasketNet` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `BasketNet` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### HarvestGross
CanonicalName: `HarvestGross`
Русское название: Сбор прибыли валовая
Краткое определение: HarvestGross — денежная величина `HarvestGross` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Сбор прибыли валовая»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: HarvestGross
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для HarvestGross.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: HarvestGross создаётся confirmed allocation/deal event с уникальным EventID. HarvestGross меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Сбор прибыли валовая» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: HarvestGross нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: HarvestGross, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: HarvestGross создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: HarvestGross проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: HarvestGross меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: HarvestGross отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `HarvestGross` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `HarvestGross` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### HarvestNet
CanonicalName: `HarvestNet`
Русское название: Сбор прибыли чистый результат
Краткое определение: HarvestNet — денежная величина `HarvestNet` класса `ACTUAL CONFIRMED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Сбор прибыли чистый результат»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: HarvestNet
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: signed
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для HarvestNet.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: HarvestNet создаётся confirmed allocation/deal event с уникальным EventID. HarvestNet меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Сбор прибыли чистый результат» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: HarvestNet нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: HarvestNet, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::harvestNet
Python mapping: Tools/hybrid_big_sequence_model.py::harvest
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: HarvestNet создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: HarvestNet проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: HarvestNet меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: HarvestNet отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `HarvestNet` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `HarvestNet` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### SmallReverseNet
CanonicalName: `SmallReverseNet`
Русское название: Защитная позиция разворот чистый результат
Краткое определение: SmallReverseNet — денежная величина `SmallReverseNet` класса `ACTUAL CONFIRMED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Защитная позиция разворот чистый результат»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: SmallReverseNet
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: signed
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для SmallReverseNet.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: SmallReverseNet создаётся confirmed allocation/deal event с уникальным EventID. SmallReverseNet меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Защитная позиция разворот чистый результат» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: SmallReverseNet нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SmallReverseNet, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: Tools/offline_optimizer.py::small_net
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `HSB-DOC-CONFLICT-023`
Resolution stage: `3.1.5 / 3.1.6`
Статус определения: `UNRESOLVED_BUSINESS_POLICY`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: SmallReverseNet создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: SmallReverseNet проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: SmallReverseNet меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: SmallReverseNet отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `SmallReverseNet` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `SmallReverseNet` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=PARTIAL_MATCH.

### TransitionNet
CanonicalName: `TransitionNet`
Русское название: Переход чистый результат
Краткое определение: TransitionNet — денежная величина `TransitionNet` класса `ACTUAL CONFIRMED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Переход чистый результат»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: TransitionNet
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: signed
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для TransitionNet.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: TransitionNet создаётся confirmed allocation/deal event с уникальным EventID. TransitionNet меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Переход чистый результат» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: TransitionNet нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: TransitionNet, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: Tools/hybrid_geometry_model.py::transition_net
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: TransitionNet создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: TransitionNet проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: TransitionNet меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: TransitionNet отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `TransitionNet` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `TransitionNet` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=PARTIAL_MATCH.

### RealizedCyclePL
CanonicalName: `RealizedCyclePL`
Русское название: Реализованный цикл pl
Краткое определение: RealizedCyclePL — денежная величина `RealizedCyclePL` класса `ACTUAL CONFIRMED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Реализованный цикл pl»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: RealizedCyclePL
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: signed
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для RealizedCyclePL.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: RealizedCyclePL создаётся confirmed allocation/deal event с уникальным EventID. RealizedCyclePL меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Реализованный цикл pl» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: RealizedCyclePL нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RealizedCyclePL, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::realizedCyclePL
Python mapping: Tools/hybrid_small_state_machine.py::realized_cycle_pl
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: RealizedCyclePL создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: RealizedCyclePL проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: RealizedCyclePL меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: RealizedCyclePL отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `RealizedCyclePL` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `RealizedCyclePL` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### FloatingManagedPL
CanonicalName: `FloatingManagedPL`
Русское название: Плавающий управляемая pl
Краткое определение: FloatingManagedPL — денежная величина `FloatingManagedPL` класса `ACTUAL CURRENT` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Плавающий управляемая pl»; его authoritative provenance — «current position or broker-aware price model».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: FloatingManagedPL
Размерность: `MONEY_FLOATING`
Unit: `account money`
Знак: signed
Допустимый диапазон: соответствует типу `MONEY_FLOATING`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: current position or broker-aware price model
Authoritative source: current position or broker-aware price model
Время фиксации: ACTUAL CURRENT stage для FloatingManagedPL.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: FloatingManagedPL появляется при чтении текущего MT5 position snapshot. Любое исполнение, partial close или position merge изменяет FloatingManagedPL. Любой trade event после snapshot немедленно делает FloatingManagedPL stale. новый current MT5 position snapshot. После полного закрытия становится ZERO либо NOT_APPLICABLE согласно типу. Этот lifecycle относится именно к объекту «Плавающий управляемая pl» и его собственному type/source contract.
Условия stale: Любой trade event после snapshot немедленно делает FloatingManagedPL stale.
Authoritative replacement: новый current MT5 position snapshot.
Допустимые операции: сравнение и преобразование только по `MONEY_FLOATING` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: FloatingManagedPL нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: FloatingManagedPL, тип MONEY_FLOATING, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: Include/StateMachine.mqh::farFloatingPL
Python mapping: NONE_FOUND
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: ACTUAL_POSITION
Creation event: FloatingManagedPL появляется при чтении текущего MT5 position snapshot.
Validation event: FloatingManagedPL валидируется по managed identity и revision снимка.
Freeze/confirmation event: Фиксация относится только к конкретному snapshot revision.
Mutation events: Любое исполнение, partial close или position merge изменяет FloatingManagedPL.
Stale triggers: Любой trade event после snapshot немедленно делает FloatingManagedPL stale.
Replacement source: новый current MT5 position snapshot.
Terminal condition: После полного закрытия становится ZERO либо NOT_APPLICABLE согласно типу.
Persistence behavior: Live значение не заменяется persisted cache.
Restart behavior: После restart обязательно перечитывается из terminal state.
Отличие от: FloatingManagedPL отличается от sibling-терминов источником `current position or broker-aware price model`, классом `ACTUAL CURRENT` и стадией lifecycle `ACTUAL_POSITION`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ACTUAL_POSITION`; запись `FloatingManagedPL` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `FloatingManagedPL` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### ProjectedFloatingPL
CanonicalName: `ProjectedFloatingPL`
Русское название: Прогнозный плавающий pl
Краткое определение: ProjectedFloatingPL — денежная величина `ProjectedFloatingPL` класса `PROJECTED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Прогнозный плавающий pl»; его authoritative provenance — «OrderCalcProfit + explicit projected costs».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: ProjectedFloatingPL
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: signed
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для ProjectedFloatingPL.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: ProjectedFloatingPL вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs. Не мутирует; изменение inputs создаёт новую revision ProjectedFloatingPL. Market, symbol, config или snapshot revision делает ProjectedFloatingPL stale. пересчёт ProjectedFloatingPL на новом immutable snapshot. После execution projected ProjectedFloatingPL завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Прогнозный плавающий pl» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает ProjectedFloatingPL stale.
Authoritative replacement: пересчёт ProjectedFloatingPL на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: ProjectedFloatingPL нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ProjectedFloatingPL, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/StateMachine.mqh::projectedFarPL
Python mapping: NONE_FOUND
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: ProjectedFloatingPL вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs.
Validation event: ProjectedFloatingPL валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: ProjectedFloatingPL замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision ProjectedFloatingPL.
Stale triggers: Market, symbol, config или snapshot revision делает ProjectedFloatingPL stale.
Replacement source: пересчёт ProjectedFloatingPL на новом immutable snapshot.
Terminal condition: После execution projected ProjectedFloatingPL завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: ProjectedFloatingPL отличается от sibling-терминов источником `OrderCalcProfit + explicit projected costs`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `ProjectedFloatingPL` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ProjectedFloatingPL` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### RecoveryPLAnalytic
CanonicalName: `RecoveryPLAnalytic`
Русское название: Восстановление pl аналитический
Краткое определение: RecoveryPLAnalytic — денежная величина `RecoveryPL` класса `PROJECTED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Восстановление pl аналитический»; его authoritative provenance — «OrderCalcProfit + explicit projected costs».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: RecoveryPL
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: signed
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для RecoveryPLAnalytic.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: RecoveryPLAnalytic вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs. Не мутирует; изменение inputs создаёт новую revision RecoveryPLAnalytic. Market, symbol, config или snapshot revision делает RecoveryPLAnalytic stale. пересчёт RecoveryPLAnalytic на новом immutable snapshot. После execution projected RecoveryPLAnalytic завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Восстановление pl аналитический» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает RecoveryPLAnalytic stale.
Authoritative replacement: пересчёт RecoveryPLAnalytic на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: RecoveryPLAnalytic нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RecoveryPL, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Logger.mqh::recoveryPL
Python mapping: Tests/real_recovery_examples_check.py::recovery_pl
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: RecoveryPLAnalytic вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs.
Validation event: RecoveryPLAnalytic валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: RecoveryPLAnalytic замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision RecoveryPLAnalytic.
Stale triggers: Market, symbol, config или snapshot revision делает RecoveryPLAnalytic stale.
Replacement source: пересчёт RecoveryPLAnalytic на новом immutable snapshot.
Terminal condition: После execution projected RecoveryPLAnalytic завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: RecoveryPLAnalytic отличается от sibling-терминов источником `OrderCalcProfit + explicit projected costs`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `RecoveryPLAnalytic` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `RecoveryPLAnalytic` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### RecoveryPLProjected
CanonicalName: `RecoveryPLProjected`
Русское название: Восстановление pl прогнозный
Краткое определение: RecoveryPLProjected — денежная величина `RecoveryPL` класса `PROJECTED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Восстановление pl прогнозный»; его authoritative provenance — «OrderCalcProfit + explicit projected costs».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: RecoveryPL
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: signed
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для RecoveryPLProjected.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: RecoveryPLProjected вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs. Не мутирует; изменение inputs создаёт новую revision RecoveryPLProjected. Market, symbol, config или snapshot revision делает RecoveryPLProjected stale. пересчёт RecoveryPLProjected на новом immutable snapshot. После execution projected RecoveryPLProjected завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Восстановление pl прогнозный» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает RecoveryPLProjected stale.
Authoritative replacement: пересчёт RecoveryPLProjected на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: RecoveryPLProjected нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RecoveryPL, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Logger.mqh::recoveryPL
Python mapping: Tests/real_recovery_examples_check.py::recovery_pl
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: RecoveryPLProjected вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs.
Validation event: RecoveryPLProjected валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: RecoveryPLProjected замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision RecoveryPLProjected.
Stale triggers: Market, symbol, config или snapshot revision делает RecoveryPLProjected stale.
Replacement source: пересчёт RecoveryPLProjected на новом immutable snapshot.
Terminal condition: После execution projected RecoveryPLProjected завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: RecoveryPLProjected отличается от sibling-терминов источником `OrderCalcProfit + explicit projected costs`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `RecoveryPLProjected` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `RecoveryPLProjected` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### RecoveryPLCloseNow
CanonicalName: `RecoveryPLCloseNow`
Русское название: Восстановление pl закрытие сейчас
Краткое определение: RecoveryPLCloseNow — Projected broker-money result немедленного закрытия managed basket: RealizedCyclePL + FloatingManagedPL − ExpectedExitCosts без повторного Reserve. Отличительный объект записи: «Восстановление pl закрытие сейчас»; его authoritative provenance — «OrderCalcProfit + explicit projected costs».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: RecoveryPL
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: signed
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для RecoveryPLCloseNow.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: RecoveryPLCloseNow вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs. Не мутирует; изменение inputs создаёт новую revision RecoveryPLCloseNow. Market, symbol, config или snapshot revision делает RecoveryPLCloseNow stale. пересчёт RecoveryPLCloseNow на новом immutable snapshot. После execution projected RecoveryPLCloseNow завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Восстановление pl закрытие сейчас» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает RecoveryPLCloseNow stale.
Authoritative replacement: пересчёт RecoveryPLCloseNow на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: RecoveryPLCloseNow нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RecoveryPL, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Logger.mqh::recoveryPL
Python mapping: Tests/real_recovery_examples_check.py::recovery_pl
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: RecoveryPLCloseNow вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs.
Validation event: RecoveryPLCloseNow валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: RecoveryPLCloseNow замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision RecoveryPLCloseNow.
Stale triggers: Market, symbol, config или snapshot revision делает RecoveryPLCloseNow stale.
Replacement source: пересчёт RecoveryPLCloseNow на новом immutable snapshot.
Terminal condition: После execution projected RecoveryPLCloseNow завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: RecoveryPLCloseNow отличается от sibling-терминов источником `OrderCalcProfit + explicit projected costs`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `RecoveryPLCloseNow` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `RecoveryPLCloseNow` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### RealRecoveryPL
CanonicalName: `RealRecoveryPL`
Русское название: Подтверждённый восстановление pl
Краткое определение: RealRecoveryPL — денежная величина `RealRecoveryPL` класса `ACTUAL CONFIRMED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Подтверждённый восстановление pl»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: RealRecoveryPL
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: signed
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для RealRecoveryPL.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: RealRecoveryPL создаётся confirmed allocation/deal event с уникальным EventID. RealRecoveryPL меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Подтверждённый восстановление pl» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: RealRecoveryPL нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RealRecoveryPL, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: realRecoveryPL
MQL5 mapping: Include/StateMachine.mqh::CalcRealRecoveryPL
Python mapping: Tests/real_recovery_examples_check.py::recovery_pl
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: RealRecoveryPL создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: RealRecoveryPL проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: RealRecoveryPL меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: RealRecoveryPL отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `RealRecoveryPL` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `RealRecoveryPL` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### RecoverySlope
CanonicalName: `RecoverySlope`
Русское название: Восстановление наклон
Краткое определение: RecoverySlope — денежная величина `RecoverySlope` класса `PROJECTED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Восстановление наклон»; его authoritative provenance — «OrderCalcProfit + explicit projected costs».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: RecoverySlope
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: signed
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для RecoverySlope.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: RecoverySlope вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs. Не мутирует; изменение inputs создаёт новую revision RecoverySlope. Market, symbol, config или snapshot revision делает RecoverySlope stale. пересчёт RecoverySlope на новом immutable snapshot. После execution projected RecoverySlope завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Восстановление наклон» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает RecoverySlope stale.
Authoritative replacement: пересчёт RecoverySlope на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: RecoverySlope нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RecoverySlope, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Logger.mqh::recoveryPL
Python mapping: Tools/hybrid_geometry_model.py::recovery_slope
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: RecoverySlope вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs.
Validation event: RecoverySlope валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: RecoverySlope замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision RecoverySlope.
Stale triggers: Market, symbol, config или snapshot revision делает RecoverySlope stale.
Replacement source: пересчёт RecoverySlope на новом immutable snapshot.
Terminal condition: После execution projected RecoverySlope завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: RecoverySlope отличается от sibling-терминов источником `OrderCalcProfit + explicit projected costs`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `RecoverySlope` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `RecoverySlope` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### RecoveryMonotonicity
CanonicalName: `RecoveryMonotonicity`
Русское название: Восстановление монотонность
Краткое определение: RecoveryMonotonicity — денежная величина `RecoveryMonotonicity` класса `PROJECTED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Восстановление монотонность»; его authoritative provenance — «OrderCalcProfit + explicit projected costs».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: RecoveryMonotonicity
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для RecoveryMonotonicity.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: RecoveryMonotonicity вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs. Не мутирует; изменение inputs создаёт новую revision RecoveryMonotonicity. Market, symbol, config или snapshot revision делает RecoveryMonotonicity stale. пересчёт RecoveryMonotonicity на новом immutable snapshot. После execution projected RecoveryMonotonicity завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Восстановление монотонность» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает RecoveryMonotonicity stale.
Authoritative replacement: пересчёт RecoveryMonotonicity на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: RecoveryMonotonicity нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RecoveryMonotonicity, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: RecoveryMonotonicity вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs.
Validation event: RecoveryMonotonicity валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: RecoveryMonotonicity замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision RecoveryMonotonicity.
Stale triggers: Market, symbol, config или snapshot revision делает RecoveryMonotonicity stale.
Replacement source: пересчёт RecoveryMonotonicity на новом immutable snapshot.
Terminal condition: После execution projected RecoveryMonotonicity завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: RecoveryMonotonicity отличается от sibling-терминов источником `OrderCalcProfit + explicit projected costs`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `RecoveryMonotonicity` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `RecoveryMonotonicity` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### ExpectedExitCosts
CanonicalName: `ExpectedExitCosts`
Русское название: Ожидаемые выход расходы
Краткое определение: ExpectedExitCosts — денежная величина `ExpectedExitCosts` класса `PROJECTED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Ожидаемые выход расходы»; его authoritative provenance — «OrderCalcProfit + explicit projected costs».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: ExpectedExitCosts
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для ExpectedExitCosts.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: ExpectedExitCosts вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs. Не мутирует; изменение inputs создаёт новую revision ExpectedExitCosts. Market, symbol, config или snapshot revision делает ExpectedExitCosts stale. пересчёт ExpectedExitCosts на новом immutable snapshot. После execution projected ExpectedExitCosts завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Ожидаемые выход расходы» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает ExpectedExitCosts stale.
Authoritative replacement: пересчёт ExpectedExitCosts на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: ExpectedExitCosts нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ExpectedExitCosts, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: ExpectedExitCosts вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs.
Validation event: ExpectedExitCosts валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: ExpectedExitCosts замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision ExpectedExitCosts.
Stale triggers: Market, symbol, config или snapshot revision делает ExpectedExitCosts stale.
Replacement source: пересчёт ExpectedExitCosts на новом immutable snapshot.
Terminal condition: После execution projected ExpectedExitCosts завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: ExpectedExitCosts отличается от sibling-терминов источником `OrderCalcProfit + explicit projected costs`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `ExpectedExitCosts` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ExpectedExitCosts` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### CommissionCost
CanonicalName: `CommissionCost`
Русское название: Комиссия cost
Краткое определение: CommissionCost — денежная величина `CommissionCost` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Комиссия cost»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: CommissionCost
Размерность: `MONEY_COST`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_COST`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для CommissionCost.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: CommissionCost создаётся confirmed allocation/deal event с уникальным EventID. CommissionCost меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Комиссия cost» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_COST` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: CommissionCost нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CommissionCost, тип MONEY_COST, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::commission
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: CommissionCost создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: CommissionCost проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: CommissionCost меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: CommissionCost отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `CommissionCost` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `CommissionCost` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=PARTIAL_MATCH.

### SwapCost
CanonicalName: `SwapCost`
Русское название: Своп cost
Краткое определение: SwapCost — денежная величина `SwapCost` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Своп cost»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: SwapCost
Размерность: `MONEY_COST`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_COST`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для SwapCost.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: SwapCost создаётся confirmed allocation/deal event с уникальным EventID. SwapCost меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Своп cost» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_COST` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: SwapCost нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SwapCost, тип MONEY_COST, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/HybridPartialFarPreview.mqh::cost
Python mapping: NONE_FOUND
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: SwapCost создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: SwapCost проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: SwapCost меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: SwapCost отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `SwapCost` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `SwapCost` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### FeeCost
CanonicalName: `FeeCost`
Русское название: Сбор cost
Краткое определение: FeeCost — денежная величина `FeeCost` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Сбор cost»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: FeeCost
Размерность: `MONEY_COST`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_COST`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для FeeCost.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: FeeCost создаётся confirmed allocation/deal event с уникальным EventID. FeeCost меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Сбор cost» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_COST` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: FeeCost нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: FeeCost, тип MONEY_COST, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/HybridPartialFarPreview.mqh::cost
Python mapping: NONE_FOUND
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: FeeCost создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: FeeCost проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: FeeCost меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: FeeCost отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `FeeCost` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `FeeCost` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### SpreadCost
CanonicalName: `SpreadCost`
Русское название: Спред cost
Краткое определение: SpreadCost — денежная величина `SpreadCost` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Спред cost»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: SpreadCost
Размерность: `MONEY_COST`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_COST`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для SpreadCost.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: SpreadCost создаётся confirmed allocation/deal event с уникальным EventID. SpreadCost меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Спред cost» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_COST` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: SpreadCost нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SpreadCost, тип MONEY_COST, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: SpreadCost создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: SpreadCost проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: SpreadCost меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: SpreadCost отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `SpreadCost` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `SpreadCost` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### SlippageCost
CanonicalName: `SlippageCost`
Русское название: Проскальзывание cost
Краткое определение: SlippageCost — денежная величина `SlippageCost` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Проскальзывание cost»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: SlippageCost
Размерность: `MONEY_COST`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_COST`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для SlippageCost.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: SlippageCost создаётся confirmed allocation/deal event с уникальным EventID. SlippageCost меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Проскальзывание cost» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_COST` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: SlippageCost нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SlippageCost, тип MONEY_COST, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::slippage
Python mapping: Tests/unit/test_big_small_behavior.py::slippage
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: SlippageCost создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: SlippageCost проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: SlippageCost меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: SlippageCost отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `SlippageCost` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `SlippageCost` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### PositionPLSigned
CanonicalName: `PositionPLSigned`
Русское название: Позиция pl со знаком
Краткое определение: PositionPLSigned — денежная величина `Position` класса `ACTUAL CURRENT` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Позиция pl со знаком»; его authoritative provenance — «current position or broker-aware price model».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: Position
Размерность: `MONEY_FLOATING`
Unit: `account money`
Знак: signed
Допустимый диапазон: соответствует типу `MONEY_FLOATING`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: current position or broker-aware price model
Authoritative source: current position or broker-aware price model
Время фиксации: ACTUAL CURRENT stage для PositionPLSigned.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: PositionPLSigned появляется при чтении текущего MT5 position snapshot. Любое исполнение, partial close или position merge изменяет PositionPLSigned. Любой trade event после snapshot немедленно делает PositionPLSigned stale. новый current MT5 position snapshot. После полного закрытия становится ZERO либо NOT_APPLICABLE согласно типу. Этот lifecycle относится именно к объекту «Позиция pl со знаком» и его собственному type/source contract.
Условия stale: Любой trade event после snapshot немедленно делает PositionPLSigned stale.
Authoritative replacement: новый current MT5 position snapshot.
Допустимые операции: сравнение и преобразование только по `MONEY_FLOATING` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: PositionPLSigned нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Position, тип MONEY_FLOATING, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: Include/SimulationEngine.mqh::SimSignedPositionPL
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: ACTUAL_POSITION
Creation event: PositionPLSigned появляется при чтении текущего MT5 position snapshot.
Validation event: PositionPLSigned валидируется по managed identity и revision снимка.
Freeze/confirmation event: Фиксация относится только к конкретному snapshot revision.
Mutation events: Любое исполнение, partial close или position merge изменяет PositionPLSigned.
Stale triggers: Любой trade event после snapshot немедленно делает PositionPLSigned stale.
Replacement source: новый current MT5 position snapshot.
Terminal condition: После полного закрытия становится ZERO либо NOT_APPLICABLE согласно типу.
Persistence behavior: Live значение не заменяется persisted cache.
Restart behavior: После restart обязательно перечитывается из terminal state.
Отличие от: PositionPLSigned отличается от sibling-терминов источником `current position or broker-aware price model`, классом `ACTUAL CURRENT` и стадией lifecycle `ACTUAL_POSITION`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ACTUAL_POSITION`; запись `PositionPLSigned` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `PositionPLSigned` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### FarLossSigned
CanonicalName: `FarLossSigned`
Русское название: Хвостовая позиция убыток со знаком
Краткое определение: FarLossSigned — денежная величина `Far` класса `ACTUAL CONFIRMED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Хвостовая позиция убыток со знаком»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: Far
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: signed
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для FarLossSigned.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: FarLossSigned создаётся confirmed allocation/deal event с уникальным EventID. FarLossSigned меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Хвостовая позиция убыток со знаком» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: FarLossSigned нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Far, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::farLoss
Python mapping: NONE_FOUND
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: FarLossSigned создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: FarLossSigned проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: FarLossSigned меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: FarLossSigned отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `FarLossSigned` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `FarLossSigned` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### FarLossMagnitude
CanonicalName: `FarLossMagnitude`
Русское название: Хвостовая позиция убыток модуль
Краткое определение: FarLossMagnitude — денежная величина `Far` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Хвостовая позиция убыток модуль»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: Far
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для FarLossMagnitude.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: FarLossMagnitude создаётся confirmed allocation/deal event с уникальным EventID. FarLossMagnitude меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Хвостовая позиция убыток модуль» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: FarLossMagnitude нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Far, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::farLossAfter
Python mapping: Tools/hybrid_big_sequence_model.py::far_loss_after
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: FarLossMagnitude создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: FarLossMagnitude проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: FarLossMagnitude меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: FarLossMagnitude отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `FarLossMagnitude` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `FarLossMagnitude` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### PartialFarBudgetProjected
CanonicalName: `PartialFarBudgetProjected`
Русское название: Частичный хвостовая позиция бюджет прогнозный
Краткое определение: PartialFarBudgetProjected — денежная величина `PartialFarBudgetProjected` класса `PROJECTED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Частичный хвостовая позиция бюджет прогнозный»; его authoritative provenance — «OrderCalcProfit + explicit projected costs».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: PartialFarBudgetProjected
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для PartialFarBudgetProjected.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: PartialFarBudgetProjected вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs. Не мутирует; изменение inputs создаёт новую revision PartialFarBudgetProjected. Market, symbol, config или snapshot revision делает PartialFarBudgetProjected stale. пересчёт PartialFarBudgetProjected на новом immutable snapshot. После execution projected PartialFarBudgetProjected завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Частичный хвостовая позиция бюджет прогнозный» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает PartialFarBudgetProjected stale.
Authoritative replacement: пересчёт PartialFarBudgetProjected на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: PartialFarBudgetProjected нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PartialFarBudgetProjected, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: Tools/hybrid_big_sequence_model.py::partial_budget
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: PartialFarBudgetProjected вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs.
Validation event: PartialFarBudgetProjected валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: PartialFarBudgetProjected замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision PartialFarBudgetProjected.
Stale triggers: Market, symbol, config или snapshot revision делает PartialFarBudgetProjected stale.
Replacement source: пересчёт PartialFarBudgetProjected на новом immutable snapshot.
Terminal condition: После execution projected PartialFarBudgetProjected завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: PartialFarBudgetProjected отличается от sibling-терминов источником `OrderCalcProfit + explicit projected costs`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `PartialFarBudgetProjected` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `PartialFarBudgetProjected` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=PARTIAL_MATCH.

### PartialFarBudgetReal
CanonicalName: `PartialFarBudgetReal`
Русское название: Частичный хвостовая позиция бюджет подтверждённый
Краткое определение: PartialFarBudgetReal — денежная величина `PartialFarBudgetReal` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Частичный хвостовая позиция бюджет подтверждённый»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: PartialFarBudgetReal
Размерность: `MONEY_RESERVED`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_RESERVED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для PartialFarBudgetReal.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: PartialFarBudgetReal создаётся confirmed allocation/deal event с уникальным EventID. PartialFarBudgetReal меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Частичный хвостовая позиция бюджет подтверждённый» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_RESERVED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: PartialFarBudgetReal нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PartialFarBudgetReal, тип MONEY_RESERVED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::partialBudgetBefore
Python mapping: Tools/hybrid_big_sequence_model.py::partial_budget
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: PartialFarBudgetReal создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: PartialFarBudgetReal проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: PartialFarBudgetReal меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: PartialFarBudgetReal отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `PartialFarBudgetReal` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `PartialFarBudgetReal` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### PartialFarBudgetAvailable
CanonicalName: `PartialFarBudgetAvailable`
Русское название: Частичный хвостовая позиция бюджет доступный
Краткое определение: PartialFarBudgetAvailable — денежная величина `PartialFarBudgetAvailable` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Частичный хвостовая позиция бюджет доступный»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: PartialFarBudgetAvailable
Размерность: `MONEY_AVAILABLE`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_AVAILABLE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для PartialFarBudgetAvailable.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: PartialFarBudgetAvailable создаётся confirmed allocation/deal event с уникальным EventID. PartialFarBudgetAvailable меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Частичный хвостовая позиция бюджет доступный» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_AVAILABLE` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: PartialFarBudgetAvailable нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PartialFarBudgetAvailable, тип MONEY_AVAILABLE, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/HybridPartialFarPreview.mqh::budgetAvailable
Python mapping: Tools/hybrid_big_sequence_model.py::partial_budget
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: PartialFarBudgetAvailable создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: PartialFarBudgetAvailable проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: PartialFarBudgetAvailable меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: PartialFarBudgetAvailable отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `PartialFarBudgetAvailable` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `PartialFarBudgetAvailable` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### PartialFarBudgetConsumed
CanonicalName: `PartialFarBudgetConsumed`
Русское название: Частичный хвостовая позиция бюджет израсходованный
Краткое определение: PartialFarBudgetConsumed — денежная величина `PartialFarBudgetConsumed` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Частичный хвостовая позиция бюджет израсходованный»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: PartialFarBudgetConsumed
Размерность: `MONEY_CONSUMED`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_CONSUMED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для PartialFarBudgetConsumed.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: PartialFarBudgetConsumed создаётся confirmed allocation/deal event с уникальным EventID. PartialFarBudgetConsumed меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Частичный хвостовая позиция бюджет израсходованный» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_CONSUMED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: PartialFarBudgetConsumed нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PartialFarBudgetConsumed, тип MONEY_CONSUMED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: Tools/hybrid_big_sequence_model.py::partial_budget
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: PartialFarBudgetConsumed создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: PartialFarBudgetConsumed проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: PartialFarBudgetConsumed меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: PartialFarBudgetConsumed отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `PartialFarBudgetConsumed` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `PartialFarBudgetConsumed` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=PARTIAL_MATCH.

### PartialFarBudgetResidual
CanonicalName: `PartialFarBudgetResidual`
Русское название: Частичный хвостовая позиция бюджет остаточная
Краткое определение: PartialFarBudgetResidual — денежная величина `PartialFarBudgetResidual` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Частичный хвостовая позиция бюджет остаточная»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: PartialFarBudgetResidual
Размерность: `MONEY_RESIDUAL`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_RESIDUAL`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для PartialFarBudgetResidual.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: PartialFarBudgetResidual создаётся confirmed allocation/deal event с уникальным EventID. PartialFarBudgetResidual меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Частичный хвостовая позиция бюджет остаточная» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_RESIDUAL` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: PartialFarBudgetResidual нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PartialFarBudgetResidual, тип MONEY_RESIDUAL, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: Tools/hybrid_big_sequence_model.py::partial_budget
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: PartialFarBudgetResidual создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: PartialFarBudgetResidual проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: PartialFarBudgetResidual меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: PartialFarBudgetResidual отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `PartialFarBudgetResidual` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `PartialFarBudgetResidual` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=PARTIAL_MATCH.

### FinalReserveProjected
CanonicalName: `FinalReserveProjected`
Русское название: Финальный резерв прогнозный
Краткое определение: FinalReserveProjected — денежная величина `FinalReserveProjected` класса `PROJECTED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Финальный резерв прогнозный»; его authoritative provenance — «OrderCalcProfit + explicit projected costs».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: FinalReserveProjected
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для FinalReserveProjected.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: FinalReserveProjected вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs. Не мутирует; изменение inputs создаёт новую revision FinalReserveProjected. Market, symbol, config или snapshot revision делает FinalReserveProjected stale. пересчёт FinalReserveProjected на новом immutable snapshot. После execution projected FinalReserveProjected завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Финальный резерв прогнозный» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает FinalReserveProjected stale.
Authoritative replacement: пересчёт FinalReserveProjected на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: FinalReserveProjected нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: FinalReserveProjected, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::finalReserveReal
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::final_reserve_real
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: FinalReserveProjected вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs.
Validation event: FinalReserveProjected валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: FinalReserveProjected замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision FinalReserveProjected.
Stale triggers: Market, symbol, config или snapshot revision делает FinalReserveProjected stale.
Replacement source: пересчёт FinalReserveProjected на новом immutable snapshot.
Terminal condition: После execution projected FinalReserveProjected завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: FinalReserveProjected отличается от sibling-терминов источником `OrderCalcProfit + explicit projected costs`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `FinalReserveProjected` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `FinalReserveProjected` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### FinalReserveReal
CanonicalName: `FinalReserveReal`
Русское название: Финальный резерв подтверждённый
Краткое определение: FinalReserveReal — Фактически подтверждённый Reserve bucket: увеличивается exactly-once realized allocation и уменьшается confirmed consumption; projected reserve его не заменяет. Отличительный объект записи: «Финальный резерв подтверждённый»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: FinalReserveReal
Размерность: `MONEY_RESERVED`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_RESERVED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для FinalReserveReal.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: FinalReserveReal создаётся confirmed allocation/deal event с уникальным EventID. FinalReserveReal меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Финальный резерв подтверждённый» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_RESERVED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: FinalReserveReal нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: FinalReserveReal, тип MONEY_RESERVED, class ACTUAL CONFIRMED.
Legacy aliases: TotalReserve, finalReserveReal
MQL5 mapping: Include/Types.mqh::finalReserveReal
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::final_reserve_real
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: FinalReserveReal создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: FinalReserveReal проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: FinalReserveReal меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: FinalReserveReal отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `FinalReserveReal` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `FinalReserveReal` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### ReserveAddProjected
CanonicalName: `ReserveAddProjected`
Русское название: Резерв начисление прогнозный
Краткое определение: ReserveAddProjected — денежная величина `Reserve` класса `PROJECTED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Резерв начисление прогнозный»; его authoritative provenance — «OrderCalcProfit + explicit projected costs».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: Reserve
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для ReserveAddProjected.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: ReserveAddProjected вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs. Не мутирует; изменение inputs создаёт новую revision ReserveAddProjected. Market, symbol, config или snapshot revision делает ReserveAddProjected stale. пересчёт ReserveAddProjected на новом immutable snapshot. После execution projected ReserveAddProjected завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Резерв начисление прогнозный» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает ReserveAddProjected stale.
Authoritative replacement: пересчёт ReserveAddProjected на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: ReserveAddProjected нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Reserve, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::reserveAdd
Python mapping: Tools/optimize_big_scenario_min_levels.py::reserve_add
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: ReserveAddProjected вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs.
Validation event: ReserveAddProjected валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: ReserveAddProjected замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision ReserveAddProjected.
Stale triggers: Market, symbol, config или snapshot revision делает ReserveAddProjected stale.
Replacement source: пересчёт ReserveAddProjected на новом immutable snapshot.
Terminal condition: После execution projected ReserveAddProjected завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: ReserveAddProjected отличается от sibling-терминов источником `OrderCalcProfit + explicit projected costs`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `ReserveAddProjected` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ReserveAddProjected` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### ReserveAddReal
CanonicalName: `ReserveAddReal`
Русское название: Резерв начисление подтверждённый
Краткое определение: ReserveAddReal — денежная величина `Reserve` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Резерв начисление подтверждённый»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: Reserve
Размерность: `MONEY_RESERVED`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_RESERVED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для ReserveAddReal.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: ReserveAddReal создаётся confirmed allocation/deal event с уникальным EventID. ReserveAddReal меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Резерв начисление подтверждённый» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_RESERVED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: ReserveAddReal нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Reserve, тип MONEY_RESERVED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::reserveAdd
Python mapping: Tools/optimize_big_scenario_min_levels.py::reserve_add
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: ReserveAddReal создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: ReserveAddReal проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: ReserveAddReal меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: ReserveAddReal отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `ReserveAddReal` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ReserveAddReal` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### ReserveAvailable
CanonicalName: `ReserveAvailable`
Русское название: Резерв доступный
Краткое определение: ReserveAvailable — денежная величина `Reserve` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Резерв доступный»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: Reserve
Размерность: `MONEY_AVAILABLE`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_AVAILABLE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для ReserveAvailable.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: ReserveAvailable создаётся confirmed allocation/deal event с уникальным EventID. ReserveAvailable меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Резерв доступный» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_AVAILABLE` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: ReserveAvailable нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Reserve, тип MONEY_AVAILABLE, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: ReserveAvailable создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: ReserveAvailable проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: ReserveAvailable меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: ReserveAvailable отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `ReserveAvailable` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ReserveAvailable` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### ReserveConsumed
CanonicalName: `ReserveConsumed`
Русское название: Резерв израсходованный
Краткое определение: ReserveConsumed — денежная величина `Reserve` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Резерв израсходованный»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: Reserve
Размерность: `MONEY_CONSUMED`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_CONSUMED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для ReserveConsumed.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: ReserveConsumed создаётся confirmed allocation/deal event с уникальным EventID. ReserveConsumed меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Резерв израсходованный» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_CONSUMED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: ReserveConsumed нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Reserve, тип MONEY_CONSUMED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/StateMachine.mqh::reserveUsed
Python mapping: NONE_FOUND
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: ReserveConsumed создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: ReserveConsumed проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: ReserveConsumed меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: ReserveConsumed отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `ReserveConsumed` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ReserveConsumed` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### ReserveResidual
CanonicalName: `ReserveResidual`
Русское название: Резерв остаточная
Краткое определение: ReserveResidual — денежная величина `Reserve` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Резерв остаточная»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: Reserve
Размерность: `MONEY_RESIDUAL`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_RESIDUAL`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для ReserveResidual.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: ReserveResidual создаётся confirmed allocation/deal event с уникальным EventID. ReserveResidual меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Резерв остаточная» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_RESIDUAL` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: ReserveResidual нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Reserve, тип MONEY_RESIDUAL, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: ReserveResidual создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: ReserveResidual проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: ReserveResidual меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: ReserveResidual отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `ReserveResidual` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ReserveResidual` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### CarryAvailable
CanonicalName: `CarryAvailable`
Русское название: Переносимый остаток доступный
Краткое определение: CarryAvailable — денежная величина `Carry` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Переносимый остаток доступный»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: Carry
Размерность: `MONEY_AVAILABLE`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_AVAILABLE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для CarryAvailable.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: CarryAvailable создаётся confirmed allocation/deal event с уникальным EventID. CarryAvailable меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Переносимый остаток доступный» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_AVAILABLE` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: CarryAvailable нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Carry, тип MONEY_AVAILABLE, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: CarryAvailable создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: CarryAvailable проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: CarryAvailable меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: CarryAvailable отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `CarryAvailable` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `CarryAvailable` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### CarryConsumed
CanonicalName: `CarryConsumed`
Русское название: Переносимый остаток израсходованный
Краткое определение: CarryConsumed — денежная величина `Carry` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Переносимый остаток израсходованный»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: Carry
Размерность: `MONEY_CONSUMED`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_CONSUMED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для CarryConsumed.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: CarryConsumed создаётся confirmed allocation/deal event с уникальным EventID. CarryConsumed меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Переносимый остаток израсходованный» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_CONSUMED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: CarryConsumed нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Carry, тип MONEY_CONSUMED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: CarryConsumed создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: CarryConsumed проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: CarryConsumed меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: CarryConsumed отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `CarryConsumed` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `CarryConsumed` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### CarryResidual
CanonicalName: `CarryResidual`
Русское название: Переносимый остаток остаточная
Краткое определение: CarryResidual — денежная величина `Carry` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Переносимый остаток остаточная»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: Carry
Размерность: `MONEY_RESIDUAL`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_RESIDUAL`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для CarryResidual.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: CarryResidual создаётся confirmed allocation/deal event с уникальным EventID. CarryResidual меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Переносимый остаток остаточная» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_RESIDUAL` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: CarryResidual нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Carry, тип MONEY_RESIDUAL, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: CarryResidual создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: CarryResidual проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: CarryResidual меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: CarryResidual отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `CarryResidual` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `CarryResidual` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### TransitionBudgetAvailable
CanonicalName: `TransitionBudgetAvailable`
Русское название: Переход бюджет доступный
Краткое определение: TransitionBudgetAvailable — денежная величина `TransitionBudget` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Переход бюджет доступный»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: TransitionBudget
Размерность: `MONEY_AVAILABLE`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_AVAILABLE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для TransitionBudgetAvailable.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: TransitionBudgetAvailable создаётся confirmed allocation/deal event с уникальным EventID. TransitionBudgetAvailable меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Переход бюджет доступный» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_AVAILABLE` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: TransitionBudgetAvailable нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: TransitionBudget, тип MONEY_AVAILABLE, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/HybridPartialFarPreview.mqh::budgetAvailable
Python mapping: Tools/hybrid_geometry_model.py::transition_budget
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: TransitionBudgetAvailable создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: TransitionBudgetAvailable проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: TransitionBudgetAvailable меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: TransitionBudgetAvailable отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `TransitionBudgetAvailable` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `TransitionBudgetAvailable` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### FinalCloseRequirement
CanonicalName: `FinalCloseRequirement`
Русское название: Финальный закрытие требование
Краткое определение: FinalCloseRequirement — денежная величина `FinalCloseRequirement` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Финальный закрытие требование»; его authoritative provenance — «confirmed deal history / exactly-once ledger».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: FinalCloseRequirement
Размерность: `MONEY_RESERVED`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_RESERVED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для FinalCloseRequirement.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: FinalCloseRequirement создаётся confirmed allocation/deal event с уникальным EventID. FinalCloseRequirement меняется только новым confirmed consumption/allocation event. Несогласованность ledger с deal history помечает derived balance stale. reconciled ledger, построенный из persisted events и confirmed deals. Закрытие cycle запрещает новые события, сохраняя историю. Этот lifecycle относится именно к объекту «Финальный закрытие требование» и его собственному type/source contract.
Условия stale: Несогласованность ledger с deal history помечает derived balance stale.
Authoritative replacement: reconciled ledger, построенный из persisted events и confirmed deals.
Допустимые операции: сравнение и преобразование только по `MONEY_RESERVED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: FinalCloseRequirement нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: FinalCloseRequirement, тип MONEY_RESERVED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: LEDGER
Creation event: FinalCloseRequirement создаётся confirmed allocation/deal event с уникальным EventID.
Validation event: FinalCloseRequirement проверяется против deal history и cycle scope.
Freeze/confirmation event: Ledger commit выполняется exactly once по fingerprint.
Mutation events: FinalCloseRequirement меняется только новым confirmed consumption/allocation event.
Stale triggers: Несогласованность ledger с deal history помечает derived balance stale.
Replacement source: reconciled ledger, построенный из persisted events и confirmed deals.
Terminal condition: Закрытие cycle запрещает новые события, сохраняя историю.
Persistence behavior: Persisted exactly-once event является обязательным.
Restart behavior: После restart выполняется ledger/deal reconciliation; projected value не принимается.
Отличие от: FinalCloseRequirement отличается от sibling-терминов источником `confirmed deal history / exactly-once ledger`, классом `ACTUAL CONFIRMED` и стадией lifecycle `LEDGER`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `LEDGER`; запись `FinalCloseRequirement` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `FinalCloseRequirement` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### BasketRiskMoney
CanonicalName: `BasketRiskMoney`
Русское название: Корзина риск денежный
Краткое определение: BasketRiskMoney — денежная величина `BasketRiskMoney` класса `PROJECTED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Корзина риск денежный»; его authoritative provenance — «OrderCalcProfit + explicit projected costs».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: BasketRiskMoney
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для BasketRiskMoney.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: BasketRiskMoney вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs. Не мутирует; изменение inputs создаёт новую revision BasketRiskMoney. Market, symbol, config или snapshot revision делает BasketRiskMoney stale. пересчёт BasketRiskMoney на новом immutable snapshot. После execution projected BasketRiskMoney завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Корзина риск денежный» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает BasketRiskMoney stale.
Authoritative replacement: пересчёт BasketRiskMoney на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: BasketRiskMoney нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BasketRiskMoney, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: BasketRiskMoney вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs.
Validation event: BasketRiskMoney валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: BasketRiskMoney замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision BasketRiskMoney.
Stale triggers: Market, symbol, config или snapshot revision делает BasketRiskMoney stale.
Replacement source: пересчёт BasketRiskMoney на новом immutable snapshot.
Terminal condition: После execution projected BasketRiskMoney завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: BasketRiskMoney отличается от sibling-терминов источником `OrderCalcProfit + explicit projected costs`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `BasketRiskMoney` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `BasketRiskMoney` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### AccountRiskMoney
CanonicalName: `AccountRiskMoney`
Русское название: Счёт риск денежный
Краткое определение: AccountRiskMoney — денежная величина `AccountRiskMoney` класса `PROJECTED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Счёт риск денежный»; его authoritative provenance — «OrderCalcProfit + explicit projected costs».
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: AccountRiskMoney
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для AccountRiskMoney.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: AccountRiskMoney вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs. Не мутирует; изменение inputs создаёт новую revision AccountRiskMoney. Market, symbol, config или snapshot revision делает AccountRiskMoney stale. пересчёт AccountRiskMoney на новом immutable snapshot. После execution projected AccountRiskMoney завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Счёт риск денежный» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает AccountRiskMoney stale.
Authoritative replacement: пересчёт AccountRiskMoney на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: AccountRiskMoney нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: AccountRiskMoney, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: AccountRiskMoney вычисляется из snapshot inputs: OrderCalcProfit + explicit projected costs.
Validation event: AccountRiskMoney валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: AccountRiskMoney замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision AccountRiskMoney.
Stale triggers: Market, symbol, config или snapshot revision делает AccountRiskMoney stale.
Replacement source: пересчёт AccountRiskMoney на новом immutable snapshot.
Terminal condition: После execution projected AccountRiskMoney завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: AccountRiskMoney отличается от sibling-терминов источником `OrderCalcProfit + explicit projected costs`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `AccountRiskMoney` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `AccountRiskMoney` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### BigRatio
CanonicalName: `BigRatio`
Русское название: Компенсирующая позиция отношение
Краткое определение: BigRatio — безразмерная величина типа `RATIO` для BigRatio; она не интерпретируется как lot, money или percent без явной conversion. Отличительный объект записи: «Компенсирующая позиция отношение»; его authoritative provenance — «approved profile or typed formula».
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: BigRatio
Размерность: `RATIO`
Unit: `1 (dimensionless)`
Знак: >= 0
Допустимый диапазон: соответствует типу `RATIO`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для BigRatio.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: BigRatio загружается из выбранного документального/конфигурационного профиля. Внутри замороженного цикла BigRatio не изменяется; новая ревизия относится к новому plan. Изменение профиля или revision делает прежний BigRatio stale. новое approved значение BigRatio из явно выбранного профиля. Завершается вместе с конфигурационным scope цикла. Этот lifecycle относится именно к объекту «Компенсирующая позиция отношение» и его собственному type/source contract.
Условия stale: Изменение профиля или revision делает прежний BigRatio stale.
Authoritative replacement: новое approved значение BigRatio из явно выбранного профиля.
Допустимые операции: сравнение и преобразование только по `RATIO` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: BigRatio нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigRatio, тип RATIO, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/RecoveryMath.mqh::bigRatio
Python mapping: Tests/small_reverse_compression_check.py::big_ratio
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `HSB-DOC-CONFLICT-001`
Resolution stage: `3.1.7`
Статус определения: `UNRESOLVED_PARAMETER_PROFILE`
Semantic category: POLICY
Lifecycle class: POLICY
Creation event: BigRatio загружается из выбранного документального/конфигурационного профиля.
Validation event: BigRatio проверяется как POLICY до фиксации цикла.
Freeze/confirmation event: BigRatio замораживается в конфигурации конкретного CycleID.
Mutation events: Внутри замороженного цикла BigRatio не изменяется; новая ревизия относится к новому plan.
Stale triggers: Изменение профиля или revision делает прежний BigRatio stale.
Replacement source: новое approved значение BigRatio из явно выбранного профиля.
Terminal condition: Завершается вместе с конфигурационным scope цикла.
Persistence behavior: Хранится с profile revision и CycleID.
Restart behavior: После restart перечитывается и сверяется с frozen cycle configuration.
Отличие от: BigRatio отличается от sibling-терминов источником `approved profile or typed formula`, классом `POLICY/PROJECTED` и стадией lifecycle `POLICY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `POLICY`; запись `BigRatio` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `BigRatio` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### SmallRatio
CanonicalName: `SmallRatio`
Русское название: Защитная позиция отношение
Краткое определение: SmallRatio — безразмерная величина типа `RATIO` для SmallRatio; она не интерпретируется как lot, money или percent без явной conversion. Отличительный объект записи: «Защитная позиция отношение»; его authoritative provenance — «approved profile or typed formula».
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: SmallRatio
Размерность: `RATIO`
Unit: `1 (dimensionless)`
Знак: >= 0
Допустимый диапазон: соответствует типу `RATIO`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для SmallRatio.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: SmallRatio загружается из выбранного документального/конфигурационного профиля. Внутри замороженного цикла SmallRatio не изменяется; новая ревизия относится к новому plan. Изменение профиля или revision делает прежний SmallRatio stale. новое approved значение SmallRatio из явно выбранного профиля. Завершается вместе с конфигурационным scope цикла. Этот lifecycle относится именно к объекту «Защитная позиция отношение» и его собственному type/source contract.
Условия stale: Изменение профиля или revision делает прежний SmallRatio stale.
Authoritative replacement: новое approved значение SmallRatio из явно выбранного профиля.
Допустимые операции: сравнение и преобразование только по `RATIO` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: SmallRatio нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SmallRatio, тип RATIO, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Config.mqh::SmallRatio
Python mapping: Tests/small_reverse_compression_check.py::small_ratio
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `HSB-DOC-CONFLICT-002`
Resolution stage: `3.1.7`
Статус определения: `UNRESOLVED_PARAMETER_PROFILE`
Semantic category: POLICY
Lifecycle class: POLICY
Creation event: SmallRatio загружается из выбранного документального/конфигурационного профиля.
Validation event: SmallRatio проверяется как POLICY до фиксации цикла.
Freeze/confirmation event: SmallRatio замораживается в конфигурации конкретного CycleID.
Mutation events: Внутри замороженного цикла SmallRatio не изменяется; новая ревизия относится к новому plan.
Stale triggers: Изменение профиля или revision делает прежний SmallRatio stale.
Replacement source: новое approved значение SmallRatio из явно выбранного профиля.
Terminal condition: Завершается вместе с конфигурационным scope цикла.
Persistence behavior: Хранится с profile revision и CycleID.
Restart behavior: После restart перечитывается и сверяется с frozen cycle configuration.
Отличие от: SmallRatio отличается от sibling-терминов источником `approved profile or typed formula`, классом `POLICY/PROJECTED` и стадией lifecycle `POLICY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `POLICY`; запись `SmallRatio` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `SmallRatio` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### CloseBigOnSmallShare
CanonicalName: `CloseBigOnSmallShare`
Русское название: Закрытие компенсирующая позиция on защитная позиция доля
Краткое определение: CloseBigOnSmallShare — безразмерная величина типа `SHARE` для CloseBigOnSmallShare; она не интерпретируется как lot, money или percent без явной conversion. Отличительный объект записи: «Закрытие компенсирующая позиция on защитная позиция доля»; его authoritative provenance — «approved profile or typed formula».
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: CloseBigOnSmallShare
Размерность: `SHARE`
Unit: `1 (dimensionless)`
Знак: >= 0
Допустимый диапазон: соответствует типу `SHARE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для CloseBigOnSmallShare.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: CloseBigOnSmallShare загружается из выбранного документального/конфигурационного профиля. Внутри замороженного цикла CloseBigOnSmallShare не изменяется; новая ревизия относится к новому plan. Изменение профиля или revision делает прежний CloseBigOnSmallShare stale. новое approved значение CloseBigOnSmallShare из явно выбранного профиля. Завершается вместе с конфигурационным scope цикла. Этот lifecycle относится именно к объекту «Закрытие компенсирующая позиция on защитная позиция доля» и его собственному type/source contract.
Условия stale: Изменение профиля или revision делает прежний CloseBigOnSmallShare stale.
Authoritative replacement: новое approved значение CloseBigOnSmallShare из явно выбранного профиля.
Допустимые операции: сравнение и преобразование только по `SHARE` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: CloseBigOnSmallShare нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CloseBigOnSmallShare, тип SHARE, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Config.mqh::CloseBigOnSmall
Python mapping: Tests/small_reverse_compression_check.py::close_big_on_small
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `HSB-DOC-CONFLICT-003`
Resolution stage: `3.1.7`
Статус определения: `UNRESOLVED_PARAMETER_PROFILE`
Semantic category: POLICY
Lifecycle class: POLICY
Creation event: CloseBigOnSmallShare загружается из выбранного документального/конфигурационного профиля.
Validation event: CloseBigOnSmallShare проверяется как POLICY до фиксации цикла.
Freeze/confirmation event: CloseBigOnSmallShare замораживается в конфигурации конкретного CycleID.
Mutation events: Внутри замороженного цикла CloseBigOnSmallShare не изменяется; новая ревизия относится к новому plan.
Stale triggers: Изменение профиля или revision делает прежний CloseBigOnSmallShare stale.
Replacement source: новое approved значение CloseBigOnSmallShare из явно выбранного профиля.
Terminal condition: Завершается вместе с конфигурационным scope цикла.
Persistence behavior: Хранится с profile revision и CycleID.
Restart behavior: После restart перечитывается и сверяется с frozen cycle configuration.
Отличие от: CloseBigOnSmallShare отличается от sibling-терминов источником `approved profile or typed formula`, классом `POLICY/PROJECTED` и стадией lifecycle `POLICY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `POLICY`; запись `CloseBigOnSmallShare` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `CloseBigOnSmallShare` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### RemainBigOnSmallShare
CanonicalName: `RemainBigOnSmallShare`
Русское название: Remain компенсирующая позиция on защитная позиция доля
Краткое определение: RemainBigOnSmallShare — безразмерная величина типа `SHARE` для RemainBigOnSmallShare; она не интерпретируется как lot, money или percent без явной conversion. Отличительный объект записи: «Remain компенсирующая позиция on защитная позиция доля»; его authoritative provenance — «approved profile or typed formula».
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: RemainBigOnSmallShare
Размерность: `SHARE`
Unit: `1 (dimensionless)`
Знак: >= 0
Допустимый диапазон: соответствует типу `SHARE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для RemainBigOnSmallShare.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: RemainBigOnSmallShare загружается из выбранного документального/конфигурационного профиля. Внутри замороженного цикла RemainBigOnSmallShare не изменяется; новая ревизия относится к новому plan. Изменение профиля или revision делает прежний RemainBigOnSmallShare stale. новое approved значение RemainBigOnSmallShare из явно выбранного профиля. Завершается вместе с конфигурационным scope цикла. Этот lifecycle относится именно к объекту «Remain компенсирующая позиция on защитная позиция доля» и его собственному type/source contract.
Условия stale: Изменение профиля или revision делает прежний RemainBigOnSmallShare stale.
Authoritative replacement: новое approved значение RemainBigOnSmallShare из явно выбранного профиля.
Допустимые операции: сравнение и преобразование только по `SHARE` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: RemainBigOnSmallShare нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RemainBigOnSmallShare, тип SHARE, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/RecoveryMath.mqh::remainBigOnSmall
Python mapping: Tests/small_reverse_compression_check.py::remain_big_on_small
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `HSB-DOC-CONFLICT-004`
Resolution stage: `3.1.7`
Статус определения: `UNRESOLVED_PARAMETER_PROFILE`
Semantic category: POLICY
Lifecycle class: POLICY
Creation event: RemainBigOnSmallShare загружается из выбранного документального/конфигурационного профиля.
Validation event: RemainBigOnSmallShare проверяется как POLICY до фиксации цикла.
Freeze/confirmation event: RemainBigOnSmallShare замораживается в конфигурации конкретного CycleID.
Mutation events: Внутри замороженного цикла RemainBigOnSmallShare не изменяется; новая ревизия относится к новому plan.
Stale triggers: Изменение профиля или revision делает прежний RemainBigOnSmallShare stale.
Replacement source: новое approved значение RemainBigOnSmallShare из явно выбранного профиля.
Terminal condition: Завершается вместе с конфигурационным scope цикла.
Persistence behavior: Хранится с profile revision и CycleID.
Restart behavior: После restart перечитывается и сверяется с frozen cycle configuration.
Отличие от: RemainBigOnSmallShare отличается от sibling-терминов источником `approved profile or typed formula`, классом `POLICY/PROJECTED` и стадией lifecycle `POLICY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `POLICY`; запись `RemainBigOnSmallShare` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `RemainBigOnSmallShare` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### CloseFarShare
CanonicalName: `CloseFarShare`
Русское название: Закрытие хвостовая позиция доля
Краткое определение: CloseFarShare — безразмерная величина типа `SHARE` для CloseFarShare; она не интерпретируется как lot, money или percent без явной conversion. Отличительный объект записи: «Закрытие хвостовая позиция доля»; его authoritative provenance — «approved profile or typed formula».
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: CloseFarShare
Размерность: `SHARE`
Unit: `1 (dimensionless)`
Знак: >= 0
Допустимый диапазон: соответствует типу `SHARE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для CloseFarShare.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: CloseFarShare загружается из выбранного документального/конфигурационного профиля. Внутри замороженного цикла CloseFarShare не изменяется; новая ревизия относится к новому plan. Изменение профиля или revision делает прежний CloseFarShare stale. новое approved значение CloseFarShare из явно выбранного профиля. Завершается вместе с конфигурационным scope цикла. Этот lifecycle относится именно к объекту «Закрытие хвостовая позиция доля» и его собственному type/source contract.
Условия stale: Изменение профиля или revision делает прежний CloseFarShare stale.
Authoritative replacement: новое approved значение CloseFarShare из явно выбранного профиля.
Допустимые операции: сравнение и преобразование только по `SHARE` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: CloseFarShare нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CloseFarShare, тип SHARE, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Config.mqh::CloseFarShare
Python mapping: Tools/optimize_big_scenario_min_levels.py::close_far_share
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `HSB-DOC-CONFLICT-005`
Resolution stage: `3.1.7`
Статус определения: `UNRESOLVED_PARAMETER_PROFILE`
Semantic category: POLICY
Lifecycle class: POLICY
Creation event: CloseFarShare загружается из выбранного документального/конфигурационного профиля.
Validation event: CloseFarShare проверяется как POLICY до фиксации цикла.
Freeze/confirmation event: CloseFarShare замораживается в конфигурации конкретного CycleID.
Mutation events: Внутри замороженного цикла CloseFarShare не изменяется; новая ревизия относится к новому plan.
Stale triggers: Изменение профиля или revision делает прежний CloseFarShare stale.
Replacement source: новое approved значение CloseFarShare из явно выбранного профиля.
Terminal condition: Завершается вместе с конфигурационным scope цикла.
Persistence behavior: Хранится с profile revision и CycleID.
Restart behavior: После restart перечитывается и сверяется с frozen cycle configuration.
Отличие от: CloseFarShare отличается от sibling-терминов источником `approved profile or typed formula`, классом `POLICY/PROJECTED` и стадией lifecycle `POLICY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `POLICY`; запись `CloseFarShare` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `CloseFarShare` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### ReserveShare
CanonicalName: `ReserveShare`
Русское название: Резерв доля
Краткое определение: ReserveShare — безразмерная величина типа `SHARE` для Reserve; она не интерпретируется как lot, money или percent без явной conversion. Отличительный объект записи: «Резерв доля»; его authoritative provenance — «approved profile or typed formula».
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: Reserve
Размерность: `SHARE`
Unit: `1 (dimensionless)`
Знак: >= 0
Допустимый диапазон: соответствует типу `SHARE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для ReserveShare.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: ReserveShare загружается из выбранного документального/конфигурационного профиля. Внутри замороженного цикла ReserveShare не изменяется; новая ревизия относится к новому plan. Изменение профиля или revision делает прежний ReserveShare stale. новое approved значение ReserveShare из явно выбранного профиля. Завершается вместе с конфигурационным scope цикла. Этот lifecycle относится именно к объекту «Резерв доля» и его собственному type/source contract.
Условия stale: Изменение профиля или revision делает прежний ReserveShare stale.
Authoritative replacement: новое approved значение ReserveShare из явно выбранного профиля.
Допустимые операции: сравнение и преобразование только по `SHARE` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: ReserveShare нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Reserve, тип SHARE, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Config.mqh::ReserveShare
Python mapping: Tests/test_reserve_growth_ratio.py::reserve_share
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `HSB-DOC-CONFLICT-006`
Resolution stage: `3.1.7`
Статус определения: `UNRESOLVED_PARAMETER_PROFILE`
Semantic category: POLICY
Lifecycle class: POLICY
Creation event: ReserveShare загружается из выбранного документального/конфигурационного профиля.
Validation event: ReserveShare проверяется как POLICY до фиксации цикла.
Freeze/confirmation event: ReserveShare замораживается в конфигурации конкретного CycleID.
Mutation events: Внутри замороженного цикла ReserveShare не изменяется; новая ревизия относится к новому plan.
Stale triggers: Изменение профиля или revision делает прежний ReserveShare stale.
Replacement source: новое approved значение ReserveShare из явно выбранного профиля.
Terminal condition: Завершается вместе с конфигурационным scope цикла.
Persistence behavior: Хранится с profile revision и CycleID.
Restart behavior: После restart перечитывается и сверяется с frozen cycle configuration.
Отличие от: ReserveShare отличается от sibling-терминов источником `approved profile or typed formula`, классом `POLICY/PROJECTED` и стадией lifecycle `POLICY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `POLICY`; запись `ReserveShare` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ReserveShare` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### SmallReserveShare
CanonicalName: `SmallReserveShare`
Русское название: Защитная позиция резерв доля
Краткое определение: SmallReserveShare — безразмерная величина типа `SHARE` для SmallReserveShare; она не интерпретируется как lot, money или percent без явной conversion. Отличительный объект записи: «Защитная позиция резерв доля»; его authoritative provenance — «approved profile or typed formula».
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: SmallReserveShare
Размерность: `SHARE`
Unit: `1 (dimensionless)`
Знак: >= 0
Допустимый диапазон: соответствует типу `SHARE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для SmallReserveShare.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: SmallReserveShare загружается из выбранного документального/конфигурационного профиля. Внутри замороженного цикла SmallReserveShare не изменяется; новая ревизия относится к новому plan. Изменение профиля или revision делает прежний SmallReserveShare stale. новое approved значение SmallReserveShare из явно выбранного профиля. Завершается вместе с конфигурационным scope цикла. Этот lifecycle относится именно к объекту «Защитная позиция резерв доля» и его собственному type/source contract.
Условия stale: Изменение профиля или revision делает прежний SmallReserveShare stale.
Authoritative replacement: новое approved значение SmallReserveShare из явно выбранного профиля.
Допустимые операции: сравнение и преобразование только по `SHARE` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: SmallReserveShare нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SmallReserveShare, тип SHARE, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Config.mqh::SmallReserveShare
Python mapping: Tools/mql5_like_big_scenario_parameter_search.py::small_reserve_share
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: POLICY
Lifecycle class: POLICY
Creation event: SmallReserveShare загружается из выбранного документального/конфигурационного профиля.
Validation event: SmallReserveShare проверяется как POLICY до фиксации цикла.
Freeze/confirmation event: SmallReserveShare замораживается в конфигурации конкретного CycleID.
Mutation events: Внутри замороженного цикла SmallReserveShare не изменяется; новая ревизия относится к новому plan.
Stale triggers: Изменение профиля или revision делает прежний SmallReserveShare stale.
Replacement source: новое approved значение SmallReserveShare из явно выбранного профиля.
Terminal condition: Завершается вместе с конфигурационным scope цикла.
Persistence behavior: Хранится с profile revision и CycleID.
Restart behavior: После restart перечитывается и сверяется с frozen cycle configuration.
Отличие от: SmallReserveShare отличается от sibling-терминов источником `approved profile or typed formula`, классом `POLICY/PROJECTED` и стадией lifecycle `POLICY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `POLICY`; запись `SmallReserveShare` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `SmallReserveShare` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### CompressionRatio
CanonicalName: `CompressionRatio`
Русское название: Сжатие отношение
Краткое определение: CompressionRatio — безразмерная величина типа `RATIO` для CompressionRatio; она не интерпретируется как lot, money или percent без явной conversion. Отличительный объект записи: «Сжатие отношение»; его authoritative provenance — «approved profile or typed formula».
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: CompressionRatio
Размерность: `RATIO`
Unit: `1 (dimensionless)`
Знак: >= 0
Допустимый диапазон: соответствует типу `RATIO`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для CompressionRatio.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: CompressionRatio загружается из выбранного документального/конфигурационного профиля. Внутри замороженного цикла CompressionRatio не изменяется; новая ревизия относится к новому plan. Изменение профиля или revision делает прежний CompressionRatio stale. новое approved значение CompressionRatio из явно выбранного профиля. Завершается вместе с конфигурационным scope цикла. Этот lifecycle относится именно к объекту «Сжатие отношение» и его собственному type/source contract.
Условия stale: Изменение профиля или revision делает прежний CompressionRatio stale.
Authoritative replacement: новое approved значение CompressionRatio из явно выбранного профиля.
Допустимые операции: сравнение и преобразование только по `RATIO` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: CompressionRatio нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CompressionRatio, тип RATIO, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::compressionRatio
Python mapping: Tools/offline_optimizer.py::compression_ratio
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: POLICY
Lifecycle class: POLICY
Creation event: CompressionRatio загружается из выбранного документального/конфигурационного профиля.
Validation event: CompressionRatio проверяется как POLICY до фиксации цикла.
Freeze/confirmation event: CompressionRatio замораживается в конфигурации конкретного CycleID.
Mutation events: Внутри замороженного цикла CompressionRatio не изменяется; новая ревизия относится к новому plan.
Stale triggers: Изменение профиля или revision делает прежний CompressionRatio stale.
Replacement source: новое approved значение CompressionRatio из явно выбранного профиля.
Terminal condition: Завершается вместе с конфигурационным scope цикла.
Persistence behavior: Хранится с profile revision и CycleID.
Restart behavior: После restart перечитывается и сверяется с frozen cycle configuration.
Отличие от: CompressionRatio отличается от sibling-терминов источником `approved profile or typed formula`, классом `POLICY/PROJECTED` и стадией lifecycle `POLICY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `POLICY`; запись `CompressionRatio` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `CompressionRatio` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### ReserveCoverageRatio
CanonicalName: `ReserveCoverageRatio`
Русское название: Резерв покрытие отношение
Краткое определение: ReserveCoverageRatio — безразмерная величина типа `RATIO` для Reserve; она не интерпретируется как lot, money или percent без явной conversion. Отличительный объект записи: «Резерв покрытие отношение»; его authoritative provenance — «approved profile or typed formula».
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: Reserve
Размерность: `RATIO`
Unit: `1 (dimensionless)`
Знак: >= 0
Допустимый диапазон: соответствует типу `RATIO`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для ReserveCoverageRatio.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: ReserveCoverageRatio загружается из выбранного документального/конфигурационного профиля. Внутри замороженного цикла ReserveCoverageRatio не изменяется; новая ревизия относится к новому plan. Изменение профиля или revision делает прежний ReserveCoverageRatio stale. новое approved значение ReserveCoverageRatio из явно выбранного профиля. Завершается вместе с конфигурационным scope цикла. Этот lifecycle относится именно к объекту «Резерв покрытие отношение» и его собственному type/source contract.
Условия stale: Изменение профиля или revision делает прежний ReserveCoverageRatio stale.
Authoritative replacement: новое approved значение ReserveCoverageRatio из явно выбранного профиля.
Допустимые операции: сравнение и преобразование только по `RATIO` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: ReserveCoverageRatio нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Reserve, тип RATIO, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/StateMachine.mqh::reserveCoverage
Python mapping: Tools/run_full_parameter_optimization_study.py::reserve_coverage
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: POLICY
Lifecycle class: POLICY
Creation event: ReserveCoverageRatio загружается из выбранного документального/конфигурационного профиля.
Validation event: ReserveCoverageRatio проверяется как POLICY до фиксации цикла.
Freeze/confirmation event: ReserveCoverageRatio замораживается в конфигурации конкретного CycleID.
Mutation events: Внутри замороженного цикла ReserveCoverageRatio не изменяется; новая ревизия относится к новому plan.
Stale triggers: Изменение профиля или revision делает прежний ReserveCoverageRatio stale.
Replacement source: новое approved значение ReserveCoverageRatio из явно выбранного профиля.
Terminal condition: Завершается вместе с конфигурационным scope цикла.
Persistence behavior: Хранится с profile revision и CycleID.
Restart behavior: После restart перечитывается и сверяется с frozen cycle configuration.
Отличие от: ReserveCoverageRatio отличается от sibling-терминов источником `approved profile or typed formula`, классом `POLICY/PROJECTED` и стадией lifecycle `POLICY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `POLICY`; запись `ReserveCoverageRatio` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ReserveCoverageRatio` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### RecoveryCoverageRatio
CanonicalName: `RecoveryCoverageRatio`
Русское название: Восстановление покрытие отношение
Краткое определение: RecoveryCoverageRatio — безразмерная величина типа `RATIO` для RecoveryCoverageRatio; она не интерпретируется как lot, money или percent без явной conversion. Отличительный объект записи: «Восстановление покрытие отношение»; его authoritative provenance — «approved profile or typed formula».
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: RecoveryCoverageRatio
Размерность: `RATIO`
Unit: `1 (dimensionless)`
Знак: >= 0
Допустимый диапазон: соответствует типу `RATIO`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для RecoveryCoverageRatio.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: RecoveryCoverageRatio загружается из выбранного документального/конфигурационного профиля. Внутри замороженного цикла RecoveryCoverageRatio не изменяется; новая ревизия относится к новому plan. Изменение профиля или revision делает прежний RecoveryCoverageRatio stale. новое approved значение RecoveryCoverageRatio из явно выбранного профиля. Завершается вместе с конфигурационным scope цикла. Этот lifecycle относится именно к объекту «Восстановление покрытие отношение» и его собственному type/source contract.
Условия stale: Изменение профиля или revision делает прежний RecoveryCoverageRatio stale.
Authoritative replacement: новое approved значение RecoveryCoverageRatio из явно выбранного профиля.
Допустимые операции: сравнение и преобразование только по `RATIO` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: RecoveryCoverageRatio нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RecoveryCoverageRatio, тип RATIO, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: Tools/offline_optimizer.py::coverage_ratio
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: POLICY
Lifecycle class: POLICY
Creation event: RecoveryCoverageRatio загружается из выбранного документального/конфигурационного профиля.
Validation event: RecoveryCoverageRatio проверяется как POLICY до фиксации цикла.
Freeze/confirmation event: RecoveryCoverageRatio замораживается в конфигурации конкретного CycleID.
Mutation events: Внутри замороженного цикла RecoveryCoverageRatio не изменяется; новая ревизия относится к новому plan.
Stale triggers: Изменение профиля или revision делает прежний RecoveryCoverageRatio stale.
Replacement source: новое approved значение RecoveryCoverageRatio из явно выбранного профиля.
Terminal condition: Завершается вместе с конфигурационным scope цикла.
Persistence behavior: Хранится с profile revision и CycleID.
Restart behavior: После restart перечитывается и сверяется с frozen cycle configuration.
Отличие от: RecoveryCoverageRatio отличается от sibling-терминов источником `approved profile or typed formula`, классом `POLICY/PROJECTED` и стадией lifecycle `POLICY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `POLICY`; запись `RecoveryCoverageRatio` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `RecoveryCoverageRatio` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=PARTIAL_MATCH.

### MaximumNewBigToOldFarRatio
CanonicalName: `MaximumNewBigToOldFarRatio`
Русское название: Максимальное новая компенсирующая позиция to предыдущая хвостовая позиция отношение
Краткое определение: MaximumNewBigToOldFarRatio — безразмерная величина типа `RATIO` для MaximumNewBigToOldFarRatio; она не интерпретируется как lot, money или percent без явной conversion. Отличительный объект записи: «Максимальное новая компенсирующая позиция to предыдущая хвостовая позиция отношение»; его authoritative provenance — «approved profile or typed formula».
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: MaximumNewBigToOldFarRatio
Размерность: `RATIO`
Unit: `1 (dimensionless)`
Знак: >= 0
Допустимый диапазон: соответствует типу `RATIO`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для MaximumNewBigToOldFarRatio.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: MaximumNewBigToOldFarRatio загружается из выбранного документального/конфигурационного профиля. Внутри замороженного цикла MaximumNewBigToOldFarRatio не изменяется; новая ревизия относится к новому plan. Изменение профиля или revision делает прежний MaximumNewBigToOldFarRatio stale. новое approved значение MaximumNewBigToOldFarRatio из явно выбранного профиля. Завершается вместе с конфигурационным scope цикла. Этот lifecycle относится именно к объекту «Максимальное новая компенсирующая позиция to предыдущая хвостовая позиция отношение» и его собственному type/source contract.
Условия stale: Изменение профиля или revision делает прежний MaximumNewBigToOldFarRatio stale.
Authoritative replacement: новое approved значение MaximumNewBigToOldFarRatio из явно выбранного профиля.
Допустимые операции: сравнение и преобразование только по `RATIO` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: MaximumNewBigToOldFarRatio нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: MaximumNewBigToOldFarRatio, тип RATIO, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: Tools/offline_optimizer.py::new_big_to_old_far_ratio
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `HSB-DOC-CONFLICT-022`
Resolution stage: `3.1.4 / 3.1.8`
Статус определения: `UNRESOLVED_BUSINESS_POLICY`
Semantic category: POLICY
Lifecycle class: POLICY
Creation event: MaximumNewBigToOldFarRatio загружается из выбранного документального/конфигурационного профиля.
Validation event: MaximumNewBigToOldFarRatio проверяется как POLICY до фиксации цикла.
Freeze/confirmation event: MaximumNewBigToOldFarRatio замораживается в конфигурации конкретного CycleID.
Mutation events: Внутри замороженного цикла MaximumNewBigToOldFarRatio не изменяется; новая ревизия относится к новому plan.
Stale triggers: Изменение профиля или revision делает прежний MaximumNewBigToOldFarRatio stale.
Replacement source: новое approved значение MaximumNewBigToOldFarRatio из явно выбранного профиля.
Terminal condition: Завершается вместе с конфигурационным scope цикла.
Persistence behavior: Хранится с profile revision и CycleID.
Restart behavior: После restart перечитывается и сверяется с frozen cycle configuration.
Отличие от: MaximumNewBigToOldFarRatio отличается от sibling-терминов источником `approved profile or typed formula`, классом `POLICY/PROJECTED` и стадией lifecycle `POLICY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `POLICY`; запись `MaximumNewBigToOldFarRatio` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `MaximumNewBigToOldFarRatio` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=PARTIAL_MATCH.

### MinimumReserveCatchUpRatio
CanonicalName: `MinimumReserveCatchUpRatio`
Русское название: Минимальное резерв catch up отношение
Краткое определение: MinimumReserveCatchUpRatio — безразмерная величина типа `RATIO` для MinimumReserveCatchUpRatio; она не интерпретируется как lot, money или percent без явной conversion. Отличительный объект записи: «Минимальное резерв catch up отношение»; его authoritative provenance — «approved profile or typed formula».
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: MinimumReserveCatchUpRatio
Размерность: `RATIO`
Unit: `1 (dimensionless)`
Знак: >= 0
Допустимый диапазон: соответствует типу `RATIO`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для MinimumReserveCatchUpRatio.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: MinimumReserveCatchUpRatio загружается из выбранного документального/конфигурационного профиля. Внутри замороженного цикла MinimumReserveCatchUpRatio не изменяется; новая ревизия относится к новому plan. Изменение профиля или revision делает прежний MinimumReserveCatchUpRatio stale. новое approved значение MinimumReserveCatchUpRatio из явно выбранного профиля. Завершается вместе с конфигурационным scope цикла. Этот lifecycle относится именно к объекту «Минимальное резерв catch up отношение» и его собственному type/source contract.
Условия stale: Изменение профиля или revision делает прежний MinimumReserveCatchUpRatio stale.
Authoritative replacement: новое approved значение MinimumReserveCatchUpRatio из явно выбранного профиля.
Допустимые операции: сравнение и преобразование только по `RATIO` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: MinimumReserveCatchUpRatio нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: MinimumReserveCatchUpRatio, тип RATIO, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: POLICY
Lifecycle class: POLICY
Creation event: MinimumReserveCatchUpRatio загружается из выбранного документального/конфигурационного профиля.
Validation event: MinimumReserveCatchUpRatio проверяется как POLICY до фиксации цикла.
Freeze/confirmation event: MinimumReserveCatchUpRatio замораживается в конфигурации конкретного CycleID.
Mutation events: Внутри замороженного цикла MinimumReserveCatchUpRatio не изменяется; новая ревизия относится к новому plan.
Stale triggers: Изменение профиля или revision делает прежний MinimumReserveCatchUpRatio stale.
Replacement source: новое approved значение MinimumReserveCatchUpRatio из явно выбранного профиля.
Terminal condition: Завершается вместе с конфигурационным scope цикла.
Persistence behavior: Хранится с profile revision и CycleID.
Restart behavior: После restart перечитывается и сверяется с frozen cycle configuration.
Отличие от: MinimumReserveCatchUpRatio отличается от sibling-терминов источником `approved profile or typed formula`, классом `POLICY/PROJECTED` и стадией lifecycle `POLICY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `POLICY`; запись `MinimumReserveCatchUpRatio` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `MinimumReserveCatchUpRatio` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### PercentValue
CanonicalName: `PercentValue`
Русское название: Процент стоимость
Краткое определение: PercentValue — безразмерная величина типа `PERCENT` для PercentValue; она не интерпретируется как lot, money или percent без явной conversion. Отличительный объект записи: «Процент стоимость»; его authoritative provenance — «approved profile or typed formula».
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: PercentValue
Размерность: `PERCENT`
Unit: `1 (dimensionless)`
Знак: >= 0
Допустимый диапазон: соответствует типу `PERCENT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для PercentValue.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: PercentValue загружается из выбранного документального/конфигурационного профиля. Внутри замороженного цикла PercentValue не изменяется; новая ревизия относится к новому plan. Изменение профиля или revision делает прежний PercentValue stale. новое approved значение PercentValue из явно выбранного профиля. Завершается вместе с конфигурационным scope цикла. Этот lifecycle относится именно к объекту «Процент стоимость» и его собственному type/source contract.
Условия stale: Изменение профиля или revision делает прежний PercentValue stale.
Authoritative replacement: новое approved значение PercentValue из явно выбранного профиля.
Допустимые операции: сравнение и преобразование только по `PERCENT` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: PercentValue нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PercentValue, тип PERCENT, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: POLICY
Lifecycle class: POLICY
Creation event: PercentValue загружается из выбранного документального/конфигурационного профиля.
Validation event: PercentValue проверяется как POLICY до фиксации цикла.
Freeze/confirmation event: PercentValue замораживается в конфигурации конкретного CycleID.
Mutation events: Внутри замороженного цикла PercentValue не изменяется; новая ревизия относится к новому plan.
Stale triggers: Изменение профиля или revision делает прежний PercentValue stale.
Replacement source: новое approved значение PercentValue из явно выбранного профиля.
Terminal condition: Завершается вместе с конфигурационным scope цикла.
Persistence behavior: Хранится с profile revision и CycleID.
Restart behavior: После restart перечитывается и сверяется с frozen cycle configuration.
Отличие от: PercentValue отличается от sibling-терминов источником `approved profile or typed formula`, классом `POLICY/PROJECTED` и стадией lifecycle `POLICY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `POLICY`; запись `PercentValue` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `PercentValue` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### ScaleMultiplier
CanonicalName: `ScaleMultiplier`
Русское название: Масштаб множитель
Краткое определение: ScaleMultiplier — безразмерная величина типа `MULTIPLIER` для ScaleMultiplier; она не интерпретируется как lot, money или percent без явной conversion. Отличительный объект записи: «Масштаб множитель»; его authoritative provenance — «approved profile or typed formula».
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: ScaleMultiplier
Размерность: `MULTIPLIER`
Unit: `1 (dimensionless)`
Знак: >= 0
Допустимый диапазон: соответствует типу `MULTIPLIER`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для ScaleMultiplier.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: ScaleMultiplier загружается из выбранного документального/конфигурационного профиля. Внутри замороженного цикла ScaleMultiplier не изменяется; новая ревизия относится к новому plan. Изменение профиля или revision делает прежний ScaleMultiplier stale. новое approved значение ScaleMultiplier из явно выбранного профиля. Завершается вместе с конфигурационным scope цикла. Этот lifecycle относится именно к объекту «Масштаб множитель» и его собственному type/source contract.
Условия stale: Изменение профиля или revision делает прежний ScaleMultiplier stale.
Authoritative replacement: новое approved значение ScaleMultiplier из явно выбранного профиля.
Допустимые операции: сравнение и преобразование только по `MULTIPLIER` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: ScaleMultiplier нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ScaleMultiplier, тип MULTIPLIER, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::multiplier
Python mapping: Tools/offline_optimizer.py::multiplier
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: POLICY
Lifecycle class: POLICY
Creation event: ScaleMultiplier загружается из выбранного документального/конфигурационного профиля.
Validation event: ScaleMultiplier проверяется как POLICY до фиксации цикла.
Freeze/confirmation event: ScaleMultiplier замораживается в конфигурации конкретного CycleID.
Mutation events: Внутри замороженного цикла ScaleMultiplier не изменяется; новая ревизия относится к новому plan.
Stale triggers: Изменение профиля или revision делает прежний ScaleMultiplier stale.
Replacement source: новое approved значение ScaleMultiplier из явно выбранного профиля.
Terminal condition: Завершается вместе с конфигурационным scope цикла.
Persistence behavior: Хранится с profile revision и CycleID.
Restart behavior: После restart перечитывается и сверяется с frozen cycle configuration.
Отличие от: ScaleMultiplier отличается от sibling-терминов источником `approved profile or typed formula`, классом `POLICY/PROJECTED` и стадией lifecycle `POLICY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `POLICY`; запись `ScaleMultiplier` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ScaleMultiplier` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### RiskThresholdRatio
CanonicalName: `RiskThresholdRatio`
Русское название: Риск порог отношение
Краткое определение: RiskThresholdRatio — безразмерная величина типа `RATIO` для RiskThresholdRatio; она не интерпретируется как lot, money или percent без явной conversion. Отличительный объект записи: «Риск порог отношение»; его authoritative provenance — «approved profile or typed formula».
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: RiskThresholdRatio
Размерность: `RATIO`
Unit: `1 (dimensionless)`
Знак: >= 0
Допустимый диапазон: соответствует типу `RATIO`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для RiskThresholdRatio.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: RiskThresholdRatio загружается из выбранного документального/конфигурационного профиля. Внутри замороженного цикла RiskThresholdRatio не изменяется; новая ревизия относится к новому plan. Изменение профиля или revision делает прежний RiskThresholdRatio stale. новое approved значение RiskThresholdRatio из явно выбранного профиля. Завершается вместе с конфигурационным scope цикла. Этот lifecycle относится именно к объекту «Риск порог отношение» и его собственному type/source contract.
Условия stale: Изменение профиля или revision делает прежний RiskThresholdRatio stale.
Authoritative replacement: новое approved значение RiskThresholdRatio из явно выбранного профиля.
Допустимые операции: сравнение и преобразование только по `RATIO` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: RiskThresholdRatio нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RiskThresholdRatio, тип RATIO, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: POLICY
Lifecycle class: POLICY
Creation event: RiskThresholdRatio загружается из выбранного документального/конфигурационного профиля.
Validation event: RiskThresholdRatio проверяется как POLICY до фиксации цикла.
Freeze/confirmation event: RiskThresholdRatio замораживается в конфигурации конкретного CycleID.
Mutation events: Внутри замороженного цикла RiskThresholdRatio не изменяется; новая ревизия относится к новому plan.
Stale triggers: Изменение профиля или revision делает прежний RiskThresholdRatio stale.
Replacement source: новое approved значение RiskThresholdRatio из явно выбранного профиля.
Terminal condition: Завершается вместе с конфигурационным scope цикла.
Persistence behavior: Хранится с profile revision и CycleID.
Restart behavior: После restart перечитывается и сверяется с frozen cycle configuration.
Отличие от: RiskThresholdRatio отличается от sibling-терминов источником `approved profile or typed formula`, классом `POLICY/PROJECTED` и стадией lifecycle `POLICY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `POLICY`; запись `RiskThresholdRatio` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `RiskThresholdRatio` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### SymbolId
CanonicalName: `SymbolId`
Русское название: Символ идентификатор
Краткое определение: SymbolId — identity-сущность типа `SYMBOL_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Символ идентификатор»; его authoritative provenance — «MT5 properties / persisted reconciled namespace».
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: SymbolId
Размерность: `SYMBOL_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `SYMBOL_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для SymbolId.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: SymbolId создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object. Не мутирует; новый объект получает новое identity. Несовпадение scope либо закрытие объекта делает использование SymbolId stale. authoritative identity текущего terminal/deal/event object. После завершения объекта остаётся историческим ключом и не переиспользуется. Этот lifecycle относится именно к объекту «Символ идентификатор» и его собственному type/source contract.
Условия stale: Несовпадение scope либо закрытие объекта делает использование SymbolId stale.
Authoritative replacement: authoritative identity текущего terminal/deal/event object.
Допустимые операции: сравнение и преобразование только по `SYMBOL_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: SymbolId нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SymbolId, тип SYMBOL_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::symbol
Python mapping: Tests/HybridSplitBig/test_catchup_route_hardening.py::symbol
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: SymbolId создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object.
Validation event: SymbolId проверяется точным сравнением и scope filters.
Freeze/confirmation event: После выдачи SymbolId неизменяем в пределах своего объекта.
Mutation events: Не мутирует; новый объект получает новое identity.
Stale triggers: Несовпадение scope либо закрытие объекта делает использование SymbolId stale.
Replacement source: authoritative identity текущего terminal/deal/event object.
Terminal condition: После завершения объекта остаётся историческим ключом и не переиспользуется.
Persistence behavior: Persisted только вместе с type и cycle scope.
Restart behavior: После restart сверяется с terminal/deal history.
Отличие от: SymbolId отличается от sibling-терминов источником `MT5 properties / persisted reconciled namespace`, классом `ACTUAL CONFIRMED` и стадией lifecycle `IDENTITY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `SymbolId` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `SymbolId` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### MagicId
CanonicalName: `MagicId`
Русское название: Магический номер идентификатор
Краткое определение: MagicId — identity-сущность типа `MAGIC_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Магический номер идентификатор»; его authoritative provenance — «MT5 properties / persisted reconciled namespace».
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: MagicId
Размерность: `MAGIC_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `MAGIC_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для MagicId.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: MagicId создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object. Не мутирует; новый объект получает новое identity. Несовпадение scope либо закрытие объекта делает использование MagicId stale. authoritative identity текущего terminal/deal/event object. После завершения объекта остаётся историческим ключом и не переиспользуется. Этот lifecycle относится именно к объекту «Магический номер идентификатор» и его собственному type/source contract.
Условия stale: Несовпадение scope либо закрытие объекта делает использование MagicId stale.
Authoritative replacement: authoritative identity текущего terminal/deal/event object.
Допустимые операции: сравнение и преобразование только по `MAGIC_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: MagicId нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: MagicId, тип MAGIC_ID, class ACTUAL CONFIRMED.
Legacy aliases: MagicNumber
MQL5 mapping: Include/Types.mqh::magic
Python mapping: NONE_FOUND
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: MagicId создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object.
Validation event: MagicId проверяется точным сравнением и scope filters.
Freeze/confirmation event: После выдачи MagicId неизменяем в пределах своего объекта.
Mutation events: Не мутирует; новый объект получает новое identity.
Stale triggers: Несовпадение scope либо закрытие объекта делает использование MagicId stale.
Replacement source: authoritative identity текущего terminal/deal/event object.
Terminal condition: После завершения объекта остаётся историческим ключом и не переиспользуется.
Persistence behavior: Persisted только вместе с type и cycle scope.
Restart behavior: После restart сверяется с terminal/deal history.
Отличие от: MagicId отличается от sibling-терминов источником `MT5 properties / persisted reconciled namespace`, классом `ACTUAL CONFIRMED` и стадией lifecycle `IDENTITY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `MagicId` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `MagicId` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### CycleId
CanonicalName: `CycleId`
Русское название: Цикл идентификатор
Краткое определение: CycleId — Уникальный persisted identifier одного recovery cycle, неизменный до terminal completion и не переиспользуемый другим cycle. Отличительный объект записи: «Цикл идентификатор»; его authoritative provenance — «MT5 properties / persisted reconciled namespace».
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: CycleId
Размерность: `CYCLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `CYCLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для CycleId.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: CycleId создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object. Не мутирует; новый объект получает новое identity. Несовпадение scope либо закрытие объекта делает использование CycleId stale. authoritative identity текущего terminal/deal/event object. После завершения объекта остаётся историческим ключом и не переиспользуется. Этот lifecycle относится именно к объекту «Цикл идентификатор» и его собственному type/source contract.
Условия stale: Несовпадение scope либо закрытие объекта делает использование CycleId stale.
Authoritative replacement: authoritative identity текущего terminal/deal/event object.
Допустимые операции: сравнение и преобразование только по `CYCLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: CycleId нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CycleId, тип CYCLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: CycleID, cycleId
MQL5 mapping: Include/Types.mqh::cycleId
Python mapping: Tests/HybridSplitBig/test_catchup_route_hardening.py::cycle
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: CycleId создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object.
Validation event: CycleId проверяется точным сравнением и scope filters.
Freeze/confirmation event: После выдачи CycleId неизменяем в пределах своего объекта.
Mutation events: Не мутирует; новый объект получает новое identity.
Stale triggers: Несовпадение scope либо закрытие объекта делает использование CycleId stale.
Replacement source: authoritative identity текущего terminal/deal/event object.
Terminal condition: После завершения объекта остаётся историческим ключом и не переиспользуется.
Persistence behavior: Persisted только вместе с type и cycle scope.
Restart behavior: После restart сверяется с terminal/deal history.
Отличие от: CycleId отличается от sibling-терминов источником `MT5 properties / persisted reconciled namespace`, классом `ACTUAL CONFIRMED` и стадией lifecycle `IDENTITY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `CycleId` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `CycleId` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### RoleId
CanonicalName: `RoleId`
Русское название: Роль идентификатор
Краткое определение: RoleId — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Роль идентификатор»; его authoritative provenance — «MT5 properties / persisted reconciled namespace».
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: RoleId
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для RoleId.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: RoleId назначается approved role rule и связывается с position identity. RoleId меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку RoleId stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Роль идентификатор» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку RoleId stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: RoleId нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RoleId, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: ROLE
Lifecycle class: ROLE
Creation event: RoleId назначается approved role rule и связывается с position identity.
Validation event: Связка RoleId проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: RoleId меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку RoleId stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: RoleId отличается от sibling-терминов источником `MT5 properties / persisted reconciled namespace`, классом `ACTUAL CONFIRMED` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ROLE`; запись `RoleId` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `RoleId` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### PositionIdentifier
CanonicalName: `PositionIdentifier`
Русское название: Позиция идентификатор
Краткое определение: PositionIdentifier — identity-сущность типа `POSITION_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Позиция идентификатор»; его authoritative provenance — «MT5 properties / persisted reconciled namespace».
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: Position
Размерность: `POSITION_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `POSITION_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для PositionIdentifier.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: PositionIdentifier создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object. Не мутирует; новый объект получает новое identity. Несовпадение scope либо закрытие объекта делает использование PositionIdentifier stale. authoritative identity текущего terminal/deal/event object. После завершения объекта остаётся историческим ключом и не переиспользуется. Этот lifecycle относится именно к объекту «Позиция идентификатор» и его собственному type/source contract.
Условия stale: Несовпадение scope либо закрытие объекта делает использование PositionIdentifier stale.
Authoritative replacement: authoritative identity текущего terminal/deal/event object.
Допустимые операции: сравнение и преобразование только по `POSITION_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: PositionIdentifier нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Position, тип POSITION_ID, class ACTUAL CONFIRMED.
Legacy aliases: POSITION_IDENTIFIER
MQL5 mapping: Include/SimulationEngine.mqh::positionIdentifier
Python mapping: Tests/unit/test_split_final_safety_model.py::identifier
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: PositionIdentifier создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object.
Validation event: PositionIdentifier проверяется точным сравнением и scope filters.
Freeze/confirmation event: После выдачи PositionIdentifier неизменяем в пределах своего объекта.
Mutation events: Не мутирует; новый объект получает новое identity.
Stale triggers: Несовпадение scope либо закрытие объекта делает использование PositionIdentifier stale.
Replacement source: authoritative identity текущего terminal/deal/event object.
Terminal condition: После завершения объекта остаётся историческим ключом и не переиспользуется.
Persistence behavior: Persisted только вместе с type и cycle scope.
Restart behavior: После restart сверяется с terminal/deal history.
Отличие от: PositionIdentifier отличается от sibling-терминов источником `MT5 properties / persisted reconciled namespace`, классом `ACTUAL CONFIRMED` и стадией lifecycle `IDENTITY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `PositionIdentifier` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `PositionIdentifier` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### PositionTicket
CanonicalName: `PositionTicket`
Русское название: Позиция тикет
Краткое определение: PositionTicket — identity-сущность типа `POSITION_TICKET` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Позиция тикет»; его authoritative provenance — «MT5 properties / persisted reconciled namespace».
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: Position
Размерность: `POSITION_TICKET`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `POSITION_TICKET`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для PositionTicket.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: PositionTicket создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object. Не мутирует; новый объект получает новое identity. Несовпадение scope либо закрытие объекта делает использование PositionTicket stale. authoritative identity текущего terminal/deal/event object. После завершения объекта остаётся историческим ключом и не переиспользуется. Этот lifecycle относится именно к объекту «Позиция тикет» и его собственному type/source contract.
Условия stale: Несовпадение scope либо закрытие объекта делает использование PositionTicket stale.
Authoritative replacement: authoritative identity текущего terminal/deal/event object.
Допустимые операции: сравнение и преобразование только по `POSITION_TICKET` с `EXACT` и explicit provenance.
Запрещённые подмены: PositionTicket нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Position, тип POSITION_TICKET, class ACTUAL CONFIRMED.
Legacy aliases: ticket
MQL5 mapping: Include/SimulationEngine.mqh::positionTicket
Python mapping: NONE_FOUND
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: PositionTicket создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object.
Validation event: PositionTicket проверяется точным сравнением и scope filters.
Freeze/confirmation event: После выдачи PositionTicket неизменяем в пределах своего объекта.
Mutation events: Не мутирует; новый объект получает новое identity.
Stale triggers: Несовпадение scope либо закрытие объекта делает использование PositionTicket stale.
Replacement source: authoritative identity текущего terminal/deal/event object.
Terminal condition: После завершения объекта остаётся историческим ключом и не переиспользуется.
Persistence behavior: Persisted только вместе с type и cycle scope.
Restart behavior: После restart сверяется с terminal/deal history.
Отличие от: PositionTicket отличается от sibling-терминов источником `MT5 properties / persisted reconciled namespace`, классом `ACTUAL CONFIRMED` и стадией lifecycle `IDENTITY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `PositionTicket` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `PositionTicket` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### OrderTicket
CanonicalName: `OrderTicket`
Русское название: Ордер тикет
Краткое определение: OrderTicket — identity-сущность типа `ORDER_TICKET` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Ордер тикет»; его authoritative provenance — «MT5 properties / persisted reconciled namespace».
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: OrderTicket
Размерность: `ORDER_TICKET`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ORDER_TICKET`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для OrderTicket.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: OrderTicket создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object. Не мутирует; новый объект получает новое identity. Несовпадение scope либо закрытие объекта делает использование OrderTicket stale. authoritative identity текущего terminal/deal/event object. После завершения объекта остаётся историческим ключом и не переиспользуется. Этот lifecycle относится именно к объекту «Ордер тикет» и его собственному type/source contract.
Условия stale: Несовпадение scope либо закрытие объекта делает использование OrderTicket stale.
Authoritative replacement: authoritative identity текущего terminal/deal/event object.
Допустимые операции: сравнение и преобразование только по `ORDER_TICKET` с `EXACT` и explicit provenance.
Запрещённые подмены: OrderTicket нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: OrderTicket, тип ORDER_TICKET, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/SimulationEngine.mqh::ticket
Python mapping: Tests/unit/test_split_final_safety_model.py::ticket
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: OrderTicket создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object.
Validation event: OrderTicket проверяется точным сравнением и scope filters.
Freeze/confirmation event: После выдачи OrderTicket неизменяем в пределах своего объекта.
Mutation events: Не мутирует; новый объект получает новое identity.
Stale triggers: Несовпадение scope либо закрытие объекта делает использование OrderTicket stale.
Replacement source: authoritative identity текущего terminal/deal/event object.
Terminal condition: После завершения объекта остаётся историческим ключом и не переиспользуется.
Persistence behavior: Persisted только вместе с type и cycle scope.
Restart behavior: После restart сверяется с terminal/deal history.
Отличие от: OrderTicket отличается от sibling-терминов источником `MT5 properties / persisted reconciled namespace`, классом `ACTUAL CONFIRMED` и стадией lifecycle `IDENTITY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `OrderTicket` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `OrderTicket` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### DealTicket
CanonicalName: `DealTicket`
Русское название: Сделка тикет
Краткое определение: DealTicket — identity-сущность типа `DEAL_TICKET` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Сделка тикет»; его authoritative provenance — «MT5 properties / persisted reconciled namespace».
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: DealTicket
Размерность: `DEAL_TICKET`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `DEAL_TICKET`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для DealTicket.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: DealTicket создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object. Не мутирует; новый объект получает новое identity. Несовпадение scope либо закрытие объекта делает использование DealTicket stale. authoritative identity текущего terminal/deal/event object. После завершения объекта остаётся историческим ключом и не переиспользуется. Этот lifecycle относится именно к объекту «Сделка тикет» и его собственному type/source contract.
Условия stale: Несовпадение scope либо закрытие объекта делает использование DealTicket stale.
Authoritative replacement: authoritative identity текущего terminal/deal/event object.
Допустимые операции: сравнение и преобразование только по `DEAL_TICKET` с `EXACT` и explicit provenance.
Запрещённые подмены: DealTicket нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: DealTicket, тип DEAL_TICKET, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/SimulationEngine.mqh::entryDealTicket
Python mapping: Tests/unit/test_split_final_safety_model.py::ticket
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: DealTicket создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object.
Validation event: DealTicket проверяется точным сравнением и scope filters.
Freeze/confirmation event: После выдачи DealTicket неизменяем в пределах своего объекта.
Mutation events: Не мутирует; новый объект получает новое identity.
Stale triggers: Несовпадение scope либо закрытие объекта делает использование DealTicket stale.
Replacement source: authoritative identity текущего terminal/deal/event object.
Terminal condition: После завершения объекта остаётся историческим ключом и не переиспользуется.
Persistence behavior: Persisted только вместе с type и cycle scope.
Restart behavior: После restart сверяется с terminal/deal history.
Отличие от: DealTicket отличается от sibling-терминов источником `MT5 properties / persisted reconciled namespace`, классом `ACTUAL CONFIRMED` и стадией lifecycle `IDENTITY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `DealTicket` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `DealTicket` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### EventId
CanonicalName: `EventId`
Русское название: Событие идентификатор
Краткое определение: EventId — identity-сущность типа `EVENT_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Событие идентификатор»; его authoritative provenance — «MT5 properties / persisted reconciled namespace».
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: EventId
Размерность: `EVENT_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `EVENT_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для EventId.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: EventId создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object. Не мутирует; новый объект получает новое identity. Несовпадение scope либо закрытие объекта делает использование EventId stale. authoritative identity текущего terminal/deal/event object. После завершения объекта остаётся историческим ключом и не переиспользуется. Этот lifecycle относится именно к объекту «Событие идентификатор» и его собственному type/source contract.
Условия stale: Несовпадение scope либо закрытие объекта делает использование EventId stale.
Authoritative replacement: authoritative identity текущего terminal/deal/event object.
Допустимые операции: сравнение и преобразование только по `EVENT_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: EventId нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: EventId, тип EVENT_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/StateMachine.mqh::lastEventId
Python mapping: Tests/unit/test_split_final_safety_model.py::event_id
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: EventId создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object.
Validation event: EventId проверяется точным сравнением и scope filters.
Freeze/confirmation event: После выдачи EventId неизменяем в пределах своего объекта.
Mutation events: Не мутирует; новый объект получает новое identity.
Stale triggers: Несовпадение scope либо закрытие объекта делает использование EventId stale.
Replacement source: authoritative identity текущего terminal/deal/event object.
Terminal condition: После завершения объекта остаётся историческим ключом и не переиспользуется.
Persistence behavior: Persisted только вместе с type и cycle scope.
Restart behavior: После restart сверяется с terminal/deal history.
Отличие от: EventId отличается от sibling-терминов источником `MT5 properties / persisted reconciled namespace`, классом `ACTUAL CONFIRMED` и стадией lifecycle `IDENTITY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `EventId` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `EventId` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### EventKey
CanonicalName: `EventKey`
Русское название: Событие ключ
Краткое определение: EventKey — identity-сущность типа `EVENT_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Событие ключ»; его authoritative provenance — «MT5 properties / persisted reconciled namespace».
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: EventKey
Размерность: `EVENT_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `EVENT_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для EventKey.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: EventKey создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object. Не мутирует; новый объект получает новое identity. Несовпадение scope либо закрытие объекта делает использование EventKey stale. authoritative identity текущего terminal/deal/event object. После завершения объекта остаётся историческим ключом и не переиспользуется. Этот lifecycle относится именно к объекту «Событие ключ» и его собственному type/source contract.
Условия stale: Несовпадение scope либо закрытие объекта делает использование EventKey stale.
Authoritative replacement: authoritative identity текущего terminal/deal/event object.
Допустимые операции: сравнение и преобразование только по `EVENT_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: EventKey нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: EventKey, тип EVENT_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::eventKeyHash
Python mapping: Tests/unit/test_split_final_safety_model.py::event_key
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: EventKey создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object.
Validation event: EventKey проверяется точным сравнением и scope filters.
Freeze/confirmation event: После выдачи EventKey неизменяем в пределах своего объекта.
Mutation events: Не мутирует; новый объект получает новое identity.
Stale triggers: Несовпадение scope либо закрытие объекта делает использование EventKey stale.
Replacement source: authoritative identity текущего terminal/deal/event object.
Terminal condition: После завершения объекта остаётся историческим ключом и не переиспользуется.
Persistence behavior: Persisted только вместе с type и cycle scope.
Restart behavior: После restart сверяется с terminal/deal history.
Отличие от: EventKey отличается от sibling-терминов источником `MT5 properties / persisted reconciled namespace`, классом `ACTUAL CONFIRMED` и стадией lifecycle `IDENTITY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `EventKey` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `EventKey` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### SnapshotFingerprint
CanonicalName: `SnapshotFingerprint`
Русское название: Снимок отпечаток
Краткое определение: SnapshotFingerprint — identity-сущность типа `FINGERPRINT` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Снимок отпечаток»; его authoritative provenance — «MT5 properties / persisted reconciled namespace».
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: Snapshot
Размерность: `FINGERPRINT`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `FINGERPRINT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для SnapshotFingerprint.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT HASH MATCH`
Lifecycle: SnapshotFingerprint создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object. Не мутирует; новый объект получает новое identity. Несовпадение scope либо закрытие объекта делает использование SnapshotFingerprint stale. authoritative identity текущего terminal/deal/event object. После завершения объекта остаётся историческим ключом и не переиспользуется. Этот lifecycle относится именно к объекту «Снимок отпечаток» и его собственному type/source contract.
Условия stale: Несовпадение scope либо закрытие объекта делает использование SnapshotFingerprint stale.
Authoritative replacement: authoritative identity текущего terminal/deal/event object.
Допустимые операции: сравнение и преобразование только по `FINGERPRINT` с `EXACT HASH MATCH` и explicit provenance.
Запрещённые подмены: SnapshotFingerprint нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Snapshot, тип FINGERPRINT, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: Tests/HybridSplitBig/test_catchup_dimension_safe.py::fingerprint
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: SnapshotFingerprint создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object.
Validation event: SnapshotFingerprint проверяется точным сравнением и scope filters.
Freeze/confirmation event: После выдачи SnapshotFingerprint неизменяем в пределах своего объекта.
Mutation events: Не мутирует; новый объект получает новое identity.
Stale triggers: Несовпадение scope либо закрытие объекта делает использование SnapshotFingerprint stale.
Replacement source: authoritative identity текущего terminal/deal/event object.
Terminal condition: После завершения объекта остаётся историческим ключом и не переиспользуется.
Persistence behavior: Persisted только вместе с type и cycle scope.
Restart behavior: После restart сверяется с terminal/deal history.
Отличие от: SnapshotFingerprint отличается от sibling-терминов источником `MT5 properties / persisted reconciled namespace`, классом `ACTUAL CONFIRMED` и стадией lifecycle `IDENTITY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `SnapshotFingerprint` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `SnapshotFingerprint` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=PARTIAL_MATCH.

### PlanFingerprint
CanonicalName: `PlanFingerprint`
Русское название: План отпечаток
Краткое определение: PlanFingerprint — identity-сущность типа `FINGERPRINT` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «План отпечаток»; его authoritative provenance — «MT5 properties / persisted reconciled namespace».
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: Plan
Размерность: `FINGERPRINT`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `FINGERPRINT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для PlanFingerprint.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT HASH MATCH`
Lifecycle: PlanFingerprint создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object. Не мутирует; новый объект получает новое identity. Несовпадение scope либо закрытие объекта делает использование PlanFingerprint stale. authoritative identity текущего terminal/deal/event object. После завершения объекта остаётся историческим ключом и не переиспользуется. Этот lifecycle относится именно к объекту «План отпечаток» и его собственному type/source contract.
Условия stale: Несовпадение scope либо закрытие объекта делает использование PlanFingerprint stale.
Authoritative replacement: authoritative identity текущего terminal/deal/event object.
Допустимые операции: сравнение и преобразование только по `FINGERPRINT` с `EXACT HASH MATCH` и explicit provenance.
Запрещённые подмены: PlanFingerprint нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Plan, тип FINGERPRINT, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: Tests/HybridSplitBig/test_catchup_dimension_safe.py::fingerprint
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: PlanFingerprint создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object.
Validation event: PlanFingerprint проверяется точным сравнением и scope filters.
Freeze/confirmation event: После выдачи PlanFingerprint неизменяем в пределах своего объекта.
Mutation events: Не мутирует; новый объект получает новое identity.
Stale triggers: Несовпадение scope либо закрытие объекта делает использование PlanFingerprint stale.
Replacement source: authoritative identity текущего terminal/deal/event object.
Terminal condition: После завершения объекта остаётся историческим ключом и не переиспользуется.
Persistence behavior: Persisted только вместе с type и cycle scope.
Restart behavior: После restart сверяется с terminal/deal history.
Отличие от: PlanFingerprint отличается от sibling-терминов источником `MT5 properties / persisted reconciled namespace`, классом `ACTUAL CONFIRMED` и стадией lifecycle `IDENTITY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `PlanFingerprint` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `PlanFingerprint` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=PARTIAL_MATCH.

### PositionComment
CanonicalName: `PositionComment`
Русское название: Позиция комментарий
Краткое определение: PositionComment — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Позиция комментарий»; его authoritative provenance — «MT5 properties / persisted reconciled namespace».
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: Position
Размерность: `DIAGNOSTIC_TEXT`
Unit: `diagnostic text`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для PositionComment.
Projected/Actual class: `ACTUAL OBSERVATION`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT STRUCTURE`
Lifecycle: PositionComment назначается approved role rule и связывается с position identity. PositionComment меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку PositionComment stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Позиция комментарий» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку PositionComment stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: PositionComment нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Position, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: PositionComment назначается approved role rule и связывается с position identity.
Validation event: Связка PositionComment проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: PositionComment меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку PositionComment stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: PositionComment отличается от sibling-терминов источником `MT5 properties / persisted reconciled namespace`, классом `ACTUAL CONFIRMED` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ROLE`; запись `PositionComment` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `PositionComment` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### SnapshotRevision
CanonicalName: `SnapshotRevision`
Русское название: Снимок ревизия
Краткое определение: SnapshotRevision — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Снимок ревизия»; его authoritative provenance — «MT5 properties / persisted reconciled namespace».
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: Snapshot
Размерность: `EVENT_ID`
Unit: `integer revision identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для SnapshotRevision.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: SnapshotRevision назначается approved role rule и связывается с position identity. SnapshotRevision меняет привязку только через подтверждённую promotion/reconciliation. Закрытие, замена ticket или потеря cycle identity делает привязку SnapshotRevision stale. новая reconciled role-to-position binding. После полного закрытия роль отвязывается; историческая связь сохраняется. Этот lifecycle относится именно к объекту «Снимок ревизия» и его собственному type/source contract.
Условия stale: Закрытие, замена ticket или потеря cycle identity делает привязку SnapshotRevision stale.
Authoritative replacement: новая reconciled role-to-position binding.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: SnapshotRevision нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Snapshot, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: SnapshotRevision назначается approved role rule и связывается с position identity.
Validation event: Связка SnapshotRevision проверяется по Symbol, MagicNumber, CycleID и ticket/identifier.
Freeze/confirmation event: Роль фиксируется при принятии позиции в managed cycle.
Mutation events: SnapshotRevision меняет привязку только через подтверждённую promotion/reconciliation.
Stale triggers: Закрытие, замена ticket или потеря cycle identity делает привязку SnapshotRevision stale.
Replacement source: новая reconciled role-to-position binding.
Terminal condition: После полного закрытия роль отвязывается; историческая связь сохраняется.
Persistence behavior: Сохраняются CycleID, role и event evidence, но не live cache.
Restart behavior: После restart роль восстанавливается из terminal/deal state, а не из comment.
Отличие от: SnapshotRevision отличается от sibling-терминов источником `MT5 properties / persisted reconciled namespace`, классом `ACTUAL CONFIRMED` и стадией lifecycle `ROLE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `ROLE`; запись `SnapshotRevision` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `SnapshotRevision` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### StateRevision
CanonicalName: `StateRevision`
Русское название: Состояние ревизия
Краткое определение: StateRevision — identity-сущность типа `EVENT_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Состояние ревизия»; его authoritative provenance — «MT5 properties / persisted reconciled namespace».
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: StateRevision
Размерность: `EVENT_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `EVENT_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для StateRevision.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: StateRevision создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object. Не мутирует; новый объект получает новое identity. Несовпадение scope либо закрытие объекта делает использование StateRevision stale. authoritative identity текущего terminal/deal/event object. После завершения объекта остаётся историческим ключом и не переиспользуется. Этот lifecycle относится именно к объекту «Состояние ревизия» и его собственному type/source contract.
Условия stale: Несовпадение scope либо закрытие объекта делает использование StateRevision stale.
Authoritative replacement: authoritative identity текущего terminal/deal/event object.
Допустимые операции: сравнение и преобразование только по `EVENT_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: StateRevision нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: StateRevision, тип EVENT_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::stateRevision
Python mapping: NONE_FOUND
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: StateRevision создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object.
Validation event: StateRevision проверяется точным сравнением и scope filters.
Freeze/confirmation event: После выдачи StateRevision неизменяем в пределах своего объекта.
Mutation events: Не мутирует; новый объект получает новое identity.
Stale triggers: Несовпадение scope либо закрытие объекта делает использование StateRevision stale.
Replacement source: authoritative identity текущего terminal/deal/event object.
Terminal condition: После завершения объекта остаётся историческим ключом и не переиспользуется.
Persistence behavior: Persisted только вместе с type и cycle scope.
Restart behavior: После restart сверяется с terminal/deal history.
Отличие от: StateRevision отличается от sibling-терминов источником `MT5 properties / persisted reconciled namespace`, классом `ACTUAL CONFIRMED` и стадией lifecycle `IDENTITY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `StateRevision` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `StateRevision` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### State
CanonicalName: `State`
Русское название: Состояние
Краткое определение: State — typed `STATE` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Состояние»; его authoritative provenance — «state machine or immutable snapshot/reconciliation».
Архитектурный профиль: Cycle lifecycle
Торговая роль: State
Размерность: `STATE`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `STATE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: ACTUAL/CONFIRMED stage для State.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: State создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение State историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Состояние» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение State историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: State нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: State, тип STATE, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::state
Python mapping: Tests/pending_open_big_contract_check.py::state
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: State создаётся соответствующим transition, gate или observation event.
Validation event: State проверяется точным enum/schema сравнением.
Freeze/confirmation event: State фиксируется вместе с CycleID и EventID.
Mutation events: Изменяется только явно разрешённым событием своего класса.
Stale triggers: Новая state revision делает прежнее current значение State историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: State отличается от sibling-терминов источником `state machine or immutable snapshot/reconciliation`, классом `ACTUAL/CONFIRMED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `State` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `State` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### Phase
CanonicalName: `Phase`
Русское название: Фаза
Краткое определение: Phase — typed `PHASE` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Фаза»; его authoritative provenance — «state machine or immutable snapshot/reconciliation».
Архитектурный профиль: Cycle lifecycle
Торговая роль: Phase
Размерность: `PHASE`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `PHASE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: ACTUAL/CONFIRMED stage для Phase.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: Phase создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение Phase историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Фаза» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение Phase историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `PHASE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: Phase нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Phase, тип PHASE, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/StateMachine.mqh::phaseValid
Python mapping: Tools/hybrid_small_state_machine.py::phase
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: Phase создаётся соответствующим transition, gate или observation event.
Validation event: Phase проверяется точным enum/schema сравнением.
Freeze/confirmation event: Phase фиксируется вместе с CycleID и EventID.
Mutation events: Изменяется только явно разрешённым событием своего класса.
Stale triggers: Новая state revision делает прежнее current значение Phase историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: Phase отличается от sibling-терминов источником `state machine or immutable snapshot/reconciliation`, классом `ACTUAL/CONFIRMED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `Phase` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `Phase` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### Event
CanonicalName: `Event`
Русское название: Событие
Краткое определение: Event — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Событие»; его authoritative provenance — «state machine or immutable snapshot/reconciliation».
Архитектурный профиль: Cycle lifecycle
Торговая роль: Event
Размерность: `OUTCOME`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `OUTCOME`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: ACTUAL/CONFIRMED stage для Event.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: Event создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение Event историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Событие» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение Event историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: Event нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Event, тип OUTCOME, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: Event создаётся соответствующим transition, gate или observation event.
Validation event: Event проверяется точным enum/schema сравнением.
Freeze/confirmation event: Event фиксируется вместе с CycleID и EventID.
Mutation events: Изменяется только явно разрешённым событием своего класса.
Stale triggers: Новая state revision делает прежнее current значение Event историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: Event отличается от sibling-терминов источником `state machine or immutable snapshot/reconciliation`, классом `ACTUAL/CONFIRMED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `Event` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `Event` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### Observation
CanonicalName: `Observation`
Русское название: Наблюдение
Краткое определение: Observation — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Наблюдение»; его authoritative provenance — «state machine or immutable snapshot/reconciliation».
Архитектурный профиль: Cycle lifecycle
Торговая роль: Observation
Размерность: `OUTCOME`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `OUTCOME`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: ACTUAL/CONFIRMED stage для Observation.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: Observation создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение Observation историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Наблюдение» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение Observation историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: Observation нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Observation, тип OUTCOME, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: Observation создаётся соответствующим transition, gate или observation event.
Validation event: Observation проверяется точным enum/schema сравнением.
Freeze/confirmation event: Observation фиксируется вместе с CycleID и EventID.
Mutation events: Изменяется только явно разрешённым событием своего класса.
Stale triggers: Новая state revision делает прежнее current значение Observation историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: Observation отличается от sibling-терминов источником `state machine or immutable snapshot/reconciliation`, классом `ACTUAL/CONFIRMED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `Observation` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `Observation` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### GateResult
CanonicalName: `GateResult`
Русское название: Шлюз результат
Краткое определение: GateResult — typed `GATE_RESULT` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Шлюз результат»; его authoritative provenance — «state machine or immutable snapshot/reconciliation».
Архитектурный профиль: Cycle lifecycle
Торговая роль: GateResult
Размерность: `GATE_RESULT`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `GATE_RESULT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: ACTUAL/CONFIRMED stage для GateResult.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: GateResult создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение GateResult историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Шлюз результат» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение GateResult историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `GATE_RESULT` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: GateResult нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: GateResult, тип GATE_RESULT, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: GateResult создаётся соответствующим transition, gate или observation event.
Validation event: GateResult проверяется точным enum/schema сравнением.
Freeze/confirmation event: GateResult фиксируется вместе с CycleID и EventID.
Mutation events: Изменяется только явно разрешённым событием своего класса.
Stale triggers: Новая state revision делает прежнее current значение GateResult историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: GateResult отличается от sibling-терминов источником `state machine or immutable snapshot/reconciliation`, классом `ACTUAL/CONFIRMED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `GateResult` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `GateResult` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### ExecutionResult
CanonicalName: `ExecutionResult`
Русское название: Исполнение результат
Краткое определение: ExecutionResult — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Исполнение результат»; его authoritative provenance — «state machine or immutable snapshot/reconciliation».
Архитектурный профиль: Cycle lifecycle
Торговая роль: ExecutionResult
Размерность: `OUTCOME`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `OUTCOME`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: ACTUAL/CONFIRMED stage для ExecutionResult.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: ExecutionResult создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение ExecutionResult историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Исполнение результат» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение ExecutionResult историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: ExecutionResult нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ExecutionResult, тип OUTCOME, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: ExecutionResult создаётся соответствующим transition, gate или observation event.
Validation event: ExecutionResult проверяется точным enum/schema сравнением.
Freeze/confirmation event: ExecutionResult фиксируется вместе с CycleID и EventID.
Mutation events: Изменяется только явно разрешённым событием своего класса.
Stale triggers: Новая state revision делает прежнее current значение ExecutionResult историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: ExecutionResult отличается от sibling-терминов источником `state machine or immutable snapshot/reconciliation`, классом `ACTUAL/CONFIRMED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `ExecutionResult` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ExecutionResult` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### Outcome
CanonicalName: `Outcome`
Русское название: Исход
Краткое определение: Outcome — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Исход»; его authoritative provenance — «state machine or immutable snapshot/reconciliation».
Архитектурный профиль: Cycle lifecycle
Торговая роль: Outcome
Размерность: `OUTCOME`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `OUTCOME`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: ACTUAL/CONFIRMED stage для Outcome.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: Outcome создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение Outcome историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Исход» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение Outcome историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: Outcome нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Outcome, тип OUTCOME, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::outcome
Python mapping: Tests/HybridSplitBig/test_catchup_stage12.py::Outcome
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: Outcome создаётся соответствующим transition, gate или observation event.
Validation event: Outcome проверяется точным enum/schema сравнением.
Freeze/confirmation event: Outcome фиксируется вместе с CycleID и EventID.
Mutation events: Изменяется только явно разрешённым событием своего класса.
Stale triggers: Новая state revision делает прежнее current значение Outcome историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: Outcome отличается от sibling-терминов источником `state machine or immutable snapshot/reconciliation`, классом `ACTUAL/CONFIRMED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `Outcome` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `Outcome` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### ReasonCode
CanonicalName: `ReasonCode`
Русское название: Причина код
Краткое определение: ReasonCode — typed `REASON_CODE` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Причина код»; его authoritative provenance — «state machine or immutable snapshot/reconciliation».
Архитектурный профиль: Cycle lifecycle
Торговая роль: ReasonCode
Размерность: `REASON_CODE`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `REASON_CODE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: ACTUAL/CONFIRMED stage для ReasonCode.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: ReasonCode создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение ReasonCode историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Причина код» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение ReasonCode историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `REASON_CODE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: ReasonCode нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ReasonCode, тип REASON_CODE, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::reasonCode
Python mapping: Tests/unit/test_split_recovery_order_model.py::reason_code
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: ReasonCode создаётся соответствующим transition, gate или observation event.
Validation event: ReasonCode проверяется точным enum/schema сравнением.
Freeze/confirmation event: ReasonCode фиксируется вместе с CycleID и EventID.
Mutation events: Изменяется только явно разрешённым событием своего класса.
Stale triggers: Новая state revision делает прежнее current значение ReasonCode историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: ReasonCode отличается от sibling-терминов источником `state machine or immutable snapshot/reconciliation`, классом `ACTUAL/CONFIRMED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `ReasonCode` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ReasonCode` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### ErrorCode
CanonicalName: `ErrorCode`
Русское название: Ошибка код
Краткое определение: ErrorCode — typed `REASON_CODE` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Ошибка код»; его authoritative provenance — «state machine or immutable snapshot/reconciliation».
Архитектурный профиль: Cycle lifecycle
Торговая роль: ErrorCode
Размерность: `REASON_CODE`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `REASON_CODE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: ACTUAL/CONFIRMED stage для ErrorCode.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: ErrorCode создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение ErrorCode историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Ошибка код» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение ErrorCode историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `REASON_CODE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: ErrorCode нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ErrorCode, тип REASON_CODE, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::error
Python mapping: Tests/HybridSplitBig/test_catchup_stage12.py::ERROR
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: ErrorCode создаётся соответствующим transition, gate или observation event.
Validation event: ErrorCode проверяется точным enum/schema сравнением.
Freeze/confirmation event: ErrorCode фиксируется вместе с CycleID и EventID.
Mutation events: Изменяется только явно разрешённым событием своего класса.
Stale triggers: Новая state revision делает прежнее current значение ErrorCode историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: ErrorCode отличается от sibling-терминов источником `state machine or immutable snapshot/reconciliation`, классом `ACTUAL/CONFIRMED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `ErrorCode` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ErrorCode` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### DiagnosticText
CanonicalName: `DiagnosticText`
Русское название: Диагностический текст
Краткое определение: DiagnosticText — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Диагностический текст»; его authoritative provenance — «state machine or immutable snapshot/reconciliation».
Архитектурный профиль: Cycle lifecycle
Торговая роль: DiagnosticText
Размерность: `OUTCOME`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `OUTCOME`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: ACTUAL/CONFIRMED stage для DiagnosticText.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: DiagnosticText создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение DiagnosticText историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Диагностический текст» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение DiagnosticText историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: DiagnosticText нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: DiagnosticText, тип OUTCOME, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: DiagnosticText создаётся соответствующим transition, gate или observation event.
Validation event: DiagnosticText проверяется точным enum/schema сравнением.
Freeze/confirmation event: DiagnosticText фиксируется вместе с CycleID и EventID.
Mutation events: Изменяется только явно разрешённым событием своего класса.
Stale triggers: Новая state revision делает прежнее current значение DiagnosticText историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: DiagnosticText отличается от sibling-терминов источником `state machine or immutable snapshot/reconciliation`, классом `ACTUAL/CONFIRMED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `DiagnosticText` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `DiagnosticText` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### CandidatePlan
CanonicalName: `CandidatePlan`
Русское название: Кандидат план
Краткое определение: CandidatePlan — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Кандидат план»; его authoritative provenance — «state machine or immutable snapshot/reconciliation».
Архитектурный профиль: Cycle lifecycle
Торговая роль: CandidatePlan
Размерность: `PLAN_OBJECT`
Unit: `structured plan`
Знак: not numeric
Допустимый диапазон: соответствует типу `OUTCOME`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: PROJECTED stage для CandidatePlan.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: CandidatePlan создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение CandidatePlan историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Кандидат план» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение CandidatePlan историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: CandidatePlan нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CandidatePlan, тип OUTCOME, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: PLAN
Creation event: CandidatePlan создаётся соответствующим transition, gate или observation event.
Validation event: CandidatePlan проверяется точным enum/schema сравнением.
Freeze/confirmation event: CandidatePlan фиксируется вместе с CycleID и EventID.
Mutation events: immutable; replacement creates a new revision
Stale triggers: Новая state revision делает прежнее current значение CandidatePlan историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: CandidatePlan отличается от sibling-терминов источником `state machine or immutable snapshot/reconciliation`, классом `PROJECTED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `CandidatePlan` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `CandidatePlan` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### ApprovedImmutablePlan
CanonicalName: `ApprovedImmutablePlan`
Русское название: Утверждённый неизменяемый план
Краткое определение: ApprovedImmutablePlan — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Утверждённый неизменяемый план»; его authoritative provenance — «state machine or immutable snapshot/reconciliation».
Архитектурный профиль: Cycle lifecycle
Торговая роль: ApprovedImmutablePlan
Размерность: `PLAN_OBJECT`
Unit: `structured plan`
Знак: not numeric
Допустимый диапазон: соответствует типу `OUTCOME`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: PROJECTED stage для ApprovedImmutablePlan.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: ApprovedImmutablePlan создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение ApprovedImmutablePlan историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Утверждённый неизменяемый план» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение ApprovedImmutablePlan историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: ApprovedImmutablePlan нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ApprovedImmutablePlan, тип OUTCOME, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: PLAN
Creation event: ApprovedImmutablePlan создаётся соответствующим transition, gate или observation event.
Validation event: ApprovedImmutablePlan проверяется точным enum/schema сравнением.
Freeze/confirmation event: ApprovedImmutablePlan фиксируется вместе с CycleID и EventID.
Mutation events: immutable; replacement creates a new revision
Stale triggers: Новая state revision делает прежнее current значение ApprovedImmutablePlan историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: ApprovedImmutablePlan отличается от sibling-терминов источником `state machine or immutable snapshot/reconciliation`, классом `PROJECTED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `ApprovedImmutablePlan` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ApprovedImmutablePlan` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### ExecutionRequest
CanonicalName: `ExecutionRequest`
Русское название: Исполнение запрос
Краткое определение: ExecutionRequest — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Исполнение запрос»; его authoritative provenance — «state machine or immutable snapshot/reconciliation».
Архитектурный профиль: Cycle lifecycle
Торговая роль: ExecutionRequest
Размерность: `EXECUTION_REQUEST`
Unit: `structured request`
Знак: not numeric
Допустимый диапазон: соответствует типу `OUTCOME`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: ACTUAL/CONFIRMED stage для ExecutionRequest.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: ExecutionRequest создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение ExecutionRequest историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Исполнение запрос» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение ExecutionRequest историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: ExecutionRequest нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ExecutionRequest, тип OUTCOME, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: EXECUTION_REQUEST
Creation event: ExecutionRequest создаётся соответствующим transition, gate или observation event.
Validation event: ExecutionRequest проверяется точным enum/schema сравнением.
Freeze/confirmation event: ExecutionRequest фиксируется вместе с CycleID и EventID.
Mutation events: immutable; replacement creates a new revision
Stale triggers: Новая state revision делает прежнее current значение ExecutionRequest историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: ExecutionRequest отличается от sibling-терминов источником `state machine or immutable snapshot/reconciliation`, классом `ACTUAL/CONFIRMED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `ExecutionRequest` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ExecutionRequest` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### BrokerExecutionResult
CanonicalName: `BrokerExecutionResult`
Русское название: Брокерский исполнение результат
Краткое определение: BrokerExecutionResult — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Брокерский исполнение результат»; его authoritative provenance — «state machine or immutable snapshot/reconciliation».
Архитектурный профиль: Cycle lifecycle
Торговая роль: BrokerExecutionResult
Размерность: `EXECUTION_RESULT`
Unit: `structured result`
Знак: not numeric
Допустимый диапазон: соответствует типу `OUTCOME`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: ACTUAL/CONFIRMED stage для BrokerExecutionResult.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: BrokerExecutionResult создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение BrokerExecutionResult историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Брокерский исполнение результат» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение BrokerExecutionResult историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: BrokerExecutionResult нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BrokerExecutionResult, тип OUTCOME, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: EXECUTION_RESULT
Creation event: BrokerExecutionResult создаётся соответствующим transition, gate или observation event.
Validation event: BrokerExecutionResult проверяется точным enum/schema сравнением.
Freeze/confirmation event: BrokerExecutionResult фиксируется вместе с CycleID и EventID.
Mutation events: immutable; replacement creates a new revision
Stale triggers: Новая state revision делает прежнее current значение BrokerExecutionResult историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: BrokerExecutionResult отличается от sibling-терминов источником `state machine or immutable snapshot/reconciliation`, классом `ACTUAL/CONFIRMED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `BrokerExecutionResult` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `BrokerExecutionResult` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### ReconciledResult
CanonicalName: `ReconciledResult`
Русское название: Сверенный результат
Краткое определение: ReconciledResult — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Сверенный результат»; его authoritative provenance — «state machine or immutable snapshot/reconciliation».
Архитектурный профиль: Cycle lifecycle
Торговая роль: ReconciledResult
Размерность: `RECONCILED_RESULT`
Unit: `structured result`
Знак: not numeric
Допустимый диапазон: соответствует типу `OUTCOME`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: ACTUAL/CONFIRMED stage для ReconciledResult.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: ReconciledResult создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение ReconciledResult историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Сверенный результат» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение ReconciledResult историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: ReconciledResult нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ReconciledResult, тип OUTCOME, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: OBJECT
Creation event: ReconciledResult создаётся соответствующим transition, gate или observation event.
Validation event: ReconciledResult проверяется точным enum/schema сравнением.
Freeze/confirmation event: ReconciledResult фиксируется вместе с CycleID и EventID.
Mutation events: immutable; replacement creates a new revision
Stale triggers: Новая state revision делает прежнее current значение ReconciledResult историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: ReconciledResult отличается от sibling-терминов источником `state machine or immutable snapshot/reconciliation`, классом `ACTUAL/CONFIRMED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `ReconciledResult` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ReconciledResult` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### CommittedLedgerEvent
CanonicalName: `CommittedLedgerEvent`
Русское название: Зафиксированный ledger событие
Краткое определение: CommittedLedgerEvent — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Зафиксированный ledger событие»; его authoritative provenance — «state machine or immutable snapshot/reconciliation».
Архитектурный профиль: Cycle lifecycle
Торговая роль: CommittedLedgerEvent
Размерность: `LEDGER_EVENT`
Unit: `structured event`
Знак: not numeric
Допустимый диапазон: соответствует типу `OUTCOME`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: ACTUAL/CONFIRMED stage для CommittedLedgerEvent.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: CommittedLedgerEvent создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение CommittedLedgerEvent историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Зафиксированный ledger событие» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение CommittedLedgerEvent историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: CommittedLedgerEvent нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CommittedLedgerEvent, тип OUTCOME, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: LEDGER
Creation event: CommittedLedgerEvent создаётся соответствующим transition, gate или observation event.
Validation event: CommittedLedgerEvent проверяется точным enum/schema сравнением.
Freeze/confirmation event: CommittedLedgerEvent фиксируется вместе с CycleID и EventID.
Mutation events: immutable; replacement creates a new revision
Stale triggers: Новая state revision делает прежнее current значение CommittedLedgerEvent историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: CommittedLedgerEvent отличается от sibling-терминов источником `state machine or immutable snapshot/reconciliation`, классом `ACTUAL/CONFIRMED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `CommittedLedgerEvent` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `CommittedLedgerEvent` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### BaseSnapshot
CanonicalName: `BaseSnapshot`
Русское название: Базовая снимок
Краткое определение: BaseSnapshot — typed `STATE` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Базовая снимок»; его authoritative provenance — «state machine or immutable snapshot/reconciliation».
Архитектурный профиль: Cycle lifecycle
Торговая роль: BaseSnapshot
Размерность: `SNAPSHOT_PROJECTED`
Unit: `structured snapshot`
Знак: not numeric
Допустимый диапазон: соответствует типу `STATE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: PROJECTED stage для BaseSnapshot.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: BaseSnapshot создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение BaseSnapshot историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Базовая снимок» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение BaseSnapshot историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: BaseSnapshot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BaseSnapshot, тип STATE, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: SNAPSHOT
Creation event: BaseSnapshot создаётся соответствующим transition, gate или observation event.
Validation event: BaseSnapshot проверяется точным enum/schema сравнением.
Freeze/confirmation event: BaseSnapshot фиксируется вместе с CycleID и EventID.
Mutation events: immutable; replacement creates a new revision
Stale triggers: Новая state revision делает прежнее current значение BaseSnapshot историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: BaseSnapshot отличается от sibling-терминов источником `state machine or immutable snapshot/reconciliation`, классом `PROJECTED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `BaseSnapshot` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `BaseSnapshot` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### WorstSnapshot
CanonicalName: `WorstSnapshot`
Русское название: Worst снимок
Краткое определение: WorstSnapshot — typed `STATE` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Worst снимок»; его authoritative provenance — «state machine or immutable snapshot/reconciliation».
Архитектурный профиль: Cycle lifecycle
Торговая роль: WorstSnapshot
Размерность: `SNAPSHOT_WORST_CASE`
Unit: `structured snapshot`
Знак: not numeric
Допустимый диапазон: соответствует типу `STATE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: PROJECTED stage для WorstSnapshot.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: WorstSnapshot создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение WorstSnapshot историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Worst снимок» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение WorstSnapshot историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: WorstSnapshot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: WorstSnapshot, тип STATE, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: SNAPSHOT
Creation event: WorstSnapshot создаётся соответствующим transition, gate или observation event.
Validation event: WorstSnapshot проверяется точным enum/schema сравнением.
Freeze/confirmation event: WorstSnapshot фиксируется вместе с CycleID и EventID.
Mutation events: immutable; replacement creates a new revision
Stale triggers: Новая state revision делает прежнее current значение WorstSnapshot историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: WorstSnapshot отличается от sibling-терминов источником `state machine or immutable snapshot/reconciliation`, классом `PROJECTED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `WorstSnapshot` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `WorstSnapshot` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### ActualSnapshot
CanonicalName: `ActualSnapshot`
Русское название: Фактический снимок
Краткое определение: ActualSnapshot — typed `STATE` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Фактический снимок»; его authoritative provenance — «state machine or immutable snapshot/reconciliation».
Архитектурный профиль: Cycle lifecycle
Торговая роль: ActualSnapshot
Размерность: `SNAPSHOT_ACTUAL`
Unit: `structured snapshot`
Знак: not numeric
Допустимый диапазон: соответствует типу `STATE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: ACTUAL/CONFIRMED stage для ActualSnapshot.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: ActualSnapshot создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение ActualSnapshot историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Фактический снимок» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение ActualSnapshot историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: ActualSnapshot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ActualSnapshot, тип STATE, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: SNAPSHOT
Creation event: ActualSnapshot создаётся соответствующим transition, gate или observation event.
Validation event: ActualSnapshot проверяется точным enum/schema сравнением.
Freeze/confirmation event: ActualSnapshot фиксируется вместе с CycleID и EventID.
Mutation events: immutable; replacement creates a new revision
Stale triggers: Новая state revision делает прежнее current значение ActualSnapshot историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: ActualSnapshot отличается от sibling-терминов источником `state machine or immutable snapshot/reconciliation`, классом `ACTUAL/CONFIRMED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `ActualSnapshot` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ActualSnapshot` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### SnapshotStaleFlag
CanonicalName: `SnapshotStaleFlag`
Русское название: Снимок устаревший признак
Краткое определение: SnapshotStaleFlag — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Снимок устаревший признак»; его authoritative provenance — «state machine or immutable snapshot/reconciliation».
Архитектурный профиль: Cycle lifecycle
Торговая роль: Snapshot
Размерность: `OUTCOME`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `OUTCOME`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: ACTUAL/CONFIRMED stage для SnapshotStaleFlag.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: SnapshotStaleFlag создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение SnapshotStaleFlag историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Снимок устаревший признак» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение SnapshotStaleFlag историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: SnapshotStaleFlag нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Snapshot, тип OUTCOME, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: SnapshotStaleFlag создаётся соответствующим transition, gate или observation event.
Validation event: SnapshotStaleFlag проверяется точным enum/schema сравнением.
Freeze/confirmation event: SnapshotStaleFlag фиксируется вместе с CycleID и EventID.
Mutation events: Изменяется только явно разрешённым событием своего класса.
Stale triggers: Новая state revision делает прежнее current значение SnapshotStaleFlag историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: SnapshotStaleFlag отличается от sibling-терминов источником `state machine or immutable snapshot/reconciliation`, классом `ACTUAL/CONFIRMED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `SnapshotStaleFlag` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `SnapshotStaleFlag` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### FinalClosePreview
CanonicalName: `FinalClosePreview`
Русское название: Финальный закрытие preview
Краткое определение: FinalClosePreview — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Финальный закрытие preview»; его authoritative provenance — «state machine or immutable snapshot/reconciliation».
Архитектурный профиль: Cycle lifecycle
Торговая роль: FinalClosePreview
Размерность: `OUTCOME`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `OUTCOME`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: PROJECTED stage для FinalClosePreview.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: FinalClosePreview создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение FinalClosePreview историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Финальный закрытие preview» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение FinalClosePreview историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: FinalClosePreview нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: FinalClosePreview, тип OUTCOME, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::finalClosePreviewRequired
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: FinalClosePreview создаётся соответствующим transition, gate или observation event.
Validation event: FinalClosePreview проверяется точным enum/schema сравнением.
Freeze/confirmation event: FinalClosePreview фиксируется вместе с CycleID и EventID.
Mutation events: Изменяется только явно разрешённым событием своего класса.
Stale triggers: Новая state revision делает прежнее current значение FinalClosePreview историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: FinalClosePreview отличается от sibling-терминов источником `state machine or immutable snapshot/reconciliation`, классом `PROJECTED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `FinalClosePreview` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `FinalClosePreview` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### FinalCloseActualSuccess
CanonicalName: `FinalCloseActualSuccess`
Русское название: Финальный закрытие фактический успех
Краткое определение: FinalCloseActualSuccess — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «Финальный закрытие фактический успех»; его authoritative provenance — «state machine or immutable snapshot/reconciliation».
Архитектурный профиль: Cycle lifecycle
Торговая роль: FinalCloseActualSuccess
Размерность: `OUTCOME`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `OUTCOME`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: ACTUAL/CONFIRMED stage для FinalCloseActualSuccess.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: FinalCloseActualSuccess создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение FinalCloseActualSuccess историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «Финальный закрытие фактический успех» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение FinalCloseActualSuccess историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: FinalCloseActualSuccess нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: FinalCloseActualSuccess, тип OUTCOME, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: FinalCloseActualSuccess создаётся соответствующим transition, gate или observation event.
Validation event: FinalCloseActualSuccess проверяется точным enum/schema сравнением.
Freeze/confirmation event: FinalCloseActualSuccess фиксируется вместе с CycleID и EventID.
Mutation events: Изменяется только явно разрешённым событием своего класса.
Stale triggers: Новая state revision делает прежнее current значение FinalCloseActualSuccess историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: FinalCloseActualSuccess отличается от sibling-терминов источником `state machine or immutable snapshot/reconciliation`, классом `ACTUAL/CONFIRMED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `FinalCloseActualSuccess` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `FinalCloseActualSuccess` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### MoneyTolerance
CanonicalName: `MoneyTolerance`
Русское название: Денежный допуск
Краткое определение: MoneyTolerance — денежная величина `MoneyTolerance` класса `POLICY` со знаком «>=0»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Денежный допуск»; его authoritative provenance — «approved config/symbol properties».
Архитектурный профиль: Dimension-specific only
Торговая роль: MoneyTolerance
Размерность: `MONEY_TOLERANCE`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_AVAILABLE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved config/symbol properties
Authoritative source: typed tolerance policy/configuration or symbol-property threshold
Время фиксации: POLICY stage для MoneyTolerance.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: MoneyTolerance вычисляется из snapshot inputs: approved config/symbol properties. Не мутирует; изменение inputs создаёт новую revision MoneyTolerance. Market, symbol, config или snapshot revision делает MoneyTolerance stale. пересчёт MoneyTolerance на новом immutable snapshot. После execution projected MoneyTolerance завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Денежный допуск» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает MoneyTolerance stale.
Authoritative replacement: пересчёт MoneyTolerance на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `MONEY_AVAILABLE` с `self` и explicit provenance.
Запрещённые подмены: MoneyTolerance нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: MoneyTolerance, тип MONEY_AVAILABLE, class POLICY.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: TOLERANCE
Lifecycle class: TOLERANCE
Creation event: MoneyTolerance вычисляется из snapshot inputs: approved config/symbol properties.
Validation event: MoneyTolerance валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: MoneyTolerance замораживается только внутри Candidate/ApprovedPlan.
Mutation events: immutable; replacement creates a new revision
Stale triggers: Market, symbol, config или snapshot revision делает MoneyTolerance stale.
Replacement source: пересчёт MoneyTolerance на новом immutable snapshot.
Terminal condition: После execution projected MoneyTolerance завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: MoneyTolerance отличается от sibling-терминов источником `approved config/symbol properties`, классом `POLICY` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `MoneyTolerance` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `MoneyTolerance` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### VolumeToleranceLots
CanonicalName: `VolumeToleranceLots`
Русское название: Объём допуск lots
Краткое определение: VolumeToleranceLots — объём `VolumeToleranceLots` на стадии явно указанного lot lifecycle; он отличается от соседних lot stages источником `approved config/symbol properties` и не может использоваться как их evidence. Отличительный объект записи: «Объём допуск lots»; его authoritative provenance — «approved config/symbol properties».
Архитектурный профиль: Dimension-specific only
Торговая роль: VolumeToleranceLots
Размерность: `LOT_TOLERANCE`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_NORMALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved config/symbol properties
Authoritative source: typed tolerance policy/configuration or symbol-property threshold
Время фиксации: POLICY stage для VolumeToleranceLots.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: VolumeToleranceLots вычисляется из snapshot inputs: approved config/symbol properties. Не мутирует; изменение inputs создаёт новую revision VolumeToleranceLots. Market, symbol, config или snapshot revision делает VolumeToleranceLots stale. пересчёт VolumeToleranceLots на новом immutable snapshot. После execution projected VolumeToleranceLots завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Объём допуск lots» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает VolumeToleranceLots stale.
Authoritative replacement: пересчёт VolumeToleranceLots на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_NORMALIZED` с `self` и explicit provenance.
Запрещённые подмены: VolumeToleranceLots нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: VolumeToleranceLots, тип LOT_NORMALIZED, class POLICY.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: TOLERANCE
Lifecycle class: TOLERANCE
Creation event: VolumeToleranceLots вычисляется из snapshot inputs: approved config/symbol properties.
Validation event: VolumeToleranceLots валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: VolumeToleranceLots замораживается только внутри Candidate/ApprovedPlan.
Mutation events: immutable; replacement creates a new revision
Stale triggers: Market, symbol, config или snapshot revision делает VolumeToleranceLots stale.
Replacement source: пересчёт VolumeToleranceLots на новом immutable snapshot.
Terminal condition: После execution projected VolumeToleranceLots завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: VolumeToleranceLots отличается от sibling-терминов источником `approved config/symbol properties`, классом `POLICY` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `VolumeToleranceLots` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `VolumeToleranceLots` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### PriceTolerance
CanonicalName: `PriceTolerance`
Русское название: Цена допуск
Краткое определение: PriceTolerance — symbol-bound величина `PriceTolerance` типа `PRICE_PROJECTED`, получаемая из approved config/symbol properties; она не является money или lot и не использует их tolerance. Отличительный объект записи: «Цена допуск»; его authoritative provenance — «approved config/symbol properties».
Архитектурный профиль: Dimension-specific only
Торговая роль: PriceTolerance
Размерность: `PRICE_TOLERANCE`
Unit: `price`
Знак: >= 0
Допустимый диапазон: соответствует типу `PRICE_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved config/symbol properties
Authoritative source: typed tolerance policy/configuration or symbol-property threshold
Время фиксации: POLICY stage для PriceTolerance.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: PriceTolerance вычисляется из snapshot inputs: approved config/symbol properties. Не мутирует; изменение inputs создаёт новую revision PriceTolerance. Market, symbol, config или snapshot revision делает PriceTolerance stale. пересчёт PriceTolerance на новом immutable snapshot. После execution projected PriceTolerance завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Цена допуск» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает PriceTolerance stale.
Authoritative replacement: пересчёт PriceTolerance на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `PRICE_PROJECTED` с `self` и explicit provenance.
Запрещённые подмены: PriceTolerance нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PriceTolerance, тип PRICE_PROJECTED, class POLICY.
Legacy aliases: —
MQL5 mapping: Include/HybridCatchUpModel.mqh::priceTolerance
Python mapping: Tests/HybridSplitBig/test_catchup_dimension_safe.py::price_tolerance
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: TOLERANCE
Lifecycle class: TOLERANCE
Creation event: PriceTolerance вычисляется из snapshot inputs: approved config/symbol properties.
Validation event: PriceTolerance валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: PriceTolerance замораживается только внутри Candidate/ApprovedPlan.
Mutation events: immutable; replacement creates a new revision
Stale triggers: Market, symbol, config или snapshot revision делает PriceTolerance stale.
Replacement source: пересчёт PriceTolerance на новом immutable snapshot.
Terminal condition: После execution projected PriceTolerance завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: PriceTolerance отличается от sibling-терминов источником `approved config/symbol properties`, классом `POLICY` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `PriceTolerance` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `PriceTolerance` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### PointTolerance
CanonicalName: `PointTolerance`
Русское название: Размер пункта допуск
Краткое определение: PointTolerance — самостоятельная нормативная сущность `POINTS`: её значение возникает из `approved config/symbol properties` и отличается от связанных терминов lifecycle class `POLICY`. Отличительный объект записи: «Размер пункта допуск»; его authoritative provenance — «approved config/symbol properties».
Архитектурный профиль: Dimension-specific only
Торговая роль: PointTolerance
Размерность: `POINT_TOLERANCE`
Unit: `point`
Знак: >= 0
Допустимый диапазон: соответствует типу `POINTS`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved config/symbol properties
Authoritative source: typed tolerance policy/configuration or symbol-property threshold
Время фиксации: POLICY stage для PointTolerance.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: PointTolerance вычисляется из snapshot inputs: approved config/symbol properties. Не мутирует; изменение inputs создаёт новую revision PointTolerance. Market, symbol, config или snapshot revision делает PointTolerance stale. пересчёт PointTolerance на новом immutable snapshot. После execution projected PointTolerance завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Размер пункта допуск» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает PointTolerance stale.
Authoritative replacement: пересчёт PointTolerance на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `POINTS` с `self` и explicit provenance.
Запрещённые подмены: PointTolerance нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PointTolerance, тип POINTS, class POLICY.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: TOLERANCE
Lifecycle class: TOLERANCE
Creation event: PointTolerance вычисляется из snapshot inputs: approved config/symbol properties.
Validation event: PointTolerance валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: PointTolerance замораживается только внутри Candidate/ApprovedPlan.
Mutation events: immutable; replacement creates a new revision
Stale triggers: Market, symbol, config или snapshot revision делает PointTolerance stale.
Replacement source: пересчёт PointTolerance на новом immutable snapshot.
Terminal condition: После execution projected PointTolerance завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: PointTolerance отличается от sibling-терминов источником `approved config/symbol properties`, классом `POLICY` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `PointTolerance` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `PointTolerance` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### RatioTolerance
CanonicalName: `RatioTolerance`
Русское название: Отношение допуск
Краткое определение: RatioTolerance — безразмерная величина типа `RATIO` для RatioTolerance; она не интерпретируется как lot, money или percent без явной conversion. Отличительный объект записи: «Отношение допуск»; его authoritative provenance — «approved config/symbol properties».
Архитектурный профиль: Dimension-specific only
Торговая роль: RatioTolerance
Размерность: `RATIO_TOLERANCE`
Unit: `dimensionless ratio`
Знак: >= 0
Допустимый диапазон: соответствует типу `RATIO`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved config/symbol properties
Authoritative source: typed tolerance policy/configuration or symbol-property threshold
Время фиксации: POLICY stage для RatioTolerance.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: RatioTolerance загружается из выбранного документального/конфигурационного профиля. Внутри замороженного цикла RatioTolerance не изменяется; новая ревизия относится к новому plan. Изменение профиля или revision делает прежний RatioTolerance stale. новое approved значение RatioTolerance из явно выбранного профиля. Завершается вместе с конфигурационным scope цикла. Этот lifecycle относится именно к объекту «Отношение допуск» и его собственному type/source contract.
Условия stale: Изменение профиля или revision делает прежний RatioTolerance stale.
Authoritative replacement: новое approved значение RatioTolerance из явно выбранного профиля.
Допустимые операции: сравнение и преобразование только по `RATIO` с `self` и explicit provenance.
Запрещённые подмены: RatioTolerance нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RatioTolerance, тип RATIO, class POLICY.
Legacy aliases: —
MQL5 mapping: Include/HybridCatchUpModel.mqh::HybridRatioTolerance
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: TOLERANCE
Lifecycle class: TOLERANCE
Creation event: RatioTolerance загружается из выбранного документального/конфигурационного профиля.
Validation event: RatioTolerance проверяется как POLICY до фиксации цикла.
Freeze/confirmation event: RatioTolerance замораживается в конфигурации конкретного CycleID.
Mutation events: immutable; replacement creates a new revision
Stale triggers: Изменение профиля или revision делает прежний RatioTolerance stale.
Replacement source: новое approved значение RatioTolerance из явно выбранного профиля.
Terminal condition: Завершается вместе с конфигурационным scope цикла.
Persistence behavior: Хранится с profile revision и CycleID.
Restart behavior: После restart перечитывается и сверяется с frozen cycle configuration.
Отличие от: RatioTolerance отличается от sibling-терминов источником `approved config/symbol properties`, классом `POLICY` и стадией lifecycle `POLICY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `POLICY`; запись `RatioTolerance` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `RatioTolerance` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### ComparisonEpsilon
CanonicalName: `ComparisonEpsilon`
Русское название: Comparison epsilon
Краткое определение: ComparisonEpsilon — identity-сущность типа `FINGERPRINT` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Comparison epsilon»; его authoritative provenance — «approved config/symbol properties».
Архитектурный профиль: Dimension-specific only
Торговая роль: ComparisonEpsilon
Размерность: `COMPARISON_EPSILON`
Unit: `dimensionless epsilon`
Знак: >= 0
Допустимый диапазон: соответствует типу `FINGERPRINT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved config/symbol properties
Authoritative source: typed tolerance policy/configuration or symbol-property threshold
Время фиксации: POLICY stage для ComparisonEpsilon.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: ComparisonEpsilon создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object. Не мутирует; новый объект получает новое identity. Несовпадение scope либо закрытие объекта делает использование ComparisonEpsilon stale. authoritative identity текущего terminal/deal/event object. После завершения объекта остаётся историческим ключом и не переиспользуется. Этот lifecycle относится именно к объекту «Comparison epsilon» и его собственному type/source contract.
Условия stale: Несовпадение scope либо закрытие объекта делает использование ComparisonEpsilon stale.
Authoritative replacement: authoritative identity текущего terminal/deal/event object.
Допустимые операции: сравнение и преобразование только по `FINGERPRINT` с `EXACT HASH MATCH` и explicit provenance.
Запрещённые подмены: ComparisonEpsilon нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ComparisonEpsilon, тип FINGERPRINT, class POLICY.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: TOLERANCE
Lifecycle class: TOLERANCE
Creation event: ComparisonEpsilon создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object.
Validation event: ComparisonEpsilon проверяется точным сравнением и scope filters.
Freeze/confirmation event: После выдачи ComparisonEpsilon неизменяем в пределах своего объекта.
Mutation events: immutable; replacement creates a new revision
Stale triggers: Несовпадение scope либо закрытие объекта делает использование ComparisonEpsilon stale.
Replacement source: authoritative identity текущего terminal/deal/event object.
Terminal condition: После завершения объекта остаётся историческим ключом и не переиспользуется.
Persistence behavior: Persisted только вместе с type и cycle scope.
Restart behavior: После restart сверяется с terminal/deal history.
Отличие от: ComparisonEpsilon отличается от sibling-терминов источником `approved config/symbol properties`, классом `POLICY` и стадией lifecycle `IDENTITY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `ComparisonEpsilon` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ComparisonEpsilon` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### ReserveMismatchTolerance
CanonicalName: `ReserveMismatchTolerance`
Русское название: Резерв mismatch допуск
Краткое определение: ReserveMismatchTolerance — денежная величина `Reserve` класса `POLICY` со знаком «>=0»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «Резерв mismatch допуск»; его authoritative provenance — «approved config/symbol properties».
Архитектурный профиль: Dimension-specific only
Торговая роль: Reserve
Размерность: `MONEY_TOLERANCE`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_AVAILABLE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved config/symbol properties
Authoritative source: typed tolerance policy/configuration or symbol-property threshold
Время фиксации: POLICY stage для ReserveMismatchTolerance.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: ReserveMismatchTolerance вычисляется из snapshot inputs: approved config/symbol properties. Не мутирует; изменение inputs создаёт новую revision ReserveMismatchTolerance. Market, symbol, config или snapshot revision делает ReserveMismatchTolerance stale. пересчёт ReserveMismatchTolerance на новом immutable snapshot. После execution projected ReserveMismatchTolerance завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Резерв mismatch допуск» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает ReserveMismatchTolerance stale.
Authoritative replacement: пересчёт ReserveMismatchTolerance на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `MONEY_AVAILABLE` с `self` и explicit provenance.
Запрещённые подмены: ReserveMismatchTolerance нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Reserve, тип MONEY_AVAILABLE, class POLICY.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: TOLERANCE
Lifecycle class: TOLERANCE
Creation event: ReserveMismatchTolerance вычисляется из snapshot inputs: approved config/symbol properties.
Validation event: ReserveMismatchTolerance валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: ReserveMismatchTolerance замораживается только внутри Candidate/ApprovedPlan.
Mutation events: immutable; replacement creates a new revision
Stale triggers: Market, symbol, config или snapshot revision делает ReserveMismatchTolerance stale.
Replacement source: пересчёт ReserveMismatchTolerance на новом immutable snapshot.
Terminal condition: После execution projected ReserveMismatchTolerance завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: ReserveMismatchTolerance отличается от sibling-терминов источником `approved config/symbol properties`, классом `POLICY` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `ReserveMismatchTolerance` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ReserveMismatchTolerance` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### GeometryTolerance
CanonicalName: `GeometryTolerance`
Русское название: Геометрический допуск
Краткое определение: GeometryTolerance — объём `GeometryTolerance` на стадии явно указанного lot lifecycle; он отличается от соседних lot stages источником `approved config/symbol properties` и не может использоваться как их evidence. Отличительный объект записи: «Геометрический допуск»; его authoritative provenance — «approved config/symbol properties».
Архитектурный профиль: Dimension-specific only
Торговая роль: GeometryTolerance
Размерность: `LOT_TOLERANCE`
Unit: `lot`
Знак: >= 0
Допустимый диапазон: соответствует типу `LOT_NORMALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved config/symbol properties
Authoritative source: typed tolerance policy/configuration or symbol-property threshold
Время фиксации: POLICY stage для GeometryTolerance.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: GeometryTolerance вычисляется из snapshot inputs: approved config/symbol properties. Не мутирует; изменение inputs создаёт новую revision GeometryTolerance. Market, symbol, config или snapshot revision делает GeometryTolerance stale. пересчёт GeometryTolerance на новом immutable snapshot. После execution projected GeometryTolerance завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Геометрический допуск» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает GeometryTolerance stale.
Authoritative replacement: пересчёт GeometryTolerance на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_NORMALIZED` с `self` и explicit provenance.
Запрещённые подмены: GeometryTolerance нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: GeometryTolerance, тип LOT_NORMALIZED, class POLICY.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: TOLERANCE
Lifecycle class: TOLERANCE
Creation event: GeometryTolerance вычисляется из snapshot inputs: approved config/symbol properties.
Validation event: GeometryTolerance валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: GeometryTolerance замораживается только внутри Candidate/ApprovedPlan.
Mutation events: immutable; replacement creates a new revision
Stale triggers: Market, symbol, config или snapshot revision делает GeometryTolerance stale.
Replacement source: пересчёт GeometryTolerance на новом immutable snapshot.
Terminal condition: После execution projected GeometryTolerance завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: GeometryTolerance отличается от sibling-терминов источником `approved config/symbol properties`, классом `POLICY` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `GeometryTolerance` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `GeometryTolerance` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### FingerprintTolerance
CanonicalName: `FingerprintTolerance`
Русское название: Отпечаток допуск
Краткое определение: FingerprintTolerance — identity-сущность типа `FINGERPRINT` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «Отпечаток допуск»; его authoritative provenance — «approved config/symbol properties».
Архитектурный профиль: Dimension-specific only
Торговая роль: FingerprintTolerance
Размерность: `IDENTITY_MATCH_POLICY`
Unit: `dimensionless policy`
Знак: >= 0
Допустимый диапазон: соответствует типу `FINGERPRINT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved config/symbol properties
Authoritative source: typed tolerance policy/configuration or symbol-property threshold
Время фиксации: POLICY stage для FingerprintTolerance.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: FingerprintTolerance создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object. Не мутирует; новый объект получает новое identity. Несовпадение scope либо закрытие объекта делает использование FingerprintTolerance stale. authoritative identity текущего terminal/deal/event object. После завершения объекта остаётся историческим ключом и не переиспользуется. Этот lifecycle относится именно к объекту «Отпечаток допуск» и его собственному type/source contract.
Условия stale: Несовпадение scope либо закрытие объекта делает использование FingerprintTolerance stale.
Authoritative replacement: authoritative identity текущего terminal/deal/event object.
Допустимые операции: сравнение и преобразование только по `FINGERPRINT` с `EXACT HASH MATCH` и explicit provenance.
Запрещённые подмены: FingerprintTolerance нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: FingerprintTolerance, тип FINGERPRINT, class POLICY.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: Tests/HybridSplitBig/test_catchup_dimension_safe.py::fingerprint
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: TOLERANCE
Lifecycle class: TOLERANCE
Creation event: FingerprintTolerance создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object.
Validation event: FingerprintTolerance проверяется точным сравнением и scope filters.
Freeze/confirmation event: После выдачи FingerprintTolerance неизменяем в пределах своего объекта.
Mutation events: immutable; replacement creates a new revision
Stale triggers: Несовпадение scope либо закрытие объекта делает использование FingerprintTolerance stale.
Replacement source: authoritative identity текущего terminal/deal/event object.
Terminal condition: После завершения объекта остаётся историческим ключом и не переиспользуется.
Persistence behavior: Persisted только вместе с type и cycle scope.
Restart behavior: После restart сверяется с terminal/deal history.
Отличие от: FingerprintTolerance отличается от sibling-терминов источником `approved config/symbol properties`, классом `POLICY` и стадией lifecycle `IDENTITY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `FingerprintTolerance` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `FingerprintTolerance` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=PARTIAL_MATCH.

### ProjectedData
CanonicalName: `ProjectedData`
Русское название: Прогнозный данные
Краткое определение: ProjectedData — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `PROJECTED`. Отличительный объект записи: «Прогнозный данные»; его authoritative provenance — «lifecycle transition evidence».
Архитектурный профиль: All
Торговая роль: ProjectedData
Размерность: `BOOLEAN_RESULT`
Unit: `data-state enum`
Знак: not numeric
Допустимый диапазон: соответствует типу `BOOLEAN_RESULT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: PROJECTED stage для ProjectedData.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: ProjectedData вычисляется из snapshot inputs: lifecycle transition evidence. Не мутирует; изменение inputs создаёт новую revision ProjectedData. Market, symbol, config или snapshot revision делает ProjectedData stale. пересчёт ProjectedData на новом immutable snapshot. После execution projected ProjectedData завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Прогнозный данные» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает ProjectedData stale.
Authoritative replacement: пересчёт ProjectedData на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: ProjectedData нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ProjectedData, тип BOOLEAN_RESULT, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: OBJECT
Creation event: ProjectedData вычисляется из snapshot inputs: lifecycle transition evidence.
Validation event: ProjectedData валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: ProjectedData замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision ProjectedData.
Stale triggers: Market, symbol, config или snapshot revision делает ProjectedData stale.
Replacement source: пересчёт ProjectedData на новом immutable snapshot.
Terminal condition: После execution projected ProjectedData завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: ProjectedData отличается от sibling-терминов источником `lifecycle transition evidence`, классом `PROJECTED` и стадией lifecycle `OBJECT`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `OBJECT`; запись `ProjectedData` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ProjectedData` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### RequestedData
CanonicalName: `RequestedData`
Русское название: Запрошенный данные
Краткое определение: RequestedData — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `REQUESTED`. Отличительный объект записи: «Запрошенный данные»; его authoritative provenance — «lifecycle transition evidence».
Архитектурный профиль: All
Торговая роль: RequestedData
Размерность: `BOOLEAN_RESULT`
Unit: `data-state enum`
Знак: not numeric
Допустимый диапазон: соответствует типу `BOOLEAN_RESULT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: REQUESTED stage для RequestedData.
Projected/Actual class: `REQUESTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: RequestedData вычисляется из snapshot inputs: lifecycle transition evidence. Не мутирует; изменение inputs создаёт новую revision RequestedData. Market, symbol, config или snapshot revision делает RequestedData stale. пересчёт RequestedData на новом immutable snapshot. После execution projected RequestedData завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Запрошенный данные» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает RequestedData stale.
Authoritative replacement: пересчёт RequestedData на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: RequestedData нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RequestedData, тип BOOLEAN_RESULT, class REQUESTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: Tests/unit/test_money_completion_behavior.py::requested
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: OBJECT
Creation event: RequestedData вычисляется из snapshot inputs: lifecycle transition evidence.
Validation event: RequestedData валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: RequestedData замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision RequestedData.
Stale triggers: Market, symbol, config или snapshot revision делает RequestedData stale.
Replacement source: пересчёт RequestedData на новом immutable snapshot.
Terminal condition: После execution projected RequestedData завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: RequestedData отличается от sibling-терминов источником `lifecycle transition evidence`, классом `REQUESTED` и стадией lifecycle `OBJECT`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `OBJECT`; запись `RequestedData` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `RequestedData` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=PARTIAL_MATCH.

### ExecutedData
CanonicalName: `ExecutedData`
Русское название: Исполненная данные
Краткое определение: ExecutedData — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `EXECUTED`. Отличительный объект записи: «Исполненная данные»; его authoritative provenance — «lifecycle transition evidence».
Архитектурный профиль: All
Торговая роль: ExecutedData
Размерность: `BOOLEAN_RESULT`
Unit: `data-state enum`
Знак: not numeric
Допустимый диапазон: соответствует типу `BOOLEAN_RESULT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: EXECUTED stage для ExecutedData.
Projected/Actual class: `EXECUTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: ExecutedData вычисляется из snapshot inputs: lifecycle transition evidence. Не мутирует; изменение inputs создаёт новую revision ExecutedData. Market, symbol, config или snapshot revision делает ExecutedData stale. пересчёт ExecutedData на новом immutable snapshot. После execution projected ExecutedData завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Исполненная данные» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает ExecutedData stale.
Authoritative replacement: пересчёт ExecutedData на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: ExecutedData нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ExecutedData, тип BOOLEAN_RESULT, class EXECUTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: OBJECT
Creation event: ExecutedData вычисляется из snapshot inputs: lifecycle transition evidence.
Validation event: ExecutedData валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: ExecutedData замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision ExecutedData.
Stale triggers: Market, symbol, config или snapshot revision делает ExecutedData stale.
Replacement source: пересчёт ExecutedData на новом immutable snapshot.
Terminal condition: После execution projected ExecutedData завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: ExecutedData отличается от sibling-терминов источником `lifecycle transition evidence`, классом `EXECUTED` и стадией lifecycle `OBJECT`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `OBJECT`; запись `ExecutedData` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ExecutedData` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### ConfirmedData
CanonicalName: `ConfirmedData`
Русское название: Подтверждённые данные
Краткое определение: ConfirmedData — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `CONFIRMED`. Отличительный объект записи: «Подтверждённые данные»; его authoritative provenance — «lifecycle transition evidence».
Архитектурный профиль: All
Торговая роль: ConfirmedData
Размерность: `BOOLEAN_RESULT`
Unit: `data-state enum`
Знак: not numeric
Допустимый диапазон: соответствует типу `BOOLEAN_RESULT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: CONFIRMED stage для ConfirmedData.
Projected/Actual class: `CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: ConfirmedData вычисляется из snapshot inputs: lifecycle transition evidence. Не мутирует; изменение inputs создаёт новую revision ConfirmedData. Market, symbol, config или snapshot revision делает ConfirmedData stale. пересчёт ConfirmedData на новом immutable snapshot. После execution projected ConfirmedData завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Подтверждённые данные» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает ConfirmedData stale.
Authoritative replacement: пересчёт ConfirmedData на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: ConfirmedData нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ConfirmedData, тип BOOLEAN_RESULT, class CONFIRMED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: OBJECT
Creation event: ConfirmedData вычисляется из snapshot inputs: lifecycle transition evidence.
Validation event: ConfirmedData валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: ConfirmedData замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision ConfirmedData.
Stale triggers: Market, symbol, config или snapshot revision делает ConfirmedData stale.
Replacement source: пересчёт ConfirmedData на новом immutable snapshot.
Terminal condition: После execution projected ConfirmedData завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: ConfirmedData отличается от sibling-терминов источником `lifecycle transition evidence`, классом `CONFIRMED` и стадией lifecycle `OBJECT`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `OBJECT`; запись `ConfirmedData` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ConfirmedData` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### ReconciledData
CanonicalName: `ReconciledData`
Русское название: Сверенный данные
Краткое определение: ReconciledData — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `RECONCILED`. Отличительный объект записи: «Сверенный данные»; его authoritative provenance — «lifecycle transition evidence».
Архитектурный профиль: All
Торговая роль: ReconciledData
Размерность: `BOOLEAN_RESULT`
Unit: `data-state enum`
Знак: not numeric
Допустимый диапазон: соответствует типу `BOOLEAN_RESULT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: RECONCILED stage для ReconciledData.
Projected/Actual class: `RECONCILED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: ReconciledData вычисляется из snapshot inputs: lifecycle transition evidence. Не мутирует; изменение inputs создаёт новую revision ReconciledData. Market, symbol, config или snapshot revision делает ReconciledData stale. пересчёт ReconciledData на новом immutable snapshot. После execution projected ReconciledData завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Сверенный данные» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает ReconciledData stale.
Authoritative replacement: пересчёт ReconciledData на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: ReconciledData нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ReconciledData, тип BOOLEAN_RESULT, class RECONCILED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: OBJECT
Creation event: ReconciledData вычисляется из snapshot inputs: lifecycle transition evidence.
Validation event: ReconciledData валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: ReconciledData замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision ReconciledData.
Stale triggers: Market, symbol, config или snapshot revision делает ReconciledData stale.
Replacement source: пересчёт ReconciledData на новом immutable snapshot.
Terminal condition: После execution projected ReconciledData завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: ReconciledData отличается от sibling-терминов источником `lifecycle transition evidence`, классом `RECONCILED` и стадией lifecycle `OBJECT`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `OBJECT`; запись `ReconciledData` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ReconciledData` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### PersistedData
CanonicalName: `PersistedData`
Русское название: Сохранённые данные
Краткое определение: PersistedData — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `PERSISTED`. Отличительный объект записи: «Сохранённые данные»; его authoritative provenance — «lifecycle transition evidence».
Архитектурный профиль: All
Торговая роль: PersistedData
Размерность: `BOOLEAN_RESULT`
Unit: `data-state enum`
Знак: not numeric
Допустимый диапазон: соответствует типу `BOOLEAN_RESULT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: PERSISTED stage для PersistedData.
Projected/Actual class: `PERSISTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: PersistedData вычисляется из snapshot inputs: lifecycle transition evidence. Не мутирует; изменение inputs создаёт новую revision PersistedData. Market, symbol, config или snapshot revision делает PersistedData stale. пересчёт PersistedData на новом immutable snapshot. После execution projected PersistedData завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Сохранённые данные» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает PersistedData stale.
Authoritative replacement: пересчёт PersistedData на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: PersistedData нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PersistedData, тип BOOLEAN_RESULT, class PERSISTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: OBJECT
Creation event: PersistedData вычисляется из snapshot inputs: lifecycle transition evidence.
Validation event: PersistedData валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: PersistedData замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision PersistedData.
Stale triggers: Market, symbol, config или snapshot revision делает PersistedData stale.
Replacement source: пересчёт PersistedData на новом immutable snapshot.
Terminal condition: После execution projected PersistedData завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: PersistedData отличается от sibling-терминов источником `lifecycle transition evidence`, классом `PERSISTED` и стадией lifecycle `OBJECT`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `OBJECT`; запись `PersistedData` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `PersistedData` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### StaleData
CanonicalName: `StaleData`
Русское название: Устаревший данные
Краткое определение: StaleData — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `STALE`. Отличительный объект записи: «Устаревший данные»; его authoritative provenance — «lifecycle transition evidence».
Архитектурный профиль: All
Торговая роль: StaleData
Размерность: `BOOLEAN_RESULT`
Unit: `data-state enum`
Знак: not numeric
Допустимый диапазон: соответствует типу `BOOLEAN_RESULT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: STALE stage для StaleData.
Projected/Actual class: `STALE`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: StaleData вычисляется из snapshot inputs: lifecycle transition evidence. Не мутирует; изменение inputs создаёт новую revision StaleData. Market, symbol, config или snapshot revision делает StaleData stale. пересчёт StaleData на новом immutable snapshot. После execution projected StaleData завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Устаревший данные» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает StaleData stale.
Authoritative replacement: пересчёт StaleData на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: StaleData нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: StaleData, тип BOOLEAN_RESULT, class STALE.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: OBJECT
Creation event: StaleData вычисляется из snapshot inputs: lifecycle transition evidence.
Validation event: StaleData валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: StaleData замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision StaleData.
Stale triggers: Market, symbol, config или snapshot revision делает StaleData stale.
Replacement source: пересчёт StaleData на новом immutable snapshot.
Terminal condition: После execution projected StaleData завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: StaleData отличается от sibling-терминов источником `lifecycle transition evidence`, классом `STALE` и стадией lifecycle `OBJECT`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `OBJECT`; запись `StaleData` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `StaleData` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### InvalidData
CanonicalName: `InvalidData`
Русское название: Невалидные данные
Краткое определение: InvalidData — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `INVALID`. Отличительный объект записи: «Невалидные данные»; его authoritative provenance — «lifecycle transition evidence».
Архитектурный профиль: All
Торговая роль: InvalidData
Размерность: `BOOLEAN_RESULT`
Unit: `data-state enum`
Знак: not numeric
Допустимый диапазон: соответствует типу `BOOLEAN_RESULT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: INVALID stage для InvalidData.
Projected/Actual class: `INVALID`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: InvalidData вычисляется из snapshot inputs: lifecycle transition evidence. Не мутирует; изменение inputs создаёт новую revision InvalidData. Market, symbol, config или snapshot revision делает InvalidData stale. пересчёт InvalidData на новом immutable snapshot. После execution projected InvalidData завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Невалидные данные» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает InvalidData stale.
Authoritative replacement: пересчёт InvalidData на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: InvalidData нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: InvalidData, тип BOOLEAN_RESULT, class INVALID.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: OBJECT
Creation event: InvalidData вычисляется из snapshot inputs: lifecycle transition evidence.
Validation event: InvalidData валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: InvalidData замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision InvalidData.
Stale triggers: Market, symbol, config или snapshot revision делает InvalidData stale.
Replacement source: пересчёт InvalidData на новом immutable snapshot.
Terminal condition: После execution projected InvalidData завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: InvalidData отличается от sibling-терминов источником `lifecycle transition evidence`, классом `INVALID` и стадией lifecycle `OBJECT`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `OBJECT`; запись `InvalidData` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `InvalidData` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### NotApplicableValue
CanonicalName: `NotApplicableValue`
Русское название: Не применимо стоимость
Краткое определение: NotApplicableValue — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `NOTAPPLICABLEVALUE`. Отличительный объект записи: «Не применимо стоимость»; его authoritative provenance — «lifecycle transition evidence».
Архитектурный профиль: All
Торговая роль: NotApplicableValue
Размерность: `BOOLEAN_RESULT`
Unit: `data-state enum`
Знак: not numeric
Допустимый диапазон: соответствует типу `BOOLEAN_RESULT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: NOTAPPLICABLEVALUE stage для NotApplicableValue.
Projected/Actual class: `NOTAPPLICABLEVALUE`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: NotApplicableValue вычисляется из snapshot inputs: lifecycle transition evidence. Не мутирует; изменение inputs создаёт новую revision NotApplicableValue. Market, symbol, config или snapshot revision делает NotApplicableValue stale. пересчёт NotApplicableValue на новом immutable snapshot. После execution projected NotApplicableValue завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Не применимо стоимость» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает NotApplicableValue stale.
Authoritative replacement: пересчёт NotApplicableValue на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: NotApplicableValue нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: NotApplicableValue, тип BOOLEAN_RESULT, class NOTAPPLICABLEVALUE.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: OBJECT
Creation event: NotApplicableValue вычисляется из snapshot inputs: lifecycle transition evidence.
Validation event: NotApplicableValue валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: NotApplicableValue замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision NotApplicableValue.
Stale triggers: Market, symbol, config или snapshot revision делает NotApplicableValue stale.
Replacement source: пересчёт NotApplicableValue на новом immutable snapshot.
Terminal condition: После execution projected NotApplicableValue завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: NotApplicableValue отличается от sibling-терминов источником `lifecycle transition evidence`, классом `NOTAPPLICABLEVALUE` и стадией lifecycle `OBJECT`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `OBJECT`; запись `NotApplicableValue` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `NotApplicableValue` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### NotCalculatedValue
CanonicalName: `NotCalculatedValue`
Русское название: Не расчётный стоимость
Краткое определение: NotCalculatedValue — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `NOTCALCULATEDVALUE`. Отличительный объект записи: «Не расчётный стоимость»; его authoritative provenance — «lifecycle transition evidence».
Архитектурный профиль: All
Торговая роль: NotCalculatedValue
Размерность: `BOOLEAN_RESULT`
Unit: `data-state enum`
Знак: not numeric
Допустимый диапазон: соответствует типу `BOOLEAN_RESULT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: NOTCALCULATEDVALUE stage для NotCalculatedValue.
Projected/Actual class: `NOTCALCULATEDVALUE`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: NotCalculatedValue вычисляется из snapshot inputs: lifecycle transition evidence. Не мутирует; изменение inputs создаёт новую revision NotCalculatedValue. Market, symbol, config или snapshot revision делает NotCalculatedValue stale. пересчёт NotCalculatedValue на новом immutable snapshot. После execution projected NotCalculatedValue завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Не расчётный стоимость» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает NotCalculatedValue stale.
Authoritative replacement: пересчёт NotCalculatedValue на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: NotCalculatedValue нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: NotCalculatedValue, тип BOOLEAN_RESULT, class NOTCALCULATEDVALUE.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: OBJECT
Creation event: NotCalculatedValue вычисляется из snapshot inputs: lifecycle transition evidence.
Validation event: NotCalculatedValue валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: NotCalculatedValue замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision NotCalculatedValue.
Stale triggers: Market, symbol, config или snapshot revision делает NotCalculatedValue stale.
Replacement source: пересчёт NotCalculatedValue на новом immutable snapshot.
Terminal condition: После execution projected NotCalculatedValue завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: NotCalculatedValue отличается от sibling-терминов источником `lifecycle transition evidence`, классом `NOTCALCULATEDVALUE` и стадией lifecycle `OBJECT`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `OBJECT`; запись `NotCalculatedValue` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `NotCalculatedValue` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### NotAvailableValue
CanonicalName: `NotAvailableValue`
Русское название: Не доступный стоимость
Краткое определение: NotAvailableValue — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `NOTAVAILABLEVALUE`. Отличительный объект записи: «Не доступный стоимость»; его authoritative provenance — «lifecycle transition evidence».
Архитектурный профиль: All
Торговая роль: NotAvailableValue
Размерность: `BOOLEAN_RESULT`
Unit: `data-state enum`
Знак: not numeric
Допустимый диапазон: соответствует типу `BOOLEAN_RESULT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: NOTAVAILABLEVALUE stage для NotAvailableValue.
Projected/Actual class: `NOTAVAILABLEVALUE`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: NotAvailableValue вычисляется из snapshot inputs: lifecycle transition evidence. Не мутирует; изменение inputs создаёт новую revision NotAvailableValue. Market, symbol, config или snapshot revision делает NotAvailableValue stale. пересчёт NotAvailableValue на новом immutable snapshot. После execution projected NotAvailableValue завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Не доступный стоимость» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает NotAvailableValue stale.
Authoritative replacement: пересчёт NotAvailableValue на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: NotAvailableValue нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: NotAvailableValue, тип BOOLEAN_RESULT, class NOTAVAILABLEVALUE.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: OBJECT
Creation event: NotAvailableValue вычисляется из snapshot inputs: lifecycle transition evidence.
Validation event: NotAvailableValue валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: NotAvailableValue замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision NotAvailableValue.
Stale triggers: Market, symbol, config или snapshot revision делает NotAvailableValue stale.
Replacement source: пересчёт NotAvailableValue на новом immutable snapshot.
Terminal condition: После execution projected NotAvailableValue завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: NotAvailableValue отличается от sibling-терминов источником `lifecycle transition evidence`, классом `NOTAVAILABLEVALUE` и стадией lifecycle `OBJECT`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `OBJECT`; запись `NotAvailableValue` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `NotAvailableValue` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### UnknownValue
CanonicalName: `UnknownValue`
Русское название: Неизвестное стоимость
Краткое определение: UnknownValue — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `UNKNOWNVALUE`. Отличительный объект записи: «Неизвестное стоимость»; его authoritative provenance — «lifecycle transition evidence».
Архитектурный профиль: All
Торговая роль: UnknownValue
Размерность: `BOOLEAN_RESULT`
Unit: `data-state enum`
Знак: not numeric
Допустимый диапазон: соответствует типу `BOOLEAN_RESULT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: UNKNOWNVALUE stage для UnknownValue.
Projected/Actual class: `UNKNOWNVALUE`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: UnknownValue вычисляется из snapshot inputs: lifecycle transition evidence. Не мутирует; изменение inputs создаёт новую revision UnknownValue. Market, symbol, config или snapshot revision делает UnknownValue stale. пересчёт UnknownValue на новом immutable snapshot. После execution projected UnknownValue завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «Неизвестное стоимость» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает UnknownValue stale.
Authoritative replacement: пересчёт UnknownValue на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: UnknownValue нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: UnknownValue, тип BOOLEAN_RESULT, class UNKNOWNVALUE.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: OBJECT
Creation event: UnknownValue вычисляется из snapshot inputs: lifecycle transition evidence.
Validation event: UnknownValue валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: UnknownValue замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision UnknownValue.
Stale triggers: Market, symbol, config или snapshot revision делает UnknownValue stale.
Replacement source: пересчёт UnknownValue на новом immutable snapshot.
Terminal condition: После execution projected UnknownValue завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: UnknownValue отличается от sibling-терминов источником `lifecycle transition evidence`, классом `UNKNOWNVALUE` и стадией lifecycle `OBJECT`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `OBJECT`; запись `UnknownValue` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `UnknownValue` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### CurrentBid
CanonicalName: `CurrentBid`
Русское название: текущая цена Bid
Краткое определение: CurrentBid — symbol-bound величина `CurrentBid` типа `PRICE_BID`, получаемая из SymbolInfoDouble(symbol, SYMBOL_BID); она не является money или lot и не использует их tolerance. Отличительный объект записи: «текущая цена Bid»; его authoritative provenance — «SymbolInfoDouble(symbol, SYMBOL_BID)».
Архитектурный профиль: All
Торговая роль: CurrentBid
Размерность: `PRICE_BID`
Unit: `price`
Знак: > 0
Допустимый диапазон: соответствует типу `PRICE_BID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfoDouble(symbol, SYMBOL_BID)
Authoritative source: SymbolInfoDouble(symbol, SYMBOL_BID)
Время фиксации: ACTUAL CURRENT stage для CurrentBid.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `PriceTolerance`
Lifecycle: CurrentBid вычисляется из snapshot inputs: SymbolInfoDouble(symbol, SYMBOL_BID). Не мутирует; изменение inputs создаёт новую revision CurrentBid. Market, symbol, config или snapshot revision делает CurrentBid stale. пересчёт CurrentBid на новом immutable snapshot. После execution projected CurrentBid завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «текущая цена Bid» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает CurrentBid stale.
Authoritative replacement: пересчёт CurrentBid на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `PRICE_BID` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: CurrentBid нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CurrentBid, тип PRICE_BID, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: PRICE_OR_DISTANCE
Lifecycle class: PROJECTED_VALUE
Creation event: CurrentBid вычисляется из snapshot inputs: SymbolInfoDouble(symbol, SYMBOL_BID).
Validation event: CurrentBid валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: CurrentBid замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision CurrentBid.
Stale triggers: Market, symbol, config или snapshot revision делает CurrentBid stale.
Replacement source: пересчёт CurrentBid на новом immutable snapshot.
Terminal condition: После execution projected CurrentBid завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: CurrentBid отличается от sibling-терминов источником `SymbolInfoDouble(symbol, SYMBOL_BID)`, классом `ACTUAL CURRENT` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `CurrentBid` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `CurrentBid` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### CurrentAsk
CanonicalName: `CurrentAsk`
Русское название: текущая цена Ask
Краткое определение: CurrentAsk — symbol-bound величина `CurrentAsk` типа `PRICE_ASK`, получаемая из SymbolInfoDouble(symbol, SYMBOL_ASK); она не является money или lot и не использует их tolerance. Отличительный объект записи: «текущая цена Ask»; его authoritative provenance — «SymbolInfoDouble(symbol, SYMBOL_ASK)».
Архитектурный профиль: All
Торговая роль: CurrentAsk
Размерность: `PRICE_ASK`
Unit: `price`
Знак: > 0
Допустимый диапазон: соответствует типу `PRICE_ASK`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfoDouble(symbol, SYMBOL_ASK)
Authoritative source: SymbolInfoDouble(symbol, SYMBOL_ASK)
Время фиксации: ACTUAL CURRENT stage для CurrentAsk.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `PriceTolerance`
Lifecycle: CurrentAsk вычисляется из snapshot inputs: SymbolInfoDouble(symbol, SYMBOL_ASK). Не мутирует; изменение inputs создаёт новую revision CurrentAsk. Market, symbol, config или snapshot revision делает CurrentAsk stale. пересчёт CurrentAsk на новом immutable snapshot. После execution projected CurrentAsk завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «текущая цена Ask» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает CurrentAsk stale.
Authoritative replacement: пересчёт CurrentAsk на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `PRICE_ASK` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: CurrentAsk нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CurrentAsk, тип PRICE_ASK, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: PRICE_OR_DISTANCE
Lifecycle class: PROJECTED_VALUE
Creation event: CurrentAsk вычисляется из snapshot inputs: SymbolInfoDouble(symbol, SYMBOL_ASK).
Validation event: CurrentAsk валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: CurrentAsk замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision CurrentAsk.
Stale triggers: Market, symbol, config или snapshot revision делает CurrentAsk stale.
Replacement source: пересчёт CurrentAsk на новом immutable snapshot.
Terminal condition: После execution projected CurrentAsk завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: CurrentAsk отличается от sibling-терминов источником `SymbolInfoDouble(symbol, SYMBOL_ASK)`, классом `ACTUAL CURRENT` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `CurrentAsk` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `CurrentAsk` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### ReserveProjected
CanonicalName: `ReserveProjected`
Русское название: прогнозный резерв до подтверждения
Краткое определение: ReserveProjected — денежная величина `Reserve` класса `PROJECTED` со знаком «non-negative»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit. Отличительный объект записи: «прогнозный резерв до подтверждения»; его authoritative provenance — «OrderCalcProfit outputs plus explicit projected allocation model».
Архитектурный профиль: All
Торговая роль: Reserve
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: >= 0
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit outputs plus explicit projected allocation model
Authoritative source: OrderCalcProfit outputs plus explicit projected allocation model
Время фиксации: PROJECTED stage для ReserveProjected.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `MoneyTolerance`
Lifecycle: ReserveProjected вычисляется из snapshot inputs: OrderCalcProfit outputs plus explicit projected allocation model. Не мутирует; изменение inputs создаёт новую revision ReserveProjected. Market, symbol, config или snapshot revision делает ReserveProjected stale. пересчёт ReserveProjected на новом immutable snapshot. После execution projected ReserveProjected завершается и не становится actual присваиванием. Этот lifecycle относится именно к объекту «прогнозный резерв до подтверждения» и его собственному type/source contract.
Условия stale: Market, symbol, config или snapshot revision делает ReserveProjected stale.
Authoritative replacement: пересчёт ReserveProjected на новом immutable snapshot.
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: ReserveProjected нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Reserve, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::projectedReserve
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: MONEY_VALUE
Lifecycle class: PROJECTED_VALUE
Creation event: ReserveProjected вычисляется из snapshot inputs: OrderCalcProfit outputs plus explicit projected allocation model.
Validation event: ReserveProjected валидируется по типу, unit и входному fingerprint.
Freeze/confirmation event: ReserveProjected замораживается только внутри Candidate/ApprovedPlan.
Mutation events: Не мутирует; изменение inputs создаёт новую revision ReserveProjected.
Stale triggers: Market, symbol, config или snapshot revision делает ReserveProjected stale.
Replacement source: пересчёт ReserveProjected на новом immutable snapshot.
Terminal condition: После execution projected ReserveProjected завершается и не становится actual присваиванием.
Persistence behavior: Сохраняется только как plan/audit evidence, не actual ledger.
Restart behavior: После restart пересчитывается либо признаётся stale по fingerprint.
Отличие от: ReserveProjected отличается от sibling-терминов источником `OrderCalcProfit outputs plus explicit projected allocation model`, классом `PROJECTED` и стадией lifecycle `PROJECTED_VALUE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `PROJECTED_VALUE`; запись `ReserveProjected` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ReserveProjected` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### ReserveCoverage
CanonicalName: `ReserveCoverage`
Русское название: отношение доступного резерва к требованию закрытия
Краткое определение: ReserveCoverage — безразмерная величина типа `RATIO` для Reserve; она не интерпретируется как lot, money или percent без явной conversion. Отличительный объект записи: «отношение доступного резерва к требованию закрытия»; его authoritative provenance — «ReserveAvailable divided by FinalCloseRequirement».
Архитектурный профиль: All
Торговая роль: Reserve
Размерность: `RATIO`
Unit: `dimensionless`
Знак: >= 0
Допустимый диапазон: соответствует типу `RATIO`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: ReserveAvailable divided by FinalCloseRequirement
Authoritative source: ReserveAvailable divided by FinalCloseRequirement
Время фиксации: PROJECTED or ACTUAL RATIO stage для ReserveCoverage.
Projected/Actual class: `PROJECTED or ACTUAL RATIO`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: ReserveCoverage загружается из выбранного документального/конфигурационного профиля. Внутри замороженного цикла ReserveCoverage не изменяется; новая ревизия относится к новому plan. Изменение профиля или revision делает прежний ReserveCoverage stale. новое approved значение ReserveCoverage из явно выбранного профиля. Завершается вместе с конфигурационным scope цикла. Этот lifecycle относится именно к объекту «отношение доступного резерва к требованию закрытия» и его собственному type/source contract.
Условия stale: Изменение профиля или revision делает прежний ReserveCoverage stale.
Authoritative replacement: новое approved значение ReserveCoverage из явно выбранного профиля.
Допустимые операции: сравнение и преобразование только по `RATIO` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: ReserveCoverage нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Reserve, тип RATIO, class PROJECTED or ACTUAL RATIO.
Legacy aliases: —
MQL5 mapping: Include/StateMachine.mqh::reserveCoverage
Python mapping: Tools/run_full_parameter_optimization_study.py::reserve_coverage
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: POLICY
Lifecycle class: POLICY
Creation event: ReserveCoverage загружается из выбранного документального/конфигурационного профиля.
Validation event: ReserveCoverage проверяется как POLICY до фиксации цикла.
Freeze/confirmation event: ReserveCoverage замораживается в конфигурации конкретного CycleID.
Mutation events: Внутри замороженного цикла ReserveCoverage не изменяется; новая ревизия относится к новому plan.
Stale triggers: Изменение профиля или revision делает прежний ReserveCoverage stale.
Replacement source: новое approved значение ReserveCoverage из явно выбранного профиля.
Terminal condition: Завершается вместе с конфигурационным scope цикла.
Persistence behavior: Хранится с profile revision и CycleID.
Restart behavior: После restart перечитывается и сверяется с frozen cycle configuration.
Отличие от: ReserveCoverage отличается от sibling-терминов источником `ReserveAvailable divided by FinalCloseRequirement`, классом `PROJECTED or ACTUAL RATIO` и стадией lifecycle `POLICY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `POLICY`; запись `ReserveCoverage` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `ReserveCoverage` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### Symbol
CanonicalName: `Symbol`
Русское название: торговый символ цикла
Краткое определение: Symbol — identity-сущность типа `SYMBOL_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «торговый символ цикла»; его authoritative provenance — «current chart/request symbol and reconciled position symbol».
Архитектурный профиль: All
Торговая роль: Symbol
Размерность: `SYMBOL_ID`
Unit: `string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `SYMBOL_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: current chart/request symbol and reconciled position symbol
Authoritative source: current chart/request symbol and reconciled position symbol
Время фиксации: ACTUAL CONFIRMED stage для Symbol.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: Symbol создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object. Не мутирует; новый объект получает новое identity. Несовпадение scope либо закрытие объекта делает использование Symbol stale. authoritative identity текущего terminal/deal/event object. После завершения объекта остаётся историческим ключом и не переиспользуется. Этот lifecycle относится именно к объекту «торговый символ цикла» и его собственному type/source contract.
Условия stale: Несовпадение scope либо закрытие объекта делает использование Symbol stale.
Authoritative replacement: authoritative identity текущего terminal/deal/event object.
Допустимые операции: сравнение и преобразование только по `SYMBOL_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: Symbol нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Symbol, тип SYMBOL_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::symbol
Python mapping: Tests/HybridSplitBig/test_catchup_route_hardening.py::symbol
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: Symbol создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object.
Validation event: Symbol проверяется точным сравнением и scope filters.
Freeze/confirmation event: После выдачи Symbol неизменяем в пределах своего объекта.
Mutation events: Не мутирует; новый объект получает новое identity.
Stale triggers: Несовпадение scope либо закрытие объекта делает использование Symbol stale.
Replacement source: authoritative identity текущего terminal/deal/event object.
Terminal condition: После завершения объекта остаётся историческим ключом и не переиспользуется.
Persistence behavior: Persisted только вместе с type и cycle scope.
Restart behavior: После restart сверяется с terminal/deal history.
Отличие от: Symbol отличается от sibling-терминов источником `current chart/request symbol and reconciled position symbol`, классом `ACTUAL CONFIRMED` и стадией lifecycle `IDENTITY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `Symbol` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `Symbol` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### MagicNumber
CanonicalName: `MagicNumber`
Русское название: магический номер стратегии
Краткое определение: MagicNumber — identity-сущность типа `MAGIC_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «магический номер стратегии»; его authoritative provenance — «configured MagicNumber verified against position/deal properties».
Архитектурный профиль: All
Торговая роль: MagicNumber
Размерность: `MAGIC_ID`
Unit: `integer identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `MAGIC_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: configured MagicNumber verified against position/deal properties
Authoritative source: configured MagicNumber verified against position/deal properties
Время фиксации: POLICY/ACTUAL CONFIRMED stage для MagicNumber.
Projected/Actual class: `POLICY/ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: MagicNumber создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object. Не мутирует; новый объект получает новое identity. Несовпадение scope либо закрытие объекта делает использование MagicNumber stale. authoritative identity текущего terminal/deal/event object. После завершения объекта остаётся историческим ключом и не переиспользуется. Этот lifecycle относится именно к объекту «магический номер стратегии» и его собственному type/source contract.
Условия stale: Несовпадение scope либо закрытие объекта делает использование MagicNumber stale.
Authoritative replacement: authoritative identity текущего terminal/deal/event object.
Допустимые операции: сравнение и преобразование только по `MAGIC_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: MagicNumber нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: MagicNumber, тип MAGIC_ID, class POLICY/ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::magicNumber
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: MagicNumber создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object.
Validation event: MagicNumber проверяется точным сравнением и scope filters.
Freeze/confirmation event: После выдачи MagicNumber неизменяем в пределах своего объекта.
Mutation events: Не мутирует; новый объект получает новое identity.
Stale triggers: Несовпадение scope либо закрытие объекта делает использование MagicNumber stale.
Replacement source: authoritative identity текущего terminal/deal/event object.
Terminal condition: После завершения объекта остаётся историческим ключом и не переиспользуется.
Persistence behavior: Persisted только вместе с type и cycle scope.
Restart behavior: После restart сверяется с terminal/deal history.
Отличие от: MagicNumber отличается от sibling-терминов источником `configured MagicNumber verified against position/deal properties`, классом `POLICY/ACTUAL CONFIRMED` и стадией lifecycle `IDENTITY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `MagicNumber` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `MagicNumber` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### CycleID
CanonicalName: `CycleID`
Русское название: идентификатор recovery-цикла
Краткое определение: CycleID — Canonical alias spelling идентификатора recovery cycle; семантически совпадает с CycleId и не заменяет position/deal identity. Отличительный объект записи: «идентификатор recovery-цикла»; его authoritative provenance — «persisted cycle creation event confirmed by reconciliation».
Архитектурный профиль: All
Торговая роль: CycleID
Размерность: `CYCLE_ID`
Unit: `integer identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `CYCLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: persisted cycle creation event confirmed by reconciliation
Authoritative source: persisted cycle creation event confirmed by reconciliation
Время фиксации: ACTUAL CONFIRMED stage для CycleID.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: CycleID создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object. Не мутирует; новый объект получает новое identity. Несовпадение scope либо закрытие объекта делает использование CycleID stale. authoritative identity текущего terminal/deal/event object. После завершения объекта остаётся историческим ключом и не переиспользуется. Этот lifecycle относится именно к объекту «идентификатор recovery-цикла» и его собственному type/source contract.
Условия stale: Несовпадение scope либо закрытие объекта делает использование CycleID stale.
Authoritative replacement: authoritative identity текущего terminal/deal/event object.
Допустимые операции: сравнение и преобразование только по `CYCLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: CycleID нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CycleID, тип CYCLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::cycleId
Python mapping: Tests/HybridSplitBig/test_catchup_route_hardening.py::cycle
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: CycleID создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object.
Validation event: CycleID проверяется точным сравнением и scope filters.
Freeze/confirmation event: После выдачи CycleID неизменяем в пределах своего объекта.
Mutation events: Не мутирует; новый объект получает новое identity.
Stale triggers: Несовпадение scope либо закрытие объекта делает использование CycleID stale.
Replacement source: authoritative identity текущего terminal/deal/event object.
Terminal condition: После завершения объекта остаётся историческим ключом и не переиспользуется.
Persistence behavior: Persisted только вместе с type и cycle scope.
Restart behavior: После restart сверяется с terminal/deal history.
Отличие от: CycleID отличается от sibling-терминов источником `persisted cycle creation event confirmed by reconciliation`, классом `ACTUAL CONFIRMED` и стадией lifecycle `IDENTITY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `CycleID` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `CycleID` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### EventID
CanonicalName: `EventID`
Русское название: идентификатор ledger-события
Краткое определение: EventID — identity-сущность типа `EVENT_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «идентификатор ledger-события»; его authoritative provenance — «exactly-once ledger event namespace».
Архитектурный профиль: All
Торговая роль: EventID
Размерность: `EVENT_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `EVENT_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: exactly-once ledger event namespace
Authoritative source: exactly-once ledger event namespace
Время фиксации: ACTUAL CONFIRMED stage для EventID.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: EventID создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object. Не мутирует; новый объект получает новое identity. Несовпадение scope либо закрытие объекта делает использование EventID stale. authoritative identity текущего terminal/deal/event object. После завершения объекта остаётся историческим ключом и не переиспользуется. Этот lifecycle относится именно к объекту «идентификатор ledger-события» и его собственному type/source contract.
Условия stale: Несовпадение scope либо закрытие объекта делает использование EventID stale.
Authoritative replacement: authoritative identity текущего terminal/deal/event object.
Допустимые операции: сравнение и преобразование только по `EVENT_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: EventID нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: EventID, тип EVENT_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/StateMachine.mqh::lastEventId
Python mapping: Tests/unit/test_split_final_safety_model.py::event_id
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: EventID создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object.
Validation event: EventID проверяется точным сравнением и scope filters.
Freeze/confirmation event: После выдачи EventID неизменяем в пределах своего объекта.
Mutation events: Не мутирует; новый объект получает новое identity.
Stale triggers: Несовпадение scope либо закрытие объекта делает использование EventID stale.
Replacement source: authoritative identity текущего terminal/deal/event object.
Terminal condition: После завершения объекта остаётся историческим ключом и не переиспользуется.
Persistence behavior: Persisted только вместе с type и cycle scope.
Restart behavior: После restart сверяется с terminal/deal history.
Отличие от: EventID отличается от sibling-терминов источником `exactly-once ledger event namespace`, классом `ACTUAL CONFIRMED` и стадией lifecycle `IDENTITY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `EventID` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `EventID` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=PARTIAL_MATCH.

### Fingerprint
CanonicalName: `Fingerprint`
Русское название: типизированный отпечаток snapshot или plan
Краткое определение: Fingerprint — identity-сущность типа `FINGERPRINT` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind. Отличительный объект записи: «типизированный отпечаток snapshot или plan»; его authoritative provenance — «canonical serialization of typed fields and revision».
Архитектурный профиль: All
Торговая роль: Fingerprint
Размерность: `FINGERPRINT`
Unit: `hash identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `FINGERPRINT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: canonical serialization of typed fields and revision
Authoritative source: canonical serialization of typed fields and revision
Время фиксации: PROJECTED or RECONCILED stage для Fingerprint.
Projected/Actual class: `PROJECTED or RECONCILED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT HASH MATCH`
Lifecycle: Fingerprint создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object. Не мутирует; новый объект получает новое identity. Несовпадение scope либо закрытие объекта делает использование Fingerprint stale. authoritative identity текущего terminal/deal/event object. После завершения объекта остаётся историческим ключом и не переиспользуется. Этот lifecycle относится именно к объекту «типизированный отпечаток snapshot или plan» и его собственному type/source contract.
Условия stale: Несовпадение scope либо закрытие объекта делает использование Fingerprint stale.
Authoritative replacement: authoritative identity текущего terminal/deal/event object.
Допустимые операции: сравнение и преобразование только по `FINGERPRINT` с `EXACT HASH MATCH` и explicit provenance.
Запрещённые подмены: Fingerprint нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Fingerprint, тип FINGERPRINT, class PROJECTED or RECONCILED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: Tests/HybridSplitBig/test_catchup_dimension_safe.py::fingerprint
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: IDENTITY
Lifecycle class: IDENTITY
Creation event: Fingerprint создаётся владельцем identity при создании соответствующего symbol/cycle/order/deal/event object.
Validation event: Fingerprint проверяется точным сравнением и scope filters.
Freeze/confirmation event: После выдачи Fingerprint неизменяем в пределах своего объекта.
Mutation events: Не мутирует; новый объект получает новое identity.
Stale triggers: Несовпадение scope либо закрытие объекта делает использование Fingerprint stale.
Replacement source: authoritative identity текущего terminal/deal/event object.
Terminal condition: После завершения объекта остаётся историческим ключом и не переиспользуется.
Persistence behavior: Persisted только вместе с type и cycle scope.
Restart behavior: После restart сверяется с terminal/deal history.
Отличие от: Fingerprint отличается от sibling-терминов источником `canonical serialization of typed fields and revision`, классом `PROJECTED or RECONCILED` и стадией lifecycle `IDENTITY`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `IDENTITY`; запись `Fingerprint` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `Fingerprint` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=PARTIAL_MATCH.

### Comment
CanonicalName: `Comment`
Русское название: комментарий торгового объекта
Краткое определение: Comment — самостоятельная нормативная сущность `DIAGNOSTIC_TEXT`: её значение возникает из `MT5 position/order/deal comment property` и отличается от связанных терминов lifecycle class `ACTUAL OBSERVATION`. Отличительный объект записи: «комментарий торгового объекта»; его authoritative provenance — «MT5 position/order/deal comment property».
Архитектурный профиль: All
Торговая роль: Comment
Размерность: `DIAGNOSTIC_TEXT`
Unit: `text`
Знак: not numeric
Допустимый диапазон: соответствует типу `DIAGNOSTIC_TEXT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 position/order/deal comment property
Authoritative source: MT5 position/order/deal comment property
Время фиксации: ACTUAL OBSERVATION stage для Comment.
Projected/Actual class: `ACTUAL OBSERVATION`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT TEXT; never identity`
Lifecycle: Comment создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение Comment историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «комментарий торгового объекта» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение Comment историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `DIAGNOSTIC_TEXT` с `EXACT TEXT; never identity` и explicit provenance.
Запрещённые подмены: Comment нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Comment, тип DIAGNOSTIC_TEXT, class ACTUAL OBSERVATION.
Legacy aliases: —
MQL5 mapping: Include/SimulationEngine.mqh::comment
Python mapping: NONE_FOUND
Mapping status: MQL5=`PARTIAL_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: Comment создаётся соответствующим transition, gate или observation event.
Validation event: Comment проверяется точным enum/schema сравнением.
Freeze/confirmation event: Comment фиксируется вместе с CycleID и EventID.
Mutation events: Изменяется только явно разрешённым событием своего класса.
Stale triggers: Новая state revision делает прежнее current значение Comment историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: Comment отличается от sibling-терминов источником `MT5 position/order/deal comment property`, классом `ACTUAL OBSERVATION` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `Comment` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `Comment` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=PARTIAL_MATCH, Python=MISSING.

### Preview
CanonicalName: `Preview`
Русское название: read-only предварительная оценка
Краткое определение: Preview — typed `PHASE` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «read-only предварительная оценка»; его authoritative provenance — «fresh immutable snapshot evaluator».
Архитектурный профиль: All
Торговая роль: Preview
Размерность: `PREVIEW_OBJECT`
Unit: `structured preview`
Знак: not numeric
Допустимый диапазон: соответствует типу `PHASE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: fresh immutable snapshot evaluator
Authoritative source: fresh immutable snapshot evaluator
Время фиксации: PROJECTED stage для Preview.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT STRUCTURE`
Lifecycle: Preview создаётся из immutable snapshot; stale при input revision; заменяется пересчётом и никогда не становится actual присваиванием.
Условия stale: Новая state revision делает прежнее current значение Preview историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `PHASE` с `EXACT STRUCTURE` и explicit provenance.
Запрещённые подмены: Preview нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Preview, тип PHASE, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: PROJECTED_VALUE
Creation event: Preview создаётся из immutable calculation snapshot.
Validation event: Preview проверяется точным enum/schema сравнением.
Freeze/confirmation event: Preview фиксируется вместе с CycleID и EventID.
Mutation events: Не мутирует; новая revision создаёт новый object.
Stale triggers: input or snapshot revision делает object stale.
Replacement source: пересчёт на новом immutable snapshot.
Terminal condition: завершается перед execution либо freeze approved plan.
Persistence behavior: plan/audit evidence, не actual ledger commit.
Restart behavior: после restart сверяется fingerprint и пересчитывается.
Отличие от: Preview отличается от sibling-терминов источником `fresh immutable snapshot evaluator`, классом `PROJECTED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `Preview` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `Preview` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### Candidate
CanonicalName: `Candidate`
Русское название: кандидат плана до полного gate-chain
Краткое определение: Candidate — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces. Отличительный объект записи: «кандидат плана до полного gate-chain»; его authoritative provenance — «solver output tied to source fingerprint».
Архитектурный профиль: All
Торговая роль: Candidate
Размерность: `OUTCOME`
Unit: `structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `OUTCOME`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: solver output tied to source fingerprint
Authoritative source: solver output tied to source fingerprint
Время фиксации: PROJECTED stage для Candidate.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT STRUCTURE`
Lifecycle: Candidate создаётся соответствующим transition, gate или observation event. Изменяется только явно разрешённым событием своего класса. Новая state revision делает прежнее current значение Candidate историческим. последнее confirmed state/event значение того же класса. Terminal outcome завершает current lifecycle, сохраняя audit. Этот lifecycle относится именно к объекту «кандидат плана до полного gate-chain» и его собственному type/source contract.
Условия stale: Новая state revision делает прежнее current значение Candidate историческим.
Authoritative replacement: последнее confirmed state/event значение того же класса.
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT STRUCTURE` и explicit provenance.
Запрещённые подмены: Candidate нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Candidate, тип OUTCOME, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STATE_OR_RESULT
Lifecycle class: STATE
Creation event: Candidate создаётся соответствующим transition, gate или observation event.
Validation event: Candidate проверяется точным enum/schema сравнением.
Freeze/confirmation event: Candidate фиксируется вместе с CycleID и EventID.
Mutation events: Изменяется только явно разрешённым событием своего класса.
Stale triggers: Новая state revision делает прежнее current значение Candidate историческим.
Replacement source: последнее confirmed state/event значение того же класса.
Terminal condition: Terminal outcome завершает current lifecycle, сохраняя audit.
Persistence behavior: Persisted с event identity, если требуется recovery.
Restart behavior: После restart восстанавливается replay/reconciliation, не diagnostic text.
Отличие от: Candidate отличается от sibling-терминов источником `solver output tied to source fingerprint`, классом `PROJECTED` и стадией lifecycle `STATE`.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие обязательные clauses допустимы только внутри lifecycle class `STATE`; запись `Candidate` различается canonical source, type/class и полем «Отличие от».
Evidence: mapping record `Candidate` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

### Plan
CanonicalName: `Plan`
Русское название: расчётный набор действий и ожиданий
Краткое определение: Plan — structured projected набор рассчитанных действий и ожиданий, связанный с immutable snapshot revision; это не runtime State, Preview, request или execution evidence.
Архитектурный профиль: All
Торговая роль: Plan
Размерность: `PLAN_OBJECT`
Unit: `structured plan`
Знак: not numeric
Допустимый диапазон: валидная PLAN_OBJECT schema с CycleID, snapshot revision и typed actions; несогласованный fingerprint означает INVALID.
Источник возникновения: candidate planner output with revision
Authoritative source: candidate planner output with revision
Время фиксации: PROJECTED stage для Plan.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT STRUCTURE`
Lifecycle: Plan создаётся из immutable snapshot; stale при input revision; заменяется пересчётом и никогда не становится actual присваиванием.
Условия stale: input, market, symbol-property или snapshot revision делает Plan stale.
Authoritative replacement: новый validated Plan, рассчитанный на новом immutable snapshot.
Допустимые операции: schema validation, fingerprint comparison и immutable derivation в ApprovedPlan.
Запрещённые подмены: Plan нельзя подменять Preview, runtime State, ExecutionRequest или broker result.
Связанные сущности: Candidate, PlanFingerprint и ApprovedPlan; тип PLAN_OBJECT, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: Tests/adaptive_geometry_docs_check.py::plan
Mapping status: MQL5=`MISSING`; Python=`PARTIAL_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: PROJECTED_VALUE
Creation event: Plan создаётся из immutable calculation snapshot.
Validation event: Plan проверяется по PLAN_OBJECT schema, dimensions, cycle scope и SnapshotFingerprint.
Freeze/confirmation event: Validated Plan становится отдельным immutable ApprovedPlan только после всех обязательных gates.
Mutation events: Не мутирует; новая revision создаёт новый object.
Stale triggers: input or snapshot revision делает object stale.
Replacement source: пересчёт на новом immutable snapshot.
Terminal condition: завершается перед execution либо freeze approved plan.
Persistence behavior: plan/audit evidence, не actual ledger commit.
Restart behavior: после restart сверяется fingerprint и пересчитывается.
Отличие от: Plan отличается от Preview наличием candidate actions, а от ApprovedPlan отсутствием approval freeze.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие lifecycle clauses projected plan разделяются с HybridPlan; Plan отличается architecture-neutral type и source contract.
Evidence: mapping record `Plan` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=PARTIAL_MATCH.

### ApprovedPlan
CanonicalName: `ApprovedPlan`
Русское название: неизменяемый план после всех обязательных gates
Краткое определение: ApprovedPlan — immutable structured Plan после всех обязательных gates, связанный с PlanFingerprint; это не runtime State, request acceptance или execution success.
Архитектурный профиль: All
Торговая роль: ApprovedPlan
Размерность: `PLAN_OBJECT`
Unit: `structured approved plan`
Знак: not numeric
Допустимый диапазон: валидная PLAN_OBJECT schema с passed gates, CycleID, SnapshotFingerprint и PlanFingerprint; mutation после freeze запрещена.
Источник возникновения: approved immutable plan and fingerprint
Authoritative source: approved immutable plan and fingerprint
Время фиксации: PROJECTED APPROVED stage для ApprovedPlan.
Projected/Actual class: `PROJECTED APPROVED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT STRUCTURE`
Lifecycle: ApprovedPlan создаётся из immutable snapshot; stale при input revision; заменяется пересчётом и никогда не становится actual присваиванием.
Условия stale: изменение snapshot/config/market revision либо fingerprint mismatch запрещает исполнение ApprovedPlan.
Authoritative replacement: новый ApprovedPlan, полученный повторным calculation, validation и approval на новой revision.
Допустимые операции: exact fingerprint verification, immutable request derivation и audit comparison.
Запрещённые подмены: ApprovedPlan нельзя подменять mutable Candidate, runtime State, request acceptance или ExecutionResult.
Связанные сущности: Plan, PlanFingerprint и ExecutionRequest; тип PLAN_OBJECT, class PROJECTED APPROVED.
Legacy aliases: —
MQL5 mapping: NONE_FOUND
Python mapping: NONE_FOUND
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Semantic category: STRUCTURED_OBJECT
Lifecycle class: PROJECTED_VALUE
Creation event: ApprovedPlan создаётся из immutable calculation snapshot.
Validation event: ApprovedPlan повторно проверяется по fingerprint, gate evidence, cycle scope и execution preconditions.
Freeze/confirmation event: После approval объект immutable; broker request создаётся отдельно и не изменяет ApprovedPlan.
Mutation events: Не мутирует; новая revision создаёт новый object.
Stale triggers: input or snapshot revision делает object stale.
Replacement source: пересчёт на новом immutable snapshot.
Terminal condition: завершается перед execution либо freeze approved plan.
Persistence behavior: plan/audit evidence, не actual ledger commit.
Restart behavior: после restart сверяется fingerprint и пересчитывается.
Отличие от: ApprovedPlan отличается от Plan подтверждёнными gates и immutable freeze, а от ExecutionRequest отсутствием broker submission.
Semantic exception: NOT_APPLICABLE
Similarity exception reason: Общие lifecycle clauses разделяются с Plan; ApprovedPlan отличается source gate evidence, approved type и immutable fingerprint freeze.
Evidence: mapping record `ApprovedPlan` contains generated/found/accepted/rejected candidates, scores, declarations and use sites; final MQL5=MISSING, Python=MISSING.

