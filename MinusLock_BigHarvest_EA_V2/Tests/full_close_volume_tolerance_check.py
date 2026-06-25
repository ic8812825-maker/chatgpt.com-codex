from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
assert "bool IsPositionFullyClosed(double actualVolume)" in state
assert "actualVolume <= VolumeMismatchToleranceLots" in state
assert "VERIFY_FULL_CLOSE" in state
print("FULL_CLOSE_VOLUME_TOLERANCE_CHECK PASS")
