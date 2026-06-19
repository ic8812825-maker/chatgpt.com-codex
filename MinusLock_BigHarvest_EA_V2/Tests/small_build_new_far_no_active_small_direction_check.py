from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
body = text.split("void ProcessSmallBuildNewFar()", 1)[1].split("void ProcessSmallCheckReserve()", 1)[0]
assert "Ctx.savedSmallDirection" in body
assert "Ctx.savedSmallTouchPrice" in body
assert "CurrentPriceForSmallTouch(Ctx.savedSmallDirection)" in body
assert "CurrentPriceForSmallTouch(Ctx.smallDirection)" not in body
assert "Ctx.smallDirection" not in body
print("SMALL_BUILD_NEW_FAR_NO_ACTIVE_SMALL_DIRECTION_CHECK PASS")
