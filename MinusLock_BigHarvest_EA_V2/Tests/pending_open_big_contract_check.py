from pathlib import Path
root = Path(__file__).resolve().parents[1]
engine = (root / "Include" / "PendingContractEngine.mqh").read_text()
state = (root / "Include" / "StateMachine.mqh").read_text()
assert "STATE_OPEN_NEW_BIG_PENDING" in engine and "PENDING_OPEN_BIG" in engine
block = state[state.index("void RetryOpenNewBig()"):state.index("void RetryOpenNewSmall()")]
assert "PreparePendingOpenBigContext()" in block
assert "ValidatePendingContract(STATE_OPEN_NEW_BIG_PENDING)" in block
assert block.index("PreparePendingOpenBigContext()") < block.index("SetState(STATE_OPEN_NEW_BIG_PENDING")
print("PASS pending_open_big_contract_check")
