"""New fixed calendar and two-step causal activation using the archived S2 sampler."""
from bisect import bisect_left
from calendar import monthrange
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
import csv
from datetime import date
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
from zipfile import BadZipFile
import sys

from pinned import setup
setup()
import data_scan
from data_scan import DAY,MINUTE,T0,load_ticks
margin=importlib.import_module("02_MARGIN_ORACLE")


def json_out(name,data):
    Path(name+".json").write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")


def csv_out(name,rows):
    if not rows:
        raise ValueError(f"Cannot write empty {name}")
    with open(name+".csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def load_sampler():
    h4=setup()["HALR04_DIR"]/"04_CAUSAL_REPLAY.py"
    spec=importlib.util.spec_from_file_location("halr04_sampler",h4)
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def months():
    raw=json.loads(Path("03_FROZEN_PROTOCOL.json").read_text())
    for name,checksum in raw["locked_sha256"].items():
        if sha256(Path(name).read_bytes()).hexdigest()!=checksum:
            raise ValueError("Frozen source mismatch: "+name)
    return raw["calendar"]


def download(month,folder):
    from subprocess import run
    f=folder/f"historical-{month}.zip"
    if not f.is_file():
        result=run([sys.executable,"-B",str(setup()["HALR03_DIR"]/"fetch_histdata.py"),month],
                   cwd=folder,capture_output=True,text=True)
        if result.returncode or not f.exists():
            return month,str(result.stderr).strip().splitlines()[-1:] or ["archive not returned"]
    return month,None


def scan_one(job):
    folder,month=job
    data_scan.MONTHS[month]="holdout"
    try:
        return data_scan.scan(job)
    except (ValueError,OSError,BadZipFile) as error:
        return dict(month=month,error=str(error))


def calendar_days(month):
    y,m=int(month[:4]),int(month[4:])
    for j in range(1,monthrange(y,m)[1]+1):
        d=date(y,m,j)
        if d.weekday()<5:
            yield d


def build(folder,quality):
    sampler=load_sampler()
    all_candidates=[]
    all_episodes=[]
    available={r["month"] for r in quality if "valid" in r}
    for month in months():
        ok=month in available
        if ok:
            ts,b,a=load_ticks(folder,month)
        for d in calendar_days(month):
            day=d.toordinal()-T0
            row=dict(month=month,id=d.isoformat(),status="",reason="",eligible=False,complete="",
                     anchor_utc_ms="",activation_utc_ms="",anchor_bid="",anchor_ask="",
                     activation_bid="",activation_ask="",orientation="",margin_level="",mark="",reserve="",
                     execution="BROKER_ELIGIBILITY_UNKNOWN")
            all_candidates.append(row)
            if not ok:
                row.update(status="ARCHIVE_MISSING",reason="ARCHIVE")
                continue
            target=day*DAY+8*60*MINUTE
            i=bisect_left(ts,target)
            if i==len(ts) or ts[i]>=target+5*MINUTE:
                row.update(status="NO_ANCHOR",reason="NO_QUOTE_WINDOW")
                continue
            entry=(ts[i],b[i],a[i])
            row.update(anchor_utc_ms=ts[i]+18000000,anchor_bid=b[i],anchor_ask=a[i])
            cutoff=bisect_left(ts,day*DAY+14*60*MINUTE,i+1)
            initial=b[i]+a[i]
            triggered=next((j for j in range(i+1,cutoff) if abs(b[j]+a[j]-initial)>=600),None)
            if triggered is None:
                row.update(status="NO_ACTIVATION",reason="THRESHOLD_NOT_REACHED")
                continue
            j=triggered
            activation=(ts[j],b[j],a[j])
            orientation=1 if b[j]+a[j]>initial else -1
            # The sole eligibility call receives no subsequent observation.
            state=margin.assess(entry,activation,orientation)
            obs=sampler.observations(ts,b,a,j,30,12)
            full=len(obs)==13
            row.update(status="ELIGIBLE" if state["eligible"] else "EXCLUDED",
                       reason="|".join(state["reasons"]),eligible=state["eligible"],complete=full,
                       activation_utc_ms=ts[j]+18000000,activation_bid=b[j],activation_ask=a[j],
                       orientation=orientation,margin_level=state.get("margin_level_percent",""),
                       mark=state.get("mark",""),reserve=state.get("exit_reserve",""),
                       execution=state["execution"])
            if state["eligible"]:
                all_episodes.append(dict(id=d.isoformat(),month=month,orientation=orientation,
                                         entry=entry,obs=obs,complete=full))
    csv_out("04_EPISODE_LEDGER",all_candidates)
    (folder/"eligible.json").write_text(json.dumps(all_episodes,separators=(",",":"))+"\n")
    return all_candidates,all_episodes


def main(folder):
    folder=folder.resolve()
    folder.mkdir(exist_ok=True)
    plan=months()
    futures=[]
    with ThreadPoolExecutor(3) as pool:
        for month in plan:
            futures.append(pool.submit(download,month,folder))
        results=[p.result() for p in futures]
    missing=[dict(month=m,error=e) for m,e in results if e]
    with ProcessPoolExecutor(2) as pool:
        q=list(pool.map(scan_one,[(folder,m) for m,e in results if not e]))
    q.extend(missing)
    q.sort(key=lambda r:r["month"])
    assert any("valid" in r for r in q),"NEW_HOLDOUT_UNAVAILABLE"
    json_out("04_DATA_QUALITY",q)
    json_out("04_DATA_MANIFEST",dict(source="HistData EURUSD Generic ASCII Bid/Ask",
        time_zone="Fixed UTC-05:00",rights="Public download; redistribution terms unverified; raw ZIP outside Git.",
        archives=[{k:v for k,v in r.items() if k in ("month","archive","source","sha256","error","utc_first","utc_last")} for r in q]))
    x,y=build(folder,q)
    print(dict(days=len(x),eligible=len(y),archives=sum("valid" in r for r in q)))


if __name__=="__main__":
    main(Path(sys.argv[1]))
