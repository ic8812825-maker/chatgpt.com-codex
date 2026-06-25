from pathlib import Path
import csv
root = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader((root / "Optimization_Report.csv").open()))
assert len(rows) >= 100000, len(rows)
columns = rows[0].keys()
for col in [
    "RunID", "Category", "SearchPhase", "StartLot", "BigRatio", "RecoveryPL_Mean", "RecoveryPL_Min",
    "StopMaxLevelsCount", "ClosedProfitCount", "ClosedRecoveryLossCount", "Score", "StabilityScore",
    "RobustnessScore", "FinalRank", "CoverageRatio", "IsSelectableForSetFile", "Verdict"
]:
    assert col in columns, col
assert any(r["Verdict"] == "ACCEPT" for r in rows)
accepted = [r for r in rows if r["Verdict"] == "ACCEPT"]
rejected = [r for r in rows if r["Verdict"] != "ACCEPT"]
assert accepted and rejected
assert min(float(r["FinalRank"]) for r in accepted) > max(float(r["FinalRank"]) for r in rejected)
assert all(r["IsSelectableForSetFile"] == "YES" for r in accepted)
assert all(r["IsSelectableForSetFile"] == "NO" for r in rejected)
report = (root / "Best_Parameters.md").read_text()
for section in ["### SAFE", "### BALANCED", "### AGGRESSIVE", "### LOWLOT_SAFE", "## TOP ACCEPT", "## TOP REJECTED", "## Why rejected", "Sensitivity Analysis", "Required MT5 validation"]:
    assert section in report, section
print("OFFLINE_OPTIMIZER_REPORT_CHECK PASS")
