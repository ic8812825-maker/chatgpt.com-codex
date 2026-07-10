from pathlib import Path
state = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
block = state.split("void ProcessFinalClose()", 1)[1].split("void ProcessBigHarvestCloseSmall()", 1)[0]
for token in [
    "projectedBalanceAfterFinalClose",
    "projectedRecoveryPLAfterFinalClose",
    "projectedBalanceAfterFinalClose - Ctx.cycleStartBalance",
    "FINAL_CLOSE_PROFIT_FORECAST",
    "projectedRecoveryPLAfterFinalClose < MinimumRecoveryProfitMoney",
    "Ctx.totalReserve < farRemainLoss + SafetyBufferMoney",
    "FINAL_CLOSE_STOP: reserve or projected recovery PL is below minimum",
    "FINAL_CLOSE_PROFIT",
]:
    assert token in block, token
neg = block.split("if(projectedRecoveryPLAfterFinalClose < MinimumRecoveryProfitMoney", 1)[1].split("LogCycleMathDetailed", 1)[0]
assert "STATE_CLOSED_PROFIT" not in neg
print("FINAL_CLOSE_RECOVERY_PROJECTION_CHECK PASS")
