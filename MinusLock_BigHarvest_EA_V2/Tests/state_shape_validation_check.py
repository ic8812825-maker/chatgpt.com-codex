from pathlib import Path
root = Path(__file__).resolve().parents[1]
engine = (root / "Include" / "StateIntegrityEngine.mqh").read_text()
recon = (root / "Include" / "ReconciliationEngine.mqh").read_text()
ea = (root / "MinusLock_BigHarvest_EA.mq5").read_text()
for token in ["EXPECTED_POSITION_MISSING", "UNEXPECTED_POSITION_PRESENT", "INVALID_STATE_SHAPE", "VolumeMismatchToleranceLots", "GetManagedPositionByTicket", "POSITION_VOLUME"]:
    assert token in engine
assert "ValidateCurrentStateIntegrity() && ok" in recon
assert "else if(!ValidateCurrentStateIntegrity())" in ea
print("PASS state_shape_validation_check")
