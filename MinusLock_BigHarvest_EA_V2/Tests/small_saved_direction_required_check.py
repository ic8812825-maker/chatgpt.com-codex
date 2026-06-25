from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
types = (root / "Include" / "Types.mqh").read_text()
for token in ["savedSmallDirection", "savedSmallClosePrice", "savedSmallTouchPrice", "savedSmallOpenPrice", "savedSmallLot"]:
    assert token in types and token in state, token
assert "Ctx.savedSmallDirection = Ctx.smallDirection" in state
assert "SMALL_BUILD_NEW_FAR FAILED: savedSmallDirection is DIR_NONE" in state
assert "SavedSmallDirection" in state and "SavedSmallTouchPrice" in state
print("SMALL_SAVED_DIRECTION_REQUIRED_CHECK PASS")
