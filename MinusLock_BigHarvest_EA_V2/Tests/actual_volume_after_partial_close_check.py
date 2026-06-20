from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
body = state.split("void ProcessSmallCloseBigPart()", 1)[1].split("void ProcessSmallBuildNewFar()", 1)[0]
assert "GetActualPositionVolume(Ctx.bigTicket)" in body
assert "BIG_PARTIAL_CLOSE_VERIFY" in body
assert "ExpectedRemaining" in body and "ActualRemaining" in body and "Difference" in body
assert "Ctx.bigLot = actualRemaining" in body
print("ACTUAL_VOLUME_AFTER_PARTIAL_CLOSE_CHECK PASS")
