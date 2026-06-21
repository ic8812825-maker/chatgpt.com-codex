from pathlib import Path
root = Path(__file__).resolve().parents[1]
recon = (root / "Include" / "ReconciliationEngine.mqh").read_text()
for token in ["bool ValidateInitialLockIntegrity()", "ValidateInitialLockLeg", "INITIAL_LOCK_IDENTIFIER_MISMATCH", "INITIAL_LOCK_TICKET_MISMATCH", "INITIAL_LOCK_STATE_VALID", "INITIAL_LOCK_STATE_INVALID"]:
    assert token in recon, token
assert "ValidateInitialLockIntegrity() && ok" in recon
print("INITIAL_LOCK_RECONCILIATION_CHECK PASS")
