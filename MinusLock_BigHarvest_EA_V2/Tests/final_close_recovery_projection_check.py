from pathlib import Path
state = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
block = state.split("void ProcessFinalClose()", 1)[1].split("void ProcessBigHarvestCloseSmall()", 1)[0]
for token in [
    "projectedBalanceAfterFinalClose",
    "projectedRecoveryPLAfterFinalClose",
    "projectedBalanceAfterFinalClose - Ctx.cycleStartBalance",
    "FINAL_CLOSE_PROFIT_FORECAST",
    "projectedRecoveryPLAfterFinalClose <= 0.0",
    "FINAL_CLOSE_STOP: projected recovery PL is not positive",
    "FINAL_CLOSE_PROFIT",
]:
    assert token in block, token
neg = block.split("if(projectedRecoveryPLAfterFinalClose <= 0.0)", 1)[1].split("LogCycleMathDetailed", 1)[0]
assert "STATE_CLOSED_PROFIT" not in neg
print("FINAL_CLOSE_RECOVERY_PROJECTION_CHECK PASS")
