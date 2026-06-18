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

assert "Ctx.farOpenPrice = newFarOpenPrice;" in state
assert "double newFarOpenPrice = bigOpenPrice;" in state
assert "double newFarDistancePoints = CalcRealPriceFarDistancePoints(currentPrice, newFarOpenPrice);" in state
assert "double expectedNextFarLoss = CalcFarRemainLoss(newFarLot, newFarDistancePoints);" in state
assert "Ctx.effectiveFarDistancePoints = newFarDistancePoints;" in state
assert "Ctx.farOpenPrice = currentPrice;" not in state
assert "double expectedNextFarLoss = 0.0;" not in state
assert "if(!AllowRealTrading && Ctx.farLot > 0.0 && Ctx.farDirection != DIR_NONE)" not in state
assert "ROLLBACK_BIG_WITHOUT_SMALL" in state
assert "CalcSignedPositionPL(Ctx.bigDirection" in state
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

print("V2_STATIC_VALIDATION PASS: BigMove start/step formula is active, old level inputs are removed, Small-at-Far uses bigOpenPrice, reverse-risk uses real expected loss, sim records realized P/L, RefreshFar is strict, hedge/use-market/tick-log gates exist")
