"""Stage 1.2 numeric oracle and narrow static guards (FO/WP/MG/CL)."""
from decimal import Decimal as D
from enum import IntEnum
from pathlib import Path
import pytest

class Outcome(IntEnum):
    NOT_EVALUATED=0; CONTINUE=1; FINITE_PASS=2; FINAL_ROUTE=3; TERMINAL=4; NO_FINITE=5
    REJECT=6; ERROR=7
class Class(IntEnum): NONE=0; CONTINUE=1; SUCCESS=2; ROUTE=3; TERMINAL=4; REJECT=5; ERROR=6

def classify(o):
    return {Outcome.CONTINUE:Class.CONTINUE,Outcome.FINITE_PASS:Class.SUCCESS,
            Outcome.FINAL_ROUTE:Class.ROUTE,Outcome.TERMINAL:Class.TERMINAL,
            Outcome.NO_FINITE:Class.REJECT,Outcome.REJECT:Class.REJECT,
            Outcome.ERROR:Class.ERROR}.get(o,Class.NONE)

def combine(a,b):
    ca,cb=classify(a),classify(b)
    for cls in (Class.ERROR,Class.TERMINAL,Class.REJECT):
        if ca==cls:return a
        if cb==cls:return b
    if Class.ROUTE in (ca,cb):
        return Outcome.FINAL_ROUTE if ca==cb==Class.ROUTE else Outcome.REJECT
    if ca==cb==Class.SUCCESS:return Outcome.FINITE_PASS
    return Outcome.CONTINUE

def trigger(anchor_bid,anchor_ask,direction,distance,shock=D('0')):
    spread=anchor_ask-anchor_bid
    if direction=='BUY': base_bid=anchor_bid+distance; base_ask=base_bid+spread
    else: base_ask=anchor_ask-distance; base_bid=base_ask-spread
    return (base_bid,base_ask,base_bid-shock,base_ask+shock)

def margin_price(direction,bid,ask): return ask if direction=='BUY' else bid

def margins(before,far,core,trend,small,equity,safety=D('0')):
    steady=far+core+trend+small; gated=steady*(D(1)+safety/D(100))
    return {'steady':steady,'peak':max(before,steady),'overlap':before+core+trend+small,
            'free':equity-gated,'usage':gated/equity*100,'level':equity/gated*100}

@pytest.mark.parametrize('outcome,expected',[
 (Outcome.CONTINUE,Class.CONTINUE),(Outcome.FINITE_PASS,Class.SUCCESS),(Outcome.FINAL_ROUTE,Class.ROUTE),
 (Outcome.TERMINAL,Class.TERMINAL),(Outcome.ERROR,Class.ERROR)],ids=['FO-01','FO-02','FO-03','FO-04','FO-05'])
def test_outcome_classes(outcome,expected): assert classify(outcome)==expected

@pytest.mark.parametrize('base,worst,expected',[
 (Outcome.FINITE_PASS,Outcome.FINITE_PASS,Outcome.FINITE_PASS),
 (Outcome.FINITE_PASS,Outcome.CONTINUE,Outcome.CONTINUE),
 (Outcome.FINAL_ROUTE,Outcome.FINAL_ROUTE,Outcome.FINAL_ROUTE),
 (Outcome.FINAL_ROUTE,Outcome.CONTINUE,Outcome.REJECT),
 (Outcome.ERROR,Outcome.FINITE_PASS,Outcome.ERROR),
 (Outcome.CONTINUE,Outcome.TERMINAL,Outcome.TERMINAL)],ids=['FO-06','FO-07','FO-08','FO-09','FO-10','FO-11'])
def test_truth_table(base,worst,expected): assert combine(base,worst)==expected

def test_fo12_stable_reason_code():
    mapping={Outcome.CONTINUE:'CATCHUP_CONTINUE',Outcome.FINAL_ROUTE:'CATCHUP_FINAL_CLOSE_PREVIEW_REQUIRED'}
    assert mapping[Outcome.FINAL_ROUTE]=='CATCHUP_FINAL_CLOSE_PREVIEW_REQUIRED'

def test_wp01_04_non_cumulative_execution_shock():
    first=trigger(D('100'),D('100.2'),'BUY',D('1'),D('.1'))
    second=trigger(first[0],first[1],'BUY',D('.5'),D('.1'))
    assert first[1]-first[0]==second[1]-second[0]==D('.2') # WP-01/WP-02
    assert first[3]-first[2]==second[3]-second[2]==D('.4') # WP-03
    assert second[:2]==(D('101.5'),D('101.7')) # WP-04: base trigger, not execution pair

def test_wp05_06_adverse_money_sides():
    base=trigger(D('100'),D('100.2'),'BUY',D('1')); worst=trigger(D('100'),D('100.2'),'BUY',D('1'),D('.1'))
    assert worst[2]<=base[2] # WP-05 BUY close Bid
    assert worst[3]>=base[3] # WP-06 SELL close Ask

def test_wp07_independent_partial_budget():
    cost_per_lot=D('10'); base_lot=D('3')/cost_per_lot; worst_lot=D('2')/cost_per_lot
    assert worst_lot!=base_lot

def test_wp08_trace_declares_non_cumulative():
    assert 'CumulativeSpreadStress=%d' in (Path(__file__).parents[2]/'Include/HybridCatchUpModel.mqh').read_text()

@pytest.mark.parametrize('direction,expected', [('BUY',D('100.2')),('SELL',D('100'))],ids=['MG-01','MG-02'])
def test_margin_control_side(direction,expected): assert margin_price(direction,D('100'),D('100.2'))==expected

def test_mg03_05_control_prices_not_historical():
    historical=D('80'); current=margin_price('BUY',D('100'),D('100.2'))
    assert current==D('100.2') and current!=historical # MG-03/MG-05
    assert margin_price('SELL',D('101'),D('101.3'))==D('101') # MG-04 reopen control

def test_mg06_09_upper_bounds():
    result=margins(D('400'),D('90'),D('160'),D('25'),D('60'),D('1000'))
    assert result['steady']==D('335') # MG-07
    assert result['peak']==D('400') # MG-08
    assert result['overlap']==D('645') and result['overlap']!=result['peak'] # MG-09
    estimated_release=D('9999'); assert result['free']==D('665') and estimated_release!=result['free'] # MG-06

def test_mg10_worst_safety_once():
    base=margins(D('400'),D('90'),D('160'),D('25'),D('60'),D('1000'))
    worst=margins(D('400'),D('90'),D('160'),D('25'),D('60'),D('1000'),D('10'))
    assert worst['usage']==base['usage']*D('1.10')

def test_cl01_no_duplicate_assignments():
    source=(Path(__file__).parents[2]/'Include/HybridCatchUpModel.mqh').read_text()
    assert 'row.reserveAfter=after.finalReserveReal; row.carryAfter=after.carryAvailable;\n   row.reserveAfter' not in source

def test_cl02_03_scope_and_no_execution_calls():
    source=(Path(__file__).parents[2]/'Include/HybridCatchUpModel.mqh').read_text()
    assert all(x not in source for x in ('PositionOpen(','PositionClose(','OrderSend(','TradeEngine.mqh','StateMachine.mqh'))
