from pathlib import Path
root = Path(__file__).resolve().parents[1]
engine = (root / "Include" / "PendingContractEngine.mqh").read_text()
state = (root / "Include" / "StateMachine.mqh").read_text()
assert "STATE_OPEN_NEW_SMALL_PENDING" in engine and "PENDING_OPEN_SMALL" in engine
big_block = state[state.index("void RetryOpenNewBig()"):state.index("void RetryOpenNewSmall()")]
small_block = state[state.index("void RetryOpenNewSmall()"):state.index("bool ValidateFSMIntegrity()")]
assert "PreparePendingOpenSmallContext()" in big_block
assert "PENDING_OPEN_SMALL prepared" in big_block
assert big_block.index("PreparePendingOpenSmallContext()") < big_block.index("SetState(STATE_OPEN_NEW_SMALL_PENDING")
assert "PreparePendingOpenSmallContext()" in small_block
assert "ValidatePendingContract(STATE_OPEN_NEW_SMALL_PENDING)" in small_block
print("PASS pending_open_small_contract_check")
