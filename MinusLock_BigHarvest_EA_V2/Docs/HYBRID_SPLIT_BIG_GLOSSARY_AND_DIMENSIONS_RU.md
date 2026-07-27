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

## Расширенные records canonical terms

### Legacy
CanonicalName: `Legacy`
Русское название: Legacy
Краткое определение: типизированная сущность family `ARCHITECTURE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy
Торговая роль: ARCHITECTURE
Размерность: `STATE` / unit `architecture/role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact mode/role match`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ARCHITECTURE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ARCHITECTURE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `DOCUMENTED_NOT_APPROVED`
Conflict: `HSB-DOC-CONFLICT-031`
Resolution stage: `3.1.8`

### LegacyMode
CanonicalName: `LegacyMode`
Русское название: LegacyMode
Краткое определение: типизированная сущность family `ARCHITECTURE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy
Торговая роль: ARCHITECTURE
Размерность: `STATE` / unit `architecture/role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact mode/role match`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ARCHITECTURE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ARCHITECTURE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### LegacyBig
CanonicalName: `LegacyBig`
Русское название: LegacyBig
Краткое определение: типизированная сущность family `ARCHITECTURE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: LegacyBig
Торговая роль: ARCHITECTURE
Размерность: `ROLE_ID` / unit `architecture/role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact mode/role match`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ARCHITECTURE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ARCHITECTURE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### LegacySmall
CanonicalName: `LegacySmall`
Русское название: LegacySmall
Краткое определение: типизированная сущность family `ARCHITECTURE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: LegacySmall
Торговая роль: ARCHITECTURE
Размерность: `ROLE_ID` / unit `architecture/role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact mode/role match`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ARCHITECTURE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ARCHITECTURE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### LegacyFar
CanonicalName: `LegacyFar`
Русское название: LegacyFar
Краткое определение: типизированная сущность family `ARCHITECTURE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: LegacyFar
Торговая роль: ARCHITECTURE
Размерность: `ROLE_ID` / unit `architecture/role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact mode/role match`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ARCHITECTURE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ARCHITECTURE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### MonolithicBig
CanonicalName: `MonolithicBig`
Русское название: MonolithicBig
Краткое определение: типизированная сущность family `ARCHITECTURE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: MonolithicBig
Торговая роль: ARCHITECTURE
Размерность: `ROLE_ID` / unit `architecture/role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact mode/role match`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ARCHITECTURE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ARCHITECTURE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### Split
CanonicalName: `Split`
Русское название: Split
Краткое определение: типизированная сущность family `ARCHITECTURE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Split
Торговая роль: ARCHITECTURE
Размерность: `STATE` / unit `architecture/role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact mode/role match`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ARCHITECTURE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ARCHITECTURE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `DOCUMENTED_NOT_APPROVED`
Conflict: `HSB-DOC-CONFLICT-031`
Resolution stage: `3.1.8`

### SplitMode
CanonicalName: `SplitMode`
Русское название: SplitMode
Краткое определение: типизированная сущность family `ARCHITECTURE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Split
Торговая роль: ARCHITECTURE
Размерность: `STATE` / unit `architecture/role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact mode/role match`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ARCHITECTURE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ARCHITECTURE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### SplitBig
CanonicalName: `SplitBig`
Русское название: SplitBig
Краткое определение: типизированная сущность family `ARCHITECTURE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: SplitBig
Торговая роль: ARCHITECTURE
Размерность: `ROLE_ID` / unit `architecture/role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact mode/role match`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ARCHITECTURE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ARCHITECTURE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### BigCore
CanonicalName: `BigCore`
Русское название: BigCore
Краткое определение: типизированная сущность family `ARCHITECTURE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: BigCore
Торговая роль: ARCHITECTURE
Размерность: `ROLE_ID` / unit `architecture/role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact mode/role match`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ARCHITECTURE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ARCHITECTURE`.
Legacy aliases: Core
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### BigTrend
CanonicalName: `BigTrend`
Русское название: BigTrend
Краткое определение: типизированная сущность family `ARCHITECTURE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: BigTrend
Торговая роль: ARCHITECTURE
Размерность: `ROLE_ID` / unit `architecture/role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact mode/role match`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ARCHITECTURE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ARCHITECTURE`.
Legacy aliases: Trend
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### BigGross
CanonicalName: `BigGross`
Русское название: BigGross
Краткое определение: типизированная сущность family `ARCHITECTURE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: BigGross
Торговая роль: ARCHITECTURE
Размерность: `ROLE_ID` / unit `architecture/role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact mode/role match`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ARCHITECTURE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ARCHITECTURE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### SmallBase
CanonicalName: `SmallBase`
Русское название: SmallBase
Краткое определение: типизированная сущность family `ARCHITECTURE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: SmallBase
Торговая роль: ARCHITECTURE
Размерность: `ROLE_ID` / unit `architecture/role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact mode/role match`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ARCHITECTURE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ARCHITECTURE`.
Legacy aliases: Small
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### Hybrid
CanonicalName: `Hybrid`
Русское название: Hybrid
Краткое определение: типизированная сущность family `ARCHITECTURE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Hybrid
Торговая роль: ARCHITECTURE
Размерность: `STATE` / unit `architecture/role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact mode/role match`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ARCHITECTURE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ARCHITECTURE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `DOCUMENTED_NOT_APPROVED`
Conflict: `HSB-DOC-CONFLICT-031`
Resolution stage: `3.1.8`

### HybridSplitBig
CanonicalName: `HybridSplitBig`
Русское название: HybridSplitBig
Краткое определение: типизированная сущность family `ARCHITECTURE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: HybridSplitBig
Торговая роль: ARCHITECTURE
Размерность: `STATE` / unit `architecture/role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact mode/role match`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ARCHITECTURE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ARCHITECTURE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### HybridMode
CanonicalName: `HybridMode`
Русское название: HybridMode
Краткое определение: типизированная сущность family `ARCHITECTURE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Hybrid
Торговая роль: ARCHITECTURE
Размерность: `STATE` / unit `architecture/role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact mode/role match`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ARCHITECTURE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ARCHITECTURE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### HybridPlan
CanonicalName: `HybridPlan`
Русское название: HybridPlan
Краткое определение: типизированная сущность family `ARCHITECTURE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: HybridPlan
Торговая роль: ARCHITECTURE
Размерность: `STATE` / unit `architecture/role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact mode/role match`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ARCHITECTURE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ARCHITECTURE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### HybridPreview
CanonicalName: `HybridPreview`
Русское название: HybridPreview
Краткое определение: типизированная сущность family `ARCHITECTURE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: HybridPreview
Торговая роль: ARCHITECTURE
Размерность: `STATE` / unit `architecture/role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact mode/role match`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ARCHITECTURE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ARCHITECTURE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### HybridExecution
CanonicalName: `HybridExecution`
Русское название: HybridExecution
Краткое определение: типизированная сущность family `ARCHITECTURE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: HybridExecution
Торговая роль: ARCHITECTURE
Размерность: `STATE` / unit `architecture/role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: explicit mode discriminator + plan role
Authoritative source: explicit mode discriminator + plan role
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact mode/role match`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ARCHITECTURE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ARCHITECTURE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### InitialBuy
CanonicalName: `InitialBuy`
Русское название: InitialBuy
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `ROLE_ID` / unit `role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### InitialSell
CanonicalName: `InitialSell`
Русское название: InitialSell
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `ROLE_ID` / unit `role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### InitialProfitLeg
CanonicalName: `InitialProfitLeg`
Русское название: InitialProfitLeg
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `ROLE_ID` / unit `role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### InitialLosingLeg
CanonicalName: `InitialLosingLeg`
Русское название: InitialLosingLeg
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `ROLE_ID` / unit `role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### InitialIgnoredProfit
CanonicalName: `InitialIgnoredProfit`
Русское название: InitialIgnoredProfit
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `MONEY_REALIZED` / unit `account money`
Знак: >=0 diagnostic, excluded
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### OldFar
CanonicalName: `OldFar`
Русское название: OldFar
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `ROLE_ID` / unit `role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### CurrentFar
CanonicalName: `CurrentFar`
Русское название: CurrentFar
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `ROLE_ID` / unit `role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: Far
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ResidualFar
CanonicalName: `ResidualFar`
Русское название: ResidualFar
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `ROLE_ID` / unit `role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### NewFar
CanonicalName: `NewFar`
Русское название: NewFar
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `ROLE_ID` / unit `role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### LegacyBigPosition
CanonicalName: `LegacyBigPosition`
Русское название: LegacyBigPosition
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `ROLE_ID` / unit `role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### BigCorePosition
CanonicalName: `BigCorePosition`
Русское название: BigCorePosition
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `ROLE_ID` / unit `role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### BigTrendPosition
CanonicalName: `BigTrendPosition`
Русское название: BigTrendPosition
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `ROLE_ID` / unit `role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### LegacySmallPosition
CanonicalName: `LegacySmallPosition`
Русское название: LegacySmallPosition
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `ROLE_ID` / unit `role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### SmallBasePosition
CanonicalName: `SmallBasePosition`
Русское название: SmallBasePosition
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `ROLE_ID` / unit `role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ManagedPosition
CanonicalName: `ManagedPosition`
Русское название: ManagedPosition
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `ROLE_ID` / unit `role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### UnmanagedPosition
CanonicalName: `UnmanagedPosition`
Русское название: UnmanagedPosition
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `ROLE_ID` / unit `role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ForeignCyclePosition
CanonicalName: `ForeignCyclePosition`
Русское название: ForeignCyclePosition
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `ROLE_ID` / unit `role`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### FarDirection
CanonicalName: `FarDirection`
Русское название: FarDirection
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `STATE` / unit `direction enum`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### OppositeFarDirection
CanonicalName: `OppositeFarDirection`
Русское название: OppositeFarDirection
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `STATE` / unit `direction enum`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### SameAsFarDirection
CanonicalName: `SameAsFarDirection`
Русское название: SameAsFarDirection
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `STATE` / unit `direction enum`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### BigDirection
CanonicalName: `BigDirection`
Русское название: BigDirection
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `STATE` / unit `direction enum`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### SmallDirection
CanonicalName: `SmallDirection`
Русское название: SmallDirection
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `STATE` / unit `direction enum`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### TrendDirection
CanonicalName: `TrendDirection`
Русское название: TrendDirection
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `STATE` / unit `direction enum`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ReverseDirection
CanonicalName: `ReverseDirection`
Русское название: ReverseDirection
Краткое определение: типизированная сущность family `ROLE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Role-qualified architecture
Торговая роль: ROLE
Размерность: `STATE` / unit `direction enum`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: reconciled MT5 position identity and role mapping
Authoritative source: reconciled MT5 position identity and role mapping
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact role/identity; actual lot uses VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `ROLE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `ROLE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### RawLot
CanonicalName: `RawLot`
Русское название: RawLot
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_RAW` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### CalculatedLot
CanonicalName: `CalculatedLot`
Русское название: CalculatedLot
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_CALCULATED` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### NormalizedLot
CanonicalName: `NormalizedLot`
Русское название: NormalizedLot
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_NORMALIZED` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### RequestedLot
CanonicalName: `RequestedLot`
Русское название: RequestedLot
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_REQUESTED` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved immutable plan
Authoritative source: approved immutable plan
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `REQUESTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### FilledLot
CanonicalName: `FilledLot`
Русское название: FilledLot
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_FILLED` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deals/trade result
Authoritative source: confirmed deals/trade result
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ActualPositionLot
CanonicalName: `ActualPositionLot`
Русское название: ActualPositionLot
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_POSITION_ACTUAL` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: current MT5 position snapshot
Authoritative source: current MT5 position snapshot
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ResidualLotProjected
CanonicalName: `ResidualLotProjected`
Русское название: ResidualLotProjected
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_RESIDUAL` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ResidualLotActual
CanonicalName: `ResidualLotActual`
Русское название: ResidualLotActual
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_POSITION_ACTUAL` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: current MT5 position snapshot
Authoritative source: current MT5 position snapshot
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### FarLotRaw
CanonicalName: `FarLotRaw`
Русское название: FarLotRaw
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_RAW` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### FarLotCalculated
CanonicalName: `FarLotCalculated`
Русское название: FarLotCalculated
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_CALCULATED` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### FarLotNormalized
CanonicalName: `FarLotNormalized`
Русское название: FarLotNormalized
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_NORMALIZED` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### FarLotRequested
CanonicalName: `FarLotRequested`
Русское название: FarLotRequested
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_REQUESTED` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved immutable plan
Authoritative source: approved immutable plan
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `REQUESTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### FarLotFilled
CanonicalName: `FarLotFilled`
Русское название: FarLotFilled
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_FILLED` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deals/trade result
Authoritative source: confirmed deals/trade result
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### FarLotActual
CanonicalName: `FarLotActual`
Русское название: FarLotActual
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_POSITION_ACTUAL` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: current MT5 position snapshot
Authoritative source: current MT5 position snapshot
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: FarLot, Ctx.farLot
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### BigCoreLotRaw
CanonicalName: `BigCoreLotRaw`
Русское название: BigCoreLotRaw
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_RAW` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### BigCoreLotNormalized
CanonicalName: `BigCoreLotNormalized`
Русское название: BigCoreLotNormalized
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_NORMALIZED` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### BigCoreLotRequested
CanonicalName: `BigCoreLotRequested`
Русское название: BigCoreLotRequested
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_REQUESTED` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved immutable plan
Authoritative source: approved immutable plan
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `REQUESTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### BigCoreLotFilled
CanonicalName: `BigCoreLotFilled`
Русское название: BigCoreLotFilled
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_FILLED` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deals/trade result
Authoritative source: confirmed deals/trade result
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### BigCoreLotActual
CanonicalName: `BigCoreLotActual`
Русское название: BigCoreLotActual
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_POSITION_ACTUAL` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: current MT5 position snapshot
Authoritative source: current MT5 position snapshot
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### BigTrendLotRaw
CanonicalName: `BigTrendLotRaw`
Русское название: BigTrendLotRaw
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_RAW` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### BigTrendLotNormalized
CanonicalName: `BigTrendLotNormalized`
Русское название: BigTrendLotNormalized
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_NORMALIZED` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### SmallBaseLotRaw
CanonicalName: `SmallBaseLotRaw`
Русское название: SmallBaseLotRaw
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_RAW` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### SmallBaseLotNormalized
CanonicalName: `SmallBaseLotNormalized`
Русское название: SmallBaseLotNormalized
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_NORMALIZED` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### PartialFarCloseLotCalculated
CanonicalName: `PartialFarCloseLotCalculated`
Русское название: PartialFarCloseLotCalculated
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_CALCULATED` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### PartialFarCloseLotNormalized
CanonicalName: `PartialFarCloseLotNormalized`
Русское название: PartialFarCloseLotNormalized
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_NORMALIZED` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### PartialFarCloseLotRequested
CanonicalName: `PartialFarCloseLotRequested`
Русское название: PartialFarCloseLotRequested
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_REQUESTED` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved immutable plan
Authoritative source: approved immutable plan
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `REQUESTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### PartialFarCloseLotFilled
CanonicalName: `PartialFarCloseLotFilled`
Русское название: PartialFarCloseLotFilled
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_FILLED` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deals/trade result
Authoritative source: confirmed deals/trade result
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### FarResidualProjected
CanonicalName: `FarResidualProjected`
Русское название: FarResidualProjected
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_RESIDUAL` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### FarResidualActual
CanonicalName: `FarResidualActual`
Русское название: FarResidualActual
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_POSITION_ACTUAL` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: current MT5 position snapshot
Authoritative source: current MT5 position snapshot
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### NewFarCandidateLot
CanonicalName: `NewFarCandidateLot`
Русское название: NewFarCandidateLot
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_CALCULATED` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `UNRESOLVED_MODE_ROUTING`
Conflict: `HSB-DOC-CONFLICT-020`
Resolution stage: `3.1.6 / 3.1.8`

### NewFarProjectedLot
CanonicalName: `NewFarProjectedLot`
Русское название: NewFarProjectedLot
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_RAW` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `UNRESOLVED_MODE_ROUTING`
Conflict: `HSB-DOC-CONFLICT-020`
Resolution stage: `3.1.6 / 3.1.8`

### NewFarNormalizedLot
CanonicalName: `NewFarNormalizedLot`
Русское название: NewFarNormalizedLot
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_NORMALIZED` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `UNRESOLVED_MODE_ROUTING`
Conflict: `HSB-DOC-CONFLICT-020`
Resolution stage: `3.1.6 / 3.1.8`

### NewFarPromotedLot
CanonicalName: `NewFarPromotedLot`
Русское название: NewFarPromotedLot
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_NORMALIZED` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: typed formula + SymbolInfo volume constraints
Authoritative source: typed formula + SymbolInfo volume constraints
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: profile-specific lot normalization
Rounding: profile-specific lot normalization
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `UNRESOLVED_MODE_ROUTING`
Conflict: `HSB-DOC-CONFLICT-020`
Resolution stage: `3.1.6 / 3.1.8`

### NewFarActualLot
CanonicalName: `NewFarActualLot`
Русское название: NewFarActualLot
Краткое определение: типизированная сущность family `LOT`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Legacy/Split/Hybrid, role-qualified
Торговая роль: LOT
Размерность: `LOT_POSITION_ACTUAL` / unit `lot`
Знак: >=0; active position >0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: current MT5 position snapshot
Authoritative source: current MT5 position snapshot
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `VolumeToleranceLots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `LOT` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `LOT`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `UNRESOLVED_MODE_ROUTING`
Conflict: `HSB-DOC-CONFLICT-020`
Resolution stage: `3.1.6 / 3.1.8`

### Point
CanonicalName: `Point`
Русское название: Point
Краткое определение: типизированная сущность family `PRICE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: PRICE
Размерность: `PRICE_PROJECTED` / unit `price`
Знак: >0 for absolute price; delta signed
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `PRICE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `PRICE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### TickSize
CanonicalName: `TickSize`
Русское название: TickSize
Краткое определение: типизированная сущность family `PRICE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: PRICE
Размерность: `PRICE_PROJECTED` / unit `price`
Знак: >0 for absolute price; delta signed
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `PRICE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `PRICE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### TickValue
CanonicalName: `TickValue`
Русское название: TickValue
Краткое определение: типизированная сущность family `PRICE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: PRICE
Размерность: `PRICE_PROJECTED` / unit `price`
Знак: >0 for absolute price; delta signed
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `PRICE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `PRICE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### MarketBidPrice
CanonicalName: `MarketBidPrice`
Русское название: MarketBidPrice
Краткое определение: типизированная сущность family `PRICE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: PRICE
Размерность: `PRICE_BID` / unit `price`
Знак: >0 for absolute price; delta signed
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `PRICE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `PRICE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### MarketAskPrice
CanonicalName: `MarketAskPrice`
Русское название: MarketAskPrice
Краткое определение: типизированная сущность family `PRICE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: PRICE
Размерность: `PRICE_ASK` / unit `price`
Знак: >0 for absolute price; delta signed
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `PRICE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `PRICE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### PositionOpenPrice
CanonicalName: `PositionOpenPrice`
Русское название: PositionOpenPrice
Краткое определение: типизированная сущность family `PRICE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: PRICE
Размерность: `PRICE_OPEN` / unit `price`
Знак: >0 for absolute price; delta signed
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `PRICE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `PRICE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### TriggerPrice
CanonicalName: `TriggerPrice`
Русское название: TriggerPrice
Краткое определение: типизированная сущность family `PRICE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: PRICE
Размерность: `PRICE_PROJECTED` / unit `price`
Знак: >0 for absolute price; delta signed
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `PRICE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `PRICE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### TargetPrice
CanonicalName: `TargetPrice`
Русское название: TargetPrice
Краткое определение: типизированная сущность family `PRICE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: PRICE
Размерность: `PRICE_PROJECTED` / unit `price`
Знак: >0 for absolute price; delta signed
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `PRICE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `PRICE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ControlPrice
CanonicalName: `ControlPrice`
Русское название: ControlPrice
Краткое определение: типизированная сущность family `PRICE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: PRICE
Размерность: `PRICE_PROJECTED` / unit `price`
Знак: >0 for absolute price; delta signed
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `PRICE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `PRICE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ProjectedExitPrice
CanonicalName: `ProjectedExitPrice`
Русское название: ProjectedExitPrice
Краткое определение: типизированная сущность family `PRICE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: PRICE
Размерность: `PRICE_PROJECTED` / unit `price`
Знак: >0 for absolute price; delta signed
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `PRICE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `PRICE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ExecutedDealPrice
CanonicalName: `ExecutedDealPrice`
Русское название: ExecutedDealPrice
Краткое определение: типизированная сущность family `PRICE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: PRICE
Размерность: `PRICE_EXECUTED` / unit `price`
Знак: >0 for absolute price; delta signed
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `CONFIRMED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `PRICE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `PRICE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### PriceDelta
CanonicalName: `PriceDelta`
Русское название: PriceDelta
Краткое определение: типизированная сущность family `PRICE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: PRICE
Размерность: `PRICE_DELTA` / unit `price`
Знак: >0 for absolute price; delta signed
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `PRICE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `PRICE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### DistancePoints
CanonicalName: `DistancePoints`
Русское название: DistancePoints
Краткое определение: типизированная сущность family `PRICE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: PRICE
Размерность: `POINTS` / unit `point`
Знак: >0 for absolute price; delta signed
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PointTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `PRICE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `PRICE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### DistanceTicks
CanonicalName: `DistanceTicks`
Русское название: DistanceTicks
Краткое определение: типизированная сущность family `PRICE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: PRICE
Размерность: `TICKS` / unit `tick`
Знак: >0 for absolute price; delta signed
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PointTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `PRICE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `PRICE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### BidAwareClosePrice
CanonicalName: `BidAwareClosePrice`
Русское название: BidAwareClosePrice
Краткое определение: типизированная сущность family `PRICE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: PRICE
Размерность: `PRICE_BID` / unit `price`
Знак: >0 for absolute price; delta signed
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `PRICE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `PRICE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### AskAwareClosePrice
CanonicalName: `AskAwareClosePrice`
Русское название: AskAwareClosePrice
Краткое определение: типизированная сущность family `PRICE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: PRICE
Размерность: `PRICE_ASK` / unit `price`
Знак: >0 for absolute price; delta signed
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `PRICE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `PRICE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### FarOpenPriceActual
CanonicalName: `FarOpenPriceActual`
Русское название: FarOpenPriceActual
Краткое определение: типизированная сущность family `PRICE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: PRICE
Размерность: `PRICE_OPEN` / unit `price`
Знак: >0 for absolute price; delta signed
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `PRICE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `PRICE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### BigCoreOpenPriceActual
CanonicalName: `BigCoreOpenPriceActual`
Русское название: BigCoreOpenPriceActual
Краткое определение: типизированная сущность family `PRICE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: PRICE
Размерность: `PRICE_OPEN` / unit `price`
Знак: >0 for absolute price; delta signed
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `PRICE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `PRICE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### BigTrendOpenPriceActual
CanonicalName: `BigTrendOpenPriceActual`
Русское название: BigTrendOpenPriceActual
Краткое определение: типизированная сущность family `PRICE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: PRICE
Размерность: `PRICE_OPEN` / unit `price`
Знак: >0 for absolute price; delta signed
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `PRICE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `PRICE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### SmallBaseOpenPriceActual
CanonicalName: `SmallBaseOpenPriceActual`
Русское название: SmallBaseOpenPriceActual
Краткое определение: типизированная сущность family `PRICE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All profiles; Symbol-bound
Торговая роль: PRICE
Размерность: `PRICE_OPEN` / unit `price`
Знак: >0 for absolute price; delta signed
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: SymbolInfo tick/current position/deal properties
Authoritative source: SymbolInfo tick/current position/deal properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Rounding: ROUND_TO_PRICE_TICK or NO_ADDITIONAL_ROUNDING for actual
Tolerance: `PriceTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `PRICE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `PRICE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### GrossProfit
CanonicalName: `GrossProfit`
Русское название: GrossProfit
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_REALIZED` / unit `account money`
Знак: signed P/L
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### GrossLoss
CanonicalName: `GrossLoss`
Русское название: GrossLoss
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_REALIZED` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### NetProfit
CanonicalName: `NetProfit`
Русское название: NetProfit
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_REALIZED` / unit `account money`
Знак: signed P/L
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### LegNet
CanonicalName: `LegNet`
Русское название: LegNet
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_REALIZED` / unit `account money`
Знак: signed P/L
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### BasketNet
CanonicalName: `BasketNet`
Русское название: BasketNet
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_REALIZED` / unit `account money`
Знак: signed P/L
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### HarvestGross
CanonicalName: `HarvestGross`
Русское название: HarvestGross
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_REALIZED` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### HarvestNet
CanonicalName: `HarvestNet`
Русское название: HarvestNet
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_REALIZED` / unit `account money`
Знак: signed P/L
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### SmallReverseNet
CanonicalName: `SmallReverseNet`
Русское название: SmallReverseNet
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_REALIZED` / unit `account money`
Знак: signed P/L
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `UNRESOLVED_BUSINESS_POLICY`
Conflict: `HSB-DOC-CONFLICT-023`
Resolution stage: `3.1.5 / 3.1.6`

### TransitionNet
CanonicalName: `TransitionNet`
Русское название: TransitionNet
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_REALIZED` / unit `account money`
Знак: signed P/L
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### RealizedCyclePL
CanonicalName: `RealizedCyclePL`
Русское название: RealizedCyclePL
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_REALIZED` / unit `account money`
Знак: signed P/L
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### FloatingManagedPL
CanonicalName: `FloatingManagedPL`
Русское название: FloatingManagedPL
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_FLOATING` / unit `account money`
Знак: signed P/L
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: current position or broker-aware price model
Authoritative source: current position or broker-aware price model
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ProjectedFloatingPL
CanonicalName: `ProjectedFloatingPL`
Русское название: ProjectedFloatingPL
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_PROJECTED` / unit `account money`
Знак: signed P/L
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### RecoveryPLAnalytic
CanonicalName: `RecoveryPLAnalytic`
Русское название: RecoveryPLAnalytic
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_PROJECTED` / unit `account money`
Знак: signed P/L
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### RecoveryPLProjected
CanonicalName: `RecoveryPLProjected`
Русское название: RecoveryPLProjected
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_PROJECTED` / unit `account money`
Знак: signed P/L
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### RecoveryPLCloseNow
CanonicalName: `RecoveryPLCloseNow`
Русское название: RecoveryPLCloseNow
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_PROJECTED` / unit `account money`
Знак: signed P/L
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### RealRecoveryPL
CanonicalName: `RealRecoveryPL`
Русское название: RealRecoveryPL
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_REALIZED` / unit `account money`
Знак: signed P/L
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: realRecoveryPL
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### RecoverySlope
CanonicalName: `RecoverySlope`
Русское название: RecoverySlope
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_PROJECTED` / unit `account money`
Знак: signed P/L
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### RecoveryMonotonicity
CanonicalName: `RecoveryMonotonicity`
Русское название: RecoveryMonotonicity
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_PROJECTED` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ExpectedExitCosts
CanonicalName: `ExpectedExitCosts`
Русское название: ExpectedExitCosts
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_PROJECTED` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### CommissionCost
CanonicalName: `CommissionCost`
Русское название: CommissionCost
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_COST` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### SwapCost
CanonicalName: `SwapCost`
Русское название: SwapCost
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_COST` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### FeeCost
CanonicalName: `FeeCost`
Русское название: FeeCost
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_COST` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### SpreadCost
CanonicalName: `SpreadCost`
Русское название: SpreadCost
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_COST` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### SlippageCost
CanonicalName: `SlippageCost`
Русское название: SlippageCost
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_COST` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### PositionPLSigned
CanonicalName: `PositionPLSigned`
Русское название: PositionPLSigned
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_FLOATING` / unit `account money`
Знак: signed P/L
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: current position or broker-aware price model
Authoritative source: current position or broker-aware price model
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CURRENT`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### FarLossSigned
CanonicalName: `FarLossSigned`
Русское название: FarLossSigned
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_REALIZED` / unit `account money`
Знак: signed P/L
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### FarLossMagnitude
CanonicalName: `FarLossMagnitude`
Русское название: FarLossMagnitude
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_REALIZED` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### PartialFarBudgetProjected
CanonicalName: `PartialFarBudgetProjected`
Русское название: PartialFarBudgetProjected
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_PROJECTED` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### PartialFarBudgetReal
CanonicalName: `PartialFarBudgetReal`
Русское название: PartialFarBudgetReal
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_RESERVED` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### PartialFarBudgetAvailable
CanonicalName: `PartialFarBudgetAvailable`
Русское название: PartialFarBudgetAvailable
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_AVAILABLE` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### PartialFarBudgetConsumed
CanonicalName: `PartialFarBudgetConsumed`
Русское название: PartialFarBudgetConsumed
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_CONSUMED` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### PartialFarBudgetResidual
CanonicalName: `PartialFarBudgetResidual`
Русское название: PartialFarBudgetResidual
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_RESIDUAL` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### FinalReserveProjected
CanonicalName: `FinalReserveProjected`
Русское название: FinalReserveProjected
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_PROJECTED` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### FinalReserveReal
CanonicalName: `FinalReserveReal`
Русское название: FinalReserveReal
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_RESERVED` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: TotalReserve, finalReserveReal
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ReserveAddProjected
CanonicalName: `ReserveAddProjected`
Русское название: ReserveAddProjected
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_PROJECTED` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ReserveAddReal
CanonicalName: `ReserveAddReal`
Русское название: ReserveAddReal
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_RESERVED` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ReserveAvailable
CanonicalName: `ReserveAvailable`
Русское название: ReserveAvailable
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_AVAILABLE` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ReserveConsumed
CanonicalName: `ReserveConsumed`
Русское название: ReserveConsumed
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_CONSUMED` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ReserveResidual
CanonicalName: `ReserveResidual`
Русское название: ReserveResidual
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_RESIDUAL` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### CarryAvailable
CanonicalName: `CarryAvailable`
Русское название: CarryAvailable
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_AVAILABLE` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### CarryConsumed
CanonicalName: `CarryConsumed`
Русское название: CarryConsumed
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_CONSUMED` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### CarryResidual
CanonicalName: `CarryResidual`
Русское название: CarryResidual
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_RESIDUAL` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### TransitionBudgetAvailable
CanonicalName: `TransitionBudgetAvailable`
Русское название: TransitionBudgetAvailable
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_AVAILABLE` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### FinalCloseRequirement
CanonicalName: `FinalCloseRequirement`
Русское название: FinalCloseRequirement
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_RESERVED` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: confirmed deal history / exactly-once ledger
Authoritative source: confirmed deal history / exactly-once ledger
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### BasketRiskMoney
CanonicalName: `BasketRiskMoney`
Русское название: BasketRiskMoney
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_PROJECTED` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### AccountRiskMoney
CanonicalName: `AccountRiskMoney`
Русское название: AccountRiskMoney
Краткое определение: типизированная сущность family `MONEY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle/account as explicitly qualified
Торговая роль: MONEY
Размерность: `MONEY_PROJECTED` / unit `account money`
Знак: non-negative magnitude/bucket
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: OrderCalcProfit + explicit projected costs
Authoritative source: OrderCalcProfit + explicit projected costs
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Rounding: ROUND_TO_MONEY_DIGITS only at ledger boundary/display; never before conservative gate
Tolerance: `MoneyTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `MONEY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `MONEY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### BigRatio
CanonicalName: `BigRatio`
Русское название: BigRatio
Краткое определение: типизированная сущность family `RATIO`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: RATIO
Размерность: `RATIO` / unit `1 (dimensionless)`
Знак: non-negative; range stated per term
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `RATIO` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `RATIO`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `UNRESOLVED_PARAMETER_PROFILE`
Conflict: `HSB-DOC-CONFLICT-001`
Resolution stage: `3.1.7`

### SmallRatio
CanonicalName: `SmallRatio`
Русское название: SmallRatio
Краткое определение: типизированная сущность family `RATIO`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: RATIO
Размерность: `RATIO` / unit `1 (dimensionless)`
Знак: non-negative; range stated per term
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `RATIO` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `RATIO`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `UNRESOLVED_PARAMETER_PROFILE`
Conflict: `HSB-DOC-CONFLICT-002`
Resolution stage: `3.1.7`

### CloseBigOnSmallShare
CanonicalName: `CloseBigOnSmallShare`
Русское название: CloseBigOnSmallShare
Краткое определение: типизированная сущность family `RATIO`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: RATIO
Размерность: `SHARE` / unit `1 (dimensionless)`
Знак: non-negative; range stated per term
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `RATIO` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `RATIO`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `UNRESOLVED_PARAMETER_PROFILE`
Conflict: `HSB-DOC-CONFLICT-003`
Resolution stage: `3.1.7`

### RemainBigOnSmallShare
CanonicalName: `RemainBigOnSmallShare`
Русское название: RemainBigOnSmallShare
Краткое определение: типизированная сущность family `RATIO`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: RATIO
Размерность: `SHARE` / unit `1 (dimensionless)`
Знак: non-negative; range stated per term
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `RATIO` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `RATIO`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `UNRESOLVED_PARAMETER_PROFILE`
Conflict: `HSB-DOC-CONFLICT-004`
Resolution stage: `3.1.7`

### CloseFarShare
CanonicalName: `CloseFarShare`
Русское название: CloseFarShare
Краткое определение: типизированная сущность family `RATIO`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: RATIO
Размерность: `SHARE` / unit `1 (dimensionless)`
Знак: non-negative; range stated per term
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `RATIO` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `RATIO`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `UNRESOLVED_PARAMETER_PROFILE`
Conflict: `HSB-DOC-CONFLICT-005`
Resolution stage: `3.1.7`

### ReserveShare
CanonicalName: `ReserveShare`
Русское название: ReserveShare
Краткое определение: типизированная сущность family `RATIO`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: RATIO
Размерность: `SHARE` / unit `1 (dimensionless)`
Знак: non-negative; range stated per term
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `RATIO` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `RATIO`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `UNRESOLVED_PARAMETER_PROFILE`
Conflict: `HSB-DOC-CONFLICT-006`
Resolution stage: `3.1.7`

### SmallReserveShare
CanonicalName: `SmallReserveShare`
Русское название: SmallReserveShare
Краткое определение: типизированная сущность family `RATIO`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: RATIO
Размерность: `SHARE` / unit `1 (dimensionless)`
Знак: non-negative; range stated per term
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `RATIO` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `RATIO`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### CompressionRatio
CanonicalName: `CompressionRatio`
Русское название: CompressionRatio
Краткое определение: типизированная сущность family `RATIO`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: RATIO
Размерность: `RATIO` / unit `1 (dimensionless)`
Знак: non-negative; range stated per term
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `RATIO` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `RATIO`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ReserveCoverageRatio
CanonicalName: `ReserveCoverageRatio`
Русское название: ReserveCoverageRatio
Краткое определение: типизированная сущность family `RATIO`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: RATIO
Размерность: `RATIO` / unit `1 (dimensionless)`
Знак: non-negative; range stated per term
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `RATIO` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `RATIO`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### RecoveryCoverageRatio
CanonicalName: `RecoveryCoverageRatio`
Русское название: RecoveryCoverageRatio
Краткое определение: типизированная сущность family `RATIO`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: RATIO
Размерность: `RATIO` / unit `1 (dimensionless)`
Знак: non-negative; range stated per term
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `RATIO` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `RATIO`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### MaximumNewBigToOldFarRatio
CanonicalName: `MaximumNewBigToOldFarRatio`
Русское название: MaximumNewBigToOldFarRatio
Краткое определение: типизированная сущность family `RATIO`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: RATIO
Размерность: `RATIO` / unit `1 (dimensionless)`
Знак: non-negative; range stated per term
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `RATIO` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `RATIO`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `UNRESOLVED_BUSINESS_POLICY`
Conflict: `HSB-DOC-CONFLICT-022`
Resolution stage: `3.1.4 / 3.1.8`

### MinimumReserveCatchUpRatio
CanonicalName: `MinimumReserveCatchUpRatio`
Русское название: MinimumReserveCatchUpRatio
Краткое определение: типизированная сущность family `RATIO`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: RATIO
Размерность: `RATIO` / unit `1 (dimensionless)`
Знак: non-negative; range stated per term
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `RATIO` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `RATIO`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### PercentValue
CanonicalName: `PercentValue`
Русское название: PercentValue
Краткое определение: типизированная сущность family `RATIO`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: RATIO
Размерность: `PERCENT` / unit `1 (dimensionless)`
Знак: non-negative; range stated per term
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `RATIO` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `RATIO`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ScaleMultiplier
CanonicalName: `ScaleMultiplier`
Русское название: ScaleMultiplier
Краткое определение: типизированная сущность family `RATIO`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: RATIO
Размерность: `MULTIPLIER` / unit `1 (dimensionless)`
Знак: non-negative; range stated per term
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `RATIO` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `RATIO`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### RiskThresholdRatio
CanonicalName: `RiskThresholdRatio`
Русское название: RiskThresholdRatio
Краткое определение: типизированная сущность family `RATIO`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Profile-qualified; unresolved values not selected
Торговая роль: RATIO
Размерность: `RATIO` / unit `1 (dimensionless)`
Знак: non-negative; range stated per term
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved profile or typed formula
Authoritative source: approved profile or typed formula
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY/PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `RatioTolerance`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `RATIO` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `RATIO`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### SymbolId
CanonicalName: `SymbolId`
Русское название: SymbolId
Краткое определение: типизированная сущность family `IDENTITY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: IDENTITY
Размерность: `SYMBOL_ID` / unit `identifier`
Знак: non-zero/valid in active scope
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact match; FingerprintTolerance permits no semantic drift`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `IDENTITY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `IDENTITY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### MagicId
CanonicalName: `MagicId`
Русское название: MagicId
Краткое определение: типизированная сущность family `IDENTITY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: IDENTITY
Размерность: `MAGIC_ID` / unit `identifier`
Знак: non-zero/valid in active scope
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact match; FingerprintTolerance permits no semantic drift`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `IDENTITY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `IDENTITY`.
Legacy aliases: MagicNumber
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### CycleId
CanonicalName: `CycleId`
Русское название: CycleId
Краткое определение: типизированная сущность family `IDENTITY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: IDENTITY
Размерность: `CYCLE_ID` / unit `identifier`
Знак: non-zero/valid in active scope
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact match; FingerprintTolerance permits no semantic drift`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `IDENTITY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `IDENTITY`.
Legacy aliases: CycleID, cycleId
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### RoleId
CanonicalName: `RoleId`
Русское название: RoleId
Краткое определение: типизированная сущность family `IDENTITY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: IDENTITY
Размерность: `ROLE_ID` / unit `identifier`
Знак: non-zero/valid in active scope
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact match; FingerprintTolerance permits no semantic drift`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `IDENTITY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `IDENTITY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### PositionIdentifier
CanonicalName: `PositionIdentifier`
Русское название: PositionIdentifier
Краткое определение: типизированная сущность family `IDENTITY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: IDENTITY
Размерность: `POSITION_ID` / unit `identifier`
Знак: non-zero/valid in active scope
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact match; FingerprintTolerance permits no semantic drift`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `IDENTITY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `IDENTITY`.
Legacy aliases: POSITION_IDENTIFIER
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### PositionTicket
CanonicalName: `PositionTicket`
Русское название: PositionTicket
Краткое определение: типизированная сущность family `IDENTITY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: IDENTITY
Размерность: `POSITION_TICKET` / unit `identifier`
Знак: non-zero/valid in active scope
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact match; FingerprintTolerance permits no semantic drift`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `IDENTITY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `IDENTITY`.
Legacy aliases: ticket
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### OrderTicket
CanonicalName: `OrderTicket`
Русское название: OrderTicket
Краткое определение: типизированная сущность family `IDENTITY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: IDENTITY
Размерность: `ORDER_TICKET` / unit `identifier`
Знак: non-zero/valid in active scope
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact match; FingerprintTolerance permits no semantic drift`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `IDENTITY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `IDENTITY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### DealTicket
CanonicalName: `DealTicket`
Русское название: DealTicket
Краткое определение: типизированная сущность family `IDENTITY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: IDENTITY
Размерность: `DEAL_TICKET` / unit `identifier`
Знак: non-zero/valid in active scope
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact match; FingerprintTolerance permits no semantic drift`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `IDENTITY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `IDENTITY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### EventId
CanonicalName: `EventId`
Русское название: EventId
Краткое определение: типизированная сущность family `IDENTITY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: IDENTITY
Размерность: `EVENT_ID` / unit `identifier`
Знак: non-zero/valid in active scope
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact match; FingerprintTolerance permits no semantic drift`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `IDENTITY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `IDENTITY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### EventKey
CanonicalName: `EventKey`
Русское название: EventKey
Краткое определение: типизированная сущность family `IDENTITY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: IDENTITY
Размерность: `EVENT_ID` / unit `identifier`
Знак: non-zero/valid in active scope
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact match; FingerprintTolerance permits no semantic drift`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `IDENTITY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `IDENTITY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### SnapshotFingerprint
CanonicalName: `SnapshotFingerprint`
Русское название: SnapshotFingerprint
Краткое определение: типизированная сущность family `IDENTITY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: IDENTITY
Размерность: `FINGERPRINT` / unit `identifier`
Знак: non-zero/valid in active scope
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact match; FingerprintTolerance permits no semantic drift`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `IDENTITY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `IDENTITY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### PlanFingerprint
CanonicalName: `PlanFingerprint`
Русское название: PlanFingerprint
Краткое определение: типизированная сущность family `IDENTITY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: IDENTITY
Размерность: `FINGERPRINT` / unit `identifier`
Знак: non-zero/valid in active scope
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact match; FingerprintTolerance permits no semantic drift`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `IDENTITY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `IDENTITY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### PositionComment
CanonicalName: `PositionComment`
Русское название: PositionComment
Краткое определение: типизированная сущность family `IDENTITY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: IDENTITY
Размерность: `ROLE_ID` / unit `identifier`
Знак: non-zero/valid in active scope
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact match; FingerprintTolerance permits no semantic drift`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `IDENTITY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `IDENTITY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### SnapshotRevision
CanonicalName: `SnapshotRevision`
Русское название: SnapshotRevision
Краткое определение: типизированная сущность family `IDENTITY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: IDENTITY
Размерность: `ROLE_ID` / unit `identifier`
Знак: non-zero/valid in active scope
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact match; FingerprintTolerance permits no semantic drift`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `IDENTITY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `IDENTITY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### StateRevision
CanonicalName: `StateRevision`
Русское название: StateRevision
Краткое определение: типизированная сущность family `IDENTITY`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Symbol+Magic+CycleID+role scope
Торговая роль: IDENTITY
Размерность: `EVENT_ID` / unit `identifier`
Знак: non-zero/valid in active scope
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: MT5 properties / persisted reconciled namespace
Authoritative source: MT5 properties / persisted reconciled namespace
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact match; FingerprintTolerance permits no semantic drift`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `IDENTITY` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `IDENTITY`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### State
CanonicalName: `State`
Русское название: State
Краткое определение: типизированная сущность family `STATE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle lifecycle
Торговая роль: STATE
Размерность: `STATE` / unit `enum/structured record`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact enum; typed field tolerances inside snapshots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `STATE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `STATE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### Phase
CanonicalName: `Phase`
Русское название: Phase
Краткое определение: типизированная сущность family `STATE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle lifecycle
Торговая роль: STATE
Размерность: `PHASE` / unit `enum/structured record`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact enum; typed field tolerances inside snapshots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `STATE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `STATE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### Event
CanonicalName: `Event`
Русское название: Event
Краткое определение: типизированная сущность family `STATE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle lifecycle
Торговая роль: STATE
Размерность: `OUTCOME` / unit `enum/structured record`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact enum; typed field tolerances inside snapshots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `STATE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `STATE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### Observation
CanonicalName: `Observation`
Русское название: Observation
Краткое определение: типизированная сущность family `STATE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle lifecycle
Торговая роль: STATE
Размерность: `OUTCOME` / unit `enum/structured record`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact enum; typed field tolerances inside snapshots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `STATE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `STATE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### GateResult
CanonicalName: `GateResult`
Русское название: GateResult
Краткое определение: типизированная сущность family `STATE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle lifecycle
Торговая роль: STATE
Размерность: `GATE_RESULT` / unit `enum/structured record`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact enum; typed field tolerances inside snapshots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `STATE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `STATE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ExecutionResult
CanonicalName: `ExecutionResult`
Русское название: ExecutionResult
Краткое определение: типизированная сущность family `STATE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle lifecycle
Торговая роль: STATE
Размерность: `OUTCOME` / unit `enum/structured record`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact enum; typed field tolerances inside snapshots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `STATE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `STATE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### Outcome
CanonicalName: `Outcome`
Русское название: Outcome
Краткое определение: типизированная сущность family `STATE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle lifecycle
Торговая роль: STATE
Размерность: `OUTCOME` / unit `enum/structured record`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact enum; typed field tolerances inside snapshots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `STATE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `STATE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ReasonCode
CanonicalName: `ReasonCode`
Русское название: ReasonCode
Краткое определение: типизированная сущность family `STATE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle lifecycle
Торговая роль: STATE
Размерность: `REASON_CODE` / unit `enum/structured record`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact enum; typed field tolerances inside snapshots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `STATE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `STATE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ErrorCode
CanonicalName: `ErrorCode`
Русское название: ErrorCode
Краткое определение: типизированная сущность family `STATE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle lifecycle
Торговая роль: STATE
Размерность: `REASON_CODE` / unit `enum/structured record`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact enum; typed field tolerances inside snapshots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `STATE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `STATE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### DiagnosticText
CanonicalName: `DiagnosticText`
Русское название: DiagnosticText
Краткое определение: типизированная сущность family `STATE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle lifecycle
Торговая роль: STATE
Размерность: `OUTCOME` / unit `enum/structured record`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact enum; typed field tolerances inside snapshots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `STATE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `STATE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### CandidatePlan
CanonicalName: `CandidatePlan`
Русское название: CandidatePlan
Краткое определение: типизированная сущность family `STATE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle lifecycle
Торговая роль: STATE
Размерность: `OUTCOME` / unit `enum/structured record`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact enum; typed field tolerances inside snapshots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `STATE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `STATE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ApprovedImmutablePlan
CanonicalName: `ApprovedImmutablePlan`
Русское название: ApprovedImmutablePlan
Краткое определение: типизированная сущность family `STATE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle lifecycle
Торговая роль: STATE
Размерность: `OUTCOME` / unit `enum/structured record`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact enum; typed field tolerances inside snapshots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `STATE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `STATE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ExecutionRequest
CanonicalName: `ExecutionRequest`
Русское название: ExecutionRequest
Краткое определение: типизированная сущность family `STATE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle lifecycle
Торговая роль: STATE
Размерность: `OUTCOME` / unit `enum/structured record`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact enum; typed field tolerances inside snapshots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `STATE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `STATE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### BrokerExecutionResult
CanonicalName: `BrokerExecutionResult`
Русское название: BrokerExecutionResult
Краткое определение: типизированная сущность family `STATE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle lifecycle
Торговая роль: STATE
Размерность: `OUTCOME` / unit `enum/structured record`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact enum; typed field tolerances inside snapshots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `STATE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `STATE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ReconciledResult
CanonicalName: `ReconciledResult`
Русское название: ReconciledResult
Краткое определение: типизированная сущность family `STATE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle lifecycle
Торговая роль: STATE
Размерность: `OUTCOME` / unit `enum/structured record`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact enum; typed field tolerances inside snapshots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `STATE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `STATE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### CommittedLedgerEvent
CanonicalName: `CommittedLedgerEvent`
Русское название: CommittedLedgerEvent
Краткое определение: типизированная сущность family `STATE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle lifecycle
Торговая роль: STATE
Размерность: `OUTCOME` / unit `enum/structured record`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact enum; typed field tolerances inside snapshots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `STATE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `STATE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### BaseSnapshot
CanonicalName: `BaseSnapshot`
Русское название: BaseSnapshot
Краткое определение: типизированная сущность family `STATE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle lifecycle
Торговая роль: STATE
Размерность: `STATE` / unit `enum/structured record`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact enum; typed field tolerances inside snapshots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `STATE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `STATE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### WorstSnapshot
CanonicalName: `WorstSnapshot`
Русское название: WorstSnapshot
Краткое определение: типизированная сущность family `STATE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle lifecycle
Торговая роль: STATE
Размерность: `STATE` / unit `enum/structured record`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact enum; typed field tolerances inside snapshots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `STATE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `STATE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ActualSnapshot
CanonicalName: `ActualSnapshot`
Русское название: ActualSnapshot
Краткое определение: типизированная сущность family `STATE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle lifecycle
Торговая роль: STATE
Размерность: `STATE` / unit `enum/structured record`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact enum; typed field tolerances inside snapshots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `STATE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `STATE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### SnapshotStaleFlag
CanonicalName: `SnapshotStaleFlag`
Русское название: SnapshotStaleFlag
Краткое определение: типизированная сущность family `STATE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle lifecycle
Торговая роль: STATE
Размерность: `OUTCOME` / unit `enum/structured record`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact enum; typed field tolerances inside snapshots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `STATE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `STATE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### FinalClosePreview
CanonicalName: `FinalClosePreview`
Русское название: FinalClosePreview
Краткое определение: типизированная сущность family `STATE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle lifecycle
Торговая роль: STATE
Размерность: `OUTCOME` / unit `enum/structured record`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact enum; typed field tolerances inside snapshots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `STATE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `STATE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### FinalCloseActualSuccess
CanonicalName: `FinalCloseActualSuccess`
Русское название: FinalCloseActualSuccess
Краткое определение: типизированная сущность family `STATE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Cycle lifecycle
Торговая роль: STATE
Размерность: `OUTCOME` / unit `enum/structured record`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: state machine or immutable snapshot/reconciliation
Authoritative source: state machine or immutable snapshot/reconciliation
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `ACTUAL/CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact enum; typed field tolerances inside snapshots`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `STATE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `STATE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### MoneyTolerance
CanonicalName: `MoneyTolerance`
Русское название: MoneyTolerance
Краткое определение: типизированная сущность family `TOLERANCE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Dimension-specific only
Торговая роль: TOLERANCE
Размерность: `MONEY_AVAILABLE` / unit `same unit as compared operands`
Знак: >=0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved config/symbol properties
Authoritative source: approved config/symbol properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `self`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `TOLERANCE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `TOLERANCE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### VolumeToleranceLots
CanonicalName: `VolumeToleranceLots`
Русское название: VolumeToleranceLots
Краткое определение: типизированная сущность family `TOLERANCE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Dimension-specific only
Торговая роль: TOLERANCE
Размерность: `LOT_NORMALIZED` / unit `same unit as compared operands`
Знак: >=0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved config/symbol properties
Authoritative source: approved config/symbol properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `self`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `TOLERANCE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `TOLERANCE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### PriceTolerance
CanonicalName: `PriceTolerance`
Русское название: PriceTolerance
Краткое определение: типизированная сущность family `TOLERANCE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Dimension-specific only
Торговая роль: TOLERANCE
Размерность: `PRICE_PROJECTED` / unit `same unit as compared operands`
Знак: >=0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved config/symbol properties
Authoritative source: approved config/symbol properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `self`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `TOLERANCE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `TOLERANCE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### PointTolerance
CanonicalName: `PointTolerance`
Русское название: PointTolerance
Краткое определение: типизированная сущность family `TOLERANCE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Dimension-specific only
Торговая роль: TOLERANCE
Размерность: `POINTS` / unit `same unit as compared operands`
Знак: >=0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved config/symbol properties
Authoritative source: approved config/symbol properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `self`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `TOLERANCE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `TOLERANCE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### RatioTolerance
CanonicalName: `RatioTolerance`
Русское название: RatioTolerance
Краткое определение: типизированная сущность family `TOLERANCE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Dimension-specific only
Торговая роль: TOLERANCE
Размерность: `RATIO` / unit `same unit as compared operands`
Знак: >=0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved config/symbol properties
Authoritative source: approved config/symbol properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `self`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `TOLERANCE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `TOLERANCE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ComparisonEpsilon
CanonicalName: `ComparisonEpsilon`
Русское название: ComparisonEpsilon
Краткое определение: типизированная сущность family `TOLERANCE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Dimension-specific only
Торговая роль: TOLERANCE
Размерность: `FINGERPRINT` / unit `same unit as compared operands`
Знак: >=0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved config/symbol properties
Authoritative source: approved config/symbol properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `self`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `TOLERANCE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `TOLERANCE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ReserveMismatchTolerance
CanonicalName: `ReserveMismatchTolerance`
Русское название: ReserveMismatchTolerance
Краткое определение: типизированная сущность family `TOLERANCE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Dimension-specific only
Торговая роль: TOLERANCE
Размерность: `MONEY_AVAILABLE` / unit `same unit as compared operands`
Знак: >=0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved config/symbol properties
Authoritative source: approved config/symbol properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `self`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `TOLERANCE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `TOLERANCE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### GeometryTolerance
CanonicalName: `GeometryTolerance`
Русское название: GeometryTolerance
Краткое определение: типизированная сущность family `TOLERANCE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Dimension-specific only
Торговая роль: TOLERANCE
Размерность: `LOT_NORMALIZED` / unit `same unit as compared operands`
Знак: >=0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved config/symbol properties
Authoritative source: approved config/symbol properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `self`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `TOLERANCE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `TOLERANCE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### FingerprintTolerance
CanonicalName: `FingerprintTolerance`
Русское название: FingerprintTolerance
Краткое определение: типизированная сущность family `TOLERANCE`; qualifier обязателен при неоднозначности.
Архитектурный профиль: Dimension-specific only
Торговая роль: TOLERANCE
Размерность: `FINGERPRINT` / unit `same unit as compared operands`
Знак: >=0
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: approved config/symbol properties
Authoritative source: approved config/symbol properties
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `POLICY`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `self`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `TOLERANCE` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `TOLERANCE`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ProjectedData
CanonicalName: `ProjectedData`
Русское название: ProjectedData
Краткое определение: типизированная сущность family `DATA_CLASS`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All
Торговая роль: DATA_CLASS
Размерность: `BOOLEAN_RESULT` / unit `data-state enum`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PROJECTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `DATA_CLASS` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `DATA_CLASS`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### RequestedData
CanonicalName: `RequestedData`
Русское название: RequestedData
Краткое определение: типизированная сущность family `DATA_CLASS`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All
Торговая роль: DATA_CLASS
Размерность: `BOOLEAN_RESULT` / unit `data-state enum`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `REQUESTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `DATA_CLASS` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `DATA_CLASS`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ExecutedData
CanonicalName: `ExecutedData`
Русское название: ExecutedData
Краткое определение: типизированная сущность family `DATA_CLASS`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All
Торговая роль: DATA_CLASS
Размерность: `BOOLEAN_RESULT` / unit `data-state enum`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `EXECUTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `DATA_CLASS` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `DATA_CLASS`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ConfirmedData
CanonicalName: `ConfirmedData`
Русское название: ConfirmedData
Краткое определение: типизированная сущность family `DATA_CLASS`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All
Торговая роль: DATA_CLASS
Размерность: `BOOLEAN_RESULT` / unit `data-state enum`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `CONFIRMED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `DATA_CLASS` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `DATA_CLASS`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### ReconciledData
CanonicalName: `ReconciledData`
Русское название: ReconciledData
Краткое определение: типизированная сущность family `DATA_CLASS`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All
Торговая роль: DATA_CLASS
Размерность: `BOOLEAN_RESULT` / unit `data-state enum`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `RECONCILED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `DATA_CLASS` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `DATA_CLASS`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### PersistedData
CanonicalName: `PersistedData`
Русское название: PersistedData
Краткое определение: типизированная сущность family `DATA_CLASS`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All
Торговая роль: DATA_CLASS
Размерность: `BOOLEAN_RESULT` / unit `data-state enum`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `PERSISTED`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `DATA_CLASS` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `DATA_CLASS`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### StaleData
CanonicalName: `StaleData`
Русское название: StaleData
Краткое определение: типизированная сущность family `DATA_CLASS`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All
Торговая роль: DATA_CLASS
Размерность: `BOOLEAN_RESULT` / unit `data-state enum`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `STALE`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `DATA_CLASS` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `DATA_CLASS`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### InvalidData
CanonicalName: `InvalidData`
Русское название: InvalidData
Краткое определение: типизированная сущность family `DATA_CLASS`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All
Торговая роль: DATA_CLASS
Размерность: `BOOLEAN_RESULT` / unit `data-state enum`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `INVALID`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `DATA_CLASS` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `DATA_CLASS`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### NotApplicableValue
CanonicalName: `NotApplicableValue`
Русское название: NotApplicableValue
Краткое определение: типизированная сущность family `DATA_CLASS`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All
Торговая роль: DATA_CLASS
Размерность: `BOOLEAN_RESULT` / unit `data-state enum`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `NOTAPPLICABLEVALUE`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `DATA_CLASS` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `DATA_CLASS`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### NotCalculatedValue
CanonicalName: `NotCalculatedValue`
Русское название: NotCalculatedValue
Краткое определение: типизированная сущность family `DATA_CLASS`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All
Торговая роль: DATA_CLASS
Размерность: `BOOLEAN_RESULT` / unit `data-state enum`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `NOTCALCULATEDVALUE`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `DATA_CLASS` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `DATA_CLASS`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### NotAvailableValue
CanonicalName: `NotAvailableValue`
Русское название: NotAvailableValue
Краткое определение: типизированная сущность family `DATA_CLASS`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All
Торговая роль: DATA_CLASS
Размерность: `BOOLEAN_RESULT` / unit `data-state enum`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `NOTAVAILABLEVALUE`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `DATA_CLASS` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `DATA_CLASS`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

### UnknownValue
CanonicalName: `UnknownValue`
Русское название: UnknownValue
Краткое определение: типизированная сущность family `DATA_CLASS`; qualifier обязателен при неоднозначности.
Архитектурный профиль: All
Торговая роль: DATA_CLASS
Размерность: `BOOLEAN_RESULT` / unit `data-state enum`
Знак: not numeric
Диапазон: определяется типом и явным gate; NaN/infinity запрещены.
Источник: lifecycle transition evidence
Authoritative source: lifecycle transition evidence
Время фиксации: на соответствующей lifecycle stage.
Projected/Actual class: `UNKNOWNVALUE`
Normalization: NO_ADDITIONAL_ROUNDING
Rounding: NO_ADDITIONAL_ROUNDING
Tolerance: `exact state`
Lifecycle: create → validate → freeze/request/confirm as applicable → persist/reconcile → invalidate/consume.
Допустимые операции: только операции семейства `DATA_CLASS` и explicit typed conversion.
Запрещённые подмены: иной type, lifecycle class, architecture role или stale cached value.
Связанные сущности: family `DATA_CLASS`.
Legacy aliases: —
MQL5 mapping: documentary mapping only; semantic compliance not claimed.
Python mapping: documentary mapping only; semantic compliance not claimed.
Статус определения: `APPROVED_TERM`

