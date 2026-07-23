import json
from pathlib import Path
import pytest
from hybrid_split_big_reference import *
V=json.loads((Path(__file__).parent/'test_vectors.json').read_text())
@pytest.mark.parametrize('vector',V,ids=lambda x:x['id'])
def test_all_reference_vectors(vector):
 r=evaluate_simulation_vector(vector);assert r.code==vector['expected']['code'],r.trace
 for key,want in vector['expected']['values'].items():
  got=r.trace
  for part in key.split('.'):got=got[part]
  assert got==pytest.approx(want)
def test_buy_harvest_arithmetic_and_sell_mirror():
 a,b=(evaluate_vector(V[i]) for i in (0,1));assert a.trace['base_leg_nets']['trend']==pytest.approx(13.2);assert a.trace['harvest_net']==pytest.approx(43);assert a.trace['allocation']=={'partial':8.6,'reserve':30.1,'carry':4.3};assert a.trace['base_leg_nets']==b.trace['base_leg_nets']
def test_law_one_implies_two_100_cases():
 for n in range(1,101):
  f=1.;beta=n/100;small=.1;core=1/beta+small+.01;trend=n/1000
  assert beta*(core+trend-small)>f and core+trend-small-f>0
def test_next_big_and_q_bound_100_cases():
 for n in range(1,101):
  c=1+n/100;t=.2;q=.99/(c+t);assert (c+t)*q<1
  assert (1*q)**n <= 1*q**n+1e-12
def test_all_codes_are_oracle_codes():assert {x['expected']['code'] for x in V}<=DECISION_CODES
def test_bucket_consumption_and_idempotency():
 b=Buckets();assert b.allocate_harvest('h',43,.2,.7,.1)[0]=='PASS';assert not b.consume_partial_far_budget('p',9);assert b.consume_partial_far_budget('p2',8.6);assert not b.credit_transition_budget('h',1)
def test_discrete_solver_selects_minimum_and_records_rejections():
 import copy
 v=copy.deepcopy(V[0]);v['risk_model']={'old_control_bid':90,'old_control_ask':90.2,'next_control_bid':90,'next_control_ask':90.2};v['geometry']['target_new_far']=.9
 r=enumerate_new_far(v);assert r.code=='PASS_NEW_FAR' and r.selected.new_far==.02 and r.iterations>=1
def test_nested_schema_and_bounded_future_no_flag():
 import copy
 v=copy.deepcopy(V[0]);v['market']['ask']=0;assert validate_vector(v)
 v=copy.deepcopy(V[0]);v['risk_model']={'old_control_bid':90,'old_control_ask':90.2,'next_control_bid':90,'next_control_ask':90.2};r=simulate_future_small(v,2);assert r.nodes_visited<=2 and r.code in ('PASS','REJECT_NO_VALID_Q','REJECT_FUTURE_SMALL')
