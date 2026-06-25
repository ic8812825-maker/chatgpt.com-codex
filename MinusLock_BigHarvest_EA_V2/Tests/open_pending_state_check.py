from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
assert "case STATE_OPEN_NEW_BIG_PENDING:" in text and "RetryOpenNewBig();" in text
assert "case STATE_OPEN_NEW_SMALL_PENDING:" in text and "RetryOpenNewSmall();" in text
print("OPEN_PENDING_STATE_CHECK PASS")
