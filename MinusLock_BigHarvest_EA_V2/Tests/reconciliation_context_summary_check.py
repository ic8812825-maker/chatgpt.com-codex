from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
recon = (root / "Include" / "ReconciliationEngine.mqh").read_text()
for token in ["RECONCILIATION_CONTEXT_SUMMARY", "CurrentState=%s", "ManagedPositions=%d", "KnownContext=%s", "InitialLock=%s", "Pending=%s", "Retry=%s"]:
    assert token in state, token
assert 'LogReconciliationContextSummary("RunReconciliation")' in recon
assert "RECOVERY_CONTEXT_RESTORED" in state
assert 'LogReconciliationContextSummary("RecoverState")' in state
print("RECONCILIATION_CONTEXT_SUMMARY_CHECK PASS")
