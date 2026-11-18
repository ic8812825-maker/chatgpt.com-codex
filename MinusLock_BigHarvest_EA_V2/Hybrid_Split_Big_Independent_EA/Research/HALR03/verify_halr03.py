"""Check shipped artifacts and independently replay their main assertions."""
from csv import DictReader
import importlib
import json
from pathlib import Path
import unittest

from baseline_audit import audit
from meta_audit import parity


def read(name):
    with open(name+".csv") as f:
        return list(DictReader(f))


def main():
    cases=unittest.TestSuite()
    for name in ("04_EXECUTION_TESTS","test_er","test_importer"):
        cases.addTests(unittest.defaultTestLoader.loadTestsFromModule(importlib.import_module(name)))
    result=unittest.TextTestRunner(verbosity=2).run(cases)
    assert result.wasSuccessful()
    a=audit()
    assert a["status"]=="PASS"
    assert parity()==json.loads(Path("06_DELEGATE_PARITY.json").read_text())
    pins=json.loads(Path("01_REPRODUCTION_DIFF.json").read_text())
    assert all(x["identical"] for x in pins["comparisons"].values())
    staged=read("08_ROBUSTNESS_MATRIX")
    for r in staged:
        if r["profile"] in ("E0","E1","E2") and r["policy"] in ("A3-ER","M-ER","K-EXECUTABLE")                 and int(r["cost_budget"])>=29:
            assert r["flat"]==r["n"] and r["risk_violations"]=="0",r
    p=read("08_PAIRED_COMPARISON")
    for r in p:
        assert sum(int(r[k]) for k in ("both","only_left","only_right","neither"))==int(r["n"]),r
    s=read("03_FAILURE_TAXONOMY")
    assert sum(r["policy"]=="A3-selected" for r in s)==32
    assert sum(r["policy"]=="K-EXECUTABLE" for r in s)==24
    h=json.loads(Path("07_DATA_QUALITY_REPORT.json").read_text())
    assert len(h["archives"])==5 and h["episodes"]["test"]["count"]==9
    data=dict(passed=True,tests=result.testsRun,baseline_reproduced=15,
              cash_reconciled_fills=sum(x["reconciled_fills"] for x in a["cash_and_tree"]),
              failure_rows=len(s),paired_rows=len(p),trial_group_rows=len(staged),
              kernel_rows=len(read("09_VIABILITY_KERNEL")),historical_archives=len(h["archives"]))
    Path("TEST_RESULTS.json").write_text(json.dumps(data,indent=2)+"\n")
    print(data)


if __name__=="__main__":
    main()
