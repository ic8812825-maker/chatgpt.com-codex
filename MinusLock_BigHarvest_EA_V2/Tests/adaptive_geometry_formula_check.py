import math

def round_to_step(value, step):
    return int(math.floor(value / step + 0.5) * step) if step > 0 else int(math.floor(value + 0.5))

def clamp(value, lo, hi):
    return max(lo, min(hi, value))

def calc(atr, mode):
    if mode == 'SAFE':
        mult = (1.00, 1.00, 0.40, 1.30)
    elif mode == 'BALANCED':
        mult = (1.00, 1.15, 0.40, 1.50)
    elif mode == 'PROFIT':
        mult = (1.05, 1.20, 0.45, 1.60)
    else:
        raise AssertionError(mode)
    round_steps = (10, 10, 5, 50)
    mins = (100, 100, 50, 200)
    maxs = (250, 260, 125, 400)
    return tuple(clamp(round_to_step(atr * m, step), lo, hi) for m, step, lo, hi in zip(mult, round_steps, mins, maxs))

assert round_to_step(190, 10) == 190
assert round_to_step(218.5, 10) == 220
assert round_to_step(76, 5) == 75
assert round_to_step(247, 50) == 250
assert round_to_step(285, 50) == 300
assert round_to_step(304, 50) == 300
assert calc(190, 'SAFE') == (190, 190, 75, 250)
assert calc(190, 'BALANCED') == (190, 220, 75, 300)
assert calc(190, 'PROFIT') == (200, 230, 85, 300)
print('ADAPTIVE_GEOMETRY_FORMULA_CHECK PASS')
