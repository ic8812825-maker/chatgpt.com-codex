from pathlib import Path
root = Path(__file__).resolve().parents[1]
types = (root / "Include" / "Types.mqh").read_text()
state = (root / "Include" / "StateMachine.mqh").read_text()
recon = (root / "Include" / "ReconciliationEngine.mqh").read_text()
assert "STATE_RECOVERY_MISMATCH" in types
assert "STATE_RECOVERY_MISMATCH" in state
assert "STATE_RECOVERY_MISMATCH" in recon
print("RECOVERY_MISMATCH_STATE_CHECK PASS")
