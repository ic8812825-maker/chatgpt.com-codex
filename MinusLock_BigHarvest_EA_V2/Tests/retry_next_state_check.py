from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
types = (Path(__file__).resolve().parents[1] / "Include" / "Types.mqh").read_text()
for token in ["pendingOperation", "pendingNextState", "pendingTicket", "pendingLot", "pendingAttempts"]:
    assert token in types and token in text
assert "SetPendingOperation" in text
assert "SetState(nextState" in text
assert "continuing with" in text
assert 'RetryCloseTicket("RetryCloseBig", "RETRY_CLOSE_BIG", Ctx.pendingNextState)' in text
print("RETRY_NEXT_STATE_CHECK PASS")
