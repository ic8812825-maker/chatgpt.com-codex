from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
assert "BIG_HARVEST_REAL_RESERVE" in text
assert "HistorySelect" in text
assert "HistoryDealGetDouble" in text
assert "DEAL_POSITION_ID" in text
assert "RealBigHarvestNet" in text or "realBigHarvestNet" in text
assert "realBigHarvestNet * WorkReserveShare" in text
assert "realBigHarvestNet * WorkCloseFarShare" in text
idx_real = text.index("BIG_HARVEST_REAL_RESERVE")
idx_add = text.index("Ctx.totalReserve += reserveAdd", idx_real)
assert idx_add > idx_real
print("BIGHARVEST_REAL_RESERVE_CHECK PASS")
