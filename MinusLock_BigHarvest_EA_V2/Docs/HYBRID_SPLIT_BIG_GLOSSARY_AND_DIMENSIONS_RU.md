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
| BigGross | Компенсирующая позиция валовая | BigGross | ROLE_ID | integer/string identity | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| SmallBase | Защитная позиция базовая | SmallBase | ROLE_ID | integer/string identity | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT | Small | APPROVED_TERM |
| Hybrid | Гибридный | Hybrid | STATE | enum/structured record | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | DOCUMENTED_NOT_APPROVED |
| HybridSplitBig | Гибридный разделённый компенсирующая позиция | HybridSplitBig | STATE | enum/structured record | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| HybridMode | Гибридный режим | Hybrid | STATE | enum/structured record | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| HybridPlan | Гибридный план | HybridPlan | STATE | enum/structured record | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| HybridPreview | Гибридный preview | HybridPreview | STATE | enum/structured record | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| HybridExecution | Гибридный исполнение | HybridExecution | STATE | enum/structured record | not numeric | POLICY | explicit mode discriminator + plan role | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| InitialBuy | Начальная покупка | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| InitialSell | Начальная продажа | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| InitialProfitLeg | Начальная прибыль leg | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| InitialLosingLeg | Начальная убыточная leg | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| InitialIgnoredProfit | Начальная исключённая прибыль | Role-qualified architecture | MONEY_REALIZED | account money | signed confirmed result; excluded from recovery money | ACTUAL CONFIRMED | confirmed closing deal aggregation of InitialProfitLeg filtered by Symbol+Magic+CycleID+position identity | ROUND_TO_MONEY_DIGITS at ledger/report boundary | MoneyTolerance | — | APPROVED_TERM |
| OldFar | Предыдущая хвостовая позиция | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| CurrentFar | Текущая хвостовая позиция | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | Far | APPROVED_TERM |
| ResidualFar | Остаточная хвостовая позиция | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| NewFar | Новая хвостовая позиция | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| LegacyBigPosition | Устаревшая архитектура компенсирующая позиция позиция | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| BigCorePosition | Компенсирующая позиция основная часть позиция | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| BigTrendPosition | Компенсирующая позиция трендовая часть позиция | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| LegacySmallPosition | Устаревшая архитектура защитная позиция позиция | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| SmallBasePosition | Защитная позиция базовая позиция | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| ManagedPosition | Управляемая позиция | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| UnmanagedPosition | Неуправляемая позиция | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| ForeignCyclePosition | Чужая цикл позиция | Role-qualified architecture | ROLE_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| FarDirection | Хвостовая позиция направление | Role-qualified architecture | DIRECTION_ENUM | BUY/SELL enum | not numeric | ACTUAL CONFIRMED or POLICY DERIVED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| OppositeFarDirection | Противоположное хвостовая позиция направление | Role-qualified architecture | DIRECTION_ENUM | BUY/SELL enum | not numeric | ACTUAL CONFIRMED or POLICY DERIVED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| SameAsFarDirection | Совпадающее с хвостовая позиция направление | Role-qualified architecture | DIRECTION_ENUM | BUY/SELL enum | not numeric | ACTUAL CONFIRMED or POLICY DERIVED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| BigDirection | Компенсирующая позиция направление | Role-qualified architecture | DIRECTION_ENUM | BUY/SELL enum | not numeric | ACTUAL CONFIRMED or POLICY DERIVED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| SmallDirection | Защитная позиция направление | Role-qualified architecture | DIRECTION_ENUM | BUY/SELL enum | not numeric | ACTUAL CONFIRMED or POLICY DERIVED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| TrendDirection | Трендовая часть направление | Role-qualified architecture | DIRECTION_ENUM | BUY/SELL enum | not numeric | ACTUAL CONFIRMED or POLICY DERIVED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| ReverseDirection | Разворот направление | Role-qualified architecture | DIRECTION_ENUM | BUY/SELL enum | not numeric | ACTUAL CONFIRMED or POLICY DERIVED | reconciled MT5 position identity and role mapping | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| RawLot | Сырой объём в лотах | Legacy/Split/Hybrid, role-qualified | LOT_RAW | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| CalculatedLot | Расчётный объём в лотах | Legacy/Split/Hybrid, role-qualified | LOT_CALCULATED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| NormalizedLot | Нормализованный объём в лотах | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| RequestedLot | Запрошенный объём в лотах | Legacy/Split/Hybrid, role-qualified | LOT_REQUESTED | lot | >=0; active position >0 | REQUESTED | approved immutable plan | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| FilledLot | Исполненный объём в лотах | Legacy/Split/Hybrid, role-qualified | LOT_FILLED | lot | >=0; active position >0 | CONFIRMED | confirmed deals/trade result | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| ActualPositionLot | Фактический позиция объём в лотах | Legacy/Split/Hybrid, role-qualified | LOT_POSITION_ACTUAL | lot | >=0; active position >0 | ACTUAL CURRENT | current MT5 position snapshot | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| ResidualLotProjected | Остаточная объём в лотах прогнозный | Legacy/Split/Hybrid, role-qualified | LOT_RESIDUAL | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| ResidualLotActual | Остаточная объём в лотах фактический | Legacy/Split/Hybrid, role-qualified | LOT_POSITION_ACTUAL | lot | >=0; active position >0 | ACTUAL CURRENT | current MT5 position snapshot | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| FarLotRaw | Хвостовая позиция объём в лотах сырой | Legacy/Split/Hybrid, role-qualified | LOT_RAW | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| FarLotCalculated | Хвостовая позиция объём в лотах расчётный | Legacy/Split/Hybrid, role-qualified | LOT_CALCULATED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| FarLotNormalized | Хвостовая позиция объём в лотах нормализованный | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| FarLotRequested | Хвостовая позиция объём в лотах запрошенный | Legacy/Split/Hybrid, role-qualified | LOT_REQUESTED | lot | >=0; active position >0 | REQUESTED | approved immutable plan | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| FarLotFilled | Хвостовая позиция объём в лотах исполненный | Legacy/Split/Hybrid, role-qualified | LOT_FILLED | lot | >=0; active position >0 | CONFIRMED | confirmed deals/trade result | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| FarLotActual | Хвостовая позиция объём в лотах фактический | Legacy/Split/Hybrid, role-qualified | LOT_POSITION_ACTUAL | lot | >=0; active position >0 | ACTUAL CURRENT | current MT5 position snapshot | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | FarLot, Ctx.farLot | APPROVED_TERM |
| BigCoreLotRaw | Компенсирующая позиция основная часть объём в лотах сырой | Legacy/Split/Hybrid, role-qualified | LOT_RAW | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| BigCoreLotNormalized | Компенсирующая позиция основная часть объём в лотах нормализованный | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| BigCoreLotRequested | Компенсирующая позиция основная часть объём в лотах запрошенный | Legacy/Split/Hybrid, role-qualified | LOT_REQUESTED | lot | >=0; active position >0 | REQUESTED | approved immutable plan | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| BigCoreLotFilled | Компенсирующая позиция основная часть объём в лотах исполненный | Legacy/Split/Hybrid, role-qualified | LOT_FILLED | lot | >=0; active position >0 | CONFIRMED | confirmed deals/trade result | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| BigCoreLotActual | Компенсирующая позиция основная часть объём в лотах фактический | Legacy/Split/Hybrid, role-qualified | LOT_POSITION_ACTUAL | lot | >=0; active position >0 | ACTUAL CURRENT | current MT5 position snapshot | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| BigTrendLotRaw | Компенсирующая позиция трендовая часть объём в лотах сырой | Legacy/Split/Hybrid, role-qualified | LOT_RAW | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| BigTrendLotNormalized | Компенсирующая позиция трендовая часть объём в лотах нормализованный | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| SmallBaseLotRaw | Защитная позиция базовая объём в лотах сырой | Legacy/Split/Hybrid, role-qualified | LOT_RAW | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| SmallBaseLotNormalized | Защитная позиция базовая объём в лотах нормализованный | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| PartialFarCloseLotCalculated | Частичный хвостовая позиция закрытие объём в лотах расчётный | Legacy/Split/Hybrid, role-qualified | LOT_CALCULATED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| PartialFarCloseLotNormalized | Частичный хвостовая позиция закрытие объём в лотах нормализованный | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| PartialFarCloseLotRequested | Частичный хвостовая позиция закрытие объём в лотах запрошенный | Legacy/Split/Hybrid, role-qualified | LOT_REQUESTED | lot | >=0; active position >0 | REQUESTED | approved immutable plan | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| PartialFarCloseLotFilled | Частичный хвостовая позиция закрытие объём в лотах исполненный | Legacy/Split/Hybrid, role-qualified | LOT_FILLED | lot | >=0; active position >0 | CONFIRMED | confirmed deals/trade result | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| FarResidualProjected | Хвостовая позиция остаточная прогнозный | Legacy/Split/Hybrid, role-qualified | LOT_RESIDUAL | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | APPROVED_TERM |
| FarResidualActual | Хвостовая позиция остаточная фактический | Legacy/Split/Hybrid, role-qualified | LOT_POSITION_ACTUAL | lot | >=0; active position >0 | ACTUAL CURRENT | current MT5 position snapshot | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | APPROVED_TERM |
| NewFarCandidateLot | Новая хвостовая позиция кандидат объём в лотах | Legacy/Split/Hybrid, role-qualified | LOT_CALCULATED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | UNRESOLVED_MODE_ROUTING |
| NewFarProjectedLot | Новая хвостовая позиция прогнозный объём в лотах | Legacy/Split/Hybrid, role-qualified | LOT_RAW | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | UNRESOLVED_MODE_ROUTING |
| NewFarNormalizedLot | Новая хвостовая позиция нормализованный объём в лотах | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | UNRESOLVED_MODE_ROUTING |
| NewFarPromotedLot | Новая хвостовая позиция назначенный объём в лотах | Legacy/Split/Hybrid, role-qualified | LOT_NORMALIZED | lot | >=0; active position >0 | PROJECTED | typed formula + SymbolInfo volume constraints | profile-specific lot normalization | VolumeToleranceLots | — | UNRESOLVED_MODE_ROUTING |
| NewFarActualLot | Новая хвостовая позиция фактический объём в лотах | Legacy/Split/Hybrid, role-qualified | LOT_POSITION_ACTUAL | lot | >=0; active position >0 | ACTUAL CURRENT | current MT5 position snapshot | NO_ADDITIONAL_ROUNDING | VolumeToleranceLots | — | UNRESOLVED_MODE_ROUTING |
| Point | Размер пункта | All profiles; Symbol-bound | PRICE_POINT_SIZE | price per point | strictly positive symbol property | SYMBOL PROPERTY | SymbolInfoDouble(symbol, SYMBOL_POINT) | NO_ADDITIONAL_ROUNDING | EXACT PROPERTY SNAPSHOT | — | APPROVED_TERM |
| TickSize | Тик размер | All profiles; Symbol-bound | PRICE_TICK_SIZE | price per tick | strictly positive symbol property | SYMBOL PROPERTY | SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE) | NO_ADDITIONAL_ROUNDING | EXACT PROPERTY SNAPSHOT | — | APPROVED_TERM |
| TickValue | Тик стоимость | All profiles; Symbol-bound | PRICE_PROJECTED | price | >0 for absolute price; delta signed | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| MarketBidPrice | Рыночная Bid цена | All profiles; Symbol-bound | PRICE_BID | price | strictly positive | ACTUAL CURRENT | SymbolInfoDouble(symbol, SYMBOL_BID) | NO_ADDITIONAL_ROUNDING | PriceTolerance | — | APPROVED_TERM |
| MarketAskPrice | Рыночная Ask цена | All profiles; Symbol-bound | PRICE_ASK | price | strictly positive | ACTUAL CURRENT | SymbolInfoDouble(symbol, SYMBOL_ASK) | NO_ADDITIONAL_ROUNDING | PriceTolerance | — | APPROVED_TERM |
| PositionOpenPrice | Позиция открытие цена | All profiles; Symbol-bound | PRICE_OPEN | price | >0 for absolute price; delta signed | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| TriggerPrice | Триггер цена | All profiles; Symbol-bound | PRICE_PROJECTED | price | >0 for absolute price; delta signed | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| TargetPrice | Целевая цена | All profiles; Symbol-bound | PRICE_PROJECTED | price | >0 for absolute price; delta signed | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| ControlPrice | Контрольная цена | All profiles; Symbol-bound | PRICE_PROJECTED | price | >0 for absolute price; delta signed | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| ProjectedExitPrice | Прогнозный выход цена | All profiles; Symbol-bound | PRICE_PROJECTED | price | >0 for absolute price; delta signed | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| ExecutedDealPrice | Исполненная сделка цена | All profiles; Symbol-bound | PRICE_EXECUTED | price | >0 for absolute price; delta signed | CONFIRMED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| PriceDelta | Цена дельта | All profiles; Symbol-bound | PRICE_DELTA | price | signed price difference | PROJECTED | difference of two explicitly named prices | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| DistancePoints | Расстояние пункты | All profiles; Symbol-bound | DISTANCE_POINTS | points | non-negative distance | PROJECTED or ACTUAL MEASUREMENT | explicit price delta divided by SYMBOL_POINT | NO_ADDITIONAL_ROUNDING | PointTolerance | — | APPROVED_TERM |
| DistanceTicks | Расстояние тики | All profiles; Symbol-bound | DISTANCE_TICKS | ticks | non-negative distance | PROJECTED or ACTUAL MEASUREMENT | explicit price delta divided by SYMBOL_TRADE_TICK_SIZE | NO_ADDITIONAL_ROUNDING | PointTolerance | — | APPROVED_TERM |
| BidAwareClosePrice | Bid учитывающая сторону рынка закрытие цена | All profiles; Symbol-bound | PRICE_BID | price | >0 for absolute price; delta signed | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| AskAwareClosePrice | Ask учитывающая сторону рынка закрытие цена | All profiles; Symbol-bound | PRICE_ASK | price | >0 for absolute price; delta signed | PROJECTED | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| FarOpenPriceActual | Хвостовая позиция открытие цена фактический | All profiles; Symbol-bound | PRICE_OPEN | price | >0 for absolute price; delta signed | ACTUAL CURRENT | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| BigCoreOpenPriceActual | Компенсирующая позиция основная часть открытие цена фактический | All profiles; Symbol-bound | PRICE_OPEN | price | >0 for absolute price; delta signed | ACTUAL CURRENT | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| BigTrendOpenPriceActual | Компенсирующая позиция трендовая часть открытие цена фактический | All profiles; Symbol-bound | PRICE_OPEN | price | >0 for absolute price; delta signed | ACTUAL CURRENT | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| SmallBaseOpenPriceActual | Защитная позиция базовая открытие цена фактический | All profiles; Symbol-bound | PRICE_OPEN | price | >0 for absolute price; delta signed | ACTUAL CURRENT | SymbolInfo tick/current position/deal properties | ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual | PriceTolerance | — | APPROVED_TERM |
| GrossProfit | Валовая прибыль | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed P/L | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| GrossLoss | Валовая убыток | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| NetProfit | Чистый результат прибыль | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed P/L | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| LegNet | Leg чистый результат | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed P/L | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| BasketNet | Корзина чистый результат | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed P/L | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| HarvestGross | Сбор прибыли валовая | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| HarvestNet | Сбор прибыли чистый результат | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed P/L | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| SmallReverseNet | Защитная позиция разворот чистый результат | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed P/L | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | UNRESOLVED_BUSINESS_POLICY |
| TransitionNet | Переход чистый результат | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed P/L | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| RealizedCyclePL | Реализованный цикл pl | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed P/L | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| FloatingManagedPL | Плавающий управляемая pl | Cycle/account as explicitly qualified | MONEY_FLOATING | account money | signed P/L | ACTUAL CURRENT | current position or broker-aware price model | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| ProjectedFloatingPL | Прогнозный плавающий pl | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | signed P/L | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| RecoveryPLAnalytic | Восстановление pl аналитический | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | signed P/L | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| RecoveryPLProjected | Восстановление pl прогнозный | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | signed P/L | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| RecoveryPLCloseNow | Восстановление pl закрытие сейчас | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | signed P/L | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| RealRecoveryPL | Подтверждённый восстановление pl | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed P/L | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | realRecoveryPL | APPROVED_TERM |
| RecoverySlope | Восстановление наклон | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | signed P/L | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| RecoveryMonotonicity | Восстановление монотонность | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | non-negative magnitude/bucket | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| ExpectedExitCosts | Ожидаемые выход расходы | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | non-negative magnitude/bucket | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| CommissionCost | Комиссия cost | Cycle/account as explicitly qualified | MONEY_COST | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| SwapCost | Своп cost | Cycle/account as explicitly qualified | MONEY_COST | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| FeeCost | Сбор cost | Cycle/account as explicitly qualified | MONEY_COST | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| SpreadCost | Спред cost | Cycle/account as explicitly qualified | MONEY_COST | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| SlippageCost | Проскальзывание cost | Cycle/account as explicitly qualified | MONEY_COST | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| PositionPLSigned | Позиция pl со знаком | Cycle/account as explicitly qualified | MONEY_FLOATING | account money | signed P/L | ACTUAL CURRENT | current position or broker-aware price model | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| FarLossSigned | Хвостовая позиция убыток со знаком | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | signed P/L | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| FarLossMagnitude | Хвостовая позиция убыток модуль | Cycle/account as explicitly qualified | MONEY_REALIZED | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| PartialFarBudgetProjected | Частичный хвостовая позиция бюджет прогнозный | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | non-negative magnitude/bucket | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| PartialFarBudgetReal | Частичный хвостовая позиция бюджет подтверждённый | Cycle/account as explicitly qualified | MONEY_RESERVED | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| PartialFarBudgetAvailable | Частичный хвостовая позиция бюджет доступный | Cycle/account as explicitly qualified | MONEY_AVAILABLE | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| PartialFarBudgetConsumed | Частичный хвостовая позиция бюджет израсходованный | Cycle/account as explicitly qualified | MONEY_CONSUMED | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| PartialFarBudgetResidual | Частичный хвостовая позиция бюджет остаточная | Cycle/account as explicitly qualified | MONEY_RESIDUAL | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| FinalReserveProjected | Финальный резерв прогнозный | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | non-negative magnitude/bucket | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| FinalReserveReal | Финальный резерв подтверждённый | Cycle/account as explicitly qualified | MONEY_RESERVED | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | TotalReserve, finalReserveReal | APPROVED_TERM |
| ReserveAddProjected | Резерв начисление прогнозный | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | non-negative magnitude/bucket | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| ReserveAddReal | Резерв начисление подтверждённый | Cycle/account as explicitly qualified | MONEY_RESERVED | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| ReserveAvailable | Резерв доступный | Cycle/account as explicitly qualified | MONEY_AVAILABLE | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| ReserveConsumed | Резерв израсходованный | Cycle/account as explicitly qualified | MONEY_CONSUMED | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| ReserveResidual | Резерв остаточная | Cycle/account as explicitly qualified | MONEY_RESIDUAL | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| CarryAvailable | Переносимый остаток доступный | Cycle/account as explicitly qualified | MONEY_AVAILABLE | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| CarryConsumed | Переносимый остаток израсходованный | Cycle/account as explicitly qualified | MONEY_CONSUMED | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| CarryResidual | Переносимый остаток остаточная | Cycle/account as explicitly qualified | MONEY_RESIDUAL | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| TransitionBudgetAvailable | Переход бюджет доступный | Cycle/account as explicitly qualified | MONEY_AVAILABLE | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| FinalCloseRequirement | Финальный закрытие требование | Cycle/account as explicitly qualified | MONEY_RESERVED | account money | non-negative magnitude/bucket | ACTUAL CONFIRMED | confirmed deal history / exactly-once ledger | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| BasketRiskMoney | Корзина риск денежный | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | non-negative magnitude/bucket | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| AccountRiskMoney | Счёт риск денежный | Cycle/account as explicitly qualified | MONEY_PROJECTED | account money | non-negative magnitude/bucket | PROJECTED | OrderCalcProfit + explicit projected costs | ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate | MoneyTolerance | — | APPROVED_TERM |
| BigRatio | Компенсирующая позиция отношение | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | UNRESOLVED_PARAMETER_PROFILE |
| SmallRatio | Защитная позиция отношение | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | UNRESOLVED_PARAMETER_PROFILE |
| CloseBigOnSmallShare | Закрытие компенсирующая позиция on защитная позиция доля | Profile-qualified; unresolved values not selected | SHARE | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | UNRESOLVED_PARAMETER_PROFILE |
| RemainBigOnSmallShare | Remain компенсирующая позиция on защитная позиция доля | Profile-qualified; unresolved values not selected | SHARE | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | UNRESOLVED_PARAMETER_PROFILE |
| CloseFarShare | Закрытие хвостовая позиция доля | Profile-qualified; unresolved values not selected | SHARE | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | UNRESOLVED_PARAMETER_PROFILE |
| ReserveShare | Резерв доля | Profile-qualified; unresolved values not selected | SHARE | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | UNRESOLVED_PARAMETER_PROFILE |
| SmallReserveShare | Защитная позиция резерв доля | Profile-qualified; unresolved values not selected | SHARE | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| CompressionRatio | Сжатие отношение | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| ReserveCoverageRatio | Резерв покрытие отношение | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| RecoveryCoverageRatio | Восстановление покрытие отношение | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| MaximumNewBigToOldFarRatio | Максимальное новая компенсирующая позиция to предыдущая хвостовая позиция отношение | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | UNRESOLVED_BUSINESS_POLICY |
| MinimumReserveCatchUpRatio | Минимальное резерв catch up отношение | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| PercentValue | Процент стоимость | Profile-qualified; unresolved values not selected | PERCENT | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| ScaleMultiplier | Масштаб множитель | Profile-qualified; unresolved values not selected | MULTIPLIER | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| RiskThresholdRatio | Риск порог отношение | Profile-qualified; unresolved values not selected | RATIO | 1 (dimensionless) | non-negative; range stated per term | POLICY/PROJECTED | approved profile or typed formula | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| SymbolId | Символ идентификатор | Symbol+Magic+CycleID+role scope | SYMBOL_ID | integer/string identity | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| MagicId | Магический номер идентификатор | Symbol+Magic+CycleID+role scope | MAGIC_ID | integer/string identity | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | MagicNumber | APPROVED_TERM |
| CycleId | Цикл идентификатор | Symbol+Magic+CycleID+role scope | CYCLE_ID | integer/string identity | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | CycleID, cycleId | APPROVED_TERM |
| RoleId | Роль идентификатор | Symbol+Magic+CycleID+role scope | ROLE_ID | integer/string identity | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| PositionIdentifier | Позиция идентификатор | Symbol+Magic+CycleID+role scope | POSITION_ID | integer/string identity | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | POSITION_IDENTIFIER | APPROVED_TERM |
| PositionTicket | Позиция тикет | Symbol+Magic+CycleID+role scope | POSITION_TICKET | integer/string identity | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | ticket | APPROVED_TERM |
| OrderTicket | Ордер тикет | Symbol+Magic+CycleID+role scope | ORDER_TICKET | integer/string identity | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| DealTicket | Сделка тикет | Symbol+Magic+CycleID+role scope | DEAL_TICKET | integer/string identity | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| EventId | Событие идентификатор | Symbol+Magic+CycleID+role scope | EVENT_ID | integer/string identity | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| EventKey | Событие ключ | Symbol+Magic+CycleID+role scope | EVENT_ID | integer/string identity | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| SnapshotFingerprint | Снимок отпечаток | Symbol+Magic+CycleID+role scope | FINGERPRINT | integer/string identity | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT HASH MATCH | — | APPROVED_TERM |
| PlanFingerprint | План отпечаток | Symbol+Magic+CycleID+role scope | FINGERPRINT | integer/string identity | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT HASH MATCH | — | APPROVED_TERM |
| PositionComment | Позиция комментарий | Symbol+Magic+CycleID+role scope | ROLE_ID | integer/string identity | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| SnapshotRevision | Снимок ревизия | Symbol+Magic+CycleID+role scope | ROLE_ID | integer/string identity | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| StateRevision | Состояние ревизия | Symbol+Magic+CycleID+role scope | EVENT_ID | integer/string identity | non-zero/valid in active scope | ACTUAL CONFIRMED | MT5 properties / persisted reconciled namespace | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
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
| CandidatePlan | Кандидат план | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | PROJECTED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| ApprovedImmutablePlan | Утверждённый неизменяемый план | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | PROJECTED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| ExecutionRequest | Исполнение запрос | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| BrokerExecutionResult | Брокерский исполнение результат | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| ReconciledResult | Сверенный результат | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| CommittedLedgerEvent | Зафиксированный ledger событие | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| BaseSnapshot | Базовая снимок | Cycle lifecycle | STATE | enum/structured record | not numeric | PROJECTED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| WorstSnapshot | Worst снимок | Cycle lifecycle | STATE | enum/structured record | not numeric | PROJECTED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| ActualSnapshot | Фактический снимок | Cycle lifecycle | STATE | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| SnapshotStaleFlag | Снимок устаревший признак | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| FinalClosePreview | Финальный закрытие preview | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | PROJECTED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| FinalCloseActualSuccess | Финальный закрытие фактический успех | Cycle lifecycle | OUTCOME | enum/structured record | not numeric | ACTUAL/CONFIRMED | state machine or immutable snapshot/reconciliation | NO_ADDITIONAL_ROUNDING | EXACT ENUM MATCH | — | APPROVED_TERM |
| MoneyTolerance | Денежный допуск | Dimension-specific only | MONEY_AVAILABLE | same unit as compared operands | >=0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| VolumeToleranceLots | Объём допуск lots | Dimension-specific only | LOT_NORMALIZED | same unit as compared operands | >=0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| PriceTolerance | Цена допуск | Dimension-specific only | PRICE_PROJECTED | same unit as compared operands | >=0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| PointTolerance | Размер пункта допуск | Dimension-specific only | POINTS | same unit as compared operands | >=0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| RatioTolerance | Отношение допуск | Dimension-specific only | RATIO | same unit as compared operands | >=0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| ComparisonEpsilon | Comparison epsilon | Dimension-specific only | FINGERPRINT | integer/string identity | >=0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | EXACT HASH MATCH | — | APPROVED_TERM |
| ReserveMismatchTolerance | Резерв mismatch допуск | Dimension-specific only | MONEY_AVAILABLE | same unit as compared operands | >=0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| GeometryTolerance | Геометрический допуск | Dimension-specific only | LOT_NORMALIZED | same unit as compared operands | >=0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | self | — | APPROVED_TERM |
| FingerprintTolerance | Отпечаток допуск | Dimension-specific only | FINGERPRINT | integer/string identity | >=0 | POLICY | approved config/symbol properties | NO_ADDITIONAL_ROUNDING | EXACT HASH MATCH | — | APPROVED_TERM |
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
| CurrentBid | текущая цена Bid | All | PRICE_BID | price | non-negative | ACTUAL CURRENT | SymbolInfoDouble(symbol, SYMBOL_BID) | NO_ADDITIONAL_ROUNDING | PriceTolerance | — | APPROVED_TERM |
| CurrentAsk | текущая цена Ask | All | PRICE_ASK | price | non-negative | ACTUAL CURRENT | SymbolInfoDouble(symbol, SYMBOL_ASK) | NO_ADDITIONAL_ROUNDING | PriceTolerance | — | APPROVED_TERM |
| ReserveProjected | прогнозный резерв до подтверждения | All | MONEY_PROJECTED | account money | non-negative | PROJECTED | OrderCalcProfit outputs plus explicit projected allocation model | NO_ADDITIONAL_ROUNDING | MoneyTolerance | — | APPROVED_TERM |
| ReserveCoverage | отношение доступного резерва к требованию закрытия | All | RATIO | dimensionless | non-negative | PROJECTED or ACTUAL RATIO | ReserveAvailable divided by FinalCloseRequirement | NO_ADDITIONAL_ROUNDING | RatioTolerance | — | APPROVED_TERM |
| Symbol | торговый символ цикла | All | SYMBOL_ID | string identity | not numeric | ACTUAL CONFIRMED | current chart/request symbol and reconciled position symbol | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| MagicNumber | магический номер стратегии | All | MAGIC_ID | integer identity | not numeric | POLICY/ACTUAL CONFIRMED | configured MagicNumber verified against position/deal properties | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| CycleID | идентификатор recovery-цикла | All | CYCLE_ID | integer identity | not numeric | ACTUAL CONFIRMED | persisted cycle creation event confirmed by reconciliation | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| EventID | идентификатор ledger-события | All | EVENT_ID | integer/string identity | not numeric | ACTUAL CONFIRMED | exactly-once ledger event namespace | NO_ADDITIONAL_ROUNDING | EXACT | — | APPROVED_TERM |
| Fingerprint | типизированный отпечаток snapshot или plan | All | FINGERPRINT | hash identity | not numeric | PROJECTED or RECONCILED | canonical serialization of typed fields and revision | NO_ADDITIONAL_ROUNDING | EXACT HASH MATCH | — | APPROVED_TERM |
| Comment | комментарий торгового объекта | All | DIAGNOSTIC_TEXT | text | not numeric | ACTUAL OBSERVATION | MT5 position/order/deal comment property | NO_ADDITIONAL_ROUNDING | EXACT TEXT; never identity | — | APPROVED_TERM |
| Preview | read-only предварительная оценка | All | PHASE | structured record | not numeric | PROJECTED | fresh immutable snapshot evaluator | NO_ADDITIONAL_ROUNDING | EXACT STRUCTURE | — | APPROVED_TERM |
| Candidate | кандидат плана до полного gate-chain | All | OUTCOME | structured record | not numeric | PROJECTED | solver output tied to source fingerprint | NO_ADDITIONAL_ROUNDING | EXACT STRUCTURE | — | APPROVED_TERM |
| Plan | расчётный набор действий и ожиданий | All | STATE | structured record | not numeric | PROJECTED | candidate planner output with revision | NO_ADDITIONAL_ROUNDING | EXACT STRUCTURE | — | APPROVED_TERM |
| ApprovedPlan | неизменяемый план после всех обязательных gates | All | STATE | structured record | not numeric | PROJECTED APPROVED | approved immutable plan and fingerprint | NO_ADDITIONAL_ROUNDING | EXACT STRUCTURE | — | APPROVED_TERM |
<!-- STAGE_3_1_3_CANONICAL_TABLE_END -->

## Расширенные records canonical terms

### Legacy
CanonicalName: `Legacy`
Русское название: Устаревшая архитектура
Краткое определение: Legacy — typed `STATE` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
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
Lifecycle: Legacy: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: Legacy нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Legacy, тип STATE, class POLICY.
Legacy aliases: —
MQL5 mapping: Include/Config.mqh::legacy, Include/HybridCatchUpModel.mqh::legacy
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::Legacy, Tests/static/test_split_architecture_static.py::legacy
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `HSB-DOC-CONFLICT-031`
Resolution stage: `3.1.8`
Статус определения: `DOCUMENTED_NOT_APPROVED`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `Legacy`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### LegacyMode
CanonicalName: `LegacyMode`
Русское название: Устаревшая архитектура режим
Краткое определение: LegacyMode — typed `STATE` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
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
Lifecycle: LegacyMode: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: LegacyMode нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: LegacyMode, тип STATE, class POLICY.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `LegacyMode`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### LegacyBig
CanonicalName: `LegacyBig`
Русское название: Устаревшая архитектура компенсирующая позиция
Краткое определение: LegacyBig — Монолитная компенсирующая позиция Legacy mode; не является BigCore и требует явного LegacyMode qualifier.
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
Lifecycle: LegacyBig: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: LegacyBig нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: LegacyBig, тип ROLE_ID, class POLICY.
Legacy aliases: —
MQL5 mapping: Include/ReconciliationEngine.mqh::LegacyBig
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `LegacyBig`; MQL5 identifier evidence found in inspected corpus. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### LegacySmall
CanonicalName: `LegacySmall`
Русское название: Устаревшая архитектура защитная позиция
Краткое определение: LegacySmall — Монолитная защитная позиция Legacy mode; не является SmallBase без mode mapping.
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
Lifecycle: LegacySmall: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: LegacySmall нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: LegacySmall, тип ROLE_ID, class POLICY.
Legacy aliases: —
MQL5 mapping: Include/ReconciliationEngine.mqh::LegacySmall
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `LegacySmall`; MQL5 identifier evidence found in inspected corpus. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### LegacyFar
CanonicalName: `LegacyFar`
Русское название: Устаревшая архитектура хвостовая позиция
Краткое определение: LegacyFar — Хвостовая позиция Legacy cycle; роль не переносится в Hybrid plan без explicit mode routing.
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
Lifecycle: LegacyFar: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: LegacyFar нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: LegacyFar, тип ROLE_ID, class POLICY.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `LegacyFar`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### MonolithicBig
CanonicalName: `MonolithicBig`
Русское название: Монолитный компенсирующая позиция
Краткое определение: MonolithicBig — Расчётно и идентификационно единый LegacyBig без Core/Trend split; отличается от BigGross, который является суммой двух ролей.
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
Lifecycle: MonolithicBig: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: MonolithicBig нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: MonolithicBig, тип ROLE_ID, class POLICY.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `MonolithicBig`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### Split
CanonicalName: `Split`
Русское название: Разделённый
Краткое определение: Split — Архитектурное поколение, разделяющее компенсирующий Big на BigCore и BigTrend; это не runtime state и не numeric profile.
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
Lifecycle: Split: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: Split нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Split, тип STATE, class POLICY.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::Split, Include/Config.mqh::Split
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::Split, Tests/HybridSplitBig/test_hybrid_split_big_reference.py::split
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `HSB-DOC-CONFLICT-031`
Resolution stage: `3.1.8`
Статус определения: `DOCUMENTED_NOT_APPROVED`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `Split`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### SplitMode
CanonicalName: `SplitMode`
Русское название: Разделённый режим
Краткое определение: SplitMode — Явный runtime/config discriminator выбора Split role graph; не подменяется фактом наличия поля BigCore.
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
Lifecycle: SplitMode: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: SplitMode нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SplitMode, тип STATE, class POLICY.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `SplitMode`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### SplitBig
CanonicalName: `SplitBig`
Русское название: Разделённый компенсирующая позиция
Краткое определение: SplitBig — Совокупность BigCore и BigTrend в Split mode; термин обозначает role group, а не самостоятельный position identifier.
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
Lifecycle: SplitBig: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: SplitBig нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SplitBig, тип ROLE_ID, class POLICY.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `SplitBig`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### BigCore
CanonicalName: `BigCore`
Русское название: Компенсирующая позиция основная часть
Краткое определение: BigCore — Основная компенсирующая роль Split/Hybrid basket, направленная против CurrentFar и учитываемая отдельно от BigTrend; возможное использование её остатка как NewFar остаётся mode-dependent по конфликту 020.
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
Lifecycle: BigCore: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: BigCore нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigCore, тип ROLE_ID, class POLICY.
Legacy aliases: Core
MQL5 mapping: Include/HybridGeometrySolver.mqh::BigCore, Include/PendingContractEngine.mqh::BigCore
Python mapping: Tests/clean_start_split_context_check.py::BigCore, Tests/split_persistence_context_check.py::BigCore
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `BigCore`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### BigTrend
CanonicalName: `BigTrend`
Русское название: Компенсирующая позиция трендовая часть
Краткое определение: BigTrend — Дополнительная трендовая роль Split/Hybrid basket против CurrentFar; она не объединяется с BigCore в identity и не может молча быть назначена NewFar.
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
Lifecycle: BigTrend: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: BigTrend нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigTrend, тип ROLE_ID, class POLICY.
Legacy aliases: Trend
MQL5 mapping: Include/HybridGeometrySolver.mqh::BigTrend, Include/PendingContractEngine.mqh::BigTrend
Python mapping: Tests/clean_start_split_context_check.py::BigTrend, Tests/split_persistence_context_check.py::BigTrend
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `BigTrend`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### BigGross
CanonicalName: `BigGross`
Русское название: Компенсирующая позиция валовая
Краткое определение: BigGross — Сумма объёмов BigCore и BigTrend для gross-exposure checks; это расчётная величина, а не отдельная позиция или ticket.
Архитектурный профиль: BigGross
Торговая роль: BigGross
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: POLICY stage для BigGross.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: BigGross: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: BigGross нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigGross, тип ROLE_ID, class POLICY.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `BigGross`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### SmallBase
CanonicalName: `SmallBase`
Русское название: Защитная позиция базовая
Краткое определение: SmallBase — Защитная роль Split/Hybrid basket в направлении CurrentFar; её volume, P/L и identity ведутся отдельно от LegacySmall.
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
Lifecycle: SmallBase: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: SmallBase нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SmallBase, тип ROLE_ID, class POLICY.
Legacy aliases: Small
MQL5 mapping: Include/HybridGeometrySolver.mqh::SmallBase, Include/PendingContractEngine.mqh::SmallBase
Python mapping: Tests/clean_start_split_context_check.py::SmallBase, Tests/scenario/test_split_architecture_restart.py::small_base
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `SmallBase`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### Hybrid
CanonicalName: `Hybrid`
Русское название: Гибридный
Краткое определение: Hybrid — Архитектурный scope, объединяющий split roles с immutable preview/plan/gates; conflict 031 запрещает считать его alias Legacy.
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
Lifecycle: Hybrid: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: Hybrid нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Hybrid, тип STATE, class POLICY.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::hybrid, Include/Config.mqh::Hybrid
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::Hybrid, Tools/hybrid_big_sequence_model.py::Hybrid
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `HSB-DOC-CONFLICT-031`
Resolution stage: `3.1.8`
Статус определения: `DOCUMENTED_NOT_APPROVED`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `Hybrid`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### HybridSplitBig
CanonicalName: `HybridSplitBig`
Русское название: Гибридный разделённый компенсирующая позиция
Краткое определение: HybridSplitBig — Полное имя Hybrid basket с BigCore, BigTrend и SmallBase; определяет vocabulary scope, но не выбирает coefficients.
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
Lifecycle: HybridSplitBig: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: HybridSplitBig нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: HybridSplitBig, тип STATE, class POLICY.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: Tests/HybridSplitBig/test_document_consistency.py::HybridSplitBig
Mapping status: MQL5=`MISSING`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `HybridSplitBig`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. Python identifier evidence found in inspected corpus.

### HybridMode
CanonicalName: `HybridMode`
Русское название: Гибридный режим
Краткое определение: HybridMode — Mode discriminator для Hybrid plan/execution contracts; его наличие должно подтверждаться config/plan, а не comment.
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
Lifecycle: HybridMode: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: HybridMode нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: HybridMode, тип STATE, class POLICY.
Legacy aliases: —
MQL5 mapping: Include/Config.mqh::HybridMode
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `HybridMode`; MQL5 identifier evidence found in inspected corpus. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### HybridPlan
CanonicalName: `HybridPlan`
Русское название: Гибридный план
Краткое определение: HybridPlan — Immutable projected action set с revision/fingerprint и role-qualified lots; отличается от HybridPreview отсутствием права изменять frozen inputs.
Архитектурный профиль: HybridPlan
Торговая роль: HybridPlan
Размерность: `STATE`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `STATE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: POLICY stage для HybridPlan.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: HybridPlan: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: HybridPlan нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: HybridPlan, тип STATE, class POLICY.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `HybridPlan`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### HybridPreview
CanonicalName: `HybridPreview`
Русское название: Гибридный preview
Краткое определение: HybridPreview — Read-only расчёт Base/Worst candidate до approval; PASS не является broker execution success.
Архитектурный профиль: HybridPreview
Торговая роль: HybridPreview
Размерность: `STATE`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `STATE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: POLICY stage для HybridPreview.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: HybridPreview: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: HybridPreview нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: HybridPreview, тип STATE, class POLICY.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `HybridPreview`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### HybridExecution
CanonicalName: `HybridExecution`
Русское название: Гибридный исполнение
Краткое определение: HybridExecution — Исполнение ApprovedPlan с broker result, deals и reconciliation; отличается от preview фактическими evidence и возможным partial outcome.
Архитектурный профиль: HybridExecution
Торговая роль: HybridExecution
Размерность: `STATE`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `STATE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: POLICY stage для HybridExecution.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: HybridExecution: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: HybridExecution нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: HybridExecution, тип STATE, class POLICY.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `HybridExecution`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### InitialBuy
CanonicalName: `InitialBuy`
Русское название: Начальная покупка
Краткое определение: InitialBuy — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
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
Lifecycle: InitialBuy: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: InitialBuy нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: InitialBuy, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/StateMachine.mqh::InitialBuy
Python mapping: Tests/known_context_diagnostics_check.py::InitialBuy
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `InitialBuy`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### InitialSell
CanonicalName: `InitialSell`
Русское название: Начальная продажа
Краткое определение: InitialSell — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
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
Lifecycle: InitialSell: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: InitialSell нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: InitialSell, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/StateMachine.mqh::InitialSell
Python mapping: Tests/known_context_diagnostics_check.py::InitialSell
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `InitialSell`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### InitialProfitLeg
CanonicalName: `InitialProfitLeg`
Русское название: Начальная прибыль leg
Краткое определение: InitialProfitLeg — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
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
Lifecycle: InitialProfitLeg: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: InitialProfitLeg нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: InitialProfitLeg, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `InitialProfitLeg`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### InitialLosingLeg
CanonicalName: `InitialLosingLeg`
Русское название: Начальная убыточная leg
Краткое определение: InitialLosingLeg — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
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
Lifecycle: InitialLosingLeg: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: InitialLosingLeg нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: InitialLosingLeg, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `InitialLosingLeg`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### InitialIgnoredProfit
CanonicalName: `InitialIgnoredProfit`
Русское название: Начальная исключённая прибыль
Краткое определение: InitialIgnoredProfit — Подтверждённый signed net закрытия прибыльной initial leg, сохранённый только как диагностика и исключённый из Reserve и RecoveryPL decision money.
Архитектурный профиль: Role-qualified architecture
Торговая роль: InitialIgnoredProfit
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: signed confirmed result; excluded from recovery money
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed closing deal aggregation of InitialProfitLeg filtered by Symbol+Magic+CycleID+position identity
Authoritative source: confirmed closing deal aggregation of InitialProfitLeg filtered by Symbol+Magic+CycleID+position identity
Время фиксации: ACTUAL CONFIRMED stage для InitialIgnoredProfit.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS at ledger/report boundary
Rounding: ROUND_TO_MONEY_DIGITS at ledger/report boundary
Tolerance: `MoneyTolerance`
Lifecycle: InitialIgnoredProfit: возникает только из confirmed filtered deals; фиксируется exactly-once ledger event; stale при history/identity mismatch; заменяется rebuilt reconciled ledger, не OrderCalcProfit.
Условия stale: при history/identity mismatch.
Authoritative replacement: rebuilt reconciled ledger, не OrderCalcProfit..
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: InitialIgnoredProfit нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: InitialIgnoredProfit, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/Logger.mqh::InitialIgnoredProfit, Include/StateMachine.mqh::InitialIgnoredProfit
Python mapping: Tests/csv_recovery_fields_check.py::InitialIgnoredProfit, Tests/initial_ignored_profit_excluded_check.py::initialIgnoredProfit
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `InitialIgnoredProfit`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### OldFar
CanonicalName: `OldFar`
Русское название: Предыдущая хвостовая позиция
Краткое определение: OldFar — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
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
Lifecycle: OldFar: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: OldFar нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: OldFar, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::oldFar, Include/RecoveryMath.mqh::OldFar
Python mapping: Tests/fsm_integrity_strict_check.py::OldFar, Tests/small_reverse_compression_check.py::old_far
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `OldFar`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### CurrentFar
CanonicalName: `CurrentFar`
Русское название: Текущая хвостовая позиция
Краткое определение: CurrentFar — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
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
Lifecycle: CurrentFar: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: CurrentFar нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CurrentFar, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: Far
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `CurrentFar`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ResidualFar
CanonicalName: `ResidualFar`
Русское название: Остаточная хвостовая позиция
Краткое определение: ResidualFar — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
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
Lifecycle: ResidualFar: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: ResidualFar нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ResidualFar, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ResidualFar`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### NewFar
CanonicalName: `NewFar`
Русское название: Новая хвостовая позиция
Краткое определение: NewFar — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
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
Lifecycle: NewFar: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: NewFar нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: NewFar, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::newFar, Include/HybridTransitionPlanner.mqh::NewFar
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::new_far, Tests/HybridSplitBig/test_hybrid_split_big_reference.py::new_far
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `NewFar`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### LegacyBigPosition
CanonicalName: `LegacyBigPosition`
Русское название: Устаревшая архитектура компенсирующая позиция позиция
Краткое определение: LegacyBigPosition — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Role-qualified architecture
Торговая роль: LegacyBig
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для LegacyBigPosition.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: LegacyBigPosition: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: LegacyBigPosition нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: LegacyBig, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `LegacyBigPosition`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### BigCorePosition
CanonicalName: `BigCorePosition`
Русское название: Компенсирующая позиция основная часть позиция
Краткое определение: BigCorePosition — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Role-qualified architecture
Торговая роль: BigCore
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для BigCorePosition.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: BigCorePosition: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: BigCorePosition нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigCore, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `BigCorePosition`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### BigTrendPosition
CanonicalName: `BigTrendPosition`
Русское название: Компенсирующая позиция трендовая часть позиция
Краткое определение: BigTrendPosition — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Role-qualified architecture
Торговая роль: BigTrend
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для BigTrendPosition.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: BigTrendPosition: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: BigTrendPosition нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigTrend, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `BigTrendPosition`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### LegacySmallPosition
CanonicalName: `LegacySmallPosition`
Русское название: Устаревшая архитектура защитная позиция позиция
Краткое определение: LegacySmallPosition — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Role-qualified architecture
Торговая роль: LegacySmall
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для LegacySmallPosition.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: LegacySmallPosition: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: LegacySmallPosition нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: LegacySmall, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `LegacySmallPosition`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### SmallBasePosition
CanonicalName: `SmallBasePosition`
Русское название: Защитная позиция базовая позиция
Краткое определение: SmallBasePosition — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Role-qualified architecture
Торговая роль: SmallBase
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для SmallBasePosition.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: SmallBasePosition: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: SmallBasePosition нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SmallBase, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `SmallBasePosition`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ManagedPosition
CanonicalName: `ManagedPosition`
Русское название: Управляемая позиция
Краткое определение: ManagedPosition — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ManagedPosition
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для ManagedPosition.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: ManagedPosition: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: ManagedPosition нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ManagedPosition, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ManagedPosition`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### UnmanagedPosition
CanonicalName: `UnmanagedPosition`
Русское название: Неуправляемая позиция
Краткое определение: UnmanagedPosition — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Role-qualified architecture
Торговая роль: UnmanagedPosition
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для UnmanagedPosition.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: UnmanagedPosition: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: UnmanagedPosition нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: UnmanagedPosition, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `UnmanagedPosition`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ForeignCyclePosition
CanonicalName: `ForeignCyclePosition`
Русское название: Чужая цикл позиция
Краткое определение: ForeignCyclePosition — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ForeignCyclePosition
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: not numeric
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: ACTUAL CONFIRMED stage для ForeignCyclePosition.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: ForeignCyclePosition: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: ForeignCyclePosition нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ForeignCyclePosition, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ForeignCyclePosition`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### FarDirection
CanonicalName: `FarDirection`
Русское название: Хвостовая позиция направление
Краткое определение: FarDirection — Абсолютный BUY/SELL type текущей подтверждённой Far position, считанный из reconciled position snapshot.
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
Lifecycle: FarDirection: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `DIRECTION_ENUM` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: FarDirection нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Far, тип DIRECTION_ENUM, class ACTUAL CONFIRMED or POLICY DERIVED.
Legacy aliases: —
MQL5 mapping: Include/HybridCatchUpModel.mqh::farDirection, Include/HybridDecisionEngine.mqh::farDirection
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::far_direction, Tests/old_far_cleanup_after_close_check.py::farDirection
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `FarDirection`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### OppositeFarDirection
CanonicalName: `OppositeFarDirection`
Русское название: Противоположное хвостовая позиция направление
Краткое определение: OppositeFarDirection — Детерминированная инверсия FarDirection по таблице BUY→SELL и SELL→BUY.
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
Lifecycle: OppositeFarDirection: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `DIRECTION_ENUM` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: OppositeFarDirection нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: OppositeFarDirection, тип DIRECTION_ENUM, class ACTUAL CONFIRMED or POLICY DERIVED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `OppositeFarDirection`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### SameAsFarDirection
CanonicalName: `SameAsFarDirection`
Русское название: Совпадающее с хвостовая позиция направление
Краткое определение: SameAsFarDirection — Детерминированное относительное направление, равное FarDirection; не требует чтения отдельной позиции.
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
Lifecycle: SameAsFarDirection: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `DIRECTION_ENUM` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: SameAsFarDirection нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SameAsFarDirection, тип DIRECTION_ENUM, class ACTUAL CONFIRMED or POLICY DERIVED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `SameAsFarDirection`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### BigDirection
CanonicalName: `BigDirection`
Русское название: Компенсирующая позиция направление
Краткое определение: BigDirection — Role-policy direction для LegacyBig или Hybrid BigCore/BigTrend относительно Far; требует architecture qualifier.
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
Lifecycle: BigDirection: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `DIRECTION_ENUM` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: BigDirection нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigDirection, тип DIRECTION_ENUM, class ACTUAL CONFIRMED or POLICY DERIVED.
Legacy aliases: —
MQL5 mapping: Include/HybridCatchUpModel.mqh::bigDirection, Include/HybridDecisionEngine.mqh::bigDirection
Python mapping: Tests/retry_open_big_must_resolve_ticket_check.py::bigDirection, Tools/optimize_big_scenario_min_levels.py::BigDirection
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `BigDirection`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### SmallDirection
CanonicalName: `SmallDirection`
Русское название: Защитная позиция направление
Краткое определение: SmallDirection — Role-policy direction LegacySmall/SmallBase относительно Far; требует architecture qualifier.
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
Lifecycle: SmallDirection: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `DIRECTION_ENUM` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: SmallDirection нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SmallDirection, тип DIRECTION_ENUM, class ACTUAL CONFIRMED or POLICY DERIVED.
Legacy aliases: —
MQL5 mapping: Include/HybridCatchUpModel.mqh::smallDirection, Include/HybridDecisionEngine.mqh::smallDirection
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::small_direction, Tests/small_build_new_far_no_active_small_direction_check.py::smallDirection
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `SmallDirection`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### TrendDirection
CanonicalName: `TrendDirection`
Русское название: Трендовая часть направление
Краткое определение: TrendDirection — Направление BigTrend, вычисленное из FarDirection и утверждённого Hybrid role rule; не берётся из comment.
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
Lifecycle: TrendDirection: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `DIRECTION_ENUM` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: TrendDirection нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: TrendDirection, тип DIRECTION_ENUM, class ACTUAL CONFIRMED or POLICY DERIVED.
Legacy aliases: —
MQL5 mapping: Include/HybridGeometrySolver.mqh::trendDirection, Include/Types.mqh::trendDirection
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::trend_direction
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `TrendDirection`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### ReverseDirection
CanonicalName: `ReverseDirection`
Русское название: Разворот направление
Краткое определение: ReverseDirection — Направление следующего reversal role, полученное из подтверждённого transition plan; до approval остаётся projected.
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
Lifecycle: ReverseDirection: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `DIRECTION_ENUM` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: ReverseDirection нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ReverseDirection, тип DIRECTION_ENUM, class ACTUAL CONFIRMED or POLICY DERIVED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: Tests/test_dynamic_reverse_small_direction.py::reverse_direction
Mapping status: MQL5=`MISSING`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ReverseDirection`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. Python identifier evidence found in inspected corpus.

### RawLot
CanonicalName: `RawLot`
Русское название: Сырой объём в лотах
Краткое определение: RawLot — Ненормализованный объём, непосредственно полученный из исходной математической формулы; отличается от CalculatedLot отсутствием terminal constraints.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: RawLot
Размерность: `LOT_RAW`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_RAW`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для RawLot.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: RawLot: создаётся на своей pre-request стадии `PROJECTED`; invalid при изменении formula inputs/symbol constraints/fingerprint; заменяется следующим named lot stage, а не actual присваиванием.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: следующим named lot stage, а не actual присваиванием..
Допустимые операции: сравнение и преобразование только по `LOT_RAW` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: RawLot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RawLot, тип LOT_RAW, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/RecoveryMath.mqh::rawLot
Python mapping: Tests/big_scenario_math_check.py::rawLot, Tests/far_partial_budget_check.py::rawLot
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `RawLot`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### CalculatedLot
CanonicalName: `CalculatedLot`
Русское название: Расчётный объём в лотах
Краткое определение: CalculatedLot — Результат role formula до broker volume constraints; отличается от RawLot применёнными formula rules и от NormalizedLot отсутствием min/max/step.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: CalculatedLot
Размерность: `LOT_CALCULATED`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_CALCULATED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для CalculatedLot.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: CalculatedLot: создаётся на своей pre-request стадии `PROJECTED`; invalid при изменении formula inputs/symbol constraints/fingerprint; заменяется следующим named lot stage, а не actual присваиванием.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: следующим named lot stage, а не actual присваиванием..
Допустимые операции: сравнение и преобразование только по `LOT_CALCULATED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: CalculatedLot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CalculatedLot, тип LOT_CALCULATED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `CalculatedLot`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### NormalizedLot
CanonicalName: `NormalizedLot`
Русское название: Нормализованный объём в лотах
Краткое определение: NormalizedLot — CalculatedLot после Symbol volume min/max/step и named rounding policy; ещё не является requested или filled volume.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: NormalizedLot
Размерность: `LOT_NORMALIZED`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_NORMALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для NormalizedLot.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: NormalizedLot: создаётся на своей pre-request стадии `PROJECTED`; invalid при изменении formula inputs/symbol constraints/fingerprint; заменяется следующим named lot stage, а не actual присваиванием.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: следующим named lot stage, а не actual присваиванием..
Допустимые операции: сравнение и преобразование только по `LOT_NORMALIZED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: NormalizedLot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: NormalizedLot, тип LOT_NORMALIZED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/StateMachine.mqh::NormalizedLot
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `NormalizedLot`; MQL5 identifier evidence found in inspected corpus. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### RequestedLot
CanonicalName: `RequestedLot`
Русское название: Запрошенный объём в лотах
Краткое определение: RequestedLot — Frozen NormalizedLot, помещённый в один trade request; не доказывает FilledLot.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: RequestedLot
Размерность: `LOT_REQUESTED`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_REQUESTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved immutable plan
Authoritative source: approved immutable plan
Время фиксации: REQUESTED stage для RequestedLot.
Projected/Actual class: `REQUESTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: RequestedLot: создаётся при freeze ApprovedPlan; immutable внутри request; stale при fingerprint/revision mismatch; заменяется FilledLot из confirmed deals.
Условия stale: при fingerprint/revision mismatch.
Authoritative replacement: FilledLot из confirmed deals..
Допустимые операции: сравнение и преобразование только по `LOT_REQUESTED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: RequestedLot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RequestedLot, тип LOT_REQUESTED, class REQUESTED.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::requestedLot, Include/SimulationEngine.mqh::requestedLot
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `RequestedLot`; MQL5 identifier evidence found in inspected corpus. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### FilledLot
CanonicalName: `FilledLot`
Русское название: Исполненный объём в лотах
Краткое определение: FilledLot — Сумма подтверждённых deal volumes данного request/event; не равна ActualPositionLot без position reconciliation.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: FilledLot
Размерность: `LOT_FILLED`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_FILLED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deals/trade result
Authoritative source: confirmed deals/trade result
Время фиксации: CONFIRMED stage для FilledLot.
Projected/Actual class: `CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: FilledLot: появляется при confirmed deal aggregation; дополняется последующими fills того же event; stale при incomplete history; заменяется reconciled ActualPositionLot.
Условия stale: при incomplete history.
Authoritative replacement: reconciled ActualPositionLot..
Допустимые операции: сравнение и преобразование только по `LOT_FILLED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: FilledLot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: FilledLot, тип LOT_FILLED, class CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/SimulationEngine.mqh::filledLot, Include/StateMachine.mqh::FilledLot
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `FilledLot`; MQL5 identifier evidence found in inspected corpus. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ActualPositionLot
CanonicalName: `ActualPositionLot`
Русское название: Фактический позиция объём в лотах
Краткое определение: ActualPositionLot — Текущий terminal position volume после reconciliation; повторная normalization запрещена.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: ActualPositionLot
Размерность: `LOT_POSITION_ACTUAL`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_POSITION_ACTUAL`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: current MT5 position snapshot
Authoritative source: current MT5 position snapshot
Время фиксации: ACTUAL CURRENT stage для ActualPositionLot.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: ActualPositionLot: появляется из current position snapshot; обновляется после любого fill/close; stale сразу после trade event; заменяется новым reconciled snapshot; NOT_APPLICABLE после полного close.
Условия stale: сразу после trade event.
Authoritative replacement: новым reconciled snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_POSITION_ACTUAL` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: ActualPositionLot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ActualPositionLot, тип LOT_POSITION_ACTUAL, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::actualPositionLot, Include/PositionUtils.mqh::actualVolume
Python mapping: Tests/full_close_not_min_lot_check.py::actualVolume, Tests/full_close_volume_tolerance_check.py::actualVolume
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ActualPositionLot`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### ResidualLotProjected
CanonicalName: `ResidualLotProjected`
Русское название: Остаточная объём в лотах прогнозный
Краткое определение: ResidualLotProjected — Плановый остаток до execution, вычисленный из requested close; не может назначать actual role.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: ResidualLotProjected
Размерность: `LOT_RESIDUAL`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_RESIDUAL`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для ResidualLotProjected.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: ResidualLotProjected: создаётся на своей pre-request стадии `PROJECTED`; invalid при изменении formula inputs/symbol constraints/fingerprint; заменяется следующим named lot stage, а не actual присваиванием.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: следующим named lot stage, а не actual присваиванием..
Допустимые операции: сравнение и преобразование только по `LOT_RESIDUAL` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: ResidualLotProjected нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ResidualLotProjected, тип LOT_RESIDUAL, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ResidualLotProjected`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ResidualLotActual
CanonicalName: `ResidualLotActual`
Русское название: Остаточная объём в лотах фактический
Краткое определение: ResidualLotActual — Остаток текущей позиции после confirmed fills и reconciliation; заменяет projected residual.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: ResidualLotActual
Размерность: `LOT_POSITION_ACTUAL`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_POSITION_ACTUAL`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: current MT5 position snapshot
Authoritative source: current MT5 position snapshot
Время фиксации: ACTUAL CURRENT stage для ResidualLotActual.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: ResidualLotActual: появляется из current position snapshot; обновляется после любого fill/close; stale сразу после trade event; заменяется новым reconciled snapshot; NOT_APPLICABLE после полного close.
Условия stale: сразу после trade event.
Authoritative replacement: новым reconciled snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_POSITION_ACTUAL` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: ResidualLotActual нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ResidualLotActual, тип LOT_POSITION_ACTUAL, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ResidualLotActual`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### FarLotRaw
CanonicalName: `FarLotRaw`
Русское название: Хвостовая позиция объём в лотах сырой
Краткое определение: FarLotRaw — объём `Far` на стадии до broker normalization; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: Far
Размерность: `LOT_RAW`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_RAW`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для FarLotRaw.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: FarLotRaw: создаётся на своей pre-request стадии `PROJECTED`; invalid при изменении formula inputs/symbol constraints/fingerprint; заменяется следующим named lot stage, а не actual присваиванием.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: следующим named lot stage, а не actual присваиванием..
Допустимые операции: сравнение и преобразование только по `LOT_RAW` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: FarLotRaw нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Far, тип LOT_RAW, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `FarLotRaw`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### FarLotCalculated
CanonicalName: `FarLotCalculated`
Русское название: Хвостовая позиция объём в лотах расчётный
Краткое определение: FarLotCalculated — объём `Far` на стадии после роли/formula до terminal constraints; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: Far
Размерность: `LOT_CALCULATED`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_CALCULATED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для FarLotCalculated.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: FarLotCalculated: создаётся на своей pre-request стадии `PROJECTED`; invalid при изменении formula inputs/symbol constraints/fingerprint; заменяется следующим named lot stage, а не actual присваиванием.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: следующим named lot stage, а не actual присваиванием..
Допустимые операции: сравнение и преобразование только по `LOT_CALCULATED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: FarLotCalculated нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Far, тип LOT_CALCULATED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `FarLotCalculated`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### FarLotNormalized
CanonicalName: `FarLotNormalized`
Русское название: Хвостовая позиция объём в лотах нормализованный
Краткое определение: FarLotNormalized — объём `Far` на стадии после min/max/step и profile rounding; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: Far
Размерность: `LOT_NORMALIZED`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_NORMALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для FarLotNormalized.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: FarLotNormalized: создаётся на своей pre-request стадии `PROJECTED`; invalid при изменении formula inputs/symbol constraints/fingerprint; заменяется следующим named lot stage, а не actual присваиванием.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: следующим named lot stage, а не actual присваиванием..
Допустимые операции: сравнение и преобразование только по `LOT_NORMALIZED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: FarLotNormalized нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Far, тип LOT_NORMALIZED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `FarLotNormalized`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### FarLotRequested
CanonicalName: `FarLotRequested`
Русское название: Хвостовая позиция объём в лотах запрошенный
Краткое определение: FarLotRequested — объём `Far` на стадии после freeze approved plan и отправки request; он отличается от соседних lot stages источником `approved immutable plan` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: Far
Размерность: `LOT_REQUESTED`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_REQUESTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved immutable plan
Authoritative source: approved immutable plan
Время фиксации: REQUESTED stage для FarLotRequested.
Projected/Actual class: `REQUESTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: FarLotRequested: создаётся при freeze ApprovedPlan; immutable внутри request; stale при fingerprint/revision mismatch; заменяется FilledLot из confirmed deals.
Условия stale: при fingerprint/revision mismatch.
Authoritative replacement: FilledLot из confirmed deals..
Допустимые операции: сравнение и преобразование только по `LOT_REQUESTED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: FarLotRequested нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Far, тип LOT_REQUESTED, class REQUESTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `FarLotRequested`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### FarLotFilled
CanonicalName: `FarLotFilled`
Русское название: Хвостовая позиция объём в лотах исполненный
Краткое определение: FarLotFilled — объём `Far` на стадии после aggregation подтверждённых deals; он отличается от соседних lot stages источником `confirmed deals/trade result` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: Far
Размерность: `LOT_FILLED`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_FILLED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deals/trade result
Authoritative source: confirmed deals/trade result
Время фиксации: CONFIRMED stage для FarLotFilled.
Projected/Actual class: `CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: FarLotFilled: появляется при confirmed deal aggregation; дополняется последующими fills того же event; stale при incomplete history; заменяется reconciled ActualPositionLot.
Условия stale: при incomplete history.
Authoritative replacement: reconciled ActualPositionLot..
Допустимые операции: сравнение и преобразование только по `LOT_FILLED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: FarLotFilled нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Far, тип LOT_FILLED, class CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `FarLotFilled`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### FarLotActual
CanonicalName: `FarLotActual`
Русское название: Хвостовая позиция объём в лотах фактический
Краткое определение: FarLotActual — объём `Far` на стадии из текущего reconciled position/deal snapshot; он отличается от соседних lot stages источником `current MT5 position snapshot` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: Far
Размерность: `LOT_POSITION_ACTUAL`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_POSITION_ACTUAL`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: current MT5 position snapshot
Authoritative source: current MT5 position snapshot
Время фиксации: ACTUAL CURRENT stage для FarLotActual.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: FarLotActual: появляется из current position snapshot; обновляется после любого fill/close; stale сразу после trade event; заменяется новым reconciled snapshot; NOT_APPLICABLE после полного close.
Условия stale: сразу после trade event.
Authoritative replacement: новым reconciled snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_POSITION_ACTUAL` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: FarLotActual нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Far, тип LOT_POSITION_ACTUAL, class ACTUAL CURRENT.
Legacy aliases: FarLot, Ctx.farLot
MQL5 mapping: Include/BrokerMoneyModel.mqh::farLot, Include/HybridCatchUpModel.mqh::farLot
Python mapping: Tests/HybridSplitBig/test_catchup_full_dimension_contract.py::farLot, Tests/HybridSplitBig/test_catchup_temporal_model.py::farLot
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `FarLotActual`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### BigCoreLotRaw
CanonicalName: `BigCoreLotRaw`
Русское название: Компенсирующая позиция основная часть объём в лотах сырой
Краткое определение: BigCoreLotRaw — объём `BigCore` на стадии до broker normalization; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: BigCore
Размерность: `LOT_RAW`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_RAW`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для BigCoreLotRaw.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: BigCoreLotRaw: создаётся на своей pre-request стадии `PROJECTED`; invalid при изменении formula inputs/symbol constraints/fingerprint; заменяется следующим named lot stage, а не actual присваиванием.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: следующим named lot stage, а не actual присваиванием..
Допустимые операции: сравнение и преобразование только по `LOT_RAW` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: BigCoreLotRaw нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigCore, тип LOT_RAW, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `BigCoreLotRaw`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### BigCoreLotNormalized
CanonicalName: `BigCoreLotNormalized`
Русское название: Компенсирующая позиция основная часть объём в лотах нормализованный
Краткое определение: BigCoreLotNormalized — объём `BigCore` на стадии после min/max/step и profile rounding; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: BigCore
Размерность: `LOT_NORMALIZED`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_NORMALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для BigCoreLotNormalized.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: BigCoreLotNormalized: создаётся на своей pre-request стадии `PROJECTED`; invalid при изменении formula inputs/symbol constraints/fingerprint; заменяется следующим named lot stage, а не actual присваиванием.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: следующим named lot stage, а не actual присваиванием..
Допустимые операции: сравнение и преобразование только по `LOT_NORMALIZED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: BigCoreLotNormalized нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigCore, тип LOT_NORMALIZED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::bigCoreLot, Include/HybridGeometrySolver.mqh::bigCoreLot
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::core_lot, Tests/HybridSplitBig/test_catchup_temporal_model.py::core_lot
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `BigCoreLotNormalized`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### BigCoreLotRequested
CanonicalName: `BigCoreLotRequested`
Русское название: Компенсирующая позиция основная часть объём в лотах запрошенный
Краткое определение: BigCoreLotRequested — объём `BigCore` на стадии после freeze approved plan и отправки request; он отличается от соседних lot stages источником `approved immutable plan` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: BigCore
Размерность: `LOT_REQUESTED`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_REQUESTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved immutable plan
Authoritative source: approved immutable plan
Время фиксации: REQUESTED stage для BigCoreLotRequested.
Projected/Actual class: `REQUESTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: BigCoreLotRequested: создаётся при freeze ApprovedPlan; immutable внутри request; stale при fingerprint/revision mismatch; заменяется FilledLot из confirmed deals.
Условия stale: при fingerprint/revision mismatch.
Authoritative replacement: FilledLot из confirmed deals..
Допустимые операции: сравнение и преобразование только по `LOT_REQUESTED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: BigCoreLotRequested нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigCore, тип LOT_REQUESTED, class REQUESTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `BigCoreLotRequested`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### BigCoreLotFilled
CanonicalName: `BigCoreLotFilled`
Русское название: Компенсирующая позиция основная часть объём в лотах исполненный
Краткое определение: BigCoreLotFilled — объём `BigCore` на стадии после aggregation подтверждённых deals; он отличается от соседних lot stages источником `confirmed deals/trade result` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: BigCore
Размерность: `LOT_FILLED`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_FILLED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deals/trade result
Authoritative source: confirmed deals/trade result
Время фиксации: CONFIRMED stage для BigCoreLotFilled.
Projected/Actual class: `CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: BigCoreLotFilled: появляется при confirmed deal aggregation; дополняется последующими fills того же event; stale при incomplete history; заменяется reconciled ActualPositionLot.
Условия stale: при incomplete history.
Authoritative replacement: reconciled ActualPositionLot..
Допустимые операции: сравнение и преобразование только по `LOT_FILLED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: BigCoreLotFilled нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigCore, тип LOT_FILLED, class CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `BigCoreLotFilled`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### BigCoreLotActual
CanonicalName: `BigCoreLotActual`
Русское название: Компенсирующая позиция основная часть объём в лотах фактический
Краткое определение: BigCoreLotActual — объём `BigCore` на стадии из текущего reconciled position/deal snapshot; он отличается от соседних lot stages источником `current MT5 position snapshot` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: BigCore
Размерность: `LOT_POSITION_ACTUAL`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_POSITION_ACTUAL`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: current MT5 position snapshot
Authoritative source: current MT5 position snapshot
Время фиксации: ACTUAL CURRENT stage для BigCoreLotActual.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: BigCoreLotActual: появляется из current position snapshot; обновляется после любого fill/close; stale сразу после trade event; заменяется новым reconciled snapshot; NOT_APPLICABLE после полного close.
Условия stale: сразу после trade event.
Authoritative replacement: новым reconciled snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_POSITION_ACTUAL` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: BigCoreLotActual нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigCore, тип LOT_POSITION_ACTUAL, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `BigCoreLotActual`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### BigTrendLotRaw
CanonicalName: `BigTrendLotRaw`
Русское название: Компенсирующая позиция трендовая часть объём в лотах сырой
Краткое определение: BigTrendLotRaw — объём `BigTrend` на стадии до broker normalization; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: BigTrend
Размерность: `LOT_RAW`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_RAW`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для BigTrendLotRaw.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: BigTrendLotRaw: создаётся на своей pre-request стадии `PROJECTED`; invalid при изменении formula inputs/symbol constraints/fingerprint; заменяется следующим named lot stage, а не actual присваиванием.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: следующим named lot stage, а не actual присваиванием..
Допустимые операции: сравнение и преобразование только по `LOT_RAW` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: BigTrendLotRaw нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigTrend, тип LOT_RAW, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `BigTrendLotRaw`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### BigTrendLotNormalized
CanonicalName: `BigTrendLotNormalized`
Русское название: Компенсирующая позиция трендовая часть объём в лотах нормализованный
Краткое определение: BigTrendLotNormalized — объём `BigTrend` на стадии после min/max/step и profile rounding; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: BigTrend
Размерность: `LOT_NORMALIZED`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_NORMALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для BigTrendLotNormalized.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: BigTrendLotNormalized: создаётся на своей pre-request стадии `PROJECTED`; invalid при изменении formula inputs/symbol constraints/fingerprint; заменяется следующим named lot stage, а не actual присваиванием.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: следующим named lot stage, а не actual присваиванием..
Допустимые операции: сравнение и преобразование только по `LOT_NORMALIZED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: BigTrendLotNormalized нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigTrend, тип LOT_NORMALIZED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::bigTrendLot, Include/HybridGeometrySolver.mqh::bigTrendLot
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::trend_lot, Tests/HybridSplitBig/test_catchup_temporal_model.py::trend_lot
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `BigTrendLotNormalized`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### SmallBaseLotRaw
CanonicalName: `SmallBaseLotRaw`
Русское название: Защитная позиция базовая объём в лотах сырой
Краткое определение: SmallBaseLotRaw — объём `SmallBase` на стадии до broker normalization; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: SmallBase
Размерность: `LOT_RAW`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_RAW`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для SmallBaseLotRaw.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: SmallBaseLotRaw: создаётся на своей pre-request стадии `PROJECTED`; invalid при изменении formula inputs/symbol constraints/fingerprint; заменяется следующим named lot stage, а не actual присваиванием.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: следующим named lot stage, а не actual присваиванием..
Допустимые операции: сравнение и преобразование только по `LOT_RAW` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: SmallBaseLotRaw нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SmallBase, тип LOT_RAW, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `SmallBaseLotRaw`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### SmallBaseLotNormalized
CanonicalName: `SmallBaseLotNormalized`
Русское название: Защитная позиция базовая объём в лотах нормализованный
Краткое определение: SmallBaseLotNormalized — объём `SmallBase` на стадии после min/max/step и profile rounding; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: SmallBase
Размерность: `LOT_NORMALIZED`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_NORMALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для SmallBaseLotNormalized.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: SmallBaseLotNormalized: создаётся на своей pre-request стадии `PROJECTED`; invalid при изменении formula inputs/symbol constraints/fingerprint; заменяется следующим named lot stage, а не actual присваиванием.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: следующим named lot stage, а не actual присваиванием..
Допустимые операции: сравнение и преобразование только по `LOT_NORMALIZED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: SmallBaseLotNormalized нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SmallBase, тип LOT_NORMALIZED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::smallBaseLot, Include/HybridGeometrySolver.mqh::smallBaseLot
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::small_lot, Tests/HybridSplitBig/test_catchup_temporal_model.py::small_lot
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `SmallBaseLotNormalized`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### PartialFarCloseLotCalculated
CanonicalName: `PartialFarCloseLotCalculated`
Русское название: Частичный хвостовая позиция закрытие объём в лотах расчётный
Краткое определение: PartialFarCloseLotCalculated — объём `PartialFarClose` на стадии после роли/formula до terminal constraints; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: PartialFarClose
Размерность: `LOT_CALCULATED`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_CALCULATED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для PartialFarCloseLotCalculated.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: PartialFarCloseLotCalculated: создаётся на своей pre-request стадии `PROJECTED`; invalid при изменении formula inputs/symbol constraints/fingerprint; заменяется следующим named lot stage, а не actual присваиванием.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: следующим named lot stage, а не actual присваиванием..
Допустимые операции: сравнение и преобразование только по `LOT_CALCULATED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: PartialFarCloseLotCalculated нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PartialFarClose, тип LOT_CALCULATED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `PartialFarCloseLotCalculated`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### PartialFarCloseLotNormalized
CanonicalName: `PartialFarCloseLotNormalized`
Русское название: Частичный хвостовая позиция закрытие объём в лотах нормализованный
Краткое определение: PartialFarCloseLotNormalized — объём `PartialFarClose` на стадии после min/max/step и profile rounding; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: PartialFarClose
Размерность: `LOT_NORMALIZED`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_NORMALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для PartialFarCloseLotNormalized.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: PartialFarCloseLotNormalized: создаётся на своей pre-request стадии `PROJECTED`; invalid при изменении formula inputs/symbol constraints/fingerprint; заменяется следующим named lot stage, а не actual присваиванием.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: следующим named lot stage, а не actual присваиванием..
Допустимые операции: сравнение и преобразование только по `LOT_NORMALIZED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: PartialFarCloseLotNormalized нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PartialFarClose, тип LOT_NORMALIZED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `PartialFarCloseLotNormalized`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### PartialFarCloseLotRequested
CanonicalName: `PartialFarCloseLotRequested`
Русское название: Частичный хвостовая позиция закрытие объём в лотах запрошенный
Краткое определение: PartialFarCloseLotRequested — объём `PartialFarClose` на стадии после freeze approved plan и отправки request; он отличается от соседних lot stages источником `approved immutable plan` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: PartialFarClose
Размерность: `LOT_REQUESTED`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_REQUESTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved immutable plan
Authoritative source: approved immutable plan
Время фиксации: REQUESTED stage для PartialFarCloseLotRequested.
Projected/Actual class: `REQUESTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: PartialFarCloseLotRequested: создаётся при freeze ApprovedPlan; immutable внутри request; stale при fingerprint/revision mismatch; заменяется FilledLot из confirmed deals.
Условия stale: при fingerprint/revision mismatch.
Authoritative replacement: FilledLot из confirmed deals..
Допустимые операции: сравнение и преобразование только по `LOT_REQUESTED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: PartialFarCloseLotRequested нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PartialFarClose, тип LOT_REQUESTED, class REQUESTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `PartialFarCloseLotRequested`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### PartialFarCloseLotFilled
CanonicalName: `PartialFarCloseLotFilled`
Русское название: Частичный хвостовая позиция закрытие объём в лотах исполненный
Краткое определение: PartialFarCloseLotFilled — объём `PartialFarClose` на стадии после aggregation подтверждённых deals; он отличается от соседних lot stages источником `confirmed deals/trade result` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: PartialFarClose
Размерность: `LOT_FILLED`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_FILLED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deals/trade result
Authoritative source: confirmed deals/trade result
Время фиксации: CONFIRMED stage для PartialFarCloseLotFilled.
Projected/Actual class: `CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: PartialFarCloseLotFilled: появляется при confirmed deal aggregation; дополняется последующими fills того же event; stale при incomplete history; заменяется reconciled ActualPositionLot.
Условия stale: при incomplete history.
Authoritative replacement: reconciled ActualPositionLot..
Допустимые операции: сравнение и преобразование только по `LOT_FILLED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: PartialFarCloseLotFilled нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PartialFarClose, тип LOT_FILLED, class CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `PartialFarCloseLotFilled`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### FarResidualProjected
CanonicalName: `FarResidualProjected`
Русское название: Хвостовая позиция остаточная прогнозный
Краткое определение: FarResidualProjected — объём `FarResidual` на стадии в read-only preview; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: FarResidual
Размерность: `LOT_RESIDUAL`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_RESIDUAL`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для FarResidualProjected.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: FarResidualProjected: создаётся на своей pre-request стадии `PROJECTED`; invalid при изменении formula inputs/symbol constraints/fingerprint; заменяется следующим named lot stage, а не actual присваиванием.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: следующим named lot stage, а не actual присваиванием..
Допустимые операции: сравнение и преобразование только по `LOT_RESIDUAL` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: FarResidualProjected нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: FarResidual, тип LOT_RESIDUAL, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `FarResidualProjected`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### FarResidualActual
CanonicalName: `FarResidualActual`
Русское название: Хвостовая позиция остаточная фактический
Краткое определение: FarResidualActual — объём `FarResidual` на стадии из текущего reconciled position/deal snapshot; он отличается от соседних lot stages источником `current MT5 position snapshot` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: FarResidual
Размерность: `LOT_POSITION_ACTUAL`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_POSITION_ACTUAL`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: current MT5 position snapshot
Authoritative source: current MT5 position snapshot
Время фиксации: ACTUAL CURRENT stage для FarResidualActual.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: FarResidualActual: появляется из current position snapshot; обновляется после любого fill/close; stale сразу после trade event; заменяется новым reconciled snapshot; NOT_APPLICABLE после полного close.
Условия stale: сразу после trade event.
Authoritative replacement: новым reconciled snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_POSITION_ACTUAL` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: FarResidualActual нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: FarResidual, тип LOT_POSITION_ACTUAL, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `FarResidualActual`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### NewFarCandidateLot
CanonicalName: `NewFarCandidateLot`
Русское название: Новая хвостовая позиция кандидат объём в лотах
Краткое определение: NewFarCandidateLot — объём `NewFar` на стадии до approval и execution; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: NewFar
Размерность: `LOT_CALCULATED`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_CALCULATED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для NewFarCandidateLot.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: NewFarCandidateLot: создаётся на своей pre-request стадии `PROJECTED`; invalid при изменении formula inputs/symbol constraints/fingerprint; заменяется следующим named lot stage, а не actual присваиванием.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: следующим named lot stage, а не actual присваиванием..
Допустимые операции: сравнение и преобразование только по `LOT_CALCULATED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: NewFarCandidateLot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: NewFar, тип LOT_CALCULATED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `HSB-DOC-CONFLICT-020`
Resolution stage: `3.1.6 / 3.1.8`
Статус определения: `UNRESOLVED_MODE_ROUTING`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `NewFarCandidateLot`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### NewFarProjectedLot
CanonicalName: `NewFarProjectedLot`
Русское название: Новая хвостовая позиция прогнозный объём в лотах
Краткое определение: NewFarProjectedLot — объём `NewFar` на стадии в read-only preview; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: NewFar
Размерность: `LOT_RAW`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_RAW`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для NewFarProjectedLot.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: NewFarProjectedLot: создаётся на своей pre-request стадии `PROJECTED`; invalid при изменении formula inputs/symbol constraints/fingerprint; заменяется следующим named lot stage, а не actual присваиванием.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: следующим named lot stage, а не actual присваиванием..
Допустимые операции: сравнение и преобразование только по `LOT_RAW` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: NewFarProjectedLot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: NewFar, тип LOT_RAW, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `HSB-DOC-CONFLICT-020`
Resolution stage: `3.1.6 / 3.1.8`
Статус определения: `UNRESOLVED_MODE_ROUTING`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `NewFarProjectedLot`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### NewFarNormalizedLot
CanonicalName: `NewFarNormalizedLot`
Русское название: Новая хвостовая позиция нормализованный объём в лотах
Краткое определение: NewFarNormalizedLot — объём `NewFar` на стадии после min/max/step и profile rounding; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: NewFar
Размерность: `LOT_NORMALIZED`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_NORMALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для NewFarNormalizedLot.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: NewFarNormalizedLot: создаётся на своей pre-request стадии `PROJECTED`; invalid при изменении formula inputs/symbol constraints/fingerprint; заменяется следующим named lot stage, а не actual присваиванием.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: следующим named lot stage, а не actual присваиванием..
Допустимые операции: сравнение и преобразование только по `LOT_NORMALIZED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: NewFarNormalizedLot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: NewFar, тип LOT_NORMALIZED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `HSB-DOC-CONFLICT-020`
Resolution stage: `3.1.6 / 3.1.8`
Статус определения: `UNRESOLVED_MODE_ROUTING`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `NewFarNormalizedLot`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### NewFarPromotedLot
CanonicalName: `NewFarPromotedLot`
Русское название: Новая хвостовая позиция назначенный объём в лотах
Краткое определение: NewFarPromotedLot — объём `NewFar` на стадии после role validation и persistence; он отличается от соседних lot stages источником `typed formula + SymbolInfo volume constraints` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: NewFar
Размерность: `LOT_NORMALIZED`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_NORMALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: PROJECTED stage для NewFarPromotedLot.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: NewFarPromotedLot: создаётся на своей pre-request стадии `PROJECTED`; invalid при изменении formula inputs/symbol constraints/fingerprint; заменяется следующим named lot stage, а не actual присваиванием.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: следующим named lot stage, а не actual присваиванием..
Допустимые операции: сравнение и преобразование только по `LOT_NORMALIZED` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: NewFarPromotedLot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: NewFar, тип LOT_NORMALIZED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `HSB-DOC-CONFLICT-020`
Resolution stage: `3.1.6 / 3.1.8`
Статус определения: `UNRESOLVED_MODE_ROUTING`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `NewFarPromotedLot`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### NewFarActualLot
CanonicalName: `NewFarActualLot`
Русское название: Новая хвостовая позиция фактический объём в лотах
Краткое определение: NewFarActualLot — объём `NewFar` на стадии из текущего reconciled position/deal snapshot; он отличается от соседних lot stages источником `current MT5 position snapshot` и не может использоваться как их evidence.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: NewFar
Размерность: `LOT_POSITION_ACTUAL`
Unit: `lot`
Знак: >=0; active position >0
Допустимый диапазон: соответствует типу `LOT_POSITION_ACTUAL`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: current MT5 position snapshot
Authoritative source: current MT5 position snapshot
Время фиксации: ACTUAL CURRENT stage для NewFarActualLot.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: NewFarActualLot: появляется из current position snapshot; обновляется после любого fill/close; stale сразу после trade event; заменяется новым reconciled snapshot; NOT_APPLICABLE после полного close.
Условия stale: сразу после trade event.
Authoritative replacement: новым reconciled snapshot.
Допустимые операции: сравнение и преобразование только по `LOT_POSITION_ACTUAL` с `VolumeToleranceLots` и explicit provenance.
Запрещённые подмены: NewFarActualLot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: NewFar, тип LOT_POSITION_ACTUAL, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `HSB-DOC-CONFLICT-020`
Resolution stage: `3.1.6 / 3.1.8`
Статус определения: `UNRESOLVED_MODE_ROUTING`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `NewFarActualLot`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### Point
CanonicalName: `Point`
Русское название: Размер пункта
Краткое определение: Point — Размер одного terminal point для конкретного Symbol (`SYMBOL_POINT`); symbol property, а не projected market price и не TickSize.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: Point
Размерность: `PRICE_POINT_SIZE`
Unit: `price per point`
Знак: strictly positive symbol property
Допустимый диапазон: соответствует типу `PRICE_POINT_SIZE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfoDouble(symbol, SYMBOL_POINT)
Authoritative source: SymbolInfoDouble(symbol, SYMBOL_POINT)
Время фиксации: SYMBOL PROPERTY stage для Point.
Projected/Actual class: `SYMBOL PROPERTY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT PROPERTY SNAPSHOT`
Lifecycle: Point: считывается при SymbolInfo property snapshot; не зависит от market tick; stale при symbol-property refresh; заменяется новым exact property snapshot.
Условия stale: при symbol-property refresh.
Authoritative replacement: новым exact property snapshot..
Допустимые операции: сравнение и преобразование только по `PRICE_POINT_SIZE` с `EXACT PROPERTY SNAPSHOT` и explicit provenance.
Запрещённые подмены: Point нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Point, тип PRICE_POINT_SIZE, class SYMBOL PROPERTY.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::point, Include/GeometryEngine.mqh::Point
Python mapping: Tests/adaptive_geometry_atr_chain_check.py::Point, Tests/small_at_far_scenario_log.py::point
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `Point`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### TickSize
CanonicalName: `TickSize`
Русское название: Тик размер
Краткое определение: TickSize — Минимальный trade tick price increment (`SYMBOL_TRADE_TICK_SIZE`); не считается равным Point без проверки symbol properties.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: TickSize
Размерность: `PRICE_TICK_SIZE`
Unit: `price per tick`
Знак: strictly positive symbol property
Допустимый диапазон: соответствует типу `PRICE_TICK_SIZE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE)
Authoritative source: SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE)
Время фиксации: SYMBOL PROPERTY stage для TickSize.
Projected/Actual class: `SYMBOL PROPERTY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT PROPERTY SNAPSHOT`
Lifecycle: TickSize: считывается при SymbolInfo property snapshot; не зависит от market tick; stale при symbol-property refresh; заменяется новым exact property snapshot.
Условия stale: при symbol-property refresh.
Authoritative replacement: новым exact property snapshot..
Допустимые операции: сравнение и преобразование только по `PRICE_TICK_SIZE` с `EXACT PROPERTY SNAPSHOT` и explicit provenance.
Запрещённые подмены: TickSize нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: TickSize, тип PRICE_TICK_SIZE, class SYMBOL PROPERTY.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::SYMBOL_TRADE_TICK_SIZE, Include/RecoveryMath.mqh::tickSize
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `TickSize`; MQL5 identifier evidence found in inspected corpus. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### TickValue
CanonicalName: `TickValue`
Русское название: Тик стоимость
Краткое определение: TickValue — symbol-bound величина `TickValue` типа `PRICE_PROJECTED`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: TickValue
Размерность: `PRICE_PROJECTED`
Unit: `price`
Знак: >0 for absolute price; delta signed
Допустимый диапазон: соответствует типу `PRICE_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: PROJECTED stage для TickValue.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: TickValue: фиксируется из named price/property inputs; stale при market or position change; replaced by fresh market/deal/property value according to class.
Условия stale: при market or position change.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `PRICE_PROJECTED` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: TickValue нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: TickValue, тип PRICE_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/RecoveryMath.mqh::tickValue, Include/SimulationEngine.mqh::tickValue
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `TickValue`; MQL5 identifier evidence found in inspected corpus. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### MarketBidPrice
CanonicalName: `MarketBidPrice`
Русское название: Рыночная Bid цена
Краткое определение: MarketBidPrice — symbol-bound величина `MarketBidPrice` типа `PRICE_BID`, получаемая из SymbolInfoDouble(symbol, SYMBOL_BID); она не является money или lot и не использует их tolerance.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: MarketBidPrice
Размерность: `PRICE_BID`
Unit: `price`
Знак: strictly positive
Допустимый диапазон: соответствует типу `PRICE_BID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfoDouble(symbol, SYMBOL_BID)
Authoritative source: SymbolInfoDouble(symbol, SYMBOL_BID)
Время фиксации: ACTUAL CURRENT stage для MarketBidPrice.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `PriceTolerance`
Lifecycle: MarketBidPrice: фиксируется из named price/property inputs; stale при market or position change; replaced by fresh market/deal/property value according to class.
Условия stale: при market or position change.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `PRICE_BID` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: MarketBidPrice нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: MarketBidPrice, тип PRICE_BID, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `MarketBidPrice`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### MarketAskPrice
CanonicalName: `MarketAskPrice`
Русское название: Рыночная Ask цена
Краткое определение: MarketAskPrice — symbol-bound величина `MarketAskPrice` типа `PRICE_ASK`, получаемая из SymbolInfoDouble(symbol, SYMBOL_ASK); она не является money или lot и не использует их tolerance.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: MarketAskPrice
Размерность: `PRICE_ASK`
Unit: `price`
Знак: strictly positive
Допустимый диапазон: соответствует типу `PRICE_ASK`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfoDouble(symbol, SYMBOL_ASK)
Authoritative source: SymbolInfoDouble(symbol, SYMBOL_ASK)
Время фиксации: ACTUAL CURRENT stage для MarketAskPrice.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `PriceTolerance`
Lifecycle: MarketAskPrice: фиксируется из named price/property inputs; stale при market or position change; replaced by fresh market/deal/property value according to class.
Условия stale: при market or position change.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `PRICE_ASK` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: MarketAskPrice нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: MarketAskPrice, тип PRICE_ASK, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `MarketAskPrice`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### PositionOpenPrice
CanonicalName: `PositionOpenPrice`
Русское название: Позиция открытие цена
Краткое определение: PositionOpenPrice — symbol-bound величина `Position` типа `PRICE_OPEN`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: Position
Размерность: `PRICE_OPEN`
Unit: `price`
Знак: >0 for absolute price; delta signed
Допустимый диапазон: соответствует типу `PRICE_OPEN`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: PROJECTED stage для PositionOpenPrice.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: PositionOpenPrice: фиксируется из named price/property inputs; stale при market or position change; replaced by fresh market/deal/property value according to class.
Условия stale: при market or position change.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `PRICE_OPEN` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: PositionOpenPrice нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Position, тип PRICE_OPEN, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/SimulationEngine.mqh::positionOpenPrice, Include/Types.mqh::positionOpenPrice
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `PositionOpenPrice`; MQL5 identifier evidence found in inspected corpus. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### TriggerPrice
CanonicalName: `TriggerPrice`
Русское название: Триггер цена
Краткое определение: TriggerPrice — symbol-bound величина `TriggerPrice` типа `PRICE_PROJECTED`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: TriggerPrice
Размерность: `PRICE_PROJECTED`
Unit: `price`
Знак: >0 for absolute price; delta signed
Допустимый диапазон: соответствует типу `PRICE_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: PROJECTED stage для TriggerPrice.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: TriggerPrice: фиксируется из named price/property inputs; stale при market or position change; replaced by fresh market/deal/property value according to class.
Условия stale: при market or position change.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `PRICE_PROJECTED` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: TriggerPrice нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: TriggerPrice, тип PRICE_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/HybridFutureSmallSolver.mqh::triggerPrice, Include/Types.mqh::triggerPrice
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `TriggerPrice`; MQL5 identifier evidence found in inspected corpus. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### TargetPrice
CanonicalName: `TargetPrice`
Русское название: Целевая цена
Краткое определение: TargetPrice — symbol-bound величина `TargetPrice` типа `PRICE_PROJECTED`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: TargetPrice
Размерность: `PRICE_PROJECTED`
Unit: `price`
Знак: >0 for absolute price; delta signed
Допустимый диапазон: соответствует типу `PRICE_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: PROJECTED stage для TargetPrice.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: TargetPrice: фиксируется из named price/property inputs; stale при market or position change; replaced by fresh market/deal/property value according to class.
Условия stale: при market or position change.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `PRICE_PROJECTED` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: TargetPrice нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: TargetPrice, тип PRICE_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `TargetPrice`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ControlPrice
CanonicalName: `ControlPrice`
Русское название: Контрольная цена
Краткое определение: ControlPrice — symbol-bound величина `ControlPrice` типа `PRICE_PROJECTED`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: ControlPrice
Размерность: `PRICE_PROJECTED`
Unit: `price`
Знак: >0 for absolute price; delta signed
Допустимый диапазон: соответствует типу `PRICE_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: PROJECTED stage для ControlPrice.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: ControlPrice: фиксируется из named price/property inputs; stale при market or position change; replaced by fresh market/deal/property value according to class.
Условия stale: при market or position change.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `PRICE_PROJECTED` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: ControlPrice нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ControlPrice, тип PRICE_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ControlPrice`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ProjectedExitPrice
CanonicalName: `ProjectedExitPrice`
Русское название: Прогнозный выход цена
Краткое определение: ProjectedExitPrice — symbol-bound величина `ProjectedExitPrice` типа `PRICE_PROJECTED`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: ProjectedExitPrice
Размерность: `PRICE_PROJECTED`
Unit: `price`
Знак: >0 for absolute price; delta signed
Допустимый диапазон: соответствует типу `PRICE_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: PROJECTED stage для ProjectedExitPrice.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: ProjectedExitPrice: фиксируется из named price/property inputs; stale при market or position change; replaced by fresh market/deal/property value according to class.
Условия stale: при market or position change.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `PRICE_PROJECTED` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: ProjectedExitPrice нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ProjectedExitPrice, тип PRICE_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ProjectedExitPrice`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ExecutedDealPrice
CanonicalName: `ExecutedDealPrice`
Русское название: Исполненная сделка цена
Краткое определение: ExecutedDealPrice — symbol-bound величина `ExecutedDealPrice` типа `PRICE_EXECUTED`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: ExecutedDealPrice
Размерность: `PRICE_EXECUTED`
Unit: `price`
Знак: >0 for absolute price; delta signed
Допустимый диапазон: соответствует типу `PRICE_EXECUTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: CONFIRMED stage для ExecutedDealPrice.
Projected/Actual class: `CONFIRMED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: ExecutedDealPrice: фиксируется из named price/property inputs; stale при market or position change; replaced by fresh market/deal/property value according to class.
Условия stale: при market or position change.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `PRICE_EXECUTED` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: ExecutedDealPrice нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ExecutedDealPrice, тип PRICE_EXECUTED, class CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ExecutedDealPrice`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### PriceDelta
CanonicalName: `PriceDelta`
Русское название: Цена дельта
Краткое определение: PriceDelta — symbol-bound величина `PriceDelta` типа `PRICE_DELTA`, получаемая из difference of two explicitly named prices; она не является money или lot и не использует их tolerance.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: PriceDelta
Размерность: `PRICE_DELTA`
Unit: `price`
Знак: signed price difference
Допустимый диапазон: соответствует типу `PRICE_DELTA`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: difference of two explicitly named prices
Authoritative source: difference of two explicitly named prices
Время фиксации: PROJECTED stage для PriceDelta.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: PriceDelta: фиксируется из named price/property inputs; stale при market or position change; replaced by fresh market/deal/property value according to class.
Условия stale: при market or position change.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `PRICE_DELTA` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: PriceDelta нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PriceDelta, тип PRICE_DELTA, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `PriceDelta`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### DistancePoints
CanonicalName: `DistancePoints`
Русское название: Расстояние пункты
Краткое определение: DistancePoints — symbol-bound величина `DistancePoints` типа `DISTANCE_POINTS`, получаемая из explicit price delta divided by SYMBOL_POINT; она не является money или lot и не использует их tolerance.
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
Lifecycle: DistancePoints: фиксируется из named price/property inputs; stale при market or position change; replaced by fresh market/deal/property value according to class.
Условия stale: при market or position change.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `DISTANCE_POINTS` с `PointTolerance` и explicit provenance.
Запрещённые подмены: DistancePoints нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: DistancePoints, тип DISTANCE_POINTS, class PROJECTED or ACTUAL MEASUREMENT.
Legacy aliases: —
MQL5 mapping: Include/HybridCatchUpModel.mqh::distancePoints
Python mapping: Tools/mql5_like_big_scenario_parameter_search.py::distance_points
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `DistancePoints`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### DistanceTicks
CanonicalName: `DistanceTicks`
Русское название: Расстояние тики
Краткое определение: DistanceTicks — symbol-bound величина `DistanceTicks` типа `DISTANCE_TICKS`, получаемая из explicit price delta divided by SYMBOL_TRADE_TICK_SIZE; она не является money или lot и не использует их tolerance.
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
Lifecycle: DistanceTicks: фиксируется из named price/property inputs; stale при market or position change; replaced by fresh market/deal/property value according to class.
Условия stale: при market or position change.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `DISTANCE_TICKS` с `PointTolerance` и explicit provenance.
Запрещённые подмены: DistanceTicks нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: DistanceTicks, тип DISTANCE_TICKS, class PROJECTED or ACTUAL MEASUREMENT.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `DistanceTicks`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### BidAwareClosePrice
CanonicalName: `BidAwareClosePrice`
Русское название: Bid учитывающая сторону рынка закрытие цена
Краткое определение: BidAwareClosePrice — symbol-bound величина `BidAwareClosePrice` типа `PRICE_BID`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: BidAwareClosePrice
Размерность: `PRICE_BID`
Unit: `price`
Знак: >0 for absolute price; delta signed
Допустимый диапазон: соответствует типу `PRICE_BID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: PROJECTED stage для BidAwareClosePrice.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: BidAwareClosePrice: фиксируется из named price/property inputs; stale при market or position change; replaced by fresh market/deal/property value according to class.
Условия stale: при market or position change.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `PRICE_BID` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: BidAwareClosePrice нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BidAwareClosePrice, тип PRICE_BID, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `BidAwareClosePrice`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### AskAwareClosePrice
CanonicalName: `AskAwareClosePrice`
Русское название: Ask учитывающая сторону рынка закрытие цена
Краткое определение: AskAwareClosePrice — symbol-bound величина `AskAwareClosePrice` типа `PRICE_ASK`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: AskAwareClosePrice
Размерность: `PRICE_ASK`
Unit: `price`
Знак: >0 for absolute price; delta signed
Допустимый диапазон: соответствует типу `PRICE_ASK`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: PROJECTED stage для AskAwareClosePrice.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: AskAwareClosePrice: фиксируется из named price/property inputs; stale при market or position change; replaced by fresh market/deal/property value according to class.
Условия stale: при market or position change.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `PRICE_ASK` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: AskAwareClosePrice нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: AskAwareClosePrice, тип PRICE_ASK, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `AskAwareClosePrice`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### FarOpenPriceActual
CanonicalName: `FarOpenPriceActual`
Русское название: Хвостовая позиция открытие цена фактический
Краткое определение: FarOpenPriceActual — symbol-bound величина `Far` типа `PRICE_OPEN`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: Far
Размерность: `PRICE_OPEN`
Unit: `price`
Знак: >0 for absolute price; delta signed
Допустимый диапазон: соответствует типу `PRICE_OPEN`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: ACTUAL CURRENT stage для FarOpenPriceActual.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: FarOpenPriceActual: фиксируется из named price/property inputs; stale при market or position change; replaced by fresh market/deal/property value according to class.
Условия stale: при market or position change.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `PRICE_OPEN` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: FarOpenPriceActual нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Far, тип PRICE_OPEN, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `FarOpenPriceActual`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### BigCoreOpenPriceActual
CanonicalName: `BigCoreOpenPriceActual`
Русское название: Компенсирующая позиция основная часть открытие цена фактический
Краткое определение: BigCoreOpenPriceActual — symbol-bound величина `BigCore` типа `PRICE_OPEN`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: BigCore
Размерность: `PRICE_OPEN`
Unit: `price`
Знак: >0 for absolute price; delta signed
Допустимый диапазон: соответствует типу `PRICE_OPEN`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: ACTUAL CURRENT stage для BigCoreOpenPriceActual.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: BigCoreOpenPriceActual: фиксируется из named price/property inputs; stale при market or position change; replaced by fresh market/deal/property value according to class.
Условия stale: при market or position change.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `PRICE_OPEN` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: BigCoreOpenPriceActual нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigCore, тип PRICE_OPEN, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `BigCoreOpenPriceActual`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### BigTrendOpenPriceActual
CanonicalName: `BigTrendOpenPriceActual`
Русское название: Компенсирующая позиция трендовая часть открытие цена фактический
Краткое определение: BigTrendOpenPriceActual — symbol-bound величина `BigTrend` типа `PRICE_OPEN`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: BigTrend
Размерность: `PRICE_OPEN`
Unit: `price`
Знак: >0 for absolute price; delta signed
Допустимый диапазон: соответствует типу `PRICE_OPEN`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: ACTUAL CURRENT stage для BigTrendOpenPriceActual.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: BigTrendOpenPriceActual: фиксируется из named price/property inputs; stale при market or position change; replaced by fresh market/deal/property value according to class.
Условия stale: при market or position change.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `PRICE_OPEN` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: BigTrendOpenPriceActual нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigTrend, тип PRICE_OPEN, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `BigTrendOpenPriceActual`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### SmallBaseOpenPriceActual
CanonicalName: `SmallBaseOpenPriceActual`
Русское название: Защитная позиция базовая открытие цена фактический
Краткое определение: SmallBaseOpenPriceActual — symbol-bound величина `SmallBase` типа `PRICE_OPEN`, получаемая из SymbolInfo tick/current position/deal properties; она не является money или lot и не использует их tolerance.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: SmallBase
Размерность: `PRICE_OPEN`
Unit: `price`
Знак: >0 for absolute price; delta signed
Допустимый диапазон: соответствует типу `PRICE_OPEN`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: ACTUAL CURRENT stage для SmallBaseOpenPriceActual.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: SmallBaseOpenPriceActual: фиксируется из named price/property inputs; stale при market or position change; replaced by fresh market/deal/property value according to class.
Условия stale: при market or position change.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `PRICE_OPEN` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: SmallBaseOpenPriceActual нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SmallBase, тип PRICE_OPEN, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `SmallBaseOpenPriceActual`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### GrossProfit
CanonicalName: `GrossProfit`
Русское название: Валовая прибыль
Краткое определение: GrossProfit — денежная величина `GrossProfit` класса `ACTUAL CONFIRMED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: GrossProfit
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: signed P/L
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для GrossProfit.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: GrossProfit: возникает только из confirmed filtered deals; фиксируется exactly-once ledger event; stale при history/identity mismatch; заменяется rebuilt reconciled ledger, не OrderCalcProfit.
Условия stale: при history/identity mismatch.
Authoritative replacement: rebuilt reconciled ledger, не OrderCalcProfit..
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: GrossProfit нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: GrossProfit, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::grossProfit, Include/HybridCatchUpModel.mqh::grossProfit
Python mapping: Tools/offline_optimizer.py::gross_profit
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `GrossProfit`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### GrossLoss
CanonicalName: `GrossLoss`
Русское название: Валовая убыток
Краткое определение: GrossLoss — денежная величина `GrossLoss` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: GrossLoss
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для GrossLoss.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: GrossLoss: возникает только из confirmed filtered deals; фиксируется exactly-once ledger event; stale при history/identity mismatch; заменяется rebuilt reconciled ledger, не OrderCalcProfit.
Условия stale: при history/identity mismatch.
Authoritative replacement: rebuilt reconciled ledger, не OrderCalcProfit..
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: GrossLoss нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: GrossLoss, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: Tools/offline_optimizer.py::gross_loss
Mapping status: MQL5=`MISSING`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `GrossLoss`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. Python identifier evidence found in inspected corpus.

### NetProfit
CanonicalName: `NetProfit`
Русское название: Чистый результат прибыль
Краткое определение: NetProfit — денежная величина `NetProfit` класса `ACTUAL CONFIRMED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: NetProfit
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: signed P/L
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для NetProfit.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: NetProfit: возникает только из confirmed filtered deals; фиксируется exactly-once ledger event; stale при history/identity mismatch; заменяется rebuilt reconciled ledger, не OrderCalcProfit.
Условия stale: при history/identity mismatch.
Authoritative replacement: rebuilt reconciled ledger, не OrderCalcProfit..
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: NetProfit нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: NetProfit, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/Logger.mqh::NetProfit, Include/RecoveryMath.mqh::netProfit
Python mapping: Tests/big_profit_split_check.py::netProfit, Tests/big_scenario_approved_net_model_check.py::NetProfit
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `NetProfit`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### LegNet
CanonicalName: `LegNet`
Русское название: Leg чистый результат
Краткое определение: LegNet — денежная величина `LegNet` класса `ACTUAL CONFIRMED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: LegNet
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: signed P/L
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для LegNet.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: LegNet: возникает только из confirmed filtered deals; фиксируется exactly-once ledger event; stale при history/identity mismatch; заменяется rebuilt reconciled ledger, не OrderCalcProfit.
Условия stale: при history/identity mismatch.
Authoritative replacement: rebuilt reconciled ledger, не OrderCalcProfit..
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: LegNet нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: LegNet, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/StateMachine.mqh::legNet
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::leg_net
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `LegNet`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### BasketNet
CanonicalName: `BasketNet`
Русское название: Корзина чистый результат
Краткое определение: BasketNet — денежная величина `BasketNet` класса `ACTUAL CONFIRMED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: BasketNet
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: signed P/L
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для BasketNet.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: BasketNet: возникает только из confirmed filtered deals; фиксируется exactly-once ledger event; stale при history/identity mismatch; заменяется rebuilt reconciled ledger, не OrderCalcProfit.
Условия stale: при history/identity mismatch.
Authoritative replacement: rebuilt reconciled ledger, не OrderCalcProfit..
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: BasketNet нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BasketNet, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/HybridGeometrySolver.mqh::basketNet
Python mapping: Tools/prove_hybrid_split_big.py::BasketNet
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `BasketNet`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### HarvestGross
CanonicalName: `HarvestGross`
Русское название: Сбор прибыли валовая
Краткое определение: HarvestGross — денежная величина `HarvestGross` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: HarvestGross
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для HarvestGross.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: HarvestGross: возникает только из confirmed filtered deals; фиксируется exactly-once ledger event; stale при history/identity mismatch; заменяется rebuilt reconciled ledger, не OrderCalcProfit.
Условия stale: при history/identity mismatch.
Authoritative replacement: rebuilt reconciled ledger, не OrderCalcProfit..
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: HarvestGross нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: HarvestGross, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `HarvestGross`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### HarvestNet
CanonicalName: `HarvestNet`
Русское название: Сбор прибыли чистый результат
Краткое определение: HarvestNet — денежная величина `HarvestNet` класса `ACTUAL CONFIRMED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: HarvestNet
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: signed P/L
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для HarvestNet.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: HarvestNet: возникает только из confirmed filtered deals; фиксируется exactly-once ledger event; stale при history/identity mismatch; заменяется rebuilt reconciled ledger, не OrderCalcProfit.
Условия stale: при history/identity mismatch.
Authoritative replacement: rebuilt reconciled ledger, не OrderCalcProfit..
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: HarvestNet нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: HarvestNet, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/HybridCatchUpModel.mqh::HarvestNet, Include/Types.mqh::harvestNet
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::harvest_net, Tests/HybridSplitBig/test_hybrid_split_big_reference.py::harvest_net
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `HarvestNet`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### SmallReverseNet
CanonicalName: `SmallReverseNet`
Русское название: Защитная позиция разворот чистый результат
Краткое определение: SmallReverseNet — денежная величина `SmallReverseNet` класса `ACTUAL CONFIRMED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: SmallReverseNet
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: signed P/L
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для SmallReverseNet.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: SmallReverseNet: возникает только из confirmed filtered deals; фиксируется exactly-once ledger event; stale при history/identity mismatch; заменяется rebuilt reconciled ledger, не OrderCalcProfit.
Условия stale: при history/identity mismatch.
Authoritative replacement: rebuilt reconciled ledger, не OrderCalcProfit..
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: SmallReverseNet нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SmallReverseNet, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/Logger.mqh::SmallReverseNet, Include/RecoveryMath.mqh::SmallReverseNet
Python mapping: Tests/recovery_reconcile_check.py::SmallReverseNet
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `HSB-DOC-CONFLICT-023`
Resolution stage: `3.1.5 / 3.1.6`
Статус определения: `UNRESOLVED_BUSINESS_POLICY`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `SmallReverseNet`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### TransitionNet
CanonicalName: `TransitionNet`
Русское название: Переход чистый результат
Краткое определение: TransitionNet — денежная величина `TransitionNet` класса `ACTUAL CONFIRMED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: TransitionNet
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: signed P/L
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для TransitionNet.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: TransitionNet: возникает только из confirmed filtered deals; фиксируется exactly-once ledger event; stale при history/identity mismatch; заменяется rebuilt reconciled ledger, не OrderCalcProfit.
Условия stale: при history/identity mismatch.
Authoritative replacement: rebuilt reconciled ledger, не OrderCalcProfit..
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: TransitionNet нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: TransitionNet, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::transitionNet, Include/HybridFutureSmallSolver.mqh::transitionNet
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::transition_net, Tests/test_hybrid_geometry.py::transition_net
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `TransitionNet`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### RealizedCyclePL
CanonicalName: `RealizedCyclePL`
Русское название: Реализованный цикл pl
Краткое определение: RealizedCyclePL — денежная величина `RealizedCyclePL` класса `ACTUAL CONFIRMED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: RealizedCyclePL
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: signed P/L
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для RealizedCyclePL.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: RealizedCyclePL: возникает только из confirmed filtered deals; фиксируется exactly-once ledger event; stale при history/identity mismatch; заменяется rebuilt reconciled ledger, не OrderCalcProfit.
Условия stale: при history/identity mismatch.
Authoritative replacement: rebuilt reconciled ledger, не OrderCalcProfit..
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: RealizedCyclePL нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RealizedCyclePL, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/HybridCatchUpModel.mqh::realizedCyclePL, Include/Types.mqh::realizedCyclePL
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `RealizedCyclePL`; MQL5 identifier evidence found in inspected corpus. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### FloatingManagedPL
CanonicalName: `FloatingManagedPL`
Русское название: Плавающий управляемая pl
Краткое определение: FloatingManagedPL — денежная величина `FloatingManagedPL` класса `ACTUAL CURRENT` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: FloatingManagedPL
Размерность: `MONEY_FLOATING`
Unit: `account money`
Знак: signed P/L
Допустимый диапазон: соответствует типу `MONEY_FLOATING`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: current position or broker-aware price model
Authoritative source: current position or broker-aware price model
Время фиксации: ACTUAL CURRENT stage для FloatingManagedPL.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: FloatingManagedPL: вычисляется для named current/projected close prices; stale на следующем market tick или position change; заменяется свежим broker-aware snapshot.
Условия stale: на следующем market tick или position change.
Authoritative replacement: свежим broker-aware snapshot..
Допустимые операции: сравнение и преобразование только по `MONEY_FLOATING` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: FloatingManagedPL нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: FloatingManagedPL, тип MONEY_FLOATING, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `FloatingManagedPL`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ProjectedFloatingPL
CanonicalName: `ProjectedFloatingPL`
Русское название: Прогнозный плавающий pl
Краткое определение: ProjectedFloatingPL — денежная величина `ProjectedFloatingPL` класса `PROJECTED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: ProjectedFloatingPL
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: signed P/L
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для ProjectedFloatingPL.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: ProjectedFloatingPL: рассчитывается для frozen snapshot через broker-aware model; stale при price/cost/revision change; после execution заменяется separately named actual money, не переименованием.
Условия stale: при price/cost/revision change.
Authoritative replacement: separately named actual money, не переименованием..
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: ProjectedFloatingPL нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ProjectedFloatingPL, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ProjectedFloatingPL`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### RecoveryPLAnalytic
CanonicalName: `RecoveryPLAnalytic`
Русское название: Восстановление pl аналитический
Краткое определение: RecoveryPLAnalytic — денежная величина `RecoveryPL` класса `PROJECTED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: RecoveryPL
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: signed P/L
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для RecoveryPLAnalytic.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: RecoveryPLAnalytic: рассчитывается для frozen snapshot через broker-aware model; stale при price/cost/revision change; после execution заменяется separately named actual money, не переименованием.
Условия stale: при price/cost/revision change.
Authoritative replacement: separately named actual money, не переименованием..
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: RecoveryPLAnalytic нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RecoveryPL, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `RecoveryPLAnalytic`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### RecoveryPLProjected
CanonicalName: `RecoveryPLProjected`
Русское название: Восстановление pl прогнозный
Краткое определение: RecoveryPLProjected — денежная величина `RecoveryPL` класса `PROJECTED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: RecoveryPL
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: signed P/L
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для RecoveryPLProjected.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: RecoveryPLProjected: рассчитывается для frozen snapshot через broker-aware model; stale при price/cost/revision change; после execution заменяется separately named actual money, не переименованием.
Условия stale: при price/cost/revision change.
Authoritative replacement: separately named actual money, не переименованием..
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: RecoveryPLProjected нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RecoveryPL, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `RecoveryPLProjected`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### RecoveryPLCloseNow
CanonicalName: `RecoveryPLCloseNow`
Русское название: Восстановление pl закрытие сейчас
Краткое определение: RecoveryPLCloseNow — Projected broker-money result немедленного закрытия managed basket: RealizedCyclePL + FloatingManagedPL − ExpectedExitCosts без повторного Reserve.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: RecoveryPL
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: signed P/L
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для RecoveryPLCloseNow.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: RecoveryPLCloseNow: рассчитывается для frozen snapshot через broker-aware model; stale при price/cost/revision change; после execution заменяется separately named actual money, не переименованием.
Условия stale: при price/cost/revision change.
Authoritative replacement: separately named actual money, не переименованием..
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: RecoveryPLCloseNow нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RecoveryPL, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `RecoveryPLCloseNow`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### RealRecoveryPL
CanonicalName: `RealRecoveryPL`
Русское название: Подтверждённый восстановление pl
Краткое определение: RealRecoveryPL — денежная величина `RealRecoveryPL` класса `ACTUAL CONFIRMED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: RealRecoveryPL
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: signed P/L
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для RealRecoveryPL.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: RealRecoveryPL: возникает только из confirmed filtered deals; фиксируется exactly-once ledger event; stale при history/identity mismatch; заменяется rebuilt reconciled ledger, не OrderCalcProfit.
Условия stale: при history/identity mismatch.
Authoritative replacement: rebuilt reconciled ledger, не OrderCalcProfit..
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: RealRecoveryPL нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RealRecoveryPL, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: realRecoveryPL
MQL5 mapping: Include/Logger.mqh::RealRecoveryPL, Include/StateMachine.mqh::RealRecoveryPL
Python mapping: Tests/closed_profit_guard_check.py::realRecoveryPL, Tests/closed_recovery_loss_state_check.py::realRecoveryPL
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `RealRecoveryPL`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### RecoverySlope
CanonicalName: `RecoverySlope`
Русское название: Восстановление наклон
Краткое определение: RecoverySlope — денежная величина `RecoverySlope` класса `PROJECTED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: RecoverySlope
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: signed P/L
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для RecoverySlope.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: RecoverySlope: рассчитывается для frozen snapshot через broker-aware model; stale при price/cost/revision change; после execution заменяется separately named actual money, не переименованием.
Условия stale: при price/cost/revision change.
Authoritative replacement: separately named actual money, не переименованием..
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: RecoverySlope нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RecoverySlope, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/HybridGeometrySolver.mqh::RecoverySlope
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::recovery_slope, Tools/hybrid_big_sequence_model.py::recovery_slope
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `RecoverySlope`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### RecoveryMonotonicity
CanonicalName: `RecoveryMonotonicity`
Русское название: Восстановление монотонность
Краткое определение: RecoveryMonotonicity — денежная величина `RecoveryMonotonicity` класса `PROJECTED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: RecoveryMonotonicity
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для RecoveryMonotonicity.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: RecoveryMonotonicity: рассчитывается для frozen snapshot через broker-aware model; stale при price/cost/revision change; после execution заменяется separately named actual money, не переименованием.
Условия stale: при price/cost/revision change.
Authoritative replacement: separately named actual money, не переименованием..
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: RecoveryMonotonicity нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RecoveryMonotonicity, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `RecoveryMonotonicity`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ExpectedExitCosts
CanonicalName: `ExpectedExitCosts`
Русское название: Ожидаемые выход расходы
Краткое определение: ExpectedExitCosts — денежная величина `ExpectedExitCosts` класса `PROJECTED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: ExpectedExitCosts
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для ExpectedExitCosts.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: ExpectedExitCosts: рассчитывается для frozen snapshot через broker-aware model; stale при price/cost/revision change; после execution заменяется separately named actual money, не переименованием.
Условия stale: при price/cost/revision change.
Authoritative replacement: separately named actual money, не переименованием..
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: ExpectedExitCosts нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ExpectedExitCosts, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ExpectedExitCosts`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### CommissionCost
CanonicalName: `CommissionCost`
Русское название: Комиссия cost
Краткое определение: CommissionCost — денежная величина `CommissionCost` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: CommissionCost
Размерность: `MONEY_COST`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_COST`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для CommissionCost.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: CommissionCost: projected variant создаётся cost model, actual variant — confirmed deal field/effect; stale при stage mismatch; replacement обязан сохранять отдельное имя Actual/Expected.
Условия stale: при stage mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MONEY_COST` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: CommissionCost нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CommissionCost, тип MONEY_COST, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `CommissionCost`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### SwapCost
CanonicalName: `SwapCost`
Русское название: Своп cost
Краткое определение: SwapCost — денежная величина `SwapCost` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: SwapCost
Размерность: `MONEY_COST`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_COST`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для SwapCost.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: SwapCost: projected variant создаётся cost model, actual variant — confirmed deal field/effect; stale при stage mismatch; replacement обязан сохранять отдельное имя Actual/Expected.
Условия stale: при stage mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MONEY_COST` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: SwapCost нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SwapCost, тип MONEY_COST, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `SwapCost`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### FeeCost
CanonicalName: `FeeCost`
Русское название: Сбор cost
Краткое определение: FeeCost — денежная величина `FeeCost` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: FeeCost
Размерность: `MONEY_COST`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_COST`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для FeeCost.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: FeeCost: projected variant создаётся cost model, actual variant — confirmed deal field/effect; stale при stage mismatch; replacement обязан сохранять отдельное имя Actual/Expected.
Условия stale: при stage mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MONEY_COST` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: FeeCost нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: FeeCost, тип MONEY_COST, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `FeeCost`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### SpreadCost
CanonicalName: `SpreadCost`
Русское название: Спред cost
Краткое определение: SpreadCost — денежная величина `SpreadCost` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: SpreadCost
Размерность: `MONEY_COST`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_COST`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для SpreadCost.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: SpreadCost: projected variant создаётся cost model, actual variant — confirmed deal field/effect; stale при stage mismatch; replacement обязан сохранять отдельное имя Actual/Expected.
Условия stale: при stage mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MONEY_COST` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: SpreadCost нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SpreadCost, тип MONEY_COST, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::spreadCost, Include/Types.mqh::spreadCost
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `SpreadCost`; MQL5 identifier evidence found in inspected corpus. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### SlippageCost
CanonicalName: `SlippageCost`
Русское название: Проскальзывание cost
Краткое определение: SlippageCost — денежная величина `SlippageCost` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: SlippageCost
Размерность: `MONEY_COST`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_COST`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для SlippageCost.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: SlippageCost: projected variant создаётся cost model, actual variant — confirmed deal field/effect; stale при stage mismatch; replacement обязан сохранять отдельное имя Actual/Expected.
Условия stale: при stage mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MONEY_COST` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: SlippageCost нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SlippageCost, тип MONEY_COST, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::slippageCost, Include/HybridCatchUpModel.mqh::slippageCost
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `SlippageCost`; MQL5 identifier evidence found in inspected corpus. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### PositionPLSigned
CanonicalName: `PositionPLSigned`
Русское название: Позиция pl со знаком
Краткое определение: PositionPLSigned — денежная величина `Position` класса `ACTUAL CURRENT` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: Position
Размерность: `MONEY_FLOATING`
Unit: `account money`
Знак: signed P/L
Допустимый диапазон: соответствует типу `MONEY_FLOATING`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: current position or broker-aware price model
Authoritative source: current position or broker-aware price model
Время фиксации: ACTUAL CURRENT stage для PositionPLSigned.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: PositionPLSigned: вычисляется для named current/projected close prices; stale на следующем market tick или position change; заменяется свежим broker-aware snapshot.
Условия stale: на следующем market tick или position change.
Authoritative replacement: свежим broker-aware snapshot..
Допустимые операции: сравнение и преобразование только по `MONEY_FLOATING` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: PositionPLSigned нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Position, тип MONEY_FLOATING, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `PositionPLSigned`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### FarLossSigned
CanonicalName: `FarLossSigned`
Русское название: Хвостовая позиция убыток со знаком
Краткое определение: FarLossSigned — денежная величина `Far` класса `ACTUAL CONFIRMED` со знаком «signed P/L»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: Far
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: signed P/L
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для FarLossSigned.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: FarLossSigned: возникает только из confirmed filtered deals; фиксируется exactly-once ledger event; stale при history/identity mismatch; заменяется rebuilt reconciled ledger, не OrderCalcProfit.
Условия stale: при history/identity mismatch.
Authoritative replacement: rebuilt reconciled ledger, не OrderCalcProfit..
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: FarLossSigned нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Far, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `FarLossSigned`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### FarLossMagnitude
CanonicalName: `FarLossMagnitude`
Русское название: Хвостовая позиция убыток модуль
Краткое определение: FarLossMagnitude — денежная величина `Far` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: Far
Размерность: `MONEY_REALIZED`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_REALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для FarLossMagnitude.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: FarLossMagnitude: возникает только из confirmed filtered deals; фиксируется exactly-once ledger event; stale при history/identity mismatch; заменяется rebuilt reconciled ledger, не OrderCalcProfit.
Условия stale: при history/identity mismatch.
Authoritative replacement: rebuilt reconciled ledger, не OrderCalcProfit..
Допустимые операции: сравнение и преобразование только по `MONEY_REALIZED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: FarLossMagnitude нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Far, тип MONEY_REALIZED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `FarLossMagnitude`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### PartialFarBudgetProjected
CanonicalName: `PartialFarBudgetProjected`
Русское название: Частичный хвостовая позиция бюджет прогнозный
Краткое определение: PartialFarBudgetProjected — денежная величина `PartialFarBudgetProjected` класса `PROJECTED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: PartialFarBudgetProjected
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для PartialFarBudgetProjected.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: PartialFarBudgetProjected: рассчитывается для frozen snapshot через broker-aware model; stale при price/cost/revision change; после execution заменяется separately named actual money, не переименованием.
Условия stale: при price/cost/revision change.
Authoritative replacement: separately named actual money, не переименованием..
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: PartialFarBudgetProjected нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PartialFarBudgetProjected, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `PartialFarBudgetProjected`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### PartialFarBudgetReal
CanonicalName: `PartialFarBudgetReal`
Русское название: Частичный хвостовая позиция бюджет подтверждённый
Краткое определение: PartialFarBudgetReal — денежная величина `PartialFarBudgetReal` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: PartialFarBudgetReal
Размерность: `MONEY_RESERVED`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_RESERVED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для PartialFarBudgetReal.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: PartialFarBudgetReal: возникает из confirmed allocation/debit; меняется только idempotent ledger event; stale при ledger mismatch; восстанавливается deal-history reconciliation.
Условия stale: при ledger mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MONEY_RESERVED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: PartialFarBudgetReal нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PartialFarBudgetReal, тип MONEY_RESERVED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `PartialFarBudgetReal`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### PartialFarBudgetAvailable
CanonicalName: `PartialFarBudgetAvailable`
Русское название: Частичный хвостовая позиция бюджет доступный
Краткое определение: PartialFarBudgetAvailable — денежная величина `PartialFarBudgetAvailable` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: PartialFarBudgetAvailable
Размерность: `MONEY_AVAILABLE`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_AVAILABLE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для PartialFarBudgetAvailable.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: PartialFarBudgetAvailable: возникает из confirmed allocation/debit; меняется только idempotent ledger event; stale при ledger mismatch; восстанавливается deal-history reconciliation.
Условия stale: при ledger mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MONEY_AVAILABLE` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: PartialFarBudgetAvailable нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PartialFarBudgetAvailable, тип MONEY_AVAILABLE, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/HybridCatchUpModel.mqh::partialFarBudgetAvailable, Include/HybridPartialFarPreview.mqh::partialFarBudgetAvailable
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `PartialFarBudgetAvailable`; MQL5 identifier evidence found in inspected corpus. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### PartialFarBudgetConsumed
CanonicalName: `PartialFarBudgetConsumed`
Русское название: Частичный хвостовая позиция бюджет израсходованный
Краткое определение: PartialFarBudgetConsumed — денежная величина `PartialFarBudgetConsumed` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: PartialFarBudgetConsumed
Размерность: `MONEY_CONSUMED`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_CONSUMED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для PartialFarBudgetConsumed.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: PartialFarBudgetConsumed: возникает из confirmed allocation/debit; меняется только idempotent ledger event; stale при ledger mismatch; восстанавливается deal-history reconciliation.
Условия stale: при ledger mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MONEY_CONSUMED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: PartialFarBudgetConsumed нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PartialFarBudgetConsumed, тип MONEY_CONSUMED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `PartialFarBudgetConsumed`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### PartialFarBudgetResidual
CanonicalName: `PartialFarBudgetResidual`
Русское название: Частичный хвостовая позиция бюджет остаточная
Краткое определение: PartialFarBudgetResidual — денежная величина `PartialFarBudgetResidual` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: PartialFarBudgetResidual
Размерность: `MONEY_RESIDUAL`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_RESIDUAL`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для PartialFarBudgetResidual.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: PartialFarBudgetResidual: возникает из confirmed allocation/debit; меняется только idempotent ledger event; stale при ledger mismatch; восстанавливается deal-history reconciliation.
Условия stale: при ledger mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MONEY_RESIDUAL` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: PartialFarBudgetResidual нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PartialFarBudgetResidual, тип MONEY_RESIDUAL, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `PartialFarBudgetResidual`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### FinalReserveProjected
CanonicalName: `FinalReserveProjected`
Русское название: Финальный резерв прогнозный
Краткое определение: FinalReserveProjected — денежная величина `FinalReserveProjected` класса `PROJECTED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: FinalReserveProjected
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для FinalReserveProjected.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: FinalReserveProjected: рассчитывается для frozen snapshot через broker-aware model; stale при price/cost/revision change; после execution заменяется separately named actual money, не переименованием.
Условия stale: при price/cost/revision change.
Authoritative replacement: separately named actual money, не переименованием..
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: FinalReserveProjected нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: FinalReserveProjected, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `FinalReserveProjected`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### FinalReserveReal
CanonicalName: `FinalReserveReal`
Русское название: Финальный резерв подтверждённый
Краткое определение: FinalReserveReal — Фактически подтверждённый Reserve bucket: увеличивается exactly-once realized allocation и уменьшается confirmed consumption; projected reserve его не заменяет.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: FinalReserveReal
Размерность: `MONEY_RESERVED`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_RESERVED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для FinalReserveReal.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: FinalReserveReal: возникает из confirmed allocation/debit; меняется только idempotent ledger event; stale при ledger mismatch; восстанавливается deal-history reconciliation.
Условия stale: при ledger mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MONEY_RESERVED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: FinalReserveReal нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: FinalReserveReal, тип MONEY_RESERVED, class ACTUAL CONFIRMED.
Legacy aliases: TotalReserve, finalReserveReal
MQL5 mapping: Include/HybridCatchUpModel.mqh::finalReserveReal, Include/HybridTransitionPlanner.mqh::totalReserve
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::final_reserve_real, Tests/HybridSplitBig/test_catchup_stage12.py::finalReserveReal
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `FinalReserveReal`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### ReserveAddProjected
CanonicalName: `ReserveAddProjected`
Русское название: Резерв начисление прогнозный
Краткое определение: ReserveAddProjected — денежная величина `Reserve` класса `PROJECTED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: Reserve
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для ReserveAddProjected.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: ReserveAddProjected: рассчитывается для frozen snapshot через broker-aware model; stale при price/cost/revision change; после execution заменяется separately named actual money, не переименованием.
Условия stale: при price/cost/revision change.
Authoritative replacement: separately named actual money, не переименованием..
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: ReserveAddProjected нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Reserve, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ReserveAddProjected`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ReserveAddReal
CanonicalName: `ReserveAddReal`
Русское название: Резерв начисление подтверждённый
Краткое определение: ReserveAddReal — денежная величина `Reserve` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: Reserve
Размерность: `MONEY_RESERVED`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_RESERVED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для ReserveAddReal.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: ReserveAddReal: возникает из confirmed allocation/debit; меняется только idempotent ledger event; stale при ledger mismatch; восстанавливается deal-history reconciliation.
Условия stale: при ledger mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MONEY_RESERVED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: ReserveAddReal нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Reserve, тип MONEY_RESERVED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ReserveAddReal`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ReserveAvailable
CanonicalName: `ReserveAvailable`
Русское название: Резерв доступный
Краткое определение: ReserveAvailable — денежная величина `Reserve` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: Reserve
Размерность: `MONEY_AVAILABLE`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_AVAILABLE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для ReserveAvailable.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: ReserveAvailable: возникает из confirmed allocation/debit; меняется только idempotent ledger event; stale при ledger mismatch; восстанавливается deal-history reconciliation.
Условия stale: при ledger mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MONEY_AVAILABLE` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: ReserveAvailable нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Reserve, тип MONEY_AVAILABLE, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::reserveAvailable, Include/HybridTransitionPlanner.mqh::totalReserve
Python mapping: Tests/bigharvest_real_reserve_check.py::totalReserve, Tests/final_close_recovery_projection_check.py::totalReserve
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ReserveAvailable`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### ReserveConsumed
CanonicalName: `ReserveConsumed`
Русское название: Резерв израсходованный
Краткое определение: ReserveConsumed — денежная величина `Reserve` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: Reserve
Размерность: `MONEY_CONSUMED`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_CONSUMED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для ReserveConsumed.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: ReserveConsumed: возникает из confirmed allocation/debit; меняется только idempotent ledger event; stale при ledger mismatch; восстанавливается deal-history reconciliation.
Условия stale: при ledger mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MONEY_CONSUMED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: ReserveConsumed нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Reserve, тип MONEY_CONSUMED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ReserveConsumed`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ReserveResidual
CanonicalName: `ReserveResidual`
Русское название: Резерв остаточная
Краткое определение: ReserveResidual — денежная величина `Reserve` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: Reserve
Размерность: `MONEY_RESIDUAL`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_RESIDUAL`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для ReserveResidual.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: ReserveResidual: возникает из confirmed allocation/debit; меняется только idempotent ledger event; stale при ledger mismatch; восстанавливается deal-history reconciliation.
Условия stale: при ledger mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MONEY_RESIDUAL` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: ReserveResidual нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Reserve, тип MONEY_RESIDUAL, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ReserveResidual`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### CarryAvailable
CanonicalName: `CarryAvailable`
Русское название: Переносимый остаток доступный
Краткое определение: CarryAvailable — денежная величина `Carry` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: Carry
Размерность: `MONEY_AVAILABLE`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_AVAILABLE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для CarryAvailable.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: CarryAvailable: возникает из confirmed allocation/debit; меняется только idempotent ledger event; stale при ledger mismatch; восстанавливается deal-history reconciliation.
Условия stale: при ledger mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MONEY_AVAILABLE` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: CarryAvailable нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Carry, тип MONEY_AVAILABLE, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/HybridCatchUpModel.mqh::carryAvailable, Include/Types.mqh::carryAvailable
Python mapping: Tests/HybridSplitBig/test_catchup_stage12.py::carryAvailable
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `CarryAvailable`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### CarryConsumed
CanonicalName: `CarryConsumed`
Русское название: Переносимый остаток израсходованный
Краткое определение: CarryConsumed — денежная величина `Carry` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: Carry
Размерность: `MONEY_CONSUMED`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_CONSUMED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для CarryConsumed.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: CarryConsumed: возникает из confirmed allocation/debit; меняется только idempotent ledger event; stale при ledger mismatch; восстанавливается deal-history reconciliation.
Условия stale: при ledger mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MONEY_CONSUMED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: CarryConsumed нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Carry, тип MONEY_CONSUMED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `CarryConsumed`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### CarryResidual
CanonicalName: `CarryResidual`
Русское название: Переносимый остаток остаточная
Краткое определение: CarryResidual — денежная величина `Carry` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: Carry
Размерность: `MONEY_RESIDUAL`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_RESIDUAL`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для CarryResidual.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: CarryResidual: возникает из confirmed allocation/debit; меняется только idempotent ledger event; stale при ledger mismatch; восстанавливается deal-history reconciliation.
Условия stale: при ledger mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MONEY_RESIDUAL` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: CarryResidual нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Carry, тип MONEY_RESIDUAL, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `CarryResidual`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### TransitionBudgetAvailable
CanonicalName: `TransitionBudgetAvailable`
Русское название: Переход бюджет доступный
Краткое определение: TransitionBudgetAvailable — денежная величина `TransitionBudget` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: TransitionBudget
Размерность: `MONEY_AVAILABLE`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_AVAILABLE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для TransitionBudgetAvailable.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: TransitionBudgetAvailable: возникает из confirmed allocation/debit; меняется только idempotent ledger event; stale при ledger mismatch; восстанавливается deal-history reconciliation.
Условия stale: при ledger mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MONEY_AVAILABLE` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: TransitionBudgetAvailable нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: TransitionBudget, тип MONEY_AVAILABLE, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `TransitionBudgetAvailable`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### FinalCloseRequirement
CanonicalName: `FinalCloseRequirement`
Русское название: Финальный закрытие требование
Краткое определение: FinalCloseRequirement — денежная величина `FinalCloseRequirement` класса `ACTUAL CONFIRMED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: FinalCloseRequirement
Размерность: `MONEY_RESERVED`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_RESERVED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: ACTUAL CONFIRMED stage для FinalCloseRequirement.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: FinalCloseRequirement: возникает из confirmed allocation/debit; меняется только idempotent ledger event; stale при ledger mismatch; восстанавливается deal-history reconciliation.
Условия stale: при ledger mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MONEY_RESERVED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: FinalCloseRequirement нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: FinalCloseRequirement, тип MONEY_RESERVED, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `FinalCloseRequirement`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### BasketRiskMoney
CanonicalName: `BasketRiskMoney`
Русское название: Корзина риск денежный
Краткое определение: BasketRiskMoney — денежная величина `BasketRiskMoney` класса `PROJECTED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: BasketRiskMoney
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для BasketRiskMoney.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: BasketRiskMoney: рассчитывается для frozen snapshot через broker-aware model; stale при price/cost/revision change; после execution заменяется separately named actual money, не переименованием.
Условия stale: при price/cost/revision change.
Authoritative replacement: separately named actual money, не переименованием..
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: BasketRiskMoney нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BasketRiskMoney, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `BasketRiskMoney`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### AccountRiskMoney
CanonicalName: `AccountRiskMoney`
Русское название: Счёт риск денежный
Краткое определение: AccountRiskMoney — денежная величина `AccountRiskMoney` класса `PROJECTED` со знаком «non-negative magnitude/bucket»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: AccountRiskMoney
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: non-negative magnitude/bucket
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: PROJECTED stage для AccountRiskMoney.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: AccountRiskMoney: рассчитывается для frozen snapshot через broker-aware model; stale при price/cost/revision change; после execution заменяется separately named actual money, не переименованием.
Условия stale: при price/cost/revision change.
Authoritative replacement: separately named actual money, не переименованием..
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: AccountRiskMoney нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: AccountRiskMoney, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `AccountRiskMoney`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### BigRatio
CanonicalName: `BigRatio`
Русское название: Компенсирующая позиция отношение
Краткое определение: BigRatio — безразмерная величина типа `RATIO` для BigRatio; она не интерпретируется как lot, money или percent без явной conversion.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: BigRatio
Размерность: `RATIO`
Unit: `1 (dimensionless)`
Знак: non-negative; range stated per term
Допустимый диапазон: соответствует типу `RATIO`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для BigRatio.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: BigRatio: создаётся из authoritative source `approved profile or typed formula`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `RATIO` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: BigRatio нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BigRatio, тип RATIO, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Config.mqh::BigRatio, Include/RecoveryMath.mqh::BigRatio
Python mapping: Tests/big_scenario_20_80_vs_90_10_check.py::big_ratio, Tests/big_scenario_90_10_split_check.py::big_ratio
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `HSB-DOC-CONFLICT-001`
Resolution stage: `3.1.7`
Статус определения: `UNRESOLVED_PARAMETER_PROFILE`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `BigRatio`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### SmallRatio
CanonicalName: `SmallRatio`
Русское название: Защитная позиция отношение
Краткое определение: SmallRatio — безразмерная величина типа `RATIO` для SmallRatio; она не интерпретируется как lot, money или percent без явной conversion.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: SmallRatio
Размерность: `RATIO`
Unit: `1 (dimensionless)`
Знак: non-negative; range stated per term
Допустимый диапазон: соответствует типу `RATIO`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для SmallRatio.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: SmallRatio: создаётся из authoritative source `approved profile or typed formula`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `RATIO` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: SmallRatio нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SmallRatio, тип RATIO, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Config.mqh::SmallRatio
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::small_ratio, Tests/big_scenario_20_80_vs_90_10_check.py::small_ratio
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `HSB-DOC-CONFLICT-002`
Resolution stage: `3.1.7`
Статус определения: `UNRESOLVED_PARAMETER_PROFILE`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `SmallRatio`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### CloseBigOnSmallShare
CanonicalName: `CloseBigOnSmallShare`
Русское название: Закрытие компенсирующая позиция on защитная позиция доля
Краткое определение: CloseBigOnSmallShare — безразмерная величина типа `SHARE` для CloseBigOnSmallShare; она не интерпретируется как lot, money или percent без явной conversion.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: CloseBigOnSmallShare
Размерность: `SHARE`
Unit: `1 (dimensionless)`
Знак: non-negative; range stated per term
Допустимый диапазон: соответствует типу `SHARE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для CloseBigOnSmallShare.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: CloseBigOnSmallShare: создаётся из authoritative source `approved profile or typed formula`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `SHARE` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: CloseBigOnSmallShare нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CloseBigOnSmallShare, тип SHARE, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `HSB-DOC-CONFLICT-003`
Resolution stage: `3.1.7`
Статус определения: `UNRESOLVED_PARAMETER_PROFILE`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `CloseBigOnSmallShare`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### RemainBigOnSmallShare
CanonicalName: `RemainBigOnSmallShare`
Русское название: Remain компенсирующая позиция on защитная позиция доля
Краткое определение: RemainBigOnSmallShare — безразмерная величина типа `SHARE` для RemainBigOnSmallShare; она не интерпретируется как lot, money или percent без явной conversion.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: RemainBigOnSmallShare
Размерность: `SHARE`
Unit: `1 (dimensionless)`
Знак: non-negative; range stated per term
Допустимый диапазон: соответствует типу `SHARE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для RemainBigOnSmallShare.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: RemainBigOnSmallShare: создаётся из authoritative source `approved profile or typed formula`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `SHARE` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: RemainBigOnSmallShare нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RemainBigOnSmallShare, тип SHARE, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `HSB-DOC-CONFLICT-004`
Resolution stage: `3.1.7`
Статус определения: `UNRESOLVED_PARAMETER_PROFILE`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `RemainBigOnSmallShare`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### CloseFarShare
CanonicalName: `CloseFarShare`
Русское название: Закрытие хвостовая позиция доля
Краткое определение: CloseFarShare — безразмерная величина типа `SHARE` для CloseFarShare; она не интерпретируется как lot, money или percent без явной conversion.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: CloseFarShare
Размерность: `SHARE`
Unit: `1 (dimensionless)`
Знак: non-negative; range stated per term
Допустимый диапазон: соответствует типу `SHARE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для CloseFarShare.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: CloseFarShare: создаётся из authoritative source `approved profile or typed formula`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `SHARE` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: CloseFarShare нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CloseFarShare, тип SHARE, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Config.mqh::CloseFarShare, Include/StateMachine.mqh::CloseFarShare
Python mapping: Tests/big_monetary_recovery_model_check.py::CloseFarShare, Tests/big_profit_split_check.py::CloseFarShare
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `HSB-DOC-CONFLICT-005`
Resolution stage: `3.1.7`
Статус определения: `UNRESOLVED_PARAMETER_PROFILE`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `CloseFarShare`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### ReserveShare
CanonicalName: `ReserveShare`
Русское название: Резерв доля
Краткое определение: ReserveShare — безразмерная величина типа `SHARE` для Reserve; она не интерпретируется как lot, money или percent без явной conversion.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: Reserve
Размерность: `SHARE`
Unit: `1 (dimensionless)`
Знак: non-negative; range stated per term
Допустимый диапазон: соответствует типу `SHARE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для ReserveShare.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: ReserveShare: создаётся из authoritative source `approved profile or typed formula`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `SHARE` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: ReserveShare нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Reserve, тип SHARE, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Config.mqh::ReserveShare, Include/RecoveryMath.mqh::ReserveShare
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::reserve_share, Tests/big_monetary_recovery_model_check.py::ReserveShare
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `HSB-DOC-CONFLICT-006`
Resolution stage: `3.1.7`
Статус определения: `UNRESOLVED_PARAMETER_PROFILE`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ReserveShare`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### SmallReserveShare
CanonicalName: `SmallReserveShare`
Русское название: Защитная позиция резерв доля
Краткое определение: SmallReserveShare — безразмерная величина типа `SHARE` для SmallReserveShare; она не интерпретируется как lot, money или percent без явной conversion.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: SmallReserveShare
Размерность: `SHARE`
Unit: `1 (dimensionless)`
Знак: non-negative; range stated per term
Допустимый диапазон: соответствует типу `SHARE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для SmallReserveShare.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: SmallReserveShare: создаётся из authoritative source `approved profile or typed formula`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `SHARE` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: SmallReserveShare нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SmallReserveShare, тип SHARE, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Config.mqh::SmallReserveShare, Include/StateMachine.mqh::SmallReserveShare
Python mapping: Tests/default_parameters_v241_check.py::SmallReserveShare, Tests/validate_v2_static.py::SmallReserveShare
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `SmallReserveShare`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### CompressionRatio
CanonicalName: `CompressionRatio`
Русское название: Сжатие отношение
Краткое определение: CompressionRatio — безразмерная величина типа `RATIO` для CompressionRatio; она не интерпретируется как lot, money или percent без явной conversion.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: CompressionRatio
Размерность: `RATIO`
Unit: `1 (dimensionless)`
Знак: non-negative; range stated per term
Допустимый диапазон: соответствует типу `RATIO`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для CompressionRatio.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: CompressionRatio: создаётся из authoritative source `approved profile or typed formula`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `RATIO` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: CompressionRatio нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CompressionRatio, тип RATIO, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::compressionRatio
Python mapping: Tools/offline_optimizer.py::CompressionRatio
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `CompressionRatio`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### ReserveCoverageRatio
CanonicalName: `ReserveCoverageRatio`
Русское название: Резерв покрытие отношение
Краткое определение: ReserveCoverageRatio — безразмерная величина типа `RATIO` для Reserve; она не интерпретируется как lot, money или percent без явной conversion.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: Reserve
Размерность: `RATIO`
Unit: `1 (dimensionless)`
Знак: non-negative; range stated per term
Допустимый диапазон: соответствует типу `RATIO`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для ReserveCoverageRatio.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: ReserveCoverageRatio: создаётся из authoritative source `approved profile or typed formula`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `RATIO` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: ReserveCoverageRatio нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Reserve, тип RATIO, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ReserveCoverageRatio`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### RecoveryCoverageRatio
CanonicalName: `RecoveryCoverageRatio`
Русское название: Восстановление покрытие отношение
Краткое определение: RecoveryCoverageRatio — безразмерная величина типа `RATIO` для RecoveryCoverageRatio; она не интерпретируется как lot, money или percent без явной conversion.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: RecoveryCoverageRatio
Размерность: `RATIO`
Unit: `1 (dimensionless)`
Знак: non-negative; range stated per term
Допустимый диапазон: соответствует типу `RATIO`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для RecoveryCoverageRatio.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: RecoveryCoverageRatio: создаётся из authoritative source `approved profile or typed formula`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `RATIO` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: RecoveryCoverageRatio нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RecoveryCoverageRatio, тип RATIO, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `RecoveryCoverageRatio`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### MaximumNewBigToOldFarRatio
CanonicalName: `MaximumNewBigToOldFarRatio`
Русское название: Максимальное новая компенсирующая позиция to предыдущая хвостовая позиция отношение
Краткое определение: MaximumNewBigToOldFarRatio — безразмерная величина типа `RATIO` для MaximumNewBigToOldFarRatio; она не интерпретируется как lot, money или percent без явной conversion.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: MaximumNewBigToOldFarRatio
Размерность: `RATIO`
Unit: `1 (dimensionless)`
Знак: non-negative; range stated per term
Допустимый диапазон: соответствует типу `RATIO`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для MaximumNewBigToOldFarRatio.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: MaximumNewBigToOldFarRatio: создаётся из authoritative source `approved profile or typed formula`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `RATIO` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: MaximumNewBigToOldFarRatio нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: MaximumNewBigToOldFarRatio, тип RATIO, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Config.mqh::MaximumNewBigToOldFarRatio, Include/HybridCatchUpModel.mqh::MaximumNewBigToOldFarRatio
Python mapping: Tools/prove_hybrid_split_big.py::MaximumNewBigToOldFarRatio
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `HSB-DOC-CONFLICT-022`
Resolution stage: `3.1.4 / 3.1.8`
Статус определения: `UNRESOLVED_BUSINESS_POLICY`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `MaximumNewBigToOldFarRatio`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### MinimumReserveCatchUpRatio
CanonicalName: `MinimumReserveCatchUpRatio`
Русское название: Минимальное резерв catch up отношение
Краткое определение: MinimumReserveCatchUpRatio — безразмерная величина типа `RATIO` для MinimumReserveCatchUpRatio; она не интерпретируется как lot, money или percent без явной conversion.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: MinimumReserveCatchUpRatio
Размерность: `RATIO`
Unit: `1 (dimensionless)`
Знак: non-negative; range stated per term
Допустимый диапазон: соответствует типу `RATIO`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для MinimumReserveCatchUpRatio.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: MinimumReserveCatchUpRatio: создаётся из authoritative source `approved profile or typed formula`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `RATIO` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: MinimumReserveCatchUpRatio нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: MinimumReserveCatchUpRatio, тип RATIO, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/Config.mqh::MinimumReserveCatchUpRatio, Include/HybridCatchUpModel.mqh::MinimumReserveCatchUpRatio
Python mapping: Tools/prove_hybrid_split_big.py::MinimumReserveCatchUpRatio
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `MinimumReserveCatchUpRatio`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### PercentValue
CanonicalName: `PercentValue`
Русское название: Процент стоимость
Краткое определение: PercentValue — безразмерная величина типа `PERCENT` для PercentValue; она не интерпретируется как lot, money или percent без явной conversion.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: PercentValue
Размерность: `PERCENT`
Unit: `1 (dimensionless)`
Знак: non-negative; range stated per term
Допустимый диапазон: соответствует типу `PERCENT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для PercentValue.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: PercentValue: создаётся из authoritative source `approved profile or typed formula`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `PERCENT` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: PercentValue нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PercentValue, тип PERCENT, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `PercentValue`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ScaleMultiplier
CanonicalName: `ScaleMultiplier`
Русское название: Масштаб множитель
Краткое определение: ScaleMultiplier — безразмерная величина типа `MULTIPLIER` для ScaleMultiplier; она не интерпретируется как lot, money или percent без явной conversion.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: ScaleMultiplier
Размерность: `MULTIPLIER`
Unit: `1 (dimensionless)`
Знак: non-negative; range stated per term
Допустимый диапазон: соответствует типу `MULTIPLIER`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для ScaleMultiplier.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: ScaleMultiplier: создаётся из authoritative source `approved profile or typed formula`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `MULTIPLIER` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: ScaleMultiplier нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ScaleMultiplier, тип MULTIPLIER, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ScaleMultiplier`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### RiskThresholdRatio
CanonicalName: `RiskThresholdRatio`
Русское название: Риск порог отношение
Краткое определение: RiskThresholdRatio — безразмерная величина типа `RATIO` для RiskThresholdRatio; она не интерпретируется как lot, money или percent без явной conversion.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: RiskThresholdRatio
Размерность: `RATIO`
Unit: `1 (dimensionless)`
Знак: non-negative; range stated per term
Допустимый диапазон: соответствует типу `RATIO`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: POLICY/PROJECTED stage для RiskThresholdRatio.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: RiskThresholdRatio: создаётся из authoritative source `approved profile or typed formula`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `RATIO` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: RiskThresholdRatio нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RiskThresholdRatio, тип RATIO, class POLICY/PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `RiskThresholdRatio`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### SymbolId
CanonicalName: `SymbolId`
Русское название: Символ идентификатор
Краткое определение: SymbolId — identity-сущность типа `SYMBOL_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: SymbolId
Размерность: `SYMBOL_ID`
Unit: `integer/string identity`
Знак: non-zero/valid in active scope
Допустимый диапазон: соответствует типу `SYMBOL_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для SymbolId.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: SymbolId: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `SYMBOL_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: SymbolId нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: SymbolId, тип SYMBOL_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `SymbolId`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### MagicId
CanonicalName: `MagicId`
Русское название: Магический номер идентификатор
Краткое определение: MagicId — identity-сущность типа `MAGIC_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: MagicId
Размерность: `MAGIC_ID`
Unit: `integer/string identity`
Знак: non-zero/valid in active scope
Допустимый диапазон: соответствует типу `MAGIC_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для MagicId.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: MagicId: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MAGIC_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: MagicId нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: MagicId, тип MAGIC_ID, class ACTUAL CONFIRMED.
Legacy aliases: MagicNumber
MQL5 mapping: Include/BrokerMoneyModel.mqh::MagicNumber, Include/Config.mqh::MagicNumber
Python mapping: Tests/big_monetary_recovery_model_check.py::MagicNumber, Tests/big_scenario_multisymbol_guard_check.py::MagicNumber
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `MagicId`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### CycleId
CanonicalName: `CycleId`
Русское название: Цикл идентификатор
Краткое определение: CycleId — Уникальный persisted identifier одного recovery cycle, неизменный до terminal completion и не переиспользуемый другим cycle.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: CycleId
Размерность: `CYCLE_ID`
Unit: `integer/string identity`
Знак: non-zero/valid in active scope
Допустимый диапазон: соответствует типу `CYCLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для CycleId.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: CycleId: создаётся один раз при cycle start; persisted и immutable до terminal close; после close архивируется и никогда не переиспользуется; restart authority — reconciliation.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `CYCLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: CycleId нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CycleId, тип CYCLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: CycleID, cycleId
MQL5 mapping: Include/HybridCatchUpModel.mqh::cycleId, Include/HybridDecisionEngine.mqh::cycleId
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::cycle_id, Tests/legacy_persistence_context_check.py::CycleId
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `CycleId`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### RoleId
CanonicalName: `RoleId`
Русское название: Роль идентификатор
Краткое определение: RoleId — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: RoleId
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: non-zero/valid in active scope
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для RoleId.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: RoleId: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: RoleId нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RoleId, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `RoleId`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### PositionIdentifier
CanonicalName: `PositionIdentifier`
Русское название: Позиция идентификатор
Краткое определение: PositionIdentifier — identity-сущность типа `POSITION_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: Position
Размерность: `POSITION_ID`
Unit: `integer/string identity`
Знак: non-zero/valid in active scope
Допустимый диапазон: соответствует типу `POSITION_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для PositionIdentifier.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: PositionIdentifier: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `POSITION_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: PositionIdentifier нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Position, тип POSITION_ID, class ACTUAL CONFIRMED.
Legacy aliases: POSITION_IDENTIFIER
MQL5 mapping: Include/PositionResolutionEngine.mqh::identifier, Include/PositionUtils.mqh::identifier
Python mapping: Tests/identifier_reconciliation_check.py::POSITION_IDENTIFIER, Tests/open_new_small_requires_big_context_check.py::identifier
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `PositionIdentifier`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### PositionTicket
CanonicalName: `PositionTicket`
Русское название: Позиция тикет
Краткое определение: PositionTicket — identity-сущность типа `POSITION_TICKET` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: Position
Размерность: `POSITION_TICKET`
Unit: `integer/string identity`
Знак: non-zero/valid in active scope
Допустимый диапазон: соответствует типу `POSITION_TICKET`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для PositionTicket.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: PositionTicket: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `POSITION_TICKET` с `EXACT` и explicit provenance.
Запрещённые подмены: PositionTicket нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Position, тип POSITION_TICKET, class ACTUAL CONFIRMED.
Legacy aliases: ticket
MQL5 mapping: Include/BrokerMoneyModel.mqh::ticket, Include/PendingContractEngine.mqh::ticket
Python mapping: Tests/open_new_small_requires_big_context_check.py::ticket, Tests/pending_close_big_contract_check.py::ticket
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `PositionTicket`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### OrderTicket
CanonicalName: `OrderTicket`
Русское название: Ордер тикет
Краткое определение: OrderTicket — identity-сущность типа `ORDER_TICKET` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: OrderTicket
Размерность: `ORDER_TICKET`
Unit: `integer/string identity`
Знак: non-zero/valid in active scope
Допустимый диапазон: соответствует типу `ORDER_TICKET`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для OrderTicket.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: OrderTicket: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ORDER_TICKET` с `EXACT` и explicit provenance.
Запрещённые подмены: OrderTicket нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: OrderTicket, тип ORDER_TICKET, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `OrderTicket`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### DealTicket
CanonicalName: `DealTicket`
Русское название: Сделка тикет
Краткое определение: DealTicket — identity-сущность типа `DEAL_TICKET` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: DealTicket
Размерность: `DEAL_TICKET`
Unit: `integer/string identity`
Знак: non-zero/valid in active scope
Допустимый диапазон: соответствует типу `DEAL_TICKET`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для DealTicket.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: DealTicket: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `DEAL_TICKET` с `EXACT` и explicit provenance.
Запрещённые подмены: DealTicket нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: DealTicket, тип DEAL_TICKET, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/ReconciliationEngine.mqh::dealTicket, Include/SimulationEngine.mqh::dealTicket
Python mapping: Tests/big_monetary_recovery_model_check.py::dealTicket, Tests/big_scenario_multisymbol_guard_check.py::dealTicket
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `DealTicket`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### EventId
CanonicalName: `EventId`
Русское название: Событие идентификатор
Краткое определение: EventId — identity-сущность типа `EVENT_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: EventId
Размерность: `EVENT_ID`
Unit: `integer/string identity`
Знак: non-zero/valid in active scope
Допустимый диапазон: соответствует типу `EVENT_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для EventId.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: EventId: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `EVENT_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: EventId нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: EventId, тип EVENT_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/StateMachine.mqh::EventId, Include/Types.mqh::eventId
Python mapping: Tests/static/test_split_architecture_static.py::EventId, Tests/unit/test_split_final_safety_model.py::event_id
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `EventId`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### EventKey
CanonicalName: `EventKey`
Русское название: Событие ключ
Краткое определение: EventKey — identity-сущность типа `EVENT_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: EventKey
Размерность: `EVENT_ID`
Unit: `integer/string identity`
Знак: non-zero/valid in active scope
Допустимый диапазон: соответствует типу `EVENT_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для EventKey.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: EventKey: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `EVENT_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: EventKey нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: EventKey, тип EVENT_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/StateMachine.mqh::EventKey, Include/Types.mqh::eventKey
Python mapping: Tests/unit/test_split_exact_persistence_model.py::event_key, Tests/unit/test_split_final_safety_model.py::event_key
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `EventKey`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### SnapshotFingerprint
CanonicalName: `SnapshotFingerprint`
Русское название: Снимок отпечаток
Краткое определение: SnapshotFingerprint — identity-сущность типа `FINGERPRINT` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: Snapshot
Размерность: `FINGERPRINT`
Unit: `integer/string identity`
Знак: non-zero/valid in active scope
Допустимый диапазон: соответствует типу `FINGERPRINT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для SnapshotFingerprint.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT HASH MATCH`
Lifecycle: SnapshotFingerprint: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `FINGERPRINT` с `EXACT HASH MATCH` и explicit provenance.
Запрещённые подмены: SnapshotFingerprint нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Snapshot, тип FINGERPRINT, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/HybridCatchUpModel.mqh::fingerprint, Include/HybridDecisionEngine.mqh::snapshotFingerprint
Python mapping: Tests/HybridSplitBig/test_catchup_dimension_safe.py::fingerprint, Tests/HybridSplitBig/test_catchup_route_state.py::fingerprint
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `SnapshotFingerprint`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### PlanFingerprint
CanonicalName: `PlanFingerprint`
Русское название: План отпечаток
Краткое определение: PlanFingerprint — identity-сущность типа `FINGERPRINT` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: Plan
Размерность: `FINGERPRINT`
Unit: `integer/string identity`
Знак: non-zero/valid in active scope
Допустимый диапазон: соответствует типу `FINGERPRINT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для PlanFingerprint.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT HASH MATCH`
Lifecycle: PlanFingerprint: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `FINGERPRINT` с `EXACT HASH MATCH` и explicit provenance.
Запрещённые подмены: PlanFingerprint нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Plan, тип FINGERPRINT, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/HybridCatchUpModel.mqh::fingerprint, Include/Types.mqh::fingerprint
Python mapping: Tests/HybridSplitBig/test_catchup_dimension_safe.py::fingerprint, Tests/HybridSplitBig/test_catchup_route_state.py::fingerprint
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `PlanFingerprint`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### PositionComment
CanonicalName: `PositionComment`
Русское название: Позиция комментарий
Краткое определение: PositionComment — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: Position
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: non-zero/valid in active scope
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для PositionComment.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: PositionComment: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: PositionComment нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Position, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `PositionComment`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### SnapshotRevision
CanonicalName: `SnapshotRevision`
Русское название: Снимок ревизия
Краткое определение: SnapshotRevision — identity-сущность типа `ROLE_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: Snapshot
Размерность: `ROLE_ID`
Unit: `integer/string identity`
Знак: non-zero/valid in active scope
Допустимый диапазон: соответствует типу `ROLE_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для SnapshotRevision.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: SnapshotRevision: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `ROLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: SnapshotRevision нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Snapshot, тип ROLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `SnapshotRevision`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### StateRevision
CanonicalName: `StateRevision`
Русское название: Состояние ревизия
Краткое определение: StateRevision — identity-сущность типа `EVENT_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: StateRevision
Размерность: `EVENT_ID`
Unit: `integer/string identity`
Знак: non-zero/valid in active scope
Допустимый диапазон: соответствует типу `EVENT_ID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: ACTUAL CONFIRMED stage для StateRevision.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT`
Lifecycle: StateRevision: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `EVENT_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: StateRevision нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: StateRevision, тип EVENT_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/HybridCatchUpModel.mqh::stateRevision, Include/Types.mqh::stateRevision
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `StateRevision`; MQL5 identifier evidence found in inspected corpus. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### State
CanonicalName: `State`
Русское название: Состояние
Краткое определение: State — typed `STATE` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
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
Lifecycle: State: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: State нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: State, тип STATE, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/GeometryEngine.mqh::State, Include/HybridCatchUpModel.mqh::state
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::state, Tests/HybridSplitBig/test_catchup_route_state.py::state
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `State`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### Phase
CanonicalName: `Phase`
Русское название: Фаза
Краткое определение: Phase — typed `PHASE` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
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
Lifecycle: Phase: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `PHASE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: Phase нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Phase, тип PHASE, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/StateIntegrityEngine.mqh::Phase, Include/StateMachine.mqh::Phase
Python mapping: Tests/phase_state_matrix_check.py::phase, Tests/unit/test_big_small_behavior.py::phase
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `Phase`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### Event
CanonicalName: `Event`
Русское название: Событие
Краткое определение: Event — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
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
Lifecycle: Event: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: Event нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Event, тип OUTCOME, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/Types.mqh::event, Tests/MQL5/BigSmallStateMachineTest.mq5::Event
Python mapping: Tests/HybridSplitBig/test_document_consistency.py::Event, Tests/historical/test_reserve_ledger_idempotency.historical.py::event
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `Event`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### Observation
CanonicalName: `Observation`
Русское название: Наблюдение
Краткое определение: Observation — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
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
Lifecycle: Observation: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: Observation нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Observation, тип OUTCOME, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `Observation`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### GateResult
CanonicalName: `GateResult`
Русское название: Шлюз результат
Краткое определение: GateResult — typed `GATE_RESULT` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
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
Lifecycle: GateResult: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `GATE_RESULT` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: GateResult нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: GateResult, тип GATE_RESULT, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `GateResult`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ExecutionResult
CanonicalName: `ExecutionResult`
Русское название: Исполнение результат
Краткое определение: ExecutionResult — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
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
Lifecycle: ExecutionResult: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: ExecutionResult нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ExecutionResult, тип OUTCOME, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ExecutionResult`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### Outcome
CanonicalName: `Outcome`
Русское название: Исход
Краткое определение: Outcome — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
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
Lifecycle: Outcome: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: Outcome нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Outcome, тип OUTCOME, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/HybridCatchUpModel.mqh::Outcome, Include/Types.mqh::outcome
Python mapping: Tests/HybridSplitBig/test_catchup_route_hardening.py::outcome, Tests/HybridSplitBig/test_catchup_route_state.py::outcome
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `Outcome`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### ReasonCode
CanonicalName: `ReasonCode`
Русское название: Причина код
Краткое определение: ReasonCode — typed `REASON_CODE` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
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
Lifecycle: ReasonCode: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `REASON_CODE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: ReasonCode нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ReasonCode, тип REASON_CODE, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/GeometryEngine.mqh::reasonCode, Include/HybridCatchUpModel.mqh::ReasonCode
Python mapping: Tests/adaptive_geometry_no_auto_manual_fallback_check.py::reasonCode, Tests/unit/test_split_recovery_order_model.py::reason_code
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ReasonCode`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### ErrorCode
CanonicalName: `ErrorCode`
Русское название: Ошибка код
Краткое определение: ErrorCode — typed `REASON_CODE` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
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
Lifecycle: ErrorCode: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `REASON_CODE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: ErrorCode нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ErrorCode, тип REASON_CODE, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/HybridDecisionEngine.mqh::errorCode, Include/Types.mqh::errorCode
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ErrorCode`; MQL5 identifier evidence found in inspected corpus. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### DiagnosticText
CanonicalName: `DiagnosticText`
Русское название: Диагностический текст
Краткое определение: DiagnosticText — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
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
Lifecycle: DiagnosticText: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: DiagnosticText нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: DiagnosticText, тип OUTCOME, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/Logger.mqh::message, Include/ReconciliationEngine.mqh::message
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `DiagnosticText`; MQL5 identifier evidence found in inspected corpus. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### CandidatePlan
CanonicalName: `CandidatePlan`
Русское название: Кандидат план
Краткое определение: CandidatePlan — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
Архитектурный профиль: Cycle lifecycle
Торговая роль: CandidatePlan
Размерность: `OUTCOME`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `OUTCOME`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: PROJECTED stage для CandidatePlan.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: CandidatePlan: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: CandidatePlan нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CandidatePlan, тип OUTCOME, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `CandidatePlan`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ApprovedImmutablePlan
CanonicalName: `ApprovedImmutablePlan`
Русское название: Утверждённый неизменяемый план
Краткое определение: ApprovedImmutablePlan — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
Архитектурный профиль: Cycle lifecycle
Торговая роль: ApprovedImmutablePlan
Размерность: `OUTCOME`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `OUTCOME`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: PROJECTED stage для ApprovedImmutablePlan.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: ApprovedImmutablePlan: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: ApprovedImmutablePlan нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ApprovedImmutablePlan, тип OUTCOME, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ApprovedImmutablePlan`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ExecutionRequest
CanonicalName: `ExecutionRequest`
Русское название: Исполнение запрос
Краткое определение: ExecutionRequest — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
Архитектурный профиль: Cycle lifecycle
Торговая роль: ExecutionRequest
Размерность: `OUTCOME`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `OUTCOME`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: ACTUAL/CONFIRMED stage для ExecutionRequest.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: ExecutionRequest: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: ExecutionRequest нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ExecutionRequest, тип OUTCOME, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ExecutionRequest`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### BrokerExecutionResult
CanonicalName: `BrokerExecutionResult`
Русское название: Брокерский исполнение результат
Краткое определение: BrokerExecutionResult — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
Архитектурный профиль: Cycle lifecycle
Торговая роль: BrokerExecutionResult
Размерность: `OUTCOME`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `OUTCOME`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: ACTUAL/CONFIRMED stage для BrokerExecutionResult.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: BrokerExecutionResult: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: BrokerExecutionResult нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BrokerExecutionResult, тип OUTCOME, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `BrokerExecutionResult`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ReconciledResult
CanonicalName: `ReconciledResult`
Русское название: Сверенный результат
Краткое определение: ReconciledResult — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
Архитектурный профиль: Cycle lifecycle
Торговая роль: ReconciledResult
Размерность: `OUTCOME`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `OUTCOME`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: ACTUAL/CONFIRMED stage для ReconciledResult.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: ReconciledResult: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: ReconciledResult нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ReconciledResult, тип OUTCOME, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ReconciledResult`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### CommittedLedgerEvent
CanonicalName: `CommittedLedgerEvent`
Русское название: Зафиксированный ledger событие
Краткое определение: CommittedLedgerEvent — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
Архитектурный профиль: Cycle lifecycle
Торговая роль: CommittedLedgerEvent
Размерность: `OUTCOME`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `OUTCOME`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: ACTUAL/CONFIRMED stage для CommittedLedgerEvent.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: CommittedLedgerEvent: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: CommittedLedgerEvent нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CommittedLedgerEvent, тип OUTCOME, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `CommittedLedgerEvent`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### BaseSnapshot
CanonicalName: `BaseSnapshot`
Русское название: Базовая снимок
Краткое определение: BaseSnapshot — typed `STATE` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
Архитектурный профиль: Cycle lifecycle
Торговая роль: BaseSnapshot
Размерность: `STATE`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `STATE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: PROJECTED stage для BaseSnapshot.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: BaseSnapshot: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: BaseSnapshot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: BaseSnapshot, тип STATE, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `BaseSnapshot`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### WorstSnapshot
CanonicalName: `WorstSnapshot`
Русское название: Worst снимок
Краткое определение: WorstSnapshot — typed `STATE` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
Архитектурный профиль: Cycle lifecycle
Торговая роль: WorstSnapshot
Размерность: `STATE`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `STATE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: PROJECTED stage для WorstSnapshot.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: WorstSnapshot: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: WorstSnapshot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: WorstSnapshot, тип STATE, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `WorstSnapshot`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ActualSnapshot
CanonicalName: `ActualSnapshot`
Русское название: Фактический снимок
Краткое определение: ActualSnapshot — typed `STATE` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
Архитектурный профиль: Cycle lifecycle
Торговая роль: ActualSnapshot
Размерность: `STATE`
Unit: `enum/structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `STATE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: ACTUAL/CONFIRMED stage для ActualSnapshot.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT ENUM MATCH`
Lifecycle: ActualSnapshot: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: ActualSnapshot нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ActualSnapshot, тип STATE, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ActualSnapshot`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### SnapshotStaleFlag
CanonicalName: `SnapshotStaleFlag`
Русское название: Снимок устаревший признак
Краткое определение: SnapshotStaleFlag — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
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
Lifecycle: SnapshotStaleFlag: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: SnapshotStaleFlag нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Snapshot, тип OUTCOME, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `SnapshotStaleFlag`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### FinalClosePreview
CanonicalName: `FinalClosePreview`
Русское название: Финальный закрытие preview
Краткое определение: FinalClosePreview — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
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
Lifecycle: FinalClosePreview: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: FinalClosePreview нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: FinalClosePreview, тип OUTCOME, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `FinalClosePreview`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### FinalCloseActualSuccess
CanonicalName: `FinalCloseActualSuccess`
Русское название: Финальный закрытие фактический успех
Краткое определение: FinalCloseActualSuccess — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
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
Lifecycle: FinalCloseActualSuccess: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT ENUM MATCH` и explicit provenance.
Запрещённые подмены: FinalCloseActualSuccess нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: FinalCloseActualSuccess, тип OUTCOME, class ACTUAL/CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `FinalCloseActualSuccess`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### MoneyTolerance
CanonicalName: `MoneyTolerance`
Русское название: Денежный допуск
Краткое определение: MoneyTolerance — денежная величина `MoneyTolerance` класса `POLICY` со знаком «>=0»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Dimension-specific only
Торговая роль: MoneyTolerance
Размерность: `MONEY_AVAILABLE`
Unit: `same unit as compared operands`
Знак: >=0
Допустимый диапазон: соответствует типу `MONEY_AVAILABLE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved config/symbol properties
Authoritative source: approved config/symbol properties
Время фиксации: POLICY stage для MoneyTolerance.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `self`
Lifecycle: MoneyTolerance: возникает из confirmed allocation/debit; меняется только idempotent ledger event; stale при ledger mismatch; восстанавливается deal-history reconciliation.
Условия stale: при ledger mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MONEY_AVAILABLE` с `self` и explicit provenance.
Запрещённые подмены: MoneyTolerance нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: MoneyTolerance, тип MONEY_AVAILABLE, class POLICY.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `MoneyTolerance`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### VolumeToleranceLots
CanonicalName: `VolumeToleranceLots`
Русское название: Объём допуск lots
Краткое определение: VolumeToleranceLots — объём `VolumeToleranceLots` на стадии явно указанного lot lifecycle; он отличается от соседних lot stages источником `approved config/symbol properties` и не может использоваться как их evidence.
Архитектурный профиль: Dimension-specific only
Торговая роль: VolumeToleranceLots
Размерность: `LOT_NORMALIZED`
Unit: `same unit as compared operands`
Знак: >=0
Допустимый диапазон: соответствует типу `LOT_NORMALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved config/symbol properties
Authoritative source: approved config/symbol properties
Время фиксации: POLICY stage для VolumeToleranceLots.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `self`
Lifecycle: VolumeToleranceLots: создаётся на своей pre-request стадии `POLICY`; invalid при изменении formula inputs/symbol constraints/fingerprint; заменяется следующим named lot stage, а не actual присваиванием.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: следующим named lot stage, а не actual присваиванием..
Допустимые операции: сравнение и преобразование только по `LOT_NORMALIZED` с `self` и explicit provenance.
Запрещённые подмены: VolumeToleranceLots нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: VolumeToleranceLots, тип LOT_NORMALIZED, class POLICY.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `VolumeToleranceLots`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### PriceTolerance
CanonicalName: `PriceTolerance`
Русское название: Цена допуск
Краткое определение: PriceTolerance — symbol-bound величина `PriceTolerance` типа `PRICE_PROJECTED`, получаемая из approved config/symbol properties; она не является money или lot и не использует их tolerance.
Архитектурный профиль: Dimension-specific only
Торговая роль: PriceTolerance
Размерность: `PRICE_PROJECTED`
Unit: `same unit as compared operands`
Знак: >=0
Допустимый диапазон: соответствует типу `PRICE_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved config/symbol properties
Authoritative source: approved config/symbol properties
Время фиксации: POLICY stage для PriceTolerance.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `self`
Lifecycle: PriceTolerance: фиксируется из named price/property inputs; stale при market or position change; replaced by fresh market/deal/property value according to class.
Условия stale: при market or position change.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `PRICE_PROJECTED` с `self` и explicit provenance.
Запрещённые подмены: PriceTolerance нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PriceTolerance, тип PRICE_PROJECTED, class POLICY.
Legacy aliases: —
MQL5 mapping: Include/HybridCatchUpModel.mqh::priceTolerance
Python mapping: Tests/HybridSplitBig/test_catchup_dimension_safe.py::price_tolerance
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `PriceTolerance`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### PointTolerance
CanonicalName: `PointTolerance`
Русское название: Размер пункта допуск
Краткое определение: PointTolerance — самостоятельная нормативная сущность `POINTS`: её значение возникает из `approved config/symbol properties` и отличается от связанных терминов lifecycle class `POLICY`.
Архитектурный профиль: Dimension-specific only
Торговая роль: PointTolerance
Размерность: `POINTS`
Unit: `same unit as compared operands`
Знак: >=0
Допустимый диапазон: соответствует типу `POINTS`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved config/symbol properties
Authoritative source: approved config/symbol properties
Время фиксации: POLICY stage для PointTolerance.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `self`
Lifecycle: PointTolerance: создаётся из authoritative source `approved config/symbol properties`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `POINTS` с `self` и explicit provenance.
Запрещённые подмены: PointTolerance нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PointTolerance, тип POINTS, class POLICY.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `PointTolerance`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### RatioTolerance
CanonicalName: `RatioTolerance`
Русское название: Отношение допуск
Краткое определение: RatioTolerance — безразмерная величина типа `RATIO` для RatioTolerance; она не интерпретируется как lot, money или percent без явной conversion.
Архитектурный профиль: Dimension-specific only
Торговая роль: RatioTolerance
Размерность: `RATIO`
Unit: `same unit as compared operands`
Знак: >=0
Допустимый диапазон: соответствует типу `RATIO`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved config/symbol properties
Authoritative source: approved config/symbol properties
Время фиксации: POLICY stage для RatioTolerance.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `self`
Lifecycle: RatioTolerance: создаётся из authoritative source `approved config/symbol properties`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `RATIO` с `self` и explicit provenance.
Запрещённые подмены: RatioTolerance нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RatioTolerance, тип RATIO, class POLICY.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `RatioTolerance`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ComparisonEpsilon
CanonicalName: `ComparisonEpsilon`
Русское название: Comparison epsilon
Краткое определение: ComparisonEpsilon — identity-сущность типа `FINGERPRINT` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Dimension-specific only
Торговая роль: ComparisonEpsilon
Размерность: `FINGERPRINT`
Unit: `integer/string identity`
Знак: >=0
Допустимый диапазон: соответствует типу `FINGERPRINT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved config/symbol properties
Authoritative source: approved config/symbol properties
Время фиксации: POLICY stage для ComparisonEpsilon.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT HASH MATCH`
Lifecycle: ComparisonEpsilon: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `FINGERPRINT` с `EXACT HASH MATCH` и explicit provenance.
Запрещённые подмены: ComparisonEpsilon нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ComparisonEpsilon, тип FINGERPRINT, class POLICY.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ComparisonEpsilon`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ReserveMismatchTolerance
CanonicalName: `ReserveMismatchTolerance`
Русское название: Резерв mismatch допуск
Краткое определение: ReserveMismatchTolerance — денежная величина `Reserve` класса `POLICY` со знаком «>=0»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: Dimension-specific only
Торговая роль: Reserve
Размерность: `MONEY_AVAILABLE`
Unit: `same unit as compared operands`
Знак: >=0
Допустимый диапазон: соответствует типу `MONEY_AVAILABLE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved config/symbol properties
Authoritative source: approved config/symbol properties
Время фиксации: POLICY stage для ReserveMismatchTolerance.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `self`
Lifecycle: ReserveMismatchTolerance: возникает из confirmed allocation/debit; меняется только idempotent ledger event; stale при ledger mismatch; восстанавливается deal-history reconciliation.
Условия stale: при ledger mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MONEY_AVAILABLE` с `self` и explicit provenance.
Запрещённые подмены: ReserveMismatchTolerance нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Reserve, тип MONEY_AVAILABLE, class POLICY.
Legacy aliases: —
MQL5 mapping: Include/Config.mqh::ReserveMismatchTolerance, Include/ReconciliationEngine.mqh::ReserveMismatchTolerance
Python mapping: Tests/reconciliation_soft_volume_sync_check.py::ReserveMismatchTolerance, Tests/reserve_mismatch_not_fatal_check.py::ReserveMismatchTolerance
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ReserveMismatchTolerance`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### GeometryTolerance
CanonicalName: `GeometryTolerance`
Русское название: Геометрический допуск
Краткое определение: GeometryTolerance — объём `GeometryTolerance` на стадии явно указанного lot lifecycle; он отличается от соседних lot stages источником `approved config/symbol properties` и не может использоваться как их evidence.
Архитектурный профиль: Dimension-specific only
Торговая роль: GeometryTolerance
Размерность: `LOT_NORMALIZED`
Unit: `same unit as compared operands`
Знак: >=0
Допустимый диапазон: соответствует типу `LOT_NORMALIZED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved config/symbol properties
Authoritative source: approved config/symbol properties
Время фиксации: POLICY stage для GeometryTolerance.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `self`
Lifecycle: GeometryTolerance: создаётся на своей pre-request стадии `POLICY`; invalid при изменении formula inputs/symbol constraints/fingerprint; заменяется следующим named lot stage, а не actual присваиванием.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: следующим named lot stage, а не actual присваиванием..
Допустимые операции: сравнение и преобразование только по `LOT_NORMALIZED` с `self` и explicit provenance.
Запрещённые подмены: GeometryTolerance нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: GeometryTolerance, тип LOT_NORMALIZED, class POLICY.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `GeometryTolerance`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### FingerprintTolerance
CanonicalName: `FingerprintTolerance`
Русское название: Отпечаток допуск
Краткое определение: FingerprintTolerance — identity-сущность типа `FINGERPRINT` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
Архитектурный профиль: Dimension-specific only
Торговая роль: FingerprintTolerance
Размерность: `FINGERPRINT`
Unit: `integer/string identity`
Знак: >=0
Допустимый диапазон: соответствует типу `FINGERPRINT`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved config/symbol properties
Authoritative source: approved config/symbol properties
Время фиксации: POLICY stage для FingerprintTolerance.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT HASH MATCH`
Lifecycle: FingerprintTolerance: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `FINGERPRINT` с `EXACT HASH MATCH` и explicit provenance.
Запрещённые подмены: FingerprintTolerance нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: FingerprintTolerance, тип FINGERPRINT, class POLICY.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `FingerprintTolerance`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ProjectedData
CanonicalName: `ProjectedData`
Русское название: Прогнозный данные
Краткое определение: ProjectedData — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `PROJECTED`.
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
Lifecycle: ProjectedData: создаётся из authoritative source `lifecycle transition evidence`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: ProjectedData нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ProjectedData, тип BOOLEAN_RESULT, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ProjectedData`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### RequestedData
CanonicalName: `RequestedData`
Русское название: Запрошенный данные
Краткое определение: RequestedData — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `REQUESTED`.
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
Lifecycle: RequestedData: создаётся из authoritative source `lifecycle transition evidence`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: RequestedData нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: RequestedData, тип BOOLEAN_RESULT, class REQUESTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `RequestedData`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ExecutedData
CanonicalName: `ExecutedData`
Русское название: Исполненная данные
Краткое определение: ExecutedData — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `EXECUTED`.
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
Lifecycle: ExecutedData: создаётся из authoritative source `lifecycle transition evidence`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: ExecutedData нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ExecutedData, тип BOOLEAN_RESULT, class EXECUTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ExecutedData`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ConfirmedData
CanonicalName: `ConfirmedData`
Русское название: Подтверждённые данные
Краткое определение: ConfirmedData — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `CONFIRMED`.
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
Lifecycle: ConfirmedData: создаётся из authoritative source `lifecycle transition evidence`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: ConfirmedData нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ConfirmedData, тип BOOLEAN_RESULT, class CONFIRMED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ConfirmedData`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ReconciledData
CanonicalName: `ReconciledData`
Русское название: Сверенный данные
Краткое определение: ReconciledData — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `RECONCILED`.
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
Lifecycle: ReconciledData: создаётся из authoritative source `lifecycle transition evidence`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: ReconciledData нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ReconciledData, тип BOOLEAN_RESULT, class RECONCILED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ReconciledData`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### PersistedData
CanonicalName: `PersistedData`
Русское название: Сохранённые данные
Краткое определение: PersistedData — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `PERSISTED`.
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
Lifecycle: PersistedData: создаётся из authoritative source `lifecycle transition evidence`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: PersistedData нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: PersistedData, тип BOOLEAN_RESULT, class PERSISTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `PersistedData`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### StaleData
CanonicalName: `StaleData`
Русское название: Устаревший данные
Краткое определение: StaleData — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `STALE`.
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
Lifecycle: StaleData: создаётся из authoritative source `lifecycle transition evidence`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: StaleData нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: StaleData, тип BOOLEAN_RESULT, class STALE.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `StaleData`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### InvalidData
CanonicalName: `InvalidData`
Русское название: Невалидные данные
Краткое определение: InvalidData — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `INVALID`.
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
Lifecycle: InvalidData: создаётся из authoritative source `lifecycle transition evidence`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: InvalidData нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: InvalidData, тип BOOLEAN_RESULT, class INVALID.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `InvalidData`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### NotApplicableValue
CanonicalName: `NotApplicableValue`
Русское название: Не применимо стоимость
Краткое определение: NotApplicableValue — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `NOTAPPLICABLEVALUE`.
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
Lifecycle: NotApplicableValue: создаётся из authoritative source `lifecycle transition evidence`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: NotApplicableValue нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: NotApplicableValue, тип BOOLEAN_RESULT, class NOTAPPLICABLEVALUE.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `NotApplicableValue`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### NotCalculatedValue
CanonicalName: `NotCalculatedValue`
Русское название: Не расчётный стоимость
Краткое определение: NotCalculatedValue — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `NOTCALCULATEDVALUE`.
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
Lifecycle: NotCalculatedValue: создаётся из authoritative source `lifecycle transition evidence`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: NotCalculatedValue нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: NotCalculatedValue, тип BOOLEAN_RESULT, class NOTCALCULATEDVALUE.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `NotCalculatedValue`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### NotAvailableValue
CanonicalName: `NotAvailableValue`
Русское название: Не доступный стоимость
Краткое определение: NotAvailableValue — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `NOTAVAILABLEVALUE`.
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
Lifecycle: NotAvailableValue: создаётся из authoritative source `lifecycle transition evidence`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: NotAvailableValue нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: NotAvailableValue, тип BOOLEAN_RESULT, class NOTAVAILABLEVALUE.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `NotAvailableValue`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### UnknownValue
CanonicalName: `UnknownValue`
Русское название: Неизвестное стоимость
Краткое определение: UnknownValue — самостоятельная нормативная сущность `BOOLEAN_RESULT`: её значение возникает из `lifecycle transition evidence` и отличается от связанных терминов lifecycle class `UNKNOWNVALUE`.
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
Lifecycle: UnknownValue: создаётся из authoritative source `lifecycle transition evidence`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `BOOLEAN_RESULT` с `exact state` и explicit provenance.
Запрещённые подмены: UnknownValue нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: UnknownValue, тип BOOLEAN_RESULT, class UNKNOWNVALUE.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `UnknownValue`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### CurrentBid
CanonicalName: `CurrentBid`
Русское название: текущая цена Bid
Краткое определение: CurrentBid — symbol-bound величина `CurrentBid` типа `PRICE_BID`, получаемая из SymbolInfoDouble(symbol, SYMBOL_BID); она не является money или lot и не использует их tolerance.
Архитектурный профиль: All
Торговая роль: CurrentBid
Размерность: `PRICE_BID`
Unit: `price`
Знак: non-negative
Допустимый диапазон: соответствует типу `PRICE_BID`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfoDouble(symbol, SYMBOL_BID)
Authoritative source: SymbolInfoDouble(symbol, SYMBOL_BID)
Время фиксации: ACTUAL CURRENT stage для CurrentBid.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `PriceTolerance`
Lifecycle: CurrentBid: фиксируется из named price/property inputs; stale при market or position change; replaced by fresh market/deal/property value according to class.
Условия stale: при market or position change.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `PRICE_BID` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: CurrentBid нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CurrentBid, тип PRICE_BID, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::bid, Include/HybridCatchUpModel.mqh::bid
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::bid, Tests/HybridSplitBig/test_catchup_route_hardening.py::bid
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `CurrentBid`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### CurrentAsk
CanonicalName: `CurrentAsk`
Русское название: текущая цена Ask
Краткое определение: CurrentAsk — symbol-bound величина `CurrentAsk` типа `PRICE_ASK`, получаемая из SymbolInfoDouble(symbol, SYMBOL_ASK); она не является money или lot и не использует их tolerance.
Архитектурный профиль: All
Торговая роль: CurrentAsk
Размерность: `PRICE_ASK`
Unit: `price`
Знак: non-negative
Допустимый диапазон: соответствует типу `PRICE_ASK`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: SymbolInfoDouble(symbol, SYMBOL_ASK)
Authoritative source: SymbolInfoDouble(symbol, SYMBOL_ASK)
Время фиксации: ACTUAL CURRENT stage для CurrentAsk.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `PriceTolerance`
Lifecycle: CurrentAsk: фиксируется из named price/property inputs; stale при market or position change; replaced by fresh market/deal/property value according to class.
Условия stale: при market or position change.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `PRICE_ASK` с `PriceTolerance` и explicit provenance.
Запрещённые подмены: CurrentAsk нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CurrentAsk, тип PRICE_ASK, class ACTUAL CURRENT.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::ask, Include/HybridCatchUpModel.mqh::ask
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::ask, Tests/HybridSplitBig/test_catchup_route_hardening.py::ask
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `CurrentAsk`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### ReserveProjected
CanonicalName: `ReserveProjected`
Русское название: прогнозный резерв до подтверждения
Краткое определение: ReserveProjected — денежная величина `Reserve` класса `PROJECTED` со знаком «non-negative»; она отличается от gross/projected/confirmed siblings источником и допустимостью ledger commit.
Архитектурный профиль: All
Торговая роль: Reserve
Размерность: `MONEY_PROJECTED`
Unit: `account money`
Знак: non-negative
Допустимый диапазон: соответствует типу `MONEY_PROJECTED`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: OrderCalcProfit outputs plus explicit projected allocation model
Authoritative source: OrderCalcProfit outputs plus explicit projected allocation model
Время фиксации: PROJECTED stage для ReserveProjected.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `MoneyTolerance`
Lifecycle: ReserveProjected: рассчитывается для frozen snapshot через broker-aware model; stale при price/cost/revision change; после execution заменяется separately named actual money, не переименованием.
Условия stale: при price/cost/revision change.
Authoritative replacement: separately named actual money, не переименованием..
Допустимые операции: сравнение и преобразование только по `MONEY_PROJECTED` с `MoneyTolerance` и explicit provenance.
Запрещённые подмены: ReserveProjected нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Reserve, тип MONEY_PROJECTED, class PROJECTED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ReserveProjected`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### ReserveCoverage
CanonicalName: `ReserveCoverage`
Русское название: отношение доступного резерва к требованию закрытия
Краткое определение: ReserveCoverage — безразмерная величина типа `RATIO` для Reserve; она не интерпретируется как lot, money или percent без явной conversion.
Архитектурный профиль: All
Торговая роль: Reserve
Размерность: `RATIO`
Unit: `dimensionless`
Знак: non-negative
Допустимый диапазон: соответствует типу `RATIO`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: ReserveAvailable divided by FinalCloseRequirement
Authoritative source: ReserveAvailable divided by FinalCloseRequirement
Время фиксации: PROJECTED or ACTUAL RATIO stage для ReserveCoverage.
Projected/Actual class: `PROJECTED or ACTUAL RATIO`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: ReserveCoverage: создаётся из authoritative source `ReserveAvailable divided by FinalCloseRequirement`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `RATIO` с `RatioTolerance` и explicit provenance.
Запрещённые подмены: ReserveCoverage нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Reserve, тип RATIO, class PROJECTED or ACTUAL RATIO.
Legacy aliases: —
MQL5 mapping: Include/Logger.mqh::ReserveCoverage, Include/StateMachine.mqh::ReserveCoverage
Python mapping: Tests/atr_stop_max_levels_diagnosis_check.py::ReserveCoverage, Tests/big_scenario_math_check.py::ReserveCoverage
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ReserveCoverage`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### Symbol
CanonicalName: `Symbol`
Русское название: торговый символ цикла
Краткое определение: Symbol — identity-сущность типа `SYMBOL_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
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
Lifecycle: Symbol: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `SYMBOL_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: Symbol нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Symbol, тип SYMBOL_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/GeometryEngine.mqh::Symbol, Include/HybridCatchUpModel.mqh::symbol
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::symbol, Tests/HybridSplitBig/test_catchup_full_dimension_contract.py::symbol
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `Symbol`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### MagicNumber
CanonicalName: `MagicNumber`
Русское название: магический номер стратегии
Краткое определение: MagicNumber — identity-сущность типа `MAGIC_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
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
Lifecycle: MagicNumber: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `MAGIC_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: MagicNumber нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: MagicNumber, тип MAGIC_ID, class POLICY/ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/BrokerMoneyModel.mqh::MagicNumber, Include/Config.mqh::MagicNumber
Python mapping: Tests/big_monetary_recovery_model_check.py::MagicNumber, Tests/big_scenario_multisymbol_guard_check.py::MagicNumber
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `MagicNumber`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### CycleID
CanonicalName: `CycleID`
Русское название: идентификатор recovery-цикла
Краткое определение: CycleID — Canonical alias spelling идентификатора recovery cycle; семантически совпадает с CycleId и не заменяет position/deal identity.
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
Lifecycle: CycleID: создаётся один раз при cycle start; persisted и immutable до terminal close; после close архивируется и никогда не переиспользуется; restart authority — reconciliation.
Условия stale: при изменении authoritative inputs или revision.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `CYCLE_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: CycleID нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: CycleID, тип CYCLE_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/HybridCatchUpModel.mqh::cycleId, Include/HybridDecisionEngine.mqh::cycleId
Python mapping: Tests/legacy_persistence_context_check.py::CycleId, Tests/recover_state_position_reconcile_check.py::CycleId
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `CycleID`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### EventID
CanonicalName: `EventID`
Русское название: идентификатор ledger-события
Краткое определение: EventID — identity-сущность типа `EVENT_ID` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
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
Lifecycle: EventID: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `EVENT_ID` с `EXACT` и explicit provenance.
Запрещённые подмены: EventID нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: EventID, тип EVENT_ID, class ACTUAL CONFIRMED.
Legacy aliases: —
MQL5 mapping: Include/StateMachine.mqh::eventId, Include/Types.mqh::eventId
Python mapping: Tests/static/test_split_architecture_static.py::eventId
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `EventID`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### Fingerprint
CanonicalName: `Fingerprint`
Русское название: типизированный отпечаток snapshot или plan
Краткое определение: Fingerprint — identity-сущность типа `FINGERPRINT` для разграничения торгового объекта/цикла; она сравнивается точно и не заменяется Comment или другим ticket kind.
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
Lifecycle: Fingerprint: фиксируется при создании/получении соответствующего object; stale при lifecycle/revision mismatch; replacement допускается только confirmed terminal/reconciliation evidence.
Условия stale: при lifecycle/revision mismatch.
Authoritative replacement: reconciled value того же canonical type.
Допустимые операции: сравнение и преобразование только по `FINGERPRINT` с `EXACT HASH MATCH` и explicit provenance.
Запрещённые подмены: Fingerprint нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Fingerprint, тип FINGERPRINT, class PROJECTED or RECONCILED.
Legacy aliases: —
MQL5 mapping: Include/HybridCatchUpModel.mqh::fingerprint, Include/Types.mqh::fingerprint
Python mapping: Tests/HybridSplitBig/test_catchup_dimension_safe.py::fingerprint, Tests/HybridSplitBig/test_catchup_route_state.py::fingerprint
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `Fingerprint`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### Comment
CanonicalName: `Comment`
Русское название: комментарий торгового объекта
Краткое определение: Comment — самостоятельная нормативная сущность `DIAGNOSTIC_TEXT`: её значение возникает из `MT5 position/order/deal comment property` и отличается от связанных терминов lifecycle class `ACTUAL OBSERVATION`.
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
Lifecycle: Comment: создаётся из authoritative source `MT5 position/order/deal comment property`; stale при изменении входного scope/revision; заменяется новым значением того же canonical type после validation.
Условия stale: при изменении входного scope/revision.
Authoritative replacement: новым значением того же canonical type после validation..
Допустимые операции: сравнение и преобразование только по `DIAGNOSTIC_TEXT` с `EXACT TEXT; never identity` и explicit provenance.
Запрещённые подмены: Comment нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Comment, тип DIAGNOSTIC_TEXT, class ACTUAL OBSERVATION.
Legacy aliases: —
MQL5 mapping: Include/GeometryEngine.mqh::Comment, Include/PendingContractEngine.mqh::Comment
Python mapping: Tests/orphan_position_detection_check.py::Comment, Tests/static/test_split_architecture_static.py::comment
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `Comment`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### Preview
CanonicalName: `Preview`
Русское название: read-only предварительная оценка
Краткое определение: Preview — typed `PHASE` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
Архитектурный профиль: All
Торговая роль: Preview
Размерность: `PHASE`
Unit: `structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `PHASE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: fresh immutable snapshot evaluator
Authoritative source: fresh immutable snapshot evaluator
Время фиксации: PROJECTED stage для Preview.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT STRUCTURE`
Lifecycle: Preview: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `PHASE` с `EXACT STRUCTURE` и explicit provenance.
Запрещённые подмены: Preview нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Preview, тип PHASE, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/HybridCatchUpModel.mqh::preview, Include/HybridMarginModel.mqh::preview
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `Preview`; MQL5 identifier evidence found in inspected corpus. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

### Candidate
CanonicalName: `Candidate`
Русское название: кандидат плана до полного gate-chain
Краткое определение: Candidate — typed `OUTCOME` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
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
Lifecycle: Candidate: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `OUTCOME` с `EXACT STRUCTURE` и explicit provenance.
Запрещённые подмены: Candidate нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Candidate, тип OUTCOME, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/HybridCatchUpModel.mqh::candidate, Include/HybridPartialFarPreview.mqh::candidate
Python mapping: Tests/HybridSplitBig/hybrid_split_big_reference.py::candidate, Tests/HybridSplitBig/test_catchup_dimension_safe.py::candidate
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `Candidate`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### Plan
CanonicalName: `Plan`
Русское название: расчётный набор действий и ожиданий
Краткое определение: Plan — typed `STATE` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
Архитектурный профиль: All
Торговая роль: Plan
Размерность: `STATE`
Unit: `structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `STATE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: candidate planner output with revision
Authoritative source: candidate planner output with revision
Время фиксации: PROJECTED stage для Plan.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT STRUCTURE`
Lifecycle: Plan: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT STRUCTURE` и explicit provenance.
Запрещённые подмены: Plan нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: Plan, тип STATE, class PROJECTED.
Legacy aliases: —
MQL5 mapping: Include/HybridCatchUpModel.mqh::plan, Include/HybridMarginModel.mqh::plan
Python mapping: Tests/HybridSplitBig/test_catchup_temporal_model.py::plan, Tests/HybridSplitBig/test_document_consistency.py::plan
Mapping status: MQL5=`SEMANTIC_MATCH`; Python=`SEMANTIC_MATCH`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `Plan`; MQL5 identifier evidence found in inspected corpus. Python identifier evidence found in inspected corpus.

### ApprovedPlan
CanonicalName: `ApprovedPlan`
Русское название: неизменяемый план после всех обязательных gates
Краткое определение: ApprovedPlan — typed `STATE` lifecycle-сущность с exact comparison; она отличается от DiagnosticText и от соседних state/result namespaces.
Архитектурный профиль: All
Торговая роль: ApprovedPlan
Размерность: `STATE`
Unit: `structured record`
Знак: not numeric
Допустимый диапазон: соответствует типу `STATE`; NaN/infinity и несогласованный sentinel запрещены.
Источник возникновения: approved immutable plan and fingerprint
Authoritative source: approved immutable plan and fingerprint
Время фиксации: PROJECTED APPROVED stage для ApprovedPlan.
Projected/Actual class: `PROJECTED APPROVED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `EXACT STRUCTURE`
Lifecycle: ApprovedPlan: возникает из конкретного FSM/gate/role transition; действует до следующего typed transition; stale при state revision mismatch; заменяется новым exact enum/result.
Условия stale: при state revision mismatch.
Authoritative replacement: новым exact enum/result..
Допустимые операции: сравнение и преобразование только по `STATE` с `EXACT STRUCTURE` и explicit provenance.
Запрещённые подмены: ApprovedPlan нельзя подменять sibling lifecycle stage, другим architecture role, stale cache или одноимённым diagnostic text.
Связанные сущности: ApprovedPlan, тип STATE, class PROJECTED APPROVED.
Legacy aliases: —
MQL5 mapping: NOT_APPLICABLE
Python mapping: NOT_APPLICABLE
Mapping status: MQL5=`MISSING`; Python=`MISSING`
Conflict: `NOT_APPLICABLE`
Resolution stage: `NOT_APPLICABLE`
Статус определения: `APPROVED_TERM`
Evidence: `HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json` record `ApprovedPlan`; No isolated MQL5 identifier found in inspected project corpus; canonical term remains normative/documentation-level. No isolated Python identifier found in inspected project corpus; canonical term remains normative/documentation-level.

