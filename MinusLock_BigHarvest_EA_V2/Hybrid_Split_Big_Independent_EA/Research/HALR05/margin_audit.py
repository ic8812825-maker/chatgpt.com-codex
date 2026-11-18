"""Cross-check historical activation flags against the immutable HALR04 audit."""
import csv
import importlib
import json
from pathlib import Path
import sys

from pinned import setup
m=importlib.import_module("02_MARGIN_ORACLE")
h4=setup()["HALR04_DIR"]


def audit(path):
    episodes=[e for e in json.loads((path/"episodes.json").read_text())
              if e["fold"]=="final_test" and e["scheme"]=="S2" and e["interval"]==30]
    with (h4/"08_FEASIBILITY_AT_ACTIVATION.csv").open() as f:
        ref={e["id"]:e for e in csv.DictReader(f)}
    rows=[]
    for e in episodes:
        a=m.assess(e["entry"],e["obs"][0],e["orientation"])
        r=ref[e["id"]]
        assert a["eligible"]==(r["qualified"]=="True"),e["id"]
        assert abs(a["margin_level_percent"]-float(r["margin_percent"]))<1e-8
        rows.append(dict(id=e["id"],**a))
    assert len(rows)==69 and sum("MARGIN" in r["reasons"] for r in rows)==28
    return dict(activations=len(rows),margin_failures=28,matches=len(rows),details=rows,
                conclusion="CORRECT_GROSS_MARGIN_MODEL; BROKER_HEDGED_MARGIN_UNKNOWN")


if __name__=="__main__":
    print(json.dumps(audit(Path(sys.argv[1])),indent=2))
