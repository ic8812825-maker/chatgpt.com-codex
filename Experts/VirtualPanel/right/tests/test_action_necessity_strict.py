from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import ACTIONS, SimConfig, markdown_table, run_closed_loop

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    rows = []
    ok = True
    for i, a in enumerate(ACTIONS):
        cfg = SimConfig(scenario="jump", seed=3350 + i, steps=220)
        with_a = run_closed_loop(cfg, force_action=a)
        without_a = run_closed_loop(cfg, disable_action=a)

        e_with = sum(with_a.deltas) / max(1, len(with_a.deltas))
        e_without = sum(without_a.deltas) / max(1, len(without_a.deltas))
        degradation = abs(e_without - e_with) + 0.1 * abs(max(without_a.values) - max(with_a.values))
        worse = degradation > 1e-5
        ok = ok and worse
        rows.append({"action": a, "degradation": round(degradation, 6), "worse": worse})

    lines = ["# ALE_ACTION_NECESSITY_STRICT", "", markdown_table(rows, ["action", "degradation", "worse"]), "", f"- all_degradation_positive: {ok}", f"- verdict: {'PASS' if ok else 'FAIL'}"]
    (ROOT / "ALE_ACTION_NECESSITY_STRICT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
