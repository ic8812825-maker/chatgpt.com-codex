from pathlib import Path
state = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
block = state[state.index("void RetryOpenNewSmall()"):state.index("bool ValidateFSMIntegrity()")]
assert "ResolveOpenedPositionAfterOpen" in block
assert "ApplyResolvedPositionToSmall" in block
assert "Ctx.smallLot = Ctx.pendingLot" not in block
assert "Ctx.smallTicket = opened.ticket" not in block
assert block.index("ApplyResolvedPositionToSmall") < block.index("SetState(STATE_BIG_SMALL_OPENED")
print("PASS retry_open_small_resolution_check")
