from pathlib import Path
root = Path(__file__).resolve().parents[1]
optimizer = (root / "Tools" / "offline_optimizer.py").read_text()
report = (root / "Best_Parameters.md").read_text()
assert "for lot in [0.01, 0.05, 0.10]" in optimizer
assert "LOWLOT candidate found at StartLot=" in report or "LOWLOT_SAFE_NOT_FOUND" in report
if "LOWLOT candidate found at StartLot=" in report:
    line = next(line for line in report.splitlines() if line.startswith("LOWLOT candidate found at StartLot="))
    assert any(line.endswith(str(lot)) for lot in [0.01, 0.05, 0.1, 0.10]), line
print("OFFLINE_LOWLOT_PRIORITY_CHECK PASS")
