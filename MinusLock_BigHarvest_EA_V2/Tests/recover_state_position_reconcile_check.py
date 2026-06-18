from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
pos = (Path(__file__).resolve().parents[1] / "Include" / "PositionUtils.mqh").read_text()
for token in ["CycleId", "InitialProfitIgnored", "EffectiveFarDistancePoints", "CycleStartBalance", "RealCyclePL", "FinalCloseAllowed", "LastRetryState", "RetryTicket", "RetryLot", "RetryAttempts"]:
    assert token in text
assert "ReconcileRecoveredPosition" in text
assert "GetManagedPositionByTicket" in text
assert "GetManagedPositionByComment" in text
assert "POSITION_IDENTIFIER" in text
assert "STATE_RECOVERY_PENDING" in text and "STATE_MANUAL_INTERVENTION_REQUIRED" in text
assert "Managed positions found" in text
assert "Symbol" in text and "MagicNumber" in text and "OpenPrice" in text
print("RECOVER_STATE_POSITION_RECONCILE_CHECK PASS")
