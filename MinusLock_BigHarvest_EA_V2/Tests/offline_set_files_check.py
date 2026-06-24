from pathlib import Path
root = Path(__file__).resolve().parents[1]
for name in ["USDJPY_M30_SAFE.set", "USDJPY_M30_BALANCED.set", "USDJPY_M30_LOWLOT_SAFE.set"]:
    text = (root / "Sets" / name).read_text()
    for token in ["StartLot=", "BigRatio=", "SmallRatio=", "CloseBigOnSmall=", "RemainBigOnSmall=", "AllowRealTrading=true", "UseInternalSimulation=false", "UseMarketOrders=true"]:
        assert token in text, (name, token)
aggressive_set = root / "Sets" / "USDJPY_M30_AGGRESSIVE.set"
if aggressive_set.exists():
    text = aggressive_set.read_text()
    assert "StartLot=" in text and "AllowRealTrading=true" in text
else:
    assert (root / "Sets" / "USDJPY_M30_AGGRESSIVE_NOT_FOUND.txt").exists()
print("OFFLINE_SET_FILES_CHECK PASS")
