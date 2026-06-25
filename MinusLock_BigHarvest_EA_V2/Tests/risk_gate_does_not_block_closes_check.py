from pathlib import Path
root = Path(__file__).resolve().parents[1]
ea = (root / "MinusLock_BigHarvest_EA.mq5").read_text()
sm = (root / "Include" / "StateMachine.mqh").read_text()
assert "if(!riskOk && AllowRealTrading && StopOnRiskGateBlocked)" not in ea
assert "Ctx.riskGateOk = riskOk" in ea
assert "RunStateMachine();" in ea
assert "OpenInitialLock blocked" in sm and "OpenBigSmall blocked" in sm
assert "RiskGate blocks only new openings" in sm
assert "ProcessFinalClose" in sm and "MaxSpreadPoints" not in sm
print("RISK_GATE_DOES_NOT_BLOCK_CLOSES_CHECK PASS")
