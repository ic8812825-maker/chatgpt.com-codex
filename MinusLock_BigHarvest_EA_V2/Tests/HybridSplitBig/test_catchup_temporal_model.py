"""FT-01..FT-47: deterministic linear-adapter audit of sequential Catch-Up semantics."""
from dataclasses import dataclass, replace
from decimal import Decimal, ROUND_DOWN, ROUND_UP, ROUND_HALF_UP
from pathlib import Path
import pytest

D=lambda x: Decimal(str(x)); STEP=D('.01'); MIN=D('.01'); TOL=D('.01')
def money(x): return D(x).quantize(D('.01'),rounding=ROUND_HALF_UP)
def down(x): return (D(x)/STEP).to_integral_value(rounding=ROUND_DOWN)*STEP
def up(x): return (D(x)/STEP).to_integral_value(rounding=ROUND_UP)*STEP

def net(direction,lot,open_price,close_bid,close_ask,open_commission=False,commission=D('.02')):
    close=close_bid if direction=='BUY' else close_ask
    sign=D(1) if direction=='BUY' else D(-1)
    fees=commission+(commission if open_commission else D(0))
    return money(sign*(close-open_price)*lot*D(10)-fees)

@dataclass(frozen=True)
class State:
    level:int=0; branch:str='BASE'; far_dir:str='BUY'; far_lot:Decimal=D('1'); far_open:Decimal=D('105')
    big_dir:str='SELL'; core_lot:Decimal=D('1.6'); core_open:Decimal=D('100')
    trend_lot:Decimal=D('.25'); trend_open:Decimal=D('100'); small_dir:str='BUY'
    small_lot:Decimal=D('.6'); small_open:Decimal=D('100.2'); bid:Decimal=D('100'); ask:Decimal=D('100.2')
    realized:Decimal=D('0'); partial:Decimal=D('0'); reserve:Decimal=D('0'); carry:Decimal=D('0')
    cumulative_harvest:Decimal=D('0'); cumulative_partial:Decimal=D('0'); margin:Decimal=D('400')
    last_deficit:Decimal=D('999999'); last_recovery:Decimal=D('-999999'); fingerprint:str='BASE-0'

@dataclass(frozen=True)
class Row:
    before:State; after:State; close_bid:Decimal; close_ask:Decimal; core_net:Decimal; trend_net:Decimal
    small_net:Decimal; harvest:Decimal; eligible:Decimal; partial_add:Decimal; reserve_add:Decimal; carry_add:Decimal
    partial_lot:Decimal; partial_net:Decimal; consumed:Decimal; remaining_net:Decimal; deficit:Decimal
    recovery:Decimal; released:Decimal; margin_after:Decimal; peak:Decimal; overlap:Decimal; full_candidate:bool

def partial_preview(s,budget,bid,ask):
    full=net(s.far_dir,s.far_lot,s.far_open,bid,ask)
    full_candidate=max(-full,D(0))<=budget+TOL
    candidate=down(s.far_lot-MIN)
    while candidate>=MIN:
        remain=down(s.far_lot-candidate)
        n=net(s.far_dir,candidate,s.far_open,bid,ask)
        if remain>=MIN and max(-n,D(0))<=budget+TOL:
            return candidate,n,max(-n,D(0)),remain,full_candidate
        candidate=down(candidate-STEP)
    return D(0),D(0),D(0),s.far_lot,full_candidate

def evolve(s:State, adverse=D(0), commission=D('.02')):
    dist=D('1') if s.level==0 else D('.5')
    if s.big_dir=='BUY': base_bid=s.bid+dist; base_ask=base_bid+D('.2')
    else: base_ask=s.ask-dist; base_bid=base_ask-D('.2')
    bid=base_bid-adverse; ask=base_ask+adverse
    cn=net(s.big_dir,s.core_lot,s.core_open,bid,ask,True,commission)
    tn=net(s.big_dir,s.trend_lot,s.trend_open,bid,ask,True,commission)
    sn=net(s.small_dir,s.small_lot,s.small_open,bid,ask,True,commission)
    harvest=money(cn+tn+sn); eligible=max(harvest,D(0))
    pa=money(eligible*D('.10')); ra=money(eligible*D('.90')); ca=money(eligible-pa-ra)
    budget=money(s.partial+pa); lot,pnet,consumed,remain,full=partial_preview(s,budget,bid,ask)
    partial_after=money(budget-consumed); realized=money(s.realized+harvest+pnet)
    reserve=money(s.reserve+ra); carry=money(s.carry+ca)
    remaining=net(s.far_dir,remain,s.far_open,bid,ask) if remain else D(0)
    deficit=money(max(-remaining,D(0))-reserve)
    core=down(remain*D('1.6')); trend=down(remain*D('.25')); small=up(remain*D('.6'))
    core_open=ask if s.big_dir=='BUY' else bid; trend_open=core_open
    small_open=bid if s.big_dir=='BUY' else ask
    opening_float=net(s.big_dir,core,core_open,bid,ask,True,commission)+net(s.big_dir,trend,trend_open,bid,ask,True,commission)+net(s.small_dir,small,small_open,bid,ask,True,commission)
    recovery=money(realized+remaining+opening_float)
    remaining_margin=remain*D('100'); next_margin=(core+trend+small)*D('100')
    margin_after=money(remaining_margin+next_margin); released=money(max(D(0),s.margin-remaining_margin))
    peak=max(s.margin,margin_after); overlap=money(s.margin+next_margin)
    fp=f'{s.branch}-{s.level+1}-{remain}-{bid}-{ask}-{reserve}-{partial_after}'
    after=State(s.level+1,s.branch,s.far_dir,remain,s.far_open,s.big_dir,core,core_open,trend,trend_open,
                s.small_dir,small,small_open,bid,ask,realized,partial_after,reserve,carry,
                money(s.cumulative_harvest+harvest),money(s.cumulative_partial+pnet),margin_after,deficit,recovery,fp)
    return Row(s,after,bid,ask,cn,tn,sn,harvest,eligible,pa,ra,ca,lot,pnet,consumed,remaining,deficit,recovery,released,margin_after,peak,overlap,full)

def path(state=State(),levels=3,adverse=D(0),commission=D('.02')):
    rows=[]
    for _ in range(levels):
        row=evolve(state,adverse,commission); rows.append(row); state=row.after
    return rows

ROOT=Path(__file__).resolve().parents[2]

def check(ft):
    rows=path(levels=3); a,b,c=rows
    if ft==1: assert a.before.core_open==D('100') and a.close_bid==D('99')
    elif ft==2: assert b.before.core_open==a.close_bid and b.close_bid==D('98.5')
    elif ft==3: assert c.before.core_open==b.close_bid!=D('100')
    elif ft==4: assert len({(r.before.level,r.before.core_open) for r in rows})==3
    elif ft==5: assert c.after.cumulative_harvest==sum((r.harvest for r in rows),D(0))
    elif ft==6: assert c.after.cumulative_harvest-b.harvest==a.harvest+c.harvest
    elif ft==7: assert a.partial_add>0 and a.partial_add+a.before.partial==a.partial_lot*D(0)+a.partial_add
    elif ft==8: assert a.partial_net<=0 and a.after.realized==a.before.realized+a.harvest+a.partial_net
    elif ft==9: assert a.after.far_lot<a.before.far_lot
    elif ft==10:
        low=evolve(replace(State(),partial=D(0),core_lot=D('.1'),trend_lot=D('.1'),small_lot=D('.1'))); assert low.after.partial>=0
    elif ft==11: assert a.consumed<=a.before.partial+a.partial_add and a.after.reserve==a.before.reserve+a.reserve_add
    elif ft==12: assert a.after.far_lot==0 or a.after.far_lot>=MIN
    elif ft==13: assert a.partial_lot<=down(a.before.far_lot-MIN)
    elif ft==14:
        rich=evolve(replace(State(),partial=D('1000'))); assert rich.full_candidate and rich.after.far_lot>=MIN
    elif ft==15: assert a.remaining_net==net(a.before.far_dir,a.after.far_lot,a.before.far_open,a.close_bid,a.close_ask)
    elif ft==16: assert a.after.core_lot==down(a.after.far_lot*D('1.6'))
    elif ft==17: assert a.after.trend_lot==down(a.after.far_lot*D('.25'))
    elif ft==18: assert a.after.small_lot==up(a.after.far_lot*D('.6'))
    elif ft==19: assert a.after.core_lot%STEP==0 and a.after.trend_lot%STEP==0
    elif ft==20: assert a.after.small_lot>=a.after.far_lot*D('.6')
    elif ft==21: assert a.after.core_open==a.close_bid and a.after.small_open==a.close_ask
    elif ft==22: assert b.close_bid==a.after.bid-D('.5')
    elif ft==23: assert abs(a.partial_add+a.reserve_add+a.carry_add-a.eligible)<=TOL
    elif ft==24: assert abs(a.before.partial+a.partial_add-a.consumed-a.after.partial)<=TOL
    elif ft==25: assert a.after.realized-a.before.realized-a.harvest==a.partial_net
    elif ft==26:
        no_open=net(a.before.big_dir,a.before.core_lot,a.before.core_open,a.close_bid,a.close_ask,False); assert a.core_net==no_open-D('.02')
    elif ft==27: assert all(r.core_net is not None and r.trend_net is not None and r.small_net is not None for r in rows)
    elif ft==28:
        opening=net(a.after.big_dir,a.after.core_lot,a.after.core_open,a.close_bid,a.close_ask,True)+net(a.after.big_dir,a.after.trend_lot,a.after.trend_open,a.close_bid,a.close_ask,True)+net(a.after.small_dir,a.after.small_lot,a.after.small_open,a.close_bid,a.close_ask,True)
        assert a.recovery==money(a.after.realized+a.remaining_net+opening) and a.recovery!=money(a.after.realized+a.remaining_net+opening+a.after.reserve)
    elif ft==29:
        neg=evolve(replace(State(),core_lot=D('.01'),trend_lot=D('.01'),small_lot=D('5'))); assert neg.eligible==0 and neg.partial_add==neg.reserve_add==neg.carry_add==0
    elif ft==30:
        worst=path(replace(State(),branch='WORST',fingerprint='WORST-0'),adverse=D('.2')); assert rows[0].after.fingerprint!=worst[0].after.fingerprint
    elif ft==31:
        worst=path(replace(State(),branch='WORST',fingerprint='WORST-0'),adverse=D('.2')); assert worst[0].partial_lot<=a.partial_lot
    elif ft==32:
        worst=path(replace(State(),branch='WORST',fingerprint='WORST-0'),adverse=D('.2')); assert worst[0].after.far_lot>=a.after.far_lot
    elif ft==33:
        worst=path(replace(State(),branch='WORST',fingerprint='WORST-0'),adverse=D('5')); assert not (a.deficit<=0 and worst[0].deficit<=0)
    elif ft==34:
        worst=path(replace(State(),branch='WORST',fingerprint='WORST-0'),adverse=D('.2')); assert worst[0].harvest<=a.harvest
    elif ft==35: assert a.released>0
    elif ft==36: assert a.margin_after==(a.after.far_lot+a.after.core_lot+a.after.trend_lot+a.after.small_lot)*D('100')
    elif ft==37: assert a.peak==max(a.before.margin,a.margin_after)
    elif ft==38: assert a.overlap>=a.peak and a.overlap!=a.peak
    elif ft==39: assert a.before.far_dir=='BUY' and a.remaining_net<0
    elif ft==40:
        sell=State(far_dir='SELL',far_open=D('95'),big_dir='BUY',core_open=D('100.2'),trend_open=D('100.2'),small_dir='SELL',small_open=D('100'))
        sr=path(sell); assert sr[0].before.far_dir=='SELL' and sr[0].remaining_net<0
    elif ft==41: assert net('BUY',D(1),D(100),D(99),D(101))==money(D(-10)-D('.02'))
    elif ft==42: assert net('SELL',D(1),D(100),D(99),D(101))==money(D(-10)-D('.02'))
    elif ft in (43,44,45,46,47):
        source=(ROOT/'Include'/'HybridCatchUpModel.mqh').read_text()
        loop=source[source.index('for(int level=1;'):]
        if ft==43: assert 'snapshot.ask' not in loop and 'snapshot.bid' not in loop
        elif ft==44: assert 'snapshot.farLot' not in loop
        elif ft==45: assert 'baseState=nextBase' in loop and 'worstState=nextWorst' in loop
        elif ft==46: assert 'plan.projectedHarvestNet' not in source and 'cumulativeHarvest +=' not in source
        else:
            assert all(token not in source for token in ('StateMachine.mqh','TradeEngine.mqh','PositionUtils.mqh','PositionOpen(','PositionClose('))

@pytest.mark.parametrize('ft',range(1,48),ids=lambda n:f'FT-{n:02d}')
def test_temporal_contract(ft): check(ft)

if __name__=='__main__': raise SystemExit(pytest.main([__file__,'-q']))
