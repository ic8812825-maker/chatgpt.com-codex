from pathlib import Path
lot = (Path(__file__).resolve().parents[1] / "Include" / "LotUtils.mqh").read_text()
recon = (Path(__file__).resolve().parents[1] / "Include" / "ReconciliationEngine.mqh").read_text()
assert "NormalizeVolumeToStep" in lot
assert "SYMBOL_VOLUME_STEP" in lot
assert "SYMBOL_VOLUME_MIN" in lot
assert "SYMBOL_VOLUME_MAX" in lot
assert "NormalizeVolumeToStep" in recon
assert "LOT_STEP_OVERRIDE_WARNING" in lot
assert "return brokerStep" in lot
print("NORMALIZE_VOLUME_TO_STEP_CHECK PASS")
