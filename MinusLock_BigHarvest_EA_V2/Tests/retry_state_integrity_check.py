from pathlib import Path
engine = (Path(__file__).resolve().parents[1] / "Include" / "StateIntegrityEngine.mqh").read_text()
for token in ["INVALID_RETRY_CONTEXT", "retryCounter", "RetryStartTime", "retryTicket", "retryLot", "retryAttempts"]:
    assert token in engine
assert "IsStateIntegrityRetryState" in engine
assert "IsStateIntegrityClosePendingState" in engine
print("PASS retry_state_integrity_check")
