from pathlib import Path
root = Path(__file__).resolve().parents[1]
recon = (root / "Include" / "ReconciliationEngine.mqh").read_text()
assert "CONTEXT_CLEARED_WITH_LIVE_POSITION" in recon
assert "CountManagedOpenPositions() > 0" in recon
assert "STATE_RECOVERY_MISMATCH" in recon
print("CONTEXT_CLEARED_WITH_LIVE_POSITION_CHECK PASS")
