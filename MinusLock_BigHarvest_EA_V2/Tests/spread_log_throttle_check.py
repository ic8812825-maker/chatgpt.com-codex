from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "RiskManager.mqh").read_text()
config = (Path(__file__).resolve().parents[1] / "Include" / "Config.mqh").read_text()
assert "input int    RiskGateLogIntervalSeconds = 60" in config
for token in ["LastRiskGateLogTime", "ShouldLogRiskGateNow", "RiskGate became BLOCKED", "RiskGate became OK", "Spread blocked"]:
    assert token in text
assert text.count("Spread blocked") == 1
print("SPREAD_LOG_THROTTLE_CHECK PASS")
