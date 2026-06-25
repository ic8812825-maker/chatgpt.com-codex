from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
assert "ApplyPendingCloseSuccessToContext" in text
assert "ClearPendingOperationContext" in text
assert "switch(Ctx.pendingActionType)" in text
for leg in ["Ctx.bigTicket = 0", "Ctx.smallTicket = 0", "Ctx.farTicket = 0"]:
    assert leg in text
assert "StringFind(Ctx.pendingOperation" not in text
print("RETRY_CONTEXT_CLEANUP_CHECK PASS")
