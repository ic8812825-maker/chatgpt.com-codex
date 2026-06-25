from pathlib import Path
root = Path(__file__).resolve().parents[1]
engine = (root / "Include" / "PositionResolutionEngine.mqh").read_text()
state = (root / "Include" / "StateMachine.mqh").read_text()
assert "POSITION_RESOLUTION_FAILED" in engine
assert "STATE_POSITION_RESOLUTION_ERROR" in engine
assert "SetState(STATE_POSITION_RESOLUTION_ERROR" in engine
assert "StateToString(STATE_POSITION_RESOLUTION_ERROR)" in state
print("PASS position_resolution_fail_check")
