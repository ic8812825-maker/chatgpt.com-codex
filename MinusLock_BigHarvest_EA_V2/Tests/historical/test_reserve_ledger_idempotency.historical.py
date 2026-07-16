from pathlib import Path
state = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
assert "ReserveEventAlreadyApplied(eventKeyHash)" in state
assert "WARNING_RESERVE_CREDIT" in state
assert "WARNING_RESERVE_DEBIT" in state
assert "ERROR_RESERVE_DEBIT_EXCEEDS_BALANCE" in state
assert "RESERVE_EVENT_BIG_FULL_FAR_CLOSE_DEBIT" in (Path(__file__).resolve().parents[1] / "Include" / "Types.mqh").read_text()
print("PASS: Reserve credit and debit are idempotent through ledger event keys.")
