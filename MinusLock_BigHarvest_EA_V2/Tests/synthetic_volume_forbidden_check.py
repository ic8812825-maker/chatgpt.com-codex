from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
promote = state.split("bool PromoteRemainingBigToNewFar()", 1)[1].split("bool TryRecoverPromotedBigAsFar", 1)[0]
body = state.split("void ProcessSmallBuildNewFar()", 1)[1].split("void ProcessSmallCheckReserve()", 1)[0]
assert "GetActualPositionVolume(remainingBig.ticket)" in promote
assert "CalcRemainBigLotOnSmall" not in body and "CalcRemainBigLotOnSmall" not in promote
assert "PROMOTE_REMAINING_BIG_TO_FAR_FAILED" in promote and "PromoteRemainingBigToNewFar()" in body
print("SYNTHETIC_VOLUME_FORBIDDEN_CHECK PASS")
