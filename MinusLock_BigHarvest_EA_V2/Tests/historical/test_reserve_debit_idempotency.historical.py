from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
assert "ApplyReserveDebit" in text
assert "ReserveEventAlreadyApplied(eventKeyHash)" in text
assert "WARNING_RESERVE_DEBIT" in text
print("PASS reserve debit idempotency guard present")
