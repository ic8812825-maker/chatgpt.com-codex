# Отчёт второй коррекции Этапа 3.1.3

## Причина второй коррекции

Первая коррекция подтверждала в основном наличие token, а не объявление и использование программного identifier. Validator также пропускал смысловое противоречие `BigGross`: определение объёма было ошибочно связано с `ROLE_ID`. Вторая коррекция не меняет runtime и не начинает Этап 3.1.4.

## BigGross correction

`BigGross` теперь однозначно означает projected сумму `BigCoreLotProjected + BigTrendLotProjected` одного immutable plan: `LOT_CALCULATED`, unit `lot`, класс `PROJECTED`, допуск `VolumeToleranceLots`. Это не role, ticket или actual position volume. Статус `DOCUMENTED_NOT_APPROVED` не выбирает business policy.

## Semantic type audit methodology

Все 230 строк проверяются между canonical table и extended record. `Semantic category` связывается с Type; далее независимо проверяются Unit, Sign/Class, Source, Rounding, Tolerance и lifecycle class. Для каждого record добавлены конкретные creation, validation, freeze, mutation, stale, replacement, terminal, persistence и restart события, а также `Отличие от`.

## MQL5 parser methodology

Lightweight parser удаляет line/block comments и string/character literals, затем индексирует function signatures, parameters, struct/class fields, global/local declarations, reads и writes. Проверено 37 MQL5/MQH source files только в режиме чтения.

## Python AST methodology

Все Python sources проекта разобраны стандартным `ast`: `FunctionDef`, `ClassDef`, arguments, `Name`, `Attribute`, assignments и uses. Regex token presence не считается mapping evidence.

## Declaration evidence and use evidence methodology

Статусы EXACT/SEMANTIC требуют declaration evidence, реальный read/write site, semantic note и lifecycle role. Cache не может считаться authoritative exact actual value. Поскольку прежние 161 status `SEMANTIC_MATCH` были основаны на token presence, все они честно понижены до `MISSING`; фиктивная переклассификация token в другой kind не выполнялась.

## Mapping status downgrade report

```text
PREVIOUS_MQL5_SEMANTIC_MATCH=88
PREVIOUS_PYTHON_SEMANTIC_MATCH=73
CONFIRMED_AFTER_DECLARATION_USE_AUDIT=0
MQL5_DOWNGRADED_TO_PARTIAL=0
MQL5_DOWNGRADED_TO_AMBIGUOUS=0
MQL5_DOWNGRADED_TO_MISSING=88
PYTHON_DOWNGRADED_TO_PARTIAL=0
PYTHON_DOWNGRADED_TO_AMBIGUOUS=0
PYTHON_DOWNGRADED_TO_MISSING=73
REASON=token occurrence did not prove one complete canonical entity, authoritative source and lifecycle
```

## Lifecycle rewrite methodology

Logical lifecycle classes (`POLICY`, `ROLE`, `PROJECTED_VALUE`, `REQUESTED`, `DEAL`, `ACTUAL_POSITION`, `LEDGER`, `SYMBOL_PROPERTY`, `STATE`, `IDENTITY`, `OBJECT`) define required events, while every record names its own object, source, stale trigger and replacement. Normalization removes canonical names before duplicate detection.

## Negative test isolation methodology

20 mutations assert one named semantic counter each. Controls include definition/type contradiction, money/lot tolerance, projected source for realized money, actual rounding, enum/identity tolerance, token/comment/string mapping, absent declaration/use evidence, authoritative cache, MISSING/NOT_APPLICABLE conflict, normalized duplicates, projected-to-actual assignment, unresolved policy, Markdown/JSON parity and lifecycle class. Ten positive controls protect legitimate MISSING, NOT_APPLICABLE, role, realized money, actual lot, enum, projected, ledger, symbol property and ratio cases.

## Remaining mappings

All MQL5 and Python records are `MISSING` with empty identifier arrays. Это сознательный conservative результат: отсутствие доказанного mapping лучше ложного `SEMANTIC_MATCH`. `identifier_kind=token` отсутствует.

## Conflict control and scope control

```text
PARAMETER_PROFILE_SELECTED=NO
BUSINESS_POLICY_SELECTED=NO
CONFLICT_020_RESOLVED=NO
CONFLICT_022_RESOLVED=NO
CONFLICT_023_RESOLVED=NO
CONFLICT_031_RESOLVED=NO
MQL5_CHANGED=NO
MQH_CHANGED=NO
TRADING_LOGIC_CHANGED=NO
STAGE_3_1_4_STARTED=NO
NEW_CONFLICTS_FOUND=0
```

## Validator output

`STATISTICS_SOURCE=validator generated`

```text
CANONICAL_TERMS=230
EXTENDED_RECORDS=230
INVALID_DEFINITION_TYPE_SEMANTICS=0
INVALID_TYPE_UNIT=0
INVALID_TYPE_CLASS=0
INVALID_TYPE_TOLERANCE=0
INVALID_TYPE_SOURCE=0
INVALID_ACTUAL_ROUNDING=0
INVALID_LIFECYCLE_CLASS=0
TOKEN_IDENTIFIER_KINDS=0
MAPPING_WITHOUT_DECLARATION_EVIDENCE=0
MAPPING_WITHOUT_USE_EVIDENCE=0
IDENTIFIER_ONLY_IN_COMMENT=0
IDENTIFIER_ONLY_IN_STRING=0
UNPROVEN_EXACT_MAPPING=0
UNPROVEN_SEMANTIC_MAPPING=0
CACHE_MARKED_AUTHORITATIVE=0
MAPPING_STATUS_PARITY_ERROR=0
MISSING_NOT_APPLICABLE_CONFLICT=0
NORMALIZED_DUPLICATE_LIFECYCLES=0
GENERIC_LIFECYCLES=0
MISSING_CREATION_EVENT=0
MISSING_STALE_TRIGGER=0
MISSING_REPLACEMENT_SOURCE=0
MISSING_TERMINAL_CONDITION=0
NEAR_DUPLICATE_DEFINITIONS=0
DEFINITIONS_WITHOUT_DISTINGUISHING_CLAUSE=0
FORBIDDEN_PROJECTED_TO_ACTUAL_TRANSITION=0
UNRESOLVED_POLICY_APPROVED=0
UNRESOLVED_ITEMS_WITHOUT_CONFLICT_ID=0
UNRESOLVED_ITEMS_WITHOUT_RESOLUTION_STAGE=0
MQL5_FILES_PARSED=37
MQL5_DECLARATIONS_FOUND=4075
MQL5_USE_SITES_FOUND=13288
PYTHON_FILES_PARSED=258
PYTHON_AST_DECLARATIONS_FOUND=5643
PYTHON_USE_SITES_FOUND=18558
MQL5_EXACT_MATCH=0
MQL5_SEMANTIC_MATCH=0
MQL5_PARTIAL_MATCH=0
MQL5_AMBIGUOUS=0
MQL5_MISSING=230
MQL5_NOT_APPLICABLE=0
PYTHON_EXACT_MATCH=0
PYTHON_SEMANTIC_MATCH=0
PYTHON_PARTIAL_MATCH=0
PYTHON_AMBIGUOUS=0
PYTHON_MISSING=230
PYTHON_NOT_APPLICABLE=0
NEGATIVE_TESTS_TOTAL=20
NEGATIVE_TESTS_PASSED=20
POSITIVE_TESTS_TOTAL=10
POSITIVE_TESTS_PASSED=10
STAGE_3_1_3_SECOND_CORRECTION_VALIDATION=PASS
```

## Per-term audit summary

| Canonical term | Semantic category | Type audit result | Lifecycle class | MQL5 status | Python status | Authoritative source verified | Manual review status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Legacy | STATE_OR_RESULT | PASS (`STATE`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| LegacyMode | STATE_OR_RESULT | PASS (`STATE`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| LegacyBig | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| LegacySmall | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| LegacyFar | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| MonolithicBig | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| Split | STATE_OR_RESULT | PASS (`STATE`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| SplitMode | STATE_OR_RESULT | PASS (`STATE`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| SplitBig | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| BigCore | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| BigTrend | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| BigGross | LOT_VALUE | PASS (`LOT_CALCULATED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | BigGross corrected as projected lot sum |
| SmallBase | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| Hybrid | STATE_OR_RESULT | PASS (`STATE`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| HybridSplitBig | STATE_OR_RESULT | PASS (`STATE`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| HybridMode | STATE_OR_RESULT | PASS (`STATE`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| HybridPlan | STATE_OR_RESULT | PASS (`STATE`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| HybridPreview | STATE_OR_RESULT | PASS (`STATE`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| HybridExecution | STATE_OR_RESULT | PASS (`STATE`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| InitialBuy | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| InitialSell | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| InitialProfitLeg | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| InitialLosingLeg | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| InitialIgnoredProfit | MONEY_VALUE | PASS (`MONEY_REALIZED`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| OldFar | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| CurrentFar | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ResidualFar | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| NewFar | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| LegacyBigPosition | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| BigCorePosition | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| BigTrendPosition | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| LegacySmallPosition | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| SmallBasePosition | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ManagedPosition | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| UnmanagedPosition | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ForeignCyclePosition | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| FarDirection | STRUCTURED_OBJECT | PASS (`DIRECTION_ENUM`) | OBJECT | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| OppositeFarDirection | STRUCTURED_OBJECT | PASS (`DIRECTION_ENUM`) | OBJECT | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| SameAsFarDirection | STRUCTURED_OBJECT | PASS (`DIRECTION_ENUM`) | OBJECT | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| BigDirection | STRUCTURED_OBJECT | PASS (`DIRECTION_ENUM`) | OBJECT | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| SmallDirection | STRUCTURED_OBJECT | PASS (`DIRECTION_ENUM`) | OBJECT | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| TrendDirection | STRUCTURED_OBJECT | PASS (`DIRECTION_ENUM`) | OBJECT | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ReverseDirection | STRUCTURED_OBJECT | PASS (`DIRECTION_ENUM`) | OBJECT | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| RawLot | LOT_VALUE | PASS (`LOT_RAW`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| CalculatedLot | LOT_VALUE | PASS (`LOT_CALCULATED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| NormalizedLot | LOT_VALUE | PASS (`LOT_NORMALIZED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| RequestedLot | LOT_VALUE | PASS (`LOT_REQUESTED`) | REQUESTED | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| FilledLot | LOT_VALUE | PASS (`LOT_FILLED`) | DEAL | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ActualPositionLot | LOT_VALUE | PASS (`LOT_POSITION_ACTUAL`) | ACTUAL_POSITION | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ResidualLotProjected | LOT_VALUE | PASS (`LOT_RESIDUAL`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ResidualLotActual | LOT_VALUE | PASS (`LOT_POSITION_ACTUAL`) | ACTUAL_POSITION | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| FarLotRaw | LOT_VALUE | PASS (`LOT_RAW`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| FarLotCalculated | LOT_VALUE | PASS (`LOT_CALCULATED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| FarLotNormalized | LOT_VALUE | PASS (`LOT_NORMALIZED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| FarLotRequested | LOT_VALUE | PASS (`LOT_REQUESTED`) | REQUESTED | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| FarLotFilled | LOT_VALUE | PASS (`LOT_FILLED`) | DEAL | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| FarLotActual | LOT_VALUE | PASS (`LOT_POSITION_ACTUAL`) | ACTUAL_POSITION | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| BigCoreLotRaw | LOT_VALUE | PASS (`LOT_RAW`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| BigCoreLotNormalized | LOT_VALUE | PASS (`LOT_NORMALIZED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| BigCoreLotRequested | LOT_VALUE | PASS (`LOT_REQUESTED`) | REQUESTED | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| BigCoreLotFilled | LOT_VALUE | PASS (`LOT_FILLED`) | DEAL | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| BigCoreLotActual | LOT_VALUE | PASS (`LOT_POSITION_ACTUAL`) | ACTUAL_POSITION | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| BigTrendLotRaw | LOT_VALUE | PASS (`LOT_RAW`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| BigTrendLotNormalized | LOT_VALUE | PASS (`LOT_NORMALIZED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| SmallBaseLotRaw | LOT_VALUE | PASS (`LOT_RAW`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| SmallBaseLotNormalized | LOT_VALUE | PASS (`LOT_NORMALIZED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| PartialFarCloseLotCalculated | LOT_VALUE | PASS (`LOT_CALCULATED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| PartialFarCloseLotNormalized | LOT_VALUE | PASS (`LOT_NORMALIZED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| PartialFarCloseLotRequested | LOT_VALUE | PASS (`LOT_REQUESTED`) | REQUESTED | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| PartialFarCloseLotFilled | LOT_VALUE | PASS (`LOT_FILLED`) | DEAL | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| FarResidualProjected | LOT_VALUE | PASS (`LOT_RESIDUAL`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| FarResidualActual | LOT_VALUE | PASS (`LOT_POSITION_ACTUAL`) | ACTUAL_POSITION | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| NewFarCandidateLot | LOT_VALUE | PASS (`LOT_CALCULATED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| NewFarProjectedLot | LOT_VALUE | PASS (`LOT_RAW`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| NewFarNormalizedLot | LOT_VALUE | PASS (`LOT_NORMALIZED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| NewFarPromotedLot | LOT_VALUE | PASS (`LOT_NORMALIZED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| NewFarActualLot | LOT_VALUE | PASS (`LOT_POSITION_ACTUAL`) | ACTUAL_POSITION | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| Point | PRICE_OR_DISTANCE | PASS (`PRICE_POINT_SIZE`) | SYMBOL_PROPERTY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| TickSize | PRICE_OR_DISTANCE | PASS (`PRICE_TICK_SIZE`) | SYMBOL_PROPERTY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| TickValue | PRICE_OR_DISTANCE | PASS (`PRICE_PROJECTED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| MarketBidPrice | PRICE_OR_DISTANCE | PASS (`PRICE_BID`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| MarketAskPrice | PRICE_OR_DISTANCE | PASS (`PRICE_ASK`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| PositionOpenPrice | PRICE_OR_DISTANCE | PASS (`PRICE_OPEN`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| TriggerPrice | PRICE_OR_DISTANCE | PASS (`PRICE_PROJECTED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| TargetPrice | PRICE_OR_DISTANCE | PASS (`PRICE_PROJECTED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ControlPrice | PRICE_OR_DISTANCE | PASS (`PRICE_PROJECTED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ProjectedExitPrice | PRICE_OR_DISTANCE | PASS (`PRICE_PROJECTED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ExecutedDealPrice | PRICE_OR_DISTANCE | PASS (`PRICE_EXECUTED`) | DEAL | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| PriceDelta | PRICE_OR_DISTANCE | PASS (`PRICE_DELTA`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| DistancePoints | PRICE_OR_DISTANCE | PASS (`DISTANCE_POINTS`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| DistanceTicks | PRICE_OR_DISTANCE | PASS (`DISTANCE_TICKS`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| BidAwareClosePrice | PRICE_OR_DISTANCE | PASS (`PRICE_BID`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| AskAwareClosePrice | PRICE_OR_DISTANCE | PASS (`PRICE_ASK`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| FarOpenPriceActual | PRICE_OR_DISTANCE | PASS (`PRICE_OPEN`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| BigCoreOpenPriceActual | PRICE_OR_DISTANCE | PASS (`PRICE_OPEN`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| BigTrendOpenPriceActual | PRICE_OR_DISTANCE | PASS (`PRICE_OPEN`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| SmallBaseOpenPriceActual | PRICE_OR_DISTANCE | PASS (`PRICE_OPEN`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| GrossProfit | MONEY_VALUE | PASS (`MONEY_REALIZED`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| GrossLoss | MONEY_VALUE | PASS (`MONEY_REALIZED`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| NetProfit | MONEY_VALUE | PASS (`MONEY_REALIZED`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| LegNet | MONEY_VALUE | PASS (`MONEY_REALIZED`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| BasketNet | MONEY_VALUE | PASS (`MONEY_REALIZED`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| HarvestGross | MONEY_VALUE | PASS (`MONEY_REALIZED`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| HarvestNet | MONEY_VALUE | PASS (`MONEY_REALIZED`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| SmallReverseNet | MONEY_VALUE | PASS (`MONEY_REALIZED`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| TransitionNet | MONEY_VALUE | PASS (`MONEY_REALIZED`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| RealizedCyclePL | MONEY_VALUE | PASS (`MONEY_REALIZED`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| FloatingManagedPL | MONEY_VALUE | PASS (`MONEY_FLOATING`) | ACTUAL_POSITION | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ProjectedFloatingPL | MONEY_VALUE | PASS (`MONEY_PROJECTED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| RecoveryPLAnalytic | MONEY_VALUE | PASS (`MONEY_PROJECTED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| RecoveryPLProjected | MONEY_VALUE | PASS (`MONEY_PROJECTED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| RecoveryPLCloseNow | MONEY_VALUE | PASS (`MONEY_PROJECTED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| RealRecoveryPL | MONEY_VALUE | PASS (`MONEY_REALIZED`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| RecoverySlope | MONEY_VALUE | PASS (`MONEY_PROJECTED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| RecoveryMonotonicity | MONEY_VALUE | PASS (`MONEY_PROJECTED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ExpectedExitCosts | MONEY_VALUE | PASS (`MONEY_PROJECTED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| CommissionCost | MONEY_VALUE | PASS (`MONEY_COST`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| SwapCost | MONEY_VALUE | PASS (`MONEY_COST`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| FeeCost | MONEY_VALUE | PASS (`MONEY_COST`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| SpreadCost | MONEY_VALUE | PASS (`MONEY_COST`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| SlippageCost | MONEY_VALUE | PASS (`MONEY_COST`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| PositionPLSigned | MONEY_VALUE | PASS (`MONEY_FLOATING`) | ACTUAL_POSITION | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| FarLossSigned | MONEY_VALUE | PASS (`MONEY_REALIZED`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| FarLossMagnitude | MONEY_VALUE | PASS (`MONEY_REALIZED`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| PartialFarBudgetProjected | MONEY_VALUE | PASS (`MONEY_PROJECTED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| PartialFarBudgetReal | MONEY_VALUE | PASS (`MONEY_RESERVED`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| PartialFarBudgetAvailable | MONEY_VALUE | PASS (`MONEY_AVAILABLE`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| PartialFarBudgetConsumed | MONEY_VALUE | PASS (`MONEY_CONSUMED`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| PartialFarBudgetResidual | MONEY_VALUE | PASS (`MONEY_RESIDUAL`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| FinalReserveProjected | MONEY_VALUE | PASS (`MONEY_PROJECTED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| FinalReserveReal | MONEY_VALUE | PASS (`MONEY_RESERVED`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ReserveAddProjected | MONEY_VALUE | PASS (`MONEY_PROJECTED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ReserveAddReal | MONEY_VALUE | PASS (`MONEY_RESERVED`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ReserveAvailable | MONEY_VALUE | PASS (`MONEY_AVAILABLE`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ReserveConsumed | MONEY_VALUE | PASS (`MONEY_CONSUMED`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ReserveResidual | MONEY_VALUE | PASS (`MONEY_RESIDUAL`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| CarryAvailable | MONEY_VALUE | PASS (`MONEY_AVAILABLE`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| CarryConsumed | MONEY_VALUE | PASS (`MONEY_CONSUMED`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| CarryResidual | MONEY_VALUE | PASS (`MONEY_RESIDUAL`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| TransitionBudgetAvailable | MONEY_VALUE | PASS (`MONEY_AVAILABLE`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| FinalCloseRequirement | MONEY_VALUE | PASS (`MONEY_RESERVED`) | LEDGER | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| BasketRiskMoney | MONEY_VALUE | PASS (`MONEY_PROJECTED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| AccountRiskMoney | MONEY_VALUE | PASS (`MONEY_PROJECTED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| BigRatio | POLICY | PASS (`RATIO`) | POLICY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| SmallRatio | POLICY | PASS (`RATIO`) | POLICY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| CloseBigOnSmallShare | POLICY | PASS (`SHARE`) | POLICY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| RemainBigOnSmallShare | POLICY | PASS (`SHARE`) | POLICY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| CloseFarShare | POLICY | PASS (`SHARE`) | POLICY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ReserveShare | POLICY | PASS (`SHARE`) | POLICY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| SmallReserveShare | POLICY | PASS (`SHARE`) | POLICY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| CompressionRatio | POLICY | PASS (`RATIO`) | POLICY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ReserveCoverageRatio | POLICY | PASS (`RATIO`) | POLICY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| RecoveryCoverageRatio | POLICY | PASS (`RATIO`) | POLICY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| MaximumNewBigToOldFarRatio | POLICY | PASS (`RATIO`) | POLICY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| MinimumReserveCatchUpRatio | POLICY | PASS (`RATIO`) | POLICY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| PercentValue | POLICY | PASS (`PERCENT`) | POLICY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ScaleMultiplier | POLICY | PASS (`MULTIPLIER`) | POLICY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| RiskThresholdRatio | POLICY | PASS (`RATIO`) | POLICY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| SymbolId | IDENTITY | PASS (`SYMBOL_ID`) | IDENTITY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| MagicId | IDENTITY | PASS (`MAGIC_ID`) | IDENTITY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| CycleId | IDENTITY | PASS (`CYCLE_ID`) | IDENTITY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| RoleId | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| PositionIdentifier | IDENTITY | PASS (`POSITION_ID`) | IDENTITY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| PositionTicket | IDENTITY | PASS (`POSITION_TICKET`) | IDENTITY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| OrderTicket | IDENTITY | PASS (`ORDER_TICKET`) | IDENTITY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| DealTicket | IDENTITY | PASS (`DEAL_TICKET`) | IDENTITY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| EventId | IDENTITY | PASS (`EVENT_ID`) | IDENTITY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| EventKey | IDENTITY | PASS (`EVENT_ID`) | IDENTITY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| SnapshotFingerprint | IDENTITY | PASS (`FINGERPRINT`) | IDENTITY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| PlanFingerprint | IDENTITY | PASS (`FINGERPRINT`) | IDENTITY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| PositionComment | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| SnapshotRevision | ROLE | PASS (`ROLE_ID`) | ROLE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| StateRevision | IDENTITY | PASS (`EVENT_ID`) | IDENTITY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| State | STATE_OR_RESULT | PASS (`STATE`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| Phase | STATE_OR_RESULT | PASS (`PHASE`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| Event | STATE_OR_RESULT | PASS (`OUTCOME`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| Observation | STATE_OR_RESULT | PASS (`OUTCOME`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| GateResult | STATE_OR_RESULT | PASS (`GATE_RESULT`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ExecutionResult | STATE_OR_RESULT | PASS (`OUTCOME`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| Outcome | STATE_OR_RESULT | PASS (`OUTCOME`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ReasonCode | STATE_OR_RESULT | PASS (`REASON_CODE`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ErrorCode | STATE_OR_RESULT | PASS (`REASON_CODE`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| DiagnosticText | STATE_OR_RESULT | PASS (`OUTCOME`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| CandidatePlan | STATE_OR_RESULT | PASS (`OUTCOME`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ApprovedImmutablePlan | STATE_OR_RESULT | PASS (`OUTCOME`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ExecutionRequest | STATE_OR_RESULT | PASS (`OUTCOME`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| BrokerExecutionResult | STATE_OR_RESULT | PASS (`OUTCOME`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ReconciledResult | STATE_OR_RESULT | PASS (`OUTCOME`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| CommittedLedgerEvent | STATE_OR_RESULT | PASS (`OUTCOME`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| BaseSnapshot | STATE_OR_RESULT | PASS (`STATE`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| WorstSnapshot | STATE_OR_RESULT | PASS (`STATE`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ActualSnapshot | STATE_OR_RESULT | PASS (`STATE`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| SnapshotStaleFlag | STATE_OR_RESULT | PASS (`OUTCOME`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| FinalClosePreview | STATE_OR_RESULT | PASS (`OUTCOME`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| FinalCloseActualSuccess | STATE_OR_RESULT | PASS (`OUTCOME`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| MoneyTolerance | MONEY_VALUE | PASS (`MONEY_AVAILABLE`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| VolumeToleranceLots | LOT_VALUE | PASS (`LOT_NORMALIZED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| PriceTolerance | PRICE_OR_DISTANCE | PASS (`PRICE_PROJECTED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| PointTolerance | PRICE_OR_DISTANCE | PASS (`POINTS`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| RatioTolerance | POLICY | PASS (`RATIO`) | POLICY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ComparisonEpsilon | IDENTITY | PASS (`FINGERPRINT`) | IDENTITY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ReserveMismatchTolerance | MONEY_VALUE | PASS (`MONEY_AVAILABLE`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| GeometryTolerance | LOT_VALUE | PASS (`LOT_NORMALIZED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| FingerprintTolerance | IDENTITY | PASS (`FINGERPRINT`) | IDENTITY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ProjectedData | STRUCTURED_OBJECT | PASS (`BOOLEAN_RESULT`) | OBJECT | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| RequestedData | STRUCTURED_OBJECT | PASS (`BOOLEAN_RESULT`) | OBJECT | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ExecutedData | STRUCTURED_OBJECT | PASS (`BOOLEAN_RESULT`) | OBJECT | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ConfirmedData | STRUCTURED_OBJECT | PASS (`BOOLEAN_RESULT`) | OBJECT | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ReconciledData | STRUCTURED_OBJECT | PASS (`BOOLEAN_RESULT`) | OBJECT | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| PersistedData | STRUCTURED_OBJECT | PASS (`BOOLEAN_RESULT`) | OBJECT | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| StaleData | STRUCTURED_OBJECT | PASS (`BOOLEAN_RESULT`) | OBJECT | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| InvalidData | STRUCTURED_OBJECT | PASS (`BOOLEAN_RESULT`) | OBJECT | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| NotApplicableValue | STRUCTURED_OBJECT | PASS (`BOOLEAN_RESULT`) | OBJECT | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| NotCalculatedValue | STRUCTURED_OBJECT | PASS (`BOOLEAN_RESULT`) | OBJECT | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| NotAvailableValue | STRUCTURED_OBJECT | PASS (`BOOLEAN_RESULT`) | OBJECT | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| UnknownValue | STRUCTURED_OBJECT | PASS (`BOOLEAN_RESULT`) | OBJECT | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| CurrentBid | PRICE_OR_DISTANCE | PASS (`PRICE_BID`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| CurrentAsk | PRICE_OR_DISTANCE | PASS (`PRICE_ASK`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ReserveProjected | MONEY_VALUE | PASS (`MONEY_PROJECTED`) | PROJECTED_VALUE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ReserveCoverage | POLICY | PASS (`RATIO`) | POLICY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| Symbol | IDENTITY | PASS (`SYMBOL_ID`) | IDENTITY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| MagicNumber | IDENTITY | PASS (`MAGIC_ID`) | IDENTITY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| CycleID | IDENTITY | PASS (`CYCLE_ID`) | IDENTITY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| EventID | IDENTITY | PASS (`EVENT_ID`) | IDENTITY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| Fingerprint | IDENTITY | PASS (`FINGERPRINT`) | IDENTITY | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| Comment | STATE_OR_RESULT | PASS (`DIAGNOSTIC_TEXT`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| Preview | STATE_OR_RESULT | PASS (`PHASE`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| Candidate | STATE_OR_RESULT | PASS (`OUTCOME`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| Plan | STATE_OR_RESULT | PASS (`STATE`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |
| ApprovedPlan | STATE_OR_RESULT | PASS (`STATE`) | STATE | MISSING | MISSING | PASS | PASS | type/unit/class/source/tolerance/lifecycle contract checked |

## Final status

```text
SUMMARY
STAGE=3.1.3_SECOND_CORRECTION
STATUS=PASS
BASE_COMMIT=6026b44d4e6d83f509b91a254b7313124dc2aad3

SCOPE
FILES_OUTSIDE_PROJECT=0
MQL5_CHANGED=NO
MQH_CHANGED=NO
TRADING_LOGIC_CHANGED=NO
STAGE_3_1_4_STARTED=NO

SEMANTIC_TYPE_AUDIT
CANONICAL_TERMS=230
TERMS_AUDITED=230
BIG_GROSS_TYPE=PASS
INVALID_DEFINITION_TYPE_SEMANTICS=0
INVALID_TYPE_UNIT=0
INVALID_TYPE_CLASS=0
INVALID_TYPE_TOLERANCE=0
INVALID_TYPE_SOURCE=0
INVALID_LIFECYCLE_CLASS=0

MAPPING_EVIDENCE
TOKEN_IDENTIFIER_KINDS=0
MAPPING_WITHOUT_DECLARATION_EVIDENCE=0
MAPPING_WITHOUT_USE_EVIDENCE=0
IDENTIFIER_ONLY_IN_COMMENT=0
IDENTIFIER_ONLY_IN_STRING=0
UNPROVEN_EXACT_MAPPING=0
UNPROVEN_SEMANTIC_MAPPING=0
CACHE_MARKED_AUTHORITATIVE=0
MISSING_NOT_APPLICABLE_CONFLICT=0

LIFECYCLE_AUDIT
NORMALIZED_DUPLICATE_LIFECYCLES=0
GENERIC_LIFECYCLES=0
MISSING_CREATION_EVENT=0
MISSING_STALE_TRIGGER=0
MISSING_REPLACEMENT_SOURCE=0
MISSING_TERMINAL_CONDITION=0

DEFINITION_AUDIT
NEAR_DUPLICATE_DEFINITIONS=0
DEFINITIONS_WITHOUT_DISTINGUISHING_CLAUSE=0

TESTING
NEGATIVE_TESTS_TOTAL=20
NEGATIVE_TESTS_PASSED=20
POSITIVE_TESTS_TOTAL=10
POSITIVE_TESTS_PASSED=10
VALIDATOR_RESULT=PASS
```

STAGE_3_1_3_SECOND_CORRECTION_STATUS=PASS
Этап 3.1.3 ожидает повторную независимую проверку пользователя.
Этап 3.1.4 не выполнялся.
