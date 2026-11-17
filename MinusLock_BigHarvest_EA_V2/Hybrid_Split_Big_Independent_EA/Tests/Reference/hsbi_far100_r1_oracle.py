"""Independent research-only EURUSD arithmetic. Never imports production or sends orders."""
from __future__ import annotations
from dataclasses import dataclass,replace,asdict
from decimal import Decimal as D,localcontext,ROUND_FLOOR,ROUND_CEILING
from fractions import Fraction
from pathlib import Path
import json,hashlib,subprocess,datetime,sys,platform
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'Tests/Evidence/FAR100_R1'
ZERO=D('0');ONE=D('1');STEP=D('.01');TICK=D('.00001');CONTRACT=D('100000')
SOURCE= '8640bf464eda220d9096adb99bc8bcb390ed68e7'
def finite(x):return isinstance(x,D) and x.is_finite()
def grid(x,step=STEP,minimum=STEP,maximum=D('100')):
 return all(finite(v) for v in (x,step,minimum,maximum)) and step>0 and minimum<=x<=maximum and x%step==0
@dataclass(frozen=True)
class Position:
 identifier:str;role:str;direction:int;volume:D;open_price:D;swap_per_lot:D=D('-1')
def valid(p):return bool(p.identifier) and p.direction in (-1,1) and grid(p.volume) and finite(p.open_price) and p.open_price>0 and p.open_price%TICK==0 and finite(p.swap_per_lot)
def fixture(direction=-1):
 mirror=lambda p:D('2.20000')-D(p) if direction==1 else D(p)
 return [Position('MODEL_F0','FAR',direction,ONE,mirror('1.10000')),Position('MODEL_C0','BIG_CORE',-direction,D('1.20'),mirror('1.10500')),Position('MODEL_T0','BIG_TREND',-direction,D('.60'),mirror('1.10500')),Position('MODEL_S0','SMALL_BASE',direction,D('.50'),mirror('1.10500'))]
def quote(bid='1.10250',spread='.00020',direction=-1):
 bid=D(bid);ask=bid+D(spread)
 return (D('2.20000')-ask,D('2.20000')-bid) if direction==1 else (bid,ask)
def gross(p,bid,ask,volume=None):
 v=p.volume if volume is None else volume
 if not valid(p) or not grid(v) or v>p.volume or not all(finite(z) for z in (bid,ask)) or bid<=0 or ask<bid or bid%TICK or ask%TICK:raise ValueError('DOMAIN_OR_GRID')
 side=bid if p.direction==1 else ask
 return (side-p.open_price)*p.direction*v*CONTRACT
# Independent tick-count rational oracle; does not call Decimal PnL/cost functions.
def rational_net(p,bid,ask,volume=None,commission='3.5',slippage='1'):
 v=Fraction(str(p.volume if volume is None else volume));side=Fraction(str(bid if p.direction==1 else ask));entry=Fraction(str(p.open_price))
 ticks=(side-entry)/Fraction(1,100000)
 return p.direction*ticks*v+Fraction(str(p.swap_per_lot))*v-Fraction(commission)*v-Fraction(slippage)*v

def leg(p,bid,ask,volume=None,commission=D('3.5'),slippage=D('1'),fee=D('0'),profit_tick=D('1'),loss_tick=D('1')):
 v=p.volume if volume is None else volume;g=gross(p,bid,ask,v)
 # Asymmetric ticks are an explicitly separate synthetic payout, not EURUSD broker evidence.
 g=g*(profit_tick if g>=0 else loss_tick)
 return dict(PositionID=p.identifier,Role=p.role,Direction='BUY' if p.direction==1 else 'SELL',OpenPrice=p.open_price,OpenVolume=p.volume,ClosedVolume=v,ResidualVolume=p.volume-v,Bid=bid,Ask=ask,GrossPnL=g,Swap=p.swap_per_lot*v,Commission=-commission*v,Fee=-fee*v,Slippage=-slippage*v,NetPnL=g+p.swap_per_lot*v-commission*v-fee*v-slippage*v,ValueKind='SYNTHETIC_PROJECTED_CLOSE_NOT_BROKER_FILL')
def net(p,bid,ask,volume=None,**kw):return leg(p,bid,ask,volume,**kw)['NetPnL']
def geometry(f,ratios=(D('1.2'),D('.6'),D('.5')),step=STEP):
 if not finite(f) or not grid(f,step,step):return dict(valid=False,reason='FAR_OFF_GRID')
 floor=lambda x:(x/step).to_integral_value(rounding=ROUND_FLOOR)*step
 ceil=lambda x:(x/step).to_integral_value(rounding=ROUND_CEILING)*step
 c,t,s=floor(f*ratios[0]),floor(f*ratios[1]),ceil(f*ratios[2]);b=c+t-s;slope=b-f
 bounds=all(v==0 or grid(v,step,step) for v in (c,t,s)) and c>=step and s>=step
 return dict(F=f,C=c,T=t,S=s,Bnet=b,RecoverySlope=slope,valid=bounds and slope>0,reason='SLOPE_OR_GRID' if not(bounds and slope>0) else 'GEOMETRY_ONLY_VALID')
def exposure(ps):
 b=sum((p.volume for p in ps if p.direction==1),ZERO);s=sum((p.volume for p in ps if p.direction==-1),ZERO)
 return dict(GrossBUY=b,GrossSELL=s,NetLotSELLminusBUY=s-b,TotalGrossExposure=b+s)
def marks(ps,bid,ask):return sum((gross(p,bid,ask)+p.swap_per_lot*p.volume for p in ps),ZERO)
def close_value(ps,bid,ask):return sum((net(p,bid,ask) for p in ps),ZERO)
# InitialProfit 100 is economic but excluded from recovery. No historical harvest in main fixture.
DEPOSIT=D('100000');INITIAL=D('100');OPEN_RATE=D('3.5');OPEN_COST=D('11.55');R0=INITIAL-OPEN_COST
THRESHOLD=D('16');BUFFER=D('5');SHARE=D('.8')
def metrics(ps,bid,ask,r=R0,peak=D('100100')):
 exp=exposure(ps);u=marks(ps,bid,ask);liq=close_value(ps,bid,ask);balance=DEPOSIT+r;equity=balance+u
 mid=(bid+ask)/2;unit=CONTRACT*mid/D('100')
 margin_profiles={
  'SYN_GROSS_1_100':(exp['GrossBUY']+exp['GrossSELL'])*unit,
  'SYN_HEDGED_MAX':max(exp['GrossBUY'],exp['GrossSELL'])*unit,
  'SYN_HEDGED20':(max(exp['GrossBUY'],exp['GrossSELL'])+D('.2')*min(exp['GrossBUY'],exp['GrossSELL']))*unit}
 risks=[max(ZERO,u-marks(ps,bid+d,ask+d)) for d in [D('-.01'),D('.01')] if bid+d>0]
 risk=max(risks,default=ZERO)
 return dict(**exp,UnrealizedMarkNet=u,UnrealizedCloseNowNet=liq,RealizedCycleAll=r,RecoveryRealizedA=r-INITIAL,EconomicCycleCloseNow=r+liq,RecoveryPLCloseNowA=r-INITIAL+liq,Balance=balance,EquityMark=equity,EquityCloseNow=balance+liq,
 MarginProfiles={k:dict(MarginUsed=v,ProjectedMarginAfter=v,FreeMarginAfter=equity-v,MarginLevel=equity/v*100 if v else 'INFINITE_NO_MARGIN') for k,v in margin_profiles.items()},WorstCaseLoss='UNBOUNDED_MARKET_NOT_PROVEN',GapStressLoss=risk,RiskControlSymmetric100pip=risk,CycleDrawdown=max(ZERO,(DEPOSIT-equity)/DEPOSIT*100),AccountDrawdown=max(ZERO,(peak-equity)/peak*100),BrokerMarginProof='UNAVAILABLE',BrokerRiskProof='UNAVAILABLE')
def next_basket(core,n,bid,ask):
 g=geometry(n)
 if not g['valid']:return None
 far=replace(core,role='FAR',volume=n)
 d=-far.direction
 new=[Position('MODEL_NEXT_C','BIG_CORE',d,g['C'],ask if d==1 else bid,ZERO),Position('MODEL_NEXT_T','BIG_TREND',d,g['T'],ask if d==1 else bid,ZERO)]
 new.append(Position('MODEL_NEXT_S','SMALL_BASE',far.direction,g['S'],ask if far.direction==1 else bid,ZERO))
 # Zero T is geometrically allowed by some DTOs but not a valid money leg; fail closed.
 if any(not valid(p) for p in new):return None
 return [far]+new

def candidate_rows(direction=-1,policy='RESEARCH_ALPHA50',bid=None,ask=None):
 ps=fixture(direction);bid,ask=quote(direction=direction) if bid is None else (bid,ask)
 f,c,t,s=ps;g=geometry(ONE);old=metrics(ps,bid,ask);rows=[]
 alpha,minlots,minratio=(D('.5'),D('.01'),D('.5')) if policy=='RESEARCH_ALPHA50' else (D('.6'),D('.2'),D('.2'))
 for i in range(1,100):
  n=D(i)/100;compression=ONE-n;reasons=[]
  cm=net(s,bid,ask)+net(f,bid,ask)+net(t,bid,ask)+net(c,bid,ask,c.volume-n)
  residual=net(c,bid,ask,n);loss=max(ZERO,-cm)
  corefull=max(ZERO,net(c,bid,ask));corepart=max(ZERO,net(c,bid,ask,c.volume-n))
  a=max(ZERO,-net(f,bid,ask));cu=SHARE*corefull-a-BUFFER
  if n>alpha or compression<minlots or compression<minratio:reasons.append('COMPRESSION_LIMIT')
  if cu<=0:reasons.append('CORE_ONLY_CATCHUP_NONPOSITIVE')
  if loss>D('1000'):reasons.append('TRANSITION_CAP_1000')
  nxt=next_basket(c,n,bid,ask);nm=metrics(nxt,bid,ask,r=R0+cm-OPEN_RATE*sum((p.volume for p in nxt[1:]),ZERO)) if nxt else None
  if not nxt:reasons.append('NEXT_GEOMETRY_OR_MONEY_LEG')
  if nm and nm['TotalGrossExposure']>=old['TotalGrossExposure']:reasons.append('NEXT_GROSS_NOT_COMPRESSED')
  if nm and not nm['RiskControlSymmetric100pip']<old['RiskControlSymmetric100pip']-D('1'):reasons.append('SYN_RISK_NOT_REDUCED')
  # No authority is fabricated. Missing proofs remain listed even on mathematically rejected rows.
  negative=[net(s,bid,ask),net(f,bid,ask),net(t,bid,ask),net(c,bid,ask,c.volume-n)]
  pref=[];acc=ZERO
  for x in negative:acc+=x;pref.append(max(ZERO,-acc))
  cashneed=sum((max(ZERO,-v) for v in negative),ZERO)
  rows.append(dict(Direction='SELL' if direction==-1 else 'BUY',Policy=policy,CandidateN=n,Compression=compression,BrokerGrid='SYNTHETIC_GRID_VALID',Geometry=g,NextGeometry=geometry(n),RecoveryMoney=R0-INITIAL+cm+residual,
    CatchUp=cu,CatchUpPartialCore=SHARE*corepart-a-BUFFER,QuantityLHS=SHARE*g['Bnet'],FarObligationVolume=ONE,FarLossMoney=a,TransitionClosingNet=cm,TransitionLoss=loss,ResidualCoreCloseNowNet=residual,FullBasketCloseNowNet=close_value(ps,bid,ask),FundingPrefixNeed=max(pref),ConservativeFundingNeed=cashneed,TransitionBudgetAvailable=ZERO,
    RiskOld=old['RiskControlSymmetric100pip'],RiskNext=nm['RiskControlSymmetric100pip'] if nm else 'UNAVAILABLE',Margin=nm['MarginProfiles'] if nm else 'UNAVAILABLE',NextMetrics=nm,
    ActualResidual='UNAVAILABLE',SourceIdentity='UNAVAILABLE',FutureSmall='UNPROVEN',BrokerProof='UNAVAILABLE',FinalStatus='REJECT',RejectReasons=reasons+['ACTUAL_SOURCE_FUNDING_FUTURE_PROOFS_UNAVAILABLE']))
 return rows

def transition(n=D('.4'),direction=-1,bid=None,ask=None):
 ps=fixture(direction);bid,ask=quote(direction=direction) if bid is None else (bid,ask)
 f,c,t,s=ps;expected=close_value(ps,bid,ask);r=R0;rows=[]
 def snap(step,aid,p=None,v=ZERO,grossmoney=ZERO,cost=ZERO,deal=ZERO,kind='CONTROL',state='PROJECTED_ONLY_NOT_AUTHORIZED'):
  m=metrics(ps,bid,ask,r)
  rows.append(dict(Step=step,ActionID=aid,PositionIdentifier=p.identifier if p else 'UNAVAILABLE',RoleBefore=p.role if p else 'NONE',RoleAfter=('BIG_CORE' if p and p.role=='BIG_CORE' and v else 'CLOSED') if v else (p.role if p else 'NONE'),VolumeBefore=p.volume if p else ZERO,RequestedClose=v,ActualClosed='UNAVAILABLE',SimulatedClosed=v,VolumeAfter=p.volume-v if p else ZERO,FillStatus='SYNTHETIC_'+kind,DealIDs='MODEL_ONLY:'+aid,GrossMoney=grossmoney,Costs=cost,DealNet=deal,CyclePnL=m['EconomicCycleCloseNow'],Risk=m['RiskControlSymmetric100pip'],Margin=m['MarginProfiles'],State=state,Metrics=m,Positions=[asdict(x) for x in ps]))
 # Control steps are separate from physical fills. Trigger/provider/funding remain unavailable.
 for i,name in enumerate(['REVALIDATION','IMMUTABLE_PLAN','TRIGGER_HOLD_RETRACE_DEBOUNCE','FUNDING_AND_FOUR_CAPS'],1):snap(i,'MODEL_'+name)
 for k,(idx,v) in enumerate([(3,s.volume),(0,f.volume),(2,t.volume),(1,c.volume-n)]):
  p=next(x for x in ps if x.identifier==[f,c,t,s][idx].identifier)
  val=leg(p,bid,ask,v);dr=val['NetPnL'];r+=dr
  ps=[replace(x,volume=x.volume-v) if x.identifier==p.identifier else x for x in ps]
  ps=[x for x in ps if x.volume>0]
  # Fill price includes slippage; no second slippage deduction in simulated DealNet.
  slip_price=TICK;fill=(bid-slip_price) if p.direction==1 else (ask+slip_price)
  fillgross=(fill-p.open_price)*p.direction*v*CONTRACT
  assert fillgross+val['Swap']+val['Commission']+val['Fee']==dr
  snap(5+2*k,'MODEL_CLOSE_'+p.role,p,v,fillgross,-val['Swap']-val['Commission']-val['Fee'],dr,'COMPLETED_MODEL')
  snap(6+2*k,'MODEL_CONFIRM_'+p.role,p,kind='CONFIRM_MODEL')
  assert r+close_value(ps,bid,ask)==R0+expected
 for i,name in [(13,'READ_ACTUAL_RESIDUAL'),(14,'NEWFAR_SOLVER'),(15,'PROMOTION'),(16,'PERSIST'),(17,'RECONCILIATION'),(18,'NEXT_STATE')]:
  if i==15:ps=[replace(x,role='FAR') for x in ps]
  snap(i,'MODEL_'+name,ps[0] if ps else None,kind='COUNTERFACTUAL_CONTROL')
  if i==15:rows[-1]['RoleBefore']='BIG_CORE';rows[-1]['RoleAfter']='FAR'
 return dict(Status='COUNTERFACTUAL_ONLY_NOT_SOLVER_SELECTED',N=n,Direction=direction,Rows=rows,ClosingNet=r-R0,ResidualNet=close_value(ps,bid,ask),FullBasketNet=expected,RealBrokerFills=0)

class Barrier:
 """Reference metadata state, not a durable/native execution backend."""
 def __init__(self,expected=D('.50'),identifier='MODEL_S0'):
  self.expected=expected;self.identifier=identifier;self.filled=ZERO;self.events={};self.unknown=False;self.conflict=False
 def event(self,eventid,volume,identifier=None,complete=True):
  identifier=identifier or self.identifier;body=(str(volume),identifier,complete)
  if eventid in self.events:
   if self.events[eventid]!=body:self.conflict=True;return 'CONFLICT'
   return 'NO_OP'
  if not grid(volume) or identifier!=self.identifier or self.filled+volume>self.expected:self.conflict=True;return 'REJECT'
  self.events[eventid]=body;self.filled+=volume
  return 'COMPLETED_MODEL' if self.can_advance else 'PENDING'
 @property
 def can_advance(self):return self.filled==self.expected and not self.unknown and not self.conflict

def admission(x):
 """Research contract predicate; COMPONENT_ONLY is never broker permission."""
 if not x.get('fresh'):return 'STALE_SNAPSHOT'
 if not x.get('deals_complete'):return 'MISSING_DEAL'
 if not x.get('core_present'):return 'MISSING_CORE'
 if x.get('core_id')!=x.get('original_core_id'):return 'IDENTIFIER_MISMATCH'
 if x.get('far_count')!=1:return 'TWO_FAR_OR_MISSING_FAR'
 if not x.get('reconciled'):return 'UNRECONCILED'
 if x.get('outcome')!='COMPLETED':return 'PENDING_OR_UNKNOWN'
 if x.get('actual_residual')!=x.get('planned_residual'):return 'VOLUME_CHANGED'
 if not finite(x.get('free')) or not finite(x.get('need')):return 'NONFINITE_FUNDING'
 if x['free']<x['need']:return 'INSUFFICIENT_FUNDING'
 return 'COMPONENT_ONLY_NO_DISPATCH'

class Inventory:
 def __init__(self):self.sources={};self.free={};self.seen={}
 def post(self,key,body,amount):
  if key in self.sources:return 'NO_OP' if self.sources[key]==body else 'CONFLICT'
  if not finite(amount) or amount<0:return 'REJECT'
  self.sources[key]=body;self.free[key]=amount;return 'SOURCE_OBSERVED_MODEL'
 def debit(self,key,event,amount):
  if event in self.seen:return 'NO_OP' if self.seen[event]==(key,amount) else 'CONFLICT'
  if key not in self.free:return 'UNAVAILABLE'
  if not finite(amount) or amount<0:return 'REJECT'
  if amount>self.free[key]:return 'INSUFFICIENT_FREE'
  self.free[key]-=amount;self.seen[event]=(key,amount);return 'DEBIT_MODEL'

def dumps(obj):return json.dumps(obj,default=lambda x:format(x,'f') if isinstance(x,D) else str(x),ensure_ascii=False,indent=2)+'\n'
def make_data():
 OUT.mkdir(parents=True,exist_ok=True)
 stage=json.loads((OUT/'documentation_stage.json').read_text());assert stage['math_started'] is False
 candidates=[r for d in (-1,1) for policy in ['RESEARCH_ALPHA50','HISTORICAL_TEST_ALPHA60'] for r in candidate_rows(d,policy)]
 for row in candidates:row.pop('NextMetrics',None)
 (OUT/'new_far_candidates.json').write_text(json.dumps(candidates,default=lambda v:format(v,'f') if isinstance(v,D) else str(v),ensure_ascii=False,separators=(',',':'))+'\n')
 transitions=[transition(direction=d) for d in (-1,1)];(OUT/'physical_transitions.json').write_text(dumps(transitions))
 scenarios=[]
 for label,bid,spread,stale in [('A_STRONG_BIG','1.13000','.00020',False),('B_SMALL','1.10250','.00020',False),('E_LONG_TREND','1.20000','.00020',False),('F_GAP','1.08000','.00300',True),('G_SPREAD_COMMISSION','1.10500','.00200',False),('I_THRESHOLD','1.12419','.00020',False)]:
  for d in (-1,1):
   b,a=quote(bid,spread,d);ps=fixture(d);m=metrics(ps,b,a);legs=[leg(p,b,a,commission=D('50') if label.startswith('G_') else D('3.5')) for p in ps]
   if label.startswith('G_'):
    m['HighCommissionNet']=sum((x['NetPnL'] for x in legs),ZERO);m['HighCommissionRecoveryA']=R0-INITIAL+m['HighCommissionNet']
   scenarios.append(dict(Scenario=label,Direction=d,Bid=b,Ask=a,Stale=stale,Legs=legs,Metrics=m,OrdinaryFinalCloseResultGate=m['RecoveryPLCloseNowA']>=THRESHOLD and not stale,FinancialAuthorization='UNAVAILABLE',TriggerConfirmation='UNAVAILABLE',BrokerProof='UNAVAILABLE'))
 # After-flip return is diagnostic only, with inherited Core identity/open basis.
 for d in (-1,1):
  b,a=quote(direction=d);ps=next_basket(fixture(d)[1],D('.4'),b,a);br,ar=quote('1.10000',direction=d);tr=transition(direction=d)
  r=R0+tr['ClosingNet']-OPEN_RATE*sum((p.volume for p in ps[1:]),ZERO)
  scenarios.append(dict(Scenario='C_RETURN_AFTER_COUNTERFACTUAL_FLIP',Direction=d,N='0.40_DIAGNOSTIC_NOT_SELECTED',Positions=[asdict(p) for p in ps],Metrics=metrics(ps,br,ar,r),FinancialAuthorization='BLOCKED_PREDECESSOR_NOT_ADMISSIBLE'))
 (OUT/'scenarios.json').write_text(dumps(scenarios))
 multi=[]
 for d in (-1,1):
  rows=candidate_rows(d);validrows=[r for r in rows if r['FinalStatus']=='QUALIFIED']
  assert not validrows
  multi.append(dict(StartDirection=d,CompletedAuthorizedTransitions=0,PotentialTransition1='NO_SAFE_NEW_FAR',Reason='for every N: eligible Core<=0,full old Far loss275.50,buffer5 => margin -280.50;funding0;actual/native/future missing',Candidates=len(rows),Subsequent=[dict(Level=k,Status='NOT_REACHED',FarVolume='UNAVAILABLE',PositionID='UNAVAILABLE') for k in range(2,6)]))
 (OUT/'multi_transition.json').write_text(dumps(multi))
 curve=[];ps=fixture()
 for i in range(2501):
  b=D('1.10500')+D(i)*TICK;a=b+D('.00020')
  fn=net(ps[0],b,a);cn=net(ps[1],b,a);tn=net(ps[2],b,a)
  m=SHARE*max(ZERO,cn)-max(ZERO,-fn)-BUFFER
  mp=SHARE*max(ZERO,net(ps[1],b,a,D('.8')))-max(ZERO,-fn)-BUFFER
  curve.append(dict(Bid=b,Ask=a,RecoveryA=R0-INITIAL+close_value(ps,b,a),CoreOnlyCatchUp=m,ClosedCoreOnlyCatchUpN040=mp,CoreTrendConditionalCatchUp=SHARE*max(ZERO,cn+tn)-max(ZERO,-fn)-BUFFER,Authority='UNAVAILABLE'))
 (OUT/'control_price_curve.json').write_text(json.dumps(curve,default=lambda v:format(v,'f'),separators=(',',':'))+'\n')

 grids=[dict(step=str(st),F='1',geometry=geometry(ONE,step=st),terminal_at_min=[str(n) for n in [st] if not any(ZERO<D(i)*st<st for i in range(1,100))]) for st in [D('.01'),D('.1'),D('.25')]]
 (OUT/'grid_boundaries.json').write_text(dumps(grids))
 meta=dict(SourceCommitSHA=SOURCE,CheckedAtUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),ExecutionMode='LOCAL_RESEARCH_GIT_PLUS_GITHUB_MCP_PUBLICATION',python=sys.version,platform=platform.platform(),EvidenceClass='SYNTHETIC_MATH_ONLY',BrokerProof='UNAVAILABLE',NativeMQL5='NOT_RUN_METAEDITOR_NOT_FOUND',params=dict(Symbol='EURUSD_SYNTHETIC_USD',ContractSize=CONTRACT,TickSize=TICK,TickValueProfit='1',TickValueLoss='1',LotMin=STEP,LotMax='100',LotStep=STEP,Spread='.00020',OpeningCommissionPerLot='3.5',ClosingCommissionPerLot='3.5',AccruedSwapPerLot='-1',SlippagePerLot='1',Fee='0',StartingBalance=DEPOSIT+R0,StartingEquityMark=metrics(fixture(),*quote('1.10500'))['EquityMark'],InitialExcluded=INITIAL,HistoricalHarvest='0',TransitionBudget='0',FinalReserve='0',PartialFarBudget='0',ReserveShare='.8_RESEARCH_ONLY',MinProfit='10',SafetyBuffer='5',MoneyTolerance='1'))
 (OUT/'run_metadata.json').write_text(dumps(meta))
 print(dumps(dict(candidate_rows=len(candidates),physical_ledger_rows=sum(len(t['Rows']) for t in transitions),scenario_records=len(scenarios),qualified=0,math_result='MATH_AUDIT_UNPROVEN')))
if __name__=='__main__':make_data()
