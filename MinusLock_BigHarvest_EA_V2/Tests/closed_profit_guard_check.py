from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
set_state = state.split("void SetState(EAState nextState, string reason)", 1)[1].split("string StateKey", 1)[0]
assert "nextState == STATE_CLOSED_PROFIT" in set_state
assert "CountManagedOpenPositions() > 0" in set_state
assert "CLOSED_PROFIT_BLOCKED: managed positions or live leg context still open" in set_state
assert "HasOpenLegContext()" in set_state
assert "VerifyFullClose" in set_state
assert "STATE_MANUAL_INTERVENTION_REQUIRED" in set_state
print("CLOSED_PROFIT_GUARD_CHECK PASS")
