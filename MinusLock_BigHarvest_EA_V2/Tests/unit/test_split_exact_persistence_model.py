from dataclasses import dataclass, replace

MASK32 = 0xFFFFFFFF
MASK64 = 0xFFFFFFFFFFFFFFFF
LONG_MAX = 2**63 - 1
LONG_MIN = -2**63


def split_ulong64(value: int) -> tuple[int, int]:
    assert 0 <= value <= MASK64
    return (value >> 32) & MASK32, value & MASK32


def restore_ulong64(high: int, low: int) -> int:
    return ((high & MASK32) << 32) | (low & MASK32)


def split_long64(value: int) -> tuple[int, int]:
    assert LONG_MIN <= value <= LONG_MAX
    return split_ulong64(value & MASK64)


def restore_long64(high: int, low: int) -> int:
    raw = restore_ulong64(high, low)
    return raw - 2**64 if raw >= 2**63 else raw


def stable_symbol_hash64(symbol: str) -> int:
    h = 1469598103934665603
    for ch in symbol:
        h = ((h ^ ord(ch)) * 1099511628211) & MASK64
    return h - 2**64 if h >= 2**63 else h


@dataclass(frozen=True)
class Snapshot:
    symbol: str
    magic: int
    cycle_id: int
    level: int
    reverse_cycle: int
    far_id: int
    big_id: int
    small_id: int
    core_id: int
    trend_id: int
    small_base_id: int
    reverse_small_id: int
    event_type: int

    @property
    def symbol_hash(self) -> int:
        return stable_symbol_hash64(self.symbol)


def event_key(snapshot: Snapshot) -> int:
    payload = '|'.join(map(str, [
        snapshot.symbol_hash, len(snapshot.symbol), snapshot.magic, snapshot.cycle_id,
        snapshot.level, snapshot.reverse_cycle, snapshot.big_id, snapshot.small_id,
        snapshot.core_id, snapshot.trend_id, snapshot.small_base_id,
        snapshot.reverse_small_id, snapshot.far_id, snapshot.event_type,
    ]))
    return stable_symbol_hash64(payload)


def serialize_snapshot(snapshot: Snapshot) -> dict[str, int | float]:
    data: dict[str, int | float] = {}
    fields = {
        'MagicNumber': snapshot.magic,
        'CycleId': snapshot.cycle_id,
        'FarIdentifier': snapshot.far_id,
        'BigIdentifier': snapshot.big_id,
        'SmallIdentifier': snapshot.small_id,
        'BigCoreIdentifier': snapshot.core_id,
        'BigTrendIdentifier': snapshot.trend_id,
        'SmallBaseIdentifier': snapshot.small_base_id,
        'ReverseSmallIdentifier': snapshot.reverse_small_id,
    }
    for name, value in fields.items():
        hi, lo = split_ulong64(value)
        data[f'{name}High32'] = hi
        data[f'{name}Low32'] = lo
    hi, lo = split_long64(snapshot.symbol_hash)
    data['SymbolHashHigh32'] = hi
    data['SymbolHashLow32'] = lo
    data['SymbolLength'] = len(snapshot.symbol)
    hi, lo = split_long64(event_key(snapshot))
    data['EventKeyHashHigh32'] = hi
    data['EventKeyHashLow32'] = lo
    data['Level'] = snapshot.level
    data['ReverseCycle'] = snapshot.reverse_cycle
    data['EventType'] = snapshot.event_type
    return data


def deserialize_snapshot(data: dict[str, int | float], runtime_symbol: str) -> Snapshot:
    required = [
        'MagicNumberHigh32', 'MagicNumberLow32', 'CycleIdHigh32', 'CycleIdLow32',
        'FarIdentifierHigh32', 'FarIdentifierLow32', 'BigCoreIdentifierHigh32',
        'BigCoreIdentifierLow32', 'BigTrendIdentifierHigh32', 'BigTrendIdentifierLow32',
        'SmallBaseIdentifierHigh32', 'SmallBaseIdentifierLow32', 'SymbolHashHigh32',
        'SymbolHashLow32', 'EventKeyHashHigh32', 'EventKeyHashLow32',
    ]
    missing = [key for key in required if key not in data]
    if missing:
        raise KeyError('RESERVE_LEDGER_REQUIRED_FIELD_MISSING:' + ','.join(missing))
    stored_symbol_hash = restore_long64(int(data['SymbolHashHigh32']), int(data['SymbolHashLow32']))
    if stored_symbol_hash != stable_symbol_hash64(runtime_symbol) or int(data['SymbolLength']) != len(runtime_symbol):
        raise ValueError('RESERVE_LEDGER_SYMBOL_MISMATCH')
    snap = Snapshot(
        symbol=runtime_symbol,
        magic=restore_ulong64(int(data['MagicNumberHigh32']), int(data['MagicNumberLow32'])),
        cycle_id=restore_ulong64(int(data['CycleIdHigh32']), int(data['CycleIdLow32'])),
        level=int(data['Level']),
        reverse_cycle=int(data['ReverseCycle']),
        far_id=restore_ulong64(int(data['FarIdentifierHigh32']), int(data['FarIdentifierLow32'])),
        big_id=restore_ulong64(int(data.get('BigIdentifierHigh32', 0)), int(data.get('BigIdentifierLow32', 0))),
        small_id=restore_ulong64(int(data.get('SmallIdentifierHigh32', 0)), int(data.get('SmallIdentifierLow32', 0))),
        core_id=restore_ulong64(int(data['BigCoreIdentifierHigh32']), int(data['BigCoreIdentifierLow32'])),
        trend_id=restore_ulong64(int(data['BigTrendIdentifierHigh32']), int(data['BigTrendIdentifierLow32'])),
        small_base_id=restore_ulong64(int(data['SmallBaseIdentifierHigh32']), int(data['SmallBaseIdentifierLow32'])),
        reverse_small_id=restore_ulong64(int(data.get('ReverseSmallIdentifierHigh32', 0)), int(data.get('ReverseSmallIdentifierLow32', 0))),
        event_type=int(data['EventType']),
    )
    stored_event_key = restore_long64(int(data['EventKeyHashHigh32']), int(data['EventKeyHashLow32']))
    if stored_event_key != event_key(snap):
        raise ValueError('RESERVE_EVENT_KEY_COMPONENT_MISMATCH')
    return snap


class Ledger:
    def __init__(self):
        self.entries: dict[int, float] = {}
        self.reserve = 0.0

    def apply(self, snap: Snapshot, amount: float) -> bool:
        key = event_key(snap)
        if key in self.entries:
            return False
        self.entries[key] = amount
        self.reserve += amount
        return True


def test_ulong64_round_trip_full_range():
    for value in [0, 1, 2**32 - 1, 2**32, 2**53 - 1, 2**53, 2**53 + 1, 2**63 - 1, 2**64 - 1]:
        assert restore_ulong64(*split_ulong64(value)) == value


def test_long64_round_trip_full_range():
    for value in [LONG_MIN, -(2**53) - 1, -1, 0, 1, 2**53 + 1, LONG_MAX]:
        assert restore_long64(*split_long64(value)) == value


def test_legacy_double_format_loses_identifier_above_2_pow_53():
    value = 2**53 + 1
    assert int(float(value)) != value


def test_full_event_key_serialization_with_large_identifiers_bit_exact():
    large = 2**53 + 12345
    snap = Snapshot('EURUSD', 2**53 + 7, 2**53 + 9, 3, 1, large, large + 1, large + 2, large + 3, large + 4, large + 5, large + 6, 2)
    data = serialize_snapshot(snap)
    restored = deserialize_snapshot(dict(data), 'EURUSD')
    assert restored == snap
    assert event_key(restored) == event_key(snap)


def test_symbols_with_same_length_have_distinct_hashes():
    symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD']
    hashes = {stable_symbol_hash64(symbol) for symbol in symbols}
    assert len(hashes) == len(symbols)


def test_symbol_mismatch_rejects_ledger_restore():
    snap = Snapshot('EURUSD', 8812825, 17, 1, 0, 2**53 + 1, 0, 0, 2**53 + 2, 2**53 + 3, 2**53 + 4, 0, 2)
    data = serialize_snapshot(snap)
    try:
        deserialize_snapshot(data, 'GBPUSD')
    except ValueError as exc:
        assert str(exc) == 'RESERVE_LEDGER_SYMBOL_MISMATCH'
    else:
        raise AssertionError('symbol mismatch accepted')


def test_missing_required_identifier_low32_rejects_restore():
    snap = Snapshot('EURUSD', 8812825, 17, 1, 0, 2**53 + 1, 0, 0, 2**53 + 2, 2**53 + 3, 2**53 + 4, 0, 2)
    data = serialize_snapshot(snap)
    del data['BigCoreIdentifierLow32']
    try:
        deserialize_snapshot(data, 'EURUSD')
    except KeyError as exc:
        assert 'RESERVE_LEDGER_REQUIRED_FIELD_MISSING' in str(exc)
    else:
        raise AssertionError('missing required field accepted')


def test_duplicate_credit_and_debit_after_restart_are_idempotent_with_large_ids():
    base = Snapshot('EURUSD', 8812825, 2**53 + 10, 2, 0, 2**53 + 11, 0, 0, 2**53 + 12, 2**53 + 13, 2**53 + 14, 0, 2)
    ledger = Ledger()
    assert ledger.apply(base, 315.0)
    restored = Ledger(); restored.entries = dict(ledger.entries); restored.reserve = ledger.reserve
    assert not restored.apply(base, 315.0)
    debit = replace(base, event_type=3)
    assert restored.apply(debit, -120.0)
    reserve_after_debit = restored.reserve
    restored_again = Ledger(); restored_again.entries = dict(restored.entries); restored_again.reserve = restored.reserve
    assert not restored_again.apply(debit, -120.0)
    assert restored_again.reserve == reserve_after_debit


def test_context_mutation_after_snapshot_does_not_change_event_key():
    snap = Snapshot('EURUSD', 8812825, 2**53 + 20, 3, 0, 2**53 + 21, 0, 0, 2**53 + 22, 2**53 + 23, 2**53 + 24, 0, 3)
    frozen_key = event_key(snap)
    mutated_context = Snapshot('EURUSD', 8812825, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3)
    assert event_key(mutated_context) != frozen_key
    assert event_key(snap) == frozen_key


def test_recovery_context_exact_restore_for_large_ticket_and_identifier_values():
    fields = {
        'FarTicket': 2**53 + 101,
        'FarIdentifier': 2**53 + 102,
        'BigCoreTicket': 2**53 + 103,
        'BigCoreIdentifier': 2**53 + 104,
        'BigTrendIdentifier': 2**53 + 105,
        'SmallBaseIdentifier': 2**53 + 106,
        'CycleId': 2**53 + 107,
        'PendingTicket': 2**53 + 108,
        'RetryTicket': 2**53 + 109,
    }
    serialized = {}
    for name, value in fields.items():
        hi, lo = split_ulong64(value)
        serialized[name + 'High32'] = hi
        serialized[name + 'Low32'] = lo
    restored = {name: restore_ulong64(serialized[name + 'High32'], serialized[name + 'Low32']) for name in fields}
    assert restored == fields
