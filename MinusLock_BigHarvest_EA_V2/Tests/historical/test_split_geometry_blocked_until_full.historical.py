from pathlib import Path
root = Path(__file__).resolve().parents[1]
ea = (root / "MinusLock_BigHarvest_EA.mq5").read_text()
assert "#ifndef SPLIT_GEOMETRY_FULLY_IMPLEMENTED" in ea
assert "ERROR_SPLIT_GEOMETRY_NOT_IMPLEMENTED" in ea
assert "return INIT_FAILED" in ea
print("PASS split geometry is blocked until full implementation macro is defined")
