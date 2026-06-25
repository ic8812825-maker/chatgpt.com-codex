from pathlib import Path
root = Path(__file__).resolve().parents[1]
recon = (root / "Include" / "ReconciliationEngine.mqh").read_text()
for token in ["Ctx.initialBuyTicket", "Ctx.initialSellTicket", "Ctx.initialBuyIdentifier", "Ctx.initialSellIdentifier", "IsManagedPositionKnownToContext"]:
    assert token in recon, token
print("INITIAL_LOCK_ORPHAN_PROTECTION_CHECK PASS")
