from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING


def down(value, step=Decimal('0.01')):
    return (Decimal(str(value)) / step).to_integral_value(rounding=ROUND_FLOOR) * step


def up(value, step=Decimal('0.01')):
    return (Decimal(str(value)) / step).to_integral_value(rounding=ROUND_CEILING) * step


def split_lots(far):
    far = Decimal(str(far))
    core = down(far * Decimal('1.60'))
    trend = down(far * Decimal('0.25'))
    small = up(far * Decimal('0.60'))
    gross = down(core + trend - small)
    reserve_growth = down(gross * Decimal('0.90'))
    return core, trend, small, gross, reserve_growth


def test_rounded_split_geometry_base_conditions():
    core, trend, small, gross, reserve_growth = split_lots('1.00')
    assert core == Decimal('1.60')
    assert trend == Decimal('0.25')
    assert small == Decimal('0.60')
    assert gross == Decimal('1.25')
    assert gross > Decimal('1.00')
    assert reserve_growth > Decimal('1.00')


def test_next_level_uses_actual_far_remainder():
    first = split_lots('1.00')
    second = split_lots('0.93')
    assert second[0] == Decimal('1.48')
    assert second[1] == Decimal('0.23')
    assert second[2] == Decimal('0.56')
    assert second[3] == Decimal('1.15')
    assert second[3] != first[3]
