from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
for token in ["CycleStartTime", "CurrentBigMovePoints", "CumulativeBigMovePoints", "InitialFarDistancePoints", "CurrentClosePrice", "SmallReverseNet", "ProjectedReserveCoverage", "ReverseStrength"]:
    assert token in text, token
for token in ["Saved State", "Recovered State", "Open Positions", "Unknown Positions", "Missing Positions", "Duplicate Positions"]:
    assert token in text, token
assert "ReconcileRecoveredPosition" in text
print("RECOVERY_RECONCILE_CHECK PASS")
