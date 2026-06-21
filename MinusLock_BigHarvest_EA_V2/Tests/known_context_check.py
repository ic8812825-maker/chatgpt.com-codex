from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
for token in ["bool HasKnownContext()", "HasInitialBuyContext()", "HasInitialSellContext()", "HasFarContext()", "HasBigContext()", "HasSmallContext()", "HasPendingOperationContext()", "HasRetryOperationContext()"]:
    assert token in state, token
assert "return HasKnownContext();" in state
print("KNOWN_CONTEXT_CHECK PASS")
