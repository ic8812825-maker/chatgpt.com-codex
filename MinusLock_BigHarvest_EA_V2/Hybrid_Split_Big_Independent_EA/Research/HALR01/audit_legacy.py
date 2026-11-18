"""Cross-check the adapter against an immutable, separately supplied source."""
import argparse
import importlib.util
from itertools import accumulate
from pathlib import Path
import sys

from preserve import Params
from scenarios import sample
from simulate import run


def verify(path):
    spec = importlib.util.spec_from_file_location("umlrs_source", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    params = Params(net=12, trigger=140, horizon=12)
    legacy_params = module.Policy("J", 50, 12, 140, 1, 12, 180)
    max_error = 0.
    for scenario in sample(1903, 1000):
        orientation, moves, _ = scenario
        quotes = [module.Event(x) for x in accumulate(moves, initial=0)]
        reference = module.run(legacy_params, quotes, orientation)
        actual = run("J Balanced", scenario, params, 180)
        max_error = max(max_error, abs(reference["pnl"] - actual.pnl))
    if max_error > 1e-8:
        raise AssertionError(max_error)
    return dict(cases=1000, tolerance=1e-8, max_abs_error=max_error)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    print(verify(parser.parse_args().source))
