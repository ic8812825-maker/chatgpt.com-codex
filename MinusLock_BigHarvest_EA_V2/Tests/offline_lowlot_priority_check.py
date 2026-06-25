from pathlib import Path
import csv
root = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader((root / "Optimization_Report.csv").open()))
accepted_lots = {row["StartLot"] for row in rows if row["Verdict"] == "ACCEPT"}
report = (root / "Best_Parameters.md").read_text()
assert "LOWLOT candidate found at StartLot=" in report or "LOWLOT_SAFE_NOT_FOUND" in report
set_path = root / "Sets" / "USDJPY_M30_LOWLOT_SAFE.set"
if "0.01" in accepted_lots:
    assert "LOWLOT candidate found at StartLot=0.01" in report
    assert "StartLot=0.01" in set_path.read_text()
elif "0.05" in accepted_lots:
    assert "LOWLOT candidate found at StartLot=0.05" in report
    assert "StartLot=0.05" in set_path.read_text()
elif "0.10" in accepted_lots:
    assert "LOWLOT candidate found at StartLot=0.1" in report or "LOWLOT candidate found at StartLot=0.10" in report
    assert "StartLot=0.1" in set_path.read_text() or "StartLot=0.10" in set_path.read_text()
else:
    assert (root / "Sets" / "USDJPY_M30_LOWLOT_SAFE_NOT_FOUND.txt").exists()
print("OFFLINE_LOWLOT_PRIORITY_CHECK PASS")
