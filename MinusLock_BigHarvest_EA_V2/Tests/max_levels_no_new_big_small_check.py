from pathlib import Path
root = Path(__file__).resolve().parents[1]
text = (root / "Include" / "StateMachine.mqh").read_text()
open_block = text.split("void OpenBigSmall()", 1)[1].split("void CheckBigOrSmallScenario()", 1)[0]
retry_big = text.split("void RetryOpenNewBig()", 1)[1].split("void RetryOpenNewSmall()", 1)[0]
assert "Ctx.harvestLevel >= WorkMaxHarvestLevels" in open_block
assert "STATE_MAX_LEVELS_DECISION" in open_block
assert "Ctx.harvestLevel >= WorkMaxHarvestLevels" in retry_big
assert "STATE_MAX_LEVELS_DECISION" in retry_big
assert "WorkMaxHarvestLevels reached" in open_block + retry_big
print("MAX_LEVELS_NO_NEW_BIG_SMALL_CHECK PASS")
