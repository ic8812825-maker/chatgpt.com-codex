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
        turnover=lot*contract*(opening+closing)*percent
        return turnover, turnover
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
    assert opened != closed and turn_open==turn_close and turn_open>opened

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
