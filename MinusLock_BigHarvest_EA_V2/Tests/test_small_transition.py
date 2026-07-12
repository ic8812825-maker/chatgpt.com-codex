from pathlib import Path
root=Path(__file__).resolve().parents[1]
types=(root/"Include"/"Types.mqh").read_text()
for token in ["reverseSmallTicket", "reverseConfirmed", "bigTrendClosedForReverse", "STATE_REVERSE_CONFIRMATION_WAIT", "STATE_REVERSE_CLOSE_BIG_TREND", "STATE_REVERSE_OPEN_DYNAMIC_SMALL", "STATE_SMALL_CLOSE_BIG_CORE_PART"]:
    assert token in types, token
print("PASS split small transition fields/states present")
