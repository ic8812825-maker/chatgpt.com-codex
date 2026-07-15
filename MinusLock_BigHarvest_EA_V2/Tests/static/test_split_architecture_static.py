from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE = (ROOT / 'Include' / 'StateMachine.mqh').read_text(encoding='utf-8')
INTEGRITY = (ROOT / 'Include' / 'StateIntegrityEngine.mqh').read_text(encoding='utf-8')
RECON = (ROOT / 'Include' / 'ReconciliationEngine.mqh').read_text(encoding='utf-8')
RESOLUTION = (ROOT / 'Include' / 'PositionResolutionEngine.mqh').read_text(encoding='utf-8')
PENDING = (ROOT / 'Include' / 'PendingContractEngine.mqh').read_text(encoding='utf-8')
TYPES = (ROOT / 'Include' / 'Types.mqh').read_text(encoding='utf-8')


def test_state_integrity_has_split_leg_validator_and_flags():
    assert 'ValidateSplitStateIntegrityLeg' in INTEGRITY
    for token in ['requireBigCore', 'requireBigTrend', 'requireSmallBase', 'forbidBigCore', 'forbidBigTrend', 'forbidSmallBase']:
        assert token in INTEGRITY
    assert 'legacy_big_small_present' in INTEGRITY


def test_position_resolution_has_all_split_roles_and_priority_sources():
    for token in ['ResolveBigCorePosition', 'ResolveBigTrendPosition', 'ResolveSmallBasePosition']:
        assert token in RESOLUTION
    for token in ['Saved ticket', 'POSITION_IDENTIFIER', 'Role comment + CycleId + Level', 'Direction + volume + open time']:
        assert token in RESOLUTION


def test_reconciliation_knows_split_topologies_and_not_orphan():
    for token in ['ValidateBigCorePosition', 'ValidateBigTrendPosition', 'ValidateSmallBasePosition', 'ReconcileSplitTopology', 'CurrentSplitTopology']:
        assert token in RECON
    assert 'ORPHAN_BIG_CORE' in RECON and 'ORPHAN_BIG_TREND' in RECON and 'ORPHAN_SMALL_BASE' in RECON


def test_pending_contracts_are_split_specific():
    for state in ['STATE_SPLIT_OPEN_CORE_PENDING', 'STATE_SPLIT_OPEN_SMALL_BASE_PENDING', 'STATE_SPLIT_OPEN_TREND_PENDING', 'STATE_SPLIT_CLOSE_CORE_PENDING', 'STATE_SPLIT_CLOSE_TREND_PENDING', 'STATE_SPLIT_CLOSE_SMALL_BASE_PENDING', 'STATE_SPLIT_CLOSE_FAR_PARTIAL_PENDING', 'STATE_SPLIT_CLOSE_FAR_FULL_PENDING']:
        assert state in TYPES
        assert state in PENDING
        assert state in STATE
    for action in ['PENDING_OPEN_BIG_CORE', 'PENDING_OPEN_SMALL_BASE', 'PENDING_OPEN_BIG_TREND', 'PENDING_CLOSE_BIG_CORE_FULL', 'PENDING_CLOSE_BIG_TREND_FULL', 'PENDING_CLOSE_SMALL_BASE_FULL']:
        assert action in PENDING


def test_partial_far_uses_actual_history_and_min_residual_guard():
    for token in ['CalculateActualPartialFarLossFromHistory', 'DEAL_FEE', 'DEAL_POSITION_ID) != Ctx.farIdentifier', 'STATE_SPLIT_PARTIAL_HISTORY_PENDING', 'AdjustPartialFarLotForMinimumResidual']:
        assert token in STATE
    assert 'pendingProjectedPartialFarLoss' in STATE
    assert 'actualPartialLoss' in STATE
    assert 'PartialBudgetAvailable' in STATE


def test_split_final_close_comment_and_guard_are_present():
    assert 'SPLIT_FINAL_CLOSE_PROFIT' in STATE
    assert 'IsProfitSystemCloseComment' in STATE
    assert 'CompleteSplitFullFarClose' in STATE
    assert 'RESERVE_EVENT_SPLIT_BIG_FINAL_DEBIT' in STATE
    assert 'SPLIT_CLOSED_PROFIT' in STATE


def test_reserve_ledger_persistence_is_checked_on_recover():
    assert 'SPLIT_RESERVE_LEDGER_SAVE' in STATE
    assert 'SPLIT_RESERVE_LEDGER_RESTORE' in STATE
    assert 'VerifyReserveLedgerPersistence' in STATE
    assert 'RESERVE_LEDGER_PERSISTENCE_MISMATCH' in STATE


def test_split_max_levels_is_isolated_from_legacy_state():
    assert 'STATE_SPLIT_MAX_LEVELS_DECISION' in TYPES
    assert 'STATE_SPLIT_MAX_LEVELS_DECISION' in STATE
    assert 'STATE_SPLIT_MAX_LEVELS_DECISION' in INTEGRITY


def test_stage3_event_key_hash_is_not_persisted_as_single_double():
    assert 'EventKeyHashHigh32' in STATE
    assert 'EventKeyHashLow32' in STATE
    assert 'GlobalVariableSet(StateKey(prefix + "EventKeyHash"), (double)ReserveLedger[ledgerIndex].eventKeyHash)' not in STATE
    assert 'RestoreReserveEventKeyHash' in STATE
    assert 'RESERVE_EVENT_KEY_RESTORE_FAILED' in STATE


def test_stage3_open_pending_classifier_does_not_require_ticket():
    assert 'IsOpenPendingState' in INTEGRITY
    open_block = INTEGRITY[INTEGRITY.index('if(IsOpenPendingState(state))'):INTEGRITY.index('else', INTEGRITY.index('if(IsOpenPendingState(state))'))]
    assert 'pendingTicket' not in open_block
    assert 'retryTicket' not in open_block
    assert 'pendingLot > VolumeMismatchToleranceLots' in open_block
    assert 'pendingDirection != DIR_NONE' in open_block


def test_stage4_uses_exact_64bit_helpers_and_symbol_hash_not_length_only():
    for token in ['SplitUlong64', 'RestoreUlong64', 'SplitLong64', 'RestoreLong64', 'StableSymbolHash64']:
        assert token in STATE
    assert 'SymbolHash"), (double)StringToInteger(IntegerToString(StringLen' not in STATE
    assert 'SaveStateUlong64("CycleId", Ctx.cycleId)' in STATE
    assert 'LoadOptionalStateUlong64("CycleId", Ctx.cycleId)' in STATE


def test_stage4_reserve_ledger_exact_fields_and_required_loaders():
    for token in [
        'SaveStateLong64(prefix + "EventId"',
        'SaveStateUlong64(prefix + "MagicNumber"',
        'SaveStateUlong64(prefix + "CycleId"',
        'SaveStateLong64(prefix + "BigCoreIdentifier"',
        'LoadRequiredStateLong64(prefix + "EventKeyHashHigh32"',
        'RESERVE_LEDGER_REQUIRED_FIELD_MISSING',
        'RESERVE_LEDGER_SYMBOL_MISMATCH',
        'RESERVE_EVENT_KEY_COMPONENT_MISMATCH',
    ]:
        assert token in STATE


def test_stage4_final_debit_uses_frozen_snapshot_before_context_clear():
    final_close = STATE[STATE.index('void CompleteSplitFullFarClose'):STATE.index('void ProcessSplitBigOpenCore')]
    assert 'BuildReserveEventContext(RESERVE_EVENT_SPLIT_BIG_FINAL_DEBIT, finalDebitSnapshot)' in final_close
    assert final_close.index('BuildReserveEventContext(RESERVE_EVENT_SPLIT_BIG_FINAL_DEBIT, finalDebitSnapshot)') < final_close.index('ApplyReserveDebitSnapshot(finalDebitSnapshot')
    assert final_close.index('ApplyReserveDebitSnapshot(finalDebitSnapshot') < final_close.index('ClearSplitRoleContext')


def test_stage5_recovery_and_transaction_guards_are_present():
    assert 'MathAbs(legacy) >= 9007199254740992.0' in STATE
    assert 'bool recoveryLoadOk = true' in STATE
    assert 'RECOVERY_REQUIRED_FIELD_LOAD_FAILED' in STATE
    assert 'ValidateRequiredRecoveredContextForState' in STATE
    for token in ['ReserveTransaction', 'RESERVE_TX_PREPARED', 'RESERVE_TX_LEDGER_WRITTEN', 'RESERVE_TX_CACHE_UPDATED', 'RESERVE_TX_COMPLETED']:
        assert token in TYPES or token in STATE
    for token in ['SaveReserveTransaction', 'RecoverPendingReserveTransaction', 'ExecuteReserveTransaction', 'StartReserveTransaction']:
        assert token in STATE
    assert 'RESERVE_LEDGER_EVENT_ID_GAP' in STATE


def test_stage6_recover_state_order_and_phase_aware_guards():
    recover = STATE[STATE.index('bool RecoverState()'):STATE.index('void ResetRecoveryContext()', STATE.index('bool RecoverState()'))]
    for token in [
        'RecoveryInProgress = true',
        'RECOVERY_CONTEXT_LOAD_COMPLETE',
        'RECOVERY_LEDGER_LOAD_COMPLETE',
        'RECOVERY_TRANSACTION_LOAD_COMPLETE',
        'ValidateReserveLedgerStructureOnly',
        'ValidateLedgerAndCacheForTransactionPhase',
        'RecoverPendingReserveTransaction',
        'VerifyReserveLedgerPersistence',
        'ValidateRequiredRecoveredContextForState',
        'RECOVERY_RECONCILIATION_BEGIN',
        'RecoveryInProgress = false',
    ]:
        assert token in recover
    assert recover.index('PendingActionType') < recover.index('LoadReserveTransaction')
    assert recover.index('LoadReserveTransaction') < recover.index('ValidateLedgerAndCacheForTransactionPhase')
    assert recover.index('ValidateLedgerAndCacheForTransactionPhase') < recover.index('RecoverPendingReserveTransaction')
    assert recover.index('RecoverPendingReserveTransaction') < recover.index('VerifyReserveLedgerPersistence')
    assert recover.index('VerifyReserveLedgerPersistence') < recover.index('ValidateRequiredRecoveredContextForState')
    assert recover.index('ValidateRequiredRecoveredContextForState') < recover.index('RECOVERY_RECONCILIATION_BEGIN')


def test_stage6_transaction_matching_completed_and_next_tx_persistence():
    for token in [
        'ValidateLedgerEntryAgainstTransaction',
        'entry.eventId == tx.expectedLedgerEventId',
        'entry.bigCoreIdentifier',
        'RESERVE_TX_COMPLETED',
        'COMPLETED_EVENT_NOT_FOUND',
        'COMPLETED_LEDGER_MISMATCH',
        'NextReserveTransactionId',
        'SaveStateLong64("NextReserveTransactionId"',
        'RESERVE_TRANSACTION_ID_SEQUENCE_ERROR',
    ]:
        assert token in STATE


def test_stage6_recovery_failure_marker_and_reset_safety():
    assert 'SaveRecoveryFailureMarker' in STATE
    assert 'RecoveryFailureActive' in STATE
    assert 'SaveState();\n      return false;' not in STATE[STATE.index('bool RecoverState()'):STATE.index('void ResetRecoveryContext()', STATE.index('bool RecoverState()'))]
    reset = STATE[STATE.index('void ApplyReserveReset'):STATE.index('double RebuildReserveFromLedger')]
    assert 'StartReserveTransaction(snapshot, delta)' in reset
    assert 'AppendReserveLedgerEntry(RESERVE_EVENT_RESET' not in reset


def test_stage6_split_close_context_states_are_validated():
    block = STATE[STATE.index('bool ValidateRequiredRecoveredContextForState'):STATE.index('bool RecoverState()')]
    for state in [
        'STATE_SPLIT_BIG_HARVEST_CLOSE_CORE',
        'STATE_SPLIT_CLOSE_CORE_PENDING',
        'STATE_SPLIT_BIG_HARVEST_CLOSE_TREND',
        'STATE_SPLIT_CLOSE_TREND_PENDING',
        'STATE_SPLIT_BIG_HARVEST_CLOSE_SMALL_BASE',
        'STATE_SPLIT_CLOSE_SMALL_BASE_PENDING',
        'STATE_SPLIT_BIG_HARVEST_CALC_NET',
        'STATE_SPLIT_BIG_HARVEST_CHECK_FULL_FAR',
        'STATE_SPLIT_MAX_LEVELS_DECISION',
    ]:
        assert state in block


def test_stage7_reserve_transaction_event_type_rules_and_reset_without_far():
    assert 'ValidateReserveTransactionContextByEventType' in STATE
    required = STATE[STATE.index('bool ValidateReserveTransactionRequiredFields'):STATE.index('bool LoadReserveTransaction')]
    assert 'ValidateReserveTransactionContextByEventType(ActiveReserveTransaction)' in required
    rules = STATE[STATE.index('string ReserveEventTypeRequirementsToString'):STATE.index('bool ValidateReserveTransactionRequiredFields')]
    assert 'RESERVE_EVENT_RESET' in rules
    assert 'EventType=RESERVE_EVENT_RESET RequiredFar=NO' in rules


def test_stage7_recovery_failure_marker_persists_original_state_and_reason_code():
    assert 'enum RecoveryFailureReason' in TYPES
    assert 'RecoveryFailureReasonCode' in STATE
    assert 'bool MarkRecoveryFailure(string reason, EAState originalState)' in STATE
    marker = STATE[STATE.index('void SaveRecoveryFailureMarker'):STATE.index('void ClearRecoveryFailureMarker')]
    assert 'RecoveryFailureOriginalState' in marker
    assert '(double)originalState' in marker
    assert 'SaveState();' not in marker


def test_stage7_recover_state_checks_reconciliation_and_integrity_before_pass():
    recover = STATE[STATE.index('bool RecoverState()'):STATE.index('void ResetRecoveryContext()', STATE.index('bool RecoverState()'))]
    assert 'return MarkRecoveryFailure("RECOVERY_RECONCILIATION_FAILED", recoveredState)' in recover
    assert 'bool integrityOk = ValidateCurrentStateIntegrity();' in recover
    assert 'return MarkRecoveryFailure("RECOVERY_STATE_INTEGRITY_FAILED", recoveredState)' in recover
    assert recover.index('bool integrityOk = ValidateCurrentStateIntegrity();') < recover.index('RECOVERY_COMPLETE')
    assert recover.index('ClearRecoveryFailureMarker();') < recover.index('RECOVERY_COMPLETE')


def test_stage7_recovery_operation_gate_is_used_by_key_paths():
    for token in [
        'TradingOperationAllowedDuringRecovery("RunStateMachine", false)',
        'TradingOperationAllowedDuringRecovery("OpenInitialLock", false)',
        'TradingOperationAllowedDuringRecovery("OpenBigSmall", false)',
        'TradingOperationAllowedDuringRecovery("OpenSplitRole", false)',
        'TradingOperationAllowedDuringRecovery("StartReserveTransaction", false)',
    ]:
        assert token in STATE
    trade = (ROOT / 'Include' / 'TradeEngine.mqh').read_text(encoding='utf-8')
    assert 'TradingOperationAllowedDuringRecovery("OpenPosition", false)' in trade


def test_stage7_actual_split_harvest_net_calculated_is_persisted_and_validated():
    assert 'actualSplitHarvestNetCalculated' in TYPES
    assert 'ActualSplitHarvestNetCalculated' in STATE
    state_validation = STATE[STATE.index('bool ValidateRequiredRecoveredContextForState'):STATE.index('bool RecoverState()')]
    assert 'Ctx.actualSplitHarvestNetCalculated' in state_validation
    assert 'Ctx.actualSplitHarvestNet != 0.0' not in state_validation
    assert 'Ctx.actualSplitHarvestNetCalculated = historyComplete' in STATE


def test_stage7_reserve_reset_guard_blocks_unsafe_start():
    reset = STATE[STATE.index('bool CanStartReserveReset'):STATE.index('void ApplyReserveReset')]
    for token in ['STATE_IDLE', 'STATE_STOP', 'STATE_CLOSED_PROFIT', 'STATE_CLOSED_RECOVERY_LOSS', 'CountManagedOpenPositions()', 'HasOpenLegContext()', 'ActiveReserveTransaction.active', 'RecoveryInProgress', 'RESERVE_RESET_BLOCKED']:
        assert token in reset
    apply_reset = STATE[STATE.index('void ApplyReserveReset'):STATE.index('double RebuildReserveFromLedger')]
    assert 'CanStartReserveReset()' in apply_reset
    assert 'StartReserveTransaction(snapshot, delta)' in apply_reset


def test_next_stage_oninit_recovery_failure_never_resets_unless_clean_start():
    main = (ROOT / 'MinusLock_BigHarvest_EA.mq5').read_text(encoding='utf-8')
    oninit = main[main.index('int OnInit()'):main.index('void OnDeinit')]
    assert 'IsProvenCleanStart()' in oninit
    assert 'RECOVERY_FAILURE_INIT_BLOCKED' in oninit
    failure_block = oninit[oninit.index('if(!RecoverState())'):oninit.index('else if(!ValidateNoOrphanManagedPositions())')]
    assert failure_block.index('IsProvenCleanStart()') < failure_block.index('ResetRecoveryContext()')
    assert 'return INIT_FAILED;' in failure_block
    state = STATE
    assert 'bool IsProvenCleanStart()' in state
    for token in ['CLEAN_START_CONFIRMED', 'RECOVERY_CONTEXT_RESET_FORBIDDEN', 'MANAGED_POSITIONS_PRESENT_DURING_RECOVERY_FAILURE']:
        assert token in state


def test_money_model_file_and_inputs_exist_and_ordercalc_is_primary():
    money = (ROOT / 'Include' / 'BrokerMoneyModel.mqh').read_text(encoding='utf-8')
    config = (ROOT / 'Include' / 'Config.mqh').read_text(encoding='utf-8')
    main = (ROOT / 'MinusLock_BigHarvest_EA.mq5').read_text(encoding='utf-8')
    for token in ['CalcProjectedPositionNetMoney', 'CalcProjectedCloseNetMoney', 'CalcProjectedOpenAndCloseCosts', 'CalcProjectedMarginMoney', 'CalcProjectedBasketNetMoney', 'CalcFarCloseLossWorstCaseMoney', 'CalcMoveRecoveryDeltaMoney']:
        assert token in money
    assert 'OrderCalcProfit' in money
    assert 'OrderCalcMargin' in money
    assert 'SYMBOL_TRADE_TICK_VALUE_PROFIT' in money or 'SYMBOL_TRADE_TICK_VALUE_LOSS' in money
    for token in ['EstimatedOpenCommissionPerLot', 'EstimatedCloseCommissionPerLot', 'EstimatedSwapBufferMoney', 'SpreadExpansionBufferPoints', 'SlippageSafetyMultiplier', 'ExecutionSafetyBufferMoney']:
        assert token in config
    assert '#include "Include/BrokerMoneyModel.mqh"' in main


def test_money_model_replaces_ordercalcprofit_fallback_in_projected_close():
    block = STATE[STATE.index('bool CalculateProjectedPositionCloseNet'):STATE.index('bool CalculateProjectedFarCloseNet')]
    assert 'CalcProjectedCloseNetMoney' in block
    assert 'BROKER_MONEY_MODEL_REQUIRED' in block
    assert 'else if(!OrderCalcProfit' not in block


def test_final_close_gate_exists_and_small_reserve_uses_it():
    assert 'struct FinalCloseEvaluation' in TYPES
    assert 'bool EvaluateFinalCloseGate' in STATE
    gate = STATE[STATE.index('bool EvaluateFinalCloseGate'):STATE.index('void ProcessSmallCheckReserve')]
    for token in ['farCloseLossWorstCase', 'totalCoverageAvailable', 'projectedRecoveryPL', 'coveragePass', 'recoveryPass', 'finalAllowed']:
        assert token in gate
    small = STATE[STATE.index('void ProcessSmallCheckReserve'):STATE.index('string DiagnoseStopMaxLevelsReason')]
    assert 'EvaluateFinalCloseGate(finalGate)' in small
    assert 'CalcFinalCloseAllowed' not in small


def test_isolated_split_test_sets_and_geometry_assert():
    safe = (ROOT / 'Sets' / 'SPLIT_TEST_SAFE.set').read_text(encoding='utf-8')
    balanced = (ROOT / 'Sets' / 'SPLIT_TEST_BALANCED.set').read_text(encoding='utf-8')
    for content in [safe, balanced]:
        assert 'UseSplitBigGeometry=true' in content
        assert 'UseLegacySingleBigGeometry=false' in content
        assert 'UseDynamicReverseSmall=true' in content
        assert 'AllowRealTrading=false' in content
    main = (ROOT / 'MinusLock_BigHarvest_EA.mq5').read_text(encoding='utf-8')
    assert 'ERROR_EXACTLY_ONE_GEOMETRY_MODE_REQUIRED' in main
