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
assert "Ctx.pendingReserveAdd = realBigHarvestNet * WorkReserveShare" in text
idx_add = text.index("ApplyReserveCredit(RESERVE_EVENT_BIG_HARVEST_ADD, Ctx.pendingReserveAdd)", idx_real)
assert idx_add > idx_real
assert "Ctx.totalReserve += Ctx.pendingReserveAdd" not in text
print("BIGHARVEST_REAL_RESERVE_CHECK PASS")
