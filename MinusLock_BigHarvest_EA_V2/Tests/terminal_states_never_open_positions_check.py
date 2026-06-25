from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
block = text.split("case STATE_CLOSED_PROFIT:", 1)[1].split("case STATE_OPEN_NEW_BIG_PENDING:", 1)[0]
for forbidden in ["RetryOpenNewBig", "RetryOpenNewSmall", "OpenBigSmall", "OpenInitialLock"]:
    assert forbidden not in block, forbidden
assert "case STATE_STOP:" in block and "case STATE_ERROR:" in block
assert "break;" in block
print("TERMINAL_STATES_NEVER_OPEN_POSITIONS_CHECK PASS")
