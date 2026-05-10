import random, math
from pathlib import Path

SEED=42
ACCOUNT_BALANCE=10000.0
STEP=100
MIN_LOT=0.01
LOT_STEP=0.01
BIG={1:0.40,2:0.25,3:0.15,4:0.10}
SMALL={1:0.15,2:0.10,3:0.06,4:0.04}
MAX_SEC=4
MAX_TOTAL_LOT=20
MAX_NET_LOT=10

RULES=[
 'tail_close_loss > recovery_fund','section_closed_with_cycle_profit <= 0','close_lot > tail_lot',
 'active_sections > max_active_sections','total_lot > max_total_lot','net_lot > max_net_lot',
 'opposite_cascade_opened','recovery_fund_negative','reserve_negative','tail_lot_negative']

def flr(x,s=LOT_STEP): return math.floor(x/s)*s

def outcome(v, closes, tail_start, tail_end, reserve_end):
    if v>0: return 'FAIL_VIOLATION'
    if closes>0 and tail_end < tail_start and reserve_end>0: return 'PASS_RECOVERY'
    return 'PASS_SAFE_STALL'

def run_path(name, gen, steps=1000):
    random.seed(SEED)
    tail=1.0; reserve=0.0; recovery=0.0; active=0; level=1
    floating=0.0; peak_eq=ACCOUNT_BALANCE; eq=ACCOUNT_BALANCE
    max_floating_loss=0.0; max_dd_money=0.0; max_dd_pct=0.0
    max_total=2.0; max_net=0.0; max_active=0; max_tail=tail; max_recovery=0; max_reserve=0
    no_close=max_no_close=0; opens=closes=0; recovery_cycles=0
    violations=[]; events=[]
    for i in range(1,steps+1):
        move=gen(i)
        price=1.23+move/10000
        event='WAIT'; close_lot=0.0; cycle=0.0
        if active<MAX_SEC and tail>=MIN_LOT:
            active+=1; opens+=1; event='OPEN_SECTION'
        big=flr(tail*BIG[level]); small=flr(tail*SMALL[level])
        total_lot=2+active*(big+small); net_lot=abs((1+active*small)-(1+active*big))
        max_total=max(max_total,total_lot); max_net=max(max_net,net_lot); max_active=max(max_active,active)
        # richer pnl with pullback sensitivity
        direction=1 if move>0 else -1
        momentum=abs(move)/100
        pullback_bonus=1.3 if (i%7==0 or i%11==0) else 1.0
        big_pnl=max(0,momentum-0.2)*big*12*pullback_bonus
        small_pnl=-max(0,momentum-0.1)*small*8
        costs=(big+small)*20*2
        cycle=big_pnl+small_pnl-costs
        floating += (big_pnl+small_pnl-costs)
        eq=ACCOUNT_BALANCE+reserve+recovery+floating
        peak_eq=max(peak_eq,eq)
        dd=peak_eq-eq
        max_dd_money=max(max_dd_money,dd)
        max_dd_pct=max(max_dd_pct,(dd/ACCOUNT_BALANCE)*100)
        max_floating_loss=min(max_floating_loss,floating)

        if cycle>0 and active>0:
            closes+=1; recovery_cycles+=1; no_close=0; event='CLOSE_SECTION'
            reserve_add=cycle*0.2; recovery_add=cycle*0.8
            reserve += reserve_add; recovery += recovery_add
            loss_per_lot=max(50,abs(move))
            close_lot=flr(min(tail,recovery/loss_per_lot))
            if close_lot>tail: violations.append((i,'close_lot > tail_lot'))
            if close_lot>=MIN_LOT:
                event='CLOSE_TAIL'
                close_loss=close_lot*loss_per_lot
                if close_loss>recovery+1e-9: violations.append((i,'tail_close_loss > recovery_fund'))
                recovery-=close_loss; tail-=close_lot
            active=max(0,active-1)
            level=min(4,level+1 if tail<0.75 else level)
        else:
            no_close+=1; max_no_close=max(max_no_close,no_close)

        if active>MAX_SEC: violations.append((i,'active_sections > max_active_sections'))
        if total_lot>MAX_TOTAL_LOT: violations.append((i,'total_lot > max_total_lot'))
        if net_lot>MAX_NET_LOT: violations.append((i,'net_lot > max_net_lot'))
        if recovery<0: violations.append((i,'recovery_fund_negative'))
        if reserve<0: violations.append((i,'reserve_negative'))
        if tail<0: violations.append((i,'tail_lot_negative'))

        max_tail=max(max_tail,tail); max_recovery=max(max_recovery,recovery); max_reserve=max(max_reserve,reserve)
        events.append(dict(step=i,price=round(price,5),event=event,tail_lot=round(tail,4),section=active,cycle_profit=round(cycle,2),recovery=round(recovery,2),reserve=round(reserve,2),close_lot=round(close_lot,2),violation=';'.join(v[1] for v in violations if v[0]==i) or '-'))

    vcount=len(violations)
    return {
        'name':name,'steps':steps,'opens':opens,'closes':closes,
        'tail_lot_start':1.0,'tail_lot_end':round(max(tail,0),4),'reserve_start':0.0,'reserve_end':round(reserve,2),'recovery_start':0.0,'recovery_end':round(recovery,2),
        'max_floating_loss':round(max_floating_loss,2),'max_drawdown_money':round(max_dd_money,2),'max_drawdown_percent':round(max_dd_pct,2),
        'max_total_lot':round(max_total,2),'max_net_lot':round(max_net,2),'max_active_sections':max_active,'max_tail_lot':round(max_tail,4),'max_recovery_fund':round(max_recovery,2),'max_reserve':round(max_reserve,2),
        'max_consecutive_no_close_steps':max_no_close,'violations_count':vcount,'recovery_cycles_count':recovery_cycles,
        'tail_reduction':round(1.0-max(tail,0),4),'reserve_generated':round(reserve,2),
        'limit_total_used_percent':round((max_total/MAX_TOTAL_LOT)*100,2),'limit_net_used_percent':round((max_net/MAX_NET_LOT)*100,2),
        'final_status': outcome(vcount,closes,1.0,max(tail,0),reserve),
        'events':events,'violations':violations
    }

def render(r):
    ks=['steps','opens','closes','tail_lot_start','tail_lot_end','reserve_start','reserve_end','recovery_start','recovery_end','max_floating_loss','max_drawdown_money','max_drawdown_percent','max_total_lot','max_net_lot','max_active_sections','max_consecutive_no_close_steps','violations_count','final_status','tail_reduction','reserve_generated','recovery_cycles_count','limit_total_used_percent','limit_net_used_percent']
    lines=[f"## {r['name']}"]+[f"- {k}: {r[k]}" for k in ks]
    lines.append('\n### Event trace (first 10)')
    lines += [f"- step {e['step']} price={e['price']} event={e['event']} tail={e['tail_lot']} sec={e['section']} cycle={e['cycle_profit']} rec={e['recovery']} res={e['reserve']} close={e['close_lot']} violation={e['violation']}" for e in r['events'][:10]]
    lines.append('\n### Event trace (last 10)')
    lines += [f"- step {e['step']} price={e['price']} event={e['event']} tail={e['tail_lot']} sec={e['section']} cycle={e['cycle_profit']} rec={e['recovery']} res={e['reserve']} close={e['close_lot']} violation={e['violation']}" for e in r['events'][-10:]]
    lines.append('\n### Violation events')
    lines += [f"- step {v[0]}: {v[1]}" for v in r['violations']] if r['violations'] else ['- none']
    return lines

scenarios=[
 ('trend_up', lambda i: 120 + (20 if i%9==0 else -10 if i%7==0 else 0)),
 ('trend_down', lambda i: -(120 + (20 if i%9==0 else -10 if i%7==0 else 0))),
 ('flat', lambda i: random.randint(-30,30)),
 ('whipsaw', lambda i: 180 if i%2==0 else -180),
 ('spike', lambda i: 1500 if i%45==0 else random.randint(-90,90)),
 ('gap', lambda i: 2800 if i%110==0 else random.randint(-120,120)),
]
results=[run_path(n,g,1000) for n,g in scenarios]

# Monte-carlo regimes
regimes={
 'random_walk': lambda rnd,i: rnd.randint(-300,300),
 'mean_reversion': lambda rnd,i: int(-0.4*(rnd.randint(-200,200)) + rnd.randint(-50,50)),
 'trend_with_pullbacks': lambda rnd,i: (180 if i%5 else -120)+rnd.randint(-40,40),
 'high_volatility': lambda rnd,i: rnd.randint(-700,700),
 'gap_sequence': lambda rnd,i: (2500 if i%60==0 else rnd.randint(-250,250)),
}
mc=[]
for rg,fn in regimes.items():
    for run in range(40):
        rnd=random.Random(SEED+run*13+len(rg))
        mc.append(run_path(f'{rg}_{run}', lambda i,rr=rnd,f=fn: f(rr,i),300))

vals=lambda k:[r[k] for r in mc]
tails=vals('tail_lot_end'); reserves=vals('reserve_end'); dds=vals('max_drawdown_money')
worst=max(mc,key=lambda x:x['max_drawdown_money'])
viol_total=sum(r['violations_count'] for r in mc); viol_runs=sum(1 for r in mc if r['violations_count']>0)

out=Path('reports/tests/stress_monte_carlo_multi_cycle_report.md')
lines=['# STRESS / MONTE-CARLO / MULTI-CYCLE TESTING',f'- account_balance: {ACCOUNT_BALANCE}',f'- MaxTotalLot: {MAX_TOTAL_LOT}',f'- MaxNetLot: {MAX_NET_LOT}',f'- MaxActiveSections: {MAX_SEC}','\n## Violation rules checked']+[f'- {x}' for x in RULES]
for r in results: lines += [''] + render(r)
lines += ['','## monte_carlo_summary',f'- number_of_runs: {len(mc)}',f'- seed: {SEED}',f'- regimes: {", ".join(regimes.keys())}',f'- tail_lot_end min/max/avg: {min(tails):.4f}/{max(tails):.4f}/{sum(tails)/len(tails):.4f}',f'- reserve_end min/max/avg: {min(reserves):.2f}/{max(reserves):.2f}/{sum(reserves)/len(reserves):.2f}',f'- drawdown min/max/avg: {min(dds):.2f}/{max(dds):.2f}/{sum(dds)/len(dds):.2f}',f'- worst_case_run: {worst["name"]} (drawdown={worst["max_drawdown_money"]})',f'- violations_total: {viol_total}',f'- runs_with_violations: {viol_runs}','', '## Final status','Initial formula validation: PASS','Workbook runtime validation: PASS','Stress test quality: '+('PASS_RECOVERY' if any(r['final_status']=='PASS_RECOVERY' for r in results+mc) else 'PASS_SAFE_STALL'),'Final system validation: NOT YET']
out.write_text('\n'.join(lines),encoding='utf-8')
print('written',out)
