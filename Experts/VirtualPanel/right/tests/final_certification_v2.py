from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECKS = [
    ("Objective alignment", "ALE_OBJECTIVE_ALIGNMENT_V2.md"),
    ("Action sanity", "ALE_ACTION_SANITY_V2.md"),
    ("Causality", "ALE_ACTION_CAUSALITY_STRICT.md"),
    ("Action necessity", "ALE_ACTION_NECESSITY_STRICT.md"),
    ("Adversarial", "ALE_ADVERSARIAL_V2.md"),
    ("Delay breakpoint", "ALE_DELAY_BREAKPOINT_V2.md"),
    ("Failure", "ALE_FAILURE_V2.md"),
    ("Dual-flow", "ALE_DUAL_FLOW_V2.md"),
    ("MPC argmin", "ALE_TRUE_ARGMIN_FIXED.md"),
    ("Model vs Real", "ALE_MODEL_REALITY_DEEP.md"),
]


def status(path: Path) -> str:
    if not path.exists():
        return "❌"
    t = path.read_text(encoding="utf-8")
    return "✅" if "verdict: PASS" in t else "❌"


def run() -> None:
    statuses = []
    lines = ["# ALE_FINAL_CERTIFICATION_V2", "", "| test | status |", "|---|---|"]
    for name, fn in CHECKS:
        st = status(ROOT / fn)
        statuses.append(st)
        lines.append(f"| {name} | {st} |")

    prod = all(s == "✅" for s in statuses)
    lines += ["", "SYSTEM STATUS:", "- [ ] Research", "- [ ] Prototype", f"- [{'x' if not prod else ' '}] Pre-production", f"- [{'x' if prod else ' '}] ✅ Production-ready"]
    (ROOT / "ALE_FINAL_CERTIFICATION_V2.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
