from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
promote = text.split("bool PromoteRemainingBigToNewFar()", 1)[1].split("bool TryRecoverPromotedBigAsFar", 1)[0]
body = text.split("void ProcessSmallBuildNewFar()", 1)[1].split("void ProcessSmallCheckReserve()", 1)[0]
assert "PromoteRemainingBigToNewFar()" in body
assert "Ctx.savedSmallDirection" in body or "Ctx.savedSmallDirection" in promote
assert "Ctx.savedSmallTouchPrice" in promote
assert "CurrentPriceForSmallTouch(Ctx.savedSmallDirection)" in promote
assert "CurrentPriceForSmallTouch(Ctx.smallDirection)" not in body
print("SMALL_BUILD_NEW_FAR_NO_ACTIVE_SMALL_DIRECTION_CHECK PASS")
