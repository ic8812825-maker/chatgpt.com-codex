from pathlib import Path
root = Path(__file__).resolve().parents[1]
recon = (root / "Include" / "ReconciliationEngine.mqh").read_text()
periodic = recon[recon.index("void RunPeriodicReconciliation") :]
assert "if(State == STATE_RECOVERY_MISMATCH)" in periodic
assert "LogReconciliationRepeatWarning" in periodic and "suppressed" in recon
assert periodic.index("if(State == STATE_RECOVERY_MISMATCH)") < periodic.index("RunReconciliation()")
print("RECONCILIATION_STOPS_AFTER_FATAL_ERROR_CHECK PASS")
