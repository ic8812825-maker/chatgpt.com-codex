from pathlib import Path
root = Path(__file__).resolve().parents[1]
recon = (root / "Include" / "ReconciliationEngine.mqh").read_text()
for token in ["bool ValidateNoOrphanManagedPositions()", "ORPHAN_MANAGED_POSITION DETECTED", "MagicNumber", "POSITION_SYMBOL", "Ticket=%I64u", "Identifier=%I64u", "Volume=%.2f", "Direction=%s", "Comment=%s"]:
    assert token in recon, token
print("ORPHAN_POSITION_DETECTION_CHECK PASS")
