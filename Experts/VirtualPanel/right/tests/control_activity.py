from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import SimConfig, percentile, run_closed_loop

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    r = run_closed_loop(SimConfig(scenario="jump", seed=1401, steps=260))
    hold = r.actions.count("HOLD") / max(1, len(r.actions))
    q50 = percentile(r.control_strength, 0.5)
    q90 = percentile(r.control_strength, 0.9)
    verdict = "PASS" if hold < 0.3 and q50 > 0.0 else "FAIL"

    lines = [
        "# ALE_CONTROL_ACTIVITY",
        "",
        f"- hold_share: {hold:.6f}",
        f"- q50_control_strength: {q50:.6f}",
        f"- q90_control_strength: {q90:.6f}",
        "- target: HOLD < 30%, q50 > 0",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_CONTROL_ACTIVITY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
