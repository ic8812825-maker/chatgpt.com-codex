from pathlib import Path
root = Path(__file__).resolve().parents[1]
config = (root / "Include" / "Config.mqh").read_text(encoding="utf-8")
state = (root / "Include" / "StateMachine.mqh").read_text(encoding="utf-8")
types = (root / "Include" / "Types.mqh").read_text(encoding="utf-8")
assert "CloseAllOnInvalidGeometry" in config
assert "CloseAllManagedPositionsWithComment" in state
assert "HandleInvalidGeometry" in state
assert "STATE_INVALID_GEOMETRY_CLOSED" in types
assert "STATE_MANUAL_INTERVENTION_REQUIRED" in types
print("INVALID_GEOMETRY_EMERGENCY_CHECK PASS")
