from pathlib import Path
state = (Path(__file__).parents[1] / "Include" / "StateMachine.mqh").read_text(encoding="utf-8")
assert 'string roles[] = {"BigCore", "BigTrend", "SmallBase", "ReverseSmall"}' in state
assert 'InspectPersistedUInt64(roles[i] + "Ticket"' in state
assert 'InspectPersistedUInt64(roles[i] + "Identifier"' in state
assert 'PersistedDoubleNonZero("SplitGeometryActive", 0.5)' in state
assert "SPLIT_CONTEXT_MALFORMED" in state
assert 'GlobalVariableCheck(StateKey("CycleATRRaw"))' not in state[state.index("bool IsProvenCleanStart()"):state.index("bool RecoverState()")]
print("SPLIT_PERSISTENCE_CONTEXT_CHECK_PASS")
