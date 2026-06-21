from pathlib import Path
root = Path(__file__).resolve().parents[1]
types = (root / "Include" / "Types.mqh").read_text()
fields = [
    "initialBuyTicket", "initialSellTicket",
    "initialBuyIdentifier", "initialSellIdentifier",
    "initialBuyLot", "initialSellLot",
    "initialBuyOpenPrice", "initialSellOpenPrice",
    "initialLockRecovered",
]
for field in fields:
    assert field in types, field
print("INITIAL_LOCK_CONTEXT_FIELDS_CHECK PASS")
