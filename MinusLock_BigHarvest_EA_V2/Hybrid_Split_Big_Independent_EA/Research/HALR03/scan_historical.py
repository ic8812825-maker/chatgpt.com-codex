"""Parallel read-only quality scan of the five independent source archives."""
from concurrent.futures import ProcessPoolExecutor
import importlib
import json
from pathlib import Path

mod=importlib.import_module("07_CSV_IMPORTER")
FOLDS={"202301":"training","202307":"validation","202401":"diagnostic_test","202003":"stress","202407":"test"}


def scan(month):
    q,slots=mod.audit_file(Path(f"../historical-{month}.zip"),"-5")
    q.update(month=month,fold=FOLDS[month],source="HistData Generic ASCII tick Bid/Ask")
    Path(f"../slots-{month}.json").write_text(json.dumps(slots))
    print(month,q["rows"],q["valid"],q["sampled_slots"],flush=True)
    return q


if __name__=="__main__":
    with ProcessPoolExecutor(2) as pool:
        q=list(pool.map(scan,FOLDS))
    Path("07_DATA_QUALITY_REPORT.json").write_text(json.dumps({"archives":q},indent=2)+"\n")
