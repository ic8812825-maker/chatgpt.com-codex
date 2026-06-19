from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "ReconciliationEngine.mqh").read_text()
for token in ["NormalizeVolumeToStep(ctxLot)", "NormalizeVolumeToStep(snapshot.lot)", "RECON_AUTO_SYNC_FAR_VOLUME", "RECON WARNING", "RECOVERABLE", "RECON_TOLERANCE_USED"]:
    assert token in text
assert "MathMax(GetEffectiveLotStep(), ReserveMismatchTolerance)" in text
print("RECONCILIATION_SOFT_VOLUME_SYNC_CHECK PASS")
