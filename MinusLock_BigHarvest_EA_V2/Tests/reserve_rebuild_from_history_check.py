from pathlib import Path
root = Path(__file__).resolve().parents[1]
recon = (root / "Include" / "ReconciliationEngine.mqh").read_text()
config = (root / "Include" / "Config.mqh").read_text()
state = (root / "Include" / "StateMachine.mqh").read_text()
for token in ["CalculateReserveFromHistory", "HistoryDealsTotal", "RESERVE_REBUILD_SKIP_INITIAL_LOCK", "RESERVE_REBUILD_FROM_LEDGER", "ReserveMismatchTolerance", "RESERVE_REBUILD_UNVERIFIED"]:
    assert token in recon + config
assert "RebuildReserveFromLedger" in state + recon
print("RESERVE_REBUILD_FROM_HISTORY_CHECK PASS")
