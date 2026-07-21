#!/usr/bin/env python3
"""Run an independent Hybrid Split Big proof simulation from JSON config."""
from __future__ import annotations
import argparse, json, sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hybrid_geometry_model import Broker, Candidate, all_start_lot_bounds, evaluate, monotonicity_trace


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("config", help="JSON with optional broker, candidate, far_lot, far_distance and points")
    p.add_argument("--output", type=Path)
    a = p.parse_args()
    raw = json.loads(Path(a.config).read_text(encoding="utf-8"))
    broker = Broker(**raw.get("broker", {})); candidate = Candidate(**raw["candidate"])
    far = raw.get("far_lot", 1.0); distance = raw.get("far_distance", 200.0)
    points = raw.get("points", [0, 1, 5, 10, 25, 50, 100, 150, 200, 300, 400])
    e = evaluate(candidate, broker, far, distance, raw.get("cost_multiplier", 1.0))
    trace = monotonicity_trace(candidate, broker, far, points, raw.get("cost_multiplier", 1.0))
    result = {"evaluation": e.row(), "points": points, "projected_recovery_pl": trace,
              "monotonicity_pass": all(b > a + candidate.minimum_improvement - 1e-9 for a, b in zip(trace, trace[1:])),
              "reverse_bounds": all_start_lot_bounds(candidate, broker),
              "mandatory_pass": e.accepted}
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if a.output: a.output.write_text(text + "\n", encoding="utf-8")
    else: print(text)
    return 0 if result["mandatory_pass"] and result["monotonicity_pass"] else 2
if __name__ == "__main__": raise SystemExit(main())
