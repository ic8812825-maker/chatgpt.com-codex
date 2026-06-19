from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
assert "PENDING_CLOSE_FAR_PARTIAL" in state
block = state.split("case PENDING_CLOSE_FAR_PARTIAL:", 1)[1].split("case PENDING_CLOSE_OLD_FAR_FULL:", 1)[0]
assert "Ctx.farLot = NormalizeLotDown(MathMax(0.0, Ctx.farLot - Ctx.retryLot));" in block
assert "Ctx.farTicket = 0" in block  # only inside min-lot cleanup
assert "Ctx.farDirection = DIR_NONE" in block  # only inside min-lot cleanup
assert "STATE_BIG_HARVEST_CHECK_FINAL" in state
assert 'SetPendingOperation(PENDING_CLOSE_FAR_PARTIAL, "BIG_HARVEST_CLOSE_FAR"' in state
assert 'StringFind(Ctx.pendingOperation' not in state
print("PARTIAL_FAR_RETRY_PRESERVES_CONTEXT_CHECK PASS")
