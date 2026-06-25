from pathlib import Path
root = Path(__file__).resolve().parents[1]
recon = (root / "Include" / "ReconciliationEngine.mqh").read_text()
main = (root / "MinusLock_BigHarvest_EA.mq5").read_text()
for token in ["ValidateFarPosition", "ValidateBigPosition", "ValidateSmallPosition", "RunReconciliation", "RunPeriodicReconciliation", "RECONCILIATION PASS", "RECONCILIATION FAIL"]:
    assert token in recon
assert '#include "Include/ReconciliationEngine.mqh"' in main
assert "RunReconciliation()" in main
print("RECONCILIATION_ENGINE_STATIC_CHECK PASS")
