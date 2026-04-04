from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import SimConfig, run_closed_loop, summarize

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    r = run_closed_loop(SimConfig(scenario="jump", seed=3100, steps=300))
    m = summarize(r)
    expand_runaway = m["action_expand"] > 0 and m["max_V"] > 1.5
    safe_dom = m["action_safe"] > 0.30
    hard_share = m["action_hard"]
    verdict = "PASS" if (not expand_runaway) and (not safe_dom) and hard_share < 0.20 else "FAIL"

    lines = [
        "# ALE_ACTION_SANITY_V2",
        "",
        f"- max_V: {m['max_V']:.6f}",
        f"- action_expand: {m['action_expand']:.6f}",
        f"- action_safe: {m['action_safe']:.6f}",
        f"- action_hard: {hard_share:.6f}",
        f"- expand_runaway: {expand_runaway}",
        f"- safe_dominance: {safe_dom}",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_ACTION_SANITY_V2.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
