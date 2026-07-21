#!/usr/bin/env python3
"""Deterministic multi-objective search for Hybrid Split Big candidates.

Uses two independent samplers (stratified Latin hypercube and uniform random)
and writes both accepted Pareto candidates and rejected diagnostics.
"""
from __future__ import annotations
import argparse, csv, json, random, sys
from pathlib import Path
from typing import Iterable, List

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hybrid_geometry_model import ARCHITECTURES, Broker, Candidate, Evaluation, evaluate, monotonicity_trace, select_minimum_safe_new_far

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ["architecture", "core_ratio", "trend_ratio", "small_ratio", "reserve_share", "target_far_ratio", "safety_factor", "min_net_exposure", "max_new_big_ratio", "minimum_improvement", "accepted", "reject_reason", "core_lot", "trend_lot", "small_lot", "new_far_lot", "net_big_exposure", "recovery_slope", "reserve_slope", "far_loss_slope", "catchup_ratio", "new_far_ratio", "new_big_gross_ratio", "new_big_directional_ratio", "margin_percent", "transition_gross", "transition_costs", "transition_net", "reserve_credit", "transition_budget", "reverse_bound", "score", "method"]

def candidate(r: random.Random, i: int, n: int, method: str) -> Candidate:
    # Stratification gives coverage; random search probes different ordering.
    def x(lo, hi, salt):
        u = ((i + r.random()) / n if method == "lhs" else r.random())
        return lo + (hi - lo) * ((u + salt) % 1.0)
    return Candidate(ARCHITECTURES[i % len(ARCHITECTURES)], x(.8, 2.5, .11), x(.01, 1., .29), x(.05, 1.2, .47), x(.5, 1., .61), x(.2, .9, .79), x(1.05, 1.30, .13), x(.01, .5, .37), x(.5, 1., .53), .01)

def robust(e: Evaluation, broker: Broker) -> bool:
    points = (0, 1, 5, 10, 25, 50, 100, 150, 200, 300, 400)
    for multiplier in (1.0, 2.0):
        test = select_minimum_safe_new_far(e.candidate, broker, 1.0, 200.0, multiplier)
        trace = monotonicity_trace(e.candidate, broker, 1.0, points, multiplier)
        if not test.accepted or any(b < a + e.candidate.minimum_improvement - 1e-9 for a, b in zip(trace, trace[1:])):
            return False
    return True

def pareto(rows: List[Evaluation]) -> List[Evaluation]:
    # A dense 100k search may leave many feasible rows.  Pareto comparison on
    # the strongest screened subset preserves report usefulness without an
    # accidental quadratic 100k-by-100k runtime.
    rows = sorted(rows, key=lambda e: e.score, reverse=True)[:3000]
    out=[]
    for x in rows:
        dominated=False
        for y in rows:
            if y is x: continue
            no_worse=(y.new_far_ratio<=x.new_far_ratio and y.new_big_gross_ratio<=x.new_big_gross_ratio and y.margin_percent<=x.margin_percent and y.catchup_ratio>=x.catchup_ratio and y.recovery_slope>=x.recovery_slope)
            better=(y.new_far_ratio<x.new_far_ratio or y.new_big_gross_ratio<x.new_big_gross_ratio or y.margin_percent<x.margin_percent or y.catchup_ratio>x.catchup_ratio or y.recovery_slope>x.recovery_slope)
            if no_worse and better: dominated=True; break
        if not dominated: out.append(x)
    return sorted(out, key=lambda e: (-e.score, e.new_far_ratio))

def write(path: Path, rows: Iterable[Evaluation], methods: dict[int,str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=FIELDS); w.writeheader()
        for e in rows:
            row=e.row(); row["method"]=methods[id(e)]; w.writerow({k:row.get(k, "") for k in FIELDS})

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--runs", type=int, default=100_000); ap.add_argument("--seed", type=int, default=20260720); ap.add_argument("--reports", type=Path, default=ROOT/"Reports")
    a=ap.parse_args(); r=random.Random(a.seed); broker=Broker(); all_rows=[]; methods={}
    for method in ("lhs", "random"):
        for i in range(a.runs // 2):
            e=select_minimum_safe_new_far(candidate(r,i,a.runs//2,method),broker)
            if e.accepted and not robust(e,broker):
                e.accepted=False; e.reject_reason="STRESS_OR_MONOTONICITY"; e.score=-1e9
            all_rows.append(e); methods[id(e)]=method
    accepted=[e for e in all_rows if e.accepted]; rejected=[e for e in all_rows if not e.accepted]; front=pareto(accepted)
    write(a.reports/"Hybrid_Candidates.csv", accepted, methods); write(a.reports/"Hybrid_Rejected_Candidates.csv", rejected, methods); write(a.reports/"Hybrid_Pareto_Front.csv", front, methods)
    best=front[:10]
    (a.reports/"Hybrid_Best_Configurations.json").write_text(json.dumps([e.row() for e in best], ensure_ascii=False, indent=2)+"\n",encoding="utf-8")
    report=["# Hybrid Split Big — отчёт оптимизации", "", f"Проверено кандидатов: {len(all_rows)} (LHS + random, seed={a.seed}).", f"Допущено жёсткими Gate: {len(accepted)}; отклонено: {len(rejected)}.", "", "## Метод", "Кандидат допускается только после проверки положительного наклона RecoveryPL, catch-up Reserve, округления, NewFar, NewBig, margin и удвоенных расходов. Reserve credit и transition budget раздельны; бюджет перехода не является Reserve.", "", "## Pareto-front", "|Архитектура|NewFar|NewBig gross|Catch-up|Recovery slope|Margin %|Reverse bound|", "|---|---:|---:|---:|---:|---:|---:|"]
    for e in best: report.append(f"|{e.candidate.architecture}|{e.new_far_ratio:.3f}|{e.new_big_gross_ratio:.3f}|{e.catchup_ratio:.3f}|{e.recovery_slope:.3f}|{e.margin_percent:.1f}|{e.reverse_bound}|")
    report += ["", "## Ограничение", "Результаты являются независимым математическим screening. Они не заменяют MetaEditor compile, Every Tick based on real ticks, реальные retcode/fill и terminal restart."]
    (a.reports/"Hybrid_Optimization_Report_RU.md").write_text("\n".join(report)+"\n",encoding="utf-8")
    print(f"runs={len(all_rows)} accepted={len(accepted)} pareto={len(front)}")
    return 0 if accepted else 2
if __name__ == "__main__": raise SystemExit(main())
