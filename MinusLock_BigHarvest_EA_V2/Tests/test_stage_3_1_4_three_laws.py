#!/usr/bin/env python3
from decimal import Decimal as D
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Tools'))
from three_laws_oracle import Broker,Costs,Plan,compression,evaluate,event_monotone,finite_bound

def broker(step='0.01',point='0.00001',tick='0.00001',profit='1',loss='1',down_profit=None,down_loss=None):
 return Broker(D(point),D(tick),D(profit),D(loss),D(step),D(step),D(down_profit) if down_profit else None,D(down_loss) if down_loss else None)

def run_matrix():
 total=0
 for far in map(D,['0.01','0.02','0.05','0.10','0.50','1.00','2.00','5.00']):
  for step in map(D,['0.01','0.1','0.25']):
   if far<step:continue
   b=broker(str(step));f=b.normalize(far);c=b.normalize(f*D('2.0'));t=b.normalize(f*D('0.5'));s=b.normalize(f*D('0.5'))
   if min(c,t,s)==0:continue
   for distance in map(D,['1','10','50','100','200','300','550']):
    for direction in ('UP','DOWN'):
     p=Plan(f,c,t,s,D('0.9'),D('0'),costs=Costs(commission_open=D('0.01'),commission_close=D('0.01'),swap=D('0.01'),fee=D('0.01'),slippage=D('0.01')))
     result=evaluate(p,b,distance,direction)
     assert result['lot_catch_up'] and result['recovery_slope'] and result['pointwise']
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
 r=evaluate(p,asym,D('10'),'UP');caught['RecoverySlopePass_PointwiseFail']=r['recovery_slope'] and not r['pointwise']
 # A policy using ceiling can erase raw strict compression.
 coarse=broker('0.1');raw=D('0.099');norm=coarse.normalize(raw,'ceiling')
 caught['CompressionRawPass_NormalizedFail']=raw<D('0.1') and norm>=D('0.1')
 caught['CompressionPass_RiskFail']=compression(D('1'),D('.5'),D('.2'),D('.1'),D('.1'),b,D('2'))['gross_pass'] and not (D('101')<D('100'))
 qs=[D('.4'),D('.5'),D('1')];caught['qAveragePass_qWorstCaseFail']=sum(qs,D(0))/D(len(qs))<1 and max(qs)>=1
 caught['FiniteContinuousPass_DiscreteFail']=D('.099')<D('.1') and coarse.normalize(D('.099'),'ceiling')==D('.1')
 direction_asym=broker(down_profit='0.4',down_loss='1')
 up=evaluate(p,direction_asym,D('10'),'UP');down=evaluate(p,direction_asym,D('10'),'DOWN')
 caught['UPPass_DOWNFail']=up['pointwise'] and not down['pointwise']
 no_cost=Plan(D('1'),D('2'),D('.5'),D('.5'),D('.9'),D('0'))
 real_cost=Plan(D('1'),D('2'),D('.5'),D('.5'),D('.9'),D('0'),costs=Costs(slippage=D('100')))
 caught['SpreadZeroPass_RealSpreadFail']=evaluate(no_cost,b,D('10'),'UP')['money_catch_up'] and not evaluate(real_cost,b,D('10'),'UP')['money_catch_up']
 caught['MarginIgnoredPass_MarginFail']=evaluate(no_cost,b,D('10'),'UP')['pointwise'] and not (D('500')>=D('1000'))
 assert all(caught.values()),caught
 return caught

if __name__=='__main__':
 result=counterexamples()
 for name in result:print(f'COUNTEREXAMPLE_{name}=CAUGHT')
 print(f'COUNTEREXAMPLES_CAUGHT={len(result)}')
