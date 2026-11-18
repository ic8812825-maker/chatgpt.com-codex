"""Read anonymized execution events; never connects to a broker."""
import argparse
import csv
from datetime import datetime
from decimal import Decimal,InvalidOperation
import json
from pathlib import Path
from statistics import mean

EVENTS={"SEND","ACK","FILL","REJECT","CANCEL_SENT","CANCEL_ACK","UNKNOWN",
        "RESTART","RECONCILE","MARGIN","STOP_OUT","SWAP"}


def time(value):
    d=datetime.fromisoformat(value.replace("Z","+00:00"))
    if d.utcoffset() is None:
        raise ValueError("timestamp requires explicit UTC offset")
    return d


def dec(event,k,default=None):
    val=event.get(k)
    if val in (None,""):
        if default is None:
            raise ValueError(f"missing {k}")
        return Decimal(default)
    out=Decimal(str(val))
    if not out.is_finite():
        raise ValueError(f"nonfinite {k}")
    return out


def percentile(values,p):
    if not values:
        return None
    from math import ceil
    return sorted(values)[max(0,ceil(p*len(values))-1)]


def summarize(rows):
    sent={}
    deal=set()
    remaining={}
    unresolved=set()
    cancel_pending=set()
    done=set()
    clocks=[]
    slips=[]
    lots=[]
    rejections=partials=restarts=stops=margin_events=cancel_races=0
    fees=swap=Decimal(0)
    last=None
    for e in rows:
        t=time(e["timestamp"])
        kind=e["event"]
        if kind not in EVENTS or last is not None and t<last:
            raise ValueError(f"unknown event or reversed wall clock: {kind}")
        last=t
        key=e.get("order_id")
        if kind=="SEND":
            if not key or key in sent:
                raise ValueError("missing or reused order ID")
            qty=dec(e,"lots")
            bid,ask=dec(e,"bid"),dec(e,"ask")
            side=e.get("side")
            if qty<=0 or bid<=0 or ask<bid or side not in ("BUY","SELL"):
                raise ValueError("invalid order or bid ask")
            sent[key]=(t,side,bid,ask)
            remaining[key]=qty
            unresolved.add(key)
        elif kind in ("ACK","FILL","REJECT","CANCEL_SENT","CANCEL_ACK","UNKNOWN","RECONCILE"):
            if key not in sent or key in done:
                raise ValueError(f"unmatched or terminal order: {key}")
            if kind=="FILL":
                qty=dec(e,"lots")
                unique=e.get("deal_id")
                if not unique or unique in deal or qty<=0 or qty>remaining[key]:
                    raise ValueError("duplicate or inconsistent fill")
                fill_time,side,bid,ask=sent[key]
                price=dec(e,"price")
                if price<=0:
                    raise ValueError("invalid fill price")
                deal.add(unique)
                remaining[key]-=qty
                clocks.append((t-fill_time).total_seconds()*1000)
                slips.append(float((price-ask if side=="BUY" else bid-price)/Decimal(".00001")))
                lots.append(float(qty))
                fees+=dec(e,"commission","0")
                if key in cancel_pending:
                    cancel_races+=1
                if remaining[key]:
                    partials+=1
                else:
                    done.add(key)
                    unresolved.discard(key)
                    cancel_pending.discard(key)
            elif kind=="REJECT" or kind=="CANCEL_ACK":
                rejections+=kind=="REJECT"
                done.add(key)
                unresolved.discard(key)
                cancel_pending.discard(key)
            elif kind=="CANCEL_SENT":
                cancel_pending.add(key)
            elif kind=="UNKNOWN":
                unresolved.add(key)
            elif kind=="RECONCILE":
                # Open status remains live; a terminal snapshot can discharge only
                # a confirmed cancellation/rejection, never invent a missing fill.
                if e.get("status") in ("CANCELLED","REJECTED"):
                    done.add(key)
                    unresolved.discard(key)
                    cancel_pending.discard(key)
        elif kind=="RESTART":
            restarts+=1
            unresolved.update(set(sent)-done)
        elif kind=="SWAP":
            swap+=dec(e,"cash")
        elif kind in ("MARGIN","STOP_OUT"):
            dec(e,"margin")
            dec(e,"equity")
            margin_events+=1
            stops+=kind=="STOP_OUT"
    return dict(orders=len(sent),confirmed_deals=len(deal),partial_fills=partials,
                unresolved_orders=len(unresolved),rejections=rejections,cancel_race_fills=cancel_races,
                restarts=restarts,margin_events=margin_events,stopouts=stops,
                commission=str(fees),cash_swap=str(swap),
                median_confirmed_send_to_fill_ms=percentile(clocks,.5),
                p95_confirmed_send_to_fill_ms=percentile(clocks,.95),
                p95_signed_slippage_points=percentile(slips,.95),
                larger_observed_single_fill_lots=max(lots,default=None),
                guaranteed_capacity=None,guaranteed_delay=None)


def load(path):
    with path.open(encoding="utf-8-sig",newline="") as f:
        return json.load(f) if path.suffix.lower()==".json" else list(csv.DictReader(f))


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("path",type=Path)
    cfg=p.parse_args()
    print(json.dumps(summarize(load(cfg.path)),indent=2))
