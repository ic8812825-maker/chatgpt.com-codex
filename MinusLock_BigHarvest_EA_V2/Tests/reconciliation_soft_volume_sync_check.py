from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "ReconciliationEngine.mqh").read_text()
for token in ["NormalizeVolumeToStep(ctxLot)", "NormalizeVolumeToStep(snapshot.lot)", "WARNING", "RECON_TOLERANCE_USED", "VolumeMismatchToleranceLots"]:
    assert token in text
assert "MathMax(GetEffectiveLotStep(), ReserveMismatchTolerance)" not in text
assert "RECOVERABLE" not in text
assert "RECON_AUTO_SYNC_FAR_VOLUME" not in text
print("RECONCILIATION_SOFT_VOLUME_SYNC_CHECK PASS")
