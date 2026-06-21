from pathlib import Path
state = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
block = state[state.index("void RetryOpenNewBig()"):state.index("void RetryOpenNewSmall()")]
assert "PreparePendingOpenSmallContext()" in block
assert "PENDING_OPEN_SMALL prepared" in block
assert block.index("PreparePendingOpenSmallContext()") < block.index("SetState(STATE_OPEN_NEW_SMALL_PENDING")
assert "PENDING_OPEN_SMALL" in (Path(__file__).resolve().parents[1] / "Include" / "PendingContractEngine.mqh").read_text()
print("PASS open_new_small_pending_context_check")
