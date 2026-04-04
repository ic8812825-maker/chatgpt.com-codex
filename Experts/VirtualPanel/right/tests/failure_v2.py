from __future__ import annotations

from pathlib import Path
from statistics import mean

from ale_alc_certification_lib import SimConfig, markdown_table, run_closed_loop

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    tests = [
        ("margin0", SimConfig("margin_cascade", seed=3601, steps=260, slippage=2.4, spread=2.6)),
        ("liquidity0", SimConfig("freeze", seed=3602, steps=260, slippage=2.3, spread=2.5)),
        ("infinite_spread", SimConfig("spread_explosion", seed=3603, steps=260, slippage=2.6, spread=12.0)),
        ("execution_fail", SimConfig("jump", seed=3604, steps=260, control_delay=45, latency_jitter=30, slippage=2.2)),
    ]
    rows = []
    for name, cfg in tests:
        r = run_closed_loop(cfg)
        emergency_hits = sum(1 for a in r.actions if a in ("SAFE", "HARD"))
        rows.append({"case": name, "collapse": int(r.collapse), "emergency_hits": emergency_hits, "max_V": round(max(r.values), 6)})

    collapse = mean(x["collapse"] for x in rows)
    emergency_all = all((x["emergency_hits"] > 0) or (x["case"] == "execution_fail" and x["collapse"] == 0) for x in rows)
    verdict = "PASS" if collapse == 0.0 and emergency_all else "FAIL"
    lines = ["# ALE_FAILURE_V2", "", markdown_table(rows, ["case", "collapse", "emergency_hits", "max_V"]), "", f"- collapse_rate: {collapse:.6f}", f"- emergency_triggered_all: {emergency_all}", f"- verdict: {verdict}"]
    (ROOT / "ALE_FAILURE_V2.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
