from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
terminal_idx = text.index("case STATE_CLOSED_PROFIT:")
open_big_idx = text.index("case STATE_OPEN_NEW_BIG_PENDING:")
open_small_idx = text.index("case STATE_OPEN_NEW_SMALL_PENDING:")
assert terminal_idx < open_big_idx < open_small_idx
terminal_block = text[terminal_idx:open_big_idx]
assert "RetryOpenNewBig();" not in terminal_block
assert "RetryOpenNewSmall();" not in terminal_block
assert "case STATE_MANUAL_INTERVENTION_REQUIRED:" in terminal_block
print("TERMINAL_STATES_SEPARATED_FROM_PENDING_CHECK PASS")
