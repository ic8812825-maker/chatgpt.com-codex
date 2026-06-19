from pathlib import Path
root = Path(__file__).resolve().parents[1]
recon = (root / "Include" / "ReconciliationEngine.mqh").read_text()
block = recon[recon.index("if(reserveDiff > ReserveMismatchTolerance)") : recon.index("ok = ValidateHarvestLevelFromHistory")]
assert "RECONCILIATION WARNING RESERVE_REBUILD_UNVERIFIED" in block
assert "STATE_RECOVERY_MISMATCH" not in block
assert "ok = false" not in block
assert "Ctx.totalReserve = realReserve" not in block
print("RESERVE_MISMATCH_NOT_FATAL_CHECK PASS")
