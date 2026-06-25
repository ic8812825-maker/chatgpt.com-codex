from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
body = state.split("bool ReconcileRecoveredPosition", 1)[1].split("void LogManagedPositionsForRecovery", 1)[0]
assert "GetActualPositionVolume(snapshot.ticket)" in body
assert "SavedVolume" in body and "ActualVolume" in body
assert "lot = actualVolume" in body
print("RECOVERY_USES_ACTUAL_VOLUME_CHECK PASS")
