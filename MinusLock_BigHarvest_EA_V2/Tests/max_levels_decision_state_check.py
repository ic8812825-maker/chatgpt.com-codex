from pathlib import Path
root = Path(__file__).resolve().parents[1]
types = (root / "Include" / "Types.mqh").read_text()
state = (root / "Include" / "StateMachine.mqh").read_text()
assert "STATE_MAX_LEVELS_DECISION" in types
assert "STATE_MAX_LEVELS_DECISION" in state
assert "ProcessMaxLevelsDecision" in state
assert "[MAX_LEVELS_DECISION]" in state
print("MAX_LEVELS_DECISION_STATE_CHECK PASS")
