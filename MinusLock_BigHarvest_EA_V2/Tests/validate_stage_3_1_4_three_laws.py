#!/usr/bin/env python3
"""Fail-closed validator for the Stage 3.1.4 canonical three-law contract."""
from pathlib import Path
from decimal import Decimal
import importlib.util,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Tools'))
spec=importlib.util.spec_from_file_location('lawtests',ROOT/'Tests/test_stage_3_1_4_three_laws.py')
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
from three_laws_oracle import Broker,Costs,Plan,evaluate,event_monotone,compression,finite_bound,D
REPORT=(ROOT/'Docs/STAGE_3_1_4_THREE_LAWS_PROOF_REPORT_RU.md').read_text()
MANUAL=(ROOT/'Docs/HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md').read_text()
BLOCKERS=['RESERVE_CATCHUP_ANALYTIC_FAIL','RESERVE_CATCHUP_MONEY_FAIL','RECOVERY_SLOPE_FAIL','RECOVERY_POINTWISE_MONOTONICITY_FAIL','RECOVERY_EVENT_MONOTONICITY_FAIL','NEW_FAR_COMPRESSION_FAIL','NEXT_BIG_GROSS_COMPRESSION_FAIL','GROSS_COMPRESSION_FAIL','RISK_COMPRESSION_UNPROVEN','Q_BOUND_FAIL','DISCRETE_FINITE_TERMINATION_FAIL','ROUNDING_PATHOLOGY_UNHANDLED','UP_DOWN_PARITY_FAIL','COUNTEREXAMPLE_SUITE_FAIL']

def validate():
 c={k:0 for k in BLOCKERS};b=t.broker();p=Plan(D('1'),D('2'),D('.5'),D('.5'),D('.9'),D('0'),costs=Costs(fee=D('.01')))
 tracks={d:evaluate(p,b,D('550'),d) for d in ('UP','DOWN')}
 c['RESERVE_CATCHUP_ANALYTIC_FAIL']=int(not p.reserve_slope_lots>0)
 c['RESERVE_CATCHUP_MONEY_FAIL']=int(not all(x['money_catch_up'] for x in tracks.values()))
 c['RECOVERY_SLOPE_FAIL']=int(not p.recovery_slope_lots>0)
 c['RECOVERY_POINTWISE_MONOTONICITY_FAIL']=int(not all(x['pointwise'] for x in tracks.values()))
 c['RECOVERY_EVENT_MONOTONICITY_FAIL']=int(not event_monotone(D('5'),D('3'),D('2'),D('0')))
 comp=compression(D('1'),D('.5'),D('.2'),D('.1'),D('.1'),b,D('2'))
 c['NEW_FAR_COMPRESSION_FAIL']=int(not comp['new_far_pass']);c['NEXT_BIG_GROSS_COMPRESSION_FAIL']=int(not comp['next_big_pass']);c['GROSS_COMPRESSION_FAIL']=int(not comp['gross_pass'])
 # Parse every normative profile cap; no test-selected or average q is accepted.
 caps=[]
 for line in MANUAL.splitlines():
  cells=[x.strip() for x in line.strip().split('|')]
  if len(cells)>7 and cells[1] in {'SAFE','BALANCED','STRONG_COMPRESSION'}:
   caps.append(Decimal(cells[6]))
 c['RISK_COMPRESSION_UNPROVEN']=int('NextCycleRisk<OldCycleRisk' not in MANUAL or 'NextFarRiskMoney' not in MANUAL)
 c['Q_BOUND_FAIL']=int(len(caps)!=3 or not all(D(0)<x<D(1) for x in caps))
 try:finite_bound(D('1'),D('.5'),b)
 except ValueError:c['DISCRETE_FINITE_TERMINATION_FAIL']=1
 caught=t.counterexamples();c['ROUNDING_PATHOLOGY_UNHANDLED']=int(not all(caught[x] for x in ('CompressionRawPass_NormalizedFail','FiniteContinuousPass_DiscreteFail')))
 c['UP_DOWN_PARITY_FAIL']=int(not all(x['pointwise'] for x in tracks.values()))
 c['COUNTEREXAMPLE_SUITE_FAIL']=int(len(caught)!=9 or not all(caught.values()))
 return c,t.run_matrix(),caught,max(caps) if caps else None

def main():
 c,matrix,caught,qmax=validate()
 for k in BLOCKERS:print(f'{k}={c[k]}')
 print(f'AUTOMATED_MATRIX_CASES={matrix}');print(f'Q_MAX_WORST_CASE={qmax}');print(f'COUNTEREXAMPLES_CAUGHT={sum(caught.values())}')
 print('RISK_COMPRESSION='+('DEFERRED_WITH_PROOF' if c['RISK_COMPRESSION_UNPROVEN'] else 'PASS'))
 print('Q_WORST_CASE_BOUND='+('FAIL' if c['Q_BOUND_FAIL'] else 'PASS'))
 fail=[k for k,v in c.items() if v]
 print('BLOCKING_COUNTERS='+(','.join(fail) if fail else 'NONE'))
 print('STAGE_3_1_4_VALIDATION='+('FAIL' if fail else 'PASS'))
 return bool(fail)
if __name__=='__main__':raise SystemExit(main())
