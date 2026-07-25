"""Stage 1.2.4 continuation DIM-CONT-01..10 and full source inventory."""
from decimal import Decimal as D
from pathlib import Path
import re
STEP=D('.01'); LOT_TOL=D('.000001'); RATIO_TOL=D('.000001'); PERCENT_TOL=D('.000001')
def lot_less(a,b): return D(a)<D(b)-LOT_TOL
def lot_equal(a,b): return abs(D(a)-D(b))<=LOT_TOL
def lot_less_equal(a,b): return D(a)<=D(b)+LOT_TOL
def lot_greater(a,b): return D(a)>D(b)+LOT_TOL
def lot_greater_equal(a,b): return D(a)>=D(b)-LOT_TOL
def ratio_less(a,b): return D(a)<D(b)-RATIO_TOL
def percent_ge(a,b): return D(a)>=D(b)-PERCENT_TOL
def percent_le(a,b): return D(a)<=D(b)+PERCENT_TOL
def temporal(before,after,closed): return lot_less_equal(after,before) and (lot_equal(closed,0) or lot_less(after,before))
def new_big_reject(new,limit): return lot_greater_equal(new,limit)
def slope_pass(slope): return lot_greater(slope,0)
def worst_bid_adverse(symbol_point,base,worst): return D(worst)<=D(base)+D(symbol_point)*D('1e-3')
def test_dim_cont_01_min_far(): assert lot_less('.009','.01')
def test_dim_cont_02_real_step_and_increase(): assert temporal('.10','.09','.01') and not temporal('.10','.11','0')
def test_dim_cont_03_partial_zero(): assert lot_equal('1e-10',0) and not lot_equal('.01',0)
def test_dim_cont_04_ratio_boundary(): assert ratio_less('.999','1') and not ratio_less(D('1')-RATIO_TOL/2,'1')
def test_dim_cont_05_inventory_money_only(): assert not dimension_violations()
def test_dim_cont_06_new_big_boundary(): assert new_big_reject('.05','.05') and not new_big_reject('.049','.05')
def test_dim_cont_07_lot_slope(): assert not slope_pass(0) and not slope_pass(LOT_TOL/2) and slope_pass(LOT_TOL*2)
def test_dim_cont_08_margin_level_percent(): assert percent_ge(D('200')-PERCENT_TOL/2,'200') and not percent_ge('199.99','200')
def test_dim_cont_09_margin_usage_percent(): assert percent_le(D('50')+PERCENT_TOL/2,'50') and not percent_le('50.01','50')
def test_dim_cont_10_explicit_worst_symbol(): assert worst_bid_adverse('.00001','1.10000','1.09999')
ROOT=Path(__file__).resolve().parents[2]; SOURCE=ROOT/'Include'/'HybridCatchUpModel.mqh'
NON_MONEY=re.compile(r'(farLot|farLotClosed|coreLot|trendLot|smallLot|openPrice|triggerBid|triggerAsk|anchorBid|anchorAsk|marginLevel|marginUsage|Ratio|Points)',re.I)
MONEY_CONTEXT=('HybridMoney','partialAdd','reserveAdd','carryAdd','eligibleHarvest','coverageDeficit','Recovery','finalReserve','lastCoverage','netMoney','fullFarLoss','MarketCostDeterioration')
def dimension_violations():
 bad=[]
 for no,line in enumerate(SOURCE.read_text().splitlines(),1):
  if 'MoneyCalculationTolerance' not in line: continue
  if NON_MONEY.search(line) or not any(token.lower() in line.lower() for token in MONEY_CONTEXT): bad.append((no,line.strip()))
 return bad
def test_static_forbidden_patterns_and_symbol_provenance():
 source=SOURCE.read_text(); assert not dimension_violations(),f'DIMENSION_CONTRACT_VIOLATION {dimension_violations()}'
 assert 'HybridWorstRowIsAdverse(snapshot.symbol' in source
 assert 'stateAfter.symbol!=""' not in source
 for helper in ('HybridLotLess','HybridLotLessOrEqual','HybridLotGreater','HybridLotGreaterOrEqual','HybridRatioLess','HybridPercentGreaterOrEqual','HybridPercentLessOrEqual'): assert helper in source

def partial_exists(partial_lot): return lot_greater(partial_lot,0)
def test_dim_hotfix_01_noise_partial_absent(): assert not partial_exists('1e-10')
def test_dim_hotfix_02_real_partial_present(): assert partial_exists('.01')
def test_dim_hotfix_03_half_tolerance_absent(): assert not partial_exists(LOT_TOL/2)
def test_dim_hotfix_04_twice_tolerance_present(): assert partial_exists(LOT_TOL*2)
def margin_transition_body():
 source=SOURCE.read_text(); start=source.index('bool HybridCatchUpMarginTransition('); end=source.index('\nbool BuildInitialHybridCatchUpState',start); return source[start:end]
def test_dim_hotfix_05_no_direct_partial_zero_comparisons():
 compact=re.sub(r'\s+','',margin_transition_body())
 forbidden=(r'partialLot(?:>|>=|!=|==)0(?:\.0)?',r'MathAbs\(partialLot\)(?:<=|<)MoneyCalculationTolerance',r'partialLot(?:>|<=)MoneyCalculationTolerance')
 assert not any(re.search(pattern,compact) for pattern in forbidden)
def test_dim_hotfix_06_scoped_lot_aware_partial():
 compact=re.sub(r'\s+','',margin_transition_body()); assert 'HybridLotGreater(before.symbol,partialLot,0.0)' in compact
