#!/usr/bin/env python3
"""Aggregated fail-closed validator for every Stage 3.1.4 proof domain."""
from pathlib import Path
import importlib.util,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Tools'))
spec=importlib.util.spec_from_file_location('lawtests',ROOT/'Tests/test_stage_3_1_4_three_laws.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
from three_laws_oracle import D,Side,projected_profit
BLOCKERS=['RESERVE_CATCHUP_ANALYTIC_FAIL','RESERVE_CATCHUP_MONEY_FAIL','RESERVE_CATCHUP_LEVEL_PATH_FAIL','RECOVERY_SLOPE_FAIL','RECOVERY_POINTWISE_MONOTONICITY_FAIL','RECOVERY_EVENT_MONOTONICITY_FAIL','SPREAD_MODEL_FAIL','BID_ASK_SIDE_MODEL_FAIL','NEW_FAR_COMPRESSION_FAIL','NEXT_BIG_GROSS_COMPRESSION_FAIL','GROSS_COMPRESSION_FAIL','RISK_COMPRESSION_UNPROVEN','Q_BOUND_FAIL','Q_DOMAIN_UNPROVEN','DISCRETE_FINITE_TERMINATION_FAIL','ROUNDING_PATHOLOGY_UNHANDLED','UP_DOWN_PARITY_FAIL','COUNTEREXAMPLE_SUITE_FAIL']

def aggregate():
 c={k:0 for k in BLOCKERS}
 matrix=t.run_matrix();deficits=t.deficit_matrix();cost_total,cost_pass=t.cost_matrix();broker_total,broker_pass=t.broker_matrix();event_total,event_pass=t.event_matrix();risk_total,risk_pass=t.risk_matrix();q=t.q_matrix();comp=t.compression_matrix();gross_total,gross_pass=t.gross_domain_matrix();caught=t.counterexamples()
 b=t.broker();buy=projected_profit(Side.BUY,D('1'),b.ask0,b.bid0,b.ask0,b.tick_size,b.tick_value_profit,b.tick_value_loss);sell=projected_profit(Side.SELL,D('1'),b.bid0,b.bid0,b.ask0,b.tick_size,b.tick_value_profit,b.tick_value_loss)
 c['RESERVE_CATCHUP_ANALYTIC_FAIL']=int(not all(x['lot_catch_up'] for x in deficits.values()))
 c['RESERVE_CATCHUP_MONEY_FAIL']=int(not (all(x['money_catch_up'] for n,x in deficits.items() if n!='IMPOSSIBLE') and not deficits['IMPOSSIBLE']['money_catch_up'] and cost_total==cost_pass))
 c['RESERVE_CATCHUP_LEVEL_PATH_FAIL']=int(not all(x['coverage_path']['coverage_monotone'] for x in deficits.values()))
 c['RECOVERY_SLOPE_FAIL']=int(matrix<200);c['RECOVERY_POINTWISE_MONOTONICITY_FAIL']=int(matrix<200)
 c['RECOVERY_EVENT_MONOTONICITY_FAIL']=int(event_total!=event_pass or event_total<11)
 c['SPREAD_MODEL_FAIL']=int(not caught.get('SpreadZeroPass_RealSpreadFail'))
 c['BID_ASK_SIDE_MODEL_FAIL']=int(not (buy<0 and sell<0 and b.ask0==b.bid0+b.spread_price))
 c['NEW_FAR_COMPRESSION_FAIL']=int(comp['total']!=comp['passed']);c['NEXT_BIG_GROSS_COMPRESSION_FAIL']=c['NEW_FAR_COMPRESSION_FAIL']
 c['GROSS_COMPRESSION_FAIL']=int(gross_total!=gross_pass or comp['total']!=comp['passed'])
 c['RISK_COMPRESSION_UNPROVEN']=int(risk_total!=risk_pass or risk_total<4 or comp['total']!=comp['passed'])
 c['Q_BOUND_FAIL']=int(not q['pass']);c['Q_DOMAIN_UNPROVEN']=int(q['system_q_theorem']!='PASS' or q['transitions']<24)
 c['DISCRETE_FINITE_TERMINATION_FAIL']=int(comp['total']!=comp['passed'])
 c['ROUNDING_PATHOLOGY_UNHANDLED']=int(not all(caught.get(x) for x in ('CompressionRawPass_NormalizedFail','FiniteContinuousPass_DiscreteFail')))
 c['UP_DOWN_PARITY_FAIL']=int(broker_total!=broker_pass or broker_total<12)
 c['COUNTEREXAMPLE_SUITE_FAIL']=int(len(caught)<14 or not all(caught.values()))
 return c,{'AUTOMATED_MATRIX_CASES':matrix,'COST_SCENARIOS_TOTAL':cost_total,'BROKER_SCENARIOS_TOTAL':broker_total,'EVENT_SCENARIOS_TOTAL':event_total,'RISK_SCENARIOS_TOTAL':risk_total,'COMPRESSION_MATRIX_CASES':comp['total'],'GROSS_DOMAIN_CASES':gross_total,'Q_TRANSITIONS':q['transitions'],'OBSERVED_Q_MAX':q['observed_q_max'],'POLICY_Q_CAP':q['policy_q_cap'],'COUNTEREXAMPLES_TOTAL':len(caught),'COUNTEREXAMPLES_CAUGHT':sum(caught.values())}

def main():
 c,stats=aggregate()
 for k,v in c.items():print(f'{k}={v}')
 for k,v in stats.items():print(f'{k}={v}')
 print('BROKER_MODEL_BID_ASK='+('PASS' if not c['BID_ASK_SIDE_MODEL_FAIL'] else 'FAIL'))
 print('SPREAD_MODEL='+('PASS' if not c['SPREAD_MODEL_FAIL'] else 'FAIL'))
 print('RESERVE_LEVEL_PATH='+('PASS' if not c['RESERVE_CATCHUP_LEVEL_PATH_FAIL'] else 'FAIL'))
 print('RESERVE_MONEY_DOMAIN='+('PASS' if not c['RESERVE_CATCHUP_MONEY_FAIL'] else 'FAIL'))
 print('RECOVERY_POINTWISE_DOMAIN='+('PASS' if not c['RECOVERY_POINTWISE_MONOTONICITY_FAIL'] else 'FAIL'))
 print('RECOVERY_EVENT_DOMAIN='+('PASS' if not c['RECOVERY_EVENT_MONOTONICITY_FAIL'] else 'FAIL'))
 print('GROSS_COMPRESSION_DOMAIN='+('PASS' if not c['GROSS_COMPRESSION_FAIL'] else 'FAIL'))
 print('RISK_COMPRESSION_DOMAIN='+('PASS' if not c['RISK_COMPRESSION_UNPROVEN'] else 'FAIL'))
 print('Q_BOUND='+('PASS' if not c['Q_BOUND_FAIL'] and not c['Q_DOMAIN_UNPROVEN'] else 'FAIL'))
 print('FINITE_GRID_RANK='+('PASS' if not c['DISCRETE_FINITE_TERMINATION_FAIL'] else 'FAIL'))
 fail=[k for k,v in c.items() if v];print('BLOCKING_COUNTERS='+(','.join(fail) if fail else 'NONE'));print('STAGE_3_1_4_VALIDATION='+('FAIL' if fail else 'PASS'));return bool(fail)
if __name__=='__main__':raise SystemExit(main())
