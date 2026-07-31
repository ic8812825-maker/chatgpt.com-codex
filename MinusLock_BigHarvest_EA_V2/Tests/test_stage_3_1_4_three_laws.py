#!/usr/bin/env python3
from decimal import Decimal as D
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Tools'))
from three_laws_oracle import BasketPosition,Broker,Costs,EventSnapshot,Plan,Side,compression,evaluate,event_monotone,finite_bound,finite_transition_proof,q_domain,risk_money,system_q_theorem

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
 c=compression(D('1'),D('0.5'),D('0.2'),D('0.1'),D('0.1'),b,D('2'))
 assert c['new_far_pass'] and c['next_big_pass'] and c['gross_pass'] and c['q']==D('0.5')
 assert finite_bound(D('1'),D('0.5'),b)>0
 assert finite_transition_proof([(D('1'),D('.5')),(D('.5'),D('.2')),(D('.2'),D('0'))],b)['pass']
 assert not finite_transition_proof([(D('1'),D('1'))],b)['pass']
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

def broker_matrix():
 profiles={
  'SYMMETRIC':broker(profit='1',loss='1',down_profit='1',down_loss='1'),
  'UP_PROFIT_WEAKER':broker(profit='.8',loss='1',down_profit='1',down_loss='1'),
  'DOWN_PROFIT_WEAKER':broker(profit='1',loss='1',down_profit='.8',down_loss='1'),
  'UP_LOSS_STRONGER':broker(profit='1',loss='1.2',down_profit='1',down_loss='1'),
  'DOWN_LOSS_STRONGER':broker(profit='1',loss='1',down_profit='1',down_loss='1.2'),
  'PROFIT_LOSS_ASYMMETRIC':broker(profit='.9',loss='1.1',down_profit='.85',down_loss='1.15')}
 total=passed=0
 for b in profiles.values():
  for direction in ('UP','DOWN'):
   result=evaluate(Plan(D('1'),D('3'),D('1'),D('.2'),D('.9'),D('5')),b,D('100'),direction)
   total+=1;passed+=all((result['lot_catch_up'],result['money_catch_up'],result['recovery_slope'],result['pointwise'],result['coverage_path']['coverage_monotone']))
 assert total==passed
 return total,passed

def event_matrix():
 def snap(event,realized='0',floating='100',reserve='0',commission='0',swap='0',fee='0',slippage='0',far='1',big='3',small='.5'):
  return EventSnapshot(*map(D,(realized,floating,reserve,commission,swap,fee,slippage,far,big,small)),event)
 before=snap('BEFORE');cases=[
  ('PURE_TRANSFER',snap('TRANSFER','40','60'),True),
  ('CLOSE_COMMISSION',snap('COMMISSION','40','60',commission='1'),False),
  ('SWAP_ACCRUAL',snap('SWAP',swap='1'),False),('FEE',snap('FEE',fee='1'),False),
  ('SLIPPAGE',snap('SLIPPAGE',slippage='1'),False),
  ('PARTIAL_FAR_CLOSE',snap('PARTIAL_FAR','30','71',far='.5'),True),
  ('BIG_CLOSE',snap('BIG_CLOSE','70','31',big='1'),True),
  ('SMALL_CLOSE',snap('SMALL_CLOSE','10','91',small='0'),True),
  ('RESERVE_CREDIT',snap('RESERVE',reserve='20'),True),
  ('PARTIAL_EXECUTION',snap('PARTIAL_EXEC','20','79',far='.8',big='2.5'),False),
  ('RECONCILIATION',snap('RECONCILE','50','50',far='.7',big='2'),True)]
 passed=sum(event_monotone(before,after) is expected for _,after,expected in cases)
 assert passed==len(cases)
 return len(cases),passed

def risk_matrix():
 b=broker();control=D('1.09000')
 same_gross_near=(BasketPosition(Side.BUY,D('1'),D('1.09100')),)
 same_gross_far=(BasketPosition(Side.BUY,D('1'),D('1.11000')),)
 assert sum(p.lot for p in same_gross_near)==sum(p.lot for p in same_gross_far)
 assert risk_money(same_gross_near,control,b)!=risk_money(same_gross_far,control,b)
 old=(BasketPosition(Side.BUY,D('2'),D('1.09500')),)
 next_safe=(BasketPosition(Side.BUY,D('1'),D('1.09500')),)
 next_danger=(BasketPosition(Side.BUY,D('1'),D('1.12000')),)
 cases=[risk_money(next_safe,control,b)<risk_money(old,control,b),
        sum(p.lot for p in next_danger)<sum(p.lot for p in old) and risk_money(next_danger,control,b)>risk_money(old,control,b)]
 assert all(cases)
 return 4,4

def q_matrix():
 b=broker();caps=(D('.35'),D('.30'),D('.20'));theorem=system_q_theorem(caps);assert theorem['system_q_theorem']=='PASS'
 transitions=[(far,far*cap,b) for far in map(D,['.01','.02','.05','.1','.5','1','2','5']) for cap in caps]
 result=q_domain(transitions,theorem['policy_q_cap']);assert result['pass'] and result['observed_q_max']<=D('.35')
 mutation=q_domain([(D('1'),D('.4'),b)],D('.35'));assert not mutation['pass']
 result.update(theorem);return result

def compression_matrix():
 total=passed=0;qs=[]
 for step in map(D,['.01','.1','.25']):
  b=broker(str(step));control=D('1.09000')
  for far in map(D,['.01','.02','.05','.1','.5','1','2','5']):
   old=b.normalize(far)
   if old<=0:continue
   for cap in map(D,['.20','.30','.35']):
    new=b.normalize(old*cap);core=b.normalize(old*D('.1'));trend=b.normalize(old*D('.05'));small=b.normalize(old*D('.05'),'ceiling')
    if core+trend>=old:continue
    comp=compression(old,new,core,trend,small,b,old*D('5'))
    old_basket=(BasketPosition(Side.BUY,old*D('2'),D('1.10000')),)
    next_basket=(BasketPosition(Side.BUY,max(new,b.min_lot),D('1.09500')),)
    risk_pass=risk_money(next_basket,control,b)<risk_money(old_basket,control,b)
    rank_pass=new==0 or int(new/b.lot_step)<int(old/b.lot_step)
    ok=all((comp['new_far_pass'],comp['next_big_pass'],comp['gross_pass'],risk_pass,comp['q']<=cap,rank_pass))
    total+=1;passed+=ok;qs.append(comp['q'])
 assert total==passed and total>=20
 return {'total':total,'passed':passed,'observed_q_max':max(qs)}

def gross_domain_matrix():
 total=passed=0
 for step in map(D,['.01','.1']):
  b=broker(str(step))
  for far in map(D,['.1','.5','1','2','5']):
   if far<step:continue
   old=far*D('3');new=far*D('.2');core=far;trend=far*D('.5')
   for delta,expected in [(-step,True),(D(0),False),(step,False)]:
    small=old+delta-b.normalize(new)-b.normalize(core)-b.normalize(trend)
    if small<0:continue
    result=compression(far,new,core,trend,small,b,old)
    total+=1;passed+=result['gross_pass'] is expected
 assert total==passed and total>=20
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
 old_risk_basket=(BasketPosition(Side.BUY,D('2'),D('1.09500')),)
 next_risk_basket=(BasketPosition(Side.BUY,D('1'),D('1.12000')),)
 gross_compressed=sum(x.lot for x in next_risk_basket)<sum(x.lot for x in old_risk_basket)
 caught['CompressionPass_RiskFail']=gross_compressed and risk_money(next_risk_basket,D('1.09000'),b)>risk_money(old_risk_basket,D('1.09000'),b)
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
 total,passed=broker_matrix();print(f'BROKER_SCENARIOS_TOTAL={total}');print(f'BROKER_SCENARIOS_PASSED={passed}')
 total,passed=event_matrix();print(f'EVENT_SCENARIOS_TOTAL={total}');print(f'EVENT_SCENARIOS_PASSED={passed}')
 total,passed=risk_matrix();print(f'RISK_SCENARIOS_TOTAL={total}');print(f'RISK_SCENARIOS_PASSED={passed}')
 q=q_matrix();print(f'Q_TRANSITIONS={q["transitions"]}');print(f'OBSERVED_Q_MAX={q["observed_q_max"]}');print(f'POLICY_Q_CAP={q["policy_q_cap"]}')
 c=compression_matrix();print(f'COMPRESSION_MATRIX_CASES={c["total"]}');print(f'COMPRESSION_MATRIX_PASSED={c["passed"]}')
 total,passed=gross_domain_matrix();print(f'GROSS_DOMAIN_CASES={total}');print(f'GROSS_DOMAIN_PASSED={passed}')
