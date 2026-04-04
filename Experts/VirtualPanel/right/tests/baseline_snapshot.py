from __future__ import annotations

from collections import Counter
from pathlib import Path

from ale_alc_certification_lib import SimConfig, markdown_table, percentile, run_closed_loop, summarize

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    scenarios = ["trend", "jump", "freeze", "dual-flow"]
    rows = []
    all_actions = Counter()
    all_strength = []
    all_dv = []

    for i, sc in enumerate(scenarios):
        res = run_closed_loop(SimConfig(scenario=sc, seed=100 + i, dual_flow=(sc == "dual-flow")))
        m = summarize(res)
        all_actions.update(res.actions)
        all_strength.extend(res.control_strength)
        all_dv.extend(res.deltas)
        rows.append({
            "scenario": sc,
            "E_dV": round(m["E_dV"], 6),
            "P_dV_le_0": round(m["P_dV_le_0"], 6),
            "max_V": round(m["max_V"], 6),
            "entropy": round(m["entropy"], 6),
            "cvar_95": round(m["cvar_95"], 6),
        })

    total_actions = sum(all_actions.values())
    safe_share = all_actions["SAFE"] / max(1, total_actions)
    all_used = all_actions["EXPAND"] > 0 and all_actions["COMPRESS"] > 0 and all_actions["PARTIAL"] > 0 and all_actions["HARD"] > 0
    flat_control = (percentile(all_strength, 0.9) - percentile(all_strength, 0.1)) < 0.2

    lines = [
        "# ALE_BASELINE_FULL",
        "",
        "Re-baseline with action distribution, entropy, control-strength spread and ΔV tails.",
        "",
        "## Scenario metrics",
        markdown_table(rows, ["scenario", "E_dV", "P_dV_le_0", "max_V", "entropy", "cvar_95"]),
        "",
        "## Global action distribution",
    ]
    for a, c in sorted(all_actions.items()):
        lines.append(f"- {a}: {c} ({c / max(1,total_actions):.4f})")

    lines += [
        "",
        "## Control-strength histogram (quantiles)",
        f"- q10: {percentile(all_strength, 0.10):.4f}",
        f"- q50: {percentile(all_strength, 0.50):.4f}",
        f"- q90: {percentile(all_strength, 0.90):.4f}",
        "",
        "## ΔV tail",
        f"- p95: {percentile(all_dv, 0.95):.6f}",
        f"- p99: {percentile(all_dv, 0.99):.6f}",
        "",
        "## KPI",
        f"- SAFE domination check (<0.55): {safe_share:.4f}",
        f"- all key actions used: {all_used}",
        f"- flat control detected: {flat_control}",
    ]
    (ROOT / "ALE_BASELINE_FULL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
