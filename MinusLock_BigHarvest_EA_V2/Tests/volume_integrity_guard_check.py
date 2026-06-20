from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
config = (root / "Include" / "Config.mqh").read_text()
assert "input double VolumeMismatchToleranceLots = 0.001;" in config
assert "bool VerifyPositionVolumeIntegrity" in state
for token in ["ExpectedVolume", "ActualVolume", "Difference", "POSITION_VOLUME_INTEGRITY_FAIL"]:
    assert token in state
print("VOLUME_INTEGRITY_GUARD_CHECK PASS")
