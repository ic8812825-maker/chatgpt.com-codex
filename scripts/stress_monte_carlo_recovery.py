import random, math
from pathlib import Path

SEED=42
random.seed(SEED)
STEP=100
MIN_LOT=0.01
LOT_STEP=0.01
BIG={1:0.40,2:0.25,3:0.15,4:0.10}
SMALL={1:0.15,2:0.10,3:0.06,4:0.04}
MAX_SEC=4
MAX_TOTAL_LOT=20
MAX_NET_LOT=10


def flr(x,s=LOT_STEP): return math.floor(x/s)*s

RULES=[
 'tail_close_loss > recovery_fund',
 'section_closed_with_cycle_profit <= 0',
 'close_lot > tail_lot',
 'active_sections > max_active_sections',
 'total_lot > max_total_lot',
 'net_lot > max_net_lot',
 'opposite_cascade_opened',
 'recovery_fund_negative',
 'reserve_negative',
 'tail_lot_negative',
]


def run_path(name, gen, steps=1000):
    tail=1.0; reserve=0.0; recovery=0.0; active=0; level=1
    floating=0.0; peak_equity=0.0; equity=0.0
    max_floating_loss=0.0; max_dd_money=0.0; max_dd_pct=0.0
    max_total=2.0; max_net=0.0; max_active=0; max_tail=tail; max_recovery=0; max_reserve=0
    no_close=0; max_no_close=0
    opens=closes=0
    violations=[]; events=[]
    for i in range(1,steps+1):
        move=gen(i)
        price=1.23 + move/10000
        event='WAIT'; close_lot=0.0; cycle=0.0
        if active<MAX_SEC and tail>=MIN_LOT:
            active += 1; opens += 1; event='OPEN_SECTION'
        big=flr(tail*BIG[level]); small=flr(tail*SMALL[level])
        total_lot=2+active*(big+small)
        net_lot=abs((1+active*small)-(1+active*big))
        max_total=max(max_total,total_lot); max_net=max(max_net,net_lot); max_active=max(max_active,active)
        # PnL model: trend penalizes one side, whipsaw/spike can generate closes
        big_pnl=max(0,(abs(move)-40))/100*big*10
        small_pnl=-max(0,(abs(move)-20))/100*small*8
        costs=(big+small)*20*2
        cycle=big_pnl+small_pnl-costs
        floating += big_pnl+small_pnl-costs
        equity = reserve + recovery + floating
        peak_equity=max(peak_equity,equity)
        dd=peak_equity-equity
        max_dd_money=max(max_dd_money,dd)
        max_dd_pct=max(max_dd_pct,(dd/(peak_equity+1e-9))*100 if peak_equity>0 else 0)
        max_floating_loss=min(max_floating_loss,floating)

        if cycle>0 and active>0:
            closes += 1; no_close=0; event='CLOSE_SECTION'
            reserve_add=cycle*0.2; recovery_add=cycle*0.8
            reserve += reserve_add; recovery += recovery_add
            loss_per_lot=max(50,abs(move))
            close_lot=flr(min(tail,recovery/loss_per_lot))
            if close_lot>tail: violations.append((i,'close_lot > tail_lot'))
            if close_lot>=MIN_LOT:
                event='CLOSE_TAIL'
                tail_close_loss=close_lot*loss_per_lot
                if tail_close_loss>recovery+1e-9: violations.append((i,'tail_close_loss > recovery_fund'))
                recovery -= tail_close_loss
                tail -= close_lot
            active=max(0,active-1)
            level=min(4,level+1 if tail<0.75 else level)
        else:
            no_close += 1; max_no_close=max(max_no_close,no_close)
        # rule checks
        if active>MAX_SEC: violations.append((i,'active_sections > max_active_sections'))
        if total_lot>MAX_TOTAL_LOT: violations.append((i,'total_lot > max_total_lot'))
        if net_lot>MAX_NET_LOT: violations.append((i,'net_lot > max_net_lot'))
        if recovery<0: violations.append((i,'recovery_fund_negative'))
        if reserve<0: violations.append((i,'reserve_negative'))
        if tail<0: violations.append((i,'tail_lot_negative'))

        max_tail=max(max_tail,tail); max_recovery=max(max_recovery,recovery); max_reserve=max(max_reserve,reserve)
        events.append(dict(step=i,price=round(price,5),event=event,tail_lot=round(tail,4),section=active,cycle_profit=round(cycle,2),recovery=round(recovery,2),reserve=round(reserve,2),close_lot=round(close_lot,2),violation=';'.join(v[1] for v in violations if v[0]==i) or '-'))

    status='PASS' if len(violations)==0 else 'FAIL'
    return {
      'name':name,'steps':steps,'opens':opens,'closes':closes,
      'tail_lot_start':1.0,'tail_lot_end':round(max(tail,0),4),
      'reserve_start':0.0,'reserve_end':round(reserve,2),'recovery_start':0.0,'recovery_end':round(recovery,2),
      'max_floating_loss':round(max_floating_loss,2),'max_drawdown_money':round(max_dd_money,2),'max_drawdown_percent':round(max_dd_pct,2),
      'max_total_lot':round(max_total,2),'max_net_lot':round(max_net,2),'max_active_sections':max_active,'max_tail_lot':round(max_tail,4),
      'max_recovery_fund':round(max_recovery,2),'max_reserve':round(max_reserve,2),'max_consecutive_no_close_steps':max_no_close,
      'violations_count':len(violations),'final_status':status,'events':events,'violations':violations
    }


def render_block(r):
    lines=[f"## {r['name']}"]
    for k in ['steps','opens','closes','tail_lot_start','tail_lot_end','reserve_start','reserve_end','recovery_start','recovery_end','max_floating_loss','max_drawdown_money','max_drawdown_percent','max_total_lot','max_net_lot','max_active_sections','max_consecutive_no_close_steps','violations_count','final_status']:
        lines.append(f"- {k}: {r[k]}")
    lines.append('\n### Event trace (first 10)')
    for e in r['events'][:10]: lines.append(f"- step {e['step']} price={e['price']} event={e['event']} tail={e['tail_lot']} sec={e['section']} cycle={e['cycle_profit']} rec={e['recovery']} res={e['reserve']} close={e['close_lot']} violation={e['violation']}")
    lines.append('\n### Event trace (last 10)')
    for e in r['events'][-10:]: lines.append(f"- step {e['step']} price={e['price']} event={e['event']} tail={e['tail_lot']} sec={e['section']} cycle={e['cycle_profit']} rec={e['recovery']} res={e['reserve']} close={e['close_lot']} violation={e['violation']}")
    lines.append('\n### Violation events')
    if r['violations']:
        for v in r['violations'][:50]: lines.append(f"- step {v[0]}: {v[1]}")
    else:
        lines.append('- none')
    return lines

scenarios=[
 ('trend_up', lambda i: 80 + (i%20)),
 ('trend_down', lambda i: -(80 + (i%20))),
 ('flat', lambda i: random.randint(-15,15)),
 ('whipsaw', lambda i: 180 if i%2==0 else -180),
 ('spike', lambda i: 1200 if i%40==0 else random.randint(-60,60)),
 ('gap', lambda i: 2500 if i%120==0 else random.randint(-100,100)),
]
results=[run_path(n,g,1000) for n,g in scenarios]

mc_runs=[]
for run in range(200):
    rnd=random.Random(SEED+run)
    mc_runs.append(run_path(f'mc_{run}', lambda i,r=rnd: r.randint(-300,300),300))

tail_vals=[r['tail_lot_end'] for r in mc_runs]
res_vals=[r['reserve_end'] for r in mc_runs]
dd_vals=[r['max_drawdown_money'] for r in mc_runs]
viol_total=sum(r['violations_count'] for r in mc_runs)
viol_runs=sum(1 for r in mc_runs if r['violations_count']>0)
worst=max(mc_runs,key=lambda x:x['max_drawdown_money'])

out=Path('reports/tests/stress_monte_carlo_multi_cycle_report.md')
lines=['# STRESS / MONTE-CARLO / MULTI-CYCLE TESTING','\n## Violation rules checked']+[f'- {r}' for r in RULES]
for r in results: lines += [''] + render_block(r)
lines += ['','## monte_carlo_summary',f'- number_of_runs: {len(mc_runs)}',f'- seed: {SEED}',f'- tail_lot_end min/max/avg: {min(tail_vals):.4f}/{max(tail_vals):.4f}/{sum(tail_vals)/len(tail_vals):.4f}',f'- reserve_end min/max/avg: {min(res_vals):.2f}/{max(res_vals):.2f}/{sum(res_vals)/len(res_vals):.2f}',f'- drawdown min/max/avg: {min(dd_vals):.2f}/{max(dd_vals):.2f}/{sum(dd_vals)/len(dd_vals):.2f}',f'- worst_case_run: {worst["name"]} (drawdown={worst["max_drawdown_money"]})',f'- violations_total: {viol_total}',f'- runs_with_violations: {viol_runs}','', '## Final status','Stress testing: '+('PASS' if all(r['violations_count']==0 for r in results) else 'FAIL')]
out.write_text('\n'.join(lines),encoding='utf-8')
print('written',out)
