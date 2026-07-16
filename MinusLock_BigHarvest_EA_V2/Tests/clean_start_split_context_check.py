from pathlib import Path


state = (Path(__file__).parents[1] / "Include" / "StateMachine.mqh").read_text(encoding="utf-8")

required_roles = ("BigCore", "BigTrend", "SmallBase", "ReverseSmall")
for role in required_roles:
    assert f'StateKey("{role}TicketHigh32")' in state
    assert f'StateKey("{role}TicketLow32")' in state
    assert f'StateKey("{role}IdentifierHigh32")' in state
    assert f'StateKey("{role}IdentifierLow32")' in state

for diagnostic in (
    "LegacyContext=",
    "SplitContext=",
    "InitialContext=",
    "PendingContext=",
    "RetryContext=",
    "ReserveLedger=",
    "ReserveTransaction=",
    "FailureMarker=",
    "ManagedPositions=",
    "CleanStartResult=",
):
    assert diagnostic in state

# A persisted zero retry is inactive; a half-written uint64 remains fail-safe malformed.
assert "retryTicketMalformed = (retryHighExists != retryLowExists)" in state
assert 'GlobalVariableGet(StateKey("RetryTicketHigh32")) > 0.5' in state
assert 'GlobalVariableGet(StateKey("LastRetryState")) != (double)STATE_IDLE' in state
assert "retryTicketMalformed || retryTicketActive" in state

assert "!hasLegacyContext && !hasSplitContext && managed == 0" in state

print("CLEAN_START_SPLIT_CONTEXT_CHECK_PASS")
