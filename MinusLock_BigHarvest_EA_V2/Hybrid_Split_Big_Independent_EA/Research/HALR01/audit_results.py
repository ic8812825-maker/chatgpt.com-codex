"""Replay selected test policies and check result invariants."""
from collections import Counter
from csv import DictReader
import json
from pathlib import Path

from money import Config
from preserve import Params
from scenarios import sample, stress
from simulate import run
from study import BUDGETS, TEST


def load(path):
    with Path(path).open() as f:
        return list(DictReader(f))


def verify():
    paths = list(sample(*TEST))
    stresses = list(stress())
    rows = load("BUDGET_FRONTIER.csv")
    assert [int(x["budget"]) for x in rows] == list(BUDGETS)
    for x in rows:
        budget = int(x["budget"])
        p = Params(**json.loads(x["params"]))
        config = Config(gross_limit=int(x["gross_limit"]))
        results = [run(x["variant"], s, p, budget, config) for s in paths]
        recoveries = sum(o.recovered_at is not None for o in results)
        assert recoveries == int(x["recoveries"])
        assert abs(min(o.pnl for o in results) - float(x["worst"])) < 1e-7
        assert sum(o.violations for o in results) == int(x["violations"])
        stress_violations = sum(run(x["variant"], s, p, budget, config).violations
                                for s in stresses)
        assert stress_violations == int(x["stress_violations"])
        assert float(x["exhaustive_intracycle_loss"]) <= budget

    comparisons = load("COMPARISON_RESULTS.csv")
    exact = [r for r in comparisons if r["split"] == "exhaustive_6"]
    assert len(exact) == 15
    assert all(int(r["n"]) == 31250 for r in exact)
    assert float(next(r for r in exact if r["variant"] == "K")["worst"]) == -58
    assert float(next(r for r in exact if r["variant"] == "M-minimax")["worst"]) == -58
    actions = {}
    for row in comparisons:
        if row["budget"] != "180" or row["split"] != "independent_test":
            continue
        if not row["variant"].startswith("M-"):
            continue
        p = Params(**json.loads(row["params"]))
        cfg = Config(gross_limit=int(row["gross_limit"]))
        counts = Counter()
        for s in paths:
            trace = []
            run(row["variant"], s, p, 180, cfg, trace=trace)
            counts.update(event[-1] for event in trace)
        actions[row["variant"]] = dict(sorted(counts.items()))
    checks = dict(meta_action_counts=actions, replayed_rows=len(rows), best_policy_test_paths=len(paths),
                  stress_paths=len(stresses), exhaustive_policy_rows=len(exact))
    Path("AUDIT_RESULTS.json").write_text(json.dumps(checks, indent=2) + "\n")
    return checks


if __name__ == "__main__":
    print(verify())
