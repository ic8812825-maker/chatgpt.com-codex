from pathlib import Path
state = (Path(__file__).parents[1] / "Include" / "StateMachine.mqh").read_text(encoding="utf-8")
section = state[state.index("void EvaluatePendingPersistence"):state.index("bool IsProvenCleanStart()")]
for field in ("PendingTicket", "PendingBigPositionId", "PendingSmallPositionId"):
    assert f'InspectPersistedUInt64("{field}"' in section
for field in ("PendingRealNet", "PendingCloseFarBudget", "PendingReserveAdd", "PendingSmallReserveAdd", "PendingCloseFarLot", "PendingPartialFarBudgetAvailable", "PendingProjectedPartialFarLoss"):
    assert f'PersistedDoubleNonZero("{field}"' in section
assert "PendingActionMatchesState" in section
assert "PENDING_CONTEXT_MALFORMED" in section
print("PENDING_PERSISTENCE_CONTEXT_CHECK_PASS")
