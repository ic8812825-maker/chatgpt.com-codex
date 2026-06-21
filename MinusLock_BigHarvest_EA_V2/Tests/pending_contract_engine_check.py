from pathlib import Path
root = Path(__file__).resolve().parents[1]
engine = (root / "Include" / "PendingContractEngine.mqh").read_text()
ea = (root / "MinusLock_BigHarvest_EA.mq5").read_text()
state = (root / "Include" / "StateMachine.mqh").read_text()
for token in ["ValidatePendingContract", "PreparePendingOpenBigContext", "PreparePendingOpenSmallContext", "PreparePendingCloseBigContext", "PreparePendingCloseSmallContext", "PreparePendingCloseFarContext", "PreparePendingFinalCloseContext"]:
    assert token in engine
for token in ["PENDING_CONTRACT_CREATED", "PENDING_CONTRACT_VALID", "PENDING_CONTRACT_INVALID", "STATE_ACTION_MISMATCH", "PENDING_CONTRACT_MISSING"]:
    assert token in engine
assert 'Include/PendingContractEngine.mqh' in ea
assert "ValidatePendingContract(EAState targetState);" in state
print("PASS pending_contract_engine_check")
