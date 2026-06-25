from pathlib import Path
root = Path(__file__).resolve().parents[1]
engine = (root / "Include" / "PendingContractEngine.mqh").read_text()
state = (root / "Include" / "StateMachine.mqh").read_text()
assert "STATE_CLOSE_SMALL_PENDING" in engine and "PENDING_CLOSE_SMALL_FULL" in engine
assert "PreparePendingCloseSmallContext" in engine
assert "ticket must equal Small" in engine
assert "SetPendingOperation(PENDING_CLOSE_SMALL_FULL" in state
print("PASS pending_close_small_contract_check")
