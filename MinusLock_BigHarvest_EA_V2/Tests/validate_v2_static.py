from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
state = (ROOT / "Include" / "StateMachine.mqh").read_text(encoding="utf-8")
sim = (ROOT / "Include" / "SimulationEngine.mqh").read_text(encoding="utf-8")
main = (ROOT / "MinusLock_BigHarvest_EA.mq5").read_text(encoding="utf-8")
config = (ROOT / "Include" / "Config.mqh").read_text(encoding="utf-8")
risk_math = (ROOT / "Include" / "RecoveryMath.mqh").read_text(encoding="utf-8")

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

print("V2_STATIC_VALIDATION PASS: Small-at-Far uses bigOpenPrice, reverse-risk uses real expected loss, sim records realized P/L, RefreshFar is strict, hedge/use-market/tick-log gates exist")
