# Отчёт третьей коррекции Этапа 3.1.3

## Причина и защита от vacuous PASS

Каждый из 230 терминов связан с отдельным audit для MQL5 и Python. `MISSING` требует generated candidates, завершённый поиск, inspected files и классификацию каждого найденного candidate. Полный `MISSING`, coverage ниже 25, accepted candidate без mapping entry и рассинхронизация отдельного audit JSON блокируют validator.

## Candidate generation, declaration/use proof and scoring

Variants строятся из canonical/alias, camel/Pascal/snake и смысловых suffix. MQL5 evidence указывает declaration line вне comments/strings и read/write sites; Python evidence подтверждается `ast`. После дополнительного semantic-key review generic совпадения (`current`, `result` и аналогичные) отклонены, если declaration/type/context не содержит отличительного компонента canonical entity. Поэтому статистика ниже меньше первоначальной и не максимизирует `PARTIAL_MATCH`.

Score учитывает name, family/type, source, lifecycle, scope и projected/actual признаки. Score не создаёт `EXACT_MATCH`: все принятые связи остаются `PARTIAL_MATCH`, пока authoritative и полный lifecycle contract не доказаны.

## Candidate audit totals

```text
MQL5_FOUND_CANDIDATES=1504
MQL5_ACCEPTED_CANDIDATES=98
MQL5_REJECTED_CANDIDATES=1406
PYTHON_FOUND_CANDIDATES=1232
PYTHON_ACCEPTED_CANDIDATES=80
PYTHON_REJECTED_CANDIDATES=1152
MQL5_MANUAL_MAPPING_REVIEWS=30
PYTHON_MANUAL_MAPPING_REVIEWS=30
```

## Semantic contract audit

Definition family, Type, Unit, Sign, Projected/Actual class, source matrix and lifecycle matrix валидируются независимо. Position terms не допускают `ROLE_ID` без substantive exception; plan/preview/execution objects не допускают state masquerading. Similarity использует Jaccard и `SequenceMatcher` с порогом 0.85. Structured lifecycle exceptions требуют явной причины.

## Manual mapping audit

`MANUAL_REVIEWED` ниже означает: reviewer=`agent`; evidence=конкретная declaration/use entry либо документированный rejection audit; decision=указанный final status. Остальные строки имеют только `VALIDATOR_VERIFIED`, без декларативного заявления о ручном review.

## Per-term candidate and semantic audit

| Canonical term | Semantic category | Type | Sign audit | Source audit | Lifecycle audit | MQL5 found | MQL5 accepted | MQL5 rejected | MQL5 status | Python found | Python accepted | Python rejected | Python status | Review evidence and decision |
| --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- | --- |
| Legacy | STATE_OR_RESULT | `STATE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 6 | 0 | 6 | MISSING | 1 | 0 | 1 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| LegacyMode | STATE_OR_RESULT | `STATE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 7 | 0 | 7 | MISSING | 3 | 0 | 3 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| LegacyBig | ROLE | `ROLE_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 5 | 0 | 5 | MISSING | 3 | 0 | 3 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| LegacySmall | ROLE | `ROLE_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| LegacyFar | ROLE | `ROLE_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 2 | 0 | 2 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| MonolithicBig | ROLE | `ROLE_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 0 | 0 | 0 | MISSING | 0 | 0 | 0 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| Split | STATE_OR_RESULT | `STATE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 5 | 0 | 5 | MISSING | 5 | 0 | 5 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| SplitMode | STATE_OR_RESULT | `STATE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 7 | 0 | 7 | MISSING | 3 | 0 | 3 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| SplitBig | ROLE | `ROLE_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 5 | 0 | 5 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| BigCore | ROLE | `ROLE_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| BigTrend | ROLE | `ROLE_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| BigGross | LOT_VALUE | `LOT_CALCULATED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 0 | 8 | MISSING | MANUAL_REVIEWED: agent; MQL5 evidence=Include/Types.mqh:990::nextBigGross; declaration/use checked; decision=PARTIAL_MATCH |
| SmallBase | ROLE | `ROLE_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| Hybrid | STATE_OR_RESULT | `STATE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 1 | 0 | 1 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| HybridSplitBig | STATE_OR_RESULT | `STATE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 5 | 0 | 5 | MISSING | 2 | 0 | 2 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| HybridMode | STATE_OR_RESULT | `STATE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 3 | 0 | 3 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| HybridPlan | STRUCTURED_OBJECT | `PLAN_OBJECT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 7 | 0 | 7 | MISSING | 3 | 0 | 3 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| HybridPreview | STRUCTURED_OBJECT | `PREVIEW_OBJECT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 1 | 0 | 1 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| HybridExecution | STRUCTURED_OBJECT | `EXECUTION_OBJECT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 6 | 0 | 6 | MISSING | 2 | 0 | 2 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| InitialBuy | ROLE | `ROLE_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 2 | 0 | 2 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| InitialSell | ROLE | `ROLE_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 5 | 0 | 5 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| InitialProfitLeg | ROLE | `ROLE_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 4 | 0 | 4 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| InitialLosingLeg | ROLE | `ROLE_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 6 | 0 | 6 | MISSING | 4 | 0 | 4 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| InitialIgnoredProfit | MONEY_VALUE | `MONEY_REALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| OldFar | ROLE | `ROLE_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 5 | 0 | 5 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| CurrentFar | ROLE | `ROLE_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 7 | 0 | 7 | MISSING | 5 | 0 | 5 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ResidualFar | ROLE | `ROLE_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 3 | 0 | 3 | MISSING | 1 | 0 | 1 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| NewFar | ROLE | `ROLE_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| LegacyBigPosition | IDENTITY | `POSITION_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 2 | 0 | 2 | MISSING | MANUAL_REVIEWED: agent; MQL5 evidence=Include/StateMachine.mqh:3568::bigPositionId; declaration/use checked; decision=PARTIAL_MATCH |
| BigCorePosition | IDENTITY | `POSITION_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 5 | 0 | 5 | MISSING | MANUAL_REVIEWED: agent; MQL5 evidence=Include/ReconciliationEngine.mqh:168::ValidateBigCorePosition; declaration/use checked; decision=PARTIAL_MATCH |
| BigTrendPosition | IDENTITY | `POSITION_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 6 | 0 | 6 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| LegacySmallPosition | IDENTITY | `POSITION_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 0 | 0 | 0 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| SmallBasePosition | IDENTITY | `POSITION_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ManagedPosition | IDENTITY | `POSITION_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| UnmanagedPosition | IDENTITY | `POSITION_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 6 | 0 | 6 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ForeignCyclePosition | IDENTITY | `POSITION_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 0 | 0 | 0 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| FarDirection | STRUCTURED_OBJECT | `DIRECTION_ENUM` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| OppositeFarDirection | STRUCTURED_OBJECT | `DIRECTION_ENUM` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 6 | 1 | 5 | PARTIAL_MATCH | 4 | 0 | 4 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| SameAsFarDirection | STRUCTURED_OBJECT | `DIRECTION_ENUM` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 6 | 1 | 5 | PARTIAL_MATCH | 5 | 0 | 5 | MISSING | MANUAL_REVIEWED: agent; MQL5 evidence=Include/Types.mqh:508::farDirection; declaration/use checked; decision=PARTIAL_MATCH |
| BigDirection | STRUCTURED_OBJECT | `DIRECTION_ENUM` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| SmallDirection | STRUCTURED_OBJECT | `DIRECTION_ENUM` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 0 | 8 | MISSING | MANUAL_REVIEWED: agent; MQL5 evidence=Include/Types.mqh:510::smallDirection; declaration/use checked; decision=PARTIAL_MATCH |
| TrendDirection | STRUCTURED_OBJECT | `DIRECTION_ENUM` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ReverseDirection | STRUCTURED_OBJECT | `DIRECTION_ENUM` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 1 | 7 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; Python evidence=Tests/test_dynamic_reverse_small_direction.py:2::reverse_direction; AST declaration/use checked; decision=PARTIAL_MATCH |
| RawLot | LOT_VALUE | `LOT_RAW` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| CalculatedLot | LOT_VALUE | `LOT_CALCULATED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| NormalizedLot | LOT_VALUE | `LOT_NORMALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| RequestedLot | LOT_VALUE | `LOT_REQUESTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| FilledLot | LOT_VALUE | `LOT_FILLED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ActualPositionLot | LOT_VALUE | `LOT_POSITION_ACTUAL` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ResidualLotProjected | LOT_VALUE | `LOT_RESIDUAL` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 4 | 0 | 4 | MISSING | 0 | 0 | 0 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ResidualLotActual | LOT_VALUE | `LOT_POSITION_ACTUAL` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 6 | 0 | 6 | MISSING | 2 | 0 | 2 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| FarLotRaw | LOT_VALUE | `LOT_RAW` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| FarLotCalculated | LOT_VALUE | `LOT_CALCULATED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| FarLotNormalized | LOT_VALUE | `LOT_NORMALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| FarLotRequested | LOT_VALUE | `LOT_REQUESTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| FarLotFilled | LOT_VALUE | `LOT_FILLED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| FarLotActual | LOT_VALUE | `LOT_POSITION_ACTUAL` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; MQL5 evidence=Include/Types.mqh:496::farLot; declaration/use checked; decision=PARTIAL_MATCH; MANUAL_REVIEWED: agent; Python evidence=Tools/hybrid_geometry_model.py:96::far_lot; AST declaration/use checked; decision=PARTIAL_MATCH |
| BigCoreLotRaw | LOT_VALUE | `LOT_RAW` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; MQL5 evidence=Include/Logger.mqh:183::closeBigLotRaw; declaration/use checked; decision=PARTIAL_MATCH; MANUAL_REVIEWED: agent; Python evidence=Tools/hybrid_geometry_model.py:51::core_lot; AST declaration/use checked; decision=PARTIAL_MATCH |
| BigCoreLotNormalized | LOT_VALUE | `LOT_NORMALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| BigCoreLotRequested | LOT_VALUE | `LOT_REQUESTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| BigCoreLotFilled | LOT_VALUE | `LOT_FILLED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| BigCoreLotActual | LOT_VALUE | `LOT_POSITION_ACTUAL` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| BigTrendLotRaw | LOT_VALUE | `LOT_RAW` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; MQL5 evidence=Include/Types.mqh:940::trendLot; declaration/use checked; decision=PARTIAL_MATCH; MANUAL_REVIEWED: agent; Python evidence=Tools/hybrid_geometry_model.py:52::trend_lot; AST declaration/use checked; decision=PARTIAL_MATCH |
| BigTrendLotNormalized | LOT_VALUE | `LOT_NORMALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 6 | 0 | 6 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| SmallBaseLotRaw | LOT_VALUE | `LOT_RAW` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| SmallBaseLotNormalized | LOT_VALUE | `LOT_NORMALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| PartialFarCloseLotCalculated | LOT_VALUE | `LOT_CALCULATED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| PartialFarCloseLotNormalized | LOT_VALUE | `LOT_NORMALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| PartialFarCloseLotRequested | LOT_VALUE | `LOT_REQUESTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| PartialFarCloseLotFilled | LOT_VALUE | `LOT_FILLED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| FarResidualProjected | LOT_VALUE | `LOT_RESIDUAL` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 7 | 0 | 7 | MISSING | 0 | 0 | 0 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| FarResidualActual | LOT_VALUE | `LOT_POSITION_ACTUAL` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 4 | 0 | 4 | MISSING | 1 | 0 | 1 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| NewFarCandidateLot | LOT_VALUE | `LOT_CALCULATED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| NewFarProjectedLot | LOT_VALUE | `LOT_RAW` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 0 | 8 | MISSING | MANUAL_REVIEWED: agent; MQL5 evidence=Include/BrokerMoneyModel.mqh:19::projectedNewFarLot; declaration/use checked; decision=PARTIAL_MATCH |
| NewFarNormalizedLot | LOT_VALUE | `LOT_NORMALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| NewFarPromotedLot | LOT_VALUE | `LOT_NORMALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| NewFarActualLot | LOT_VALUE | `LOT_POSITION_ACTUAL` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| Point | PRICE_OR_DISTANCE | `PRICE_POINT_SIZE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 3 | 1 | 2 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| TickSize | PRICE_OR_DISTANCE | `PRICE_TICK_SIZE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 3 | 1 | 2 | PARTIAL_MATCH | 4 | 0 | 4 | MISSING | MANUAL_REVIEWED: agent; MQL5 evidence=Include/SimulationEngine.mqh:48::tickSize; declaration/use checked; decision=PARTIAL_MATCH |
| TickValue | PRICE_OR_DISTANCE | `PRICE_PROJECTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 7 | 1 | 6 | PARTIAL_MATCH | 4 | 0 | 4 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| MarketBidPrice | PRICE_OR_DISTANCE | `PRICE_BID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 1 | 0 | 1 | MISSING | 2 | 0 | 2 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| MarketAskPrice | PRICE_OR_DISTANCE | `PRICE_ASK` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 1 | 0 | 1 | MISSING | 1 | 0 | 1 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| PositionOpenPrice | PRICE_OR_DISTANCE | `PRICE_OPEN` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| TriggerPrice | PRICE_OR_DISTANCE | `PRICE_PROJECTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 4 | 0 | 4 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| TargetPrice | PRICE_OR_DISTANCE | `PRICE_PROJECTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 7 | 0 | 7 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ControlPrice | PRICE_OR_DISTANCE | `PRICE_PROJECTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 3 | 0 | 3 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ProjectedExitPrice | PRICE_OR_DISTANCE | `PRICE_PROJECTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 7 | 0 | 7 | MISSING | 1 | 0 | 1 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ExecutedDealPrice | PRICE_OR_DISTANCE | `PRICE_EXECUTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 2 | 0 | 2 | MISSING | 0 | 0 | 0 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| PriceDelta | PRICE_OR_DISTANCE | `PRICE_DELTA` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 2 | 0 | 2 | MISSING | 4 | 0 | 4 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| DistancePoints | PRICE_OR_DISTANCE | `DISTANCE_POINTS` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| DistanceTicks | PRICE_OR_DISTANCE | `DISTANCE_TICKS` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 4 | 0 | 4 | MISSING | 5 | 0 | 5 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| BidAwareClosePrice | PRICE_OR_DISTANCE | `PRICE_BID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 6 | 0 | 6 | MISSING | 0 | 0 | 0 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| AskAwareClosePrice | PRICE_OR_DISTANCE | `PRICE_ASK` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 4 | 0 | 4 | MISSING | 0 | 0 | 0 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| FarOpenPriceActual | PRICE_OR_DISTANCE | `PRICE_OPEN` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 7 | 1 | 6 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; MQL5 evidence=Include/Types.mqh:500::farOpenPrice; declaration/use checked; decision=PARTIAL_MATCH; MANUAL_REVIEWED: agent; Python evidence=Tests/small_at_far_scenario_log.py:12::far_open_price; AST declaration/use checked; decision=PARTIAL_MATCH |
| BigCoreOpenPriceActual | PRICE_OR_DISTANCE | `PRICE_OPEN` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 4 | 0 | 4 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| BigTrendOpenPriceActual | PRICE_OR_DISTANCE | `PRICE_OPEN` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 5 | 0 | 5 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| SmallBaseOpenPriceActual | PRICE_OR_DISTANCE | `PRICE_OPEN` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 7 | 1 | 6 | PARTIAL_MATCH | 1 | 0 | 1 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| GrossProfit | MONEY_VALUE | `MONEY_REALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| GrossLoss | MONEY_VALUE | `MONEY_REALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| NetProfit | MONEY_VALUE | `MONEY_REALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| LegNet | MONEY_VALUE | `MONEY_REALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 7 | 1 | 6 | PARTIAL_MATCH | 8 | 0 | 8 | MISSING | MANUAL_REVIEWED: agent; MQL5 evidence=Include/StateMachine.mqh:5511::legNet; declaration/use checked; decision=PARTIAL_MATCH |
| BasketNet | MONEY_VALUE | `MONEY_REALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 5 | 0 | 5 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| HarvestGross | MONEY_VALUE | `MONEY_REALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| HarvestNet | MONEY_VALUE | `MONEY_REALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 6 | 1 | 5 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; MQL5 evidence=Include/Types.mqh:1104::harvestNet; declaration/use checked; decision=PARTIAL_MATCH; MANUAL_REVIEWED: agent; Python evidence=Tools/hybrid_big_sequence_model.py:23::harvest; AST declaration/use checked; decision=PARTIAL_MATCH |
| SmallReverseNet | MONEY_VALUE | `MONEY_REALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| TransitionNet | MONEY_VALUE | `MONEY_REALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| RealizedCyclePL | MONEY_VALUE | `MONEY_REALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 3 | 1 | 2 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; Python evidence=Tools/hybrid_small_state_machine.py:11::realized_cycle_pl; AST declaration/use checked; decision=PARTIAL_MATCH |
| FloatingManagedPL | MONEY_VALUE | `MONEY_FLOATING` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 2 | 1 | 1 | PARTIAL_MATCH | 2 | 0 | 2 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ProjectedFloatingPL | MONEY_VALUE | `MONEY_PROJECTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 3 | 0 | 3 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| RecoveryPLAnalytic | MONEY_VALUE | `MONEY_PROJECTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| RecoveryPLProjected | MONEY_VALUE | `MONEY_PROJECTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; MQL5 evidence=Include/Logger.mqh:345::recoveryPL; declaration/use checked; decision=PARTIAL_MATCH; MANUAL_REVIEWED: agent; Python evidence=Tests/real_recovery_examples_check.py:7::recovery_pl; AST declaration/use checked; decision=PARTIAL_MATCH |
| RecoveryPLCloseNow | MONEY_VALUE | `MONEY_PROJECTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| RealRecoveryPL | MONEY_VALUE | `MONEY_REALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| RecoverySlope | MONEY_VALUE | `MONEY_PROJECTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| RecoveryMonotonicity | MONEY_VALUE | `MONEY_PROJECTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 6 | 0 | 6 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ExpectedExitCosts | MONEY_VALUE | `MONEY_PROJECTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 7 | 0 | 7 | MISSING | 7 | 0 | 7 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| CommissionCost | MONEY_VALUE | `MONEY_COST` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| SwapCost | MONEY_VALUE | `MONEY_COST` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 6 | 0 | 6 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| FeeCost | MONEY_VALUE | `MONEY_COST` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 5 | 0 | 5 | MISSING | MANUAL_REVIEWED: agent; MQL5 evidence=Include/HybridPartialFarPreview.mqh:52::cost; declaration/use checked; decision=PARTIAL_MATCH |
| SpreadCost | MONEY_VALUE | `MONEY_COST` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 6 | 0 | 6 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| SlippageCost | MONEY_VALUE | `MONEY_COST` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 5 | 1 | 4 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; MQL5 evidence=Include/BrokerMoneyModel.mqh:19::slippage; declaration/use checked; decision=PARTIAL_MATCH; MANUAL_REVIEWED: agent; Python evidence=Tests/unit/test_big_small_behavior.py:155::slippage; AST declaration/use checked; decision=PARTIAL_MATCH |
| PositionPLSigned | MONEY_VALUE | `MONEY_FLOATING` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 7 | 1 | 6 | PARTIAL_MATCH | 3 | 0 | 3 | MISSING | MANUAL_REVIEWED: agent; MQL5 evidence=Include/SimulationEngine.mqh:57::SimSignedPositionPL; declaration/use checked; decision=PARTIAL_MATCH |
| FarLossSigned | MONEY_VALUE | `MONEY_REALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| FarLossMagnitude | MONEY_VALUE | `MONEY_REALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| PartialFarBudgetProjected | MONEY_VALUE | `MONEY_PROJECTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 6 | 1 | 5 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; Python evidence=Tools/hybrid_big_sequence_model.py:28::partial_budget; AST declaration/use checked; decision=PARTIAL_MATCH |
| PartialFarBudgetReal | MONEY_VALUE | `MONEY_RESERVED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; MQL5 evidence=Include/Types.mqh:1106::partialBudgetBefore; declaration/use checked; decision=PARTIAL_MATCH; MANUAL_REVIEWED: agent; Python evidence=Tools/hybrid_big_sequence_model.py:28::partial_budget; AST declaration/use checked; decision=PARTIAL_MATCH |
| PartialFarBudgetAvailable | MONEY_VALUE | `MONEY_AVAILABLE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; Python evidence=Tools/hybrid_big_sequence_model.py:28::partial_budget; AST declaration/use checked; decision=PARTIAL_MATCH |
| PartialFarBudgetConsumed | MONEY_VALUE | `MONEY_CONSUMED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 1 | 7 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; Python evidence=Tools/hybrid_big_sequence_model.py:28::partial_budget; AST declaration/use checked; decision=PARTIAL_MATCH |
| PartialFarBudgetResidual | MONEY_VALUE | `MONEY_RESIDUAL` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| FinalReserveProjected | MONEY_VALUE | `MONEY_PROJECTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| FinalReserveReal | MONEY_VALUE | `MONEY_RESERVED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ReserveAddProjected | MONEY_VALUE | `MONEY_PROJECTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ReserveAddReal | MONEY_VALUE | `MONEY_RESERVED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; Python evidence=Tools/optimize_big_scenario_min_levels.py:213::reserve_add; AST declaration/use checked; decision=PARTIAL_MATCH |
| ReserveAvailable | MONEY_VALUE | `MONEY_AVAILABLE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ReserveConsumed | MONEY_VALUE | `MONEY_CONSUMED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 0 | 8 | MISSING | MANUAL_REVIEWED: agent; MQL5 evidence=Include/StateMachine.mqh:4227::reserveUsed; declaration/use checked; decision=PARTIAL_MATCH |
| ReserveResidual | MONEY_VALUE | `MONEY_RESIDUAL` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| CarryAvailable | MONEY_VALUE | `MONEY_AVAILABLE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 5 | 0 | 5 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| CarryConsumed | MONEY_VALUE | `MONEY_CONSUMED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 4 | 0 | 4 | MISSING | 4 | 0 | 4 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| CarryResidual | MONEY_VALUE | `MONEY_RESIDUAL` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 4 | 0 | 4 | MISSING | 2 | 0 | 2 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| TransitionBudgetAvailable | MONEY_VALUE | `MONEY_AVAILABLE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 5 | 1 | 4 | PARTIAL_MATCH | 7 | 1 | 6 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| FinalCloseRequirement | MONEY_VALUE | `MONEY_RESERVED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| BasketRiskMoney | MONEY_VALUE | `MONEY_PROJECTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 6 | 0 | 6 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| AccountRiskMoney | MONEY_VALUE | `MONEY_PROJECTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 6 | 0 | 6 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| BigRatio | POLICY | `RATIO` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| SmallRatio | POLICY | `RATIO` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| CloseBigOnSmallShare | POLICY | `SHARE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; Python evidence=Tests/small_reverse_compression_check.py:7::close_big_on_small; AST declaration/use checked; decision=PARTIAL_MATCH |
| RemainBigOnSmallShare | POLICY | `SHARE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 5 | 1 | 4 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; MQL5 evidence=Include/RecoveryMath.mqh:318::remainBigOnSmall; declaration/use checked; decision=PARTIAL_MATCH; MANUAL_REVIEWED: agent; Python evidence=Tests/small_reverse_compression_check.py:1::remain_big_on_small; AST declaration/use checked; decision=PARTIAL_MATCH |
| CloseFarShare | POLICY | `SHARE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; Python evidence=Tools/optimize_big_scenario_min_levels.py:86::close_far_share; AST declaration/use checked; decision=PARTIAL_MATCH |
| ReserveShare | POLICY | `SHARE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| SmallReserveShare | POLICY | `SHARE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 6 | 1 | 5 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| CompressionRatio | POLICY | `RATIO` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 6 | 1 | 5 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; MQL5 evidence=Include/BrokerMoneyModel.mqh:19::compressionRatio; declaration/use checked; decision=PARTIAL_MATCH; MANUAL_REVIEWED: agent; Python evidence=Tools/offline_optimizer.py:107::compression_ratio; AST declaration/use checked; decision=PARTIAL_MATCH |
| ReserveCoverageRatio | POLICY | `RATIO` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 6 | 1 | 5 | PARTIAL_MATCH | 7 | 1 | 6 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; MQL5 evidence=Include/StateMachine.mqh:4755::reserveCoverage; declaration/use checked; decision=PARTIAL_MATCH; MANUAL_REVIEWED: agent; Python evidence=Tools/run_full_parameter_optimization_study.py:290::reserve_coverage; AST declaration/use checked; decision=PARTIAL_MATCH |
| RecoveryCoverageRatio | POLICY | `RATIO` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 2 | 0 | 2 | MISSING | 3 | 1 | 2 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| MaximumNewBigToOldFarRatio | POLICY | `RATIO` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 3 | 0 | 3 | MISSING | 5 | 1 | 4 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; Python evidence=Tools/offline_optimizer.py:108::new_big_to_old_far_ratio; AST declaration/use checked; decision=PARTIAL_MATCH |
| MinimumReserveCatchUpRatio | POLICY | `RATIO` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 6 | 0 | 6 | MISSING | 0 | 0 | 0 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| PercentValue | POLICY | `PERCENT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 6 | 0 | 6 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ScaleMultiplier | POLICY | `MULTIPLIER` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 6 | 1 | 5 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| RiskThresholdRatio | POLICY | `RATIO` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 0 | 0 | 0 | MISSING | 0 | 0 | 0 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| SymbolId | IDENTITY | `SYMBOL_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| MagicId | IDENTITY | `MAGIC_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 7 | 0 | 7 | MISSING | MANUAL_REVIEWED: agent; MQL5 evidence=Include/Types.mqh:923::magic; declaration/use checked; decision=PARTIAL_MATCH |
| CycleId | IDENTITY | `CYCLE_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; MQL5 evidence=Include/Types.mqh:166::cycleId; declaration/use checked; decision=PARTIAL_MATCH; MANUAL_REVIEWED: agent; Python evidence=Tests/HybridSplitBig/test_catchup_route_hardening.py:11::cycle; AST declaration/use checked; decision=PARTIAL_MATCH |
| RoleId | ROLE | `ROLE_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 7 | 0 | 7 | MISSING | 4 | 0 | 4 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| PositionIdentifier | IDENTITY | `POSITION_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 4 | 1 | 3 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| PositionTicket | IDENTITY | `POSITION_TICKET` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 5 | 0 | 5 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| OrderTicket | IDENTITY | `ORDER_TICKET` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 2 | 1 | 1 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; Python evidence=Tests/unit/test_split_final_safety_model.py:27::ticket; AST declaration/use checked; decision=PARTIAL_MATCH |
| DealTicket | IDENTITY | `DEAL_TICKET` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 1 | 1 | 0 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| EventId | IDENTITY | `EVENT_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| EventKey | IDENTITY | `EVENT_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| SnapshotFingerprint | IDENTITY | `FINGERPRINT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 5 | 1 | 4 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; Python evidence=Tests/HybridSplitBig/test_catchup_dimension_safe.py:13::fingerprint; AST declaration/use checked; decision=PARTIAL_MATCH |
| PlanFingerprint | IDENTITY | `FINGERPRINT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 3 | 1 | 2 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| PositionComment | STATE_OR_RESULT | `DIAGNOSTIC_TEXT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 7 | 0 | 7 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| SnapshotRevision | IDENTITY | `EVENT_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 4 | 0 | 4 | MISSING | 2 | 0 | 2 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| StateRevision | IDENTITY | `EVENT_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 7 | 1 | 6 | PARTIAL_MATCH | 5 | 0 | 5 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| State | STATE_OR_RESULT | `STATE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| Phase | STATE_OR_RESULT | `PHASE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 4 | 1 | 3 | PARTIAL_MATCH | 6 | 1 | 5 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| Event | STATE_OR_RESULT | `OUTCOME` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 7 | 0 | 7 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| Observation | STATE_OR_RESULT | `OUTCOME` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 0 | 0 | 0 | MISSING | 0 | 0 | 0 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| GateResult | STATE_OR_RESULT | `GATE_RESULT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 4 | 0 | 4 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ExecutionResult | STATE_OR_RESULT | `OUTCOME` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 6 | 0 | 6 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| Outcome | STATE_OR_RESULT | `OUTCOME` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 5 | 1 | 4 | PARTIAL_MATCH | 3 | 1 | 2 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ReasonCode | STATE_OR_RESULT | `REASON_CODE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ErrorCode | STATE_OR_RESULT | `REASON_CODE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 5 | 1 | 4 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| DiagnosticText | STATE_OR_RESULT | `OUTCOME` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 0 | 0 | 0 | MISSING | 2 | 0 | 2 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| CandidatePlan | STATE_OR_RESULT | `OUTCOME` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 3 | 0 | 3 | MISSING | 7 | 0 | 7 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ApprovedImmutablePlan | STATE_OR_RESULT | `OUTCOME` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 0 | 0 | 0 | MISSING | 0 | 0 | 0 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ExecutionRequest | STATE_OR_RESULT | `OUTCOME` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 7 | 0 | 7 | MISSING | 2 | 0 | 2 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| BrokerExecutionResult | STATE_OR_RESULT | `OUTCOME` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 5 | 0 | 5 | MISSING | 4 | 0 | 4 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ReconciledResult | STATE_OR_RESULT | `OUTCOME` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 4 | 0 | 4 | MISSING | 5 | 0 | 5 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| CommittedLedgerEvent | STATE_OR_RESULT | `OUTCOME` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 1 | 0 | 1 | MISSING | 0 | 0 | 0 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| BaseSnapshot | STATE_OR_RESULT | `STATE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| WorstSnapshot | STATE_OR_RESULT | `STATE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 7 | 0 | 7 | MISSING | 5 | 0 | 5 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ActualSnapshot | STATE_OR_RESULT | `STATE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 7 | 0 | 7 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| SnapshotStaleFlag | STATE_OR_RESULT | `OUTCOME` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 2 | 0 | 2 | MISSING | 2 | 0 | 2 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| FinalClosePreview | STATE_OR_RESULT | `OUTCOME` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 7 | 0 | 7 | MISSING | MANUAL_REVIEWED: agent; MQL5 evidence=Include/Types.mqh:1116::finalClosePreviewRequired; declaration/use checked; decision=PARTIAL_MATCH |
| FinalCloseActualSuccess | STATE_OR_RESULT | `OUTCOME` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 4 | 0 | 4 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| MoneyTolerance | MONEY_VALUE | `MONEY_AVAILABLE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| VolumeToleranceLots | LOT_VALUE | `LOT_NORMALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 2 | 0 | 2 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| PriceTolerance | PRICE_OR_DISTANCE | `PRICE_PROJECTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 6 | 1 | 5 | PARTIAL_MATCH | 4 | 1 | 3 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; MQL5 evidence=Include/HybridCatchUpModel.mqh:398::priceTolerance; declaration/use checked; decision=PARTIAL_MATCH; MANUAL_REVIEWED: agent; Python evidence=Tests/HybridSplitBig/test_catchup_dimension_safe.py:11::price_tolerance; AST declaration/use checked; decision=PARTIAL_MATCH |
| PointTolerance | PRICE_OR_DISTANCE | `POINTS` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 5 | 0 | 5 | MISSING | 5 | 0 | 5 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| RatioTolerance | POLICY | `RATIO` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 7 | 1 | 6 | PARTIAL_MATCH | 7 | 0 | 7 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ComparisonEpsilon | IDENTITY | `FINGERPRINT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 0 | 0 | 0 | MISSING | 0 | 0 | 0 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ReserveMismatchTolerance | MONEY_VALUE | `MONEY_AVAILABLE` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| GeometryTolerance | LOT_VALUE | `LOT_NORMALIZED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 6 | 0 | 6 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| FingerprintTolerance | IDENTITY | `FINGERPRINT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 6 | 1 | 5 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; Python evidence=Tests/HybridSplitBig/test_catchup_dimension_safe.py:13::fingerprint; AST declaration/use checked; decision=PARTIAL_MATCH |
| ProjectedData | STRUCTURED_OBJECT | `BOOLEAN_RESULT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 6 | 0 | 6 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| RequestedData | STRUCTURED_OBJECT | `BOOLEAN_RESULT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 1 | 0 | 1 | MISSING | 2 | 1 | 1 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ExecutedData | STRUCTURED_OBJECT | `BOOLEAN_RESULT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 0 | 0 | 0 | MISSING | 1 | 0 | 1 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ConfirmedData | STRUCTURED_OBJECT | `BOOLEAN_RESULT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 1 | 0 | 1 | MISSING | 0 | 0 | 0 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ReconciledData | STRUCTURED_OBJECT | `BOOLEAN_RESULT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 0 | 0 | 0 | MISSING | 0 | 0 | 0 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| PersistedData | STRUCTURED_OBJECT | `BOOLEAN_RESULT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 2 | 0 | 2 | MISSING | 0 | 0 | 0 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| StaleData | STRUCTURED_OBJECT | `BOOLEAN_RESULT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 0 | 0 | 0 | MISSING | 1 | 0 | 1 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| InvalidData | STRUCTURED_OBJECT | `BOOLEAN_RESULT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 1 | 0 | 1 | MISSING | 2 | 0 | 2 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| NotApplicableValue | STRUCTURED_OBJECT | `BOOLEAN_RESULT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 1 | 0 | 1 | MISSING | 1 | 0 | 1 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| NotCalculatedValue | STRUCTURED_OBJECT | `BOOLEAN_RESULT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 1 | 0 | 1 | MISSING | 1 | 0 | 1 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| NotAvailableValue | STRUCTURED_OBJECT | `BOOLEAN_RESULT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 0 | 0 | 0 | MISSING | 1 | 0 | 1 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| UnknownValue | STRUCTURED_OBJECT | `BOOLEAN_RESULT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 3 | 0 | 3 | MISSING | 1 | 0 | 1 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| CurrentBid | PRICE_OR_DISTANCE | `PRICE_BID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 5 | 0 | 5 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| CurrentAsk | PRICE_OR_DISTANCE | `PRICE_ASK` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 5 | 0 | 5 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ReserveProjected | MONEY_VALUE | `MONEY_PROJECTED` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ReserveCoverage | POLICY | `RATIO` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; MQL5 evidence=Include/StateMachine.mqh:4755::reserveCoverage; declaration/use checked; decision=PARTIAL_MATCH; MANUAL_REVIEWED: agent; Python evidence=Tools/run_full_parameter_optimization_study.py:290::reserve_coverage; AST declaration/use checked; decision=PARTIAL_MATCH |
| Symbol | IDENTITY | `SYMBOL_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 7 | 1 | 6 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; MQL5 evidence=Include/Types.mqh:257::symbol; declaration/use checked; decision=PARTIAL_MATCH; MANUAL_REVIEWED: agent; Python evidence=Tests/HybridSplitBig/test_catchup_route_hardening.py:11::symbol; AST declaration/use checked; decision=PARTIAL_MATCH |
| MagicNumber | IDENTITY | `MAGIC_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 7 | 1 | 6 | PARTIAL_MATCH | 1 | 0 | 1 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| CycleID | IDENTITY | `CYCLE_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; MQL5 evidence=Include/Types.mqh:166::cycleId; declaration/use checked; decision=PARTIAL_MATCH; MANUAL_REVIEWED: agent; Python evidence=Tests/HybridSplitBig/test_catchup_route_hardening.py:11::cycle; AST declaration/use checked; decision=PARTIAL_MATCH |
| EventID | IDENTITY | `EVENT_ID` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 8 | 1 | 7 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; MQL5 evidence=Include/StateMachine.mqh:434::lastEventId; declaration/use checked; decision=PARTIAL_MATCH; MANUAL_REVIEWED: agent; Python evidence=Tests/unit/test_split_final_safety_model.py:56::event_id; AST declaration/use checked; decision=PARTIAL_MATCH |
| Fingerprint | IDENTITY | `FINGERPRINT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 0 | 8 | MISSING | 3 | 1 | 2 | PARTIAL_MATCH | MANUAL_REVIEWED: agent; Python evidence=Tests/HybridSplitBig/test_catchup_dimension_safe.py:13::fingerprint; AST declaration/use checked; decision=PARTIAL_MATCH |
| Comment | STATE_OR_RESULT | `DIAGNOSTIC_TEXT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 8 | 1 | 7 | PARTIAL_MATCH | 3 | 0 | 3 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| Preview | STRUCTURED_OBJECT | `PREVIEW_OBJECT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 1 | 0 | 1 | MISSING | 1 | 0 | 1 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| Candidate | STATE_OR_RESULT | `OUTCOME` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 4 | 0 | 4 | MISSING | 8 | 0 | 8 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| Plan | STRUCTURED_OBJECT | `PLAN_OBJECT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 1 | 0 | 1 | MISSING | 3 | 1 | 2 | PARTIAL_MATCH | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |
| ApprovedPlan | STRUCTURED_OBJECT | `PLAN_OBJECT` | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | VALIDATOR_VERIFIED | 0 | 0 | 0 | MISSING | 1 | 0 | 1 | MISSING | VALIDATOR_VERIFIED: candidate audit + semantic matrices; no manual-review claim |

## Mapping summary and vacuous-pass control

```text
MQL5_EXACT_MATCH=0
MQL5_SEMANTIC_MATCH=0
MQL5_PARTIAL_MATCH=98
MQL5_AMBIGUOUS=0
MQL5_MISSING=132
MQL5_NOT_APPLICABLE=0
MQL5_NON_MISSING=98
PYTHON_EXACT_MATCH=0
PYTHON_SEMANTIC_MATCH=0
PYTHON_PARTIAL_MATCH=80
PYTHON_AMBIGUOUS=0
PYTHON_MISSING=150
PYTHON_NOT_APPLICABLE=0
PYTHON_NON_MISSING=80
MQL5_ALL_MAPPINGS_MISSING=0
PYTHON_ALL_MAPPINGS_MISSING=0
MISSING_WITHOUT_CANDIDATE_AUDIT=0
MISSING_WITH_UNREVIEWED_CANDIDATES=0
MISSING_WITH_ACCEPTED_CANDIDATE=0
NON_MISSING_WITH_EMPTY_ENTRIES=0
MISSING_WITH_NONEMPTY_ENTRIES=0
CANDIDATE_AUDIT_PARITY_ERROR=0
```

## Full validator output

`STATISTICS_SOURCE=validator generated`

```text
CANONICAL_TERMS=230
MQL5_TERMS_WITH_CANDIDATE_AUDIT=230
PYTHON_TERMS_WITH_CANDIDATE_AUDIT=230
MQL5_NON_MISSING=98
PYTHON_NON_MISSING=80
MQL5_ALL_MAPPINGS_MISSING=0
PYTHON_ALL_MAPPINGS_MISSING=0
MISSING_WITHOUT_CANDIDATE_AUDIT=0
MISSING_WITH_UNREVIEWED_CANDIDATES=0
MISSING_WITH_ACCEPTED_CANDIDATE=0
MISSING_WITH_NONEMPTY_ENTRIES=0
NON_MISSING_WITH_EMPTY_ENTRIES=0
CANDIDATE_WITHOUT_REJECTION_REASON=0
CANDIDATE_WITHOUT_SCORE=0
CANDIDATE_STATUS_INCONSISTENT=0
CANDIDATE_AUDIT_PARITY_ERROR=0
INVALID_TYPE_SIGN=0
INVALID_SIGN_SEMANTICS=0
INVALID_SOURCE_MATRIX=0
INVALID_LIFECYCLE_MATRIX=0
POSITION_ROLE_AMBIGUITY=0
PLAN_STATE_AMBIGUITY=0
NEAR_DUPLICATE_DEFINITIONS=0
NEAR_DUPLICATE_LIFECYCLES=0
NEGATIVE_TESTS_TOTAL=30
NEGATIVE_TESTS_PASSED=30
POSITIVE_TESTS_TOTAL=15
POSITIVE_TESTS_PASSED=15
STAGE_3_1_3_THIRD_CORRECTION_VALIDATION=PASS
```

## Conflict and scope control

```text
PARAMETER_PROFILE_SELECTED=NO
BUSINESS_POLICY_SELECTED=NO
CONFLICT_020_RESOLVED=NO
CONFLICT_022_RESOLVED=NO
CONFLICT_023_RESOLVED=NO
CONFLICT_031_RESOLVED=NO
NEW_CONFLICTS_FOUND=0
MQL5_CHANGED=NO
MQH_CHANGED=NO
TRADING_LOGIC_CHANGED=NO
STAGE_3_1_4_STARTED=NO
```

## Final status

STAGE_3_1_3_THIRD_CORRECTION_STATUS=PASS
Этап 3.1.3 ожидает повторную независимую проверку пользователя.
Этап 3.1.4 не выполнялся.
