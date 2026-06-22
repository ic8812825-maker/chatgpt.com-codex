from pathlib import Path
root = Path(__file__).resolve().parents[1]
types = (root / "Include" / "Types.mqh").read_text()
state = (root / "Include" / "StateMachine.mqh").read_text()
integrity = (root / "Include" / "StateIntegrityEngine.mqh").read_text()
assert "STATE_CLOSED_RECOVERY_LOSS" in types
assert 'case STATE_CLOSED_RECOVERY_LOSS: return "STATE_CLOSED_RECOVERY_LOSS";' in types
set_state = state.split("void SetState(EAState nextState, string reason)", 1)[1].split("string StateKey", 1)[0]
assert "STATE_CLOSED_RECOVERY_LOSS" in set_state
assert "realRecoveryPL <= 0" in set_state
assert "STATE_CLOSED_RECOVERY_LOSS" in integrity.split("bool IsStateIntegrityTerminalState", 1)[1].split("bool IsStateIntegrityPendingState", 1)[0]
print("CLOSED_RECOVERY_LOSS_STATE_CHECK PASS")
