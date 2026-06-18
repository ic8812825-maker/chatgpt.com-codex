from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
types = (Path(__file__).resolve().parents[1] / "Include" / "Types.mqh").read_text()
assert "pendingDirection" in types and "pendingComment" in types
for fn in ["void RetryOpenNewBig()", "void RetryOpenNewSmall()"]:
    assert fn in text
assert "OpenPosition(Ctx.pendingDirection, Ctx.pendingLot, Ctx.pendingComment)" in text
assert "STATE_OPEN_NEW_BIG_PENDING" in text and "STATE_OPEN_NEW_SMALL_PENDING" in text
assert "SetState(STATE_FAR_ACTIVE" not in text.split("void RetryOpenNewBig()",1)[1].split("void RetryOpenNewSmall()",1)[0]
print("OPEN_PENDING_RETRY_CHECK PASS")
