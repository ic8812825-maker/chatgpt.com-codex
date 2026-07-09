from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
for token in ["CalculateRealNetForClosedPositions", "DEAL_POSITION_ID", "DEAL_MAGIC", "DEAL_SYMBOL", "DEAL_ENTRY_OUT", "DEAL_ENTRY_IN", "DEAL_ENTRY_INOUT", "DEAL_ENTRY_OUT_BY", "DEAL_FEE", "pendingBigPositionId", "pendingSmallPositionId"]:
    assert token in text, token
assert "BigLifecycleNet" in text and "SmallLifecycleNet" in text and "BigSmallNet" in text
assert "realBigHarvestNet = Ctx.realCyclePL" not in text
print("BIG_HARVEST_REAL_DEALS_CHECK PASS")
