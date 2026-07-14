from dataclasses import dataclass, field
from enum import Enum, auto

class Phase(Enum):
    PREPARED = auto()
    LEDGER_WRITTEN = auto()
    CACHE_UPDATED = auto()
    COMPLETED = auto()

@dataclass(frozen=True)
class Snapshot:
    event_key: int
    event_type: str = 'credit'
    far_id: int = 101
    core_id: int = 201
    trend_id: int = 202
    small_base_id: int = 203

@dataclass
class LedgerEntry:
    event_id: int
    event_key: int
    amount: float
    reserve_before: float
    reserve_after: float
    snapshot: Snapshot

@dataclass
class Transaction:
    active: bool
    transaction_id: int
    phase: Phase
    amount: float
    reserve_before: float
    reserve_after: float
    expected_event_id: int
    snapshot: Snapshot

@dataclass
class SerializedState:
    cache_reserve: float
    next_event_id: int
    next_tx_id: int
    ledger: list[LedgerEntry] = field(default_factory=list)
    tx: Transaction | None = None
    pending_loaded: bool = True
    pending_valid: bool = True
    load_ok: bool = True
    full_save_called: bool = False
    reconciliation_called: bool = False
    strict_validation_before_recovery: bool = False
    state: str = 'STATE_SPLIT_GEOMETRY_ACTIVE'

class RecoveryModel:
    def recover(self, s: SerializedState):
        order = []
        order.append('reset')
        order.append('load_context')
        order.append('load_pending_retry')
        order.append('load_ledger')
        order.append('load_transaction')
        if not s.load_ok:
            order.append('fail_fast')
            return 'STATE_RECOVERY_MISMATCH', order
        order.append('ledger_structure_only')
        order.append('phase_aware_validation')
        if not self._phase_aware_ok(s):
            return 'STATE_RECOVERY_MISMATCH', order
        order.append('recover_transaction')
        self._resume_transaction(s)
        order.append('strict_ledger_validation')
        assert not s.strict_validation_before_recovery
        order.append('state_context_validation')
        if not s.pending_valid:
            return 'STATE_RECOVERY_MISMATCH', order
        order.append('reconciliation')
        s.reconciliation_called = True
        return 'OK', order

    def _find(self, s: SerializedState, key: int):
        matches = [e for e in s.ledger if e.event_key == key]
        if len(matches) > 1:
            return 'duplicate'
        return matches[0] if matches else None

    def _entry_matches_tx(self, e: LedgerEntry, tx: Transaction):
        return (
            e.event_id == tx.expected_event_id
            and e.event_key == tx.snapshot.event_key
            and e.amount == tx.amount
            and e.reserve_before == tx.reserve_before
            and e.reserve_after == tx.reserve_after
            and e.snapshot == tx.snapshot
        )

    def _phase_aware_ok(self, s: SerializedState):
        tx = s.tx
        if tx is None or not tx.active:
            ledger_reserve = s.ledger[-1].reserve_after if s.ledger else 0.0
            return ledger_reserve == s.cache_reserve
        found = self._find(s, tx.snapshot.event_key)
        if found == 'duplicate':
            return False
        if tx.phase is Phase.PREPARED:
            return (found is None and s.cache_reserve == tx.reserve_before) or (found and self._entry_matches_tx(found, tx))
        if tx.phase is Phase.LEDGER_WRITTEN:
            return bool(found and self._entry_matches_tx(found, tx) and s.cache_reserve in (tx.reserve_before, tx.reserve_after))
        if tx.phase is Phase.CACHE_UPDATED:
            return bool(found and self._entry_matches_tx(found, tx) and s.cache_reserve == tx.reserve_after)
        if tx.phase is Phase.COMPLETED:
            return bool(found and self._entry_matches_tx(found, tx) and s.cache_reserve == tx.reserve_after)
        return False

    def _resume_transaction(self, s: SerializedState):
        tx = s.tx
        if tx is None or not tx.active:
            return
        found = self._find(s, tx.snapshot.event_key)
        if tx.phase is Phase.PREPARED:
            if found is None:
                s.ledger.append(LedgerEntry(tx.expected_event_id, tx.snapshot.event_key, tx.amount, tx.reserve_before, tx.reserve_after, tx.snapshot))
                s.next_event_id = tx.expected_event_id + 1
            tx.phase = Phase.LEDGER_WRITTEN
        if tx.phase is Phase.LEDGER_WRITTEN:
            s.cache_reserve = tx.reserve_after
            tx.phase = Phase.CACHE_UPDATED
        if tx.phase is Phase.CACHE_UPDATED:
            tx.phase = Phase.COMPLETED
        if tx.phase is Phase.COMPLETED:
            tx.active = False


def make_tx(phase: Phase, cache_before=True, ledger=False):
    snap = Snapshot(9001)
    tx = Transaction(True, 7, phase, 315.0, 100.0, 415.0, 3, snap)
    entries = [LedgerEntry(1, 111, 100.0, 0.0, 100.0, Snapshot(111))]
    if ledger:
        entries.append(LedgerEntry(3, snap.event_key, tx.amount, tx.reserve_before, tx.reserve_after, snap))
    cache = tx.reserve_before if cache_before else tx.reserve_after
    return SerializedState(cache_reserve=cache, next_event_id=3 if not ledger else 4, next_tx_id=8, ledger=entries, tx=tx)


def test_recovery_order_loads_pending_and_transaction_before_validation():
    s = make_tx(Phase.PREPARED, ledger=False)
    status, order = RecoveryModel().recover(s)
    assert status == 'OK'
    assert order.index('load_pending_retry') < order.index('load_transaction') < order.index('phase_aware_validation')
    assert order.index('recover_transaction') < order.index('strict_ledger_validation') < order.index('state_context_validation') < order.index('reconciliation')


def test_prepared_restart_without_ledger_writes_once_and_updates_cache():
    s = make_tx(Phase.PREPARED, ledger=False)
    status, _ = RecoveryModel().recover(s)
    assert status == 'OK'
    assert len([e for e in s.ledger if e.event_key == 9001]) == 1
    assert s.cache_reserve == 415.0
    assert s.tx and not s.tx.active


def test_prepared_crash_window_with_existing_ledger_does_not_duplicate():
    s = make_tx(Phase.PREPARED, ledger=True)
    status, _ = RecoveryModel().recover(s)
    assert status == 'OK'
    assert len([e for e in s.ledger if e.event_key == 9001]) == 1
    assert s.cache_reserve == 415.0


def test_ledger_written_accepts_cache_before_or_after():
    for cache_before in (True, False):
        s = make_tx(Phase.LEDGER_WRITTEN, cache_before=cache_before, ledger=True)
        status, _ = RecoveryModel().recover(s)
        assert status == 'OK'
        assert s.cache_reserve == 415.0
        assert s.tx and not s.tx.active


def test_cache_updated_and_completed_recover_without_mutating_ledger():
    for phase in (Phase.CACHE_UPDATED, Phase.COMPLETED):
        s = make_tx(phase, cache_before=False, ledger=True)
        before = list(s.ledger)
        status, _ = RecoveryModel().recover(s)
        assert status == 'OK'
        assert s.ledger == before
        assert s.tx and not s.tx.active


def test_corrupted_ledger_entry_causes_recovery_mismatch():
    s = make_tx(Phase.LEDGER_WRITTEN, ledger=True)
    s.ledger[-1].reserve_after = 999.0
    status, _ = RecoveryModel().recover(s)
    assert status == 'STATE_RECOVERY_MISMATCH'
    assert not s.reconciliation_called


def test_partial_pending_loaded_before_state_validation():
    s = make_tx(Phase.PREPARED, ledger=False)
    s.state = 'STATE_SPLIT_PARTIAL_HISTORY_PENDING'
    s.pending_valid = True
    status, order = RecoveryModel().recover(s)
    assert status == 'OK'
    assert order.index('load_pending_retry') < order.index('state_context_validation')


def test_load_failure_is_non_destructive_and_stops_before_reconciliation():
    s = make_tx(Phase.PREPARED, ledger=False)
    s.load_ok = False
    status, order = RecoveryModel().recover(s)
    assert status == 'STATE_RECOVERY_MISMATCH'
    assert 'reconciliation' not in order
    assert not s.full_save_called

class GateOperation(Enum):
    NEW_TRADE = auto()
    RECOVERY_CONTINUATION = auto()
    READ_ONLY = auto()


def event_context_valid(event_type: str, cycle_id=1, far=0, big=0, small=0, core=0, trend=0, small_base=0, harvest=0):
    if cycle_id == 0:
        return False
    if event_type == 'RESERVE_EVENT_RESET':
        return True
    if event_type == 'RESERVE_EVENT_SPLIT_BIG_HARVEST_ADD':
        return far != 0 and core != 0 and trend != 0 and small_base != 0 and harvest > 0
    if event_type == 'RESERVE_EVENT_SPLIT_BIG_FINAL_DEBIT':
        return far != 0 and core != 0 and trend != 0 and small_base != 0 and harvest > 0
    if event_type == 'RESERVE_EVENT_BIG_HARVEST_ADD':
        return far != 0 and big != 0 and small != 0 and harvest > 0
    return far != 0


def test_stage7_reset_event_context_does_not_require_far_identifier():
    assert event_context_valid('RESERVE_EVENT_RESET', cycle_id=1, far=0, core=0, trend=0, small_base=0)
    assert not event_context_valid('RESERVE_EVENT_SPLIT_BIG_HARVEST_ADD', cycle_id=1, far=0, core=2, trend=3, small_base=4, harvest=1)
    assert event_context_valid('RESERVE_EVENT_SPLIT_BIG_HARVEST_ADD', cycle_id=1, far=1, core=2, trend=3, small_base=4, harvest=1)


def make_reset_tx(phase: Phase, before: float, after: float, ledger=False):
    snap = Snapshot(event_key=4444, event_type='RESERVE_EVENT_RESET', far_id=0, core_id=0, trend_id=0, small_base_id=0)
    tx = Transaction(True, 11, phase, after - before, before, after, 1, snap)
    entries = []
    if ledger:
        entries.append(LedgerEntry(1, snap.event_key, tx.amount, tx.reserve_before, tx.reserve_after, snap))
    cache = before if phase in (Phase.PREPARED, Phase.LEDGER_WRITTEN) else after
    return SerializedState(cache_reserve=cache, next_event_id=1 if not ledger else 2, next_tx_id=12, ledger=entries, tx=tx, state='STATE_IDLE')


def test_stage7_reserve_reset_without_far_recovers_all_phases_and_deltas():
    for before, after in [(100.0, 0.0), (0.0, 100.0), (100.0, 50.0)]:
        for phase, has_ledger in [
            (Phase.PREPARED, False),
            (Phase.PREPARED, True),
            (Phase.LEDGER_WRITTEN, True),
            (Phase.CACHE_UPDATED, True),
            (Phase.COMPLETED, True),
        ]:
            s = make_reset_tx(phase, before, after, ledger=has_ledger)
            status, _ = RecoveryModel().recover(s)
            assert status == 'OK'
            assert s.cache_reserve == after
            assert len([e for e in s.ledger if e.event_key == 4444]) == 1
            assert s.tx and not s.tx.active


def can_start_reset(state='STATE_IDLE', managed=0, leg_context=False, active_tx=False, recovery=False):
    return state in {'STATE_IDLE', 'STATE_STOP', 'STATE_CLOSED_PROFIT', 'STATE_CLOSED_RECOVERY_LOSS'} and managed == 0 and not leg_context and not active_tx and not recovery


def test_stage7_reserve_reset_blocks_open_far_and_active_transaction():
    assert can_start_reset()
    assert not can_start_reset(leg_context=True)
    assert not can_start_reset(managed=1)
    assert not can_start_reset(active_tx=True)
    assert not can_start_reset(recovery=True)


def mark_failure(store: dict, reason_code: int, original_state: str):
    before = dict(store)
    store['RecoveryFailureActive'] = True
    store['RecoveryFailureReasonCode'] = reason_code
    store['RecoveryFailureOriginalState'] = original_state
    return before


def test_stage7_failure_marker_preserves_original_state_reason_and_context():
    store = {'State': 'STATE_SPLIT_PARTIAL_HISTORY_PENDING', 'CycleId': 42, 'FarIdentifier': 99, 'PendingTicket': 123, 'LedgerCount': 2, 'ActiveReserveTransaction': True}
    before = mark_failure(store, 8, store['State'])
    assert store['RecoveryFailureOriginalState'] == 'STATE_SPLIT_PARTIAL_HISTORY_PENDING'
    assert store['RecoveryFailureReasonCode'] == 8
    for key in ['State', 'CycleId', 'FarIdentifier', 'PendingTicket', 'LedgerCount', 'ActiveReserveTransaction']:
        assert store[key] == before[key]
    store['RecoveryFailureActive'] = False
    assert store['RecoveryFailureActive'] is False


def recover_terminal(integrity_ok=True, reconciliation_ok=True):
    logs = []
    if not reconciliation_ok:
        logs.append('RECOVERY_ABORTED')
        return False, logs, 'RECOVERY_FAILURE_RECONCILIATION'
    if not integrity_ok:
        logs.append('RECOVERY_ABORTED')
        return False, logs, 'RECOVERY_FAILURE_STATE_INTEGRITY'
    logs.append('RECOVERY_COMPLETE Result=PASS')
    return True, logs, 'RECOVERY_FAILURE_NONE'


def test_stage7_integrity_and_reconciliation_failures_do_not_return_success():
    ok, logs, reason = recover_terminal(integrity_ok=True, reconciliation_ok=True)
    assert ok and logs == ['RECOVERY_COMPLETE Result=PASS'] and reason == 'RECOVERY_FAILURE_NONE'
    ok, logs, reason = recover_terminal(integrity_ok=False, reconciliation_ok=True)
    assert not ok and 'RECOVERY_COMPLETE Result=PASS' not in logs and reason == 'RECOVERY_FAILURE_STATE_INTEGRITY'
    ok, logs, reason = recover_terminal(integrity_ok=True, reconciliation_ok=False)
    assert not ok and 'RECOVERY_COMPLETE Result=PASS' not in logs and reason == 'RECOVERY_FAILURE_RECONCILIATION'


def operation_allowed(recovery: bool, op: GateOperation):
    if not recovery:
        return True
    return op in (GateOperation.RECOVERY_CONTINUATION, GateOperation.READ_ONLY)


def test_stage7_recovery_in_progress_gate_blocks_new_operations_only():
    assert not operation_allowed(True, GateOperation.NEW_TRADE)
    assert operation_allowed(True, GateOperation.RECOVERY_CONTINUATION)
    assert operation_allowed(True, GateOperation.READ_ONLY)
    assert operation_allowed(False, GateOperation.NEW_TRADE)


def split_harvest_net_context_valid(net: float, calculated: bool):
    return calculated


def test_stage7_zero_split_harvest_net_uses_calculated_flag():
    assert split_harvest_net_context_valid(0.0, True)
    assert not split_harvest_net_context_valid(0.0, False)
