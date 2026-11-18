"""Replay immutable HALR-01 result rows with its own simulator."""
import argparse
from concurrent.futures import ProcessPoolExecutor
import csv
import json
from pathlib import Path
import sys


def replay(row):
    from money import Config
    from preserve import Params
    from scenarios import exhaustive, sample, stress
    from simulate import run
    split = row["split"]
    paths = ({"independent_test": lambda: sample(202603,1200),
              "exhaustive_6": exhaustive, "adversarial_holdout": stress}[split])()
    p = Params(**json.loads(row["params"]))
    c = Config(gross_limit=int(row["gross_limit"]))
    a = [run(row["variant"], scenario, p, 180, c) for scenario in paths]
    actual = [len(a), sum(o.recovered_at is not None for o in a),
              sum(o.violations for o in a), min(o.pnl for o in a), sum(o.remaining>0 for o in a)]
    expect = [float(row[k]) for k in ("n","recoveries","violations","worst","residual")]
    if any(abs(x-y)>1e-7 for x,y in zip(actual,expect)):
        raise AssertionError((row["variant"], split, actual, expect))
    return dict(variant=row["variant"], split=split, trials=len(a), recoveries=actual[1],
                violations=actual[2], worst=actual[3], residual=actual[4])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source",type=Path)
    parser.add_argument("--quick",action="store_true")
    args = parser.parse_args()
    sys.path.insert(0,str(args.source.resolve()))
    with (args.source/"COMPARISON_RESULTS.csv").open() as f:
        rows = [r for r in csv.DictReader(f) if r["budget"]=="180"
                and (not args.quick or r["split"]!="exhaustive_6")]
    with ProcessPoolExecutor(2) as pool:
        print(json.dumps(list(pool.map(replay,rows)),indent=2))
