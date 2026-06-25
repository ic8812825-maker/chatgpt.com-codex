from pathlib import Path
import csv
root = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader((root / "Optimization_Report.csv").open()))
assert rows
accepted_seen = False
for row in rows:
    if row["Verdict"] == "ACCEPT":
        accepted_seen = True
        assert row["IsSelectableForSetFile"] == "YES"
        assert float(row["FinalRank"]) > -999999999.0
    else:
        assert row["IsSelectableForSetFile"] == "NO"
        assert float(row["Score"]) < 0.0
        assert float(row["FinalRank"]) <= -999999999.0
assert accepted_seen
report = (root / "Best_Parameters.md").read_text()
assert "Rejected rows are diagnostics only" in report
assert "No `.set` file was generated from a rejected row" in report
print("OFFLINE_REJECTED_NOT_SELECTABLE_CHECK PASS")
