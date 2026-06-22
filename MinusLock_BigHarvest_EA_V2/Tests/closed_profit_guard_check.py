from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
set_state = state.split("void SetState(EAState nextState, string reason)", 1)[1].split("string StateKey", 1)[0]
can_enter = state.split("bool CanEnterClosedProfit()", 1)[1].split("void SetState", 1)[0]
assert "nextState == STATE_CLOSED_PROFIT" in set_state
assert "CountManagedOpenPositions() == 0" in can_enter
assert "CLOSED_PROFIT_BLOCKED" in set_state
assert "HasOpenLegContext()" in can_enter
assert "VerifyFullClose" in set_state
assert "Ctx.realRecoveryPL > 0.0" in can_enter
assert "Ctx.lastCloseWasSystemClose" in can_enter
assert "IsProfitSystemCloseComment" in can_enter
assert "STATE_CLOSED_RECOVERY_LOSS" in set_state
assert "STATE_MANUAL_INTERVENTION_REQUIRED" in set_state
print("CLOSED_PROFIT_GUARD_CHECK PASS")
