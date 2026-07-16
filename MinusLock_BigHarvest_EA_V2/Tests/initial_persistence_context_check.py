from pathlib import Path

state = (Path(__file__).parents[1] / "Include" / "StateMachine.mqh").read_text(encoding="utf-8")
for field in ("InitialBuyTicket", "InitialSellTicket", "InitialBuyIdentifier", "InitialSellIdentifier"):
    assert f'InspectPersistedUInt64("{field}"' in state
assert "buyTicketActive != buyIdentifierActive" in state
assert "sellTicketActive != sellIdentifierActive" in state
assert "buyTicket.restoredValue == sellTicket.restoredValue" in state
assert "buyIdentifier.restoredValue == sellIdentifier.restoredValue" in state
assert "INITIAL_CONTEXT_MALFORMED" in state
print("INITIAL_PERSISTENCE_CONTEXT_CHECK_PASS")
