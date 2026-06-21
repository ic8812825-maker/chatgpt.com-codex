from pathlib import Path
engine = (Path(__file__).resolve().parents[1] / "Include" / "StateIntegrityEngine.mqh").read_text()
for token in ["INVALID_PENDING_CONTEXT", "pendingActionType", "pendingTicket", "pendingNextState", "pendingLot", "retryTicket", "retryLot"]:
    assert token in engine
for state in ["STATE_CLOSE_BIG_PENDING", "STATE_CLOSE_SMALL_PENDING", "STATE_CLOSE_NEW_FAR_PENDING", "STATE_OPEN_NEW_BIG_PENDING", "STATE_OPEN_NEW_SMALL_PENDING"]:
    assert state in engine
assert "IsStateIntegrityPendingState" in engine
print("PASS pending_state_integrity_check")
