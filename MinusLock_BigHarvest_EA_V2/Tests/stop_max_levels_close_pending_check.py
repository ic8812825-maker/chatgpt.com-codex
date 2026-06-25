from pathlib import Path
root = Path(__file__).resolve().parents[1]
text = (root / "Include" / "StateMachine.mqh").read_text()
types = (root / "Include" / "Types.mqh").read_text()
assert "STATE_STOP_MAX_LEVELS_CLOSE_PENDING" in types
assert "RetryStopMaxLevelsClose" in text
assert "STOP_MAX_LEVELS_CLOSE_FAR" in text
assert "case STATE_STOP_MAX_LEVELS_CLOSE_PENDING:" in text
assert "STATE_STOP_MAX_LEVELS" in text
print("STOP_MAX_LEVELS_CLOSE_PENDING_CHECK PASS")
