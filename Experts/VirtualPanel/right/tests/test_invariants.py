from pathlib import Path


def test_invariants_present():
    file = Path("Experts/VirtualPanel/right/ALECore.mqh")
    text = file.read_text(encoding="utf-8")

    invariants = ["I1", "I6", "I7"]

    for inv in invariants:
        assert inv in text, f"Invariant {inv} not documented"
