from pathlib import Path
state = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text(encoding="utf-8")
for token in ["RecoverState", "SaveState", "GlobalVariableSet", "GlobalVariableGet", "STATE_RECOVERY_PENDING"]:
    assert token in state
print("RESTART_RECOVERY_STATIC_CHECK PASS")
