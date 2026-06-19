from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
recon = (root / "Include" / "ReconciliationEngine.mqh").read_text()
assert "double RebuildReserveFromLedger()" in state
assert "RESERVE_REBUILD_FROM_LEDGER" in recon
assert "double ledgerReserve = RebuildReserveFromLedger();" in recon
assert "return ledgerReserve;" in recon
assert "ReserveLedgerCount" in state and "ReserveNextEventId" in state
print("RESERVE_REBUILD_FROM_LEDGER_CHECK PASS")
