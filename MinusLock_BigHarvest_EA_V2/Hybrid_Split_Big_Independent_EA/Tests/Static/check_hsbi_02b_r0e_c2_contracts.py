#!/usr/bin/env python3
"""C2 tests: literal expectations; frozen independent C1 fixture encoder, NOT evaluator expected."""
import argparse,copy,hashlib,json,sys,subprocess
from pathlib import Path
from decimal import Decimal,localcontext
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parents[1];BASE='fae7dfc18ca2d61af2f3446826ef3031825bbfd8'
sys.path.insert(0,str(ROOT/'Tests/Reference'))
import hsbi_02b_r0e_c2_contract_model as subject
import hsbi_02b_r0e_c2_schemas as schema
import check_hsbi_02b_r0e_c1_contracts as frozen
CATALOG_VERSION='HSBI-C2-REQUIRED-1'
wire=frozen.wire;view=wire.view;fixture=frozen.fixture;advance_authority=frozen.advance_authority;checksum=frozen.checksum
TARGET='Tests/Reference/hsbi_02b_r0e_c2_contract_model.py';SCHEMA='Tests/Reference/hsbi_02b_r0e_c2_schemas.py'
def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def hashes():return {str(p.relative_to(ROOT)):sha(p) for p in (Path(__file__).resolve(),Path(subject.__file__),Path(schema.__file__),Path(subject.exact.__file__),Path(subject.evidence.__file__),Path(frozen.__file__),Path(wire.__file__))}
def metadata():return dict(BaseSHA=BASE,TestedSHA=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),UTC=now(),ApprovalStatus='AWAITING_ADMIN_APPROVAL')
def save(path,data):
 p=Path(path).resolve();assert p.is_relative_to(ROOT) and 'C2' in p.name;p.write_text(json.dumps(view(data),ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def equal(a,b):return same(a,b)
def same(a,b):return view(a,True)==view(b,True)
def apply_edit(m,edit=None):
 q,s,a=fixture(m)
 if edit:edit(q,s,a)
 before=copy.deepcopy((q,s,a));r,o=m.apply_for_test(q,s,a)
 return dict(status=r['status'],zeroDelta=same(o,s),inputsUnchanged=same((q,s,a),before),state=frozen.state_summary(o))
def expected(status='REJECT'):return frozen.expected_apply(status)
def bool_policy(q,s,a):a['costSets']['COST1']['items'][0]['PolicyVersion']=True;q['costClaims'][0]['PolicyVersion']=True

def receipt_case(m,field,value):
 q,s,a=fixture(m);_,s=m.apply_for_test(q,s,a);a=advance_authority(a,q);ek=wire.encode(q['source'][:3]+(q['consumptionEvent'],));s['receipts'][ek][field]=value;a['receipts']=copy.deepcopy(s['receipts']);before=copy.deepcopy((s,a));r=m.recover_store(m.snapshot_store(s),None,a)
 return dict(status=r['status'],inputsUnchanged=same((s,a),before))
def allocation_edit(field):
 def edit(q,s,a):
  a['allocations']['A1'][field]=999
  if field=='allocationEvent':q['allocationEvent']=999;q['identity']['AllocationEventID']=999
  else:q['identity']['PolicyVersion']=999
 return edit

def chain(m):
 q,s,a=fixture(m,principal='20',risk='0');original=copy.deepcopy(s);r,s=m.apply_for_test(q,s,a);a=advance_authority(a,q)
 statuses=[r['status']];states=[frozen.state_summary(s)]
 q2=copy.deepcopy(q);q2.update(consumptionEvent=3,revision=3,PrincipalAmount=Decimal(30));q2['identity'].update(ConsumptionEventID=3,Revision=3);a['context'].update(ConsumptionEventID=3,Revision=3,PrincipalAmount=Decimal(30));r,s=m.apply_for_test(q2,s,a);statuses.append(r['status']);states.append(frozen.state_summary(s));a=advance_authority(a,q2)
 r,o=m.apply_for_test(q2,s,a);statuses.append(r['status']);no_delta=same(o,s)
 q3=copy.deepcopy(q2);q3.update(consumptionEvent=4,revision=4,PrincipalAmount=Decimal(1));q3['identity'].update(ConsumptionEventID=4,Revision=4);a['context'].update(ConsumptionEventID=4,Revision=4,PrincipalAmount=Decimal(1));r,o=m.apply_for_test(q3,s,a);statuses.append(r['status']);no_delta&=same(o,s)
 return dict(statuses=statuses,free=[st['free'] for st in states],consumed=[st['consumed'] for st in states],zeroDeltaAfterFull=no_delta,initialFree=frozen.state_summary(original)['free'])
def recovery_scope(m):
 q,s,a=fixture(m,principal='50',risk='0');_,s=m.apply_for_test(q,s,a);a=advance_authority(a,q)
 q2,_,a2=fixture(m,principal='50',risk='0.5');ek=wire.encode(q['source'][:3]+(q['consumptionEvent'],));s['receipts'][ek].update(request=q2,digest=checksum(q2),AdditionalRisk=Decimal('.5'),RequiredBalance=Decimal('50.5'),costDigest=checksum(a2['costSets']['COST1']));a['receipts']=copy.deepcopy(s['receipts']);a['costSets']=a2['costSets'];before=copy.deepcopy((s,a))
 return dict(recovery=m.recover_store(m.snapshot_store(s),None,a)['status'],newAuthorization=m.authorize(q2,fixture(m,principal='50',risk='.5')[1],a2)['status'],inputsUnchanged=same((s,a),before))

def cases():
 out=[]
 # Frozen literal scenarios retained; test fixtures/encoder are not expected evaluators.
 for c in frozen.cases():
  row=dict(c);row['TestID']='C2-BASE-'+c['TestID']
  if c['TestID']=='APPLY-token-not-authority':row['IndependentExpected']=dict(status='REJECT',zeroDelta=True) # missing required authority fields: explicit C2 schema priority
  out.append(row)
 def add(i,op,fn,exp,guard=None):out.append(dict(TestID='C2-'+i,GuardID=guard or i,Operation=op,run=fn,IndependentExpected=exp,Classes=['C2'],Input=dict(Change=i)))
 add('bool-policy','apply_for_test',lambda m:apply_edit(m,bool_policy),expected())
 for tag,v in [('null',None),('empty',{}),('bool',True)]:add('batch-'+tag,'apply_for_test',lambda m,v=v:apply_edit(m,lambda q,s,a:a['batches']['T1'].__setitem__('expected',v)),expected('UNAVAILABLE' if v is None else 'REJECT'))
 add('history-empty','apply_for_test',lambda m:apply_edit(m,lambda q,s,a:a['history'].__setitem__(wire.encode(('B1','S1',1,99)),{})),expected())
 add('snapshot-payload','recover_store',lambda m:m.recover_store(dict(schema='HSBI-C1-STORE-SNAPSHOT-1',checksum='0'*64),None,fixture(m)[2])['status'],'CONFLICT')
 add('receipt-digest','recover_store',lambda m:receipt_case(m,'digest','0'*64),dict(status='CONFLICT',inputsUnchanged=True))
 add('receipt-equation','recover_store',lambda m:receipt_case(m,'RequiredBalance',Decimal(999)),dict(status='CONFLICT',inputsUnchanged=True))
 for field in ('purpose','intent'):
  add('planned-'+field,'apply_for_test',lambda m,f=field:apply_edit(m,lambda q,s,a:q.__setitem__(f,'FinalClose' if f=='purpose' else 'FOREIGN_INTENT')),expected())
 for f in ('allocationEvent','PolicyVersion'):add('ledger-'+f,'apply_for_test',lambda m,f=f:apply_edit(m,allocation_edit(f)),expected())
 def receipt_clause(m,kind):
  q,s,a=fixture(m);_,s=m.apply_for_test(q,s,a);a=advance_authority(a,q);ek=wire.encode(q['source'][:3]+(q['consumptionEvent'],));r=s['receipts'][ek]
  if kind=='nonnegative':r.update(AdditionalRisk=Decimal('-.5'),RequiredBalance=Decimal('9.5'))
  else:
   principal=Decimal(11 if kind=='principal' else 9);r['request']['PrincipalAmount']=principal;r['evaluationContext']['PrincipalAmount']=principal;r['digest']=checksum(r['request'])
   if kind=='core':r.update(DebitAmount=Decimal(9),RequiredBalance=Decimal('9.5'))
  a['receipts']=copy.deepcopy(s['receipts']);before=copy.deepcopy((s,a));result=m.recover_store(m.snapshot_store(s),None,a)
  return dict(status=result['status'],inputsUnchanged=same((s,a),before))
 for c in ('nonnegative','principal','core'):add('receipt-clause-'+c,'recover_store',lambda m,c=c:receipt_clause(m,c),dict(status='CONFLICT',inputsUnchanged=True))
 add('chain','apply_for_test',chain,dict(statuses=['COMMITTED_IN_MEMORY','COMMITTED_IN_MEMORY','NO_OP','REJECT'],free=[wire.N('30'),wire.N('0')],consumed=[wire.N('20'),wire.N('50')],zeroDeltaAfterFull=True,initialFree=wire.N('50')))
 add('recovery-scope','recover_store',recovery_scope,dict(recovery='RECONCILED_MODEL_ONLY',newAuthorization='REJECT',inputsUnchanged=True))

 def json_case(m,raw):
  try:m.evidence.loads(raw);return 'VALID'
  except ValueError:return 'REJECT'
 add('JSON-control','loads',lambda m:json_case(m,'{"ExitCode":0,"Result":"PASS"}'),'VALID')
 for tag,raw in [('duplicate','{"Result":"FAIL","Result":"PASS"}'),('reverse','{"Result":"PASS","Result":"FAIL"}'),('same','{"Result":"PASS","Result":"PASS"}'),('nested','{"Rows":[{"ExitCode":1,"ExitCode":0}]}'),('nan','{"x":NaN}'),('infinity','{"x":Infinity}'),('counter','{"ExitCode":false}')]:add('JSON-'+tag,'loads',lambda m,raw=raw:json_case(m,raw),'REJECT')
 def direct_schema(m,typ,value):
  try:m.dto.validate(typ,value);return 'VALID'
  except m.Malformed:return 'REJECT'
  except m.Unsupported:return 'UNAVAILABLE'
 for typ,lo,hi in [('uid',1,2**64-1),('account',1,2**63-1),('magic',-(2**63),2**63-1)]:
  for label,value in [('min',lo),('max',hi)]:add('ID-'+typ+'-'+label,'validate',lambda m,k=typ,v=value:direct_schema(m,k,v),'VALID')
  for label,value in [('true',True),('false',False),('zero',0),('float',1.5),('text','1'),('overflow',hi+1)]:add('ID-'+typ+'-'+label,'validate',lambda m,k=typ,v=value:direct_schema(m,k,v),'REJECT')
 def pure_bool(m):
  q,s,a=fixture(m);bool_policy(q,s,a);return m.cost_coverage(q['costClaims'],a['costSets']['COST1'])['status']
 add('cost-bool-direct','cost_coverage',pure_bool,'CONFLICT')
 def unknown_cost(m):
  q,s,a=fixture(m);a['costSets']['COST1']['items'][0]['extra']='unexpected';return m.cost_coverage(q['costClaims'],a['costSets']['COST1'])['status']
 add('cost-unknown-field','cost_coverage',unknown_cost,'CONFLICT')
 add('schema-unknown-field','validate',lambda m:direct_schema(m,{'object':{'x':'text'}},{'x':'ok','extra':'invalid'}),'REJECT')
 def unused_authority(q,s,a):
  a['costSets']['UNUSED']=copy.deepcopy(a['costSets']['COST1']);a['costSets']['UNUSED']['items'][0]['PolicyVersion']=True
 add('authority-unused-malformed','apply_for_test',lambda m:apply_edit(m,unused_authority),expected())
 return out

# Systematic required-field probes from independently constructed positive DTO trees.
# Literal expected: missing required field => REJECT (apply) / CONFLICT (recovery).
def paths(value,path=()):
 if type(value) is dict:
  for k,v in value.items():
   yield path+(k,),v
   yield from paths(v,path+(k,))
 elif type(value) in (list,tuple):
  for i,v in enumerate(value):yield from paths(v,path+(i,))
def location(obj,path):
 for k in path[:-1]:obj=obj[k]
 return obj,path[-1]
def schema_specs():
 q,s,a=fixture(subject);_,committed=subject.apply_for_test(q,s,a);a2=advance_authority(a,q)
 # Structural entries/keys of maps are optional inventory, not required fields.
 variants=[('apply',(q,s,a)),('recovery',(subject.snapshot_store(committed),a2))];out=[]
 for mode,objects in variants:
  for path,v in paths(list(objects)):
   parent,_=location(list(objects),path)
   if type(parent) is not dict:continue
   field=path[-1]
   if field not in {'schema','source','identity','kind','entry','currency','digits','profit','swap','commission','fee','rawNet','postedNet','PolicyVersion','Account','Magic','Broker','Server','Symbol','Cycle','Position','Deal','Order','Event','Role','Plan','Revision','Snapshot','EconomicEventID','AllocationEventID','ConsumptionEventID','AllocationID','allocationEvent','consumptionEvent','allocation','PrincipalAmount','bucket','purpose','intent','revision','BatchID','CostSetID','costClaims','ledger','receipts','complete','history','coreJournal','allocations','context','batches','fillHistory','costSets','refs','expected','expectedVolume','RequiredDeals','historyComplete','NettingPolicy','cap','volume','net','Complete','Authority','items','CostID','Applicability','Amount','AmountBasis','RiskBasis','Window','AlreadyIncluded','AdditionalDeduction','OverlapKnown','sources','events','journalComplete','recordDigest','granted','phase','unallocated','policyVersion','buckets','OriginalGrant','Consumed','Reserved','RemainingFree','Reservations','sequence','payload','digest','grants','commit','event','amount','request','DebitAmount','RequiredBalance','AdditionalRisk','sourceDigest','allocationDigest','batchDigest','costDigest','evaluationContext','checksum','fresh'}:continue
   # Missing always violates required schema, including nullable fields.
   changes=[('missing','DELETE')]
   if type(v) not in (dict,list,tuple) and v is not None and field not in ('digits','NettingPolicy'):changes.append(('null',None))
   if v is not None:
    if type(v) is bool:changes += [('wrong-type','BOOL')]
    elif type(v) is int:changes += [('bool',True),('false',False),('zero',0),('negative',-1),('float',1.5),('string','1'),('overflow',2**64)]
    elif type(v) in (dict,list,tuple):changes += [('wrong-container',True)]
    elif type(v) is str:changes += [('wrong-type',True)]
    else:changes += [('bool',True),('nonfinite',Decimal('NaN'))]
   for tag,val in changes:
    # digits0 and signed Magic -1 are legal, not negative schema probes.
    if type(v) is int and ((field=='digits' and tag=='zero') or (field=='Magic' and tag=='negative')):continue
    if type(v) is int and field=='digits' and tag in ('negative','overflow'):continue # Unsupported precision => unavailable, tested separately.
    out.append(dict(TestID='C2-SCHEMA-'+str(len(out)+1),Mode=mode,Path=path,Change=tag,Value=val,Expected='REJECT' if mode=='apply' else 'CONFLICT'))
 return out

def run(m=subject,with_schema=True):
 rows=[];configs=wire.contexts();started=now()
 for index,ctx in enumerate(configs):
  for case in cases():
   with localcontext(ctx) as active:
    before=wire.context_state(active)
    try:
     calls=set();captured=[]
     allowed={getattr(m,'__file__',''),m.dto.__file__,m.evidence.__file__,m.exact.__file__}
     def profile(frame,event,arg):
      if event=='call' and frame.f_code.co_filename in allowed:
       calls.add(frame.f_code.co_name)
       if index==0 and frame.f_code.co_name==case['Operation']:captured.append(dict(Function=frame.f_code.co_name,Line=frame.f_code.co_firstlineno,Arguments=view(dict(frame.f_locals))))
     sys.setprofile(profile);actual=view(case['run'](m));sys.setprofile(None);exp=view(case['IndependentExpected']);ok=actual==exp and wire.context_state(active)==before
     rows.append(dict(TestID=case['TestID'],GuardID=case['GuardID'],Operation=case['Operation'],ContextID=index,IndependentExpected=exp,Actual=actual,ContextUnchanged=wire.context_state(active)==before,SubjectCalls=sorted(calls),Input=dict(Profile=case['Input'],Calls=captured) if index==0 else dict(Context0InputRef=case['TestID']),Comparisons=2,Result='PASS' if ok else 'FAIL'))
    except Exception as e:
     sys.setprofile(None);rows.append(dict(TestID=case['TestID'],ContextID=index,Result='INFRASTRUCTURE_ERROR',ErrorType=type(e).__name__,Error=str(e)))
 probes=[]
 if with_schema:
  # Use subject only for valid setup; expected negative results are literal schema rules.
  q,s,a=fixture(m);_,s2=m.apply_for_test(q,s,a);a2=advance_authority(a,q)
  for spec in schema_specs():
   objects=copy.deepcopy([q,s,a] if spec['Mode']=='apply' else [m.snapshot_store(s2),a2]);parent,k=location(objects,spec['Path'])
   if spec['Change']=='missing':del parent[k]
   else:parent[k]='not-a-bool' if spec['Value']=='BOOL' else spec['Value']
   original=copy.deepcopy(objects)
   try:
    if spec['Mode']=='apply':r,out=m.apply_for_test(*objects);zero=same(out,objects[1])
    else:r=m.recover_store(objects[0],None,objects[1]);zero=r.get('store') is None
    unchanged=same(objects,original);ok=r['status']==spec['Expected'] and zero and unchanged
    probes.append(dict(TestID=spec['TestID'],Path=list(spec['Path']),Mode=spec['Mode'],Change=spec['Change'],InputValue=repr(spec['Value']),IndependentExpected=spec['Expected'],Actual=r['status'],ZeroDelta=zero,InputsUnchanged=unchanged,Result='PASS' if ok else 'FAIL'))
   except Exception as e:probes.append(dict(TestID=spec['TestID'],Path=list(spec['Path']),Change=spec['Change'],Result='INFRASTRUCTURE_ERROR',ErrorType=type(e).__name__,Error=str(e)))
 return dict(Scenarios=len(cases()),ContextConfigurations=view([wire.context_state(c) for c in configs]),Executions=len(rows),Comparisons=2*len(rows)+3*len(probes),SchemaProbes=len(probes),Pass=sum(r['Result']=='PASS' for r in rows),Fail=sum(r['Result']=='FAIL' for r in rows)+sum(r['Result']=='FAIL' for r in probes),InfrastructureErrors=sum(r['Result']=='INFRASTRUCTURE_ERROR' for r in rows+probes),Rows=rows,SchemaRows=probes,StartedUtc=started,FinishedUtc=now())
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',default='Tests/Evidence/NEXT_STAGE_02B_R0E_C2_TEST_RESULTS.json');args=p.parse_args();r=dict(metadata(),**run(),Command=[sys.executable,*sys.argv],SourceHashes=hashes());r['ExitCode']=int(r['Fail']+r['InfrastructureErrors']>0);save(args.output,r);print({k:v for k,v in r.items() if k not in ('Rows','SchemaRows','ContextConfigurations','SourceHashes')});print([x for x in r['Rows']+r['SchemaRows'] if x['Result']!='PASS'][:18]);return r['ExitCode']
if __name__=='__main__':raise SystemExit(main())
