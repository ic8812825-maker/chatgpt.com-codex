from pathlib import Path
root = Path(__file__).resolve().parents[1]
text = (root / "Include" / "StateMachine.mqh").read_text()
block = text.split("void ProcessMaxLevelsDecision()", 1)[1].split("void RetryStopMaxLevelsClose()", 1)[0]
assert "ClosePositionByTicketWithComment" in block
assert "if(!Ctx.riskGateOk" not in block
assert "LogRiskGateBlocked" not in block
print("RISK_GATE_DOES_NOT_BLOCK_MAX_LEVELS_CLOSE_CHECK PASS")
