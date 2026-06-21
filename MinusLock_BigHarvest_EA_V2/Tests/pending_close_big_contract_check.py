from pathlib import Path
root = Path(__file__).resolve().parents[1]
engine = (root / "Include" / "PendingContractEngine.mqh").read_text()
state = (root / "Include" / "StateMachine.mqh").read_text()
assert "STATE_CLOSE_BIG_PENDING" in engine and "PENDING_CLOSE_BIG_FULL" in engine
assert "PreparePendingCloseBigContext" in engine
assert "ticket must equal Big" in engine
assert "SetPendingOperation(PENDING_CLOSE_BIG_FULL" in state
print("PASS pending_close_big_contract_check")
