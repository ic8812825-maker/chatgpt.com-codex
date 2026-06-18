from pathlib import Path
root = Path(__file__).resolve().parents[1]
config = (root / "Include" / "Config.mqh").read_text(encoding="utf-8")
assert "input bool   UseRecommended5050Preset = false;" in config
assert "if(UseRecommended5050Preset)" in config
assert "WorkSmallRatio = SmallRatio;" in config
assert "WorkCloseBigOnSmall = CloseBigOnSmall;" in config
assert "WorkRemainBigOnSmall = RemainBigOnSmall;" in config
print("RECOMMENDED_PRESET_GUARD_CHECK PASS")
