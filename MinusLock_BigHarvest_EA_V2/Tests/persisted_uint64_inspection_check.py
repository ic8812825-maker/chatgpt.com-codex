from pathlib import Path

root = Path(__file__).parents[1]
types = (root / "Include" / "Types.mqh").read_text(encoding="utf-8")
state = (root / "Include" / "StateMachine.mqh").read_text(encoding="utf-8")

for value in ("ABSENT", "ZERO", "ACTIVE", "MALFORMED"):
    assert f"PERSISTED_UINT64_{value}" in types
assert "struct PersistedUInt64Inspection" in types
assert "bool InspectPersistedUInt64(" in state
assert "result.highExists != result.lowExists" in state
assert "RestoreUlong64(result.highValue, result.lowValue)" in state
assert "RECOVERY_CONTEXT_RESET_FORBIDDEN" in state
print("PERSISTED_UINT64_INSPECTION_CHECK_PASS")
