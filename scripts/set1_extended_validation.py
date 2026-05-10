import random, math
from pathlib import Path

SET1=dict(BaseLot=0.03,BigRatio=0.12,SmallRatio=0.03,MaxActiveSections=2,StepPoints=150,MaxTotalLot=6,MaxNetLot=3,MinMarginLevelPercent=150,MaxDDPercent=50)
ACCOUNT=10000; LEVERAGE=200; CONTRACT=100000; MARGIN_PER_LOT=CONTRACT/LEVERAGE; STOP_OUT=50

def flr(x,s=0.01): return math.floor(x/s)*s

def scenario_move(kind,i,r,gap_mult):
    if kind=='trend_up': return 120 + (30 if i%10==0 else -20 if i%6==0 else 0)
    if kind=='trend_down': return -(120 + (30 if i%10==0 else -20 if i%6==0 else 0))
    if kind=='flat': return r.randint(-60,60)
    if kind=='flat_with_level_touch': return 170 if i%30==0 else r.randint(-40,40)
    if kind=='whipsaw': return 220 if i%2==0 else -220
    if kind=='spike': return (1300*gap_mult if i%35==0 else r.randint(-140,140))
    if kind=='gap': return (2200*gap_mult if i%75==0 else r.randint(-160,160))
    return r.randint(-260,260)

def run_path(kind,steps=10000,spread_mult=1.0,gap_mult=1.0,commission=0.0,swap=0.0,seed=1):
    r=random.Random(seed)
    base=SET1['BaseLot']
    initial_positions_count=2; initial_tail_lot=base
    tail=base; reserve=0; recovery=0; active=0
    floating=0; peak=ACCOUNT; min_margin=float('inf'); max_dd=0; closes=0; viol=0; stop=False
    used_margin_start=max(2*base*MARGIN_PER_LOT,0.01)
    price_moves_count=0; level_hits=0; sections_opened=0; floating_changes=0; recovery_close_lot_sum=0
    prev_floating=0
    for i in range(1,steps+1):
        mv=scenario_move(kind,i,r,gap_mult)
        if mv!=0: price_moves_count +=1
        if abs(mv)>=SET1['StepPoints']:
            level_hits +=1
            if active<SET1['MaxActiveSections'] and tail>=0.01:
                active+=1; sections_opened +=1
        big=flr(max(0.01,tail*SET1['BigRatio'])); small=flr(max(0.01,tail*SET1['SmallRatio']))
        total=2*base + active*(big+small)
        net=abs((base+active*small)-(base+active*big))
        used=max(total*MARGIN_PER_LOT,0.01)

        momentum=abs(mv)/100
        pullback=1.7 if (i%9==0 or i%14==0) else 1.0
        big_pnl=max(0,momentum-0.12)*big*14*pullback
        small_pnl=-max(0,momentum-0.03)*small*3
        costs=(big+small)*(SET1['StepPoints']*0.08*spread_mult + commission + swap)
        cycle=big_pnl+small_pnl-costs
        floating += cycle
        if abs(floating-prev_floating)>1e-9: floating_changes +=1
        prev_floating=floating

        eq=ACCOUNT+reserve+recovery+floating
        peak=max(peak,eq)
        dd=(peak-eq)/ACCOUNT*100
        max_dd=max(max_dd,dd)
        margin=eq/used*100
        min_margin=min(min_margin,margin)
        if margin<=STOP_OUT: stop=True

        if cycle>0 and active>0:
            closes +=1
            reserve += cycle*0.2; recovery += cycle*0.8
            loss=max(30,abs(mv))
            c=flr(min(tail,recovery/loss))
            if c>=0.01:
                recovery-=c*loss; tail=max(0,tail-c); recovery_close_lot_sum += c
            active=max(0,active-1)

        if total>SET1['MaxTotalLot'] or net>SET1['MaxNetLot'] or recovery<0 or reserve<0 or tail<0: viol+=1

    invalid=(initial_positions_count<=0 or initial_tail_lot<=0 or used_margin_start<=0 or price_moves_count<=0 or level_hits<=0 or sections_opened<=0 or floating_changes<=0)
    tail_reduction=round(base-tail,4)
    if invalid:
        status='INVALID_TEST_SETUP'
    elif stop:
        status='FAIL_STOP_OUT'
    elif max_dd>SET1['MaxDDPercent'] or min_margin<SET1['MinMarginLevelPercent']:
        status='FAIL_RISK_LIMIT'
    elif viol>0:
        status='FAIL_VIOLATION'
    elif closes<=0 or tail_reduction<=0 or reserve<=0 or recovery_close_lot_sum<=0:
        status='FAIL_NO_RECOVERY'
    else:
        status='PASS_RECOVERY'
    return dict(kind=kind,status=status,initial_positions_count=initial_positions_count,initial_tail_lot=initial_tail_lot,used_margin_start=round(used_margin_start,2),price_moves_count=price_moves_count,level_hits_count=level_hits,sections_opened_count=sections_opened,floating_pnl_changes_count=floating_changes,
                closes=closes,tail_end=round(tail,4),tail_reduction=tail_reduction,recovery_close_lot_sum=round(recovery_close_lot_sum,4),reserve=round(reserve,2),max_dd=round(max_dd,2),min_margin=round(min_margin,2),stop_out=stop,violations=viol,invalid_setup=invalid)

results=[]
for k in ['trend_up','trend_down','flat','flat_with_level_touch','whipsaw','spike','gap']:
    results.append(run_path(k,steps=10000,seed=42))
results.append(run_path('spike',steps=10000,spread_mult=2,seed=43))
results.append(run_path('spike',steps=10000,spread_mult=3,seed=44))
results.append(run_path('gap',steps=10000,gap_mult=2,seed=45))
results.append(run_path('spike',steps=10000,commission=3.5,swap=1.0,seed=46))

mc=[run_path('mc',steps=2000,seed=1000+i) for i in range(1000)]

out=Path('reports/tests/set1_extended_validation_report.md')
lines=['# SET-1 Extended Validation','',f'SET-1: {SET1}','']
lines.append('## 10,000-step scenario results')
for r in results:
    lines.append(f"- {r['kind']}: status={r['status']}, closes={r['closes']}, tail_end={r['tail_end']}, tail_reduction={r['tail_reduction']}, recovery_close_lot_sum={r['recovery_close_lot_sum']}, reserve={r['reserve']}, max_dd={r['max_dd']}%, min_margin={r['min_margin']}%, stop_out={r['stop_out']}, violations={r['violations']}")
    lines.append(f"  setup_checks: initial_positions_count={r['initial_positions_count']}, initial_tail_lot={r['initial_tail_lot']}, used_margin_start={r['used_margin_start']}, price_moves_count={r['price_moves_count']}, level_hits_count={r['level_hits_count']}, sections_opened_count={r['sections_opened_count']}, floating_pnl_changes_count={r['floating_pnl_changes_count']}")

vals=lambda k:[x[k] for x in mc]
invalid_runs=sum(1 for x in mc if x['status']=='INVALID_TEST_SETUP')
lines += ['','## 1,000 Monte-Carlo runs (2,000 steps each)',f"- invalid_setup_runs={invalid_runs}",f"- status_counts: PASS_RECOVERY={sum(1 for x in mc if x['status']=='PASS_RECOVERY')}, FAIL_NO_RECOVERY={sum(1 for x in mc if x['status']=='FAIL_NO_RECOVERY')}, FAIL_RISK_LIMIT={sum(1 for x in mc if x['status']=='FAIL_RISK_LIMIT')}, FAIL_STOP_OUT={sum(1 for x in mc if x['status']=='FAIL_STOP_OUT')}, FAIL_VIOLATION={sum(1 for x in mc if x['status']=='FAIL_VIOLATION')}",f"- closes avg={sum(vals('closes'))/len(mc):.2f}",f"- tail_end min/max/avg={min(vals('tail_end')):.4f}/{max(vals('tail_end')):.4f}/{sum(vals('tail_end'))/len(mc):.4f}",f"- tail_reduction avg={sum(vals('tail_reduction'))/len(mc):.4f}",f"- recovery_close_lot_sum avg={sum(vals('recovery_close_lot_sum'))/len(mc):.4f}",f"- reserve min/max/avg={min(vals('reserve')):.2f}/{max(vals('reserve')):.2f}/{sum(vals('reserve'))/len(mc):.2f}",f"- max_dd avg={sum(vals('max_dd'))/len(mc):.2f}%",f"- min_margin avg={sum(vals('min_margin'))/len(mc):.2f}%",f"- stop_out runs={sum(1 for x in mc if x['stop_out'])}",f"- violation runs={sum(1 for x in mc if x['violations']>0)}"]

overall='ACCEPTED' if all(r['status']=='PASS_RECOVERY' for r in results) else 'REJECTED'
lines += ['','## overall_set_status',overall]
out.write_text('\n'.join(lines),encoding='utf-8')
print('written',out)
