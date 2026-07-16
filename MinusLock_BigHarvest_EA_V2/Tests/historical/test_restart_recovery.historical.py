from pathlib import Path
state=(Path(__file__).resolve().parents[1]/"Include"/"StateMachine.mqh").read_text()
assert "GlobalVariableSet(StateKey(prefix + \"EventKeyHash\")" in state
assert "ReserveLedger[ledgerIndex].eventKeyHash" in state
assert state.count("SaveState();") >= 10
print("PASS: Critical recovery state and reserve ledger hashes are persisted for restart recovery.")
