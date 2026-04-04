from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import ACTIONS, SimConfig, markdown_table, run_closed_loop, summarize

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    base = summarize(run_closed_loop(SimConfig(scenario="jump", seed=612, steps=260)))
    rows = []
    all_bad = True
    for a in ACTIONS:
        ablated = summarize(run_closed_loop(SimConfig(scenario="jump", seed=612, steps=260), disable_action=a))
        delta = (ablated["E_dV"] - base["E_dV"]) + 0.15 * (ablated["max_V"] - base["max_V"]) + 0.4 * (ablated["cvar_95"] - base["cvar_95"])
        is_bad = delta > 0
        all_bad = all_bad and is_bad
        rows.append({"action_removed": a, "objective_degradation": round(delta, 6), "worse": is_bad})

    verdict = "PASS" if all_bad else "FAIL"
    lines = [
        "# ALE_ACTION_NECESSITY_FULL",
        "",
        markdown_table(rows, ["action_removed", "objective_degradation", "worse"]),
        "",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_ACTION_NECESSITY_FULL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
