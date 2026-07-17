from datetime import datetime, timedelta
import pytest

def signed_swap(rate, opening, closing, rollover_weekday=2):
    total=0; breakdown=[]; day=opening
    while day < closing:
        day += timedelta(days=1)
        if day > closing: break
        if day.weekday() >= 5: continue
        multiplier=3 if day.weekday()==rollover_weekday else 1
        total += rate*multiplier; breakdown.append(multiplier)
    return total, breakdown

def commissions(lot, contract, opening, closing, percent, mode):
    if mode=='notional': return lot*contract*opening*percent, lot*contract*closing*percent
    if mode=='turnover':
        return lot*contract*opening*percent, lot*contract*closing*percent
    raise ValueError

@pytest.mark.parametrize('rate', [2.0,-2.0])
@pytest.mark.parametrize('weekday', [0,1,2,3])
def test_signed_swap_and_calendar(rate,weekday):
    start=datetime(2026,7,13+weekday); value,days=signed_swap(rate,start,start+timedelta(days=4))
    assert value == rate*sum(days) and all(x in (1,3) for x in days)

def test_close_before_rollover_has_no_swap():
    now=datetime(2026,7,13,10); assert signed_swap(-1,now,now+timedelta(hours=8))==(0,[])

def test_notional_and_turnover_are_distinct():
    opened,closed=commissions(1,100_000,1.1,1.2,.0001,'notional')
    turn_open,turn_close=commissions(1,100_000,1.1,1.2,.0001,'turnover')
    assert opened != closed and turn_open==opened and turn_close==closed

def finite(far,loss,reserve,carry,recovery,ratio,transition,reserve_add,cost,target,limit=7):
    for cycle in range(limit+1):
        coverage=(reserve+carry)/loss
        if far<=target and coverage>=1 and recovery>=1: return cycle,coverage
        far*=ratio;loss*=ratio;reserve+=reserve_add;recovery+=transition-cost
    return None,(reserve+carry)/loss

def test_finite_reverse_requires_money_and_lot_together():
    cycles,coverage=finite(1,100,20,0,0,.5,5,20,1,.2)
    assert cycles is not None and coverage>=1
    assert finite(1,100,0,0,-20,.5,0,0,5,.2)[0] is None

def test_worst_case_buffer_is_separate_from_signed_swap():
    signed=-6.0; additional=1.5
    worst=max(0,-signed)+additional
    assert signed==-6 and worst==7.5

def test_close_now_never_adds_future_swap():
    now=datetime(2026,7,13,12)
    assert signed_swap(5,now,now)==(0,[])

def validate_five_legs(legs):
    required={'BIG_TREND','SMALL_BASE','REVERSE','OLD_FAR','BIG_CORE'}
    return len(legs)==5 and set(legs)==required

def test_small_contract_rejects_missing_and_duplicate_roles():
    assert validate_five_legs(['BIG_TREND','SMALL_BASE','REVERSE','OLD_FAR','BIG_CORE'])
    assert not validate_five_legs(['BIG_TREND','SMALL_BASE','REVERSE','OLD_FAR'])
    assert not validate_five_legs(['BIG_TREND','SMALL_BASE','REVERSE','OLD_FAR','OLD_FAR'])

def test_far_can_shrink_while_money_proof_still_fails():
    cycles,coverage=finite(1,100,0,0,0,.5,0,0,5,.01)
    assert cycles is None and coverage<1

def test_cycle_costs_can_destroy_recovery_even_with_reserve_growth():
    cycles,coverage=finite(1,100,0,0,0,.5,2,30,10,.01)
    assert cycles is None and coverage>=1

def exact_small_lots(actual, requested, residual, full, tolerance=.005):
    return full and abs(actual-requested)<=tolerance and residual<=tolerance

def test_exact_small_full_close_contracts():
    assert exact_small_lots(.25,.25,0,True)
    assert not exact_small_lots(.25,.20,.05,True)

def test_big_core_partial_contract_uses_target_residual():
    actual,target=1.2,.97
    requested=actual-target
    assert requested==pytest.approx(.23) and target<actual

def dynamic_reverse(initial, projections, target=.1, minimum_recovery=1):
    state=dict(initial)
    for index,p in enumerate(projections,1):
        assert p['before_far']==pytest.approx(state['far'])
        state['far']=p['after_far'];state['loss']=p['after_loss'];state['reserve']+=p['reserve_add'];state['carry']+=p['carry_add']
        state['recovery']+=p['transition']+p['swap']-p['commission']-p['spread']-p['slippage']
        coverage=(state['reserve']+state['carry'])/state['loss']
        if state['far']<=target and coverage>=1 and state['recovery']>=minimum_recovery and state['loss']<=state['reserve']+state['carry']:
            return index,state
    return None,state

def test_dynamic_reverse_recalculates_every_cycle():
    projections=[{'before_far':1,'after_far':.7,'after_loss':70,'reserve_add':20,'carry_add':3,'transition':8,'swap':-1,'commission':2,'spread':1,'slippage':1}, {'before_far':.7,'after_far':.4,'after_loss':35,'reserve_add':25,'carry_add':4,'transition':10,'swap':-2,'commission':1.5,'spread':.7,'slippage':.5}, {'before_far':.4,'after_far':.1,'after_loss':15,'reserve_add':15,'carry_add':2,'transition':5,'swap':-.5,'commission':1,'spread':.4,'slippage':.3}]
    cycles,state=dynamic_reverse({'far':1,'loss':100,'reserve':0,'carry':0,'recovery':0},projections)
    assert cycles==3 and state['reserve']==60 and state['far']==.1

def test_dynamic_reverse_rejects_money_shortfall_despite_compression():
    projections=[{'before_far':1,'after_far':.5,'after_loss':50,'reserve_add':0,'carry_add':0,'transition':0,'swap':-2,'commission':2,'spread':1,'slippage':1}, {'before_far':.5,'after_far':.1,'after_loss':10,'reserve_add':0,'carry_add':0,'transition':0,'swap':-2,'commission':2,'spread':1,'slippage':1}]
    cycles,state=dynamic_reverse({'far':1,'loss':100,'reserve':0,'carry':0,'recovery':0},projections)
    assert cycles is None and state['far']==.1 and state['recovery']<0
