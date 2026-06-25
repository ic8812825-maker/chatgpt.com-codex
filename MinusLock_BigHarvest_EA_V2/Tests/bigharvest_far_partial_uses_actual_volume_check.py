from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
body = state.split("void ProcessBigHarvestCloseFar()", 1)[1].split("void ProcessBigHarvestCheckFinal()", 1)[0]
assert "RefreshFarVolumeFromTerminal" in body or "GetActualPositionVolume(Ctx.farTicket)" in body
assert "Ctx.farLot - Ctx.pendingCloseFarLot" not in body
assert "NormalizeLotDown(MathMax(0.0, Ctx.farLot - Ctx.pendingCloseFarLot))" not in body
print("BIGHARVEST_FAR_PARTIAL_USES_ACTUAL_VOLUME_CHECK PASS")
