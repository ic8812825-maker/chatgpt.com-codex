from __future__ import annotations
import subprocess
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parent))
    from common import ALE_ROOT
else:
    from .common import ALE_ROOT


HERE = Path(__file__).resolve().parent


def _run(script: str):
    subprocess.check_call([sys.executable, str(HERE / script)])


def run():
    _run("lyapunov_validator.py")
    _run("control_latency_test.py")
    _run("tail_effectiveness.py")
    _run("stability_proof.py")

    lyap = (ALE_ROOT / "ALE_LYAPUNOV_PROOF.md").read_text(encoding="utf-8")
    stability = (ALE_ROOT / "ALE_STABILITY_REPORT.md").read_text(encoding="utf-8")
    tail = (ALE_ROOT / "ALE_TAIL_EFFECTIVENESS_REPORT.md").read_text(encoding="utf-8")

    has_unstable = "unstable" in lyap
    not_global = "NOT_GLOBALLY_STABLE" in stability

    final_truth = "UNSTABLE UNDER ADVERSARIAL MODES" if (has_unstable or not_global) else "NO INSTABILITY DETECTED IN TEST GRID"

    final_lines = [
        "# ALE_RISK_CONTROL_FINAL",
        "",
        "Repo-bound verification summary.",
        "",
        "## Checks",
        f"- Lyapunov unstable labels present: {has_unstable}",
        f"- Global stability rejected: {not_global}",
        f"- Tail report generated: {bool(tail.strip())}",
        "",
        "## Verdict",
        f"- {final_truth}",
        "- Risk control should be considered valid only inside tested safe operating envelope.",
    ]
    (ALE_ROOT / "ALE_RISK_CONTROL_FINAL.md").write_text("\n".join(final_lines) + "\n", encoding="utf-8")

    truth_lines = [
        "# ALE_FINAL_TRUTH",
        "",
        "This document intentionally reports the hard result from generated evidence.",
        "",
        "- Primary verdict: " + final_truth,
        "- If adversarial modes produce positive Lyapunov drift, claims of absolute stability are false.",
        "- Therefore: deployment must enforce bounded operating conditions and live monitoring.",
    ]
    (ALE_ROOT / "ALE_FINAL_TRUTH.md").write_text("\n".join(truth_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
