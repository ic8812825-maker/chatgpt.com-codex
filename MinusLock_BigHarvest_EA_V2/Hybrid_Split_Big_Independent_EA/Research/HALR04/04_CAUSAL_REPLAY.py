"""Causal episode activation and sampling from actual observed bid/ask."""
from bisect import bisect_left,bisect_right
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from datetime import date
from pathlib import Path
import csv
import json
import sys

from data_scan import DAY,FOLDS,HERE,MINUTE,MONTHS,T0,load_ticks


def record(ts,b,a,i):
    return (ts[i],b[i],a[i])


def snapshot(ts,b,a,i,anchor):
    # All indices end at the current observed quote.
    first=ts[i]-30*MINUTE
    points=[]
    for j in range(7):
        k=bisect_right(ts,first+j*5*MINUTE,0,i+1)-1
        if k>=0:
            points.append((b[k]+a[k])/2)
    current=(b[i]+a[i])/2
    opening=(anchor[1]+anchor[2])/2
    sign=1 if current>opening else -1
    return dict(spread=a[i]-b[i],range30=max(points)-min(points) if points else None,
                momentum=sign*(current-points[0]) if len(points)>1 else None,
                sign=sign,pretrade_observations=len(points))


def observations(ts,b,a,index,minutes,h):
    if minutes==0:
        end=bisect_right(ts,ts[index]+5*MINUTE,index,len(ts))
        return [record(ts,b,a,i) for i in range(index,min(end,index+h+1))]
    result=[record(ts,b,a,index)]
    step=minutes*MINUTE
    cursor=index
    for i in range(1,h+1):
        desired=ts[index]+step*i
        cursor=bisect_left(ts,desired,cursor+1)
        if cursor==len(ts) or ts[cursor]>=desired+min(step,5*MINUTE):
            break
        result.append(record(ts,b,a,cursor))
    return result


def s2(ts,b,a,month):
    horizon=FOLDS["horizon"]
    rows=[]
    counts=Counter()
    day_first,day_last=ts[0]//DAY,ts[-1]//DAY
    for day in range(day_first,day_last+1):
        if date.fromordinal(day+T0).weekday()>=5:
            continue
        counts["scheduled"]+=1
        anchor_time=day*DAY+8*60*MINUTE
        i=bisect_left(ts,anchor_time)
        if i==len(ts) or ts[i]>=anchor_time+5*MINUTE:
            counts["missing_anchor"]+=1
            continue
        opening=record(ts,b,a,i)
        starting_mid=b[i]+a[i]
        cutoff=bisect_left(ts,day*DAY+14*60*MINUTE,i+1)
        for j in range(i+1,cutoff):
            if abs(b[j]+a[j]-starting_mid)>=600:
                features=snapshot(ts,b,a,j,opening)
                counts["activated"]+=1
                for minutes in FOLDS["interval_minutes"]:
                    obs=observations(ts,b,a,j,minutes,horizon)
                    rows.append(dict(month=month,fold=MONTHS[month],scheme="S2",
                                     interval=minutes,id=f"{month}-scheduled-{day}",
                                     orientation=features["sign"],entry=opening,features=features,
                                     obs=obs,complete=len(obs)==horizon+1))
                break
        else:
            counts["not_activated"]+=1
    assert counts["scheduled"]==sum(counts[k] for k in ("missing_anchor","activated","not_activated"))
    return rows,counts


def s1(ts,b,a,month):
    # Same first-within-two-minute 30m grid as pinned HALR03.
    sampled=[]
    threshold=120000
    i=bisect_left(ts,ts[0]//(30*MINUTE)*(30*MINUTE))
    while i<len(ts):
        slot=ts[i]//(30*MINUTE)
        if ts[i]-slot*30*MINUTE<=threshold:
            sampled.append((slot,i))
        i=bisect_left(ts,(slot+1)*30*MINUTE,i+1)
    h=FOLDS["horizon"]
    start=0
    rows=[]
    counts=Counter()
    while start<len(sampled)-1:
        counts["scheduled"]+=1
        anchor=sampled[start][1]
        j=start+1
        while j<len(sampled) and sampled[j][0]-sampled[j-1][0]<=4:
            current=sampled[j][1]
            if abs(b[current]+a[current]-b[anchor]-a[anchor])>=600:
                counts["activated"]+=1
                window=sampled[j:j+h+1]
                intact=len(window)==h+1 and all(v[0]-u[0]<=4 for u,v in zip(window,window[1:]))
                if intact:
                    entry=record(ts,b,a,anchor)
                    features=snapshot(ts,b,a,current,entry)
                    rows.append(dict(month=month,fold=MONTHS[month],scheme="S1",interval=30,
                                     id=f"{month}-legacy-{j}",orientation=features["sign"],
                                     entry=entry,features=features,complete=True,
                                     obs=[record(ts,b,a,k) for _,k in window]))
                else:
                    counts["incomplete_excluded"]+=1
                start=j+2*h+1
                break
            j+=1
        else:
            counts["not_activated"]+=1
            start=j
    return rows,counts


def run_month(args):
    folder,month=args
    ts,b,a=load_ticks(folder,month)
    episodes,counts = [],[]
    for scheme,fn in (("S1",s1),("S2",s2)):
        result,c=fn(ts,b,a,month)
        episodes+=result
        for interval in sorted({r["interval"] for r in result} or {30}):
            q=[r for r in result if r["interval"]==interval]
            counts.append(dict(month=month,fold=MONTHS[month],scheme=scheme,interval=interval,
                               scheduled=c["scheduled"],activated=c["activated"],
                               no_activation=c["not_activated"],missing_anchor=c["missing_anchor"],
                               incomplete_excluded=c["incomplete_excluded"],
                               retained=len(q),complete=sum(r["complete"] for r in q),
                               retained_incomplete=sum(not r["complete"] for r in q)))
    return episodes,counts


def prepare(folder):
    all_episodes=[]
    counters=[]
    with ProcessPoolExecutor(2) as pool:
        for episodes,counts in pool.map(run_month,[(folder,m) for m in MONTHS]):
            all_episodes+=episodes
            counters+=counts
    (folder/"episodes.json").write_text(json.dumps(all_episodes,separators=(",",":"))+"\n")
    with (HERE/"04_SAMPLING_BIAS_REPORT.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(counters[0]),lineterminator="\n")
        w.writeheader()
        w.writerows(counters)
    return counters


if __name__=="__main__":
    q=prepare(Path(sys.argv[1]))
    print(len(q),"month/scheme/interval rows")
