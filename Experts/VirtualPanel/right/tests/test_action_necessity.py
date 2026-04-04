from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import ACTIONS, SimConfig, markdown_table, run_closed_loop, summarize

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    base = run_closed_loop(SimConfig(scenario="jump", seed=512, steps=220))
    base_m = summarize(base)
    rows = []
    degradations = []
    for action in ACTIONS:
        removed = run_closed_loop(SimConfig(scenario="jump", seed=512, steps=220), disable_action=action)
        m = summarize(removed)
        deg = (m["E_dV"] - base_m["E_dV"]) + (m["max_V"] - base_m["max_V"]) * 0.1
        degradations.append(deg)
        rows.append({"removed_action": action, "E_dV": round(m["E_dV"], 6), "max_V": round(m["max_V"], 6), "degradation": round(deg, 6)})

    verdict = "PASS" if all(d > 0 for d in degradations) else "FAIL"
    lines = [
        "# ALE_ACTION_IMPORTANCE",
        "",
        "Action necessity test by ablating each action and measuring degradation.",
        "",
        markdown_table(rows, ["removed_action", "E_dV", "max_V", "degradation"]),
        "",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_ACTION_IMPORTANCE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
