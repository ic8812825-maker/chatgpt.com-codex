from __future__ import annotations

from pathlib import Path
from statistics import mean

from ale_alc_certification_lib import SimConfig, markdown_table, run_closed_loop, summarize

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    cases = [
        ("infinite_trend", SimConfig("trend", seed=3401, steps=320, slippage=1.8, spread=2.0)),
        ("spread_x10", SimConfig("spread_explosion", seed=3402, steps=320, spread=10.0, slippage=2.0)),
        ("latency_jump", SimConfig("jump", seed=3403, steps=320, control_delay=30, latency_jitter=25, slippage=1.8)),
        ("margin_cascade", SimConfig("margin_cascade", seed=3404, steps=320, slippage=2.2, spread=2.4)),
        ("fake_stability_trap", SimConfig("fake_stability_trap", seed=3405, steps=320, slippage=1.8, spread=2.0)),
    ]
    rows = []
    for name, cfg in cases:
        m = summarize(run_closed_loop(cfg))
        rows.append({"scenario": name, "E_dV": round(m["E_dV"], 6), "collapse": int(m["collapse"]), "max_V": round(m["max_V"], 6)})

    all_non_positive = all(r["E_dV"] <= 0 for r in rows)
    e = mean(r["E_dV"] for r in rows)
    c = mean(r["collapse"] for r in rows)
    vmax = max(r["max_V"] for r in rows)
    verdict = "PASS" if all_non_positive and e < 0 and c < 0.05 and vmax < 1.5 else "FAIL"

    lines = [
        "# ALE_ADVERSARIAL_V2",
        "",
        markdown_table(rows, ["scenario", "E_dV", "collapse", "max_V"]),
        "",
        f"- all_E_dV_non_positive: {all_non_positive}",
        f"- E_dV_mean: {e:.6f}",
        f"- collapse_rate: {c:.6f}",
        f"- max_V: {vmax:.6f}",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_ADVERSARIAL_V2.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
