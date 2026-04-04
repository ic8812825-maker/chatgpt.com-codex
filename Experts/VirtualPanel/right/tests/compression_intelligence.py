from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from ale_alc_certification_lib import markdown_table, run_closed_loop, SimConfig

ROOT = Path(__file__).resolve().parents[1]
LEVEL = {"SOFT": 1, "COMPRESS": 2, "PARTIAL": 3, "HARD": 4}


def run() -> None:
    r = run_closed_loop(SimConfig(scenario="jump", seed=1801, steps=320))
    skip_forbidden = True
    hard_premature = 0
    by_action = defaultdict(list)

    for i, a in enumerate(r.actions):
        if i > 0:
            p = r.actions[i - 1]
            if p in LEVEL and a in LEVEL and LEVEL[a] > LEVEL[p] + 1:
                skip_forbidden = False
        if a == "HARD" and r.values[i] < 1.3:
            hard_premature += 1
        if i < len(r.deltas):
            by_action[a].append(r.deltas[i])

    rows = []
    for a, vals in sorted(by_action.items()):
        rows.append({"action": a, "mean_dV": round(sum(vals) / max(1, len(vals)), 6), "count": len(vals)})

    verdict = "PASS" if skip_forbidden and hard_premature == 0 else "FAIL"
    lines = [
        "# ALE_COMPRESSION_INTELLIGENCE",
        "",
        f"- no_skip_escalation: {skip_forbidden}",
        f"- premature_hard_close_count: {hard_premature}",
        "",
        markdown_table(rows, ["action", "mean_dV", "count"]),
        "",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_COMPRESSION_INTELLIGENCE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
