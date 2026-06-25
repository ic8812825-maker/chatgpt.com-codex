from pathlib import Path
root = Path(__file__).resolve().parents[1]
types = (root / "Include" / "Types.mqh").read_text()
state = (root / "Include" / "StateMachine.mqh").read_text()
for token in ["enum PendingActionType", "PENDING_CLOSE_FAR_PARTIAL", "PENDING_MAX_LEVELS_FINAL_CLOSE", "PENDING_STOP_MAX_LEVELS_CLOSE", "PendingActionType pendingActionType"]:
    assert token in types
assert "StringFind(Ctx.pendingOperation" not in state
assert "switch(Ctx.pendingActionType)" in state
print("PENDING_ACTION_TYPE_CHECK PASS")
