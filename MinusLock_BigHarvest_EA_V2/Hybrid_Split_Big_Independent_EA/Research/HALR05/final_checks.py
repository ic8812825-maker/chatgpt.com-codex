"""Confirm shipped evidence, immutable dependencies, test outcomes and real quotes."""
from csv import DictReader
from gzip import open as zipped
import json
from pathlib import Path
import unittest
import sys
from independent_audit import audit


def run(folder):
    s=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover("."))
    if not s.wasSuccessful():
        raise SystemExit(1)
    a=audit(folder)
    assert a==json.loads(Path("09_INDEPENDENT_AUDIT.json").read_text())
    d=json.loads(Path("07_CONFIRMATORY_DECISION.json").read_text())
    assert d["status"]=="NEGATIVE_EVIDENCE"
    assert d["eligible"]==322 and d["blocks"]==30
    assert d["statistics"]["paired_mean"]<0
    archived={row["policy"]:0 for row in DictReader(open("08_STRESS_RESULTS.csv"))}
    with open("08_STRESS_RESULTS.csv") as f:
        for row in DictReader(f):
            archived[row["policy"]]+=1
    assert all(n==88 for n in archived.values())
    with zipped("07_CONFIRMED_JOURNALS.jsonl.gz","rt") as f:
        journals=[json.loads(line) for line in f]
    assert len(journals)==644
    assert all(r["oracle"]["flat"] and r["oracle"]["pending"]==0 for r in journals)
    a.update(primary_journals=len(journals),
             primary_confirmed_model_fills=sum(r["oracle"]["verified_fills"] for r in journals))
    Path("AUDIT_RESULTS.json").write_text(json.dumps(a,indent=2,sort_keys=True)+"\n")
    Path("TEST_RESULTS.json").write_text(json.dumps(dict(tests=s.testsRun,passed=True,
             failures=len(s.failures),errors=len(s.errors),archive_regression=archived),indent=2)+"\n")
    print(a)


if __name__=="__main__":
    run(Path(sys.argv[1]))
