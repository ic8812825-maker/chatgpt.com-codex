from pathlib import Path
state = (Path(__file__).parents[1] / "Include" / "StateMachine.mqh").read_text(encoding="utf-8")
for field in ("CycleId", "FarTicket", "FarIdentifier", "BigTicket", "BigIdentifier", "SmallTicket", "SmallIdentifier"):
    assert f'InspectPersistedUInt64("{field}"' in state
for field in ("FarLot", "BigLot", "SmallLot", "FarOpenPrice", "BigOpenPrice", "SmallOpenPrice", "HarvestLevel", "ReverseCycles"):
    assert f'PersistedDoubleNonZero("{field}"' in state
assert "LEGACY_CONTEXT_MALFORMED" in state
print("LEGACY_PERSISTENCE_CONTEXT_CHECK_PASS")
