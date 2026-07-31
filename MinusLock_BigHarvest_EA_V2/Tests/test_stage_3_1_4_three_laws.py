#!/usr/bin/env python3
from decimal import Decimal as D
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Tools'))
from three_laws_oracle import Broker,Costs,Plan,compression,evaluate,event_monotone,finite_bound

def broker(step='0.01',point='0.00001',tick='0.00001',profit='1',loss='1'):
 return Broker(D(point),D(tick),D(profit),D(loss),D(step),D(step))

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
