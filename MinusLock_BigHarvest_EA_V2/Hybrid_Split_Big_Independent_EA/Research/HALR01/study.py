"""Reproduce HALR-01 figures from deterministic experiments."""
import csv
from dataclasses import asdict, dataclass, replace
import json
import math
from pathlib import Path
from random import Random
from statistics import mean, median
import sys
import unittest

from money import Config
from preserve import Params
from scenarios import exhaustive, sample, stress
from simulate import run

BUDGETS = (58, 100, 150, 180, 250, 300, 500)
FAMILIES = ("A1", "A2", "A3", "A1-strict", "A2-strict", "A3-strict",
            "B1", "B2", "B3", "B4", "M-minimax", "M-probability", "M-adjusted")
TRAIN = (202601, 80)
VALIDATE = (202602, 160)
TEST = (202603, 1200)


@dataclass(frozen=True)
class Candidate:
    variant: str
    params: Params = Params(horizon=8)
    config: Config = Config()


def evaluate(candidate, paths, budget):
    return [run(candidate.variant, s, candidate.params, budget, candidate.config) for s in paths]


def tail_mean(losses, probability):
    mass = len(losses) * (1-probability)
    count = int(mass)
    descending = sorted(losses, reverse=True)
    return (sum(descending[:count]) + (mass-count)*descending[count]) / mass


def summary(outcomes, ci=False):
    pnl = [o.pnl for o in outcomes]
    losses = sorted(-x for x in pnl)
    n = len(outcomes)
    times = [o.recovered_at for o in outcomes if o.recovered_at is not None]
    rate = len(times)/n
    low, high = "", ""
    if ci:
        z = 1.95996398454
        center = (rate + z*z/(2*n))/(1+z*z/n)
        half = z*math.sqrt((rate*(1-rate)+z*z/(4*n))/n)/(1+z*z/n)
        low, high = max(0, center-half), min(1, center+half)
    return dict(n=n, recoveries=len(times), rate=rate, wilson_low=low, wilson_high=high,
                mean=mean(pnl), median=median(pnl), worst=min(pnl),
                worst_loss=max(0, -min(pnl)), worst_intracycle_loss=-min(o.low for o in outcomes),
                additional_loss_vs_baseline=max(0, -min(pnl)-58),
                max_drawdown=max(o.drawdown for o in outcomes),
                cvar95=tail_mean(losses,.95), cvar99=tail_mean(losses,.99),
                p95_loss=losses[math.ceil(.95*n)-1], p99_loss=losses[math.ceil(.99*n)-1],
                average_recovery_time=mean(times) if times else "",
                turnover=sum(o.turnover for o in outcomes), costs=sum(o.costs for o in outcomes),
                spread=sum(o.spread for o in outcomes), commission=sum(o.commission for o in outcomes),
                slippage=sum(o.slippage for o in outcomes), swap=sum(o.swap for o in outcomes),
                margin_stress=max(o.margin_stress for o in outcomes),
                stopouts=sum(o.stopout for o in outcomes), violations=sum(o.violations for o in outcomes),
                failures=sum(o.failures for o in outcomes), residual=sum(o.remaining>0 for o in outcomes))


def write_csv(name, rows):
    with Path(name+".csv").open("w", newline="") as file:
        out = csv.DictWriter(file, fieldnames=list(rows[0]))
        out.writeheader()
        for row in rows:
            out.writerow({k: round(v, 8) if isinstance(v, float) else v for k,v in row.items()})


def candidates(variant):
    rng = Random(99)
    yield Candidate(variant)
    # All hundred core values considered for A2; other axes use a fixed broad design.
    cores = range(1, 101) if variant.startswith("A2") else range(24)
    for value in cores:
        core = value if variant.startswith("A2") else rng.choice((1, 10, 25, 50, 75, 100))
        p = Params(net=rng.choice((10, 12, 20, 25, 30, 40, 50)), core=core,
                   trigger=rng.choice((75, 140, 200, 300)), switches=rng.choice((1, 2, 4, 6)),
                   harvest=rng.choice((.25, .5, .75)), attempts=rng.choice((1, 2, 3)),
                   horizon=rng.choice((4, 6, 8)), reserve=rng.choice((0., 5., 15.)))
        yield Candidate(variant, p, Config(gross_limit=rng.choice((300, 400, 500))))


def info(c):
    return dict(variant=c.variant, params=json.dumps(asdict(c.params), sort_keys=True),
                gross_limit=c.config.gross_limit, commission_per_side=c.config.commission)


def rank(result):
    return (result["violations"] == 0, result["rate"], -result["cvar95"], result["mean"])


def paired(a, b):
    wins = sum(x.recovered_at is not None and y.recovered_at is None for x,y in zip(a,b))
    losses = sum(y.recovered_at is not None and x.recovered_at is None for x,y in zip(a,b))
    return wins, losses, mean(x.pnl-y.pnl for x,y in zip(a,b))


def main():
    train, valid, test = (list(sample(*spec)) for spec in (TRAIN, VALIDATE, TEST))
    xpaths, spaths = list(exhaustive()), list(stress())
    opt, comparisons, matrix, budget_rows, pairs = [], [], [], [], []
    all_eval = {}
    selected_at = {}
    for budget in BUDGETS:
        chosen = [(Candidate("K"), summary(evaluate(Candidate("K"), valid, budget)))]
        for v in FAMILIES:
            scored = [(rank(s), c) for c in candidates(v)
                      for s in [summary(evaluate(c, train, budget))]]
            scored.sort(key=lambda row: row[0], reverse=True)
            shortlist = []
            for train_score, c in scored[:4]:
                valid_score = summary(evaluate(c, valid, budget))
                opt.append(dict(budget=budget, **info(c), training_rate=train_score[1],
                                training_feasible=train_score[0], **valid_score))
                shortlist.append((c, valid_score))
            chosen.append(max(shortlist, key=lambda row: rank(row[1])))
        selected_at[budget] = chosen
        print("optimized", budget, flush=True)

    for budget, chosen in selected_at.items():
        k = evaluate(Candidate("K"), test, budget)
        for c, valid_score in chosen:
            result = evaluate(c, test, budget)
            sp = evaluate(c, spaths, budget)
            all_eval[budget,c] = (result, sp)
            r = dict(budget=budget, **info(c), split="independent_test", **summary(result, True))
            comparisons.extend([r, dict(budget=budget, **info(c), split="adversarial_holdout", **summary(sp))])
            wins, losses, delta = paired(result, k)
            pairs.append(dict(budget=budget, variant=c.variant, baseline="K", n=len(k),
                              recoveries_only_candidate=wins, recoveries_only_baseline=losses,
                              mean_pnl_difference=delta))
            if budget == 180:
                fixed = evaluate(c, xpaths, budget)
                comparisons.append(dict(budget=budget, **info(c), split="exhaustive_6", **summary(fixed)))
                for scenario, outcome in zip(spaths,sp):
                    orientation, path, name = scenario
                    matrix.append(dict(variant=c.variant, orientation=orientation,
                                       scenario=name, moves=str(path), **asdict(outcome)))
        # Screen candidates in validation order against the exact fixed-execution
        # six-step tree. This tree is part of the feasibility constraints.
        ordered = sorted(chosen, key=lambda row: rank(row[1]), reverse=True)
        for c, s in ordered:
            if s["violations"]:
                continue
            fixed = evaluate(c, xpaths, budget)
            if not any(o.violations for o in fixed):
                break
        result, sp = all_eval[budget,c]
        budget_rows.append(dict(budget=budget, additional_budget=budget-58,
                                **info(c), **summary(result,True),
                                exhaustive_intracycle_loss=-min(o.low for o in fixed),
                                stress_violations=sum(o.violations for o in sp),
                                stress_status=("RISK_BOUND_NOT_PROVEN" if c.variant!="K"
                                               else "CONDITIONAL_K_IMMEDIATE_EXECUTION")))
        print("evaluated", budget, c.variant, flush=True)

    entries = selected_at[180]
    for c, _ in entries:
        if not c.variant.startswith("M"):
            continue
        a, _ = all_eval[180,c]
        for b, _ in entries:
            if b.variant.startswith(("A","B")):
                base, _ = all_eval[180,b]
                wins, losses, delta = paired(a, base)
                pairs.append(dict(budget=180, variant=c.variant, baseline=b.variant, n=len(a),
                                  recoveries_only_candidate=wins, recoveries_only_baseline=losses,
                                  mean_pnl_difference=delta))
    add_balanced(comparisons, pairs, test, xpaths)
    frontier = pareto_rows(comparisons)
    for name, rows in (("OPTIMIZATION_RESULTS",opt), ("COMPARISON_RESULTS",comparisons),
                       ("PARETO_FRONTIER",frontier), ("SCENARIO_MATRIX",matrix),
                       ("BUDGET_FRONTIER",budget_rows), ("PAIRED_RESULTS",pairs)):
        write_csv(name, rows)
    sensitivity = []
    for c, _ in entries:
        for fee in (2.25, 4.5, 9.):
            changed = replace(c, config=replace(c.config, commission=fee))
            sensitivity.append(dict(**info(changed), **summary(evaluate(changed,test,180),True)))
    write_csv("COST_SENSITIVITY",sensitivity)


def pareto_rows(comparisons):
    frontier = []
    for budget in BUDGETS:
        points = [r for r in comparisons if int(r["budget"]) == budget
                  and r["split"] == "independent_test"]
        metrics = [(round(float(p["rate"]), 8), -round(float(p["worst_loss"]), 8),
                    -round(float(p["cvar95"]), 8)) for p in points]
        for point, metric in zip(points, metrics):
            dominated = any(all(a >= b for a,b in zip(other,metric)) and other != metric
                            for other in metrics)
            if not dominated:
                frontier.append(point)
    return frontier


def add_balanced(comparisons, pairs, test, xpaths):
    c = Candidate("J Balanced", Params(net=12, trigger=140, horizon=12))
    for split, paths in (("independent_test", test), ("exhaustive_6", xpaths)):
        rows = evaluate(c, paths, 180)
        comparisons.append(dict(budget=180, **info(c), split=split,
                                **summary(rows, split=="independent_test")))
        if split == "independent_test":
            k = evaluate(Candidate("K"), paths, 180)
            wins, losses, delta = paired(rows, k)
            pairs.append(dict(budget=180, variant=c.variant, baseline="K", n=len(k),
                              recoveries_only_candidate=wins, recoveries_only_baseline=losses,
                              mean_pnl_difference=delta))


def test_report():
    suite = unittest.defaultTestLoader.discover(".")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    Path("TEST_RESULTS.json").write_text(json.dumps(
        dict(tests=result.testsRun, failures=len(result.failures), errors=len(result.errors),
             passed=result.wasSuccessful(), python=sys.version.split()[0]), indent=2)+"\n")
    if not result.wasSuccessful():
        raise SystemExit(1)


if __name__ == "__main__":
    test_report()
    main()
