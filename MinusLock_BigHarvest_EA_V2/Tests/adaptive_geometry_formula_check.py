def round_to_step(value, step):
    return round(value / step) * step if step > 0 else round(value)

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
    mins = (100, 100, 50, 200)
    maxs = (250, 260, 125, 400)
    return tuple(clamp(int(round_to_step(atr * m, 5)), lo, hi) for m, lo, hi in zip(mult, mins, maxs))

assert calc(190, 'SAFE') == (190, 190, 75, 245)  # 247 rounds to 245 with MathRound-to-step semantics
assert calc(190, 'BALANCED') == (190, 220, 75, 285)
assert calc(190, 'PROFIT') == (200, 230, 85, 305)
print('ADAPTIVE_GEOMETRY_FORMULA_CHECK PASS')
