from pathlib import Path
state = (Path(__file__).parents[1] / "Include" / "StateMachine.mqh").read_text(encoding="utf-8")
section = state[state.index("void EvaluateRetryPersistence"):state.index("bool IsProvenCleanStart()")]
assert 'InspectPersistedUInt64("RetryTicket"' in section
for field in ("RetryLot", "RetryAttempts", "LastRetryState", "PendingActionType"):
    assert f'StateKey("{field}")' in section
assert "lotActive != ticketActive" in section
assert "IsPendingContractState(retryState)" in section
assert "PendingActionMatchesState(retryState, action)" in section
assert "RETRY_CONTEXT_MALFORMED" in section
print("RETRY_PERSISTENCE_CONTEXT_COMPLETE_CHECK_PASS")
