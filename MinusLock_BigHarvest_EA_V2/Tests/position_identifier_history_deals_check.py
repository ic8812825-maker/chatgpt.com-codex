from pathlib import Path
root = Path(__file__).resolve().parents[1]
types = (root / "Include" / "Types.mqh").read_text()
pos = (root / "Include" / "PositionUtils.mqh").read_text()
state = (root / "Include" / "StateMachine.mqh").read_text()
assert "ulong identifier;" in types
assert "POSITION_IDENTIFIER" in pos
assert "pendingBigPositionId = big.identifier" in state
assert "pendingSmallPositionId = small.identifier" in state
assert "DEAL_POSITION_ID" in state
assert "pendingBigPositionId = Ctx.bigTicket" not in state
assert "pendingSmallPositionId = Ctx.smallTicket" not in state
print("POSITION_IDENTIFIER_HISTORY_DEALS_CHECK PASS")
