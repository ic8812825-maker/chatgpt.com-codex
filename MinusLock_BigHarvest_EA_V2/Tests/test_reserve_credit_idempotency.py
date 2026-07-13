from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
assert "ApplyReserveCredit" in text
assert "ReserveEventAlreadyApplied(eventKeyHash)" in text
assert "WARNING_RESERVE_CREDIT" in text
print("PASS reserve credit idempotency guard present")
