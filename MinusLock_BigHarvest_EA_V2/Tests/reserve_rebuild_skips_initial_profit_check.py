from pathlib import Path
root = Path(__file__).resolve().parents[1]
recon = (root / "Include" / "ReconciliationEngine.mqh").read_text()
calc = recon[recon.index("double CalculateReserveFromHistory") : recon.index("double GetActualFarVolume")]
assert "RESERVE_REBUILD_SKIP_INITIAL_LOCK" in calc
assert "INITIAL_BUY" in calc and "INITIAL_SELL" in calc
assert "RebuildReserveFromLedger()" in calc
assert "DEAL_PROFIT > 0" not in calc
assert "if(net > 0" not in calc
assert "WorkReserveShare" not in calc
print("RESERVE_REBUILD_SKIPS_INITIAL_PROFIT_CHECK PASS")
