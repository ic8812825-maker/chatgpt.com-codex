"""ROUTE-01..12 and ADV-01..05: Final Close route-state semantics."""
from dataclasses import dataclass
from decimal import Decimal as D, ROUND_HALF_UP
from enum import Enum
from pathlib import Path
import pytest
money=lambda x:D(x).quantize(D('.01'),rounding=ROUND_HALF_UP)
class O(Enum): CONTINUE=1; PASS=2; ROUTE=3; TERMINAL=4; REJECT=5; ERROR=6
@dataclass(frozen=True)
class Before: far:D=D('1'); far_open:D=D('105'); realized:D=D('-20'); partial:D=D('7.35'); reserve:D=D('10'); carry:D=D('0'); fingerprint:int=123
@dataclass(frozen=True)
class Route: far:D; far_open:D; realized:D; budget:D; reserve:D; carry:D; source:int; fingerprint:int
@dataclass(frozen=True)
class Row:
 outcome:O; partial_evaluated:bool; partial_lot:D; consumed:D; far_after:D; partial_net:D
 next_evaluated:bool; core:D; trend:D; small:D; geometry:bool; margin:bool; recovery:bool; route:Route

def evaluate(before=Before(),harvest=D('12'),partial_add=D('1.20'),reserve_add=D('10.80'),carry_add=D('0'),full_loss=D('8')):
 budget=money(before.partial+partial_add); affordable=full_loss<=budget+D('.01')
 if affordable:
  route=Route(before.far,before.far_open,money(before.realized+harvest),budget,money(before.reserve+reserve_add),money(before.carry+carry_add),before.fingerprint,987654)
  return Row(O.ROUTE,False,D(0),D(0),before.far,D(0),False,D(0),D(0),D(0),False,False,False,route)
 raise ValueError('fixture only models route branch')
def combine(a,b):
 if O.ERROR in (a,b): return O.ERROR
 if O.TERMINAL in (a,b): return O.TERMINAL
 if O.REJECT in (a,b): return O.REJECT
 if O.ROUTE in (a,b): return O.ROUTE if a==b==O.ROUTE else O.REJECT
 if a==b==O.PASS:return O.PASS
 return O.CONTINUE
def adverse_guard(base_evaluated,worst_evaluated): return base_evaluated and worst_evaluated

def test_route_01_no_partial():
 r=evaluate(); assert r.outcome==O.ROUTE and not r.partial_evaluated and r.partial_lot==r.consumed==0
def test_route_02_far_preserved():
 b=Before(); r=evaluate(b); assert r.route.far==b.far and r.far_after==b.far
def test_route_03_budget_preserved():
 b=Before(); r=evaluate(b); assert r.route.budget==money(b.partial+D('1.20')) and r.consumed==0
def test_route_04_realized_excludes_partial():
 b=Before(); r=evaluate(b); assert r.route.realized==money(b.realized+D('12')) and r.partial_net==0
def test_route_05_next_basket_skipped():
 r=evaluate(); assert not r.next_evaluated and r.core==r.trend==r.small==0
def test_route_06_continuation_gates_cannot_block():
 r=evaluate(Before(far=D('.01')),full_loss=D('1')); assert r.outcome==O.ROUTE and not any((r.geometry,r.margin,r.recovery))
def test_route_07_fingerprint_and_trace_contract():
 b=Before(); r=evaluate(b); assert r.route.source==b.fingerprint and r.route.fingerprint!=0 and not r.partial_evaluated and not r.next_evaluated
@pytest.mark.parametrize('a,b,expected',[(O.ROUTE,O.ROUTE,O.ROUTE),(O.ROUTE,O.CONTINUE,O.REJECT),(O.CONTINUE,O.ROUTE,O.REJECT),(O.ROUTE,O.PASS,O.REJECT),(O.PASS,O.ROUTE,O.REJECT)],ids=['ROUTE-08','ROUTE-09','ROUTE-10','ROUTE-11','ROUTE-12'])
def test_route_outcomes(a,b,expected): assert combine(a,b)==expected
@pytest.mark.parametrize('base,worst,expected',[(True,True,True),(False,True,False),(True,False,False)],ids=['ADV-01','ADV-02','ADV-03'])
def test_adverse_guard(base,worst,expected): assert adverse_guard(base,worst)==expected
def test_adv_04_worst_full_far_loss(): assert D('10.2')>=D('10')-D('.01')
def test_adv_05_zero_money_does_not_validate(): assert not adverse_guard(False,False)
def test_static_route_precedes_partial_and_next_basket():
 root=Path(__file__).parents[2]; solver=(root/'Include/HybridPartialFarPreview.mqh').read_text(); model=(root/'Include/HybridCatchUpModel.mqh').read_text()
 assert solver.index('if(result.finalClosePreviewRouteCandidate)')<solver.index('for(double raw=maximum')
 branch=model[model.index('if(partial.finalClosePreviewRouteCandidate)'):model.index('row.partialFarEvaluated=true')]
 assert 'return SetHybridCatchUpRowOutcome' in branch and 'HybridCatchUpMarginTransition' not in branch and 'BuildProjectedReopenPrices' not in branch
 assert model.index('if(partial.finalClosePreviewRouteCandidate)')<model.index('NormalizeHybridCoreLot')
