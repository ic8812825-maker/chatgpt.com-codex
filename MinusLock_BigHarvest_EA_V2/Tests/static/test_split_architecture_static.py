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
    assert 'LoadStateUlong64("CycleId", Ctx.cycleId)' in STATE


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
