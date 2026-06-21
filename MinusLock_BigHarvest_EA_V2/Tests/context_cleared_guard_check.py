from pathlib import Path
root = Path(__file__).resolve().parents[1]
recon = (root / "Include" / "ReconciliationEngine.mqh").read_text()
assert "CONTEXT_CLEARED_WITH_LIVE_POSITION" in recon
assert "if(!HasKnownContext() && CountManagedOpenPositions() > 0)" in recon
assert "Ctx.farTicket == 0 && Ctx.bigTicket == 0 && Ctx.smallTicket == 0" not in recon
print("CONTEXT_CLEARED_GUARD_CHECK PASS")
