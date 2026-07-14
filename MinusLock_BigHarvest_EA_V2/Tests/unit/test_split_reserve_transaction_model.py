from dataclasses import dataclass
from enum import Enum, auto

TWO_POW_53 = 9007199254740992

class Phase(Enum):
    NONE = auto()
    PREPARED = auto()
    LEDGER_WRITTEN = auto()
    CACHE_UPDATED = auto()
    COMPLETED = auto()

class FailPoint(Enum):
    NONE = auto()
    AFTER_PREPARED = auto()
    AFTER_LEDGER_WRITE = auto()
    AFTER_CACHE_UPDATE = auto()
    BEFORE_COMPLETED = auto()

@dataclass(frozen=True)
class Snapshot:
    event_key: int
    event_type: str
    cycle_id: int = 17
    far_id: int = 101
    core_id: int = 201
    trend_id: int = 202
    small_base_id: int = 203

@dataclass
class Transaction:
    active: bool
    transaction_id: int
    snapshot: Snapshot
    phase: Phase
    amount: float
    before: float
    after: float
    expected_event_id: int

class ReserveEngine:
    def __init__(self):
        self.reserve = 0.0
        self.ledger: list[tuple[int, int, float, float, float]] = []
        self.tx: Transaction | None = None
        self.next_event_id = 1
        self.next_tx_id = 1
        self.reconciliation_called = False
        self.trade_ops = 0

    def _ledger_has(self, key: int) -> bool:
        return any(row[1] == key for row in self.ledger)

    def _append_ledger_once(self, tx: Transaction):
        if not self._ledger_has(tx.snapshot.event_key):
            self.ledger.append((self.next_event_id, tx.snapshot.event_key, tx.amount, tx.before, tx.after))
            self.next_event_id += 1

    def apply(self, snapshot: Snapshot, amount: float, failpoint: FailPoint = FailPoint.NONE):
        if self.tx and self.tx.active and self.tx.snapshot.event_key != snapshot.event_key:
            return 'blocked_active_other_event'
        if self._ledger_has(snapshot.event_key):
            return 'duplicate_ignored'
        if not self.tx or not self.tx.active:
            self.tx = Transaction(True, self.next_tx_id, snapshot, Phase.PREPARED, amount, self.reserve, self.reserve + amount, self.next_event_id)
            self.next_tx_id += 1
            if failpoint is FailPoint.AFTER_PREPARED:
                return 'failed_after_prepared'
        return self.recover(failpoint)

    def recover(self, failpoint: FailPoint = FailPoint.NONE):
        tx = self.tx
        if tx is None or not tx.active:
            return 'nothing_to_recover'
        if tx.phase is Phase.PREPARED:
            self._append_ledger_once(tx)
            tx.phase = Phase.LEDGER_WRITTEN
            if failpoint is FailPoint.AFTER_LEDGER_WRITE:
                return 'failed_after_ledger_write'
        if tx.phase is Phase.LEDGER_WRITTEN:
            assert self._ledger_has(tx.snapshot.event_key)
            self.reserve = tx.after
            tx.phase = Phase.CACHE_UPDATED
            if failpoint is FailPoint.AFTER_CACHE_UPDATE:
                return 'failed_after_cache_update'
        if tx.phase is Phase.CACHE_UPDATED:
            assert self.reserve == tx.after
            tx.phase = Phase.COMPLETED
            if failpoint is FailPoint.BEFORE_COMPLETED:
                return 'failed_before_completed'
            tx.active = False
            return 'completed'
        if tx.phase is Phase.COMPLETED:
            tx.active = False
            return 'completed'
        raise AssertionError('unknown phase')

    def validate_event_ids(self):
        assert [row[0] for row in self.ledger] == list(range(1, len(self.ledger) + 1))
        assert self.next_event_id == len(self.ledger) + 1

def legacy_migration_allowed(stored_double: float) -> bool:
    return abs(stored_double) < TWO_POW_53

def validate_required_context(state: str, ctx: dict) -> bool:
    if state == 'STATE_FAR_ACTIVE':
        return bool(ctx.get('cycle_id') and (ctx.get('far_ticket') or ctx.get('far_id')) and ctx.get('far_lot') and ctx.get('far_direction'))
    if state == 'STATE_SPLIT_GEOMETRY_ACTIVE':
        return bool(ctx.get('cycle_id') and ctx.get('far_id') and ctx.get('core_id') and ctx.get('trend_id') and ctx.get('small_base_id') and ctx.get('level'))
    if state == 'STATE_SPLIT_BIG_HARVEST_PARTIAL_FAR':
        return bool(ctx.get('cycle_id') and ctx.get('far_id') and ctx.get('pending_time') and ctx.get('pending_lot') and ctx.get('pending_budget') is not None and ctx.get('pending_action'))
    return True

def recover_state(load_ok: bool, required_context_ok: bool, engine: ReserveEngine):
    if not load_ok:
        return {'state': 'STATE_RECOVERY_MISMATCH', 'reconciliation_called': False, 'trade_ops': 0}
    if not required_context_ok:
        return {'state': 'STATE_RECOVERY_MISMATCH', 'reconciliation_called': False, 'trade_ops': 0}
    engine.reconciliation_called = True
    return {'state': 'OK', 'reconciliation_called': True, 'trade_ops': engine.trade_ops}

def test_legacy_migration_boundary_blocks_ambiguous_2_pow_53_values():
    for value in [0.0, 1.0, float(TWO_POW_53 - 1)]:
        assert legacy_migration_allowed(value)
    for value in [float(TWO_POW_53), float(TWO_POW_53 + 1), float(-(TWO_POW_53)), float(2**63 - 1), float(-(2**63))]:
        assert not legacy_migration_allowed(value)
    assert int(float(TWO_POW_53 + 1)) == TWO_POW_53
    assert not legacy_migration_allowed(float(TWO_POW_53 + 1))

def test_recover_state_stops_before_reconciliation_and_trading_on_load_error():
    engine = ReserveEngine()
    result = recover_state(load_ok=False, required_context_ok=True, engine=engine)
    assert result == {'state': 'STATE_RECOVERY_MISMATCH', 'reconciliation_called': False, 'trade_ops': 0}

def test_required_context_is_state_specific():
    assert validate_required_context('STATE_FAR_ACTIVE', {'cycle_id': 1, 'far_id': 2, 'far_lot': 1.0, 'far_direction': 'BUY'})
    assert not validate_required_context('STATE_FAR_ACTIVE', {'cycle_id': 1, 'far_lot': 1.0, 'far_direction': 'BUY'})
    assert validate_required_context('STATE_SPLIT_GEOMETRY_ACTIVE', {'cycle_id': 1, 'far_id': 2, 'core_id': 3, 'trend_id': 4, 'small_base_id': 5, 'level': 1})
    assert not validate_required_context('STATE_SPLIT_GEOMETRY_ACTIVE', {'cycle_id': 1, 'far_id': 2, 'core_id': 3, 'small_base_id': 5, 'level': 1})

def test_credit_and_debit_without_failure_are_exactly_once_and_event_ids_contiguous():
    e = ReserveEngine()
    assert e.apply(Snapshot(1001, 'credit'), 315.0) == 'completed'
    assert e.apply(Snapshot(2002, 'debit'), -120.0) == 'completed'
    assert e.reserve == 195.0
    assert len(e.ledger) == 2
    e.validate_event_ids()

def test_restart_after_each_transaction_phase_recovers_once():
    for failpoint in [FailPoint.AFTER_PREPARED, FailPoint.AFTER_LEDGER_WRITE, FailPoint.AFTER_CACHE_UPDATE, FailPoint.BEFORE_COMPLETED]:
        e = ReserveEngine()
        result = e.apply(Snapshot(3003, 'credit'), 315.0, failpoint)
        assert result != 'completed'
        assert e.recover() == 'completed'
        assert e.reserve == 315.0
        assert len(e.ledger) == 1
        assert not e.tx.active
        e.validate_event_ids()

def test_duplicate_event_key_and_active_other_event_are_blocked():
    e = ReserveEngine()
    snap = Snapshot(4004, 'credit')
    assert e.apply(snap, 10.0, FailPoint.AFTER_PREPARED) == 'failed_after_prepared'
    assert e.apply(Snapshot(5005, 'credit'), 20.0) == 'blocked_active_other_event'
    assert e.recover() == 'completed'
    before = e.reserve
    assert e.apply(snap, 10.0) == 'duplicate_ignored'
    assert e.reserve == before
    assert len(e.ledger) == 1
