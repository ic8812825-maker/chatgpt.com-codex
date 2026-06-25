from pathlib import Path
root = Path(__file__).resolve().parents[1]
types = (root / "Include" / "Types.mqh").read_text()
pos = (root / "Include" / "PositionUtils.mqh").read_text()
recon = (root / "Include" / "ReconciliationEngine.mqh").read_text()
state = (root / "Include" / "StateMachine.mqh").read_text()
for token in ["farIdentifier", "bigIdentifier", "smallIdentifier"]:
    assert token in types and token in state
assert "POSITION_IDENTIFIER" in pos
assert "IDENTIFIER_MISMATCH" in recon
print("IDENTIFIER_RECONCILIATION_CHECK PASS")
