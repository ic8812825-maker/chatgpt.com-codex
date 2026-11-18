"""Read anonymized broker event files offline with a conserved quantity ledger."""
import argparse
import csv
from datetime import datetime
from decimal import Decimal
import json
from math import ceil
from pathlib import Path


def timestamp(value):
    t=datetime.fromisoformat(value.replace("Z","+00:00"))
    if t.utcoffset() is None:
        raise ValueError("Timestamp lacks UTC offset")
    return t


def number(event,field,default=None):
    out=event.get(field)
    if out in (None,""):
        if default is None:
            raise ValueError(f"Missing {field}")
        out=default
    x=Decimal(str(out))
    if not x.is_finite():
        raise ValueError(field)
    return x


def percentile(xs,p):
    return sorted(xs)[ceil(len(xs)*p)-1] if xs else None


def analyze(events):
    state={}
    deals=set()
    clocks=[]
    slippage=[]
    fillsizes=[]
    prev=None
    costs=swap=Decimal(0)
    rejected=late=0
    for e in events:
        time=timestamp(e["timestamp"])
        if prev is not None and time<prev:
            raise ValueError("Events out of order")
        prev=time
        label=e["event"]
        key=e.get("order_id")
        if label=="SEND":
            size=number(e,"requested_lots")
            px=number(e,"requested_price")
            if not key or key in state or size<=0 or px<=0 or e.get("side") not in ("BUY","SELL"):
                raise ValueError("Invalid SEND")
            state[key]=dict(side=e["side"],remaining=size,price=px,sent=time,state="PENDING")
            continue
        if label=="SWAP":
            swap+=number(e,"cash")
            continue
        if label=="RESTART":
            for o in state.values():
                if o["state"] not in ("FILLED","REJECTED","CANCELLED"):
                    o["state"]="UNKNOWN"
            continue
        o=state.get(key)
        if o is None or o["state"] in ("FILLED","REJECTED","CANCELLED"):
            raise ValueError(f"Unknown or terminal order {key}")
        if label=="FILL":
            deal=e.get("deal_id")
            size=number(e,"filled_lots")
            px=number(e,"execution_price")
            if not deal or deal in deals or not 0<size<=o["remaining"] or px<=0:
                raise ValueError("Invalid or duplicate fill")
            deals.add(deal)
            late+=o["state"]=="CANCEL_PENDING"
            o["remaining"]-=size
            o["state"]="FILLED" if not o["remaining"] else (
                "CANCEL_PENDING" if o["state"]=="CANCEL_PENDING" else "PARTIAL")
            sign=1 if o["side"]=="BUY" else -1
            clocks.append((time-o["sent"]).total_seconds()*1000)
            slippage.append(float(sign*(px-o["price"])/Decimal(".00001")))
            fillsizes.append(float(size))
            costs+=number(e,"commission","0")
        elif label in ("REJECT","CANCEL_ACK","CANCEL_SENT","UNKNOWN","ACK"):
            o["state"]={"REJECT":"REJECTED","CANCEL_ACK":"CANCELLED","CANCEL_SENT":"CANCEL_PENDING",
                        "UNKNOWN":"UNKNOWN","ACK":"ACCEPTED"}[label]
            rejected+=label=="REJECT"
        elif label=="RECONCILE":
            if number(e,"remaining_lots")!=o["remaining"]:
                raise ValueError("Reconciliation cannot invent a fill")
            if e.get("status") not in ("ACCEPTED","CANCELLED","REJECTED","UNKNOWN"):
                raise ValueError("Unknown reconciliation state")
            o["state"]=e["status"]
        else:
            raise ValueError(label)
    live=[o for o in state.values() if o["state"] not in ("FILLED","REJECTED","CANCELLED")]
    return dict(orders=len(state),deals=len(deals),rejected=rejected,cancel_race_fills=late,
                unresolved=len(live),outstanding_lots=str(sum((o["remaining"] for o in live),Decimal(0))),
                observed_delay_p95_ms=percentile(clocks,.95),observed_slip_p95_points=percentile(slippage,.95),
                largest_observed_fill_lots=max(fillsizes,default=None),
                cash_commission=str(costs),cash_swap=str(swap),guaranteed_future_capacity=None)


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("path",type=Path)
    a=p.parse_args()
    with a.path.open(encoding="utf-8-sig",newline="") as f:
        rows=json.load(f) if a.path.suffix==".json" else list(csv.DictReader(f))
    print(json.dumps(analyze(rows),indent=2))
