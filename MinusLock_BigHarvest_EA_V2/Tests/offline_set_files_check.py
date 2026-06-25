from pathlib import Path
root = Path(__file__).resolve().parents[1]
sets = root / "Sets"
for category in ["SAFE", "BALANCED", "AGGRESSIVE", "LOWLOT_SAFE"]:
    set_path = sets / f"USDJPY_M30_{category}.set"
    marker_path = sets / f"USDJPY_M30_{category}_NOT_FOUND.txt"
    assert set_path.exists() or marker_path.exists(), category
    assert not (set_path.exists() and marker_path.exists()), category
    if set_path.exists():
        text = set_path.read_text()
        for token in ["StartLot=", "BigRatio=", "SmallRatio=", "CloseBigOnSmall=", "RemainBigOnSmall=", "AllowRealTrading=true", "UseInternalSimulation=false", "UseMarketOrders=true"]:
            assert token in text, (category, token)
    else:
        assert f"{category}_NOT_FOUND" in marker_path.read_text(), category
print("OFFLINE_SET_FILES_CHECK PASS")
