from pathlib import Path
state=(Path(__file__).parents[1]/"Include"/"StateMachine.mqh").read_text(encoding="utf-8")
s=state[state.index("void EvaluateReserveLedgerPersistence"):state.index("bool IsProvenCleanStart()")]
for value in ("ReserveLedgerCount","ReserveNextEventId","NextReserveTransactionId","TotalReserve","ReserveLedger_"): assert value in s
assert "count == 0 && rowsExist" in s
assert "RESERVE_LEDGER_CONTEXT_MALFORMED" in s
print("RESERVE_LEDGER_PERSISTENCE_CONTEXT_CHECK_PASS")
