import random, math
from pathlib import Path

SET1=dict(BaseLot=0.03,BigRatio=0.12,SmallRatio=0.03,MaxActiveSections=2,StepPoints=150,MaxTotalLot=6,MaxNetLot=3,MinMarginLevelPercent=150,MaxDDPercent=50)
ACCOUNT=10000; LEVERAGE=200; CONTRACT=100000; MARGIN_PER_LOT=CONTRACT/LEVERAGE; STOP_OUT=50

def flr(x,s=0.01): return math.floor(x/s)*s

def run_path(kind,steps=10000,spread_mult=1.0,gap_mult=1.0,commission=0.0,swap=0.0,seed=1):
    r=random.Random(seed)
    tail=SET1['BaseLot']; reserve=0; recovery=0; active=0; level=1
    floating=0; peak=ACCOUNT; min_margin=9999; max_dd=0; closes=0; viol=0; stop=False
    for i in range(1,steps+1):
        if kind=='trend_up': mv=140 + (15 if i%13==0 else -10 if i%7==0 else 0)
        elif kind=='trend_down': mv=-(140 + (15 if i%13==0 else -10 if i%7==0 else 0))
        elif kind=='flat': mv=r.randint(-35,35)
        elif kind=='whipsaw': mv=220 if i%2==0 else -220
        elif kind=='spike': mv=(1400*gap_mult if i%55==0 else r.randint(-100,100))
        elif kind=='gap': mv=(2200*gap_mult if i%120==0 else r.randint(-120,120))
        else: mv=r.randint(-250,250)
        if active<SET1['MaxActiveSections'] and tail>=0.01: active+=1
        big=flr(tail*SET1['BigRatio']); small=flr(tail*SET1['SmallRatio'])
        total=2*SET1['BaseLot']+active*(big+small)
        net=abs((SET1['BaseLot']+active*small)-(SET1['BaseLot']+active*big))
        used=total*MARGIN_PER_LOT
        momentum=abs(mv)/100
        signal=1 if i%9 in (0,1,2) else -1
        big_pnl=max(0,momentum-0.2)*big*(14 if signal>0 else 6)
        small_pnl=-max(0,momentum-0.1)*small*(4 if signal>0 else 2)
        costs=(big+small)*SET1['StepPoints']*0.25*spread_mult + commission*(big+small)+swap*(big+small)
        cycle=big_pnl+small_pnl-costs
        floating+=cycle
        eq=ACCOUNT+reserve+recovery+floating
        peak=max(peak,eq)
        dd=(peak-eq)/ACCOUNT*100
        max_dd=max(max_dd,dd)
        margin=eq/used*100 if used>0 else 9999
        min_margin=min(min_margin,margin)
        if margin<=STOP_OUT: stop=True
        if cycle>0 and active>0:
            closes+=1; reserve+=cycle*0.2; recovery+=cycle*0.8
            loss=max(40,abs(mv)); c=flr(min(tail,recovery/loss))
            if c>=0.01: recovery-=c*loss; tail=max(0,tail-c)
            active=max(0,active-1)
        if total>SET1['MaxTotalLot'] or net>SET1['MaxNetLot'] or recovery<0 or reserve<0 or tail<0: viol+=1
    return dict(kind=kind,steps=steps,closes=closes,tail_end=round(tail,4),tail_reduction=round(SET1['BaseLot']-tail,4),reserve=round(reserve,2),max_dd=round(max_dd,2),min_margin=round(min_margin,2),stop_out=stop,violations=viol)

results=[]
for k in ['trend_up','trend_down','flat','whipsaw','spike','gap']:
    results.append(run_path(k,steps=10000,seed=42))
# stress variants
results.append(run_path('spike',steps=10000,spread_mult=2,seed=43))
results.append(run_path('spike',steps=10000,spread_mult=3,seed=44))
results.append(run_path('gap',steps=10000,gap_mult=2,seed=45))
results.append(run_path('spike',steps=10000,commission=3.5,swap=1.0,seed=46))

mc=[]
for i in range(1000):
    mc.append(run_path('mc',steps=2000,seed=1000+i))

out=Path('reports/tests/set1_extended_validation_report.md')
lines=['# SET-1 Extended Validation','',f"SET-1: {SET1}",'']
lines.append('## 10,000-step scenario results')
for r in results:
    lines.append(f"- {r['kind']}: closes={r['closes']}, tail_end={r['tail_end']}, tail_reduction={r['tail_reduction']}, reserve={r['reserve']}, max_dd={r['max_dd']}%, min_margin={r['min_margin']}%, stop_out={r['stop_out']}, violations={r['violations']}")

vals=lambda k:[x[k] for x in mc]
lines += ['','## 1,000 Monte-Carlo runs (2,000 steps each)',f"- closes avg={sum(vals('closes'))/len(mc):.2f}",f"- tail_end min/max/avg={min(vals('tail_end')):.4f}/{max(vals('tail_end')):.4f}/{sum(vals('tail_end'))/len(mc):.4f}",f"- reserve min/max/avg={min(vals('reserve')):.2f}/{max(vals('reserve')):.2f}/{sum(vals('reserve'))/len(mc):.2f}",f"- max_dd avg={sum(vals('max_dd'))/len(mc):.2f}%",f"- min_margin avg={sum(vals('min_margin'))/len(mc):.2f}%",f"- stop_out runs={sum(1 for x in mc if x['stop_out'])}",f"- violation runs={sum(1 for x in mc if x['violations']>0)}"]

lines += ['','## Verdict','SET-1 accepted for PAPER TEST ONLY if stop_out stays False and violations=0 in monitored scenarios.']
out.write_text('\n'.join(lines),encoding='utf-8')
print('written',out)
