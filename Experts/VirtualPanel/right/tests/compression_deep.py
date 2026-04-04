from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import SimConfig, run_closed_loop

ROOT = Path(__file__).resolve().parents[1]
ORDER = {"SOFT": 1, "COMPRESS": 2, "PARTIAL": 3, "HARD": 4}


def run() -> None:
    r = run_closed_loop(SimConfig(scenario="jump", seed=511, steps=280))
    chain_ok = True
    trigger_pairs = []

    for i in range(1, len(r.actions)):
        a0, a1 = r.actions[i - 1], r.actions[i]
        if a0 in ORDER and a1 in ORDER and ORDER[a1] < ORDER[a0] - 1:
            chain_ok = False
        if i < len(r.deltas):
            trigger_pairs.append((r.deltas[i - 1], ORDER.get(a1, 0)))

    corr_num = sum(max(0.0, dv) * lvl for dv, lvl in trigger_pairs)
    over_compress = r.actions.count("HARD") / max(1, len(r.actions)) > 0.35
    verdict = "PASS" if chain_ok and corr_num > 0 and not over_compress else "FAIL"

    lines = [
        "# ALE_COMPRESSION_DEEP",
        "",
        f"- escalation_chain_monotonic: {chain_ok}",
        f"- compression_trigger_score: {corr_num:.6f}",
        f"- over_compression: {over_compress}",
        f"- verdict: {verdict}",
    ]
    (ROOT / "ALE_COMPRESSION_DEEP.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
