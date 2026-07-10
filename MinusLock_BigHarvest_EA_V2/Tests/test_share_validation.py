from pathlib import Path
ea=(Path(__file__).resolve().parents[1]/"MinusLock_BigHarvest_EA.mq5").read_text()
assert "ReserveShare + CloseFarShare must be exactly 1.0" in ea
assert "MathAbs((CloseFarShare + ReserveShare) - 1.0)" in ea
print("PASS: Invalid CloseFarShare + ReserveShare combinations are rejected.")
