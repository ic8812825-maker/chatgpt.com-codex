from pathlib import Path
from risk_model import run

SET1=(0.03,0.12,0.03,2,150,6,3,150,50)
SCENARIOS=['trend_up','trend_down','flat','flat_with_level_touch','whipsaw','spike','gap']

def status(rr,p):
    if rr['invalid_setup']: return 'INVALID_TEST_SETUP'
    if rr['stop_out']: return 'FAIL_STOP_OUT'
    if rr['max_dd']>p[8] or rr['min_margin']<p[7]: return 'FAIL_RISK_LIMIT'
    if rr['violations']>0: return 'FAIL_VIOLATION'
    if rr['closes']<=0 or rr['tail_reduction']<=0 or rr['reserve']<=0 or rr['recovery_close_lot_sum']<=0: return 'FAIL_NO_RECOVERY'
    return 'PASS_RECOVERY'

results=[run(SET1,k,steps=10000,seed=42+i) for i,k in enumerate(SCENARIOS)]
results += [run(SET1,'spike',steps=10000,spread_mult=2,seed=143),run(SET1,'spike',steps=10000,spread_mult=3,seed=144),run(SET1,'gap',steps=10000,gap_mult=2,seed=145),run(SET1,'spike',steps=10000,commission=3.5,swap=1.0,seed=146)]
for r in results: r['status']=status(r,SET1)

mc=[run(SET1,'mc',steps=2000,seed=1000+i) for i in range(1000)]
mc_status=[status(r,SET1) for r in mc]
mc_pass_ratio=sum(1 for s in mc_status if s=='PASS_RECOVERY')/len(mc)

overall='ACCEPTED' if (
    all(r['status']=='PASS_RECOVERY' for r in results) and
    mc_pass_ratio>=0.95 and
    all(r['max_dd']<=SET1[8] for r in results)
) else 'REJECTED'

out=Path('reports/tests/set1_extended_validation_report.md')
L=['# SET-1 Extended Validation (Synchronized Model)','',f'SET-1: {SET1}','']
L.append('## 10,000-step scenario results')
for r in results:
    L.append(f"- {r['kind']}: status={r['status']}, closes={r['closes']}, tail_end={r['tail_end']}, tail_reduction={r['tail_reduction']}, recovery_close_lot_sum={r['recovery_close_lot_sum']}, reserve={r['reserve']}, max_dd={r['max_dd']}%, min_margin={r['min_margin']}%, stop_out={r['stop_out']}, violations={r['violations']}")
    L.append(f"  setup_checks: used_margin_start={r['used_margin_start']}, price_moves_count={r['price_moves_count']}, level_hits_count={r['level_hits_count']}, sections_opened_count={r['sections_opened_count']}, floating_pnl_changes_count={r['floating_pnl_changes_count']}")
vals=lambda k:[x[k] for x in mc]
L += ['','## 1,000 Monte-Carlo runs (2,000 steps each)',f"- mc_pass_recovery_ratio={mc_pass_ratio:.3f}",f"- status_counts: PASS_RECOVERY={sum(1 for s in mc_status if s=='PASS_RECOVERY')}, FAIL_NO_RECOVERY={sum(1 for s in mc_status if s=='FAIL_NO_RECOVERY')}, FAIL_RISK_LIMIT={sum(1 for s in mc_status if s=='FAIL_RISK_LIMIT')}, FAIL_STOP_OUT={sum(1 for s in mc_status if s=='FAIL_STOP_OUT')}, FAIL_VIOLATION={sum(1 for s in mc_status if s=='FAIL_VIOLATION')}, INVALID_TEST_SETUP={sum(1 for s in mc_status if s=='INVALID_TEST_SETUP')}",f"- closes avg={sum(vals('closes'))/len(mc):.2f}",f"- tail_end min/max/avg={min(vals('tail_end')):.4f}/{max(vals('tail_end')):.4f}/{sum(vals('tail_end'))/len(mc):.4f}",f"- tail_reduction avg={sum(vals('tail_reduction'))/len(mc):.4f}",f"- recovery_close_lot_sum avg={sum(vals('recovery_close_lot_sum'))/len(mc):.4f}",f"- reserve min/max/avg={min(vals('reserve')):.2f}/{max(vals('reserve')):.2f}/{sum(vals('reserve'))/len(mc):.2f}"]
L += ['','## overall_set_status',overall]
out.write_text('\n'.join(L),encoding='utf-8')
print('written',out)
