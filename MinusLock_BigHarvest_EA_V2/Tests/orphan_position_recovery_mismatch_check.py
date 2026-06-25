from pathlib import Path
root = Path(__file__).resolve().parents[1]
recon = (root / "Include" / "ReconciliationEngine.mqh").read_text()
body = recon.split("bool ValidateNoOrphanManagedPositions()", 1)[1].split("bool RunReconciliation()", 1)[0]
assert "SetState(STATE_RECOVERY_MISMATCH" in body
assert "ORPHAN_MANAGED_POSITION detected by ValidateNoOrphanManagedPositions" in body
print("ORPHAN_POSITION_RECOVERY_MISMATCH_CHECK PASS")
