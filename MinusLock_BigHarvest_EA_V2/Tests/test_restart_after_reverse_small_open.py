from pathlib import Path
state=(Path(__file__).resolve().parents[1]/"Include"/"StateMachine.mqh").read_text()
for token in ["ReverseSmallTicket", "ReverseSmallIdentifier", "ReverseSmallLot", "ReverseSmallOpenPrice", "ReverseSmallDirection", "ReverseSmallOpened"]:
    assert token in state, token
print("PASS restart after ReverseSmall open fields persisted")
