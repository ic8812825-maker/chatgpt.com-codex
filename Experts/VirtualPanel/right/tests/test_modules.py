from pathlib import Path

ROOT = Path("Experts/VirtualPanel/right")


def test_core_modules_present():
    modules = [
        "ALECore.mqh",
        "ALEGeometry.mqh",
        "ALEStateMachine.mqh",
    ]

    for module in modules:
        assert (ROOT / module).exists(), f"Missing module {module}"
