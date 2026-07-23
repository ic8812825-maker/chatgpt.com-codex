import json
from pathlib import Path
from hybrid_split_big_reference import *
R=VolumeRules(.01,100,.01)

def test_law_one_implies_two():
    g=Geometry(1,2,.8,.2,.9); assert g.catchup_ratio()>1 and g.recovery_slope()>0

def test_next_big_inequality():
    assert (2+.8)*.3*1 < 1

def test_reserve_is_idempotent_and_not_profit_twice():
    b=Buckets(); assert b.allocate_harvest('h1',100,.2,.7,.1); assert not b.allocate_harvest('h1',100,.2,.7,.1)
    assert b.realized_cycle_pl==100 and b.final_reserve_real==70 and b.recovery_actual_final()==100

def test_negative_harvest_no_reserve():
    b=Buckets(); b.allocate_harvest('h',-10,.2,.7,.1); assert b.final_reserve_real==0 and b.realized_cycle_pl==-10

def test_final_projection_is_not_actual(): assert projected_final(5,10)==15 and actual_final(12)==12

def test_finite_catchup(): assert finite_catchup([{'deficit':8,'recovery':1},{'deficit':3,'recovery':2},{'deficit':-1,'recovery':3}],1,2)==3

def test_no_finite_catchup_when_no_gain(): assert finite_catchup([{'deficit':8,'recovery':1},{'deficit':7.5,'recovery':2}],1,2) is None

def test_new_far_solver_and_risk():
    x=solve_new_far(1,4,100,2,.8,.2,R,lambda n: 10,lambda n:n*100,cumulative_loss=0,percent=0)
    assert x['code']=='PASS_NEW_FAR' and x['new_far']<1 and x['next']['big_gross']<1

def test_transition_and_cumulative_loss():
    b=Buckets(); assert b.transition_allowed(-2,3,5,100,.1); b.record_transition(-2); assert not b.transition_allowed(-4,5,5,100,.1)

def test_rounding_and_min_lot_terminal(): assert terminal_required(.003,.0,.01,R)
def test_partial_fill_never_reconciles(): assert reconcile(.7,.35)=='ERROR_PARTIAL_EXECUTION'
def test_buy_sell_symmetry_linear():
    assert linear_profit('BUY',1,100,101,10)==linear_profit('SELL',1,101,100,10)
def test_variable_q_bound():
    assert bounded_transitions(1,.01,.3)==4

def test_vectors_count_and_schema():
    rows=json.loads((Path(__file__).parent/'test_vectors.json').read_text()); assert len(rows)>=20
    required={'id','symbol','direction','bid','ask','positions','commission','swap','fee','slippage','reserve','shares','volume','margin','harvest_levels','expected_code'}
    assert all(required <= set(x) for x in rows)
def test_coverage_deficit(): assert coverage_deficit(20,15,2)==7
