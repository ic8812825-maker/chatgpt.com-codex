from pathlib import Path
root = Path(__file__).resolve().parents[1]
main = (root / "MinusLock_BigHarvest_EA.mq5").read_text()
state = (root / "Include" / "StateMachine.mqh").read_text()
on_tester = main.split("double OnTester()", 1)[1]
assert "RecalculateRealCycleStatsFromHistory();" in on_tester
assert "bool passByRealPL = IsRealRecoveryPass();" in on_tester
assert "double testerValue = passByRealPL ? Ctx.realRecoveryPL : -1.0;" in on_tester
assert "return -1.0;" in on_tester
assert "InitialDeposit" not in on_tester
pass_block = state.split("bool IsRealRecoveryPass()", 1)[1].split("void LogRealCycleMath", 1)[0]
for token in ["State == STATE_CLOSED_PROFIT", "Ctx.realRecoveryPL > 0.0", "CountManagedOpenPositions() == 0", "Ctx.lastCloseWasSystemClose", "IsProfitSystemCloseComment(Ctx.lastSystemCloseComment)"]:
    assert token in pass_block, token
print("ON_TESTER_RECOVERY_ONLY_CHECK PASS")
