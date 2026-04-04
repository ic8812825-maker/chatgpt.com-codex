from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import SimConfig, run_closed_loop, summarize

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    compress = summarize(run_closed_loop(SimConfig(scenario="trend", seed=810), force_action="COMPRESS"))
    expand = summarize(run_closed_loop(SimConfig(scenario="trend", seed=810), force_action="EXPAND"))
    safe = summarize(run_closed_loop(SimConfig(scenario="trend", seed=810), force_action="SAFE"))
    policy = summarize(run_closed_loop(SimConfig(scenario="trend", seed=810)))

    compress_reduces_v = compress["E_dV"] < expand["E_dV"]
    expand_controlled = expand["max_V"] < 3.0
    safe_not_dominant = policy["action_safe"] < 0.7
    verdict = "PASS" if compress_reduces_v and expand_controlled and safe_not_dominant else "FAIL"

    lines = [
        "# ALE_ACTION_CAUSALITY",
        "",
        f"- COMPRESS E[ΔV]: {compress['E_dV']:.6f}",
        f"- EXPAND E[ΔV]: {expand['E_dV']:.6f}",
        f"- EXPAND max(V): {expand['max_V']:.6f}",
        f"- SAFE policy share: {policy['action_safe']:.6f}",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_ACTION_CAUSALITY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
