from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
ea = (root / "MinusLock_BigHarvest_EA.mq5").read_text()
assert "if(!ValidateNoOrphanManagedPositions())" in ea
assert "else if(!ValidateNoOrphanManagedPositions())" in ea
recover_block = state.split("void ProcessRecoveryPending()", 1)[1].split("void ProcessBigHarvest()", 1)[0]
assert "RecoverState()" in recover_block
assert "ValidateNoOrphanManagedPositions()" in recover_block
print("ORPHAN_POSITION_AFTER_RECOVER_CHECK PASS")
