from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
types = (root / "Include" / "Types.mqh").read_text()
for token in ["oldFarTicket", "oldFarLot", "oldFarDirection", "oldFarOpenPrice"]:
    assert token in types and token in state, token
body = state.split("void ProcessSmallCloseOldFar()", 1)[1].split("void ProcessSmallCloseBigPart()", 1)[0]
for token in ["Ctx.oldFarTicket = Ctx.farTicket", "Ctx.oldFarLot = Ctx.farLot", "Ctx.oldFarDirection = Ctx.farDirection", "Ctx.oldFarOpenPrice = Ctx.farOpenPrice"]:
    assert token in body, token
for token in ["Ctx.farTicket = 0", "Ctx.farLot = 0.0", "Ctx.farDirection = DIR_NONE", "Ctx.farOpenPrice = 0.0"]:
    assert token in body, token
assert "OldFarTicket" in state and "OldFarOpenPrice" in state
print("OLD_FAR_CLEANUP_AFTER_CLOSE_CHECK PASS")
