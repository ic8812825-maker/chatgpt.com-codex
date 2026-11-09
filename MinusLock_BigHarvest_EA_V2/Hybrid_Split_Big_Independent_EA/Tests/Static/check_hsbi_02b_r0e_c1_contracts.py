#!/usr/bin/env python3
"""C1 literal scenarios + independent frozen integer/wire fixtures; no subject expected values."""
import argparse,copy,hashlib,json,sys,subprocess,ast
from pathlib import Path
from decimal import Decimal,localcontext
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2];BASE='074165b38f1b6d6253a9629c7d2def988e8e286a'
sys.path.insert(0,str(ROOT/'Tests/Reference'))
import hsbi_02b_r0e_c1_contract_model as subject
import check_hsbi_02b_r0d_contracts as wire
N=wire.N;view=wire.view
CATALOG_VERSION='HSBI-C1-REQUIRED-V1'
def checksum(x):return hashlib.sha256(wire.encode(x).encode()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def equal(a,b):return json.dumps(view(a),ensure_ascii=False,sort_keys=True,allow_nan=False)==json.dumps(view(b),ensure_ascii=False,sort_keys=True,allow_nan=False)
def record():
 return dict(identity=dict(Broker='B1',Server='S1',Account=1,Symbol='EURUSD',Magic=7,Cycle=1,Position=13,Deal=11,Order=12,Event=31,Role='BigCore',Plan=1,PolicyVersion=1,Revision=1,Snapshot=1),kind='ReconciledEconomicNet',entry='CLOSE',currency='USD',digits=2,profit=Decimal(50),swap=Decimal(0),commission=Decimal(0),fee=Decimal(0),rawNet=Decimal(50),postedNet=Decimal(50))
def grants(n='50',bucket='FinalReserve'):
 g={k:Decimal(0) for k in ('FinalReserve','PartialFar','Transition','Carry','ResidualHeld')};g[bucket]=Decimal(n);return g

def fixture(m=subject,principal='10',risk='0.5'):
 source=('B1','S1',1,11);r=record();history={wire.encode(source):r}
 core=dict(schema='HSBI-R0E-FREE-1',revision=1,sources={},allocations={},events={},journalComplete=True)
 status,core=m.fund(core,history,source,'A1',1,grants());assert status=='COMMITTED_IN_MEMORY'
 store=dict(schema='HSBI-C1-STORE-1',ledger=core,receipts={})
 payload=dict(kind='FUND',source=source,allocation='A1',event=1,grants=grants(),commit=True)
 journal={wire.encode(source[:3]+(1,)):dict(sequence=2,payload=payload,digest=checksum(payload))}
 allocation=dict(AllocationID='A1',source=source,allocationEvent=1,PolicyVersion=1,currency='USD',digits=2,grants=grants())
 context=dict(Plan=10,Revision=2,Snapshot=3,ConsumptionEventID=2,AllocationID='A1',BatchID='T1',CostSetID='COST1',PrincipalAmount=Decimal(principal),bucket='FinalReserve',purpose='CatchUp',intent='I1',fresh=True)
 refs=[('B1','S1',1,101),('B1','S1',1,102)]
 batch=dict(schema='HSBI-C1-BATCH-1',BatchID='T1',Broker='B1',Server='S1',Account=1,Symbol='EURUSD',Cycle=1,Order=21,Position=22,currency='USD',digits=2,expectedVolume=Decimal(1),RequiredDeals=tuple(refs),historyComplete=True,NettingPolicy='PROPOSED_SIGNED_BATCH_NET_V1',cap=Decimal(12))
 fills={wire.encode(k):dict(source=k,BatchID='T1',Symbol='EURUSD',Cycle=1,Order=21,Position=22,currency='USD',digits=2,volume=Decimal('0.4' if i==0 else '0.6'),net=Decimal(-5)) for i,k in enumerate(refs)}
 fact=dict(CostID='EXEC',Applicability='REQUIRED' if Decimal(risk)!=0 else 'KNOWN_ZERO',Amount=Decimal(risk),AmountBasis='NONNEGATIVE_RISK',currency='USD',RiskBasis='executionUncertainty',Window='I1',AlreadyIncluded=False,PolicyVersion=1,OverlapKnown=True)
 expectedCosts=dict(schema='HSBI-C1-COSTSET-1',Complete=True,currency='USD',digits=2,PolicyVersion=1,Authority='INDEPENDENT_FIXTURE_POLICY1',items=[fact])
 claims=[dict({k:v for k,v in fact.items() if k!='OverlapKnown'},AdditionalDeduction=Decimal(risk)!=0)]
 identity={k:r['identity'][k] for k in ('Broker','Server','Account','Symbol','Magic','Cycle','Position','Deal','Order','Role')}
 identity.update(EconomicEventID=31,AllocationEventID=1,ConsumptionEventID=2,AllocationID='A1',PolicyVersion=1,Plan=10,Revision=2,Snapshot=3)
 q=dict(schema='HSBI-C1-REQUEST-1',source=source,allocation='A1',allocationEvent=1,consumptionEvent=2,identity=identity,PrincipalAmount=Decimal(principal),bucket='FinalReserve',purpose='CatchUp',intent='I1',revision=2,BatchID='T1',CostSetID='COST1',costClaims=claims)
 a=dict(history=history,coreJournal=journal,receipts={},complete=True,allocations={'A1':allocation},context=context,batches={'T1':dict(refs=refs,expected=batch)},fillHistory=fills,costSets={'COST1':expectedCosts})
 return q,store,a

def advance_authority(a,q):
 """Independent receipt encoder from fixture operation and provider facts, never subject outputs."""
 a=copy.deepcopy(a);fact=a['costSets']['COST1']['items'][0];risk=fact['Amount'] if fact['Applicability']=='REQUIRED' and not fact['AlreadyIncluded'] else Decimal(0)
 # Values are small literal fixture decimals; normalize with independent integer wire N.
 debit=q['PrincipalAmount']
 def cents(x):
  token,n,d=wire.N(str(x));assert (int(n)*100)%int(d)==0;return (int(n)*100)//int(d)
 total=cents(debit)+cents(risk);required=Decimal(str(total//100)+'.'+str(total%100).zfill(2))
 payload=dict(kind='CONSUME_FREE',source=q['source'],allocation=q['allocation'],event=q['consumptionEvent'],bucket=q['bucket'],amount=debit,intent=q['intent'],purpose=q['purpose'],revision=q['revision'])
 ek=wire.encode(q['source'][:3]+(q['consumptionEvent'],));a['coreJournal'][ek]=dict(sequence=q['revision']+1,payload=payload,digest=checksum(payload))
 a['receipts'][ek]=dict(request=copy.deepcopy(q),digest=checksum(q),evaluationContext=copy.deepcopy(a['context']),DebitAmount=debit,RequiredBalance=required,AdditionalRisk=risk,sourceDigest=checksum(a['history'][wire.encode(q['source'])]),allocationDigest=checksum(a['allocations'][q['allocation']]),batchDigest=checksum(a['batches'][q['BatchID']]),costDigest=checksum(a['costSets'][q['CostSetID']]))
 return a

def state_summary(store):
 b=next(iter(store['ledger']['allocations'].values()))['buckets']['FinalReserve']
 return dict(free=view(b['RemainingFree']),consumed=view(b['Consumed']),reserved=view(b['Reserved']),revision=store['ledger']['revision'],receipts=len(store['receipts']))
def apply_case(m,edit=None,principal='10',risk='0.5'):
 q,s,a=fixture(m,principal,risk)
 if edit:edit(q,s,a)
 before=copy.deepcopy((q,s,a));result,out=m.apply_for_test(q,s,a)
 return dict(status=result['status'],state=state_summary(out),inputsUnchanged=view((q,s,a),True)==view(before,True),zeroDelta=view(out,True)==view(s,True))
def expected_apply(status='REJECT',free='50',consumed='0',revision=2,receipts=0):return dict(status=status,state=dict(free=N(free),consumed=N(consumed),reserved=N('0'),revision=revision,receipts=receipts),inputsUnchanged=True,zeroDelta=status!='COMMITTED_IN_MEMORY')
def identity_case(m,edit=None):
 q,s,a=fixture(m)
 if edit:edit(q,s,a)
 return m.verify_allocation_identity(q['identity'],a['history'],q['source'],a['context'],a['allocations']['A1'])
def batch_case(m,edit=None):
 q,s,a=fixture(m);b=a['batches']['T1']
 if edit:edit(b,a)
 r=m.assess_batch(b['refs'],a['fillHistory'],b['expected']);return view(r)
def costs_case(m,edit=None):
 q,s,a=fixture(m)
 if edit:edit(q,a)
 return view(m.cost_coverage(q['costClaims'],a['costSets']['COST1']))
def bad_source(m,kind):
 r=record();k=('B1','S1',1,11);h={wire.encode(k):r};s=m.new_registry();before=copy.deepcopy(s)
 if kind=='raw':r['rawNet']=Decimal(999)
 elif kind=='namespace':r['identity']['Account']=2
 elif kind=='grid':r['postedNet']=Decimal('50.005')
 status,out=m.fund(s,h,k,'A1',1,grants(),commit=kind!='grid')
 return dict(status=status,zeroDelta=view(out,True)==view(before,True))
def record_grid(m):
 r=record();r['postedNet']=Decimal('50.005')
 try:m.economic_record({wire.encode(('B1','S1',1,11)):r},('B1','S1',1,11));return 'ACCEPTED'
 except m.Malformed:return 'REJECT'
def replay_case(m,changed=False,authority_change=False,current_change=False):
 q,s,a=fixture(m);_,s=m.apply_for_test(q,s,a);a=advance_authority(a,q)
 if changed:q['intent']='CHANGED'
 if authority_change:a['history'][wire.encode(q['source'])]['profit']=Decimal(60);a['history'][wire.encode(q['source'])]['commission']=Decimal(-10)
 if current_change:a['context'].update(Plan=999,Revision=999,Snapshot=999)
 before=copy.deepcopy(s);r,out=m.apply_for_test(q,s,a)
 return dict(status=r['status'],zeroDelta=view(before,True)==view(out,True),state=state_summary(out))

def cases():
 out=[]
 def add(i,guard,op,run,expected,classes=('Positive',),input=None):
  out.append(dict(TestID=i,GuardID=guard,Operation=op,run=run,IndependentExpected=expected,Classes=list(classes),Input=input or dict(Profile='C1 independent fixture source50/Principal10/Risk0.5',Change=i)))
 add('APPLY-positive','COMPOSITION','apply_for_test',lambda m:apply_case(m),expected_apply('COMMITTED_IN_MEMORY','40','10',3,1))
 add('SOURCE-positive','SOURCE','fund',lambda m:fixture(m)[1]['ledger']['revision'],2)
 for kind in ('raw','namespace','grid'):add('SOURCE-'+kind,'SOURCE-'+kind.upper(),'fund',lambda m,k=kind:bad_source(m,k),dict(status='REJECT',zeroDelta=True),('Negative',))
 add('RECORD-grid','SOURCE-GRID','economic_record',record_grid,'REJECT',('Negative',))
 add('BALANCE-control','BALANCE','balance',lambda m:m.balance('50','10','15','25'),True)
 add('BALANCE-doublecount','BALANCE','balance',lambda m:m.balance('50','10','15','40'),False,('Negative',))
 add('APPLY-no-journal','JOURNAL','apply_for_test',lambda m:apply_case(m,lambda q,s,a:s['ledger'].__setitem__('journalComplete',False)),expected_apply('UNAVAILABLE'),('Negative','Composition'))
 def avail(m,unknown):
  q,s,a=fixture(m)
  if unknown:s['ledger']['journalComplete']=False
  return view(m.available(s,a,q['source'][:3]))
 add('AVAILABLE-control','JOURNAL','available',lambda m:avail(m,False),['KNOWN_MODEL_AVAILABLE',N('50')])
 add('AVAILABLE-incomplete','JOURNAL','available',lambda m:avail(m,True),['UNAVAILABLE',None],('Negative',))
 add('APPLY-missing-authority','COMPOSITION','apply_for_test',lambda m:apply_case(m,lambda q,s,a:a.__setitem__('history',None)),expected_apply('UNAVAILABLE'),('Negative','Composition'))
 add('APPLY-forged-allocation','ALLOCATION-VECTOR','apply_for_test',lambda m:apply_case(m,lambda q,s,a:a['allocations']['A1']['grants'].update(FinalReserve=Decimal(0),PartialFar=Decimal(50))),expected_apply(),('Negative','Composition'))
 add('IDENTITY-control','IDENTITY','verify_allocation_identity',identity_case,'PASS')
 for f in ('Broker','Server','Account','Symbol','Magic','Cycle','Position','Deal','Order','Role','EconomicEventID','AllocationEventID','ConsumptionEventID','AllocationID','PolicyVersion','Plan','Revision','Snapshot'):
  def foreign(q,s,a,f=f):q['identity'][f]=999 if type(q['identity'][f]) is int else 'FOREIGN'
  add('IDENTITY-foreign-'+f,'IDENTITY','verify_allocation_identity',lambda m,e=foreign:identity_case(m,e),'REJECT',('Negative','Identity conflict'))
 add('IDENTITY-allocation-event','ALLOCATION-EVENT','verify_allocation_identity',lambda m:identity_case(m,lambda q,s,a:a['allocations']['A1'].__setitem__('allocationEvent',999)),'REJECT',('Negative',))
 for label,value in [('none',None),('bool',True),('missing',{})]:add('IDENTITY-malformed-'+label,'MALFORMED','verify_allocation_identity',lambda m,v=value:identity_case(m,lambda q,s,a:q.__setitem__('identity',v)),'REJECT',('Negative',))
 add('IDENTITY-stale','SNAPSHOT','verify_allocation_identity',lambda m:identity_case(m,lambda q,s,a:a['context'].__setitem__('fresh',False)),'UNAVAILABLE',('Negative',))
 add('BATCH-control','BATCH','assess_batch',batch_case,dict(status='CONFIRMED',loss=N('10'),volume=N('1'),scope='BATCH_MEMBERSHIP_VERIFIED_FIXTURE'))
 def foreign_batch(b,a):
  old=b['refs'][1];new=('B1','S1',2,102);fill=a['fillHistory'].pop(wire.encode(old));fill.update(source=new,net=Decimal(100));a['fillHistory'][wire.encode(new)]=fill;b['refs'][1]=new;b['expected']['RequiredDeals']=(b['refs'][0],new);a['fillHistory'][wire.encode(b['refs'][0])]['net']=Decimal(-15)
 add('BATCH-foreign-account','BATCH-NAMESPACE','assess_batch',lambda m:batch_case(m,foreign_batch),dict(status='CONFLICT'),('Negative',))
 for f,val in [('BatchID','FOREIGN'),('Symbol','GBPUSD'),('Cycle',2),('Order',999),('Position',999),('currency','EUR'),('digits',3)]:
  add('BATCH-foreign-'+f,'BATCH-LINEAGE','assess_batch',lambda m,f=f,v=val:batch_case(m,lambda b,a:a['fillHistory'][wire.encode(b['refs'][0])].__setitem__(f,v)),dict(status='CONFLICT'),('Negative',))
 add('BATCH-pending','BATCH-COMPLETE','assess_batch',lambda m:batch_case(m,lambda b,a:b['refs'].pop()),dict(status='PENDING',loss=N('5'),volume=N('0.4')),('Boundary',))
 add('BATCH-overcap','BATCH-CAP','assess_batch',lambda m:batch_case(m,lambda b,a:a['fillHistory'][wire.encode(b['refs'][1])].__setitem__('net',Decimal(-10))),dict(status='OVER_CAP',loss=N('15'),volume=N('1')),('Negative',))
 add('BATCH-unknown-policy','BATCH','assess_batch',lambda m:batch_case(m,lambda b,a:b['expected'].__setitem__('NettingPolicy',None)),dict(status='UNAVAILABLE'),('Negative',))
 add('COST-control','COST','cost_coverage',costs_case,dict(status='COVERED',AdditionalRisk=N('.5'),scope='COMPLETE_APPLICABLE_FIXTURE_COSTSET'))
 add('COST-missing','COST-INVENTORY','cost_coverage',lambda m:costs_case(m,lambda q,a:q.__setitem__('costClaims',[])),dict(status='CONFLICT'),('Negative',))
 add('COST-omitted','COST-ONCE','cost_coverage',lambda m:costs_case(m,lambda q,a:q['costClaims'][0].__setitem__('AdditionalDeduction',False)),dict(status='CONFLICT'),('Negative',))
 add('COST-unknown','COST','cost_coverage',lambda m:costs_case(m,lambda q,a:a['costSets']['COST1']['items'][0].__setitem__('Applicability','UNKNOWN')),dict(status='UNAVAILABLE'),('Negative',))
 add('COST-duplicate','COST-INVENTORY','cost_coverage',lambda m:costs_case(m,lambda q,a:q['costClaims'].append(copy.deepcopy(q['costClaims'][0]))),dict(status='CONFLICT'),('Negative',))
 def zero_cost(m):
  q,s,a=fixture(m,risk='0');return view(m.cost_coverage(q['costClaims'],a['costSets']['COST1']))
 add('COST-knownzero','COST','cost_coverage',zero_cost,dict(status='COVERED',AdditionalRisk=N('0'),scope='COMPLETE_APPLICABLE_FIXTURE_COSTSET'),('Boundary',))
 def empty_cost(m):
  q,s,a=fixture(m);a['costSets']['COST1']['items']=[];return view(m.cost_coverage([],a['costSets']['COST1']))
 add('COST-knownempty','COST','cost_coverage',empty_cost,dict(status='COVERED',AdditionalRisk=N('0'),scope='COMPLETE_APPLICABLE_FIXTURE_COSTSET'))
 for cid,edit in [('batch',lambda q,s,a:a['fillHistory'][wire.encode(a['batches']['T1']['refs'][0])].__setitem__('Order',999)),('cost',lambda q,s,a:q['costClaims'][0].__setitem__('AdditionalDeduction',False)),('identity',lambda q,s,a:q['identity'].__setitem__('Magic',999)),('planned',lambda q,s,a:q.__setitem__('PrincipalAmount',Decimal(1)))]:
  add('APPLY-bypass-'+cid,'COMPOSITION-'+cid.upper(),'apply_for_test',lambda m,e=edit:apply_case(m,e),expected_apply(),('Negative','Composition'))
 add('APPLY-negative-amount','POSITIVE-AMOUNT','apply_for_test',lambda m:apply_case(m,lambda q,s,a:q.__setitem__('PrincipalAmount',Decimal(-10))),expected_apply(),('Negative',))
 add('APPLY-insufficient-headroom','COST-HEADROOM','apply_for_test',lambda m:apply_case(m,principal='50'),expected_apply(),('Negative',))
 add('APPLY-full','COMPOSITION','apply_for_test',lambda m:apply_case(m,principal='50',risk='0'),expected_apply('COMMITTED_IN_MEMORY','0','50',3,1),('Boundary','Conservation'))
 for label,kw,status in [('exact',{},'NO_OP'),('changed',dict(changed=True),'CONFLICT'),('authority',dict(authority_change=True),'CONFLICT'),('current-context',dict(current_change=True),'NO_OP')]:
  add('REPLAY-'+label,'REPLAY','apply_for_test',lambda m,kw=kw:replay_case(m,**kw),dict(status=status,zeroDelta=True,state=dict(free=N('40'),consumed=N('10'),reserved=N('0'),revision=3,receipts=1)),('Replay',))
 def recover_test(m,forged=False):
  q,s,a=fixture(m);_,s=m.apply_for_test(q,s,a);a=advance_authority(a,q)
  if forged:next(iter(s['ledger']['allocations'].values()))['buckets']['FinalReserve'].update(Consumed=Decimal(0),RemainingFree=Decimal(50))
  return m.recover_store(m.snapshot_store(s),None,a)['status']
 add('RECOVER-control','RECOVERY','recover_store',recover_test,'RECONCILED_MODEL_ONLY')
 add('RECOVER-forged','RECOVERY','recover_store',lambda m:recover_test(m,True),'UNAVAILABLE',('Negative',))
 add('BALANCE-no-reserve','BALANCE','balance',lambda m:m.balance('50','0','0','50'),True)
 def overfund(m):
  r=record();k=('B1','S1',1,11);h={wire.encode(k):r};_,s=m.fund(m.new_registry(),h,k,'A1',1,grants('40'),False);before=copy.deepcopy(s);status,out=m.fund(s,h,k,'A2',2,grants('20'),False);return dict(status=status,zeroDelta=view(out,True)==view(before,True))
 add('SOURCE-overfund','SOURCE-CAP','fund',overfund,dict(status='REJECT',zeroDelta=True),('Negative',))
 def special_source(m,kind):
  r=record();k=('B1','S1',1,11)
  if kind=='small':r['identity']['Role']='Small'
  else:r['kind']='ProjectedBasketNet'
  status,_=m.fund(m.new_registry(),{wire.encode(k):r},k,'A1',1,grants());return status
 for kind in ('small','projected'):add('SOURCE-'+kind,'SOURCE-'+kind.upper(),'fund',lambda m,k=kind:special_source(m,k),'REJECT',('Negative',))
 def fund_replay(m,change=False,history_change=False):
  q,s,a=fixture(m);g=grants('50','PartialFar') if change else grants()
  if history_change:a['history'][wire.encode(q['source'])].update(profit=Decimal(60),commission=Decimal(-10))
  status,out=m.fund(s['ledger'],a['history'],q['source'],'A1',1,g);return dict(status=status,zeroDelta=view(out,True)==view(s['ledger'],True))
 add('FUND-exact','FUND-REPLAY','fund',lambda m:fund_replay(m),dict(status='NO_OP',zeroDelta=True))
 add('FUND-changed','FUND-REPLAY','fund',lambda m:fund_replay(m,True),dict(status='CONFLICT',zeroDelta=True),('Negative',))
 add('FUND-authority-change','REPLAY-AUTHORITY','fund',lambda m:fund_replay(m,history_change=True),dict(status='CONFLICT',zeroDelta=True),('Negative',))
 def missing_external(m):
  q,s,a=fixture(m);a['coreJournal']=None;return view(m.available(s,a,q['source'][:3]))
 add('AVAILABLE-external-missing','JOURNAL','available',missing_external,['UNAVAILABLE',None],('Negative',))
 for field in ('allocations','context','batches','fillHistory','costSets','coreJournal','receipts'):
  add('APPLY-provider-missing-'+field,'AUTHORITY','apply_for_test',lambda m,f=field:apply_case(m,lambda q,s,a:a.__setitem__(f,None)),expected_apply('UNAVAILABLE'),('Negative','Composition'))
 def known_zero(m):
  _,_,a=fixture(m);a.update(history={},coreJournal={},receipts={});return view(m.available(m.new_store(),a,('B1','S1',1)))
 add('AVAILABLE-knownzero','JOURNAL','available',known_zero,['KNOWN_MODEL_AVAILABLE',N('0')])
 def request_bad(m,kind):
  q,s,a=fixture(m)
  if kind=='none':q=None
  elif kind=='bool':q=True
  elif kind=='schema':q['schema']='UNKNOWN-VERSION'
  elif kind=='missing':q.pop('intent')
  else:q['consumptionEvent']=kind
  before=copy.deepcopy(s);r,out=m.apply_for_test(q,s,a);return dict(status=r['status'],zeroDelta=view(out,True)==view(before,True))
 for label,value,status in [('none','none','REJECT'),('bool','bool','REJECT'),('schema','schema','UNAVAILABLE'),('missing','missing','REJECT'),('eventbool',True,'REJECT'),('eventfloat',1.5,'REJECT'),('eventzero',0,'REJECT')]:
  add('REQUEST-'+label,'MALFORMED','apply_for_test',lambda m,v=value:request_bad(m,v),dict(status=status,zeroDelta=True),('Negative',))
 def after_full(m):
  q,s,a=fixture(m,principal='50',risk='0');_,s=m.apply_for_test(q,s,a);a=advance_authority(a,q)
  q.update(consumptionEvent=3,revision=3,PrincipalAmount=Decimal('.01'));q['identity'].update(ConsumptionEventID=3,Revision=3);a['context'].update(ConsumptionEventID=3,Revision=3,PrincipalAmount=Decimal('.01'))
  before=copy.deepcopy(s);r,out=m.apply_for_test(q,s,a);return dict(status=r['status'],zeroDelta=view(before,True)==view(out,True))
 add('APPLY-after-full','COMPOSITION','apply_for_test',after_full,dict(status='REJECT',zeroDelta=True),('Negative','Conservation'))
 def token(m):
  q,s,a=fixture(m);r,out=m.apply_for_test(q,s,dict(status='ELIGIBLE_FOR_COMMIT'));return dict(status=r['status'],zeroDelta=view(s,True)==view(out,True))
 add('APPLY-token-not-authority','COMPOSITION','apply_for_test',token,dict(status='UNAVAILABLE',zeroDelta=True),('Negative','Composition'))
 def not_applicable(m):
  q,s,a=fixture(m,risk='0');a['costSets']['COST1']['items'][0]['Applicability']='NOT_APPLICABLE';q['costClaims'][0]['Applicability']='NOT_APPLICABLE';return view(m.cost_coverage(q['costClaims'],a['costSets']['COST1']))
 add('COST-not-applicable','COST','cost_coverage',not_applicable,dict(status='COVERED',AdditionalRisk=N('0'),scope='COMPLETE_APPLICABLE_FIXTURE_COSTSET'))
 add('BATCH-history-incomplete','BATCH','assess_batch',lambda m:batch_case(m,lambda b,a:b['expected'].__setitem__('historyComplete',False)),dict(status='UNAVAILABLE'),('Negative',))
 add('COST-provider-incomplete','COST','cost_coverage',lambda m:costs_case(m,lambda q,a:a['costSets']['COST1'].__setitem__('Complete',False)),dict(status='UNAVAILABLE'),('Negative',))
 def receipt_bad(m,kind):
  q,s,a=fixture(m);_,s=m.apply_for_test(q,s,a);a=advance_authority(a,q)
  if kind=='missing':s['receipts']={};a['receipts']={}
  else:
   ek=wire.encode(q['source'][:3]+(q['consumptionEvent'],));s['receipts'][ek]['sourceDigest']='0'*64;a['receipts'][ek]['sourceDigest']='0'*64
  return m.recover_store(m.snapshot_store(s),None,a)['status']
 add('RECOVER-no-receipt','RECEIPTS','recover_store',lambda m:receipt_bad(m,'missing'),'CONFLICT',('Negative',))
 add('RECOVER-bad-source-digest','RECEIPTS','recover_store',lambda m:receipt_bad(m,'source'),'CONFLICT',('Negative',))
 def historical_bad(m,kind):
  q,s,a=fixture(m);_,s=m.apply_for_test(q,s,a);a=advance_authority(a,q);ek=wire.encode(q['source'][:3]+(q['consumptionEvent'],));r=s['receipts'][ek]
  if kind=='identity':r['request']['identity']['Magic']=999;r['digest']=checksum(r['request'])
  elif kind=='allocation':r['allocationDigest']='0'*64
  else:r['evaluationContext']['PrincipalAmount']=Decimal(999)
  a['receipts']=copy.deepcopy(s['receipts']);return m.recover_store(m.snapshot_store(s),None,a)['status']
 for kind in ('identity','allocation','plan'):
  add('RECOVER-historical-'+kind,'HISTORICAL-RECEIPT','recover_store',lambda m,k=kind:historical_bad(m,k),'CONFLICT',('Negative',))
 def bad_digest_format(m):
  q,s,a=fixture(m);_,s=m.apply_for_test(q,s,a);a=advance_authority(a,q);ek=wire.encode(q['source'][:3]+(q['consumptionEvent'],));s['receipts'][ek]['batchDigest']='z'*64;a['receipts'][ek]['batchDigest']='z'*64;return m.recover_store(m.snapshot_store(s),None,a)['status']
 add('RECOVER-digest-format','DIGEST-FORMAT','recover_store',bad_digest_format,'CONFLICT',('Negative',))
 add('APPLY-bad-journal-entry','MALFORMED-JOURNAL','apply_for_test',lambda m:apply_case(m,lambda q,s,a:a['coreJournal'].__setitem__(next(iter(a['coreJournal'])),'BAD')),expected_apply(),('Negative',))
 add('APPLY-bad-store-source','MALFORMED-STORE','apply_for_test',lambda m:apply_case(m,lambda q,s,a:s['ledger']['sources'].__setitem__(next(iter(s['ledger']['sources'])),True)),expected_apply(),('Negative',))
 return out


def run(m=subject):
 rows=[];configs=wire.contexts();scenarios=cases();allowed={str(Path(m.__file__).resolve()) if hasattr(m,'__file__') else 'mutant',str(Path(subject.exact.__file__).resolve())}
 for index,ctx in enumerate(configs):
  for case in scenarios:
   calls=set();inputs=[]
   def profile(frame,event,arg):
    if event=='call' and frame.f_code.co_filename in allowed:
     calls.add(frame.f_code.co_name)
     if index==0 and frame.f_code.co_name==case['Operation']:inputs.append(view(dict(frame.f_locals)))
   with localcontext(ctx) as active:
    before=wire.context_state(active)
    try:
     sys.setprofile(profile);actual=view(case['run'](m));sys.setprofile(None)
     unchanged=wire.context_state(active)==before;expected=view(case['IndependentExpected']);ok=equal(actual,expected) and unchanged
     rows.append(dict(TestID=case['TestID'],GuardID=case['GuardID'],Operation=case['Operation'],ContextID=index,Input=dict(Profile=case['Input'],Calls=inputs) if index==0 else dict(Context0InputRef=case['TestID']),IndependentExpected=expected,Actual=actual,Result='PASS' if ok else 'FAIL',ContextUnchanged=unchanged,SubjectCalls=sorted(calls),Comparisons=2,ProofBoundary='C1 PROPOSED fixture API; no broker/durable/NewFar proof'))
    except Exception as e:
     sys.setprofile(None);rows.append(dict(TestID=case['TestID'],ContextID=index,Result='INFRASTRUCTURE_ERROR',ErrorType=type(e).__name__,Error=str(e),Comparisons=2,SubjectCalls=sorted(calls)))
 return dict(Scenarios=len(scenarios),ContextConfigurations=view([wire.context_state(c) for c in configs]),Executions=len(rows),Comparisons=sum(r['Comparisons'] for r in rows),Pass=sum(r['Result']=='PASS' for r in rows),Fail=sum(r['Result']=='FAIL' for r in rows),InfrastructureErrors=sum(r['Result']=='INFRASTRUCTURE_ERROR' for r in rows),Rows=rows)
def metadata():return dict(BaseSHA=BASE,TestedSHA=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),UTC=now(),ApprovalStatus='AWAITING_ADMIN_APPROVAL')
def hashes():return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__).resolve(),Path(subject.__file__),Path(subject.exact.__file__),Path(wire.__file__))}
def save(path,data):
 p=Path(path).resolve();assert p.is_relative_to(ROOT) and 'C1' in p.name;p.write_text(json.dumps(view(data),ensure_ascii=False,indent=2)+'\n')
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',default='Tests/Evidence/NEXT_STAGE_02B_R0E_C1_TEST_RESULTS.json');args=p.parse_args();started=now();out=dict(metadata(),**run(),StartedUtc=started,FinishedUtc=now(),Command=[sys.executable,*sys.argv],SourceHashes=hashes());out['ExitCode']=int(out['Fail']+out['InfrastructureErrors']>0);save(args.output,out)
 print(json.dumps({k:v for k,v in out.items() if k not in ('Rows','ContextConfigurations')}));print([r for r in out['Rows'] if r['Result']!='PASS'][:10]);return out['ExitCode']
if __name__=='__main__':raise SystemExit(main())
