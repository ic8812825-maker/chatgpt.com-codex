from pathlib import Path
state = (Path(__file__).parents[1] / "Include" / "StateMachine.mqh").read_text(encoding="utf-8")
section = state[state.index("void EvaluateFrozenGeometryPersistence"):state.index("bool IsProvenCleanStart()")]
assert "GeometryMode != GEOMETRY_MANUAL" in section
assert 'PersistedDoubleNonZero("GeometryReady", 0.5)' in section
assert 'PersistedDoubleNonZero("GeometryCalculatedTime")' in section
assert 'PersistedDoubleNonZero("CycleATRRaw")' in section
assert "ready && (!cycleActive || !calculated || !levelsReady)" in section
assert "FROZEN_GEOMETRY_CONTEXT_MALFORMED" in section
print("FROZEN_GEOMETRY_PERSISTENCE_CHECK_PASS")
