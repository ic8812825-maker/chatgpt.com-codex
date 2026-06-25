from pathlib import Path
root = Path(__file__).resolve().parents[1]
types = (root / "Include" / "Types.mqh").read_text()
state = (root / "Include" / "StateMachine.mqh").read_text()
for token in ["pendingReserveApplied", "pendingSmallReserveApplied", "pendingSmallReserveAdd"]:
    assert token in types and token in state
assert "if(!Ctx.pendingReserveApplied)" in state
assert "if(!Ctx.pendingSmallReserveApplied)" in state
assert "PendingReserveApplied" in state and "PendingSmallReserveApplied" in state
print("RESERVE_APPLY_ONCE_CHECK PASS")
