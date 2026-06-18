from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "Types.mqh").read_text(encoding="utf-8")
for token in [
    "STATE_CLOSE_BIG_PENDING", "STATE_CLOSE_SMALL_PENDING", "STATE_CLOSE_OLD_FAR_PENDING",
    "STATE_CLOSE_BIG_PART_PENDING", "STATE_CLOSE_NEW_FAR_PENDING", "STATE_OPEN_NEW_BIG_PENDING",
    "STATE_OPEN_NEW_SMALL_PENDING", "STATE_RECOVERY_PENDING", "STATE_MANUAL_INTERVENTION_REQUIRED",
]:
    assert token in text
print("RETRY_FSM_STATIC_CHECK PASS")
