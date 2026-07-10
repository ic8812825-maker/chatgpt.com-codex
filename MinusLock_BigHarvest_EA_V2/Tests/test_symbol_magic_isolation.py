from pathlib import Path
state = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
assert "HistoryDealGetString(dealTicket, DEAL_SYMBOL) != _Symbol" in state
assert "HistoryDealGetInteger(dealTicket, DEAL_MAGIC) != MagicNumber" in state
assert "DEAL_POSITION_ID" in state
print("PASS: Symbol + Magic isolation is enforced for deal history.")
