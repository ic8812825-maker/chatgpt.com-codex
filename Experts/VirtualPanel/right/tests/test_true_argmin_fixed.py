from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import SimConfig, _candidate_actions, choose_mpc_action, evaluate_action_objective, run_closed_loop

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    matches = 0
    trials = 0
    worst_error = 0.0

    for seed in range(300, 520):
        cfg = SimConfig(scenario="jump", seed=seed, steps=140)
        sim = run_closed_loop(cfg)
        state = sim.states[0]
        history = []
        mpc_action = choose_mpc_action(state, cfg, 1, history, seed, last_real_dv=-0.001, explore=False)

        candidates = _candidate_actions(state.v)
        dv_pred = 0.02 * state.vol + 0.02 * max(0.0, state.v - 0.8) + cfg.control_delay * 0.001
        if (state.v > 1.0 or dv_pred > 0.0) and "EXPAND" in candidates:
            candidates.remove("EXPAND")
        if state.v < 1.15 and "HARD" in candidates:
            candidates.remove("HARD")
        if abs(dv_pred) > 0.012 and "HOLD" in candidates:
            candidates.remove("HOLD")
        scores = {a: evaluate_action_objective(state, a, cfg, t=1, history=history, rng_seed=seed + i * 13, last_real_dv=-0.001) for i, a in enumerate(candidates)}
        best_action = min(scores, key=scores.get)
        err = abs(scores[mpc_action] - scores[best_action])
        matches += int(mpc_action == best_action)
        worst_error = max(worst_error, err)
        trials += 1

    match_ratio = matches / max(1, trials)
    verdict = "PASS" if match_ratio >= 0.9 and worst_error < 0.2 else "FAIL"
    lines = [
        "# ALE_TRUE_ARGMIN_FIXED",
        "",
        f"- match_ratio: {match_ratio:.6f}",
        f"- worst_error: {worst_error:.6f}",
        "- target: match_ratio >= 0.90 and worst_error < 0.2",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_TRUE_ARGMIN_FIXED.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
