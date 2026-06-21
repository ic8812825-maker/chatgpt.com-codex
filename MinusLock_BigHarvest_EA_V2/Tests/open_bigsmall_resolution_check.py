from pathlib import Path
state = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
block = state[state.index("void OpenBigSmall()"):state.index("void CheckBigOrSmallScenario()")]
assert "ResolveOpenedPositionAfterOpen(bigComment" in block
assert "ApplyResolvedPositionToBig" in block
assert "ResolveOpenedPositionAfterOpen(smallComment" in block
assert "ApplyResolvedPositionToSmall" in block
assert "Ctx.bigTicket = 0" not in block
assert "Ctx.smallTicket = 0" not in block
print("PASS open_bigsmall_resolution_check")
