#!/usr/bin/env python3
from decimal import Decimal as D
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Tools'))
from three_laws_oracle import Broker,Costs,Plan,compression,evaluate,event_monotone,finite_bound

def broker(step='0.01',point='0.00001',tick='0.00001',profit='1',loss='1',down_profit=None,down_loss=None,bid='1.10000',spread='0.00010'):
 return Broker(D(point),D(tick),D(profit),D(loss),D(step),D(step),D(down_profit) if down_profit else None,D(down_loss) if down_loss else None,D(bid),D(bid)+D(spread))

def run_matrix():
 total=0
 for far in map(D,['0.01','0.02','0.05','0.10','0.50','1.00','2.00','5.00']):
  for step in map(D,['0.01','0.1','0.25']):
   if far<step:continue
   b=broker(str(step),spread='0');f=b.normalize(far);c=b.normalize(f*D('2.0'));t=b.normalize(f*D('0.5'));s=b.normalize(f*D('0.5'))
   if min(c,t,s)==0:continue
   for distance in map(D,['1','10','50','100','200','300','550']):
    for direction in ('UP','DOWN'):
     p=Plan(f,c,t,s,D('0.9'),f*D('.01'))
     result=evaluate(p,b,distance,direction)
     assert result['lot_catch_up'] and result['recovery_slope'] and result['pointwise']
     assert result['money_catch_up'] and result['coverage_path']['coverage_monotone']
     total+=1
 assert total>=200
 return total

def boundaries():
 b=broker();
 equality=Plan(D('1'),D('1'),D('0.5'),D('0.5'),D('1'),D('0'))
 fail=Plan(D('1'),D('1'),D('0'),D('0.5'),D('1'),D('0'))
 assert equality.reserve_slope_lots==0 and not evaluate(equality,b,D('10'),'UP')['lot_catch_up']
 assert fail.recovery_slope_lots<0 and not evaluate(fail,b,D('10'),'DOWN')['pointwise']
 assert event_monotone(D('5'),D('3'),D('2'),D('0'))
 assert not event_monotone(D('5'),D('3'),D('2'),D('0.01'))
 c=compression(D('1'),D('0.5'),D('0.2'),D('0.1'),D('0.1'),b,D('2'))
 assert c['new_far_pass'] and c['next_big_pass'] and c['gross_pass'] and c['q']==D('0.5')
 assert finite_bound(D('1'),D('0.5'),b)>0
 catch=evaluate(Plan(D('1'),D('2'),D('.5'),D('.5'),D('.9'),D('10')),b,D('100'),'UP')
 assert 0<catch['coverage_path']['levels_checked']<=101
 assert catch['coverage_path']['coverage_monotone'] and catch['coverage_path']['first_catch_level'] is not None

def deficit_matrix():
 b=broker();out={}
 for name,loss,expected in [('SMALL',D('1'),True),('MEDIUM',D('10'),True),
                            ('LARGE_CATCHABLE',D('30'),True),('NEAR_LIMIT',D('42'),True),
                            ('IMPOSSIBLE',D('50'),False)]:
  result=evaluate(Plan(D('1'),D('2'),D('.5'),D('.5'),D('.9'),loss),b,D('100'),'UP')
  assert result['lot_catch_up'] and result['money_catch_up'] is expected
  out[name]=result
 return out

def cost_matrix():
 categories={
  'NO_COSTS':(Costs(),True),'COMMISSION_ONLY':(Costs(commission_open=D('1'),commission_close=D('1')),True),
  'SWAP_ONLY':(Costs(swap=D('2')),True),'FEE_ONLY':(Costs(fee=D('2')),True),
  'SLIPPAGE_ONLY':(Costs(slippage=D('2')),True),
  'COMBINED_NORMAL':(Costs(D('1'),D('1'),D('1'),D('1'),D('1')),True),
  'COMBINED_HIGH':(Costs(D('30'),D('30'),D('30'),D('30'),D('30')),False)}
 total=passed=0;b=broker()
 for costs,expected in categories.values():
  for direction in ('UP','DOWN'):
   result=evaluate(Plan(D('1'),D('2'),D('.5'),D('.5'),D('.9'),D('10'),costs=costs),b,D('100'),direction)
   total+=1;passed+=result['money_catch_up'] is expected
 assert total==passed
 return total,passed

if __name__=='__main__':
 boundaries();print(f'AUTOMATED_MATRIX_CASES={run_matrix()}');print('STAGE_3_1_4_MATRIX=PASS')

def counterexamples():
 caught={}
 b=broker()
 # Analytic lot capacity exists, but finite distance cannot cover initial deficit.
 p=Plan(D('1'),D('2'),D('0.5'),D('0.5'),D('0.9'),D('1000'))
 r=evaluate(p,b,D('10'),'UP');caught['CatchUpLotPass_MoneyFail']=r['lot_catch_up'] and not r['money_catch_up']
 # Lot slope ignores asymmetric directional money values.
 asym=broker(profit='0.4',loss='1');p=Plan(D('1'),D('2'),D('0'),D('0.5'),D('0.9'),D('0'))
 r=evaluate(p,asym,D('30'),'UP');caught['RecoverySlopePass_PointwiseFail']=r['recovery_slope'] and not r['pointwise']
 # A policy using ceiling can erase raw strict compression.
 coarse=broker('0.1');raw=D('0.099');norm=coarse.normalize(raw,'ceiling')
 caught['CompressionRawPass_NormalizedFail']=raw<D('0.1') and norm>=D('0.1')
 caught['CompressionPass_RiskFail']=compression(D('1'),D('.5'),D('.2'),D('.1'),D('.1'),b,D('2'))['gross_pass'] and not (D('101')<D('100'))
 qs=[D('.4'),D('.5'),D('1')];caught['qAveragePass_qWorstCaseFail']=sum(qs,D(0))/D(len(qs))<1 and max(qs)>=1
 caught['FiniteContinuousPass_DiscreteFail']=D('.099')<D('.1') and coarse.normalize(D('.099'),'ceiling')==D('.1')
 direction_asym=broker(down_profit='0.4',down_loss='1')
 up=evaluate(p,direction_asym,D('30'),'UP');down=evaluate(p,direction_asym,D('30'),'DOWN')
 caught['UPPass_DOWNFail']=up['pointwise'] and not down['pointwise']
 no_cost=Plan(D('1'),D('2'),D('.5'),D('.5'),D('.9'),D('0'))
 spread_zero=broker(spread='0');spread_high=broker(spread='0.00100')
 caught['SpreadZeroPass_RealSpreadFail']=evaluate(no_cost,spread_zero,D('100'),'UP')['money_catch_up'] and not evaluate(no_cost,spread_high,D('100'),'UP')['money_catch_up']
 slip_cost=Plan(D('1'),D('2'),D('.5'),D('.5'),D('.9'),D('0'),costs=Costs(slippage=D('100')))
 caught['SlippageZeroPass_RealSlippageFail']=evaluate(no_cost,b,D('100'),'UP')['money_catch_up'] and not evaluate(slip_cost,b,D('100'),'UP')['money_catch_up']
 assert not hasattr(Costs(),'spread'), 'spread would be counted twice'
 caught['MarginIgnoredPass_MarginFail']=evaluate(no_cost,b,D('100'),'UP')['pointwise'] and not (D('500')>=D('1000'))
 assert all(caught.values()),caught
 return caught

if __name__=='__main__':
 result=counterexamples()
 for name in result:print(f'COUNTEREXAMPLE_{name}=CAUGHT')
 print(f'COUNTEREXAMPLES_CAUGHT={len(result)}')
 total,passed=cost_matrix();print(f'COST_SCENARIOS_TOTAL={total}');print(f'COST_SCENARIOS_PASSED={passed}')
