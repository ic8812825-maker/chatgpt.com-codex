from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
assert "ClearClosedLegAfterRetry" in text
for token in ["Ctx.smallTicket = 0", "Ctx.smallLot = 0.0", "Ctx.smallDirection = DIR_NONE", "Ctx.smallOpenPrice = 0.0",
              "Ctx.bigTicket = 0", "Ctx.bigLot = 0.0", "Ctx.bigDirection = DIR_NONE", "Ctx.bigOpenPrice = 0.0",
              "Ctx.farTicket = 0", "Ctx.farLot = 0.0", "Ctx.farDirection = DIR_NONE", "Ctx.farOpenPrice = 0.0"]:
    assert token in text, token
assert "ClearClosedLegAfterRetry();" in text
print("RETRY_CONTEXT_CLEANUP_CHECK PASS")
