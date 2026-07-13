from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "Types.mqh").read_text()
for token in ["enum PositionRole", "ROLE_BIG_CORE", "ROLE_BIG_TREND", "ROLE_SMALL_BASE", "ROLE_REVERSE_SMALL", "BuildRoleComment", "ParseRoleComment", "ML|%s|C%I64d|L%d|R%d"]:
    assert token in text, token
print("PASS position role comments are defined")
