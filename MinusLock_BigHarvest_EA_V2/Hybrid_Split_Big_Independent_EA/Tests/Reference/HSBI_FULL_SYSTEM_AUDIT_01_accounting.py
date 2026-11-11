"""Independent exact analytical accounting FIXTURE, not HSBI strategy/execution.
Fraction from decimal strings; synthetic unit-value contract, hedging positions.
No broker, signals, funding, persistence, administrative decisions or real IO.
"""
from fractions import Fraction as Q
from copy import deepcopy

def q(x):return x if isinstance(x,Q) else Q(str(x))
class Book:
 def __init__(self,capital='1000'):
  self.initial=q(capital);self.balance=self.initial-q('.37');self.bid=q(100);self.ask=q(101);self.history=True;self.events={};self.realized=-q('.37')
  self.positions={'Far':{'side':-1,'volume':q(1),'open':q(100)},'Core':{'side':1,'volume':q('1.2'),'open':q(101)},'Trend':{'side':1,'volume':q(1),'open':q(101)},'Small':{'side':-1,'volume':q('.5'),'open':q(100)}}
 def quote(self,bid,ask):
  bid,ask=q(bid),q(ask)
  if bid<=0 or ask<bid:raise ValueError('invalid analytical quote')
  self.bid,self.ask=bid,ask
 def mark(self,p):return p['volume']*p['side']*((self.bid if p['side']==1 else self.ask)-p['open'])
 def totals(self):
  floating=sum((self.mark(p) for p in self.positions.values()),q(0));gross=sum((p['volume'] for p in self.positions.values()),q(0));net=sum((p['side']*p['volume'] for p in self.positions.values()),q(0));equity=self.balance+floating;exitfees=gross*q('.1')
  return dict(Balance=self.balance,Equity=equity,Unrealized=floating,GrossLot=gross,NetLot=net,LiquidationCyclePnL=equity-self.initial-exitfees,OutstandingVolume=gross,MarginFixture=gross*self.bid/q(100),FreeMarginFixture=equity-gross*self.bid/q(100))
 def fill(self,role,volume,event,slippage='0'):
  if not self.history:return 'UNAVAILABLE'
  volume,slippage=q(volume),q(slippage);payload=(role,volume,self.bid,self.ask,slippage)
  if event in self.events:return 'NO_OP' if self.events[event]==payload else 'CONFLICT'
  p=self.positions[role]
  if volume<=0 or volume>p['volume'] or slippage<0:return 'REJECT'
  close=(self.bid-slippage) if p['side']==1 else (self.ask+slippage);net=volume*p['side']*(close-p['open'])-volume*q('.1');self.balance+=net;self.realized+=net;p['volume']-=volume;self.events[event]=payload;return 'APPLIED_IN_MEMORY_FIXTURE'

# Guard model: independent mathematical acceptance examples only, NOT production APIs.
# Each clause is intentionally separate so its mutation has a causal probe.
def property_holds(kind,d):
 if kind=='CONSERVATION':return d['G']==d['C']+d['R']+d['F'] and min(d['G'],d['C'],d['R'],d['F'])>=0
 if kind=='DOUBLE_FUNDING':return d['newSource'] not in d['fundedSources']
 if kind=='REPLAY_IDENTITY':return d['newPayload']==d['savedPayload']
 if kind=='SOURCE_NAMESPACE':return d['requestKey']==d['authorityKey']
 if kind=='NO_FALSE_NOOP':return d['profitA']==d['profitB'] and d['commissionA']==d['commissionB'] and d['netA']==d['netB']
 if kind=='UNAVAILABLE_NOT_NEW':return d['historyComplete'] and d['sourceConfirmed']
 if kind=='ATTRIBUTION':return d['bigCredit']==(d['posted'] if d['role'] in ('BigCore','BigTrend') else 0)
 if kind=='COST_COVERAGE':return d['requiredCosts']==d['coveredCosts']
 if kind=='LOT_LIMITS':return d['min']<=d['v']<=d['max'] and d['v']%d['step']==0
 if kind=='SIGNED_EXPOSURE':return d['reportedNet']==d['buy']-d['sell'] and d['reportedGross']==d['buy']+d['sell']
 if kind=='BALANCE_EQUITY':return d['equity']==d['balance']+d['floating']
 if kind=='AFFORDABILITY':return 0<d['amount']<=d['free']
 if kind=='FSM_COMPLETION':return d['completed'] and d['positionRead'] and d['historyComplete']
 if kind=='NO_HIDDEN_RESERVE':return d['reserveAfterPreview']==d['reserveBeforePreview']
 if kind=='SNAPSHOT_BINDING':return d['snapshotId']==d['receiptId'] and d['content']==d['receiptContent']
 raise ValueError('unknown property kind')
