from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
for forbidden in [
    "Ctx.farLot - Ctx.pendingCloseFarLot",
    "Ctx.farLot - Ctx.retryLot",
    "Ctx.bigLot - Ctx.pendingCloseBigLot",
    "Ctx.bigLot - Ctx.retryLot",
    "NormalizeLotDown(MathMax(0.0, Ctx.farLot -",
    "NormalizeLotDown(MathMax(0.0, Ctx.bigLot -",
]:
    assert forbidden not in state
assert "RefreshFarVolumeFromTerminal" in state
assert "RefreshBigVolumeFromTerminal" in state
print("PARTIAL_CLOSE_NO_THEORETICAL_LOT_SUBTRACTION_CHECK PASS")
