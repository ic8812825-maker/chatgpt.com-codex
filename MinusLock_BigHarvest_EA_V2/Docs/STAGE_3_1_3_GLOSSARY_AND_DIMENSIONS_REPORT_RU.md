# Отчёт Этапа 3.1.3 — шестая коррекция

## SUMMARY

```text
STAGE=3.1.3_SIXTH_CORRECTION
STATUS=PASS
BASE_COMMIT=acc692f7edb9cf41dbd3a3a99ef272484575d42f
```

## PRE_FIX_DEFECT_REPRODUCTION

```text
SELECTED_CANDIDATE_DEPENDS_ON_JSON=YES
USE_SITE_SET_DEPENDS_ON_JSON=YES
COMPLETE_USE_GRAPH=NO
COMPLETE_CANDIDATE_DISCOVERY=NO
AMBIGUOUS_NOT_IN_PRODUCTION_SELECTION=YES
SCOPE_TEST_ANALOGUE_MAY_COUNT_AS_MATCH=YES
PER_SYMBOL_INFERENCE=NO
PER_MAGIC_INFERENCE=NO
POSITIVE_FULL_FIXTURES=PARTIAL
SEMANTIC_ADVERSARIAL_PAIRINGS=PARTIAL
```

Эти значения воспроизводят архитектуру пятой коррекции до изменения: mapping entries передавали выбранный identifier и подмножества sites в `infer_semantics`.

## DISCOVERY / USE GRAPH / DATAFLOW

```text
VALIDATOR_OWNS_CANDIDATE_DISCOVERY=YES
VALIDATOR_OWNS_USE_DISCOVERY=YES
VALIDATOR_OWNS_WINNER_SELECTION=YES
JSON_SELECTED_CANDIDATES_USED_AS_TRUTH=NO
JSON_USE_SITES_USED_AS_TRUTH=NO
TOTAL_READ_SITES_DISCOVERED=3896
TOTAL_WRITE_SITES_DISCOVERED=1029
DATAFLOW_NODES=380
DATAFLOW_EDGES=402
PER_SYMBOL_SUPPORTED=YES
PER_MAGIC_SUPPORTED=YES
PER_SYMBOL_MAGIC_SUPPORTED=YES
AMBIGUITY_PRODUCTION_PIPELINE=YES
```

## VALIDATION COUNTERS

Все новые blocking counters (`CANDIDATE_*`, use coverage, dataflow, lineage, scope, ambiguity и `UNPROVEN_EXACT_MATCH`) равны `0`. Отдельные fixture suites: `20/20` positive и `20/20` adversarial. Старые negative controls: `48/48`.

## COMPLETE CANDIDATE AUDIT (230 TERMS)

Каждая строка ниже получена независимым pipeline. Полные generated/discovered sets и полные claimed read/write sets сохранены в identifier mapping JSON; здесь приведён обозримый индекс.

| Canonical term | Language | Candidates | Winner | Runner-up | Status | Ambiguous | Reads | Writes | Claim parity |
|---|---:|---:|---|---|---|---:|---:|---:|---|
| Legacy | mql5 | 7 | `Include/StateMachine.mqh:2076:legacyReason` | `—` | PARTIAL_MATCH | NO | 3 | 1 | PASS |
| Legacy | python | 11 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| LegacyMode | mql5 | 36 | `Include/StateMachine.mqh:2076:legacyReason` | `—` | PARTIAL_MATCH | NO | 3 | 1 | PASS |
| LegacyMode | python | 22 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| LegacyBig | mql5 | 251 | `Include/Types.mqh:264:bigIdentifier` | `Include/Types.mqh:267:bigCoreIdentifier` | AMBIGUOUS | YES | 30 | 8 | PASS |
| LegacyBig | python | 186 | `Tests/unit/test_split_exact_persistence_model.py:155:test_legacy_double_format_loses_identifier_above_2_pow_53` | `—` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| LegacySmall | mql5 | 216 | `Include/Types.mqh:265:smallIdentifier` | `Include/Types.mqh:269:smallBaseIdentifier` | AMBIGUOUS | YES | 25 | 9 | PASS |
| LegacySmall | python | 170 | `Tests/unit/test_split_exact_persistence_model.py:155:test_legacy_double_format_loses_identifier_above_2_pow_53` | `—` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| LegacyFar | mql5 | 225 | `Include/Types.mqh:266:farIdentifier` | `Include/Types.mqh:291:farIdentifier` | AMBIGUOUS | YES | 63 | 10 | PASS |
| LegacyFar | python | 260 | `Tests/unit/test_split_exact_persistence_model.py:155:test_legacy_double_format_loses_identifier_above_2_pow_53` | `Tests/unit/test_split_recovery_order_model.py:232:test_stage7_reset_event_context_does_not_require_far_identifier` | AMBIGUOUS | YES | 0 | 0 | PASS |
| MonolithicBig | mql5 | 246 | `Include/Types.mqh:264:bigIdentifier` | `Include/Types.mqh:267:bigCoreIdentifier` | AMBIGUOUS | YES | 30 | 8 | PASS |
| MonolithicBig | python | 175 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| Split | mql5 | 85 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| Split | python | 28 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| SplitMode | mql5 | 114 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| SplitMode | python | 39 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| SplitBig | mql5 | 298 | `Include/Types.mqh:264:bigIdentifier` | `Include/Types.mqh:267:bigCoreIdentifier` | AMBIGUOUS | YES | 30 | 8 | PASS |
| SplitBig | python | 201 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| BigCore | mql5 | 262 | `Include/Types.mqh:267:bigCoreIdentifier` | `Include/Types.mqh:292:bigCoreIdentifier` | AMBIGUOUS | YES | 55 | 11 | PASS |
| BigCore | python | 205 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| BigTrend | mql5 | 259 | `Include/Types.mqh:268:bigTrendIdentifier` | `Include/Types.mqh:293:bigTrendIdentifier` | AMBIGUOUS | YES | 48 | 7 | PASS |
| BigTrend | python | 202 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| BigGross | mql5 | 288 | `Include/StateMachine.mqh:5175:actualBigGrossLot` | `Include/RecoveryMath.mqh:26:CalcBigLot` | PARTIAL_MATCH | NO | 5 | 2 | PASS |
| BigGross | python | 192 | `Tests/small_at_far_scenario_log.py:9:remain_big_lot` | `Tools/analyze_mt5_big_scenario_divergence.py:36:MT5_BIG_L1_LOT` | PARTIAL_MATCH | NO | 1 | 1 | PASS |
| SmallBase | mql5 | 236 | `Include/Types.mqh:269:smallBaseIdentifier` | `Include/Types.mqh:294:smallBaseIdentifier` | AMBIGUOUS | YES | 50 | 9 | PASS |
| SmallBase | python | 191 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| Hybrid | mql5 | 201 | `Include/HybridCatchUpModel.mqh:112:ValidateHybridCatchUpState` | `Include/HybridCatchUpModel.mqh:155:BuildInitialHybridCatchUpState` | AMBIGUOUS | YES | 3 | 0 | PASS |
| Hybrid | python | 24 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| HybridSplitBig | mql5 | 496 | `Include/Types.mqh:10:STATE_BIG_SMALL_OPENED` | `Include/Types.mqh:32:STATE_BIG_HARVEST` | AMBIGUOUS | YES | 5 | 0 | PASS |
| HybridSplitBig | python | 221 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| HybridMode | mql5 | 228 | `Include/HybridCatchUpModel.mqh:112:ValidateHybridCatchUpState` | `Include/HybridCatchUpModel.mqh:155:BuildInitialHybridCatchUpState` | AMBIGUOUS | YES | 3 | 0 | PASS |
| HybridMode | python | 35 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| HybridPlan | mql5 | 209 | `Include/HybridGeometrySolver.mqh:7:HybridGeometryDecision` | `Include/HybridGeometrySolver.mqh:16:HybridRecoveryProjection` | AMBIGUOUS | YES | 2 | 0 | PASS |
| HybridPlan | python | 29 | `Tools/hybrid_big_sequence_model.py:7:HybridBigSequenceState` | `Tools/hybrid_small_state_machine.py:9:HybridSmallState` | AMBIGUOUS | YES | 1 | 0 | PASS |
| HybridPreview | mql5 | 204 | `Include/Types.mqh:1084:HybridPartialFarPreviewResult` | `Include/Types.mqh:1170:HybridMarginPreview` | AMBIGUOUS | YES | 8 | 0 | PASS |
| HybridPreview | python | 26 | `Tools/hybrid_big_sequence_model.py:7:HybridBigSequenceState` | `Tools/hybrid_small_state_machine.py:9:HybridSmallState` | AMBIGUOUS | YES | 1 | 0 | PASS |
| HybridExecution | mql5 | 214 | `Include/HybridGeometrySolver.mqh:7:HybridGeometryDecision` | `Include/HybridGeometrySolver.mqh:16:HybridRecoveryProjection` | AMBIGUOUS | YES | 2 | 0 | PASS |
| HybridExecution | python | 31 | `Tools/hybrid_big_sequence_model.py:7:HybridBigSequenceState` | `Tools/hybrid_small_state_machine.py:9:HybridSmallState` | AMBIGUOUS | YES | 1 | 0 | PASS |
| InitialBuy | mql5 | 73 | `Include/Types.mqh:424:initialBuyTicket` | `Include/Types.mqh:493:initialBuyIdentifier` | AMBIGUOUS | YES | 15 | 3 | PASS |
| InitialBuy | python | 29 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| InitialSell | mql5 | 73 | `Include/Types.mqh:425:initialSellTicket` | `Include/Types.mqh:494:initialSellIdentifier` | AMBIGUOUS | YES | 15 | 3 | PASS |
| InitialSell | python | 29 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| InitialProfitLeg | mql5 | 123 | `Include/Types.mqh:424:initialBuyTicket` | `Include/Types.mqh:425:initialSellTicket` | AMBIGUOUS | YES | 15 | 3 | PASS |
| InitialProfitLeg | python | 50 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| InitialLosingLeg | mql5 | 126 | `Include/Types.mqh:424:initialBuyTicket` | `Include/Types.mqh:425:initialSellTicket` | AMBIGUOUS | YES | 15 | 3 | PASS |
| InitialLosingLeg | python | 89 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| InitialIgnoredProfit | mql5 | 128 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/Types.mqh:516:initialProfitIgnored` | SEMANTIC_MATCH | NO | 9 | 5 | PASS |
| InitialIgnoredProfit | python | 40 | `Tests/real_recovery_examples_check.py:2:initial_ignored_profit` | `Tools/offline_optimizer.py:165:initial_ignored_profit` | PARTIAL_MATCH | NO | 2 | 2 | PASS |
| OldFar | mql5 | 224 | `Include/Types.mqh:611:oldFarTicket` | `Include/Types.mqh:266:farIdentifier` | PARTIAL_MATCH | NO | 3 | 3 | PASS |
| OldFar | python | 255 | `Tests/unit/test_split_recovery_order_model.py:232:test_stage7_reset_event_context_does_not_require_far_identifier` | `—` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| CurrentFar | mql5 | 218 | `Include/Types.mqh:266:farIdentifier` | `Include/Types.mqh:291:farIdentifier` | AMBIGUOUS | YES | 63 | 10 | PASS |
| CurrentFar | python | 249 | `Tests/unit/test_split_recovery_order_model.py:232:test_stage7_reset_event_context_does_not_require_far_identifier` | `—` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| ResidualFar | mql5 | 222 | `Include/Types.mqh:266:farIdentifier` | `Include/Types.mqh:291:farIdentifier` | AMBIGUOUS | YES | 63 | 10 | PASS |
| ResidualFar | python | 254 | `Tests/unit/test_split_recovery_order_model.py:232:test_stage7_reset_event_context_does_not_require_far_identifier` | `—` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| NewFar | mql5 | 230 | `Include/Types.mqh:266:farIdentifier` | `Include/Types.mqh:291:farIdentifier` | AMBIGUOUS | YES | 63 | 10 | PASS |
| NewFar | python | 262 | `Tests/unit/test_split_recovery_order_model.py:232:test_stage7_reset_event_context_does_not_require_far_identifier` | `—` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| LegacyBigPosition | mql5 | 356 | `Include/SimulationEngine.mqh:74:positionIdentifier` | `Include/SimulationEngine.mqh:97:positionIdentifier` | AMBIGUOUS | YES | 7 | 2 | PASS |
| LegacyBigPosition | python | 220 | `Tests/unit/test_split_exact_persistence_model.py:155:test_legacy_double_format_loses_identifier_above_2_pow_53` | `—` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| BigCorePosition | mql5 | 367 | `Include/SimulationEngine.mqh:74:positionIdentifier` | `Include/SimulationEngine.mqh:97:positionIdentifier` | AMBIGUOUS | YES | 7 | 2 | PASS |
| BigCorePosition | python | 239 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| BigTrendPosition | mql5 | 364 | `Include/SimulationEngine.mqh:74:positionIdentifier` | `Include/SimulationEngine.mqh:97:positionIdentifier` | AMBIGUOUS | YES | 7 | 2 | PASS |
| BigTrendPosition | python | 236 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| LegacySmallPosition | mql5 | 323 | `Include/SimulationEngine.mqh:74:positionIdentifier` | `Include/SimulationEngine.mqh:97:positionIdentifier` | AMBIGUOUS | YES | 7 | 2 | PASS |
| LegacySmallPosition | python | 204 | `Tests/unit/test_split_exact_persistence_model.py:155:test_legacy_double_format_loses_identifier_above_2_pow_53` | `—` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| SmallBasePosition | mql5 | 343 | `Include/SimulationEngine.mqh:74:positionIdentifier` | `Include/SimulationEngine.mqh:97:positionIdentifier` | AMBIGUOUS | YES | 7 | 2 | PASS |
| SmallBasePosition | python | 225 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| ManagedPosition | mql5 | 115 | `Include/PositionUtils.mqh:70:IsManagedPositionForCurrentSymbol` | `Include/PositionUtils.mqh:76:IsManagedPositionForMagic` | AMBIGUOUS | YES | 2 | 0 | PASS |
| ManagedPosition | python | 39 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| UnmanagedPosition | mql5 | 113 | `Include/SimulationEngine.mqh:74:positionIdentifier` | `Include/SimulationEngine.mqh:97:positionIdentifier` | AMBIGUOUS | YES | 7 | 2 | PASS |
| UnmanagedPosition | python | 35 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| ForeignCyclePosition | mql5 | 175 | `Include/SimulationEngine.mqh:74:positionIdentifier` | `Include/SimulationEngine.mqh:97:positionIdentifier` | AMBIGUOUS | YES | 7 | 2 | PASS |
| ForeignCyclePosition | python | 71 | `Tests/unit/test_split_reserve_transaction_model.py:24:cycle_id` | `Tests/unit/test_split_exact_persistence_model.py:39:cycle_id` | AMBIGUOUS | YES | 4 | 4 | PASS |
| FarDirection | mql5 | 269 | `Include/BrokerMoneyModel.mqh:24:DirectionalVolumeSnapshot` | `Include/Types.mqh:1084:HybridPartialFarPreviewResult` | AMBIGUOUS | YES | 1 | 0 | PASS |
| FarDirection | python | 272 | `Tests/HybridSplitBig/hybrid_split_big_reference.py:128:NewFarCandidate` | `Tests/HybridSplitBig/hybrid_split_big_reference.py:131:NewFarSolverResult` | AMBIGUOUS | YES | 2 | 0 | PASS |
| OppositeFarDirection | mql5 | 270 | `Include/BrokerMoneyModel.mqh:24:DirectionalVolumeSnapshot` | `Include/Types.mqh:1084:HybridPartialFarPreviewResult` | AMBIGUOUS | YES | 1 | 0 | PASS |
| OppositeFarDirection | python | 272 | `Tests/HybridSplitBig/hybrid_split_big_reference.py:128:NewFarCandidate` | `Tests/HybridSplitBig/hybrid_split_big_reference.py:131:NewFarSolverResult` | AMBIGUOUS | YES | 2 | 0 | PASS |
| SameAsFarDirection | mql5 | 269 | `Include/BrokerMoneyModel.mqh:24:DirectionalVolumeSnapshot` | `Include/Types.mqh:1084:HybridPartialFarPreviewResult` | AMBIGUOUS | YES | 1 | 0 | PASS |
| SameAsFarDirection | python | 277 | `Tests/HybridSplitBig/hybrid_split_big_reference.py:128:NewFarCandidate` | `Tests/HybridSplitBig/hybrid_split_big_reference.py:131:NewFarSolverResult` | AMBIGUOUS | YES | 2 | 0 | PASS |
| BigDirection | mql5 | 299 | `Include/BrokerMoneyModel.mqh:17:BigRecoveryEvaluation` | `Include/BrokerMoneyModel.mqh:18:BigReserveCatchUpEvaluation` | AMBIGUOUS | YES | 3 | 0 | PASS |
| BigDirection | python | 198 | `Tools/hybrid_big_sequence_model.py:7:HybridBigSequenceState` | `—` | PARTIAL_MATCH | NO | 1 | 0 | PASS |
| SmallDirection | mql5 | 259 | `Include/BrokerMoneyModel.mqh:19:SmallTransitionEvaluation` | `Include/BrokerMoneyModel.mqh:21:SmallTransitionLeg` | AMBIGUOUS | YES | 4 | 0 | PASS |
| SmallDirection | python | 182 | `Tools/hybrid_small_state_machine.py:9:HybridSmallState` | `Tests/HybridSplitBig/hybrid_split_big_reference.py:134:FutureSmallResult` | PARTIAL_MATCH | NO | 1 | 0 | PASS |
| TrendDirection | mql5 | 104 | `Include/BrokerMoneyModel.mqh:24:DirectionalVolumeSnapshot` | `—` | SEMANTIC_MATCH | NO | 1 | 0 | PASS |
| TrendDirection | python | 53 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| ReverseDirection | mql5 | 171 | `Include/BrokerMoneyModel.mqh:24:DirectionalVolumeSnapshot` | `Include/BrokerMoneyModel.mqh:27:FalseReverseOption` | AMBIGUOUS | YES | 1 | 0 | PASS |
| ReverseDirection | python | 54 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| RawLot | mql5 | 282 | `Include/RecoveryMath.mqh:100:CalcCloseFarLotRaw` | `Include/RecoveryMath.mqh:4:PointValuePerLot` | SEMANTIC_MATCH | NO | 0 | 0 | PASS |
| RawLot | python | 228 | `Tools/simulate_big_scenario_trace.py:59:CloseFarLotRaw` | `Tools/optimize_big_scenario_min_levels.py:113:CloseFarLotRaw` | AMBIGUOUS | YES | 0 | 2 | PASS |
| CalculatedLot | mql5 | 282 | `Include/RecoveryMath.mqh:4:PointValuePerLot` | `Include/LotUtils.mqh:4:BrokerLotStep` | AMBIGUOUS | YES | 10 | 0 | PASS |
| CalculatedLot | python | 213 | `Tests/normalize_volume_to_step_check.py:2:lot` | `Tests/unit/test_broker_money_behavior.py:3:lot` | AMBIGUOUS | YES | 38 | 17 | PASS |
| NormalizedLot | mql5 | 275 | `Include/ReconciliationEngine.mqh:76:normalizedCtxLot` | `Include/ReconciliationEngine.mqh:76:normalizedActualLot` | AMBIGUOUS | YES | 6 | 1 | PASS |
| NormalizedLot | python | 210 | `Tests/normalize_volume_to_step_check.py:2:lot` | `Tests/unit/test_broker_money_behavior.py:3:lot` | AMBIGUOUS | YES | 38 | 17 | PASS |
| RequestedLot | mql5 | 273 | `Include/StateMachine.mqh:5459:requestedLot` | `Tests/stage_3_1_3/fixtures/positive/valid_test_analogue_partial.mqh:1:lotOracle` | SEMANTIC_MATCH | NO | 23 | 9 | PASS |
| RequestedLot | python | 214 | `Tests/normalize_volume_to_step_check.py:2:lot` | `Tests/unit/test_broker_money_behavior.py:3:lot` | AMBIGUOUS | YES | 38 | 17 | PASS |
| FilledLot | mql5 | 276 | `Include/SimulationEngine.mqh:74:filledLot` | `Include/SimulationEngine.mqh:97:filledLot` | AMBIGUOUS | YES | 13 | 6 | PASS |
| FilledLot | python | 215 | `Tests/normalize_volume_to_step_check.py:2:lot` | `Tests/unit/test_broker_money_behavior.py:3:lot` | AMBIGUOUS | YES | 38 | 17 | PASS |
| ActualPositionLot | mql5 | 417 | `Include/TradeEngine.mqh:113:currentLot` | `Include/TradeEngine.mqh:164:currentLot` | AMBIGUOUS | YES | 3 | 2 | PASS |
| ActualPositionLot | python | 268 | `Tools/hybrid_small_state_machine.py:11:actual_new_far_lot` | `Tests/unit/test_big_small_behavior.py:68:test_partial_fill_uses_actual_volume` | PARTIAL_MATCH | NO | 5 | 2 | PASS |
| ResidualLotProjected | mql5 | 325 | `Include/Types.mqh:460:projectedReverseSmallLot` | `Include/Types.mqh:462:projectedReverseSmallDirectionLot` | AMBIGUOUS | YES | 2 | 3 | PASS |
| ResidualLotProjected | python | 231 | `Tests/unit/test_split_architecture_model.py:55:test_partial_lot_does_not_leave_untradable_residual` | `Tests/normalize_volume_to_step_check.py:2:lot` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| ResidualLotActual | mql5 | 315 | `Include/TradeEngine.mqh:113:currentLot` | `Include/TradeEngine.mqh:164:currentLot` | AMBIGUOUS | YES | 3 | 2 | PASS |
| ResidualLotActual | python | 237 | `Tools/hybrid_small_state_machine.py:11:actual_new_far_lot` | `Tests/unit/test_split_architecture_model.py:55:test_partial_lot_does_not_leave_untradable_residual` | PARTIAL_MATCH | NO | 5 | 2 | PASS |
| FarLotRaw | mql5 | 463 | `Include/RecoveryMath.mqh:100:CalcCloseFarLotRaw` | `Include/HybridRoundingModel.mqh:7:NormalizeHybridNewFarLot` | SEMANTIC_MATCH | NO | 0 | 0 | PASS |
| FarLotRaw | python | 402 | `Tools/simulate_big_scenario_trace.py:59:CloseFarLotRaw` | `Tools/optimize_big_scenario_min_levels.py:113:CloseFarLotRaw` | AMBIGUOUS | YES | 0 | 2 | PASS |
| FarLotCalculated | mql5 | 463 | `Include/HybridRoundingModel.mqh:7:NormalizeHybridNewFarLot` | `Include/RecoveryMath.mqh:100:CalcCloseFarLotRaw` | AMBIGUOUS | YES | 2 | 0 | PASS |
| FarLotCalculated | python | 388 | `Tools/hybrid_big_sequence_model.py:8:far_before_lot` | `Tools/hybrid_big_sequence_model.py:8:far_after_lot` | AMBIGUOUS | YES | 1 | 1 | PASS |
| FarLotNormalized | mql5 | 456 | `Include/HybridRoundingModel.mqh:7:NormalizeHybridNewFarLot` | `Include/RecoveryMath.mqh:100:CalcCloseFarLotRaw` | AMBIGUOUS | YES | 2 | 0 | PASS |
| FarLotNormalized | python | 385 | `Tools/hybrid_big_sequence_model.py:8:far_before_lot` | `Tools/hybrid_big_sequence_model.py:8:far_after_lot` | AMBIGUOUS | YES | 1 | 1 | PASS |
| FarLotRequested | mql5 | 454 | `Include/StateMachine.mqh:5459:requestedLot` | `Include/HybridTransitionPlanner.mqh:7:oldFarLot` | SEMANTIC_MATCH | NO | 23 | 9 | PASS |
| FarLotRequested | python | 389 | `Tools/hybrid_big_sequence_model.py:8:far_before_lot` | `Tools/hybrid_big_sequence_model.py:8:far_after_lot` | AMBIGUOUS | YES | 1 | 1 | PASS |
| FarLotFilled | mql5 | 457 | `Include/SimulationEngine.mqh:74:filledLot` | `Include/SimulationEngine.mqh:97:filledLot` | AMBIGUOUS | YES | 13 | 6 | PASS |
| FarLotFilled | python | 390 | `Tools/hybrid_big_sequence_model.py:8:far_before_lot` | `Tools/hybrid_big_sequence_model.py:8:far_after_lot` | AMBIGUOUS | YES | 1 | 1 | PASS |
| FarLotActual | mql5 | 488 | `Include/TradeEngine.mqh:113:currentLot` | `Include/TradeEngine.mqh:164:currentLot` | AMBIGUOUS | YES | 3 | 2 | PASS |
| FarLotActual | python | 404 | `Tools/hybrid_small_state_machine.py:11:actual_new_far_lot` | `Tools/hybrid_big_sequence_model.py:8:far_before_lot` | PARTIAL_MATCH | NO | 5 | 2 | PASS |
| BigCoreLotRaw | mql5 | 514 | `Include/RecoveryMath.mqh:37:CalcBigCoreLot` | `Include/Types.mqh:435:bigCoreLot` | SEMANTIC_MATCH | NO | 2 | 0 | PASS |
| BigCoreLotRaw | python | 408 | `Tests/small_at_far_scenario_log.py:9:remain_big_lot` | `Tests/HybridSplitBig/test_catchup_temporal_model.py:21:core_lot` | AMBIGUOUS | YES | 1 | 1 | PASS |
| BigCoreLotNormalized | mql5 | 507 | `Include/RecoveryMath.mqh:37:CalcBigCoreLot` | `Include/Types.mqh:435:bigCoreLot` | SEMANTIC_MATCH | NO | 2 | 0 | PASS |
| BigCoreLotNormalized | python | 390 | `Tests/small_at_far_scenario_log.py:9:remain_big_lot` | `Tests/HybridSplitBig/test_catchup_temporal_model.py:21:core_lot` | AMBIGUOUS | YES | 1 | 1 | PASS |
| BigCoreLotRequested | mql5 | 505 | `Include/StateMachine.mqh:5459:requestedLot` | `Include/RecoveryMath.mqh:37:CalcBigCoreLot` | SEMANTIC_MATCH | NO | 23 | 9 | PASS |
| BigCoreLotRequested | python | 394 | `Tests/small_at_far_scenario_log.py:9:remain_big_lot` | `Tests/HybridSplitBig/test_catchup_temporal_model.py:21:core_lot` | AMBIGUOUS | YES | 1 | 1 | PASS |
| BigCoreLotFilled | mql5 | 508 | `Include/SimulationEngine.mqh:74:filledLot` | `Include/SimulationEngine.mqh:97:filledLot` | AMBIGUOUS | YES | 13 | 6 | PASS |
| BigCoreLotFilled | python | 394 | `Tests/small_at_far_scenario_log.py:9:remain_big_lot` | `Tests/HybridSplitBig/test_catchup_temporal_model.py:21:core_lot` | AMBIGUOUS | YES | 1 | 1 | PASS |
| BigCoreLotActual | mql5 | 542 | `Include/TradeEngine.mqh:113:currentLot` | `Include/TradeEngine.mqh:164:currentLot` | AMBIGUOUS | YES | 3 | 2 | PASS |
| BigCoreLotActual | python | 413 | `Tools/hybrid_small_state_machine.py:11:actual_new_far_lot` | `Tests/small_at_far_scenario_log.py:9:remain_big_lot` | PARTIAL_MATCH | NO | 5 | 2 | PASS |
| BigTrendLotRaw | mql5 | 512 | `Include/RecoveryMath.mqh:42:CalcBigTrendLot` | `Include/Types.mqh:436:bigTrendLot` | SEMANTIC_MATCH | NO | 2 | 0 | PASS |
| BigTrendLotRaw | python | 405 | `Tests/small_at_far_scenario_log.py:9:remain_big_lot` | `Tests/HybridSplitBig/test_catchup_temporal_model.py:22:trend_lot` | AMBIGUOUS | YES | 1 | 1 | PASS |
| BigTrendLotNormalized | mql5 | 505 | `Include/RecoveryMath.mqh:42:CalcBigTrendLot` | `Include/Types.mqh:436:bigTrendLot` | SEMANTIC_MATCH | NO | 2 | 0 | PASS |
| BigTrendLotNormalized | python | 387 | `Tests/small_at_far_scenario_log.py:9:remain_big_lot` | `Tests/HybridSplitBig/test_catchup_temporal_model.py:22:trend_lot` | AMBIGUOUS | YES | 1 | 1 | PASS |
| SmallBaseLotRaw | mql5 | 497 | `Include/RecoveryMath.mqh:47:CalcSmallBaseLot` | `Include/Types.mqh:437:smallBaseLot` | SEMANTIC_MATCH | NO | 2 | 0 | PASS |
| SmallBaseLotRaw | python | 395 | `Tests/HybridSplitBig/test_catchup_temporal_model.py:23:small_lot` | `Tools/analyze_mt5_big_scenario_divergence.py:37:MT5_SMALL_L1_LOT` | PARTIAL_MATCH | NO | 23 | 9 | PASS |
| SmallBaseLotNormalized | mql5 | 491 | `Include/RecoveryMath.mqh:47:CalcSmallBaseLot` | `Include/Types.mqh:437:smallBaseLot` | SEMANTIC_MATCH | NO | 2 | 0 | PASS |
| SmallBaseLotNormalized | python | 377 | `Tests/HybridSplitBig/test_catchup_temporal_model.py:23:small_lot` | `Tools/analyze_mt5_big_scenario_divergence.py:37:MT5_SMALL_L1_LOT` | PARTIAL_MATCH | NO | 23 | 9 | PASS |
| PartialFarCloseLotCalculated | mql5 | 640 | `Include/StateMachine.mqh:5227:AdjustPartialFarLotForMinimumResidual` | `Include/RecoveryMath.mqh:100:CalcCloseFarLotRaw` | SEMANTIC_MATCH | NO | 1 | 0 | PASS |
| PartialFarCloseLotCalculated | python | 491 | `Tools/hybrid_big_sequence_model.py:10:partial_far_close_lot` | `Tools/analyze_mt5_big_scenario_divergence.py:38:MT5_FAR_PARTIAL_LOT` | PARTIAL_MATCH | NO | 1 | 1 | PASS |
| PartialFarCloseLotNormalized | mql5 | 633 | `Include/StateMachine.mqh:5227:AdjustPartialFarLotForMinimumResidual` | `Include/RecoveryMath.mqh:100:CalcCloseFarLotRaw` | SEMANTIC_MATCH | NO | 1 | 0 | PASS |
| PartialFarCloseLotNormalized | python | 488 | `Tools/hybrid_big_sequence_model.py:10:partial_far_close_lot` | `Tools/analyze_mt5_big_scenario_divergence.py:38:MT5_FAR_PARTIAL_LOT` | PARTIAL_MATCH | NO | 1 | 1 | PASS |
| PartialFarCloseLotRequested | mql5 | 631 | `Include/StateMachine.mqh:5459:requestedLot` | `Include/StateMachine.mqh:5227:AdjustPartialFarLotForMinimumResidual` | AMBIGUOUS | YES | 23 | 9 | PASS |
| PartialFarCloseLotRequested | python | 492 | `Tools/hybrid_big_sequence_model.py:10:partial_far_close_lot` | `Tools/analyze_mt5_big_scenario_divergence.py:38:MT5_FAR_PARTIAL_LOT` | PARTIAL_MATCH | NO | 1 | 1 | PASS |
| PartialFarCloseLotFilled | mql5 | 634 | `Include/SimulationEngine.mqh:74:filledLot` | `Include/SimulationEngine.mqh:97:filledLot` | AMBIGUOUS | YES | 13 | 6 | PASS |
| PartialFarCloseLotFilled | python | 492 | `Tools/hybrid_big_sequence_model.py:10:partial_far_close_lot` | `Tools/analyze_mt5_big_scenario_divergence.py:38:MT5_FAR_PARTIAL_LOT` | PARTIAL_MATCH | NO | 1 | 1 | PASS |
| FarResidualProjected | mql5 | 306 | `Include/StateMachine.mqh:5227:AdjustPartialFarLotForMinimumResidual` | `Include/Types.mqh:460:projectedReverseSmallLot` | SEMANTIC_MATCH | NO | 1 | 0 | PASS |
| FarResidualProjected | python | 272 | `Tests/unit/test_split_architecture_model.py:55:test_partial_lot_does_not_leave_untradable_residual` | `Tools/hybrid_big_sequence_model.py:8:far_before_lot` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| FarResidualActual | mql5 | 298 | `Include/TradeEngine.mqh:113:currentLot` | `Include/TradeEngine.mqh:164:currentLot` | AMBIGUOUS | YES | 3 | 2 | PASS |
| FarResidualActual | python | 271 | `Tools/hybrid_small_state_machine.py:11:actual_new_far_lot` | `Tests/unit/test_split_architecture_model.py:55:test_partial_lot_does_not_leave_untradable_residual` | PARTIAL_MATCH | NO | 5 | 2 | PASS |
| NewFarCandidateLot | mql5 | 477 | `Include/HybridRoundingModel.mqh:7:NormalizeHybridNewFarLot` | `Include/BrokerMoneyModel.mqh:213:CalcTargetNewFarLot` | AMBIGUOUS | YES | 2 | 0 | PASS |
| NewFarCandidateLot | python | 435 | `Tools/hybrid_small_state_machine.py:11:target_new_far_lot` | `Tools/hybrid_small_state_machine.py:11:actual_new_far_lot` | AMBIGUOUS | YES | 4 | 1 | PASS |
| NewFarProjectedLot | mql5 | 504 | `Include/BrokerMoneyModel.mqh:222:projectedNewFarLot` | `Include/HybridRoundingModel.mqh:7:NormalizeHybridNewFarLot` | PARTIAL_MATCH | NO | 5 | 1 | PASS |
| NewFarProjectedLot | python | 414 | `Tools/hybrid_small_state_machine.py:11:target_new_far_lot` | `Tools/hybrid_small_state_machine.py:11:actual_new_far_lot` | AMBIGUOUS | YES | 4 | 1 | PASS |
| NewFarNormalizedLot | mql5 | 463 | `Include/HybridRoundingModel.mqh:7:NormalizeHybridNewFarLot` | `Include/BrokerMoneyModel.mqh:213:CalcTargetNewFarLot` | AMBIGUOUS | YES | 2 | 0 | PASS |
| NewFarNormalizedLot | python | 398 | `Tools/hybrid_small_state_machine.py:11:target_new_far_lot` | `Tools/hybrid_small_state_machine.py:11:actual_new_far_lot` | AMBIGUOUS | YES | 4 | 1 | PASS |
| NewFarPromotedLot | mql5 | 459 | `Include/HybridRoundingModel.mqh:7:NormalizeHybridNewFarLot` | `Include/BrokerMoneyModel.mqh:213:CalcTargetNewFarLot` | AMBIGUOUS | YES | 2 | 0 | PASS |
| NewFarPromotedLot | python | 398 | `Tools/hybrid_small_state_machine.py:11:target_new_far_lot` | `Tools/hybrid_small_state_machine.py:11:actual_new_far_lot` | AMBIGUOUS | YES | 4 | 1 | PASS |
| NewFarActualLot | mql5 | 490 | `Include/TradeEngine.mqh:113:currentLot` | `Include/TradeEngine.mqh:164:currentLot` | AMBIGUOUS | YES | 3 | 2 | PASS |
| NewFarActualLot | python | 413 | `Tools/hybrid_small_state_machine.py:11:actual_new_far_lot` | `Tools/hybrid_small_state_machine.py:11:target_new_far_lot` | PARTIAL_MATCH | NO | 5 | 2 | PASS |
| Point | mql5 | 92 | `Tests/MQL5/HybridSplitBig/HybridCatchUpRouteHardeningTests.mq5:26:volumeStep` | `—` | PARTIAL_MATCH | NO | 9 | 3 | PASS |
| Point | python | 88 | `Tests/HybridSplitBig/test_catchup_full_dimension_contract.py:17:symbol_point` | `Tests/HybridSplitBig/test_catchup_full_dimension_contract.py:17:worst_bid_adverse` | PARTIAL_MATCH | NO | 1 | 0 | PASS |
| TickSize | mql5 | 17 | `Include/RecoveryMath.mqh:7:tickSize` | `Include/SimulationEngine.mqh:48:tickSize` | AMBIGUOUS | YES | 4 | 2 | PASS |
| TickSize | python | 7 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| TickValue | mql5 | 16 | `Tests/MQL5/HybridSplitBig/HybridCatchUpRouteHardeningTests.mq5:15:minLot` | `Include/RecoveryMath.mqh:7:tickSize` | PARTIAL_MATCH | NO | 34 | 17 | PASS |
| TickValue | python | 4 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| MarketBidPrice | mql5 | 122 | `Include/Types.mqh:121:MarketBid` | `Include/HybridPartialFarPreview.mqh:6:price` | PARTIAL_MATCH | NO | 11 | 0 | PASS |
| MarketBidPrice | python | 43 | `Tools/hybrid_small_state_machine.py:7:open_price` | `Tools/hybrid_small_state_machine.py:7:current_price` | AMBIGUOUS | YES | 1 | 1 | PASS |
| MarketAskPrice | mql5 | 122 | `Include/Types.mqh:122:MarketAsk` | `Include/HybridPartialFarPreview.mqh:4:ask` | PARTIAL_MATCH | NO | 11 | 0 | PASS |
| MarketAskPrice | python | 42 | `Tools/hybrid_small_state_machine.py:7:open_price` | `Tools/hybrid_small_state_machine.py:7:current_price` | AMBIGUOUS | YES | 1 | 1 | PASS |
| PositionOpenPrice | mql5 | 290 | `Include/BrokerMoneyModel.mqh:45:BrokerExecutionOpenPrice` | `Include/Types.mqh:439:bigCoreOpenPrice` | SEMANTIC_MATCH | NO | 10 | 0 | PASS |
| PositionOpenPrice | python | 123 | `Tools/hybrid_small_state_machine.py:7:open_price` | `Tests/small_at_far_scenario_log.py:7:big_open_price` | PARTIAL_MATCH | NO | 1 | 1 | PASS |
| TriggerPrice | mql5 | 110 | `Include/Types.mqh:458:reverseTriggerPrice` | `Include/Types.mqh:1197:triggerPrice` | AMBIGUOUS | YES | 1 | 2 | PASS |
| TriggerPrice | python | 35 | `Tools/hybrid_small_state_machine.py:7:open_price` | `Tools/hybrid_small_state_machine.py:7:current_price` | AMBIGUOUS | YES | 1 | 1 | PASS |
| TargetPrice | mql5 | 138 | `Include/HybridCatchUpModel.mqh:7:HybridCatchUpClosePrice` | `Include/PositionUtils.mqh:13:ExitPriceForDirection` | AMBIGUOUS | YES | 2 | 0 | PASS |
| TargetPrice | python | 41 | `Tools/hybrid_small_state_machine.py:7:open_price` | `Tools/hybrid_small_state_machine.py:7:current_price` | AMBIGUOUS | YES | 1 | 1 | PASS |
| ControlPrice | mql5 | 102 | `Include/HybridCatchUpModel.mqh:7:HybridCatchUpClosePrice` | `Include/PositionUtils.mqh:13:ExitPriceForDirection` | AMBIGUOUS | YES | 2 | 0 | PASS |
| ControlPrice | python | 29 | `Tests/HybridSplitBig/test_catchup_stage12.py:81:test_mg03_05_control_prices_not_historical` | `Tools/hybrid_small_state_machine.py:7:open_price` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| ProjectedExitPrice | mql5 | 158 | `Include/HybridCatchUpModel.mqh:76:BuildProjectedReopenPrices` | `Include/PositionUtils.mqh:13:ExitPriceForDirection` | SEMANTIC_MATCH | NO | 3 | 0 | PASS |
| ProjectedExitPrice | python | 45 | `Tools/hybrid_small_state_machine.py:7:open_price` | `Tools/hybrid_small_state_machine.py:7:current_price` | AMBIGUOUS | YES | 1 | 1 | PASS |
| ExecutedDealPrice | mql5 | 171 | `Include/SimulationEngine.mqh:74:executionPrice` | `Include/HybridPartialFarPreview.mqh:6:price` | SEMANTIC_MATCH | NO | 6 | 1 | PASS |
| ExecutedDealPrice | python | 31 | `Tools/hybrid_small_state_machine.py:7:open_price` | `Tools/hybrid_small_state_machine.py:7:current_price` | AMBIGUOUS | YES | 1 | 1 | PASS |
| PriceDelta | mql5 | 105 | `Include/HybridCatchUpModel.mqh:7:HybridCatchUpClosePrice` | `Include/PositionUtils.mqh:13:ExitPriceForDirection` | AMBIGUOUS | YES | 2 | 0 | PASS |
| PriceDelta | python | 28 | `Tools/hybrid_small_state_machine.py:7:open_price` | `Tools/hybrid_small_state_machine.py:7:current_price` | AMBIGUOUS | YES | 1 | 1 | PASS |
| DistancePoints | mql5 | 98 | `Include/Types.mqh:549:workFarDistancePoints` | `Include/Types.mqh:553:initialFarDistancePoints` | AMBIGUOUS | YES | 20 | 8 | PASS |
| DistancePoints | python | 92 | `Tests/small_at_far_scenario_log.py:13:effective_far_distance_points` | `Tools/analyze_mt5_big_scenario_divergence.py:26:FAR_DISTANCE_POINTS` | PARTIAL_MATCH | NO | 3 | 1 | PASS |
| DistanceTicks | mql5 | 30 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| DistanceTicks | python | 20 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| BidAwareClosePrice | mql5 | 309 | `Include/HybridPartialFarPreview.mqh:6:price` | `Include/BrokerMoneyModel.mqh:62:price` | AMBIGUOUS | YES | 14 | 6 | PASS |
| BidAwareClosePrice | python | 163 | `Tests/HybridSplitBig/test_catchup_temporal_model.py:12:close_bid` | `Tests/HybridSplitBig/test_catchup_temporal_model.py:30:close_bid` | AMBIGUOUS | YES | 9 | 1 | PASS |
| AskAwareClosePrice | mql5 | 309 | `Include/HybridPartialFarPreview.mqh:4:ask` | `Include/HybridPartialFarPreview.mqh:6:price` | AMBIGUOUS | YES | 62 | 12 | PASS |
| AskAwareClosePrice | python | 162 | `Tests/HybridSplitBig/test_catchup_temporal_model.py:12:close_ask` | `Tests/HybridSplitBig/test_catchup_temporal_model.py:30:close_ask` | AMBIGUOUS | YES | 7 | 1 | PASS |
| FarOpenPriceActual | mql5 | 436 | `Include/Types.mqh:500:farOpenPrice` | `Include/Types.mqh:614:oldFarOpenPrice` | AMBIGUOUS | YES | 57 | 16 | PASS |
| FarOpenPriceActual | python | 352 | `Tests/small_at_far_scenario_log.py:12:far_open_price` | `Tools/mql5_like_big_scenario_parameter_search.py:40:MT5_FAR_OPEN_PRICE` | PARTIAL_MATCH | NO | 5 | 2 | PASS |
| BigCoreOpenPriceActual | mql5 | 465 | `Include/Types.mqh:439:bigCoreOpenPrice` | `Include/Types.mqh:440:bigTrendOpenPrice` | SEMANTIC_MATCH | NO | 13 | 6 | PASS |
| BigCoreOpenPriceActual | python | 312 | `Tests/small_at_far_scenario_log.py:7:big_open_price` | `Tools/mql5_like_big_scenario_parameter_search.py:41:MT5_BIG_L1_OPEN_PRICE` | PARTIAL_MATCH | NO | 5 | 1 | PASS |
| BigTrendOpenPriceActual | mql5 | 462 | `Include/Types.mqh:440:bigTrendOpenPrice` | `Include/Types.mqh:439:bigCoreOpenPrice` | SEMANTIC_MATCH | NO | 5 | 4 | PASS |
| BigTrendOpenPriceActual | python | 310 | `Tests/small_at_far_scenario_log.py:7:big_open_price` | `Tools/mql5_like_big_scenario_parameter_search.py:41:MT5_BIG_L1_OPEN_PRICE` | PARTIAL_MATCH | NO | 5 | 1 | PASS |
| SmallBaseOpenPriceActual | mql5 | 438 | `Include/Types.mqh:441:smallBaseOpenPrice` | `Include/Types.mqh:442:reverseSmallOpenPrice` | SEMANTIC_MATCH | NO | 8 | 5 | PASS |
| SmallBaseOpenPriceActual | python | 299 | `Tools/mql5_like_big_scenario_parameter_search.py:42:MT5_SMALL_L1_OPEN_PRICE` | `Tests/HybridSplitBig/hybrid_split_big_reference.py:181:small_open_price` | PARTIAL_MATCH | NO | 1 | 1 | PASS |
| GrossProfit | mql5 | 78 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/StateMachine.mqh:2677:dealCommission` | SEMANTIC_MATCH | NO | 9 | 5 | PASS |
| GrossProfit | python | 37 | `Tools/offline_optimizer.py:271:gross_profit` | `Tests/test_dynamic_reverse_small_money.py:1:small_profit` | PARTIAL_MATCH | NO | 1 | 1 | PASS |
| GrossLoss | mql5 | 88 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/StateMachine.mqh:2677:dealCommission` | AMBIGUOUS | YES | 9 | 5 | PASS |
| GrossLoss | python | 72 | `Tools/offline_optimizer.py:271:gross_profit` | `—` | PARTIAL_MATCH | NO | 1 | 1 | PASS |
| NetProfit | mql5 | 139 | `Include/HybridTransitionPlanner.mqh:14:net` | `Include/StateMachine.mqh:2676:dealProfit` | AMBIGUOUS | YES | 12 | 9 | PASS |
| NetProfit | python | 100 | `Tools/run_full_parameter_optimization_study.py:207:NetProfit` | `Tools/run_full_parameter_optimization_study.py:291:net_profit` | AMBIGUOUS | YES | 1 | 1 | PASS |
| LegNet | mql5 | 124 | `Include/HybridTransitionPlanner.mqh:14:net` | `Include/StateMachine.mqh:5640:net` | AMBIGUOUS | YES | 12 | 9 | PASS |
| LegNet | python | 88 | `Tests/HybridSplitBig/hybrid_split_big_reference.py:21:commission_in_leg_net` | `Tests/HybridSplitBig/hybrid_split_big_reference.py:22:swap_in_leg_net` | AMBIGUOUS | YES | 1 | 1 | PASS |
| BasketNet | mql5 | 115 | `Include/HybridTransitionPlanner.mqh:14:net` | `Include/StateMachine.mqh:5640:net` | AMBIGUOUS | YES | 12 | 9 | PASS |
| BasketNet | python | 88 | `Tests/HybridSplitBig/hybrid_split_big_reference.py:21:commission_in_leg_net` | `Tests/HybridSplitBig/hybrid_split_big_reference.py:22:swap_in_leg_net` | AMBIGUOUS | YES | 1 | 1 | PASS |
| HarvestGross | mql5 | 104 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/StateMachine.mqh:2677:dealCommission` | AMBIGUOUS | YES | 9 | 5 | PASS |
| HarvestGross | python | 44 | `Tools/offline_optimizer.py:271:gross_profit` | `Tests/static/test_split_architecture_static.py:233:test_stage7_actual_split_harvest_net_calculated_is_persisted_and_validated` | PARTIAL_MATCH | NO | 1 | 1 | PASS |
| HarvestNet | mql5 | 158 | `Include/HybridTransitionPlanner.mqh:14:net` | `Include/StateMachine.mqh:5640:net` | AMBIGUOUS | YES | 12 | 9 | PASS |
| HarvestNet | python | 105 | `Tests/static/test_split_architecture_static.py:233:test_stage7_actual_split_harvest_net_calculated_is_persisted_and_validated` | `Tests/unit/test_split_recovery_order_model.py:330:split_harvest_net_context_valid` | AMBIGUOUS | YES | 0 | 0 | PASS |
| SmallReverseNet | mql5 | 391 | `Include/HybridTransitionPlanner.mqh:14:net` | `Include/StateMachine.mqh:5640:net` | AMBIGUOUS | YES | 12 | 9 | PASS |
| SmallReverseNet | python | 255 | `Tests/static/test_split_big_static.py:63:test_split_small_direction_enters_explicit_reverse_fsm_not_legacy_small` | `Tests/test_dynamic_reverse_small_money.py:1:small_profit` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| TransitionNet | mql5 | 123 | `Include/HybridTransitionPlanner.mqh:14:net` | `Include/StateMachine.mqh:5640:net` | AMBIGUOUS | YES | 12 | 9 | PASS |
| TransitionNet | python | 100 | `Tests/HybridSplitBig/hybrid_split_big_reference.py:21:commission_in_leg_net` | `Tests/HybridSplitBig/hybrid_split_big_reference.py:22:swap_in_leg_net` | AMBIGUOUS | YES | 1 | 1 | PASS |
| RealizedCyclePL | mql5 | 112 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/StateMachine.mqh:2677:dealCommission` | AMBIGUOUS | YES | 9 | 5 | PASS |
| RealizedCyclePL | python | 78 | `Tools/hybrid_small_state_machine.py:11:realized_cycle_pl` | `Tests/HybridSplitBig/hybrid_split_big_reference.py:30:realized_cycle_pl` | PARTIAL_MATCH | NO | 2 | 5 | PASS |
| FloatingManagedPL | mql5 | 74 | `Include/StateMachine.mqh:4778:CalculateFarFloatingPL` | `Include/StateMachine.mqh:4794:farFloatingPL` | AMBIGUOUS | YES | 1 | 0 | PASS |
| FloatingManagedPL | python | 49 | `Tests/real_recovery_examples_check.py:6:account_pl` | `Tests/real_recovery_examples_check.py:7:recovery_pl` | AMBIGUOUS | YES | 2 | 3 | PASS |
| ProjectedFloatingPL | mql5 | 105 | `Include/Types.mqh:384:projectedRecoveryPL` | `Include/StateMachine.mqh:4778:CalculateFarFloatingPL` | SEMANTIC_MATCH | NO | 14 | 11 | PASS |
| ProjectedFloatingPL | python | 55 | `Tests/unit/test_big_small_behavior.py:155:projected_margin` | `Tests/unit/test_big_small_behavior.py:156:projected_equity` | AMBIGUOUS | YES | 1 | 0 | PASS |
| RecoveryPLAnalytic | mql5 | 99 | `Include/BrokerMoneyModel.mqh:190:CalcMoveRecoveryDeltaMoney` | `Include/Logger.mqh:345:recoveryPL` | SEMANTIC_MATCH | NO | 1 | 0 | PASS |
| RecoveryPLAnalytic | python | 74 | `Tests/real_recovery_examples_check.py:7:recovery_pl` | `Tools/score_parameters.py:12:recovery_pl` | PARTIAL_MATCH | NO | 35 | 16 | PASS |
| RecoveryPLProjected | mql5 | 99 | `Include/BrokerMoneyModel.mqh:190:CalcMoveRecoveryDeltaMoney` | `Include/Logger.mqh:345:recoveryPL` | SEMANTIC_MATCH | NO | 1 | 0 | PASS |
| RecoveryPLProjected | python | 74 | `Tests/real_recovery_examples_check.py:7:recovery_pl` | `Tools/score_parameters.py:12:recovery_pl` | PARTIAL_MATCH | NO | 35 | 16 | PASS |
| RecoveryPLCloseNow | mql5 | 106 | `Include/BrokerMoneyModel.mqh:190:CalcMoveRecoveryDeltaMoney` | `Include/Logger.mqh:345:recoveryPL` | SEMANTIC_MATCH | NO | 1 | 0 | PASS |
| RecoveryPLCloseNow | python | 79 | `Tests/real_recovery_examples_check.py:7:recovery_pl` | `Tools/score_parameters.py:12:recovery_pl` | PARTIAL_MATCH | NO | 35 | 16 | PASS |
| RealRecoveryPL | mql5 | 138 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/StateMachine.mqh:2677:dealCommission` | AMBIGUOUS | YES | 9 | 5 | PASS |
| RealRecoveryPL | python | 90 | `Tests/real_recovery_examples_check.py:7:recovery_pl` | `Tools/score_parameters.py:12:recovery_pl` | PARTIAL_MATCH | NO | 35 | 16 | PASS |
| RecoverySlope | mql5 | 101 | `Include/BrokerMoneyModel.mqh:190:CalcMoveRecoveryDeltaMoney` | `Include/Logger.mqh:345:recoveryPL` | SEMANTIC_MATCH | NO | 1 | 0 | PASS |
| RecoverySlope | python | 82 | `Tests/real_recovery_examples_check.py:7:recovery_pl` | `Tools/score_parameters.py:12:recovery_pl` | PARTIAL_MATCH | NO | 35 | 16 | PASS |
| RecoveryMonotonicity | mql5 | 99 | `Include/BrokerMoneyModel.mqh:190:CalcMoveRecoveryDeltaMoney` | `Include/Logger.mqh:345:recoveryPL` | SEMANTIC_MATCH | NO | 1 | 0 | PASS |
| RecoveryMonotonicity | python | 75 | `Tests/real_recovery_examples_check.py:7:recovery_pl` | `Tools/score_parameters.py:12:recovery_pl` | PARTIAL_MATCH | NO | 35 | 16 | PASS |
| ExpectedExitCosts | mql5 | 84 | `Include/BrokerMoneyModel.mqh:7:expectedSignedSwap` | `Include/HybridGeometrySolver.mqh:19:costs` | AMBIGUOUS | YES | 13 | 5 | PASS |
| ExpectedExitCosts | python | 55 | `Tests/HybridSplitBig/hybrid_split_big_reference.py:21:commission_in_expected_exit_costs` | `Tests/HybridSplitBig/hybrid_split_big_reference.py:22:swap_in_expected_exit_costs` | AMBIGUOUS | YES | 1 | 1 | PASS |
| CommissionCost | mql5 | 86 | `Include/SimulationEngine.mqh:74:commissionMoney` | `Include/StateMachine.mqh:2677:dealCommission` | SEMANTIC_MATCH | NO | 6 | 1 | PASS |
| CommissionCost | python | 41 | `Tests/HybridSplitBig/hybrid_split_big_reference.py:21:commission_in_expected_exit_costs` | `Tests/unit/test_broker_money_behavior.py:3:commission_side` | PARTIAL_MATCH | NO | 1 | 1 | PASS |
| SwapCost | mql5 | 76 | `Include/SimulationEngine.mqh:74:swapMoney` | `Include/StateMachine.mqh:2678:dealSwap` | SEMANTIC_MATCH | NO | 8 | 1 | PASS |
| SwapCost | python | 41 | `Tests/HybridSplitBig/hybrid_split_big_reference.py:22:swap_in_expected_exit_costs` | `Tests/unit/test_broker_money_behavior.py:3:swap_daily` | PARTIAL_MATCH | NO | 1 | 1 | PASS |
| FeeCost | mql5 | 62 | `Include/SimulationEngine.mqh:74:feeMoney` | `Include/StateMachine.mqh:2679:dealFee` | SEMANTIC_MATCH | NO | 8 | 1 | PASS |
| FeeCost | python | 31 | `Tests/HybridSplitBig/hybrid_split_big_reference.py:23:fee_in_expected_exit_costs` | `Tests/HybridSplitBig/test_catchup_route_hardening.py:8:fee` | PARTIAL_MATCH | NO | 1 | 1 | PASS |
| SpreadCost | mql5 | 59 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/StateMachine.mqh:2677:dealCommission` | AMBIGUOUS | YES | 9 | 5 | PASS |
| SpreadCost | python | 43 | `Tools/hybrid_small_state_machine.py:11:costs` | `Tests/HybridSplitBig/hybrid_split_big_reference.py:21:commission_in_expected_exit_costs` | PARTIAL_MATCH | NO | 2 | 2 | PASS |
| SlippageCost | mql5 | 54 | `Include/SimulationEngine.mqh:74:slippageMoney` | `Include/StateMachine.mqh:2676:dealProfit` | SEMANTIC_MATCH | NO | 6 | 1 | PASS |
| SlippageCost | python | 31 | `Tools/hybrid_small_state_machine.py:11:costs` | `Tests/HybridSplitBig/hybrid_split_big_reference.py:21:commission_in_expected_exit_costs` | PARTIAL_MATCH | NO | 2 | 2 | PASS |
| PositionPLSigned | mql5 | 143 | `Include/Config.mqh:143:ExecutionBufferPerPositionMoney` | `Include/StateMachine.mqh:3487:dealProfit` | SEMANTIC_MATCH | NO | 3 | 1 | PASS |
| PositionPLSigned | python | 36 | `Tests/static/test_split_architecture_static.py:19:test_position_resolution_has_all_split_roles_and_priority_sources` | `Tests/unit/test_split_final_safety_model.py:174:test_restart_open_pending_resolves_existing_position_without_duplicate_order` | AMBIGUOUS | YES | 0 | 0 | PASS |
| FarLossSigned | mql5 | 277 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/StateMachine.mqh:2677:dealCommission` | AMBIGUOUS | YES | 9 | 5 | PASS |
| FarLossSigned | python | 290 | `Tests/unit/test_money_completion_behavior.py:4:signed_swap` | `Tests/unit/test_money_completion_behavior.py:22:test_signed_swap_and_calendar` | AMBIGUOUS | YES | 3 | 0 | PASS |
| FarLossMagnitude | mql5 | 268 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/StateMachine.mqh:2677:dealCommission` | AMBIGUOUS | YES | 9 | 5 | PASS |
| FarLossMagnitude | python | 282 | `Tests/static/test_split_big_static.py:20:test_split_far_active_route_does_not_call_open_big_small` | `Tests/HybridSplitBig/test_catchup_route_state.py:35:test_route_02_far_preserved` | AMBIGUOUS | YES | 0 | 0 | PASS |
| PartialFarBudgetProjected | mql5 | 314 | `Include/HybridPartialFarPreview.mqh:4:HybridPartialFarCloseMoney` | `Include/Types.mqh:477:actualPartialFarCost` | SEMANTIC_MATCH | NO | 3 | 0 | PASS |
| PartialFarBudgetProjected | python | 329 | `Tests/scenario/test_split_big_scenario.py:35:test_reserve_is_not_used_for_partial_budget` | `Tests/unit/test_split_architecture_model.py:44:test_missing_partial_deals_must_not_update_carry_or_reserve` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| PartialFarBudgetReal | mql5 | 294 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/StateMachine.mqh:2677:dealCommission` | AMBIGUOUS | YES | 9 | 5 | PASS |
| PartialFarBudgetReal | python | 320 | `Tests/scenario/test_split_big_scenario.py:35:test_reserve_is_not_used_for_partial_budget` | `Tests/unit/test_split_architecture_model.py:44:test_missing_partial_deals_must_not_update_carry_or_reserve` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| PartialFarBudgetAvailable | mql5 | 276 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/StateMachine.mqh:2677:dealCommission` | AMBIGUOUS | YES | 9 | 5 | PASS |
| PartialFarBudgetAvailable | python | 316 | `Tests/scenario/test_split_big_scenario.py:35:test_reserve_is_not_used_for_partial_budget` | `Tests/unit/test_split_architecture_model.py:44:test_missing_partial_deals_must_not_update_carry_or_reserve` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| PartialFarBudgetConsumed | mql5 | 269 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/StateMachine.mqh:2677:dealCommission` | AMBIGUOUS | YES | 9 | 5 | PASS |
| PartialFarBudgetConsumed | python | 318 | `Tests/scenario/test_split_big_scenario.py:35:test_reserve_is_not_used_for_partial_budget` | `Tests/unit/test_split_architecture_model.py:44:test_missing_partial_deals_must_not_update_carry_or_reserve` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| PartialFarBudgetResidual | mql5 | 273 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/StateMachine.mqh:2677:dealCommission` | AMBIGUOUS | YES | 9 | 5 | PASS |
| PartialFarBudgetResidual | python | 316 | `Tests/scenario/test_split_big_scenario.py:35:test_reserve_is_not_used_for_partial_budget` | `Tests/unit/test_split_architecture_model.py:44:test_missing_partial_deals_must_not_update_carry_or_reserve` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| FinalReserveProjected | mql5 | 257 | `Include/Types.mqh:240:RESERVE_EVENT_SPLIT_BIG_FINAL_DEBIT` | `Include/Types.mqh:245:RESERVE_EVENT_FINAL_CLOSE_DEBIT` | AMBIGUOUS | YES | 5 | 0 | PASS |
| FinalReserveProjected | python | 198 | `Tools/hybrid_small_state_machine.py:11:final_reserve` | `Tests/HybridSplitBig/hybrid_split_big_reference.py:30:final_reserve_real` | PARTIAL_MATCH | NO | 1 | 1 | PASS |
| FinalReserveReal | mql5 | 246 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/StateMachine.mqh:2677:dealCommission` | AMBIGUOUS | YES | 9 | 5 | PASS |
| FinalReserveReal | python | 209 | `Tests/HybridSplitBig/hybrid_split_big_reference.py:30:final_reserve_real` | `Tests/HybridSplitBig/hybrid_split_big_reference.py:181:final_reserve_real` | AMBIGUOUS | YES | 1 | 4 | PASS |
| ReserveAddProjected | mql5 | 230 | `Include/Types.mqh:995:projectedReserveAdd` | `Include/BrokerMoneyModel.mqh:87:CalcProjectedOpenCommission` | PARTIAL_MATCH | NO | 3 | 2 | PASS |
| ReserveAddProjected | python | 163 | `Tests/small_reserve_add_check.py:1:small_reserve_add` | `Tools/hybrid_big_sequence_model.py:9:reserve_added` | PARTIAL_MATCH | NO | 3 | 0 | PASS |
| ReserveAddReal | mql5 | 206 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/StateMachine.mqh:2677:dealCommission` | AMBIGUOUS | YES | 9 | 5 | PASS |
| ReserveAddReal | python | 159 | `Tests/small_reserve_add_check.py:1:small_reserve_add` | `Tools/hybrid_big_sequence_model.py:9:reserve_added` | PARTIAL_MATCH | NO | 3 | 0 | PASS |
| ReserveAvailable | mql5 | 185 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/StateMachine.mqh:2677:dealCommission` | AMBIGUOUS | YES | 9 | 5 | PASS |
| ReserveAvailable | python | 146 | `Tests/small_reserve_add_check.py:1:small_reserve_add` | `Tests/scenario/test_split_big_scenario.py:4:reserve` | AMBIGUOUS | YES | 3 | 0 | PASS |
| ReserveConsumed | mql5 | 176 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/StateMachine.mqh:2677:dealCommission` | AMBIGUOUS | YES | 9 | 5 | PASS |
| ReserveConsumed | python | 148 | `Tests/small_reserve_add_check.py:1:small_reserve_add` | `Tests/scenario/test_split_big_scenario.py:4:reserve` | AMBIGUOUS | YES | 3 | 0 | PASS |
| ReserveResidual | mql5 | 181 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/StateMachine.mqh:2677:dealCommission` | AMBIGUOUS | YES | 9 | 5 | PASS |
| ReserveResidual | python | 147 | `Tests/small_reserve_add_check.py:1:small_reserve_add` | `Tests/scenario/test_split_big_scenario.py:4:reserve` | AMBIGUOUS | YES | 3 | 0 | PASS |
| CarryAvailable | mql5 | 53 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/StateMachine.mqh:2677:dealCommission` | AMBIGUOUS | YES | 9 | 5 | PASS |
| CarryAvailable | python | 36 | `Tests/unit/test_split_architecture_model.py:44:test_missing_partial_deals_must_not_update_carry_or_reserve` | `Tests/unit/test_split_final_safety_model.py:184:test_partial_history_restart_updates_carry_and_reserve_once` | AMBIGUOUS | YES | 0 | 0 | PASS |
| CarryConsumed | mql5 | 43 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/StateMachine.mqh:2677:dealCommission` | AMBIGUOUS | YES | 9 | 5 | PASS |
| CarryConsumed | python | 38 | `Tests/unit/test_split_architecture_model.py:44:test_missing_partial_deals_must_not_update_carry_or_reserve` | `Tests/unit/test_split_final_safety_model.py:184:test_partial_history_restart_updates_carry_and_reserve_once` | AMBIGUOUS | YES | 0 | 0 | PASS |
| CarryResidual | mql5 | 48 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/StateMachine.mqh:2677:dealCommission` | AMBIGUOUS | YES | 9 | 5 | PASS |
| CarryResidual | python | 37 | `Tests/unit/test_split_architecture_model.py:44:test_missing_partial_deals_must_not_update_carry_or_reserve` | `Tests/unit/test_split_final_safety_model.py:184:test_partial_history_restart_updates_carry_and_reserve_once` | AMBIGUOUS | YES | 0 | 0 | PASS |
| TransitionBudgetAvailable | mql5 | 71 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/StateMachine.mqh:2677:dealCommission` | AMBIGUOUS | YES | 9 | 5 | PASS |
| TransitionBudgetAvailable | python | 58 | `Tests/scenario/test_split_big_scenario.py:35:test_reserve_is_not_used_for_partial_budget` | `Tests/HybridSplitBig/test_catchup_route_state.py:37:test_route_03_budget_preserved` | AMBIGUOUS | YES | 0 | 0 | PASS |
| FinalCloseRequirement | mql5 | 254 | `Include/StateMachine.mqh:2676:dealProfit` | `Include/StateMachine.mqh:2677:dealCommission` | AMBIGUOUS | YES | 9 | 5 | PASS |
| FinalCloseRequirement | python | 166 | `Tests/static/test_split_architecture_static.py:49:test_split_final_close_comment_and_guard_are_present` | `Tests/static/test_split_architecture_static.py:286:test_final_close_gate_exists_and_small_reserve_uses_it` | AMBIGUOUS | YES | 0 | 0 | PASS |
| BasketRiskMoney | mql5 | 129 | `Include/HybridPartialFarPreview.mqh:4:HybridPartialFarCloseMoney` | `Include/HybridCatchUpModel.mqh:6:HybridCatchUpMoneyRound` | AMBIGUOUS | YES | 3 | 0 | PASS |
| BasketRiskMoney | python | 48 | `Tests/unit/test_broker_money_behavior.py:3:money` | `Tests/static/test_end_to_end_completion.py:3:money` | AMBIGUOUS | YES | 51 | 5 | PASS |
| AccountRiskMoney | mql5 | 126 | `Include/HybridPartialFarPreview.mqh:4:HybridPartialFarCloseMoney` | `Include/HybridCatchUpModel.mqh:6:HybridCatchUpMoneyRound` | AMBIGUOUS | YES | 3 | 0 | PASS |
| AccountRiskMoney | python | 45 | `Tests/unit/test_broker_money_behavior.py:3:money` | `Tests/static/test_end_to_end_completion.py:3:money` | AMBIGUOUS | YES | 51 | 5 | PASS |
| BigRatio | mql5 | 265 | `Include/Config.mqh:30:BigRatio` | `Include/Config.mqh:42:BigCoreRatio` | AMBIGUOUS | YES | 3 | 1 | PASS |
| BigRatio | python | 208 | `Tests/small_reverse_compression_check.py:1:big_ratio` | `Tests/small_reverse_compression_check.py:5:big_ratio` | AMBIGUOUS | YES | 21 | 4 | PASS |
| SmallRatio | mql5 | 234 | `Include/Config.mqh:31:SmallRatio` | `Include/Config.mqh:44:SmallBaseToFarRatio` | AMBIGUOUS | YES | 1 | 1 | PASS |
| SmallRatio | python | 200 | `Tests/small_reverse_compression_check.py:6:small_ratio` | `Tools/analyze_mt5_big_scenario_divergence.py:21:SMALL_RATIO` | PARTIAL_MATCH | NO | 21 | 5 | PASS |
| CloseBigOnSmallShare | mql5 | 606 | `Include/Config.mqh:34:CloseFarShare` | `Include/Config.mqh:36:SmallReserveShare` | AMBIGUOUS | YES | 2 | 1 | PASS |
| CloseBigOnSmallShare | python | 438 | `Tools/analyze_mt5_big_scenario_divergence.py:22:CLOSE_FAR_SHARE` | `Tools/calibrate_big_scenario_model_from_mt5_report.py:25:CLOSE_FAR_SHARE` | AMBIGUOUS | YES | 4 | 2 | PASS |
| RemainBigOnSmallShare | mql5 | 469 | `Include/Config.mqh:36:SmallReserveShare` | `Include/Config.mqh:30:BigRatio` | SEMANTIC_MATCH | NO | 4 | 1 | PASS |
| RemainBigOnSmallShare | python | 371 | `Tests/small_reverse_compression_check.py:1:big_ratio` | `Tests/small_reserve_add_check.py:1:share` | AMBIGUOUS | YES | 21 | 4 | PASS |
| CloseFarShare | mql5 | 397 | `Include/Config.mqh:34:CloseFarShare` | `Include/Config.mqh:55:HybridPartialFarShare` | SEMANTIC_MATCH | NO | 2 | 1 | PASS |
| CloseFarShare | python | 340 | `Tools/analyze_mt5_big_scenario_divergence.py:22:CLOSE_FAR_SHARE` | `Tools/calibrate_big_scenario_model_from_mt5_report.py:25:CLOSE_FAR_SHARE` | AMBIGUOUS | YES | 4 | 2 | PASS |
| ReserveShare | mql5 | 150 | `Include/Config.mqh:35:ReserveShare` | `Include/Config.mqh:36:SmallReserveShare` | AMBIGUOUS | YES | 4 | 2 | PASS |
| ReserveShare | python | 153 | `Tests/small_reserve_add_check.py:1:share` | `Tools/analyze_mt5_big_scenario_divergence.py:22:CLOSE_FAR_SHARE` | PARTIAL_MATCH | NO | 2 | 1 | PASS |
| SmallReserveShare | mql5 | 350 | `Include/Config.mqh:36:SmallReserveShare` | `Include/Config.mqh:35:ReserveShare` | SEMANTIC_MATCH | NO | 4 | 1 | PASS |
| SmallReserveShare | python | 304 | `Tests/small_reserve_add_check.py:1:share` | `Tests/small_reverse_compression_check.py:6:small_ratio` | AMBIGUOUS | YES | 2 | 1 | PASS |
| CompressionRatio | mql5 | 33 | `Include/Config.mqh:77:MinimumFarCompressionRatio` | `Include/Types.mqh:489:newFarCompressionRatio` | SEMANTIC_MATCH | NO | 1 | 1 | PASS |
| CompressionRatio | python | 64 | `Tools/offline_optimizer.py:107:compression_ratio` | `Tools/offline_optimizer.py:174:compression_ratios` | AMBIGUOUS | YES | 1 | 1 | PASS |
| ReserveCoverageRatio | mql5 | 180 | `Include/Config.mqh:60:MinimumReserveCatchUpRatio` | `Include/Config.mqh:30:BigRatio` | SEMANTIC_MATCH | NO | 7 | 1 | PASS |
| ReserveCoverageRatio | python | 213 | `Tools/offline_optimizer.py:268:coverage_ratio` | `Tools/offline_optimizer.py:478:coverage_ratio` | AMBIGUOUS | YES | 7 | 1 | PASS |
| RecoveryCoverageRatio | mql5 | 113 | `Include/Config.mqh:30:BigRatio` | `Include/Config.mqh:31:SmallRatio` | AMBIGUOUS | YES | 3 | 1 | PASS |
| RecoveryCoverageRatio | python | 161 | `Tests/unit/test_big_small_behavior.py:77:test_big_requires_strict_recovery_and_coverage_growth` | `Tools/offline_optimizer.py:268:coverage_ratio` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| MaximumNewBigToOldFarRatio | mql5 | 498 | `Include/Config.mqh:59:MaximumNewBigToOldFarRatio` | `Include/Config.mqh:78:MaximumNewFarRatio` | SEMANTIC_MATCH | NO | 8 | 1 | PASS |
| MaximumNewBigToOldFarRatio | python | 463 | `Tools/offline_optimizer.py:108:new_big_to_old_far_ratio` | `Tools/hybrid_geometry_model.py:42:max_new_big_ratio` | PARTIAL_MATCH | NO | 1 | 1 | PASS |
| MinimumReserveCatchUpRatio | mql5 | 215 | `Include/Config.mqh:60:MinimumReserveCatchUpRatio` | `Include/Config.mqh:77:MinimumFarCompressionRatio` | SEMANTIC_MATCH | NO | 7 | 1 | PASS |
| MinimumReserveCatchUpRatio | python | 207 | `Tests/test_new_far_compression.py:1:ratio` | `Tests/test_dynamic_reverse_small_direction.py:1:buffer_ratio` | AMBIGUOUS | YES | 6 | 2 | PASS |
| PercentValue | mql5 | 19 | `Include/Config.mqh:114:HybridCatchUpMarginSafetyPercent` | `Include/Config.mqh:135:CommissionPercent` | AMBIGUOUS | YES | 1 | 1 | PASS |
| PercentValue | python | 21 | `Tests/HybridSplitBig/test_catchup_full_dimension_contract.py:5:PERCENT_TOL` | `Tests/HybridSplitBig/test_catchup_full_dimension_contract.py:12:percent_ge` | AMBIGUOUS | YES | 4 | 1 | PASS |
| ScaleMultiplier | mql5 | 7 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| ScaleMultiplier | python | 24 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| RiskThresholdRatio | mql5 | 43 | `Include/Config.mqh:30:BigRatio` | `Include/Config.mqh:31:SmallRatio` | AMBIGUOUS | YES | 3 | 1 | PASS |
| RiskThresholdRatio | python | 60 | `Tests/test_new_far_compression.py:1:ratio` | `Tests/test_dynamic_reverse_small_direction.py:1:buffer_ratio` | AMBIGUOUS | YES | 6 | 2 | PASS |
| SymbolId | mql5 | 81 | `Include/Logger.mqh:6:SymbolLogPrefix` | `Include/Logger.mqh:26:CsvSafeSymbol` | AMBIGUOUS | YES | 4 | 0 | PASS |
| SymbolId | python | 83 | `Tests/HybridSplitBig/test_catchup_route_hardening.py:11:symbol` | `Tests/unit/test_split_recovery_order_model.py:21:event_id` | AMBIGUOUS | YES | 61 | 5 | PASS |
| MagicId | mql5 | 48 | `Include/Types.mqh:251:eventId` | `Include/Types.mqh:347:expectedLedgerEventId` | AMBIGUOUS | YES | 27 | 1 | PASS |
| MagicId | python | 54 | `Tests/HybridSplitBig/test_catchup_route_hardening.py:11:magic` | `Tests/unit/test_split_recovery_order_model.py:21:event_id` | AMBIGUOUS | YES | 5 | 3 | PASS |
| CycleId | mql5 | 92 | `Include/Types.mqh:251:eventId` | `Include/Types.mqh:347:expectedLedgerEventId` | AMBIGUOUS | YES | 27 | 1 | PASS |
| CycleId | python | 76 | `Tests/unit/test_split_reserve_transaction_model.py:24:cycle_id` | `Tests/unit/test_split_exact_persistence_model.py:39:cycle_id` | AMBIGUOUS | YES | 4 | 4 | PASS |
| RoleId | mql5 | 82 | `Include/Types.mqh:251:eventId` | `Include/Types.mqh:347:expectedLedgerEventId` | AMBIGUOUS | YES | 27 | 1 | PASS |
| RoleId | python | 62 | `Tests/unit/test_split_recovery_order_model.py:21:event_id` | `Tests/unit/test_split_reserve_transaction_model.py:24:cycle_id` | AMBIGUOUS | YES | 3 | 2 | PASS |
| PositionIdentifier | mql5 | 162 | `Include/SimulationEngine.mqh:74:positionIdentifier` | `Include/SimulationEngine.mqh:97:positionIdentifier` | AMBIGUOUS | YES | 7 | 2 | PASS |
| PositionIdentifier | python | 53 | `Tests/stage_3_1_3/source_evidence.py:16:identifier` | `Tests/stage_3_1_3/discovery.py:24:identifier` | AMBIGUOUS | YES | 51 | 7 | PASS |
| PositionTicket | mql5 | 194 | `Include/SimulationEngine.mqh:74:positionIdentifier` | `Include/PositionUtils.mqh:81:ticket` | AMBIGUOUS | YES | 7 | 2 | PASS |
| PositionTicket | python | 42 | `Tests/unit/test_clean_start_persistence_behavior.py:26:ticket` | `Tests/unit/test_split_final_safety_model.py:27:ticket` | AMBIGUOUS | YES | 2 | 2 | PASS |
| OrderTicket | mql5 | 99 | `Include/PositionResolutionEngine.mqh:45:IsKnownContextTicketOrIdentifier` | `Include/SimulationEngine.mqh:118:SimFindIndexByTicket` | AMBIGUOUS | YES | 2 | 0 | PASS |
| OrderTicket | python | 16 | `Tests/unit/test_clean_start_persistence_behavior.py:26:ticket` | `Tests/unit/test_split_final_safety_model.py:27:ticket` | AMBIGUOUS | YES | 2 | 2 | PASS |
| DealTicket | mql5 | 144 | `Include/SimulationEngine.mqh:74:createdDealTicket` | `Include/ReconciliationEngine.mqh:255:dealTicket` | AMBIGUOUS | YES | 4 | 2 | PASS |
| DealTicket | python | 12 | `Tests/unit/test_clean_start_persistence_behavior.py:26:ticket` | `Tests/unit/test_split_final_safety_model.py:27:ticket` | AMBIGUOUS | YES | 2 | 2 | PASS |
| EventId | mql5 | 86 | `Include/Types.mqh:251:eventId` | `Include/Types.mqh:347:expectedLedgerEventId` | AMBIGUOUS | YES | 27 | 1 | PASS |
| EventId | python | 77 | `Tests/unit/test_split_recovery_order_model.py:21:event_id` | `Tests/unit/test_split_recovery_order_model.py:36:expected_event_id` | AMBIGUOUS | YES | 3 | 2 | PASS |
| EventKey | mql5 | 62 | `Include/Types.mqh:251:eventId` | `Include/Types.mqh:347:expectedLedgerEventId` | AMBIGUOUS | YES | 27 | 1 | PASS |
| EventKey | python | 67 | `Tests/scenario/test_split_architecture_restart.py:35:test_multicurrency_event_keys_do_not_mix_same_magic` | `Tests/unit/test_split_exact_persistence_model.py:160:test_full_event_key_serialization_with_large_identifiers_bit_exact` | AMBIGUOUS | YES | 0 | 0 | PASS |
| SnapshotFingerprint | mql5 | 65 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| SnapshotFingerprint | python | 24 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| PlanFingerprint | mql5 | 17 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| PlanFingerprint | python | 16 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| PositionComment | mql5 | 162 | `Include/Types.mqh:351:PositionResolutionResult` | `Include/Types.mqh:362:PositionSnapshot` | AMBIGUOUS | YES | 21 | 0 | PASS |
| PositionComment | python | 42 | `Tools/hybrid_small_state_machine.py:6:PositionState` | `Tests/unit/test_big_small_behavior.py:6:Position` | PARTIAL_MATCH | NO | 3 | 0 | PASS |
| SnapshotRevision | mql5 | 62 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| SnapshotRevision | python | 16 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| StateRevision | mql5 | 207 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| StateRevision | python | 179 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| State | mql5 | 207 | `Include/StateMachine.mqh:4:StateIntegrityValidationInProgress` | `Include/Types.mqh:6:STATE_IDLE` | SEMANTIC_MATCH | NO | 2 | 4 | PASS |
| State | python | 179 | `Tests/test_symbol_magic_isolation.py:2:state` | `Tests/test_symbol_magic_cycle_isolation.py:2:state` | AMBIGUOUS | YES | 269 | 120 | PASS |
| Phase | mql5 | 8 | `Include/Types.mqh:108:HarvestPhase` | `Include/Types.mqh:307:RECOVERY_FAILURE_PHASE_CONFLICT` | AMBIGUOUS | YES | 5 | 0 | PASS |
| Phase | python | 22 | `Tools/hybrid_small_state_machine.py:11:phase_history` | `Tools/hybrid_small_state_machine.py:11:phase` | AMBIGUOUS | YES | 2 | 1 | PASS |
| Event | mql5 | 52 | `Include/Types.mqh:118:TestMarketEvent` | `Include/Types.mqh:278:ReserveEventContextSnapshot` | AMBIGUOUS | YES | 13 | 0 | PASS |
| Event | python | 37 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| Observation | mql5 | 0 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| Observation | python | 0 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| GateResult | mql5 | 92 | `Include/HybridDecisionEngine.mqh:4:HybridResetResult` | `Include/PositionResolutionEngine.mqh:20:ResolutionResultFromSnapshot` | AMBIGUOUS | YES | 1 | 0 | PASS |
| GateResult | python | 35 | `Tests/HybridSplitBig/hybrid_split_big_reference.py:129:gate_results` | `Tools/prove_hybrid_split_big.py:17:result` | PARTIAL_MATCH | NO | 0 | 1 | PASS |
| ExecutionResult | mql5 | 63 | `Include/BrokerMoneyModel.mqh:4:SignedSwapResult` | `Include/BrokerMoneyModel.mqh:15:CommissionBaseResult` | AMBIGUOUS | YES | 5 | 0 | PASS |
| ExecutionResult | python | 30 | `Tests/HybridSplitBig/hybrid_split_big_reference.py:26:EvaluationResult` | `Tools/offline_optimizer.py:98:ScenarioResult` | PARTIAL_MATCH | NO | 25 | 0 | PASS |
| Outcome | mql5 | 27 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| Outcome | python | 7 | `Tests/HybridSplitBig/test_catchup_stage12.py:7:Outcome` | `—` | PARTIAL_MATCH | NO | 17 | 0 | PASS |
| ReasonCode | mql5 | 119 | `Include/HybridCatchUpModel.mqh:40:HybridCatchUpReasonCode` | `Include/Types.mqh:541:geometryFallbackReasonCode` | SEMANTIC_MATCH | NO | 2 | 0 | PASS |
| ReasonCode | python | 54 | `Tests/static/test_split_architecture_static.py:201:test_stage7_recovery_failure_marker_persists_original_state_and_reason_code` | `Tests/HybridSplitBig/test_catchup_stage12.py:55:test_fo12_stable_reason_code` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| ErrorCode | mql5 | 52 | `Include/Types.mqh:95:STATE_INTEGRITY_ERROR` | `Include/Types.mqh:101:STATE_ERROR_OPEN_BIG_CORE` | AMBIGUOUS | YES | 22 | 0 | PASS |
| ErrorCode | python | 24 | `Tests/unit/test_split_reserve_transaction_model.py:130:test_recover_state_stops_before_reconciliation_and_trading_on_load_error` | `Tests/static/test_split_architecture_static.py:201:test_stage7_recovery_failure_marker_persists_original_state_and_reason_code` | AMBIGUOUS | YES | 0 | 0 | PASS |
| DiagnosticText | mql5 | 5 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| DiagnosticText | python | 72 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| CandidatePlan | mql5 | 28 | `Include/Types.mqh:962:HybridCandidatePlan` | `Include/Types.mqh:404:HybridReversePlan` | SEMANTIC_MATCH | NO | 9 | 0 | PASS |
| CandidatePlan | python | 46 | `Tools/hybrid_geometry_model.py:33:Candidate` | `Tests/stage_3_1_3/discovery.py:44:Candidate` | PARTIAL_MATCH | NO | 21 | 0 | PASS |
| ApprovedImmutablePlan | mql5 | 12 | `Include/Types.mqh:404:HybridReversePlan` | `Include/Types.mqh:962:HybridCandidatePlan` | AMBIGUOUS | YES | 5 | 0 | PASS |
| ApprovedImmutablePlan | python | 8 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| ExecutionRequest | mql5 | 18 | `Tests/stage_3_1_3/fixtures/positive/valid_request.mqh:1:ExecutionRequest` | `—` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| ExecutionRequest | python | 11 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| BrokerExecutionResult | mql5 | 75 | `Include/HybridDecisionEngine.mqh:4:HybridResetResult` | `Include/PositionResolutionEngine.mqh:20:ResolutionResultFromSnapshot` | AMBIGUOUS | YES | 1 | 0 | PASS |
| BrokerExecutionResult | python | 48 | `Tools/prove_hybrid_split_big.py:17:result` | `Tools/hybrid_big_sequence_model.py:17:result` | AMBIGUOUS | YES | 36 | 11 | PASS |
| ReconciledResult | mql5 | 50 | `Include/BrokerMoneyModel.mqh:4:SignedSwapResult` | `Include/BrokerMoneyModel.mqh:15:CommissionBaseResult` | AMBIGUOUS | YES | 5 | 0 | PASS |
| ReconciledResult | python | 23 | `Tests/HybridSplitBig/hybrid_split_big_reference.py:26:EvaluationResult` | `Tools/offline_optimizer.py:98:ScenarioResult` | PARTIAL_MATCH | NO | 25 | 0 | PASS |
| CommittedLedgerEvent | mql5 | 83 | `Tests/stage_3_1_3/fixtures/positive/valid_ledger.mqh:1:CommittedLedgerEvent` | `Include/Types.mqh:118:TestMarketEvent` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| CommittedLedgerEvent | python | 75 | `Tests/unit/test_split_architecture_model.py:5:Ledger` | `Tests/unit/test_split_recovery_order_model.py:20:LedgerEntry` | AMBIGUOUS | YES | 5 | 0 | PASS |
| BaseSnapshot | mql5 | 117 | `Include/BrokerMoneyModel.mqh:24:DirectionalVolumeSnapshot` | `Include/Types.mqh:278:ReserveEventContextSnapshot` | AMBIGUOUS | YES | 1 | 0 | PASS |
| BaseSnapshot | python | 57 | `Tests/unit/test_split_recovery_order_model.py:11:Snapshot` | `Tests/unit/test_split_reserve_transaction_model.py:21:Snapshot` | AMBIGUOUS | YES | 23 | 0 | PASS |
| WorstSnapshot | mql5 | 84 | `Include/BrokerMoneyModel.mqh:24:DirectionalVolumeSnapshot` | `Include/Types.mqh:278:ReserveEventContextSnapshot` | AMBIGUOUS | YES | 1 | 0 | PASS |
| WorstSnapshot | python | 40 | `Tests/unit/test_split_recovery_order_model.py:11:Snapshot` | `Tests/unit/test_split_reserve_transaction_model.py:21:Snapshot` | AMBIGUOUS | YES | 23 | 0 | PASS |
| ActualSnapshot | mql5 | 112 | `Tests/stage_3_1_3/fixtures/positive/valid_snapshot.mqh:1:ActualSnapshot` | `Include/BrokerMoneyModel.mqh:24:DirectionalVolumeSnapshot` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| ActualSnapshot | python | 40 | `Tests/unit/test_split_recovery_order_model.py:11:Snapshot` | `Tests/unit/test_split_reserve_transaction_model.py:21:Snapshot` | AMBIGUOUS | YES | 23 | 0 | PASS |
| SnapshotStaleFlag | mql5 | 61 | `Include/BrokerMoneyModel.mqh:24:DirectionalVolumeSnapshot` | `Include/Types.mqh:278:ReserveEventContextSnapshot` | AMBIGUOUS | YES | 1 | 0 | PASS |
| SnapshotStaleFlag | python | 20 | `Tests/unit/test_split_recovery_order_model.py:11:Snapshot` | `Tests/unit/test_split_reserve_transaction_model.py:21:Snapshot` | AMBIGUOUS | YES | 23 | 0 | PASS |
| FinalClosePreview | mql5 | 238 | `Include/Types.mqh:1097:HybridFinalCloseRouteState` | `Include/Types.mqh:376:FinalCloseEvaluation` | SEMANTIC_MATCH | NO | 9 | 0 | PASS |
| FinalClosePreview | python | 167 | `Tests/HybridSplitBig/hybrid_split_big_reference.py:177:FinalDecisionCode` | `—` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| FinalCloseActualSuccess | mql5 | 280 | `Include/Types.mqh:1097:HybridFinalCloseRouteState` | `Include/Types.mqh:376:FinalCloseEvaluation` | SEMANTIC_MATCH | NO | 9 | 0 | PASS |
| FinalCloseActualSuccess | python | 186 | `Tests/HybridSplitBig/hybrid_split_big_reference.py:177:FinalDecisionCode` | `—` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| MoneyTolerance | mql5 | 120 | `Include/Config.mqh:147:MoneyCalculationTolerance` | `Include/Config.mqh:61:MinimumRecoverySlopeMoneyPerPoint` | SEMANTIC_MATCH | NO | 30 | 1 | PASS |
| MoneyTolerance | python | 44 | `Tests/unit/test_broker_money_behavior.py:3:money` | `Tests/static/test_end_to_end_completion.py:3:money` | AMBIGUOUS | YES | 51 | 5 | PASS |
| VolumeToleranceLots | mql5 | 313 | `Include/Config.mqh:171:VolumeMismatchToleranceLots` | `Include/Config.mqh:76:MinimumFarCompressionLots` | SEMANTIC_MATCH | NO | 94 | 1 | PASS |
| VolumeToleranceLots | python | 225 | `Tests/offline_lowlot_priority_check.py:5:accepted_lots` | `Tests/HybridSplitBig/test_catchup_dimension_safe.py:9:lot_tolerance` | AMBIGUOUS | YES | 3 | 1 | PASS |
| PriceTolerance | mql5 | 116 | `Include/HybridCatchUpModel.mqh:208:HybridPriceTolerance` | `Include/HybridPartialFarPreview.mqh:6:price` | SEMANTIC_MATCH | NO | 3 | 0 | PASS |
| PriceTolerance | python | 33 | `Tests/HybridSplitBig/test_catchup_dimension_safe.py:11:price_tolerance` | `Tests/HybridSplitBig/test_catchup_dimension_safe.py:27:test_tol11_worst_price_uses_price_tolerance` | AMBIGUOUS | YES | 1 | 0 | PASS |
| PointTolerance | mql5 | 105 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| PointTolerance | python | 95 | `Tests/unit/test_split_reserve_transaction_model.py:13:FailPoint` | `—` | PARTIAL_MATCH | NO | 8 | 0 | PASS |
| RatioTolerance | mql5 | 42 | `Include/Config.mqh:30:BigRatio` | `Include/Config.mqh:31:SmallRatio` | AMBIGUOUS | YES | 3 | 1 | PASS |
| RatioTolerance | python | 62 | `Tests/test_new_far_compression.py:1:ratio` | `Tests/test_dynamic_reverse_small_direction.py:1:buffer_ratio` | AMBIGUOUS | YES | 6 | 2 | PASS |
| ComparisonEpsilon | mql5 | 0 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| ComparisonEpsilon | python | 2 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| ReserveMismatchTolerance | mql5 | 196 | `Include/Config.mqh:170:ReserveMismatchTolerance` | `Include/Config.mqh:64:RejectReserveCatchUpBelowMinimum` | SEMANTIC_MATCH | NO | 31 | 1 | PASS |
| ReserveMismatchTolerance | python | 155 | `Tests/small_reserve_add_check.py:1:small_reserve_add` | `Tests/scenario/test_split_big_scenario.py:4:reserve` | AMBIGUOUS | YES | 3 | 0 | PASS |
| GeometryTolerance | mql5 | 142 | `Include/Config.mqh:171:VolumeMismatchToleranceLots` | `Include/ReconciliationEngine.mqh:66:ReconciliationVolumeTolerance` | SEMANTIC_MATCH | NO | 94 | 1 | PASS |
| GeometryTolerance | python | 25 | `Tests/HybridSplitBig/test_catchup_dimension_safe.py:9:lot_tolerance` | `Tests/HybridSplitBig/test_catchup_dimension_safe.py:26:test_tol10_worst_far_uses_lot_tolerance` | AMBIGUOUS | YES | 1 | 0 | PASS |
| FingerprintTolerance | mql5 | 21 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| FingerprintTolerance | python | 17 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| ProjectedData | mql5 | 56 | `Include/StateMachine.mqh:3988:ProjectedCloseNetResult` | `—` | SEMANTIC_MATCH | NO | 14 | 0 | PASS |
| ProjectedData | python | 16 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| RequestedData | mql5 | 6 | `Tests/stage_3_1_3/fixtures/positive/valid_request.mqh:1:ExecutionRequest` | `—` | PARTIAL_MATCH | NO | 0 | 0 | PASS |
| RequestedData | python | 4 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| ExecutedData | mql5 | 0 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| ExecutedData | python | 0 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| ConfirmedData | mql5 | 1 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| ConfirmedData | python | 0 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| ReconciledData | mql5 | 0 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| ReconciledData | python | 0 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| PersistedData | mql5 | 18 | `Include/Types.mqh:135:PersistedUInt64Inspection` | `Include/Types.mqh:151:PersistedRoleInspection` | AMBIGUOUS | YES | 18 | 0 | PASS |
| PersistedData | python | 3 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| StaleData | mql5 | 0 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| StaleData | python | 0 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| InvalidData | mql5 | 10 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| InvalidData | python | 4 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| NotApplicableValue | mql5 | 5 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| NotApplicableValue | python | 23 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| NotCalculatedValue | mql5 | 15 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| NotCalculatedValue | python | 26 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| NotAvailableValue | mql5 | 15 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| NotAvailableValue | python | 28 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| UnknownValue | mql5 | 0 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| UnknownValue | python | 0 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| CurrentBid | mql5 | 27 | `Include/Types.mqh:121:MarketBid` | `Include/RecoveryMath.mqh:7:tickSize` | PARTIAL_MATCH | NO | 11 | 0 | PASS |
| CurrentBid | python | 17 | `Tests/HybridSplitBig/test_catchup_temporal_model.py:12:close_bid` | `Tests/HybridSplitBig/test_catchup_route_hardening.py:12:bid` | AMBIGUOUS | YES | 9 | 1 | PASS |
| CurrentAsk | mql5 | 27 | `Include/HybridPartialFarPreview.mqh:4:ask` | `Include/HybridCatchUpModel.mqh:7:ask` | AMBIGUOUS | YES | 62 | 12 | PASS |
| CurrentAsk | python | 16 | `Tests/HybridSplitBig/test_catchup_temporal_model.py:12:close_ask` | `Tests/HybridSplitBig/test_catchup_route_hardening.py:12:ask` | AMBIGUOUS | YES | 7 | 1 | PASS |
| ReserveProjected | mql5 | 225 | `Include/BrokerMoneyModel.mqh:87:CalcProjectedOpenCommission` | `Include/BrokerMoneyModel.mqh:95:CalcProjectedCloseCommission` | AMBIGUOUS | YES | 3 | 0 | PASS |
| ReserveProjected | python | 153 | `Tests/unit/test_big_small_behavior.py:155:projected_margin` | `Tests/unit/test_big_small_behavior.py:156:projected_equity` | AMBIGUOUS | YES | 1 | 0 | PASS |
| ReserveCoverage | mql5 | 156 | `Include/Config.mqh:35:ReserveShare` | `Include/Config.mqh:36:SmallReserveShare` | AMBIGUOUS | YES | 4 | 2 | PASS |
| ReserveCoverage | python | 164 | `Tools/hybrid_big_sequence_model.py:11:coverage_deficit_before` | `Tools/hybrid_big_sequence_model.py:11:coverage_deficit_after` | AMBIGUOUS | YES | 1 | 1 | PASS |
| Symbol | mql5 | 42 | `Include/Logger.mqh:6:SymbolLogPrefix` | `Include/Logger.mqh:26:CsvSafeSymbol` | AMBIGUOUS | YES | 4 | 0 | PASS |
| Symbol | python | 38 | `Tests/HybridSplitBig/test_catchup_route_hardening.py:11:symbol` | `Tests/unit/test_broker_money_behavior.py:22:test_symbol_data` | AMBIGUOUS | YES | 61 | 5 | PASS |
| MagicNumber | mql5 | 9 | `Include/Types.mqh:262:magicNumber` | `Include/Types.mqh:285:magicNumber` | AMBIGUOUS | YES | 14 | 3 | PASS |
| MagicNumber | python | 9 | `Tests/HybridSplitBig/test_catchup_route_hardening.py:11:magic` | `Tests/scenario/test_split_architecture_restart.py:35:test_multicurrency_event_keys_do_not_mix_same_magic` | AMBIGUOUS | YES | 5 | 3 | PASS |
| CycleID | mql5 | 92 | `Include/Types.mqh:251:eventId` | `Include/Types.mqh:347:expectedLedgerEventId` | AMBIGUOUS | YES | 27 | 1 | PASS |
| CycleID | python | 76 | `Tests/unit/test_split_reserve_transaction_model.py:24:cycle_id` | `Tests/unit/test_split_exact_persistence_model.py:39:cycle_id` | AMBIGUOUS | YES | 4 | 4 | PASS |
| EventID | mql5 | 86 | `Include/Types.mqh:251:eventId` | `Include/Types.mqh:347:expectedLedgerEventId` | AMBIGUOUS | YES | 27 | 1 | PASS |
| EventID | python | 77 | `Tests/unit/test_split_recovery_order_model.py:21:event_id` | `Tests/unit/test_split_recovery_order_model.py:36:expected_event_id` | AMBIGUOUS | YES | 3 | 2 | PASS |
| Fingerprint | mql5 | 5 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| Fingerprint | python | 8 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| Comment | mql5 | 53 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| Comment | python | 7 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| Preview | mql5 | 13 | `Include/Types.mqh:1084:HybridPartialFarPreviewResult` | `Include/Types.mqh:1170:HybridMarginPreview` | AMBIGUOUS | YES | 8 | 0 | PASS |
| Preview | python | 2 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| Candidate | mql5 | 18 | `Include/Types.mqh:962:HybridCandidatePlan` | `Tests/stage_3_1_3/fixtures/positive/valid_plan.mqh:1:CandidatePlan` | PARTIAL_MATCH | NO | 9 | 0 | PASS |
| Candidate | python | 38 | `Tools/hybrid_geometry_model.py:33:Candidate` | `Tests/stage_3_1_3/discovery.py:44:Candidate` | PARTIAL_MATCH | NO | 21 | 0 | PASS |
| Plan | mql5 | 12 | `Include/Types.mqh:404:HybridReversePlan` | `Include/Types.mqh:962:HybridCandidatePlan` | AMBIGUOUS | YES | 5 | 0 | PASS |
| Plan | python | 8 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |
| ApprovedPlan | mql5 | 12 | `Include/Types.mqh:404:HybridReversePlan` | `Include/Types.mqh:962:HybridCandidatePlan` | AMBIGUOUS | YES | 5 | 0 | PASS |
| ApprovedPlan | python | 8 | `—` | `—` | MISSING | NO | 0 | 0 | PASS |


## ACCEPTANCE_ATTACKS

```text
HIDDEN_CANDIDATE=PASS
HIDDEN_USE=PASS
MONEY_AS_LOT=PASS
CACHE_AS_AUTHORITY=PASS
SYMBOL_ONLY_AS_SYMBOL_MAGIC=PASS
MAGIC_ONLY_AS_SYMBOL_MAGIC=PASS
TEST_ANALOGUE_AS_RUNTIME=PASS
COMPETING_EXACT=PASS
```

## SCOPE_CONTROL

```text
MQL5_CHANGED=NO
MQH_CHANGED=NO
TRADING_LOGIC_CHANGED=NO
STAGE_3_1_4_STARTED=NO
```

```text
STAGE_3_1_3_SIXTH_CORRECTION_STATUS=PASS
```

Validator самостоятельно обнаруживает candidates и полный use graph, строит dataflow/source/scope evidence, сам выбирает winner/AMBIGUOUS/MISSING, а JSON используется только как documented claim. Этап 3.1.3 ожидает независимую проверку пользователя. Этап 3.1.4 не выполнялся.

## STAGE_3_1_3_SEVENTH_CORRECTION

### Baseline и воспроизведённые дефекты

- Исходный опубликованный baseline шестой коррекции: `3b94a2c1e59899e1e86534db7209af2ac4a8d25e`.
- Локальная расходящаяся документационная ветвь безопасно объединена с `origin/work` merge-коммитом `15c54ab15944da5728759f2a1c8a4fb4cf0da164`, без reset/rebase/force-push.
- Воспроизведены объединение одноимённых declarations, константный entity-nature proof, строковый RHS dataflow, отсутствие fixed-point unit propagation, константные scope-support flags и неточные fixture assertions.

### Архитектурные изменения

- Use graph принадлежит `DeclarationIdentity=(language,file,scope,line,column,identifier)`, поэтому shadowing не смешивает reads/writes.
- Entity nature вычисляется из declaration kind, engineering unit и domain role; function/state/ticket incompatibilities являются явными.
- Dataflow содержит разрешённые declaration/API nodes и typed edges; unit engine распространяет размерности до fixed point.
- Symbol/Magic/Cycle evidence извлекается из source filters и разрешённой helper call chain, а scope relation использует явную матрицу.
- Полный computed graph остаётся воспроизводимым runtime artifact; JSON хранит компактные documented claims и не дублирует тысячи use sites.

### Последовательность атомарных commits

Подпункты 3.1.3.7.1—3.1.3.7.8 опубликованы отдельными commits. Самый большой тематический diff — strict-fixtures commit: 13 файлов, 467 additions, 50 deletions (`MEDIUM`); остальные commits имеют класс `SMALL`.

### Проверки и scope control

- Canonical terms: 230/230.
- Positive fixtures: 25/25; adversarial fixtures: 25/25; shadowing controls: PASS.
- Runtime `*.mq5` и `*.mqh` не изменялись; добавлены только синтетические `.mqh` внутри `Tests/stage_3_1_3/fixtures/`.
- Stage 3.1.4 не начинался; business policy, parameter profiles и trading logic не менялись.

### Remaining risks

MQL5 parsing остаётся консервативным static analysis, а не компиляторным AST. Неразрешённые constructs блокируют строгий status вместо оптимистического повышения mapping. Полный graph вычисляется validator при каждом запуске и не хранится повторно в документации.

## STAGE_3_1_3_EIGHTH_CORRECTION

### Baseline и pre-fix reproduction

- Последний независимо проверенный commit: `a761f135ae7810f192269802a8b64f9b290e8c07`.
- Фактический baseline после безопасного объединения опубликованной и локальной расходящихся историй: `750ca04c127c48b03f20a24b20422b21d73ca8cf`; reset, rebase, amend и force-push не применялись.
- `PRE_FIX_DEFECT_REPRODUCTION=PASS`: подтверждены прямые production/fixture-вызовы legacy discovery, искусственный fallback и константный positive control counter audit, неполное покрытие BLOCKING, name-based arithmetic resolution, future-declaration binding, неполные lexical blocks, отсутствие Python scoped graph и global-union Symbol/Magic proof.

### Единая production-архитектура

- `semantic_engine.evaluate_canonical_mapping` является единственной реализацией discovery, evidence, ranking, ambiguity и final status. `discovery.py` сохранён только как compatibility shim без самостоятельной semantic logic.
- Production validator, fixture controls и пересчёт 230 терминов вызывают тот же API; source guard блокирует прямое использование legacy authority.
- MQL5 resolver учитывает lexical block identity, declaration-before-use, shadowing и member owner; Python resolver строит declaration-scoped identities/use/dataflow из `ast`.
- Arithmetic operands связаны с `DeclarationIdentity`, unit fixed point не ищет глобальный identifier по написанию. Symbol/Magic scope вычисляется по конкретному candidate/caller path.

### Counter audit, fixtures и mapping

- Реестр строится программно из полного production `BLOCKING`: 105/105 rules зарегистрированы; missing, ineffective, non-clean и vacuous meta-counters равны нулю.
- Positive fixtures: 25/25; adversarial fixtures: 25/25; mutation controls: 48/48 negative, 20/20 positive, 15/15 adversarial.
- `CANONICAL_TERMS=230`, `TERMS_AUDITED=230`; schema `3.1.3-eighth-correction-1` содержит обязательные compact claims для каждого non-MISSING winner, без fallback обязательных claims к computed values.
- Полные generated candidate/use/dataflow graphs удалены из mapping JSON: они воспроизводятся engine во время проверки, а документ хранит только winner/runner-up/status и core semantic claims.

### Scope control и remaining risks

- Runtime `*.mq5`/`*.mqh`, trading logic, defaults, policy и parameter profiles не изменялись. Stage 3.1.4 не начинался.
- MQL5 frontend остаётся консервативным static parser, а не compiler AST; неизвестное evidence не повышается оптимистически и должно приводить к более слабому status либо blocking counter.
