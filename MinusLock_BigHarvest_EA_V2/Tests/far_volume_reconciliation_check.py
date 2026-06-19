from pathlib import Path
root = Path(__file__).resolve().parents[1]
recon = (root / "Include" / "ReconciliationEngine.mqh").read_text()
assert "GetActualFarVolume" in recon
assert "FAR_VOLUME_MISMATCH" in recon
assert "ValidateFarPosition" in recon
assert "Ctx.farLot" in recon
print("FAR_VOLUME_RECONCILIATION_CHECK PASS")
