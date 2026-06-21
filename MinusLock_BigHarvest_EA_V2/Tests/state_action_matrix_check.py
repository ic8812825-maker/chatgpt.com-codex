from pathlib import Path
engine = (Path(__file__).resolve().parents[1] / "Include" / "PendingContractEngine.mqh").read_text()
for pair in [
    ("STATE_OPEN_NEW_BIG_PENDING", "PENDING_OPEN_BIG"),
    ("STATE_OPEN_NEW_SMALL_PENDING", "PENDING_OPEN_SMALL"),
    ("STATE_CLOSE_BIG_PENDING", "PENDING_CLOSE_BIG_FULL"),
    ("STATE_CLOSE_SMALL_PENDING", "PENDING_CLOSE_SMALL_FULL"),
    ("STATE_CLOSE_BIG_PART_PENDING", "PENDING_CLOSE_BIG_PARTIAL"),
    ("STATE_CLOSE_NEW_FAR_PENDING", "PENDING_CLOSE_FAR_PARTIAL"),
]:
    assert pair[0] in engine and pair[1] in engine
assert "PendingActionMatchesState" in engine
assert "STATE_ACTION_MISMATCH" in engine
print("PASS state_action_matrix_check")
