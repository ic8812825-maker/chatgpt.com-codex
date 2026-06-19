from pathlib import Path
root = Path(__file__).resolve().parents[1]
types = (root / "Include" / "Types.mqh").read_text()
state = (root / "Include" / "StateMachine.mqh").read_text()
for token in ["enum ReserveEventType", "RESERVE_EVENT_BIG_HARVEST_ADD", "RESERVE_EVENT_SMALL_HARVEST_ADD", "RESERVE_EVENT_FAR_COVER_DEBIT", "RESERVE_EVENT_FINAL_CLOSE_DEBIT", "struct ReserveLedgerEntry"]:
    assert token in types
for token in ["ReserveLedgerEntry ReserveLedger[]", "AppendReserveLedgerEntry", "ApplyReserveCredit", "ApplyReserveDebit", "RESERVE_LEDGER"]:
    assert token in state
assert "ApplyReserveCredit(RESERVE_EVENT_BIG_HARVEST_ADD" in state
assert "ApplyReserveCredit(RESERVE_EVENT_SMALL_HARVEST_ADD" in state
print("RESERVE_LEDGER_CREDIT_DEBIT_CHECK PASS")
