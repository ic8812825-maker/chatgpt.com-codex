from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "Config.mqh").read_text()
expected = [
    "input double BigRatio              = 1.20;",
    "input double SmallRatio            = 0.35;",
    "input double CloseBigOnSmall       = 0.35;",
    "input double RemainBigOnSmall      = 0.65;",
    "input double CloseFarShare         = 0.40;",
    "input double ReserveShare          = 0.60;",
    "input double SmallReserveShare     = 0.05;",
    "input bool   UseRecommended5050Preset = false;",
    "input int    MaxReverseCycles              = 7;",
    "input double LotStep               = 0.01;",
    "input double MaxSpreadPoints       = 60.0;",
    "input bool   AllowRealTrading      = true;",
    "input bool   UseInternalSimulation = false;",
    "input bool   UseMarketOrders       = true;",
]
for item in expected:
    assert item in text, item
assert 1.20 * 1.20 * 0.65 < 1.0
print("DEFAULT_PARAMETERS_V241_CHECK PASS")
