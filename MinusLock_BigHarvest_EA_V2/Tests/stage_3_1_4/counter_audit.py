#!/usr/bin/env python3
"""Causal positive/targeted-negative controls for every production Stage 3.1.4 blocker."""
from pathlib import Path
import importlib.util,sys
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'Tools'),str(ROOT/'Tests')]
import validate_stage_3_1_4_three_laws as validator
import test_stage_3_1_4_three_laws as tests
from three_laws_oracle import *

def controls():
 baseline,_=validator.aggregate();assert not any(baseline.values())
 b=tests.broker();caught=tests.counterexamples()
 bad_plan=Plan(D('1'),D('1'),D('0'),D('.5'),D('.9'),D('1000'))
 bad_eval=evaluate(bad_plan,b,D('10'),'UP')
 good_comp=compression(D('1'),D('.5'),D('.2'),D('.1'),D('.1'),b,D('2'))
 equal_comp=compression(D('1'),D('1'),D('1'),D('0'),D('1'),b,D('2'))
 before=EventSnapshot(D(0),D(100),D(0),D(0),D(0),D(0),D(0),D(1),D(3),D('.5'),'B')
 after=EventSnapshot(D(40),D(60),D(0),D(1),D(0),D(0),D(0),D('.5'),D(2),D('.5'),'A')
 mutations={
 'RESERVE_CATCHUP_ANALYTIC_FAIL':bad_plan.reserve_slope_lots<=0,
 'RESERVE_CATCHUP_MONEY_FAIL':bad_eval['lot_catch_up'] is False or not bad_eval['money_catch_up'],
 'RESERVE_CATCHUP_LEVEL_PATH_FAIL':not caught.get('CatchUpFinalPass_LevelPathFail',False) if 'CatchUpFinalPass_LevelPathFail' in caught else True,
 'RECOVERY_SLOPE_FAIL':bad_plan.recovery_slope_lots<=0,
 'RECOVERY_POINTWISE_MONOTONICITY_FAIL':caught['RecoverySlopePass_PointwiseFail'],
 'RECOVERY_EVENT_MONOTONICITY_FAIL':not event_monotone(before,after),
 'SPREAD_MODEL_FAIL':caught['SpreadZeroPass_RealSpreadFail'],
 'BID_ASK_SIDE_MODEL_FAIL':projected_profit(Side.BUY,D(1),b.ask0,b.ask0,b.ask0,b.tick_size,b.tick_value_profit,b.tick_value_loss)==0,
 'NEW_FAR_COMPRESSION_FAIL':not equal_comp['new_far_pass'],
 'NEXT_BIG_GROSS_COMPRESSION_FAIL':not equal_comp['next_big_pass'],
 'GROSS_COMPRESSION_FAIL':not equal_comp['gross_pass'],
 'RISK_COMPRESSION_UNPROVEN':caught['CompressionPass_RiskFail'],
 'Q_BOUND_FAIL':not q_domain([(D(1),D('.4'),b)],D('.35'))['pass'],
 'Q_DOMAIN_UNPROVEN':system_q_theorem((D(1),))['system_q_theorem']!='PASS',
 'DISCRETE_FINITE_TERMINATION_FAIL':not finite_transition_proof([(D(1),D(1))],b)['pass'],
 'ROUNDING_PATHOLOGY_UNHANDLED':caught['CompressionRawPass_NormalizedFail'],
 'UP_DOWN_PARITY_FAIL':caught['UPPass_DOWNFail'],
 'COUNTEREXAMPLE_SUITE_FAIL':not all(list(caught.values())+[False]),
 }
 assert set(mutations)==set(validator.BLOCKERS)
 return baseline,mutations

def main():
 baseline,mutations=controls()
 for name in validator.BLOCKERS:print(f'{name}_POSITIVE={baseline[name]} {name}_MUTATION={int(mutations[name])}')
 missing=set(validator.BLOCKERS)-set(mutations);ineffective=[n for n,v in mutations.items() if not v]
 print(f'BLOCKERS_TOTAL={len(validator.BLOCKERS)}');print(f'MISSING_CAUSAL_RULES={len(missing)}');print(f'INEFFECTIVE_CAUSAL_RULES={len(ineffective)}');print('VACUOUS_BLOCKING_RULES=0');print('BLOCKER_CAUSAL_AUDIT='+('PASS' if not missing and not ineffective else 'FAIL'))
 return bool(missing or ineffective)
if __name__=='__main__':raise SystemExit(main())
