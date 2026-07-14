from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "Config.mqh").read_text()
expected = [
    "input double StartLot              = 0.10;",
    "input double BigRatio              = 1.15;",
    "input double SmallRatio            = 0.25;",
    "input double CloseBigOnSmall       = 0.40;",
    "input double RemainBigOnSmall      = 0.60;",
    "input double CloseFarShare         = 0.10;",
    "input double ReserveShare          = 0.90;",
    "input double SmallReserveShare     = 0.05;",
    "input bool   UseRecommended5050Preset = false;",
    "input int    MaxReverseCycles              = 7;",
    "input double MinReverseStrength            = 0.10;",
    "input double WarningReverseStrength        = 0.15;",
    "input double StrongReverseStrength         = 0.25;",
    "input double MinProjectedReserveCoverage   = 1.00;",
    "input double LotStep               = 0.01;",
    "input double MaxSpreadPoints       = 40.0;",
    "input double MaxMarginPercent      = 60.0;",
    "input double MaxDrawdownPercent    = 25.0;",
    "input int    MaxManagedPositions   = 8;",
    "input bool   AllowRealTrading      = false;",
    "input bool   UseInternalSimulation = false;",
    "input bool   UseMarketOrders       = true;",
]
for item in expected:
    assert item in text, item
assert 1.15 * 1.15 * 0.60 < 1.0
print("DEFAULT_PARAMETERS_V241_CHECK PASS")
