from pathlib import Path
state=(Path(__file__).resolve().parents[1]/"Include"/"StateMachine.mqh").read_text()
for token in ["BigTrendTicket", "BigTrendIdentifier", "BigTrendLot", "BigTrendOpenPrice", "BigTrendDirection", "BigTrendClosedForReverse"]:
    assert token in state, token
print("PASS restart after BigTrend close fields persisted")
