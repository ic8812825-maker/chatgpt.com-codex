from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
for token in ["CalculateRealNetForClosedPositions", "DEAL_POSITION_ID", "DEAL_MAGIC", "DEAL_SYMBOL", "DEAL_ENTRY_OUT", "pendingBigPositionId", "pendingSmallPositionId"]:
    assert token in text, token
assert "RealClosedBigProfit" in text and "RealClosedSmallProfit" in text
assert "realBigHarvestNet = Ctx.realCyclePL" not in text
print("BIG_HARVEST_REAL_DEALS_CHECK PASS")
