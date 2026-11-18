"""Confirm denominators, eligibility causality and accepted raw archive identities."""
from collections import Counter,defaultdict
from csv import DictReader
import importlib
from hashlib import file_digest
import json
from pathlib import Path
import sys

io=importlib.import_module("04_CAUSAL_REPLAY")
eligibility=importlib.import_module("02_MARGIN_ORACLE")


def check(folder):
    ledger=list(DictReader(open("04_EPISODE_LEDGER.csv")))
    states=json.loads((folder/"eligible.json").read_text())
    quality=json.loads(Path("04_DATA_QUALITY.json").read_text())
    assert len(quality)==36
    for d in quality:
        if "sha256" not in d:
            continue
        with (folder/d["archive"]).open("rb") as f:
            assert file_digest(f,"sha256").hexdigest()==d["sha256"]
    by={e["id"]:e for e in states}
    periods=defaultdict(Counter)
    for row in ledger:
        c=periods[row["month"]]
        c["potential"]+=1
        c[row["status"]]+=1
        if row["status"] not in ("ELIGIBLE","EXCLUDED"):continue
        a,b,x,y,s=(int(row[k]) for k in ("anchor_bid","anchor_ask","activation_bid","activation_ask","orientation"))
        entry=(int(row["anchor_utc_ms"]),a,b)
        activation=(int(row["activation_utc_ms"]),x,y)
        e=eligibility.assess(entry,activation,s)
        assert e["eligible"]==(row["id"] in by)==(row["eligible"]=="True")
        assert "|".join(e["reasons"])==row["reason"]
        c["activated"]+=1
        c["incomplete_eligible"]+=e["eligible"] and row["complete"]=="False"
        c["incomplete_excluded"]+=(not e["eligible"] and row["complete"]=="False")
        if e["eligible"]:
            episode=by[row["id"]]
            assert [e+18000000 if i==0 else e for i,e in enumerate(episode["obs"][0])]==list(activation)
            assert len(episode["obs"])<=13 and (len(episode["obs"])==13)==episode["complete"]
            assert all(y[0]>x[0] for x,y in zip(episode["obs"],episode["obs"][1:]))
    assert len(ledger)==len({r["id"] for r in ledger})
    out=[]
    for m,r in sorted(periods.items()):
        assert r["activated"]==r["ELIGIBLE"]+r["EXCLUDED"]
        assert r["potential"]==r["activated"]+r["NO_ANCHOR"]+r["NO_ACTIVATION"]+r["ARCHIVE_MISSING"]
        out.append(dict(month=m,potential=r["potential"],activated=r["activated"],eligible=r["ELIGIBLE"],
                       excluded=r["EXCLUDED"],no_anchor=r["NO_ANCHOR"],no_activation=r["NO_ACTIVATION"],
                       archive_missing=r["ARCHIVE_MISSING"],incomplete_eligible=r["incomplete_eligible"],
                       incomplete_excluded=r["incomplete_excluded"]))
    io.csv_out("04_PERIOD_COUNTS",out)
    return dict(archives=sum("sha256" in r for r in quality),quotes=sum(r.get("valid",0) for r in quality),
                classifications=len(ledger),eligible=len(states),eligible_clusters=len({e["month"] for e in states}))


if __name__=="__main__":
    print(check(Path(sys.argv[1])))
