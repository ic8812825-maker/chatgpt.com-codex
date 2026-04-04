from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import SimConfig, run_closed_loop, summarize

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    s = summarize(run_closed_loop(SimConfig(scenario="fake_stability_trap", seed=3810, steps=320, slippage=1.9, spread=2.1)))
    verdict = "PASS" if s["E_dV"] <= 0 and s["max_V"] < 1.5 else "FAIL"
    lines = [
        "# ALE_FAKE_STABILITY_FIX",
        "",
        f"- E_dV: {s['E_dV']:.6f}",
        f"- max_V: {s['max_V']:.6f}",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_FAKE_STABILITY_FIX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
