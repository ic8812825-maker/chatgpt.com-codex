from pathlib import Path
root = Path(__file__).resolve().parents[1]
recon = (root / "Include" / "ReconciliationEngine.mqh").read_text()
state = (root / "Include" / "StateMachine.mqh").read_text()
assert "double tolerance = VolumeMismatchToleranceLots" in recon
assert "RECON_AUTO_SYNC_FAR_VOLUME" not in recon
assert "RECOVERABLE" not in recon
assert "GetActualPositionVolume(Ctx.bigTicket)" in state
assert "FAR_VOLUME_MISMATCH" not in state
print("RECONCILIATION_VOLUME_STABILITY_CHECK PASS")
