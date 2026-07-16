from pathlib import Path
s=(Path(__file__).parents[1]/"Include"/"StateMachine.mqh").read_text(encoding="utf-8")
x=s[s.index("void EvaluateReserveTransactionPersistence"):s.index("bool IsProvenCleanStart()")]
for v in ("ReserveTxTransactionId","ReserveTxEventKeyHash","ReserveTxExpectedLedgerEventId","ReserveTxCycleId","ReserveTxAmount","ReserveTxReserveBefore","ReserveTxReserveAfter"): assert v in x
assert "RESERVE_TRANSACTION_CONTEXT_MALFORMED" in x
print("RESERVE_TRANSACTION_PERSISTENCE_CONTEXT_CHECK_PASS")
