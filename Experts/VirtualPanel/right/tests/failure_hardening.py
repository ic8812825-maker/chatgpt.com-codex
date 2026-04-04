from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import SimConfig, markdown_table, run_closed_loop

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    scenarios = [
        ("margin≈0", SimConfig("margin_cascade", seed=1001, steps=260)),
        ("liquidity=0", SimConfig("freeze", seed=1002, steps=260)),
        ("infinite_vol", SimConfig("flash_crash", seed=1003, steps=260, slippage=2.2)),
        ("delay_spike", SimConfig("jump", seed=1004, steps=260, control_delay=40)),
        ("slippage_extreme", SimConfig("spread_explosion", seed=1005, steps=260, slippage=3.0, spread=2.5)),
    ]
    rows = []
    for name, cfg in scenarios:
        r = run_closed_loop(cfg)
        emergency = r.actions.count("COMPRESS") > 0
        rows.append({"scenario": name, "collapse": int(r.collapse), "max_V": round(max(r.values), 6), "emergency_control": emergency})

    diverge = any(r["collapse"] == 1 for r in rows)
    emergency = all(r["emergency_control"] for r in rows)
    verdict = "PASS" if (not diverge) and emergency else "FAIL"
    lines = [
        "# ALE_FAILURE_HARDENING",
        "",
        markdown_table(rows, ["scenario", "collapse", "max_V", "emergency_control"]),
        "",
        f"- no_divergence: {not diverge}",
        f"- emergency_control_present: {emergency}",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_FAILURE_HARDENING.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
