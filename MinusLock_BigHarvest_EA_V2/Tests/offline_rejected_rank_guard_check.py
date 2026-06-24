from pathlib import Path
import csv
root = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader((root / "Optimization_Report.csv").open()))
first_rejected = next((i for i, r in enumerate(rows) if r["Verdict"] != "ACCEPT"), None)
assert first_rejected is not None, "expected rejected diagnostics rows"
assert all(r["Verdict"] == "ACCEPT" for r in rows[:first_rejected]), "non-ACCEPT before ACCEPT block ended"
assert all(r["Verdict"] != "ACCEPT" for r in rows[first_rejected:]), "ACCEPT row found after rejected block"
for row in rows[first_rejected:first_rejected + 100]:
    assert float(row["Score"]) <= -999000.0, row["Score"]
    assert float(row["FinalRank"]) <= -999000.0, row["FinalRank"]
    assert row["IsSelectableForSetFile"] == "NO"
print("OFFLINE_REJECTED_RANK_GUARD_CHECK PASS")
