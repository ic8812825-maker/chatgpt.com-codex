from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import SimConfig, markdown_table, run_closed_loop

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    cases = [
        ("margin_zero", SimConfig("margin_cascade", seed=1000, slippage=2.0, spread=2.0)),
        ("liquidity_zero", SimConfig("freeze", seed=1001, slippage=2.2, spread=2.0, latency_jitter=10)),
        ("infinite_spread", SimConfig("spread_explosion", seed=1002, slippage=2.5, spread=20.0)),
        ("execution_fail", SimConfig("jump", seed=1003, control_delay=50, latency_jitter=25, slippage=2.3)),
    ]
    rows = []
    for name, cfg in cases:
        r = run_closed_loop(cfg)
        safe_shutdown = r.actions.count("HARD") > 0 and r.actions[-1] in ("HARD", "PARTIAL", "COMPRESS")
        rows.append({"case": name, "collapse": int(r.collapse), "safe_shutdown": safe_shutdown, "max_V": round(max(r.values), 6)})

    survives = all(row["collapse"] == 0 or row["safe_shutdown"] for row in rows)
    verdict = "PASS" if survives else "FAIL"
    lines = [
        "# ALE_FAILURE_FINAL",
        "",
        markdown_table(rows, ["case", "collapse", "safe_shutdown", "max_V"]),
        "",
        f"- survives_or_safe_shutdown: {survives}",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_FAILURE_FINAL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
