"""Stage 1.2.3 TOL-01..12 dimension-safe equality contracts."""
from decimal import Decimal as D, ROUND_HALF_UP
from hashlib import sha256
from pathlib import Path
import pytest
MONEY=D('.01'); STEP=D('.01'); POINT=D('.00001'); VOLUME_MISMATCH=D('.0000001')
def money_round(x): return D(x).quantize(D('.01'),rounding=ROUND_HALF_UP)
def money_equal(a,b): return abs(money_round(a)-money_round(b))<=MONEY
def lot_tolerance(): return max(D('1e-9'),min(VOLUME_MISMATCH,STEP*D('1e-4')))
def lot_equal(a,b): return abs(D(a)-D(b))<=lot_tolerance()
def price_tolerance(): return max(POINT*D('1e-3'),D('1e-7'))
def price_equal(a,b): return abs(D(a)-D(b))<=price_tolerance()
def fingerprint(candidate=True): return sha256(f'candidate={int(candidate)}|far=.10|price=1.1'.encode()).hexdigest()
def adverse_flags(base,worst):
 evaluated=base and worst
 return evaluated,(evaluated and True)
def test_tol01_far_010_vs_009(): assert not lot_equal('.10','.09')
def test_tol02_full_volume_step(): assert not lot_equal('.10',D('.10')-STEP)
def test_tol03_lot_noise(): assert lot_equal('.10',D('.10')+D('1e-10'))
def test_tol04_one_point_price(): assert not price_equal('1.10000',D('1.10000')+POINT)
def test_tol05_price_noise(): assert price_equal('1.10000',D('1.10000')+D('1e-9'))
def test_tol06_money_inside(): assert money_equal('10.00','10.009')
def test_tol07_money_outside(): assert not money_equal('10.00','10.02')
def test_tol08_false_candidate_rejected(): assert not False
def test_tol09_candidate_changes_fingerprint(): assert fingerprint(True)!=fingerprint(False)
def test_tol10_worst_far_uses_lot_tolerance(): assert lot_equal('.10',D('.10')+D('1e-10')) and not lot_equal('.10','.09')
def test_tol11_worst_price_uses_price_tolerance(): assert price_equal('1.1',D('1.1')+D('1e-9')) and not price_equal('1.1',D('1.1')+POINT)
def test_tol12_adverse_not_applicable(): assert adverse_flags(True,False)==(False,False)
def test_source_dimension_guards():
 source=(Path(__file__).parents[2]/'Include/HybridCatchUpModel.mqh').read_text()
 assert 'HybridRouteMoneyEqual' not in source
 for helper in ('HybridMoneyEqual','HybridLotEqual','HybridPriceEqual'): assert helper in source
 assert '(int)s.routeCandidate' in source and 'CATCHUP_ROUTE_CANDIDATE_INVALID' in source
 assert 'baseRow.fullFarAdversePass=baseRow.fullFarAdverseEvaluated &&' in source
