"""Deterministic cases, stochastic model and explicit event faults."""
from itertools import product
from random import Random
from money import Quote
from meta import D, weights

CASES = {
    "up": (150,)*6, "down": (-150,)*6,
    "tight": (30, -30)*3, "wide": (350, -350)*3,
    "up_down": (150, 150, 150, -300, -300, -300),
    "down_up": (-150, -150, -150, 300, 300, 300),
    "reversals": (150, -300, 300, -300, 300, -150),
    "false_breaks": (180, -170, -190, 170, 210, -220),
    "trend_flat_reverse": (200, 200, 0, 0, -300, -300),
    "flat_trend_reverse": (0, 0, 300, 300, -300, -300),
    "alternating_150": (150, -150)*3, "alternating_300": (300, -300)*3,
    "random_walk": tuple(Random(4).choices(D, k=6)),
    "changing_vol": (30, -30, 110, -120, -500, 550),
    "gap": (300, 300, -4000, 1300, 200, 100),
    "spread": (300, 300, -300, -300, 0, 0),
    "delay": (300, 300, -300, -300, 0, 0),
    "partial": (300, 300, -300, -300, 0, 0),
    "reject": (300, 300, -300, -300, 0, 0),
    "adaptive": (0,)*6,
    "constant": (0,)*6,
    "persistent_failure": (300, 300, -4000, 0, 0, 0),
}


def quote(mid, name, step):
    if name == "spread" and step >= 2:
        return Quote(mid, spread=100, slip=4, swap_cost=.02)
    if name == "delay" and step in (1, 3, 6):
        return Quote(mid, delay=True)
    if name == "partial" and step in (0, 2, 4, 6):
        return Quote(mid, fill_cap=13)
    if name == "reject" and step in (2, 3, 6):
        return Quote(mid, reject=True)
    if name == "persistent_failure" and step >= 2:
        return Quote(mid, reject=True)
    return Quote(mid)


def exhaustive():
    for orientation in (-1, 1):
        for path in product(D, repeat=6):
            yield orientation, path, "exhaustive"


def sample(seed, size, horizon=8):
    rng = Random(seed)
    for _ in range(size):
        orientation = rng.choice((-1, 1))
        path = []
        previous = 0
        for _ in range(horizon):
            previous = rng.choices(D, weights(previous))[0]
            path.append(previous)
        yield orientation, tuple(path), "stochastic"


def stress():
    for orientation in (-1, 1):
        for name, path in CASES.items():
            for mirror in (-1, 1):
                yield orientation, tuple(mirror*d for d in path), name
