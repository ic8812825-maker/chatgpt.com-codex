"""Streaming bid/ask importer with quality counters and fixed chronological bins."""
import argparse
from collections import Counter
import csv
from datetime import datetime,timedelta,timezone
from decimal import Decimal,InvalidOperation
import hashlib
from io import TextIOWrapper
import json
from pathlib import Path
from zoneinfo import ZoneInfo
from zipfile import ZipFile

POINT=Decimal("0.00001")
SLOT=1800


def zone(value):
    return timezone(timedelta(hours=int(value))) if value.lstrip("+-").isdigit() else ZoneInfo(value)


def price(value):
    d=Decimal(value.strip().replace(",","."))
    return d,d/POINT


def timestamp(value,tz):
    v=value.strip()
    if len(v)>=15 and v[:8].isdigit() and v[8]==" " and v[9:15].isdigit():
        return datetime(int(v[:4]),int(v[4:6]),int(v[6:8]),int(v[9:11]),
                        int(v[11:13]),int(v[13:15]),int(v[15:].ljust(6,"0") or 0),tzinfo=tz)
    d=datetime.fromisoformat(v.replace(".","-",2) if "." in v[:10] else v)
    if d.tzinfo is None:
        if d.replace(tzinfo=tz,fold=0).utcoffset()!=d.replace(tzinfo=tz,fold=1).utcoffset():
            raise ValueError("ambiguous or nonexistent local timestamp")
        d=d.replace(tzinfo=tz)
    return d


def inspect(lines,tz,raw=False,separator=None):
    counts=Counter()
    first=lines.readline()
    if raw:
        stream=csv.reader(__import__("itertools").chain([first],lines))
    else:
        delim=separator or csv.Sniffer().sniff(first,delimiters="\t;,").delimiter
        columns=next(csv.reader([first],delimiter=delim))
        header={v.strip().upper().strip("<>"):i for i,v in enumerate(columns)}
        if not {"DATE","TIME","BID","ASK"}<=header.keys():
            raise ValueError("DATE TIME BID ASK are required")
        stream=csv.reader(lines,delimiter=delim)
    slots={}
    last=-1.
    last_mid=None
    first_at=None
    precision=set()
    current_records=set()
    for row in stream:
        counts["rows"]+=1
        try:
            if raw:
                time,bid,ask=row[:3]
            else:
                time=row[header["DATE"]]+" "+row[header["TIME"]]
                bid,ask=row[header["BID"]],row[header["ASK"]]
            dt=timestamp(time,tz)
            a,b=price(bid),price(ask)
            if not a[0].is_finite() or not b[0].is_finite():
                raise ValueError("nonfinite price")
            seconds=dt.timestamp()
        except (ValueError,IndexError,InvalidOperation,OverflowError):
            counts["unreadable"]+=1
            continue
        if seconds<last:
            counts["time_reversal"]+=1
            continue
        same=seconds==last
        if same:
            counts["duplicate_timestamp"]+=1
        else:
            current_records.clear()
        key=(a[0],b[0],tuple(row[3:]) if raw else tuple(row))
        if key in current_records:
            counts["duplicate_record"]+=1
            continue
        current_records.add(key)
        if last>=0 and seconds-last>60:
            counts["gap_over_60s"]+=1
        last=seconds
        first_at=seconds if first_at is None else first_at
        precision.update((-a[0].as_tuple().exponent,-b[0].as_tuple().exponent))
        if a[1]!=a[1].to_integral_value() or b[1]!=b[1].to_integral_value():
            counts["off_tick_size"]+=1
            continue
        bid_units,ask_units=int(a[1]),int(b[1])
        spread=ask_units-bid_units
        if spread<0:
            counts["crossed"]+=1
            continue
        if spread==0:
            counts["zero_spread"]+=1
        if spread>20:
            counts["spread_over_20"]+=1
        if dt.weekday()==5 or dt.weekday()==6 and dt.hour<17 or dt.weekday()==4 and dt.hour>=17:
            counts["outside_regular_provider_session"]+=1
        mid=bid_units+ask_units
        if last_mid is not None and abs(mid-last_mid)>600:
            counts["jump_over_300"]+=1
        last_mid=mid
        counts["valid"]+=1
        slot=int(seconds)//SLOT
        # Causal sample: first observed valid quote near the grid boundary.
        if seconds-slot*SLOT<=120 and slot not in slots:
            slots[slot]=(slot,seconds,bid_units,ask_units)
    quality=dict(counts)
    quality.update(quote_precision=sorted(precision),first_utc=first_at,last_utc=last,
                   sampled_slots=len(slots),timezone=str(tz))
    return quality,list(slots.values())


def audit_file(path,timezone_value,encoding=None,separator=None):
    tz=zone(timezone_value)
    if path.suffix.lower()==".zip":
        with ZipFile(path) as z:
            people=[n for n in z.namelist() if n.lower().endswith(".csv")]
            if len(people)!=1:
                raise ValueError("expected exactly one vendor CSV")
            with TextIOWrapper(z.open(people[0]),encoding=encoding or "ascii") as f:
                quality,slots=inspect(f,tz,raw=True)
            quality["member"]=people[0]
    else:
        if encoding is None:
            with path.open("rb") as f:
                encoding="utf-16" if f.read(2) in (b"\xff\xfe",b"\xfe\xff") else "utf-8-sig"
        with path.open(encoding=encoding,newline="") as f:
            quality,slots=inspect(f,tz,separator=separator)
    with path.open("rb") as f:
        quality["sha256"]=hashlib.file_digest(f,"sha256").hexdigest()
    return quality,slots


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("input",type=Path)
    p.add_argument("--timezone",required=True)
    p.add_argument("--encoding")
    p.add_argument("--separator")
    args=p.parse_args()
    q,_=audit_file(args.input,args.timezone,args.encoding,args.separator)
    print(json.dumps(q,indent=2))
