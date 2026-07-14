from dataclasses import dataclass
from enum import Enum

VOLUME_TOL = 1e-9
LONG_MAX = 2**63 - 1
MASK64 = 2**64 - 1

class State(str, Enum):
    OPEN_BIG = 'STATE_OPEN_NEW_BIG_PENDING'
    OPEN_SMALL = 'STATE_OPEN_NEW_SMALL_PENDING'
    OPEN_CORE = 'STATE_SPLIT_OPEN_CORE_PENDING'
    OPEN_SMALL_BASE = 'STATE_SPLIT_OPEN_SMALL_BASE_PENDING'
    OPEN_TREND = 'STATE_SPLIT_OPEN_TREND_PENDING'
    CLOSE_CORE = 'STATE_SPLIT_CLOSE_CORE_PENDING'
    CLOSE_TREND = 'STATE_SPLIT_CLOSE_TREND_PENDING'
    CLOSE_SMALL_BASE = 'STATE_SPLIT_CLOSE_SMALL_BASE_PENDING'
    CLOSE_FAR_PARTIAL = 'STATE_SPLIT_CLOSE_FAR_PARTIAL_PENDING'
    CLOSE_FAR_FULL = 'STATE_SPLIT_CLOSE_FAR_FULL_PENDING'

OPEN_STATES = {State.OPEN_BIG, State.OPEN_SMALL, State.OPEN_CORE, State.OPEN_SMALL_BASE, State.OPEN_TREND}
CLOSE_STATES = {State.CLOSE_CORE, State.CLOSE_TREND, State.CLOSE_SMALL_BASE, State.CLOSE_FAR_PARTIAL, State.CLOSE_FAR_FULL}

@dataclass
class Pending:
    state: State
    action: str
    ticket: int = 0
    identifier: int = 0
    lot: float = 0.0
    direction: str = 'NONE'
    start_time: int = 0
    next_state: str = ''
    comment: str = ''
    attempts: int = 0

def validate_pending(p: Pending) -> bool:
    common = p.action != 'PENDING_NONE' and p.start_time > 0 and p.next_state and p.attempts >= 0
    if not common:
        return False
    if p.state in OPEN_STATES:
        return p.lot > VOLUME_TOL and p.direction != 'NONE' and bool(p.comment)
    if p.state in CLOSE_STATES:
        return (p.ticket != 0 or p.identifier != 0) and p.lot > VOLUME_TOL
    return False

def split_hash(h: int) -> tuple[int, int]:
    raw = h & MASK64
    return raw >> 32, raw & 0xFFFFFFFF

def restore_hash(high: int, low: int) -> int:
    raw = ((high & 0xFFFFFFFF) << 32) | (low & 0xFFFFFFFF)
    return raw - 2**64 if raw >= 2**63 else raw

@dataclass(frozen=True)
class LedgerEntry:
    event_id: int
    event_key: int
    amount: float
    before: float
    after: float
    symbol: str = 'EURUSD'
    magic: int = 8812825
    cycle_id: int = 17

class LedgerError(Exception):
    pass

class ReserveLedger:
    def __init__(self, entries=()):
        self.entries = list(entries)
        self.reserve = self.entries[-1].after if self.entries else 0.0
        self.validate()

    def validate(self):
        expected = 0.0
        ids, keys = set(), set()
        last_id = 0
        for e in self.entries:
            if e.event_id in ids or e.event_id <= last_id:
                raise LedgerError('duplicate_or_non_monotonic_event_id')
            if e.event_key in keys:
                raise LedgerError('duplicate_event_key')
            if e.symbol != 'EURUSD' or e.magic != 8812825 or e.cycle_id != 17:
                raise LedgerError('context_mismatch')
            if abs(e.before - expected) > 1e-9 or abs(e.after - (e.before + e.amount)) > 1e-9 or e.after < -1e-9:
                raise LedgerError('chain_broken')
            high, low = split_hash(e.event_key)
            assert restore_hash(high, low) == e.event_key
            ids.add(e.event_id); keys.add(e.event_key); last_id = e.event_id; expected = e.after
        self.reserve = expected

    def apply(self, event_key: int, amount: float) -> bool:
        if any(e.event_key == event_key for e in self.entries):
            return False
        before = self.reserve
        entry = LedgerEntry(len(self.entries) + 1, event_key, amount, before, before + amount)
        self.entries.append(entry)
        self.validate()
        return True

@dataclass
class Position:
    role: str
    ticket: int
    identifier: int
    lot: float
    comment: str

class RestartPendingModel:
    def __init__(self):
        self.orders_sent = 0
        self.positions: list[Position] = []

    def recover_open_pending(self, pending: Pending, role: str) -> str:
        for pos in self.positions:
            if pos.role == role and pos.comment == pending.comment and abs(pos.lot - pending.lot) <= VOLUME_TOL:
                return 'resolved_existing'
        self.orders_sent += 1
        return 'retry_sent'

def test_open_pending_without_ticket_is_valid_for_all_split_roles():
    for state, action, direction in [
        (State.OPEN_CORE, 'PENDING_OPEN_BIG_CORE', 'BUY'),
        (State.OPEN_SMALL_BASE, 'PENDING_OPEN_SMALL_BASE', 'SELL'),
        (State.OPEN_TREND, 'PENDING_OPEN_BIG_TREND', 'BUY'),
    ]:
        assert validate_pending(Pending(state, action, ticket=0, lot=1.6, direction=direction, start_time=100, next_state='NEXT', comment='ML|ROLE|C17|L1'))
        assert not validate_pending(Pending(state, action, ticket=0, lot=0.0, direction=direction, start_time=100, next_state='NEXT', comment='ML|ROLE|C17|L1'))
        assert not validate_pending(Pending(state, action, ticket=0, lot=1.6, direction='NONE', start_time=100, next_state='NEXT', comment='ML|ROLE|C17|L1'))

def test_close_pending_requires_ticket_or_identifier():
    assert not validate_pending(Pending(State.CLOSE_CORE, 'PENDING_CLOSE_BIG_CORE_FULL', lot=1.6, start_time=100, next_state='NEXT', comment='close'))
    assert validate_pending(Pending(State.CLOSE_CORE, 'PENDING_CLOSE_BIG_CORE_FULL', ticket=55, lot=1.6, start_time=100, next_state='NEXT', comment='close'))
    assert validate_pending(Pending(State.CLOSE_FAR_FULL, 'PENDING_CLOSE_FAR_FULL', identifier=9001, lot=1.0, start_time=100, next_state='NEXT', comment='close'))

def test_event_key_hash_round_trip_bit_exact_for_large_and_negative_values():
    values = [0, 1, 2**53 - 1, 2**53 + 1, LONG_MAX, -1, -2**63, 0x123456789ABCDEF - 2**63]
    for value in values:
        high, low = split_hash(value)
        assert restore_hash(high, low) == value

def test_reserve_ledger_chain_context_and_duplicate_checks():
    ok = [LedgerEntry(1, 101, 315.0, 0.0, 315.0), LedgerEntry(2, 202, -100.0, 315.0, 215.0)]
    assert ReserveLedger(ok).reserve == 215.0
    for broken in [
        [LedgerEntry(1, 101, 315.0, 1.0, 316.0)],
        [LedgerEntry(1, 101, 315.0, 0.0, 314.0)],
        [LedgerEntry(1, 101, 10.0, 0.0, 10.0), LedgerEntry(1, 102, 1.0, 10.0, 11.0)],
        [LedgerEntry(1, 101, 10.0, 0.0, 10.0), LedgerEntry(2, 101, 1.0, 10.0, 11.0)],
        [LedgerEntry(1, 101, 10.0, 0.0, 10.0, cycle_id=18)],
    ]:
        try:
            ReserveLedger(broken)
        except LedgerError:
            pass
        else:
            raise AssertionError('broken ledger was accepted')

def test_reserve_credit_and_debit_idempotency_after_serialized_restart():
    ledger = ReserveLedger()
    assert ledger.apply(1001, 315.0)
    before = ledger.reserve
    serialized = list(ledger.entries)
    restored = ReserveLedger(serialized)
    assert restored.reserve == before
    assert not restored.apply(1001, 315.0)
    assert restored.reserve == before
    assert restored.apply(2002, -120.0)
    after_debit = restored.reserve
    restored_again = ReserveLedger(list(restored.entries))
    assert not restored_again.apply(2002, -120.0)
    assert restored_again.reserve == after_debit

def test_restart_open_pending_resolves_existing_position_without_duplicate_order():
    model = RestartPendingModel()
    pending = Pending(State.OPEN_CORE, 'PENDING_OPEN_BIG_CORE', lot=1.6, direction='BUY', start_time=100, next_state='STATE_SPLIT_BIG_OPEN_SMALL_BASE', comment='ML|BC|C17|L1')
    assert model.recover_open_pending(pending, 'BC') == 'retry_sent'
    assert model.orders_sent == 1
    model = RestartPendingModel()
    model.positions.append(Position('BC', 777, 888, 1.6, 'ML|BC|C17|L1'))
    assert model.recover_open_pending(pending, 'BC') == 'resolved_existing'
    assert model.orders_sent == 0

def test_partial_history_restart_updates_carry_and_reserve_once():
    ledger = ReserveLedger()
    partial_budget = 35.0
    actual_loss = 31.25
    carry = max(0.0, partial_budget - actual_loss)
    assert carry == 3.75
    assert ledger.apply(3003, 315.0)
    restored = ReserveLedger(list(ledger.entries))
    assert not restored.apply(3003, 315.0)
    assert restored.reserve == 315.0
