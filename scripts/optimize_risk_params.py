from pathlib import Path
from risk_model import run

cands=[(0.02,0.10,0.02,1,150,4,2,120,60),(0.03,0.12,0.03,2,150,6,3,150,50),(0.04,0.12,0.03,2,180,6,3,150,60),(0.05,0.14,0.04,2,180,8,4,120,60),(0.03,0.14,0.03,2,180,6,3,120,60)]
scenarios=['trend_up_clean','trend_down_clean','trend_up_with_pullbacks','trend_down_with_pullbacks','flat_with_level_touch','whipsaw','spike','gap']

def st(rr,p,allow_stall=False):
    if rr['invalid_setup']: return 'INVALID_TEST_SETUP'
    if rr['stop_out']: return 'FAIL_STOP_OUT'
    if rr['max_dd']>p[8] or rr['min_margin']<p[7]: return 'FAIL_RISK_LIMIT'
    if rr['violations']>0: return 'FAIL_VIOLATION'
    if rr['closes']<=0 or rr['tail_reduction']<=0 or rr['reserve']<=0 or rr['recovery_close_lot_sum']<=0:
        return 'PASS_SAFE_STALL' if allow_stall else 'FAIL_NO_RECOVERY'
    return 'PASS_RECOVERY'

rows=[]
for p in cands:
    res=[]
    for i,s in enumerate(scenarios):
        rr=run(p,s,steps=2500,seed=42+i)
        rr['status']=st(rr,p,allow_stall=s in ('trend_up_clean','trend_down_clean'))
        res.append(rr)
    mc=[run(p,'mc',steps=800,seed=1000+i) for i in range(80)]
    mc_ratio=sum(1 for r in mc if st(r,p)=='PASS_RECOVERY')/len(mc)
    invalid_mand=any(r['status']=='INVALID_TEST_SETUP' for r in res)
    fail_stop=any(r['status']=='FAIL_STOP_OUT' for r in res)
    fail_viol=any(r['status']=='FAIL_VIOLATION' for r in res)
    maxdd_ok=all(r['max_dd']<=p[8] for r in res)
    ok=(not invalid_mand and not fail_stop and not fail_viol and maxdd_ok and mc_ratio>=0.95)
    score=sum(r['tail_reduction'] for r in res)*100+sum(r['reserve'] for r in res)*0.1-max(r['max_dd'] for r in res)
    rows.append((p,ok,mc_ratio,score,res))
rows=sorted(rows,key=lambda x:(x[1],x[3]),reverse=True)
acc=[r for r in rows if r[1]]
out=Path('reports/tests/risk_parameter_optimization_report.md')
L=['# Risk Parameter Optimization Report (Synchronized Model)','',f'- candidates_evaluated: {len(cands)}',f'- accepted_sets_found: {len(acc)}','',
'## accept-gate','- no INVALID_TEST_SETUP in mandatory scenarios','- no FAIL_STOP_OUT','- no FAIL_VIOLATION','- max_dd <= MaxDDPercent in all stress variants','- Monte-Carlo PASS_RECOVERY >= 95%','']
for i,(p,ok,mc,score,res) in enumerate(rows,1):
    L += [f"## SET-{i} ({'ACCEPTED' if ok else 'REJECTED'})",f"- params: {p}",f"- mc_pass_recovery_ratio={mc:.3f}, score={score:.2f}"]
    for rr in res:
        L.append(f"  - {rr['kind']}: {rr['status']}, closes={rr['closes']}, tail_reduction={rr['tail_reduction']}, reserve={rr['reserve']}, max_dd={rr['max_dd']}, min_margin={rr['min_margin']}")
    L.append('')
L += ['## overall_set_status','ACCEPTED' if acc else 'REJECTED']
out.write_text('\n'.join(L),encoding='utf-8')
print('written',out,'accepted',len(acc))
