from pathlib import Path
root = Path(__file__).resolve().parents[1]
config = (root / "Include" / "Config.mqh").read_text()
ea = (root / "MinusLock_BigHarvest_EA.mq5").read_text()
for token in ["UseSplitBigGeometry", "UseLegacySingleBigGeometry", "BigCoreRatio", "BigTrendRatio", "SmallBaseToFarRatio", "CloseBigCoreOnSmall", "RemainBigCoreOnSmall"]:
    assert token in config, token
for token in ["UseLegacySingleBigGeometry == UseSplitBigGeometry", "bigHarvestGrossRatio <= 1.0", "reserveGrowthRatio <= 1.0", "newFarCompressionRatio >= 1.0", "CloseBigCoreOnSmall + RemainBigCoreOnSmall"]:
    assert token in ea, token
print("PASS split geometry validation inputs and guards")
