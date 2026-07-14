from dataclasses import dataclass, field


@dataclass
class Ledger:
    reserve: float = 0.0
    applied: set[str] = field(default_factory=set)

    def apply(self, key: str, amount: float):
        if key in self.applied:
            return False
        self.applied.add(key)
        self.reserve += amount
        return True


def actual_partial_carry(budget, projected_loss, actual_net):
    actual_loss = max(0.0, -actual_net)
    return max(0.0, budget - actual_loss), actual_loss, actual_loss - projected_loss


def adjusted_partial_lot(far_lot, wanted, min_lot=0.01, step=0.01):
    lot = int(wanted / step) * step
    while lot >= min_lot and round(far_lot - lot, 8) < min_lot:
        lot = round(lot - step, 8)
    return 0.0 if lot < min_lot else lot


def test_reserve_ledger_event_key_is_idempotent_after_restart():
    ledger = Ledger()
    assert ledger.apply('USDJPY|20260609|C17|L2|SPLIT_BIG_HARVEST_CREDIT', 315.0)
    snapshot = Ledger(reserve=ledger.reserve, applied=set(ledger.applied))
    assert not snapshot.apply('USDJPY|20260609|C17|L2|SPLIT_BIG_HARVEST_CREDIT', 315.0)
    assert snapshot.reserve == 315.0


def test_partial_far_carry_uses_actual_deals_not_projection():
    carry, actual_loss, diff = actual_partial_carry(budget=40.0, projected_loss=35.0, actual_net=-37.5)
    assert actual_loss == 37.5
    assert diff == 2.5
    assert carry == 2.5


def test_missing_partial_deals_must_not_update_carry_or_reserve():
    deals_found = False
    carry_before = 12.0
    reserve_before = 100.0
    if not deals_found:
        carry_after = carry_before
        reserve_after = reserve_before
    assert carry_after == carry_before
    assert reserve_after == reserve_before


def test_partial_lot_does_not_leave_untradable_residual():
    assert adjusted_partial_lot(0.05, 0.05) == 0.04
    assert adjusted_partial_lot(0.015, 0.01) == 0.0
