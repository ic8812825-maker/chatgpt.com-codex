from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
body = state.split("void SetState(EAState nextState", 1)[1].split("void MarkSystemClose", 1)[0]
assert "nextState == STATE_CLOSED_PROFIT" in body
assert "VerifyFullClose(Ctx.farTicket" in body
assert "VerifyFullClose(Ctx.bigTicket" in body
assert "VerifyFullClose(Ctx.smallTicket" in body
assert "HasOpenLegContext()" in body
assert "CLOSED_PROFIT_BLOCKED" in body
print("CLOSED_PROFIT_REQUIRES_FULL_CLOSE_CHECK PASS")
