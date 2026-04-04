from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import ACTIONS, SimConfig, run_closed_loop

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    matches = 0
    trials = 0
    worst_error = 0.0

    for seed in range(300, 420):
        cfg = SimConfig(scenario="jump", seed=seed, steps=120)
        mpc = run_closed_loop(cfg)
        mpc_action = mpc.actions[0] if mpc.actions else "HOLD"

        scores = {}
        for action in ACTIONS:
            forced = run_closed_loop(cfg, force_action=action)
            scores[action] = sum(forced.deltas)

        best_action = min(scores, key=scores.get)
        if mpc_action == best_action:
            matches += 1

        worst_error = max(worst_error, abs(scores[mpc_action] - scores[best_action]))
        trials += 1

    match_ratio = matches / max(1, trials)
    threshold = 0.2
    verdict = "PASS" if match_ratio >= 0.9 and worst_error < threshold else "FAIL"

    lines = [
        "# ALE_TRUE_ARGMIN_GLOBAL",
        "",
        "True argmin check by exhaustive action replay on each decision point seed.",
        "",
        f"- match_ratio: {match_ratio:.4f} (target >= 0.90)",
        f"- worst_case_error: {worst_error:.6f} (threshold < {threshold})",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_TRUE_ARGMIN_GLOBAL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
