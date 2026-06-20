from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
body = state.split("void ProcessSmallBuildNewFar()", 1)[1].split("void ProcessSmallCheckReserve()", 1)[0]
assert "GetActualPositionVolume(Ctx.bigTicket)" in body
assert "CalcRemainBigLotOnSmall" not in body
assert "NEW_FAR_VOLUME_NOT_FOUND" in body
print("SYNTHETIC_VOLUME_FORBIDDEN_CHECK PASS")
