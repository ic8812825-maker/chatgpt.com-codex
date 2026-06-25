from pathlib import Path
root = Path(__file__).resolve().parents[1]
recon = (root / "Include" / "ReconciliationEngine.mqh").read_text()
for token in ["POSITION_IDENTIFIER", "identifier == Ctx.farIdentifier", "identifier == Ctx.bigIdentifier", "identifier == Ctx.smallIdentifier", "IsManagedPositionKnownToContext"]:
    assert token in recon, token
print("ORPHAN_POSITION_IDENTIFIER_CHECK PASS")
