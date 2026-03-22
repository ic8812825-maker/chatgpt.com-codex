from __future__ import annotations
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parent))
    from common import ALE_ROOT
else:
    from .common import ALE_ROOT


def _parse_table(path: Path):
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("| ") and not line.startswith("|---"):
            out.append([c.strip() for c in line.strip("|").split("|")])
    return out


def run():
    lyap = ALE_ROOT / "ALE_LYAPUNOV_PROOF.md"
    latency = ALE_ROOT / "ALE_CONTROL_LATENCY_REPORT.md"
    tail = ALE_ROOT / "ALE_TAIL_EFFECTIVENESS_REPORT.md"

    lyap_rows = _parse_table(lyap)
    tail_rows = _parse_table(tail)

    unstable_modes = []
    for r in lyap_rows[1:]:
        if len(r) >= 6 and r[5] == "unstable":
            unstable_modes.append(r[0])

    improved = 0
    compared = 0
    for r in tail_rows[1:]:
        if len(r) >= 4:
            compared += 1
            try:
                if float(r[3]) > 0:
                    improved += 1
            except ValueError:
                pass

    conclusion = "ROBUST_ENOUGH"
    if unstable_modes or improved < compared:
        conclusion = "NOT_GLOBALLY_STABLE"

    lines = [
        "# ALE_STABILITY_REPORT",
        "",
        "Combined proof-like validation over Lyapunov drift, latency sensitivity, and tail-risk effectiveness.",
        "",
        "## Inputs",
        f"- Lyapunov report present: {lyap.exists()}",
        f"- Control latency report present: {latency.exists()}",
        f"- Tail effectiveness report present: {tail.exists()}",
        "",
        "## Aggregated findings",
        f"- Unstable Lyapunov modes: {', '.join(unstable_modes) if unstable_modes else 'none'}",
        f"- Tail-risk improved modes: {improved}/{max(1, compared)}",
        "",
        "## Final status",
        f"- {conclusion}",
        "- If NOT_GLOBALLY_STABLE appears, system must be treated as conditionally stable only.",
    ]

    (ALE_ROOT / "ALE_STABILITY_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
