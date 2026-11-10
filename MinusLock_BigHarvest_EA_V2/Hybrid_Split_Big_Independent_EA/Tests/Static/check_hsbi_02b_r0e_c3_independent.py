#!/usr/bin/env python3
"""Independent C3 literals + integer/scale oracle; no subject expected evaluator."""
import copy,sys,json,types,hashlib,subprocess,tempfile,shutil,re
from pathlib import Path
import check_hsbi_02b_r0e_c3_common as a
import hsbi_02b_r0e_c3_mathematical_oracle as oracle
m=a.subject
CAPTURED_TRACES=[]

def cents(x,d=2):
 # Subject numeric output inspected as rational; expected is independent integer units.
 n=x.numerator if hasattr(x,'numerator') else oracle.units(str(x),d);den=x.denominator if hasattr(x,'denominator') else 10**d
 assert (n*10**d)%den==0;return n*10**d//den

def summary(s):
 r=next(iter(s['ledger']['allocations'].values()))['buckets']['FinalReserve'];return dict(Grant=cents(r['OriginalGrant']),Consumed=cents(r['Consumed']),Reserved=cents(r['Reserved']),Free=cents(r['RemainingFree']),Revision=s['ledger']['revision'],Receipts=len(s['receipts']))

def invoke(pub,sub=m,edit=None,committed=False):
 q,s,au=a.fixture(sub)
 if committed:
  _,s=sub.apply_for_test(q,s,au);au=a.c2.advance_authority(au,q)
 if edit:edit(q,s,au)
 before=copy.deepcopy((q,s,au))
 def call():
  if pub=='authorize':return sub.authorize(q,s,au),s
  if pub=='apply_for_test':return sub.apply_for_test(q,s,au)
  if pub=='available':r,n=sub.available(s,au,q['source'][:3]);return dict(status=r,FreeCents=None if n is None else cents(n)),s
  if pub=='assess_batch':b=au['batches']['T1'];return sub.assess_batch(b['refs'],au['fillHistory'],b['expected']),s
  if pub=='cost_coverage':return sub.cost_coverage(q['costClaims'],au['costSets']['COST1']),s
  if pub=='verify_allocation_identity':return dict(status=sub.verify_allocation_identity(q['identity'],au['history'],q['source'],au['context'],au['allocations']['A1'])),s
  if pub=='recover_store':r=sub.recover_store(sub.snapshot_store(s),None,au);return r,r['store'] if r.get('store') is not None else s
  raise ValueError(pub)
 (r,out),calls,lines=a.trace(call,sub)
 CAPTURED_TRACES.append(dict(PublicAPI=pub,Status=r['status'],Calls=calls,Lines=lines,StateBefore=summary(s),StateAfter=summary(out),InputsUnchanged=a.same((q,s,au),before)))
 return dict(Status=r['status'],Before=summary(s),After=summary(out),ZeroDelta=a.same(s,out),InputsUnchanged=a.same((q,s,au),before),Calls=calls,Lines=lines,Details=a.view({k:v for k,v in r.items() if k!='store'}))

def base_summary():return dict(Grant=5000,Consumed=0,Reserved=0,Free=5000,Revision=2,Receipts=0)
def test_cases():
 cases=[]
 def add(i,req,fn,expected,kind='REFERENCE',scope='PYTHON_REFERENCE'):
  cases.append(dict(TestID='C3-'+i,RequirementID=req,Run=fn,Expected=expected,Kind=kind,ProofBoundary=scope))
 pubs={'authorize':'ELIGIBLE_FOR_COMMIT','apply_for_test':'COMMITTED_IN_MEMORY','available':'KNOWN_MODEL_AVAILABLE','assess_batch':'CONFIRMED','cost_coverage':'COVERED','verify_allocation_identity':'PASS','recover_store':'RECONCILED_MODEL_ONLY'}
 for pub,status in pubs.items():
  def control(p=pub):
   r=invoke(p);return dict(Status=r['Status'],InputsUnchanged=r['InputsUnchanged'],After=r['After'],GuardObserved=p in r['Calls'])
  exp=base_summary()
  if pub=='apply_for_test':exp=dict(Grant=5000,Consumed=1000,Reserved=0,Free=4000,Revision=3,Receipts=1)
  add('PUBLIC-'+pub,'COMPOSITION',control,dict(Status=status,InputsUnchanged=True,After=exp,GuardObserved=True))
 for field in ('Account','Magic','Cycle','Deal','Order','Position','EconomicEventID','AllocationEventID','ConsumptionEventID','AllocationID','PolicyVersion','Plan','Revision','Snapshot','Broker','Server','Symbol','Role'):
  def bad(f=field):
   r=invoke('apply_for_test',edit=lambda q,s,au:q['identity'].__setitem__(f,999 if type(q['identity'][f]) is int else 'FOREIGN'));return dict(Status=r['Status'],ZeroDelta=r['ZeroDelta'],InputsUnchanged=r['InputsUnchanged'])
  add('FOREIGN-'+field,'D08',bad,dict(Status='REJECT',ZeroDelta=True,InputsUnchanged=True))
 edits=[('journal-missing',lambda q,s,au:au.__setitem__('coreJournal',None),'UNAVAILABLE'),('journal-incomplete',lambda q,s,au:s['ledger'].__setitem__('journalComplete',False),'UNAVAILABLE'),('cost-missing',lambda q,s,au:q.__setitem__('costClaims',[]),'REJECT'),('batch-foreign',lambda q,s,au:au['fillHistory'][a.wire.encode(au['batches']['T1']['refs'][0])].__setitem__('Order',999),'REJECT'),('purpose',lambda q,s,au:q.__setitem__('purpose','FinalClose'),'REJECT'),('intent',lambda q,s,au:q.__setitem__('intent','OTHER'),'REJECT'),('identity-none',lambda q,s,au:q.__setitem__('identity',None),'REJECT'),('event-bool',lambda q,s,au:q.__setitem__('consumptionEvent',True),'REJECT'),('event-zero',lambda q,s,au:q.__setitem__('consumptionEvent',0),'REJECT'),('batch-none',lambda q,s,au:au['batches']['T1'].__setitem__('expected',None),'UNAVAILABLE'),('precision',lambda q,s,au:au['allocations']['A1'].__setitem__('digits',3),'REJECT'),('currency',lambda q,s,au:au['allocations']['A1'].__setitem__('currency','EUR'),'REJECT')]
 for name,edit,status in edits:
  def neg(e=edit):
   r=invoke('apply_for_test',edit=e);return dict(Status=r['Status'],ZeroDelta=r['ZeroDelta'],InputsUnchanged=r['InputsUnchanged'])
  add('GATE-'+name,'COMPOSITION',neg,dict(Status=status,ZeroDelta=True,InputsUnchanged=True))
 def insufficient():
  def edit(q,s,au):q['PrincipalAmount']=a.c2.Decimal(50);au['context']['PrincipalAmount']=a.c2.Decimal(50)
  r=invoke('apply_for_test',edit=edit);return [r['Status'],r['ZeroDelta'],r['InputsUnchanged'],'available' in r['Calls']]
 add('INSUFFICIENT-HEADROOM','D01/D06',insufficient,['REJECT',True,True,True])
 def full_public_chain():
  q,s,au=a.fixture(m,principal='50',risk='0');r,s=m.apply_for_test(q,s,au);states=[summary(s)];statuses=[r['status']];au=a.c2.advance_authority(au,q);before=copy.deepcopy(s);r,out=m.apply_for_test(q,s,au);statuses.append(r['status']);no_delta=a.same(before,out)
  q.update(consumptionEvent=3,revision=3,PrincipalAmount=a.c2.Decimal('.01'));q['identity'].update(ConsumptionEventID=3,Revision=3);au['context'].update(ConsumptionEventID=3,Revision=3,PrincipalAmount=a.c2.Decimal('.01'));r,out=m.apply_for_test(q,s,au);statuses.append(r['status']);no_delta&=a.same(before,out)
  return dict(statuses=statuses,consumed=states[0]['Consumed'],free=states[0]['Free'],replayAndRejectZeroDelta=no_delta)
 add('FULL-CONSUMPTION-PUBLIC','D01/D07',full_public_chain,dict(statuses=['COMMITTED_IN_MEMORY','NO_OP','REJECT'],consumed=5000,free=0,replayAndRejectZeroDelta=True))
 def raw_signed():
  r=a.c2.frozen.record();r.update(profit=60,swap=-2,commission=-7,fee=-1,rawNet=50,postedNet=50);src=('B1','S1',1,11);status,state=m.fund(m.new_registry(),{a.wire.encode(src):r},src,'A',1,a.c2.frozen.grants());row=next(iter(state['allocations'].values()))['buckets']['FinalReserve'];return dict(status=status,grant=cents(row['OriginalGrant']))
 add('SIGNED-COMPONENTS','D01/D06',raw_signed,dict(status='COMMITTED_IN_MEMORY',grant=5000))
 def nonpositive_source(net):
  r=a.c2.frozen.record();r.update(profit=net,swap=0,commission=0,fee=0,rawNet=net,postedNet=net);src=('B1','S1',1,11);h={a.wire.encode(src):r};status,state=m.fund(m.new_registry(),h,src,'ZERO',1,a.c2.frozen.grants('0'));before=copy.deepcopy(state);spend,after=m._operate_for_registry_replay(state,h,src,'ZERO',2,'CONSUME_FREE','FinalReserve','.01');row=next(iter(state['allocations'].values()))['buckets']['FinalReserve'];return [status,cents(row['OriginalGrant']),spend,a.same(before,after)]
 add('ZERO-SOURCE','D01/D02',lambda:nonpositive_source(0),['COMMITTED_IN_MEMORY',0,'REJECT',True],scope='SOURCE_LOCAL_ZERO_GRANT_NOT_GLOBAL_ACCOUNT_CASH')
 add('NEGATIVE-SOURCE','D01/D02',lambda:nonpositive_source(-5),['COMMITTED_IN_MEMORY',0,'UNAVAILABLE',True],scope='NEGATIVE_ECONOMIC_SOURCE_ZERO_ALLOCATION_GLOBAL_DEBITS_UNPROVEN')
 def allocation_path():
  r=a.c2.frozen.record();src=('B1','S1',1,11);h={a.wire.encode(src):r};state=m.new_registry();st,state=m.fund(state,h,src,'P1',1,a.c2.frozen.grants('40'),False);before=copy.deepcopy(state);spend,after=m._operate_for_registry_replay(state,h,src,'P1',3,'CONSUME_FREE','FinalReserve','1');blocked=a.same(before,after)
  st2,state=m.fund(state,h,src,'P2',2,a.c2.frozen.grants('10'),True);before=copy.deepcopy(state);st3,after=m.fund(state,h,src,'P3',4,a.c2.frozen.grants('1'),True);grant=sum(cents(v['buckets']['FinalReserve']['OriginalGrant']) for v in state['allocations'].values())
  return dict(statuses=[st,spend,st2,st3],preparedSpendZeroDelta=blocked,overfundZeroDelta=a.same(before,after),grants=grant)
 add('CROSS-ALLOCATION-CONSERVATION','D01/FUNDING-GLOBAL-ATTRIBUTION',allocation_path,dict(statuses=['COMMITTED_IN_MEMORY','REJECT','COMMITTED_IN_MEMORY','REJECT'],preparedSpendZeroDelta=True,overfundZeroDelta=True,grants=5000),scope='SINGLE_SOURCE_REGISTRY_NOT_GLOBAL_ECONOMIC_DEBIT_ATTRIBUTION')
 def small():
  r=a.c2.frozen.record();r['identity']['Role']='Small';r.update(profit=10,rawNet=10,postedNet=10);src=('B1','S1',1,11);g=a.c2.frozen.grants('10','ResidualHeld');st,s=m.fund(m.new_registry(),{a.wire.encode(src):r},src,'S',1,g);rows=next(iter(s['allocations'].values()))['buckets'];return [st,cents(rows['FinalReserve']['OriginalGrant']),cents(rows['ResidualHeld']['OriginalGrant'])]
 add('SMALL-ISOLATION','D03',small,['COMMITTED_IN_MEMORY',0,1000])
 def reserve_path():
  q,s,au=a.fixture(m);state=s['ledger'];events=[];statuses=[]
  for event,kind,amount,owner in [(3,'RESERVE','15','OWNER1'),(4,'CONSUME_RESERVED','1','OWNER2'),(5,'CONSUME_FREE','10','OWNER1'),(6,'RELEASE','5','OWNER1'),(7,'CONSUME_RESERVED','10','OWNER1')]:
   before=copy.deepcopy(state);status,out=m._operate_for_registry_replay(state,au['history'],q['source'],'A1',event,kind,'FinalReserve',amount,owner,'CatchUp');state=out;row=next(iter(state['allocations'].values()))['buckets']['FinalReserve'];v=[cents(row[k]) for k in ('OriginalGrant','Consumed','Reserved','RemainingFree')];assert oracle.money_state(*v);statuses.append(status);events.append(dict(Before=a.view(before),After=a.view(out),Kind=kind,Owner=owner,Status=status))
  return dict(statuses=statuses,final=v,trace=events)
 def reserve_values():r=reserve_path();return dict(statuses=r['statuses'],final=r['final'])
 add('RESERVATION-OWNERSHIP','D01/D07',reserve_values,dict(statuses=['COMMITTED_IN_MEMORY','REJECT','COMMITTED_IN_MEMORY','COMMITTED_IN_MEMORY','COMMITTED_IN_MEMORY'],final=[5000,2000,0,3000]),scope='PYTHON_MATHEMATICAL_PRIVATE_REGISTRY_NOT_COMPOSED_AUTHORIZATION')
 def sequence():
  r=m.exact.sequential('1e28',['0.01','0.01']);e=oracle.sequential(10**30,[1,1]);return dict(status=r['status'],remaining=cents(r['remaining']),expectedIndependent=e['remaining'],local=all(cents(v['ReserveBefore'])-cents(v['Consumption'])==cents(v['ReserveAfter']) for v in r['trace']))
 add('LARGE-SMALL-DEBITS','NUM-EXACT-1',sequence,dict(status='CONSERVATION_ONLY',remaining=10**30-2,expectedIndependent=10**30-2,local=True))
 def replay(changed=False):
  q,s,au=a.fixture(m);_,s=m.apply_for_test(q,s,au);au=a.c2.advance_authority(au,q)
  if changed:q['intent']='CHANGED'
  before=copy.deepcopy(s);r,o=m.apply_for_test(q,s,au);return [r['status'],a.same(before,o)]
 add('EXACT-REPLAY','D07',replay,['NO_OP',True]);add('ALTERED-REPLAY','D07',lambda:replay(True),['CONFLICT',True])
 def netting():
  q,s,au=a.fixture(m);b=au['batches']['T1'];k0,k1=b['refs'];au['fillHistory'][a.wire.encode(k0)]['net']=-15;au['fillHistory'][a.wire.encode(k1)]['net']=100
  first=m.assess_batch([k0],au['fillHistory'],b['expected']);final=m.assess_batch(b['refs'],au['fillHistory'],b['expected']);e=oracle.transition([-1500,10000],1200)
  return dict(prefix=first['status'],final=final['status'],actualFinalLoss=cents(final['loss']),alternatives=e)
 add('BATCH-PREFIX-VS-STICKY','D05',netting,dict(prefix='OVER_CAP',final='CONFIRMED',actualFinalLoss=0,alternatives=dict(SignedBatchLoss=0,PrefixLosses=[1500,0],StickyBreach=True,PeakLoss=1500)))
 def far():r=m.far_loss('-50',dict(basis='POS1',fresh=True,absolute=40),'POS1');return [int(r['absolute']),int(r['incremental']),30>=r['absolute'],30>=r['incremental']]
 add('ABSOLUTE-VS-INCREMENTAL','D04',far,[50,10,False,True])
 def levels(variant):
  rows=[]
  for i,av,loss,transition in [(1,100,20,50),(2,20,25,1)]:rows.append(dict(id=i,available=av,loss=loss,buffer=1,transitionLoss=transition,currency='USD',digits=2,sourceFresh=True,snapshotFresh=True,complete=True,share='0.5',bnet=100,far=10))
  status,level,margin=m.assess_levels(rows,[1,2],variant);return [status,level,int(margin)]
 def exact_cancellation():
  rows=[dict(id=i,available='1e28',loss='0.010',buffer='9999999999999999999999999999.995',transitionLoss=i,currency='USD',digits=3,sourceFresh=True,snapshotFresh=True,complete=True,share='0.5',bnet=100,far=10) for i in (1,2)]
  status,level,margin=m.assess_levels(rows,[1,2]);return [status,level,cents(margin,3)]
 add('CR09-EXACT-CANCELLATION','NUM-EXACT-1/CR09',exact_cancellation,['REJECT',1,-5])
 add('CR09-ALL','CR09' ,lambda:levels('A'),['REJECT',2,-6]);add('CR09-SINGLE','CR09',lambda:levels('B'),['SINGLE_LEVEL_POSITIVE',1,79])
 def geometry():r=m.exact.geometry('.1','.01','3','.1','.01','100','.01');return [r['status'],int(r['Core']),r['slope']>0]
 add('ZERO-CORE','ZERO-CORE',geometry,['REJECT',0,True])
 for name,vals,exp in [('min',('.01','.01','1','.01','0'),True),('off-origin',('.03','.03','1','.02','0'),False),('min-origin',('.03','.03','1','.02','.03'),True),('too-large',('1.01','.01','1','.01','0'),False)]:add('LOT-'+name,'ZERO-CORE',lambda vals=vals:oracle.volume_valid(*vals),exp,scope='INDEPENDENT_MATHEMATICAL_CRITERION_NOT_BROKER_EVIDENCE')
 for operation,x,y,expected in [('add',2**63-1,0,2**63-1),('add',2**63-1,1,'UNAVAILABLE'),('mul',-(2**63),-1,'UNAVAILABLE'),('mul',-(2**63),1,-(2**63))]:
  def check(op=operation,x=x,y=y):
   try:return m.checked_add(x,y) if op=='add' else m.checked_mul(x,y)
   except m.Unsupported:return 'UNAVAILABLE'
  add('INT64-'+operation+'-'+str(x)+'-'+str(y),'MQL-DOMAIN',check,expected,scope='PYTHON_INT64_BOUNDARY_SIMULATION_NOT_MQL5_RUNTIME')
 def cost_fact(edit):
  q,s,au=a.fixture(m);edit(q,au);return m.cost_coverage(q['costClaims'],au['costSets']['COST1'])['status']
 add('COST-UNKNOWN','D06',lambda:cost_fact(lambda q,au:au['costSets']['COST1']['items'][0].__setitem__('OverlapKnown',False)),'UNAVAILABLE')
 def overlap(q,au):
  fact=copy.deepcopy(au['costSets']['COST1']['items'][0]);fact['CostID']='OTHER';au['costSets']['COST1']['items'].append(fact);claim=copy.deepcopy(q['costClaims'][0]);claim['CostID']='OTHER';q['costClaims'].append(claim)
 add('COST-OVERLAP','D06',lambda:cost_fact(overlap),'CONFLICT')
 def snap_content():
  q,s,j,au=a.c2.wire.fixture();before=copy.deepcopy((q,s,j,au));receipt=au['snapshotReceipts'][1];au['snapshot']['marketFingerprint']='CHANGED';r=m.exact.authorize(q,s,j,au);return [r,au['snapshotReceipts'][1]==receipt,a.same((s,j),(before[1],before[2]))]
 add('R0D-SNAPSHOT-CONTENT','SNAP-FIXTURE-1',snap_content,['CONFLICT',True,True],scope='FROZEN_R0D_REFERENCE_NOT_C2_COMPOSED_SNAPSHOT_INTEGRATION')
 def c2_snapshot_scope():
  r=invoke('apply_for_test',edit=lambda q,s,au:(q['identity'].__setitem__('Snapshot',999),au['context'].__setitem__('Snapshot',999)));return [r['Status'],r['After']['Free']]
 add('C2-SNAPSHOT-SCOPE','D08/SNAP-FIXTURE-1',c2_snapshot_scope,['COMMITTED_IN_MEMORY',4000],scope='LIMITED_C2_ID_BINDING_FIXTURE_NOT_CONTENT_OR_BROKER_PROOF')
 def duplicate_fills():
  q,s,au=a.fixture(m);b=au['batches']['T1'];refs=b['refs']+b['refs'];r=m.assess_batch(refs,au['fillHistory'],b['expected']);return [r['status'],cents(r['volume'])]
 add('EXACT-FILL-DUPLICATE','D05',duplicate_fills,['CONFIRMED',100])
 def changed_fill():
  q,s,au=a.fixture(m);b=au['batches']['T1'];first=m.assess_batch(b['refs'],au['fillHistory'],b['expected']);au['fillHistory'][a.wire.encode(b['refs'][0])]['net']=-20;second=m.assess_batch(b['refs'],au['fillHistory'],b['expected']);return [first['status'],second['status']]
 add('CHANGED-FILL-HISTORY-SCOPE','D05/D08',changed_fill,['CONFIRMED','OVER_CAP'],scope='CURRENT_BATCH_ASSESSMENT_NOT_CROSS_OBSERVATION_IMMUTABILITY')
 def incomplete_history():
  r=invoke('available',edit=lambda q,s,au:au.__setitem__('complete',False));return [r['Status'],r['Details'].get('FreeCents')]
 add('HISTORY-NOT-ZERO','D02',incomplete_history,['UNAVAILABLE',None])
 def canonical_types():return [m.canonical('1')!=m.canonical(1),m.canonical(1)!=m.canonical(True),m.canonical({'x':None})!=m.canonical({})]
 add('TYPED-CANONICAL','NUM-CODEC',canonical_types,[True,True,True])
 def rounding():return m.exact.posted('1.005','USD',2,None)[0]
 add('UNKNOWN-ROUNDING','NUM-DOMAIN-1',rounding,'UNAVAILABLE')
 for raw in ('{"x":1,"x":2}','{"a":[{"Result":"FAIL","Result":"PASS"}]}','{"ExitCode":false}','{"x":NaN}','{"x":Infinity}'):
  def strict(raw=raw):
   try:m.evidence.loads(raw);return 'ACCEPT'
   except ValueError:return 'REJECT'
  add('JSON-'+str(len(cases)),'NUM-CODEC',strict,'REJECT')
 return cases,reserve_path

def survivor_audit():
 source=Path(m.__file__).read_text();rows=[]
 specs=[r for r in a.mutants.catalog() if r.get('RedundancyProof')]
 for spec in specs:
  edited=source
  for old,new in spec['Edits']:assert edited.count(old)==1;edited=edited.replace(old,new)
  mutant=types.ModuleType('C3survivor');mutant.__file__='C3survivor';exec(compile(edited,'C3survivor','exec'),mutant.__dict__)
  label=spec['MutationID'];pairs=[]
  if 'cost-shape-caller' in label:
   edit=lambda q,s,au:au['costSets']['COST1']['items'][0].__setitem__('OverlapKnown',1);pubs=['cost_coverage','authorize','apply_for_test'];committed=False
  elif 'malformed-default-identity' in label:edit=lambda q,s,au:q.__setitem__('identity',None);pubs=['verify_allocation_identity','authorize','apply_for_test'];committed=False
  elif 'journal-self-repair' in label:edit=lambda q,s,au:au['coreJournal'].__setitem__(next(iter(au['coreJournal'])),'BAD');pubs=['authorize','apply_for_test','available','recover_store'];committed=False
  elif 'malformed-source-ignore' in label:edit=lambda q,s,au:s['ledger']['sources'].__setitem__(next(iter(s['ledger']['sources'])),True);pubs=['authorize','apply_for_test','available','recover_store'];committed=False
  elif 'digest-format' in label:
   def edit(q,s,au):
    k=next(iter(s['receipts']));s['receipts'][k]['batchDigest']='z'*64;au['receipts'][k]['batchDigest']='z'*64
   pubs=['authorize','apply_for_test','available','recover_store'];committed=True
  else:
   def edit(q,s,au):next(iter(s['ledger']['allocations'].values()))['buckets']['FinalReserve']['RemainingFree']=500
   pubs=['apply_for_test'];committed=False
  for pub in pubs:
   op=invoke(pub,m);mp=invoke(pub,mutant);on=invoke(pub,m,edit,committed);mn=invoke(pub,mutant,edit,committed)
   expected='CONFLICT' if pub in ('cost_coverage','available','recover_store') else 'REJECT'
   if 'outer-poststate' in label:expected='UNAVAILABLE'
   pairs.append(dict(PublicCaller=pub,PositiveOriginal=op,PositiveMutant=mp,OriginalOutcome=on,MutantOutcome=mn,IndependentExpected=expected,StatusEquivalent=on['Status']==mn['Status'],OriginalMatchesExpected=on['Status']==expected,StateDeltaZero=on['ZeroDelta'] and mn['ZeroDelta'] and on['InputsUnchanged'] and mn['InputsUnchanged']))
  non_equiv=any(not p['StatusEquivalent'] for p in pairs)
  rows.append(dict(MutationID=label,SourceFunction=spec['TargetFunction'],ExactSourceChange=[dict(old=x,new=y) for x,y in spec['Edits']],OriginalSourceHash=a.sha(Path(m.__file__)),MutantSourceHash=hashlib.sha256(edited.encode()).hexdigest(),AffectedGuard=spec['NegativeTestID'],MandatoryCaller=pubs,CallerProof=spec['RedundancyProof'],IndependentCallerAudit=pairs,Classification='NOT_GLOBALLY_REDUNDANT_STATUS_GAP' if non_equiv else 'REDUNDANT_IN_DECLARED_PUBLIC_DOMAIN',ProofBoundary='Finite public-path probes + structural caller proof, not universal mutation completeness'))
 return rows

def main():
 started=a.now();cases,reserve=test_cases();rows=[]
 for c in cases:
  row={k:v for k,v in c.items() if k!='Run'}
  try:
   trace_start=len(CAPTURED_TRACES);actual,calls,lines=a.trace(c['Run']);row.update(ExecutionTraces=CAPTURED_TRACES[trace_start:],DirectCalls=calls,DirectLines=lines,Actual=a.view(actual),Expected=a.view(c['Expected']),Result='PASS' if a.view(actual)==a.view(c['Expected']) else 'FAIL')
  except Exception as e:row.update(Result='INFRASTRUCTURE_ERROR',ErrorType=type(e).__name__,Error=str(e))
  rows.append(row)
 audit=survivor_audit();a.save('SURVIVORS',dict(a.metadata(__file__),StartedUtc=started,FinishedUtc=a.now(),Command=[sys.executable,*sys.argv],Rows=audit,StatusGaps=sum(r['Classification']=='NOT_GLOBALLY_REDUNDANT_STATUS_GAP' for r in audit),ExitCode=0))
 out=dict(a.metadata(__file__),IndependentOracleHash=a.sha(Path(oracle.__file__)),Command=[sys.executable,*sys.argv],StartedUtc=started,FinishedUtc=a.now(),Scenarios=len(rows),Pass=sum(r['Result']=='PASS' for r in rows),Fail=sum(r['Result']=='FAIL' for r in rows),InfrastructureErrors=sum(r['Result']=='INFRASTRUCTURE_ERROR' for r in rows),Rows=rows,ReservationTrace=reserve()['trace']);out['ExitCode']=int(out['Fail']+out['InfrastructureErrors']>0);a.save('INDEPENDENT_TESTS',out);print({k:out[k] for k in ('Scenarios','Pass','Fail','InfrastructureErrors','ExitCode')});print([r for r in rows if r['Result']!='PASS']);return out['ExitCode']
if __name__=='__main__':raise SystemExit(main())
