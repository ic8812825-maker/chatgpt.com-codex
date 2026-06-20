from pathlib import Path
root = Path(__file__).resolve().parents[1]
recon = (root / "Include" / "ReconciliationEngine.mqh").read_text()
config = (root / "Include" / "Config.mqh").read_text()
assert "GetActualFarVolume" in recon
assert "%s_VOLUME_MISMATCH" in recon
assert "VolumeMismatchToleranceLots" in recon + config
assert "RECON_TOLERANCE_USED" in recon
assert "ValidateFarPosition" in recon
assert "Ctx.farLot" in recon
assert "RECON_AUTO_SYNC_FAR_VOLUME" not in recon
print("FAR_VOLUME_RECONCILIATION_CHECK PASS")
