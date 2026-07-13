from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "RecoveryMath.mqh").read_text()
for token in ["CalcBigCoreLot", "CalcBigTrendLot", "CalcSmallBaseLot", "CalcSplitBigGrossLot", "ValidateRoundedSplitGeometry", "actualBigGrossLot > farLot", "actualReserveGrowthLot > farLot", "actualNewFarLot < farLot"]:
    assert token in text, token
print("PASS actual rounded split exposure helpers are present")
