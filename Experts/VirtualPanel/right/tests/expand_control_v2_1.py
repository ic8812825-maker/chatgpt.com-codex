from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import SimConfig, run_closed_loop, summarize

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    modes = ["trend", "jump", "fake_stability_trap"]
    shares = []
    maxv = []
    for i, m in enumerate(modes):
        s = summarize(run_closed_loop(SimConfig(scenario=m, seed=3800 + i, steps=280)))
        shares.append(s["action_expand"])
        maxv.append(s["max_V"])
    expand_share = sum(shares) / len(shares)
    max_v = max(maxv)
    verdict = "PASS" if expand_share <= 0.35 and max_v < 1.5 else "FAIL"
    lines = [
        "# ALE_EXPAND_CONTROL",
        "",
        f"- expand_share_mean: {expand_share:.6f}",
        f"- max_V_stress: {max_v:.6f}",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_EXPAND_CONTROL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
