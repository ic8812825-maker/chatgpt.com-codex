from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import SimConfig, run_closed_loop

ROOT = Path(__file__).resolve().parents[1]


ACTION_LEVEL = {"COMPRESS": -1.0, "SAFE": -0.4, "HOLD": 0.0, "EXPAND": 1.0}


def run() -> None:
    r = run_closed_loop(SimConfig(scenario="trend", seed=440, steps=300))
    oscillations = 0
    jitter = 0
    for i in range(1, len(r.actions)):
        pair = (r.actions[i - 1], r.actions[i])
        if pair in (("EXPAND", "COMPRESS"), ("COMPRESS", "EXPAND")):
            oscillations += 1
        if abs(ACTION_LEVEL[r.actions[i]] - ACTION_LEVEL[r.actions[i - 1]]) > 0.9:
            jitter += 1

    osc_rate = oscillations / max(1, len(r.actions) - 1)
    smooth_max = 0.0
    for i in range(1, len(r.actions)):
        smooth_max = max(smooth_max, abs(ACTION_LEVEL[r.actions[i]] - ACTION_LEVEL[r.actions[i - 1]]))

    verdict = "PASS" if osc_rate < 0.05 and smooth_max <= 1.0 else "FAIL"
    lines = [
        "# ALE_CONTROL_STABILITY",
        "",
        f"- oscillation_rate: {osc_rate:.6f} (target < 0.05)",
        f"- micro_jitter_events: {jitter}",
        f"- max_control_delta: {smooth_max:.3f}",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_CONTROL_STABILITY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
