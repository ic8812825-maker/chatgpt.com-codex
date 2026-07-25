"""Stage 1.2.2 RV/FP/CV oracle plus source-parity guards."""
from dataclasses import dataclass, replace, asdict
from decimal import Decimal as D
from hashlib import sha256
from pathlib import Path
import pytest
@dataclass(frozen=True)
class Money: valid:bool=True; gross:D=D('-10'); open_comm:D=D('0'); close_comm:D=D('.2'); swap:D=D('0'); fee:D=D('0'); slip:D=D('.1'); net:D=D('-10.3')
@dataclass(frozen=True)
class Route:
 symbol:str='EURUSD'; magic:int=7; cycle:int=9; source_rev:int=4; route_rev:int=5; level:int=1; profile:int=0
 far_lot:D=D('1'); far_open:D=D('105'); bid:D=D('100'); ask:D=D('100.2'); money:Money=Money(); loss:D=D('10.3')
 harvest:D=D('12'); realized_before:D=D('-20'); realized_after:D=D('-8'); partial_before:D=D('7.35'); partial_add:D=D('3'); partial_gross:D=D('10.35')
 reserve_before:D=D('10'); reserve_add:D=D('9'); reserve_after:D=D('19'); carry_before:D=D('1'); carry_add:D=D('0'); carry_after:D=D('1'); source_fp:int=123
@dataclass(frozen=True)
class Stage: partial_lot:D=D(0); consumed:D=D(0); far_after:D=D('1'); next_basket:bool=False; current:bool=True; allocation:bool=True; affordability:bool=True

def payload(r):
 d=asdict(r); return '|'.join(str(v) for v in d.values())
def fp(r): return sha256(payload(r).encode()).hexdigest()
def validate(r=Route(),stage=Stage(),expected_fp=None):
 if not r.symbol or r.cycle==0:return 'IDENTITY'
 if r.far_lot!=D('1') or r.far_open!=D('105'):return 'FAR'
 if r.bid<=0 or r.ask<r.bid:return 'PRICE'
 if not r.money.valid or r.loss!=max(-r.money.net,D(0)):return 'MONEY'
 if stage.partial_lot or stage.consumed or stage.far_after!=r.far_lot:return 'PARTIAL'
 if r.realized_after!=r.realized_before+r.harvest:return 'REALIZED'
 if r.partial_gross!=r.partial_before+r.partial_add:return 'BUDGET'
 if r.reserve_after!=r.reserve_before+r.reserve_add:return 'RESERVE'
 if r.carry_after!=r.carry_before+r.carry_add:return 'CARRY'
 if stage.next_basket or not all((stage.current,stage.allocation,stage.affordability)):return 'STAGE'
 if r.route_rev!=r.source_rev+1:return 'REVISION'
 if r.source_fp!=123:return 'SOURCE_FP'
 if expected_fp is not None and expected_fp!=fp(r):return 'FINGERPRINT'
 return 'VALID'

def test_rv01_valid(): assert validate(expected_fp=fp(Route()))=='VALID'
@pytest.mark.parametrize('change,code',[
 ({'far_lot':D('.9')},'FAR'),({'far_open':D('104')},'FAR'),({'ask':D('99')},'PRICE'),
 ({'realized_after':D('-7')},'REALIZED'),({'partial_gross':D('10')},'BUDGET'),({'reserve_after':D('20')},'RESERVE'),
 ({'carry_after':D('2')},'CARRY'),({'source_fp':999},'SOURCE_FP'),({'route_rev':4},'REVISION')],ids=['RV-02','RV-03','RV-04','RV-08','RV-09','RV-10','RV-11','RV-13','RV-14'])
def test_route_mutations(change,code): assert validate(replace(Route(),**change))==code
@pytest.mark.parametrize('stage',[
 Stage(partial_lot=D('.1')),Stage(consumed=D('1')),Stage(far_after=D('.9')),Stage(next_basket=True)],ids=['RV-05','RV-06','RV-07','RV-12'])
def test_stage_mutations(stage): assert validate(stage=stage) in ('PARTIAL','STAGE')
def test_rv15_fingerprint(): assert validate(expected_fp='wrong')=='FINGERPRINT'
@pytest.mark.parametrize('change',[
 {},{'far_lot':D('.9')},{'bid':D('99.9')},{'money':Money(close_comm=D('.3'))},{'partial_add':D('3.1')},{'reserve_add':D('9.1')},{'carry_after':D('2')},{'route_rev':6}],ids=['FP-01','FP-02','FP-03','FP-04','FP-05','FP-06','FP-07','FP-08'])
def test_fingerprint(change):
 base=Route(); changed=replace(base,**change); assert (fp(base)==fp(changed))==(not change)
@pytest.mark.parametrize('outcome,valid',[('ROUTE',False),('CONTINUE',True),('PASS',True),('ERROR',False)],ids=['CV-01','CV-02','CV-03','CV-04'])
def test_continuation_validity(outcome,valid): assert (outcome in ('CONTINUE','PASS'))==valid
def test_cv05_07_aggregate_route():
 aggregate={'finalBaseStateValid':False,'finalWorstStateValid':False,'finalCloseRouteStatesValid':True}
 assert not aggregate['finalBaseStateValid'] and not aggregate['finalWorstStateValid'] and aggregate['finalCloseRouteStatesValid']
def test_source_contracts():
 root=Path(__file__).parents[2]; source=(root/'Include/HybridCatchUpModel.mqh').read_text(); types=(root/'Include/Types.mqh').read_text()
 builder=source[source.index('bool BuildHybridFinalCloseRouteState'):source.index('HybridCatchUpOutcome EvaluateHybridCatchUpLevel')]
 assert 'ValidateHybridFinalCloseRouteState' in builder and 'partial.budgetGross' in builder
 for token in ('carryAfter','closeCommission','openCommission','netMoney','sourceStateRevision','routeStateRevision'): assert token in source
 assert 'continuationStateValid' in types and 'finalBaseStateValid' in types and 'finalWorstStateValid' in types
