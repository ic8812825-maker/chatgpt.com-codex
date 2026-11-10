#!/usr/bin/env python3
"""R0F literals/struct oracle, candidate profiles only. Historical evaluators are subjects, not expected."""
import copy,hashlib,json,sys,types,struct
from pathlib import Path
import check_hsbi_02b_r0f_common as a
import hsbi_02b_r0f_contract_candidate as m
import hsbi_02b_r0f_independent_fixtures as f

def shape_status(record):
 try:m.record_shape(record);return 'VALID'
 except m.Invalid:return 'REJECT'
 except m.Unavailable:return 'UNAVAILABLE'
def allocation():return dict(Source=('B1','S1',1,11),Event=1,Policy=1,Currency='USD',Precision=2,Phase='COMMITTED',EligibleNet=5000,Unallocated=0,Grants=dict(FinalReserve=5000,PartialFar=0,Transition=0,Carry=0,Residual=0))
def balance_vector(s):return [s[k] for k in ('OriginalGrant','Consumed','Reserved','Free','Revision')]
def operation_trace():
 s=m.state();events=[]
 for event,kind,amount,owner,revision in [(1,'RESERVE',1500,'O1',1),(2,'CONSUME_RESERVED',100,'O2',2),(3,'CONSUME_FREE',1000,'O1',2),(4,'RELEASE',500,'O1',3),(5,'CONSUME_RESERVED',1000,'O1',4)]:
  before=copy.deepcopy(s);status,out=m.operate(s,event,kind,amount,owner,revision);events.append(dict(Before=before,After=out,Status=status,InputUnchanged=s==before));s=out
 return events

def cases():
 out=[]
 def add(i,req,fn,expected):out.append(dict(TestID='R0F-'+i,RequirementID=req,Run=fn,Expected=expected))
 add('BALANCE-TRACE','R0F-01',lambda:[(r['Status'],balance_vector(r['After']),r['InputUnchanged']) for r in operation_trace()],[('COMMITTED_IN_MEMORY',[5000,0,1500,3500,2],True),('REJECT',[5000,0,1500,3500,2],True),('COMMITTED_IN_MEMORY',[5000,1000,1500,2500,3],True),('COMMITTED_IN_MEMORY',[5000,1000,1000,3000,4],True),('COMMITTED_IN_MEMORY',[5000,2000,0,3000,5],True)])
 for i,args,expected in [('known',(5000,1000,4000,1500,'USD',2,True),('MAPPED_FIXTURE_ONLY',dict(OriginalGrant=5000,Consumed=1000,Reserved=1500,Free=2500,RemainingGross=4000))),('currency',(5000,1000,4000,1500,None,2,True),('UNAVAILABLE',None)),('precision',(5000,1000,4000,1500,'USD',None,True),('UNAVAILABLE',None)),('owner',(5000,1000,4000,1500,'USD',2,False),('UNAVAILABLE',None)),('double-count',(5000,1000,4000,5000,'USD',2,True),('CONFLICT',None))]:add('MIGRATE-'+i,'R0F-01',lambda args=args:m.migration(*args),expected)
 def replay(changed=False):
  _,s=m.operate(m.state(),1,'CONSUME_FREE',1000,revision=1);before=copy.deepcopy(s);status,o=m.operate(s,1,'CONSUME_FREE',1100 if changed else 1000,revision=1);return status,o==before,s==before
 add('EXACT-REPLAY','R0F-01/R0F-09',replay,('NO_OP',True,True));add('ALTERED-REPLAY','R0F-01/R0F-09',lambda:replay(True),('CONFLICT',True,True))
 for tag,edit,status in [('history',lambda s:s.__setitem__('HistoryComplete',False),'UNAVAILABLE'),('prepared',lambda s:s.__setitem__('Phase','PREPARED'),'REJECT'),('currency',lambda s:s.__setitem__('Currency',None),'UNAVAILABLE'),('unknown-revision',lambda s:s.__setitem__('Revision',0),'REJECT')]:
  def negative(edit=edit):
   s=m.state();edit(s);before=copy.deepcopy(s);st,o=m.operate(s,2,'CONSUME_FREE',100);return st,s==before,o==before
  add('STATE-'+tag,'R0F-01',negative,(status,True,True))
 for tag,amount,event in [('negative',-1,2),('zero',0,2),('excess',5001,2),('bool',True,2),('event-bool',1,True)]:
  def deny(n=amount,e=event):
   s=m.state();before=copy.deepcopy(s);st,o=m.operate(s,e,'CONSUME_FREE',n);return st,s==before,o==before
  add('CONSUME-'+tag,'R0F-01',deny,('REJECT',True,True))
 add('PROJECTED-NOT-ACTUAL','R0F-02',lambda:m.confirm_source(f.record(),None),('UNAVAILABLE',None))
 add('RECONCILED-CONTROL','R0F-02',lambda:m.confirm_source(f.record(),f.authority()),('RECONCILED_FIXTURE_ONLY',5000))
 for tag,edit in [('components',lambda r:r.update(Profit=70.0,Commission=-17.0)),('net',lambda r:r.__setitem__('DealNet',999.0)),('account',lambda r:r.__setitem__('AccountLogin',2))]:
  def foreign(edit=edit):r=f.record();authority=f.authority();edit(r);return m.confirm_source(r,authority)
  add('RECONCILE-'+tag,'R0F-02/R0F-09',foreign,('CONFLICT',None))
 def unverified():r=f.record();au=f.authority();au['PolicyVerified']=False;return m.confirm_source(r,au)
 add('UNVERIFIED-PRECISION','R0F-06',unverified,('UNAVAILABLE',None))
 def posted_mismatch():au=f.authority();au['PostedNet']=5100;return m.confirm_source(f.record(),au)
 add('POSTED-COMPONENTS-MISMATCH','R0F-02',posted_mismatch,('CONFLICT',None))
 add('SMALL-ONLY','R0F-03',lambda:m.eligible('Small',1000,True),('ALLOCATABLE_FIXTURE_ONLY',dict(BigReserve=0,SmallResidualHeld=1000)))
 add('OPENING-NO-GRANT','R0F-03',lambda:m.eligible('BigCore',1000,True,False),('NOT_HARVEST_SOURCE',dict(BigReserve=0,SmallResidualHeld=0)))
 add('NEGATIVE-SOURCE','R0F-02',lambda:m.eligible('BigCore',-500,True),('ALLOCATABLE_FIXTURE_ONLY',dict(BigReserve=0,SmallResidualHeld=0)))
 add('ABSOLUTE-FAR','R0F-04',lambda:dict(absolute=max(0,-(-5000)),incremental=max(0,5000-4000),absoluteCovered=3000>=5000,incrementCovered=3000>=1000),dict(absolute=5000,incremental=1000,absoluteCovered=False,incrementCovered=True))
 add('MARGIN-ZERO-REJECT','R0F-04',lambda:(5000-4900-100)>0,False)
 add('ALL-LEVEL-MARGIN','R0F-04',lambda:min(10000-2000-100,2000-2500-100),-600)
 for policy,gates in [('A',[False,True]),('B',[False,False]),('C',[False,False])]:
  add('TRANSITION-'+policy,'R0F-05',lambda policy=policy:m.transition([-1500,10000],1200,policy),dict(status='ASSESSED_FIXTURE_ONLY',policy=policy,trace=[dict(Net=-1500,CurrentLoss=1500,PeakLoss=1500,StickyBreach=True,CapGate=gates[0]),dict(Net=8500,CurrentLoss=0,PeakLoss=1500,StickyBreach=True,CapGate=gates[1])]))
 add('TRANSITION-CAP-EQUALITY','R0F-05',lambda:[m.transition([-1200],1200,p)['trace'][0]['CapGate'] for p in ('A','B','C')],[True,True,True])
 add('TRANSITION-NO-DEFAULT','R0F-05',lambda:m.transition([-1500,10000],1200,None),dict(status='UNAVAILABLE',policy=None,trace=[]))
 for tag,x,text,hexvalue in f.GOLDENS:
  add('CODEC-A-'+tag,'R0F-06',lambda x=x:m.text17(x),text)
  add('CODEC-B-'+tag,'R0F-06',lambda x=x:f'{m.raw64_bits(x):016x}',hexvalue)
  add('INDEPENDENT-IEEE-'+tag,'R0F-06',lambda x=x:struct.pack('>d',0.0 if x==0 else x).hex(),hexvalue)
 add('CODEC-RECORD-GOLDEN','R0F-06',lambda:m.encode_record(f.record(),'B').hex(),f.binary_record(f.record()).hex())
 add('CODEC-A-GOLDEN','R0F-06',lambda:m.encode_record(f.record(),'A').hex(),f.text_record(f.record()).hex())
 add('CODEC-A-ROUNDTRIP','R0F-06',lambda:f.decoded_text(m.encode_record(f.record(),'A')),f.record())
 add('CODEC-B-ROUNDTRIP','R0F-06',lambda:f.decoded_binary(m.encode_record(f.record(),'B')),f.record())
 def profiles_equivalent():
  r=f.record();return m.encode_record(r,'A')!=m.encode_record(r,'B') and f.decoded_binary(m.encode_record(r,'B'))==r
 def delimiter_collision(profile):
  r=f.record();r.update(Broker='B|S',Server='X');q=f.record();q.update(Broker='B',Server='S|X');return m.encode_record(r,profile)!=m.encode_record(q,profile)
 for profile in ('A','B'):add('CODEC-DELIMITER-'+profile,'R0F-06',lambda p=profile:delimiter_collision(p),True)
 add('CODEC-PROFILES-DISTINCT','R0F-06',profiles_equivalent,True)
 for field in f.ORDER:
  if field in ('Broker','Server','AccountLogin','DealTicket'):continue
  def mutate(field=field):
   r0=f.record();r=copy.deepcopy(r0);v=r[field]
   if field=='SchemaVersion':r[field]=2
   elif type(v) is bool:
    r[field]=False;r['SourcePlan' if field=='SourcePlanApplicable' else 'SourcePolicyVersion']=None
   elif field=='Role':r[field]='BigTrend'
   elif field=='EntryType':r[field]='OUT_BY'
   elif field=='DealType':r[field]='BUY'
   elif type(v) in (int,float):r[field]=v+1
   else:r[field]=v+'X'
   return m.duplicate(r0,r)
  add('IDENTITY-'+field,'R0F-07',mutate,'UNAVAILABLE' if field=='SchemaVersion' else 'CONFLICT')
 for field,val in [('Broker','B2'),('Server','S2'),('AccountLogin',2),('DealTicket',12)]:
  def namespace(field=field,val=val):r=f.record();r[field]=val;return m.duplicate(f.record(),r)
  add('NAMESPACE-'+field,'R0F-07',namespace,'NEW_IDENTITY_ONLY')
 add('RAW-SIGNED-SUM','R0F-02',lambda:m.raw_signed_sum(f.record()),(50,1))
 def raw_binary_sum():r=f.record();r.update(Profit=.1,Swap=.2,Commission=0.0,Fee=0.0,DealNet=.3);return m.raw_signed_sum(r)
 add('RAW-NOT-POSTED','R0F-02/R0F-06',raw_binary_sum,(10808639105689191,36028797018963968))
 add('ECONOMIC-EXACT','R0F-07',lambda:m.duplicate(f.record(),f.record()),'NO_OP')
 def equal_net_components():r=f.record();r.update(Profit=70.0,Commission=-17.0);return m.duplicate(f.record(),r)
 add('ECONOMIC-SAME-NET-ALTERED-COMPONENTS','R0F-07',equal_net_components,'CONFLICT')
 for field,value,expected in [('AccountLogin',True,'REJECT'),('Magic',False,'REJECT'),('Precision',None,'UNAVAILABLE'),('Currency',None,'UNAVAILABLE'),('SourcePlan',None,'UNAVAILABLE'),('Profit',float('nan'),'REJECT'),('TimestampMsc',2**63,'REJECT')]:
  def malformed(field=field,value=value):r=f.record();r[field]=value;return shape_status(r)
  add('SCHEMA-'+field,'R0F-07',malformed,expected)
 def swapped():r=allocation();r['Grants'].update(FinalReserve=0,PartialFar=5000);return m.allocation_duplicate(allocation(),r)
 add('BUCKET-PERMUTATION','R0F-08',swapped,'CONFLICT');add('ALLOCATION-EXACT','R0F-08',lambda:m.allocation_duplicate(allocation(),allocation()),'NO_OP')
 def malformed_allocation():r=allocation();r['Source']=();return m.allocation_duplicate(allocation(),r)
 add('ALLOCATION-MALFORMED-SOURCE','R0F-08',malformed_allocation,'REJECT')
 def partial():r=allocation();r.update(Phase='PREPARED',Unallocated=1000);r['Grants']['FinalReserve']=4000;return m.allocation_duplicate(r,copy.deepcopy(r))
 add('PREPARED-CONSERVATION','R0F-08',partial,'NO_OP')
 for tag,flag,expected in [('malformed',1,'CONFLICT'),('unknown',False,'UNAVAILABLE'),('known',True,'COVERED_FIXTURE_ONLY')]:add('COST-'+tag,'R0F-10',lambda flag=flag:m.cost_status(dict(OverlapKnown=flag,Applicable=True,AlreadyIncluded=False,AdditionalDeduction=True)),expected)
 def large_chain():
  s=m.state((2**63)-1);_,s=m.operate(s,1,'CONSUME_FREE',1,revision=1);_,s=m.operate(s,2,'CONSUME_FREE',1,revision=2);return s['Free'],s['Consumed'],s['OriginalGrant']==s['Free']+s['Consumed']+s['Reserved']
 add('INT64-SMALL-DEBITS','R0F-06',large_chain,(2**63-3,2,True))
 for name,n in [('max-plus-one',2**63),('min-minus-one',-2**63-1)]:
  def overflow(n=n):
   try:m.checked(n);return 'ACCEPT'
   except m.Unavailable:return 'UNAVAILABLE'
  add('OVERFLOW-'+name,'R0F-06',overflow,'UNAVAILABLE')
 return out

def gap():
 import check_hsbi_02b_r0e_c2_contracts as c2
 old=c2.subject;src=Path(old.__file__).read_text();needle='if expected is not None:dto.validate("CostSet",expected)';assert src.count(needle)==1;mutated=src.replace(needle,'pass');mut=types.ModuleType('R0F_gap_mutant');mut.__file__='R0F_gap_mutant';exec(compile(mutated,'R0F_gap_mutant','exec'),mut.__dict__)
 rows=[]
 for model in (old,mut):
  q,s,au=c2.fixture(model);positive=model.cost_coverage(q['costClaims'],au['costSets']['COST1'])['status'];au['costSets']['COST1']['items'][0]['OverlapKnown']=1;before=copy.deepcopy((q,s,au));pure=model.cost_coverage(q['costClaims'],au['costSets']['COST1'])['status'];authorize=model.authorize(q,s,au)['status'];r,o=model.apply_for_test(q,s,au);rows.append(dict(PositiveControl=positive,Cost=pure,Authorize=authorize,Apply=r['status'],ZeroDelta=c2.same(o,s),InputsUnchanged=c2.same((q,s,au),before)))
 return dict(Rows=rows,OriginalSourceHash=a.sha(Path(old.__file__)),MutantSourceHash=hashlib.sha256(mutated.encode()).hexdigest(),ExactEdit=dict(old=needle,new='pass'),SourceFile=str(Path(old.__file__).relative_to(a.ROOT)),Classification='STATUS_CONTRACT_GAP_NOT_GLOBAL_REDUNDANCY',ProductionRemediated=False)

def main():
 started=a.now();rows=[]
 for c in cases():
  row={k:v for k,v in c.items() if k!='Run'}
  try:actual=c['Run']();row.update(Actual=actual,Result='PASS' if actual==c['Expected'] else 'FAIL')
  except Exception as e:row.update(Result='INFRASTRUCTURE_ERROR',ErrorType=type(e).__name__,Error=str(e))
  rows.append(row)
 g=gap();expected=[dict(PositiveControl='COVERED',Cost='CONFLICT',Authorize='REJECT',Apply='REJECT',ZeroDelta=True,InputsUnchanged=True),dict(PositiveControl='COVERED',Cost='UNAVAILABLE',Authorize='REJECT',Apply='REJECT',ZeroDelta=True,InputsUnchanged=True)];g['IndependentExpected']=expected;g['Result']='PASS' if g['Rows']==expected else 'FAIL';a.save('STATUS_GAP',g)
 result=dict(a.meta(__file__),Command=[sys.executable,*sys.argv],StartedUtc=started,FinishedUtc=a.now(),FixtureSourceHash=a.sha(Path(f.__file__)),CandidateSourceHash=a.sha(Path(m.__file__)),Scenarios=len(rows),Pass=sum(r['Result']=='PASS' for r in rows),Fail=sum(r['Result']=='FAIL' for r in rows),InfrastructureErrors=sum(r['Result']=='INFRASTRUCTURE_ERROR' for r in rows),Rows=rows,OperationTrace=operation_trace(),StatusGapResult=g['Result']);result['ExitCode']=int(result['Fail']+result['InfrastructureErrors']>0 or g['Result']!='PASS');a.save('TEST_RESULTS',result)
 a.save('CODEC_GOLDENS',dict(Profiles=['HSBI-T17Z-1','HSBI-F64Z-1'],Vectors=[dict(ID=tag,RawInput=float.hex(x),Text17Expected=t,BitsExpected=h) for tag,x,t,h in f.GOLDENS],RecordFields=list(f.ORDER),RecordBinaryHex=f.binary_record(f.record()).hex(),RecordTextHex=f.text_record(f.record()).hex(),RecordBinarySHA256=hashlib.sha256(f.binary_record(f.record())).hexdigest(),ExpectedSource='Literal IEEE754 vectors + independent struct packing; not subject encoder',MQL5Compile='NOT_RUN'))
 print({k:result[k] for k in ('Scenarios','Pass','Fail','InfrastructureErrors','ExitCode')});print([r for r in rows if r['Result']!='PASS']);return result['ExitCode']
if __name__=='__main__':raise SystemExit(main())
