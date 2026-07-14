
def simulate_three_levels(start_far=1.0, point_value=1.0):
    far = start_far
    reserve = 0.0
    carry = 0.0
    rows = []
    for level, distance in enumerate([280, 300, 320], 1):
        core = int(far * 1.60 * 100) / 100
        trend = int(far * 0.25 * 100) / 100
        small = -(-int(far * 0.60 * 1000) // 10) / 100
        harvest = (core + trend - small) * distance * point_value
        full_loss = far * (170 + distance) * point_value
        if reserve + harvest >= full_loss + 2.0:
            rows.append((level, far, core, trend, small, harvest, reserve, 'FULL'))
            far = 0.0
            break
        reserve_add = harvest * 0.90
        partial_budget = harvest - reserve_add + carry
        close_lot = int((partial_budget / (170 + distance)) * 100) / 100
        actual_loss = close_lot * (170 + distance)
        carry = max(0.0, partial_budget - actual_loss)
        far = round(far - close_lot, 2)
        reserve += reserve_add
        rows.append((level, far, core, trend, small, harvest, reserve, 'PARTIAL'))
    return rows


def test_numeric_split_big_base_scenario_reaches_full_close():
    rows = simulate_three_levels()
    assert rows[0][1] <= 0.94
    assert rows[0][6] >= 300
    assert rows[-1][-1] == 'FULL'


def test_reserve_is_not_used_for_partial_budget():
    rows = simulate_three_levels()
    # L1 harvest is split 90/10; the Far only decreases by the 10% budget plus carry, not by reserve.
    assert rows[0][1] > 0.90
    assert rows[0][6] > 300
