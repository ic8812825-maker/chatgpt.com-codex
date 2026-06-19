from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
state = (ROOT / "Include" / "StateMachine.mqh").read_text(encoding="utf-8")
sim = (ROOT / "Include" / "SimulationEngine.mqh").read_text(encoding="utf-8")
main = (ROOT / "MinusLock_BigHarvest_EA.mq5").read_text(encoding="utf-8")
config = (ROOT / "Include" / "Config.mqh").read_text(encoding="utf-8")
risk_math = (ROOT / "Include" / "RecoveryMath.mqh").read_text(encoding="utf-8")
docs_text = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "Docs").glob("*.md"))

old_big_move_params = tuple("BigMoveLevel" + suffix for suffix in ("1", "2", "3"))
for token in old_big_move_params:
    assert token not in config
    assert token not in risk_math
    assert token not in docs_text

assert "BigMoveStartPoints" in config
assert "BigMoveStepPoints" in config
assert "BigMoveStartPoints + (level - 1) * BigMoveStepPoints" in risk_math
assert "L(level) = BigMoveStartPoints + (level - 1) * BigMoveStepPoints" in docs_text

assert "Ctx.farOpenPrice = Ctx.bigOpenPrice;" in state
assert "Ctx.effectiveFarDistancePoints = CalcRealPriceFarDistancePoints(currentPrice, Ctx.farOpenPrice);" in state
assert "double expectedNextFarLoss = CalcFarRemainLoss(newFarLot, Ctx.effectiveFarDistancePoints);" in state
assert "Ctx.farOpenPrice = currentPrice;" not in state
assert "double expectedNextFarLoss = 0.0;" not in state
assert "if(!AllowRealTrading && Ctx.farLot > 0.0 && Ctx.farDirection != DIR_NONE)" not in state
assert "ROLLBACK_BIG_WITHOUT_SMALL" in state
assert "SimClosedDeals" in sim
assert "SimRecordClosedDeal" in sim
assert "SimRecalculateClosedStats" in sim
assert "ACCOUNT_MARGIN_MODE_RETAIL_HEDGING" in main
assert "INIT_PARAMETERS_INCORRECT" in main
assert "VerboseTickLogs" in config and "if(VerboseTickLogs)" in main
assert "reason = \"ExpectedNextFarLoss <= 0\";" in risk_math

for token in [
    "SmallReserveShare", "MaxSlippagePoints", "MaxDrawdownPercent", "MaxManagedPositions",
    "StopOnRiskGateBlocked", "CloseAllOnInvalidGeometry", "UseInternalSimulation",
]:
    assert token in config

for token in ["ValidateRiskCompression", "CalcSmallReserveAdd", "CalcRealFarLossMoney"]:
    assert token in risk_math

for token in ["RecoverState", "SaveState", "STOP_REVERSE_LIMIT_CLOSE_NEW_FAR", "ROLLBACK_INITIAL_BUY_WITHOUT_SELL", "SMALL_RESERVE_ADD"]:
    assert token in state


for token in [
    "RiskGateLogIntervalSeconds", "MaxCloseRetryAttempts", "RetryLogIntervalSeconds",
    "Ctx.riskGateOk = riskOk", "OpenInitialLock blocked", "OpenBigSmall blocked",
    "RetryCloseBig();", "RetryCloseSmall();", "RetryCloseOldFar();", "RetryCloseBigPart();", "RetryCloseNewFar();",
    "BIG_HARVEST_REAL_RESERVE", "DEAL_POSITION_ID", "ReconcileRecoveredPosition", "STATE_MAX_LEVELS_DECISION", "CloseFarOnMaxLevels", "STOP_MAX_LEVELS_CLOSE_FAR",
]:
    assert token in (config + main + state)

assert "if(!riskOk && AllowRealTrading && StopOnRiskGateBlocked)" not in main
assert "input double MaxSpreadPoints       = 60.0;" in config
assert "input double CloseFarShare         = 0.40;" in config
assert "input double ReserveShare          = 0.60;" in config
assert "input int    MaxReverseCycles              = 7;" in config


for token in [
    "STATE_BIG_HARVEST_CLOSE_BIG", "STATE_BIG_HARVEST_CLOSE_SMALL", "STATE_BIG_HARVEST_CALC_NET", "STATE_BIG_HARVEST_CLOSE_FAR", "STATE_BIG_HARVEST_CHECK_FINAL",
    "STATE_SMALL_CLOSE_SMALL", "STATE_SMALL_CLOSE_OLD_FAR", "STATE_SMALL_CLOSE_BIG_PART", "STATE_SMALL_BUILD_NEW_FAR", "STATE_SMALL_CHECK_RESERVE",
    "pendingOperation", "pendingNextState", "SetPendingOperation", "CalculateRealNetForClosedPositions",
    "smallScenarioRealAfter - Ctx.smallScenarioRealBefore", "RetryOpenNewBig", "RetryOpenNewSmall",
]:
    assert token in (config + main + state)
assert "Ctx.realCyclePL - totalReserveBefore" not in state

print("V2_STATIC_VALIDATION PASS: BigMove start/step formula is active, old level inputs are removed, Small-at-Far uses bigOpenPrice, reverse-risk uses real expected loss, sim records realized P/L, RefreshFar is strict, hedge/use-market/tick-log gates exist")
