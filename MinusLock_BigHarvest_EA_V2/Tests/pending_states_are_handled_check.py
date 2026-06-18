from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
required = {
    "STATE_CLOSE_BIG_PENDING": "RetryCloseBig();",
    "STATE_CLOSE_SMALL_PENDING": "RetryCloseSmall();",
    "STATE_CLOSE_OLD_FAR_PENDING": "RetryCloseOldFar();",
    "STATE_CLOSE_BIG_PART_PENDING": "RetryCloseBigPart();",
    "STATE_CLOSE_NEW_FAR_PENDING": "RetryCloseNewFar();",
    "STATE_REVERSE_LIMIT_CLOSE_PENDING": "RetryReverseLimitClose();",
    "STATE_RECOVERY_PENDING": "ProcessRecoveryPending();",
}
for state, handler in required.items():
    assert f"case {state}:" in text, state
    assert handler in text, handler
assert "MaxCloseRetryAttempts" in text
assert "RetryLogIntervalSeconds" in text
assert "STATE_MANUAL_INTERVENTION_REQUIRED" in text
print("PENDING_STATES_ARE_HANDLED_CHECK PASS")
