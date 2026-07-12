from pathlib import Path
root=Path(__file__).resolve().parents[1]
types=(root/"Include"/"Types.mqh").read_text()
for token in ["bigCoreTicket", "bigTrendTicket", "smallBaseTicket", "STATE_BIG_HARVEST_CLOSE_CORE", "STATE_BIG_HARVEST_CLOSE_TREND", "STATE_BIG_HARVEST_CLOSE_SMALL_BASE"]:
    assert token in types, token
print("PASS split Big full harvest roles/states present")
