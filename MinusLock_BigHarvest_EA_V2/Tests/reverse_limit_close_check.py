from pathlib import Path
state = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text(encoding="utf-8")
types = (Path(__file__).resolve().parents[1] / "Include" / "Types.mqh").read_text(encoding="utf-8")
assert "STOP_REVERSE_LIMIT_CLOSE_NEW_FAR" in state
assert "STATE_REVERSE_LIMIT_CLOSED" in types
assert "STATE_REVERSE_LIMIT_CLOSE_PENDING" in types
print("REVERSE_LIMIT_CLOSE_CHECK PASS")
