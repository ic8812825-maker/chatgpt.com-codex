from pathlib import Path
state = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
block = state.split("double CalcRealRecoveryPL()", 1)[1].split("bool RecalculateRealCycleStatsFromHistory()", 1)[0]
assert "Ctx.cycleCurrentBalance = AccountInfoDouble(ACCOUNT_BALANCE);" in block
assert "Ctx.cycleBalancePL = Ctx.cycleCurrentBalance - Ctx.cycleStartBalance;" in block
assert "Ctx.realRecoveryPL = Ctx.cycleBalancePL;" in block
assert "Ctx.realRecoveryPL = Ctx.realCyclePL" not in block
assert "InitialDeposit" not in block
print("REAL_RECOVERY_PL_CYCLE_BALANCE_CHECK PASS")
