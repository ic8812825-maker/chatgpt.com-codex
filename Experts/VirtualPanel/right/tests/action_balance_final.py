from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import ACTIONS, SimConfig, markdown_table, run_closed_loop, summarize

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    scenarios = ["trend", "jump", "freeze", "dual-flow"]
    agg = {a: 0.0 for a in ACTIONS}
    rows = []
    for i, sc in enumerate(scenarios):
        m = summarize(run_closed_loop(SimConfig(scenario=sc, seed=1500 + i, dual_flow=(sc == "dual-flow"), steps=260)))
        for a in ACTIONS:
            agg[a] += m[f"action_{a.lower()}"]

    for a in ACTIONS:
        agg[a] /= len(scenarios)
        rows.append({"action": a, "share": round(agg[a], 6)})

    min_ok = all(agg[a] > 0.05 for a in ACTIONS)
    expand_ok = agg["EXPAND"] > 0.05
    verdict = "PASS" if min_ok and expand_ok else "FAIL"

    lines = [
        "# ALE_ACTION_BALANCE_FINAL",
        "",
        markdown_table(rows, ["action", "share"]),
        "",
        f"- all_actions_gt_5pct: {min_ok}",
        f"- expand_gt_5pct: {expand_ok}",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_ACTION_BALANCE_FINAL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
