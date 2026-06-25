from pathlib import Path
import csv
root = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader((root / "Optimization_Report.csv").open()))
assert len(rows) >= 1000
columns = rows[0].keys()
for col in ["RunID", "Category", "StartLot", "BigRatio", "RecoveryPL_Mean", "RecoveryPL_Min", "StopMaxLevelsCount", "ClosedProfitCount", "ClosedRecoveryLossCount", "Score", "Verdict"]:
    assert col in columns, col
assert any(r["Verdict"] == "ACCEPT" for r in rows)
report = (root / "Best_Parameters.md").read_text()
for section in ["### SAFE", "### BALANCED", "### AGGRESSIVE", "### LOWLOT_SAFE", "Required MT5 validation"]:
    assert section in report, section
print("OFFLINE_OPTIMIZER_REPORT_CHECK PASS")
