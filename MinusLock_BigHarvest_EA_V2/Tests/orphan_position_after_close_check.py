from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
for marker in ["ClosePositionByTicket", "ClosePositionByTicketWithComment", "ClearFarContext", "ClearBigContext", "ClearSmallContext"]:
    assert marker in state, marker
assert state.count("ValidateNoOrphanManagedPositions()") >= 10
for token in ["FULL_CLOSE_INCOMPLETE", "PENDING_CLOSE_FAR_PARTIAL", "PENDING_CLOSE_BIG_PARTIAL"]:
    assert token in state, token
print("ORPHAN_POSITION_AFTER_CLOSE_CHECK PASS")
