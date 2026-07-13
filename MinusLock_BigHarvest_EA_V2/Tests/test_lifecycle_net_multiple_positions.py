from pathlib import Path
root = Path(__file__).resolve().parents[1]
types = (root / "Include" / "Types.mqh").read_text()
state = (root / "Include" / "StateMachine.mqh").read_text()
assert "struct LifecycleNetResult" in types
assert "CalculateLifecycleNetForPositionIds" in state
for token in ["DEAL_PROFIT", "DEAL_COMMISSION", "DEAL_SWAP", "DEAL_FEE", "DEAL_SYMBOL", "DEAL_MAGIC", "DEAL_POSITION_ID", "PositionIdInList"]:
    assert token in state, token
print("PASS lifecycle net supports multiple position identifiers")
