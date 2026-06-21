from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
for token in ["KNOWN_CONTEXT_PRESENT", "InitialBuy=%s", "InitialSell=%s", "Far=%s", "Big=%s", "Small=%s", "Pending=%s", "Retry=%s", "KnownContext=%s"]:
    assert token in state, token
print("KNOWN_CONTEXT_DIAGNOSTICS_CHECK PASS")
