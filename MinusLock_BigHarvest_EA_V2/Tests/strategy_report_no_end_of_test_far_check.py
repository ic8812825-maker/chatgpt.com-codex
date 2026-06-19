from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
config = (root / "Include" / "Config.mqh").read_text()
assert "input bool   CloseFarOnMaxLevels = true;" in config
assert "STOP_MAX_LEVELS_CLOSE_FAR" in state
assert "NOT_CLOSED: reserve insufficient and CloseFarOnMaxLevels=false" in state
assert "MaxHarvestLevels reached; residual Far closed" in state
print("STRATEGY_REPORT_NO_END_OF_TEST_FAR_CHECK PASS")
