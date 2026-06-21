from pathlib import Path
state = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
block = state[state.index("void RetryOpenNewBig()"):state.index("void RetryOpenNewSmall()")]
assert "ResolveOpenedPositionAfterOpen" in block
assert "ApplyResolvedPositionToBig" in block
assert "Ctx.bigLot = Ctx.pendingLot" not in block
assert "Ctx.bigTicket = opened.ticket" not in block
assert block.index("ApplyResolvedPositionToBig") < block.index("PreparePendingOpenSmallContext()")
print("PASS retry_open_big_resolution_check")
