from __future__ import annotations

from pathlib import Path

from ale_alc_certification_lib import ACTIONS, SimConfig, markdown_table, run_closed_loop

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    rows = []
    for a in ACTIONS:
        r = run_closed_loop(SimConfig(scenario="jump", seed=3200, steps=180), force_action=a)
        de = r.states[-1].exposure - r.states[0].exposure
        dm = r.states[-1].margin - r.states[0].margin
        dr = r.states[-1].risk - r.states[0].risk
        dv = sum(r.deltas) / max(1, len(r.deltas))
        rows.append({"action": a, "d_exposure": round(de, 6), "d_margin": round(dm, 6), "d_risk": round(dr, 6), "dV_real": round(dv, 6)})

    compress = next(x for x in rows if x["action"] == "COMPRESS")["dV_real"] < 0
    expand = next(x for x in rows if x["action"] == "EXPAND")["dV_real"] <= 0.10
    safe_not_best = sorted(rows, key=lambda x: x["dV_real"])[0]["action"] != "SAFE"
    verdict = "PASS" if compress and expand and safe_not_best else "FAIL"

    lines = ["# ALE_ACTION_CAUSALITY_STRICT", "", markdown_table(rows, ["action", "d_exposure", "d_margin", "d_risk", "dV_real"]), "", f"- compress_dV_negative: {compress}", f"- expand_controlled: {expand}", f"- safe_not_always_best: {safe_not_best}", f"- verdict: {verdict}"]
    (ROOT / "ALE_ACTION_CAUSALITY_STRICT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
