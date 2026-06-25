from pathlib import Path
root = Path(__file__).resolve().parents[1]
recon = (root / "Include" / "ReconciliationEngine.mqh").read_text()
ea = (root / "MinusLock_BigHarvest_EA.mq5").read_text()
state = (root / "Include" / "StateMachine.mqh").read_text()
for token in ["bool ValidateStatePositionConsistency()", "STATE_INITIAL_LOCK_OPENED", "STATE_FAR_ACTIVE", "STATE_BIG_SMALL_OPENED", "STATE_BIG_HARVEST", "STATE_SMALL_SCENARIO", "STATE_WAIT_SMALL_TO_FAR"]:
    assert token in recon, token
assert "ValidateStatePositionConsistency() && ok" in recon
assert "ValidateStatePositionConsistency()" in ea
assert "ValidateStatePositionConsistency()" in state
print("INITIAL_LOCK_STATE_CONSISTENCY_CHECK PASS")
