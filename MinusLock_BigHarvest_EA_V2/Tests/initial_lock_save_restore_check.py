from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
for key in ["InitialBuyTicket", "InitialSellTicket", "InitialBuyIdentifier", "InitialSellIdentifier", "InitialBuyLot", "InitialSellLot", "InitialBuyOpenPrice", "InitialSellOpenPrice", "InitialLockRecovered"]:
    assert f'StateKey("{key}")' in state, key
assert "RegisterInitialLockFromSnapshots" in state
assert "INITIAL_LOCK_REGISTERED" in state
assert "INITIAL_LOCK_RECOVERED" in state
assert "STATE_INITIAL_LOCK_OPENED" in state
print("INITIAL_LOCK_SAVE_RESTORE_CHECK PASS")
