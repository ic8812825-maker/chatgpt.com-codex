from pathlib import Path
root = Path(__file__).resolve().parents[1]
recon = (root / "Include" / "ReconciliationEngine.mqh").read_text()
config = (root / "Include" / "Config.mqh").read_text()
for token in ["CalculateReserveFromHistory", "HistoryDealsTotal", "HistoryDealGetDouble", "DEAL_PROFIT", "DEAL_COMMISSION", "DEAL_SWAP", "ReserveMismatchTolerance", "RESERVE_MISMATCH"]:
    assert token in recon + config
print("RESERVE_REBUILD_FROM_HISTORY_CHECK PASS")
