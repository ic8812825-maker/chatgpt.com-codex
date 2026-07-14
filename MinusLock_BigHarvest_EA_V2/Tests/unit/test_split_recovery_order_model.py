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
