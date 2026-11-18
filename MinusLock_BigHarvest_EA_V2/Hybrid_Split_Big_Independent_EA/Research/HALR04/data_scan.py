"""Read immutable HistData ZIPs and create local exact integer tick arrays."""
from array import array
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from datetime import date,timedelta,timezone
from hashlib import file_digest
import json
from pathlib import Path
import struct
import sys
from zipfile import ZipFile

HERE=Path(__file__).resolve().parent
FOLDS=json.loads((HERE/"periods.json").read_text())
CATEGORIES=("training","validation","final_test","baseline_diagnostic","crisis_diagnostic")
MONTHS={m:k for k in CATEGORIES for m in FOLDS[k]}
T0=date(1970,1,1).toordinal()
MINUTE=60000
DAY=1440*MINUTE


def to_units(text):
    left,point,right=text.partition(b".")
    if not point or not right.isdigit() or not left.isdigit():
        raise ValueError("price")
    n=int(left)*100000+int(right[:5].ljust(5,b"0"))
    if len(right)>5 and any(x!=48 for x in right[5:]):
        raise ArithmeticError("off grid")
    return n,len(right)


def scan(dataset):
    folder,month=dataset
    archive=folder/f"historical-{month}.zip"
    ticks=array("Q")
    bids=array("I")
    asks=array("I")
    quality=Counter()
    prec=set()
    current_day=b""
    last_time=-1
    last_mid=None
    same_epoch=set()
    with ZipFile(archive) as data:
        source=[x for x in data.namelist() if x.lower().endswith(".csv")]
        if len(source)!=1:
            raise ValueError(source)
        with data.open(source[0]) as stream:
            for line in stream:
                quality["rows"]+=1
                try:
                    t,b,a,volume=line.strip().split(b",",3)
                    if len(t)!=18 or t[8]!=32:
                        raise ValueError("timestamp")
                    if t[:8]!=current_day:
                        d=date(int(t[:4]),int(t[4:6]),int(t[6:8]))
                        day=(d.toordinal()-T0)*DAY
                        weekday=d.weekday()
                        current_day=t[:8]
                    hr,mi,ss,ms=int(t[9:11]),int(t[11:13]),int(t[13:15]),int(t[15:18])
                    if hr>23 or mi>59 or ss>59:
                        raise ValueError("clock")
                    epoch=day+hr*3600000+mi*MINUTE+ss*1000+ms
                    bid,p1=to_units(b)
                    ask,p2=to_units(a)
                except (ValueError,OverflowError):
                    quality["unreadable"]+=1
                    continue
                except ArithmeticError:
                    quality["off_grid"]+=1
                    continue
                prec.update((p1,p2))
                if epoch<last_time:
                    quality["time_reversal"]+=1
                    continue
                rec=bid,ask,volume
                if epoch==last_time:
                    quality["duplicate_timestamp"]+=1
                    if rec in same_epoch:
                        quality["duplicate_record"]+=1
                        continue
                else:
                    same_epoch.clear()
                same_epoch.add(rec)
                if last_time>=0 and epoch-last_time>60000:
                    quality["gaps_over_minute"]+=1
                if last_time>=0 and epoch-last_time>7200000:
                    quality["gaps_over_two_hours"]+=1
                last_time=epoch
                if ask<bid:
                    quality["negative_spread"]+=1
                    continue
                if ask==bid:
                    quality["zero_spread"]+=1
                if ask-bid>32:
                    quality["spread_over_32"]+=1
                if weekday==5 or weekday==6 and hr<17 or weekday==4 and hr>=17:
                    quality["outside_regular_week"]+=1
                mid=ask+bid
                if last_mid is not None and abs(mid-last_mid)>600:
                    quality["jumps_over_300"]+=1
                last_mid=mid
                ticks.append(epoch)
                bids.append(bid)
                asks.append(ask)
    if not ticks:
        raise ValueError(f"No genuine valid quotes: {month}")
    with (folder/f"{month}.ticks").open("wb") as out:
        out.write(struct.pack("<Q",len(ticks)))
        ticks.tofile(out)
        bids.tofile(out)
        asks.tofile(out)
    with archive.open("rb") as f:
        sha=file_digest(f,"sha256").hexdigest()
    from datetime import datetime
    utc=lambda t:datetime.fromtimestamp(t/1000+18000,timezone.utc).isoformat()
    q={key:quality[key] for key in ("rows","unreadable","off_grid","time_reversal","duplicate_timestamp",
          "duplicate_record","gaps_over_minute","gaps_over_two_hours","negative_spread","zero_spread",
          "spread_over_32","outside_regular_week","jumps_over_300")}
    q.update(month=month,fold=MONTHS[month],sha256=sha,archive=archive.name,
             source=(f"https://www.histdata.com/download-free-forex-historical-data/"
                     f"?/ascii/tick-data-quotes/EURUSD/{month[:4]}/{int(month[4:])}"),
             valid=len(ticks),utc_first=utc(ticks[0]),utc_last=utc(ticks[-1]),
             fixed_offset="UTC-05:00",precision=sorted(prec))
    print(month,q["rows"],q["valid"],flush=True)
    return q


def load_ticks(folder,month):
    with (folder/f"{month}.ticks").open("rb") as f:
        count=struct.unpack("<Q",f.read(8))[0]
        ticks,bids,asks=array("Q"),array("I"),array("I")
        for a in (ticks,bids,asks):
            a.fromfile(f,count)
    return ticks,bids,asks


if __name__=="__main__":
    folder=Path(sys.argv[1])
    with ProcessPoolExecutor(2) as pool:
        rows=list(pool.map(scan,[(folder,m) for m in MONTHS]))
    (HERE/"03_DATA_QUALITY_REPORT.json").write_text(json.dumps(rows,indent=2)+"\n")
    (HERE/"03_DATA_MANIFEST.json").write_text(json.dumps({
        "source_format":FOLDS["provider"],"calendar":FOLDS,
        "archives":[{k:r[k] for k in ("month","fold","archive","sha256","source")} for r in rows],
        "rights":"Public download. Redistribution terms not independently confirmed; archives omitted from Git.",
        "acquire":"Run the pinned HALR-03 fetch_histdata.py using the listed months"
    },indent=2)+"\n")
