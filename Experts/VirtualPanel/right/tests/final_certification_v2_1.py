from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = [
    ("Objective", "ALE_OBJECTIVE_ALIGNMENT_V2.md"),
    ("Expand control", "ALE_EXPAND_CONTROL.md"),
    ("Fake stability fix", "ALE_FAKE_STABILITY_FIX.md"),
    ("Action sanity", "ALE_ACTION_SANITY_V2.md"),
    ("Causality", "ALE_ACTION_CAUSALITY_STRICT.md"),
    ("Necessity", "ALE_ACTION_NECESSITY_STRICT.md"),
    ("Adversarial", "ALE_ADVERSARIAL_V2.md"),
    ("Delay realism", "ALE_DELAY_REALISM.md"),
    ("Delay breakpoint", "ALE_DELAY_BREAKPOINT_V2.md"),
    ("Failure", "ALE_FAILURE_V2.md"),
    ("Dual-flow", "ALE_DUAL_FLOW_V2.md"),
    ("MPC", "ALE_TRUE_ARGMIN_FIXED.md"),
    ("Model", "ALE_MODEL_REALITY_DEEP.md"),
]


def status(p: Path) -> str:
    if not p.exists():
        return "❌"
    t = p.read_text(encoding="utf-8")
    return "✅" if "verdict: PASS" in t else "❌"


def run() -> None:
    lines = ["# ALE_FINAL_CERTIFICATION_V2_1", "", "| test | status |", "|---|---|"]
    states = []
    for n, fn in CHECKS:
        st = status(ROOT / fn)
        states.append(st)
        lines.append(f"| {n} | {st} |")
    prod = all(x == "✅" for x in states)
    lines += ["", "SYSTEM STATUS:", "- [ ] Research", "- [ ] Prototype", f"- [{'x' if not prod else ' '}] Pre-production", f"- [{'x' if prod else ' '}] ✅ Production-ready"]
    (ROOT / "ALE_FINAL_CERTIFICATION_V2_1.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
