from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import SimConfig, run_closed_loop

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    r = run_closed_loop(SimConfig(scenario="jump", seed=440, steps=320, latency_jitter=5))
    osc_depth = 0
    stickiness_changes = 0
    deriv_max = 0.0

    for i in range(3, len(r.actions)):
        seq = r.actions[i - 3 : i + 1]
        if seq == ["EXPAND", "SOFT", "COMPRESS", "EXPAND"]:
            osc_depth += 1
    for i in range(1, len(r.actions)):
        if r.actions[i] != r.actions[i - 1]:
            stickiness_changes += 1
        deriv_max = max(deriv_max, abs(r.control_strength[i] - r.control_strength[i - 1]))

    change_rate = stickiness_changes / max(1, len(r.actions) - 1)
    verdict = "PASS" if deriv_max < 0.9 and change_rate < 0.75 and osc_depth == 0 else "FAIL"

    lines = [
        "# ALE_CONTROL_STABILITY_DEEP",
        "",
        f"- oscillation_depth_events: {osc_depth}",
        f"- d(control_strength)/dt max: {deriv_max:.6f}",
        f"- action_change_rate: {change_rate:.6f}",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_CONTROL_STABILITY_DEEP.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
