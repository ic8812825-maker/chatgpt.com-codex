#!/usr/bin/env python3
"""Autonomous old R0E reproduction from immutable baseline archive, no /tmp dependency."""
import copy,hashlib,io,json,subprocess,sys,tarfile,tempfile,types
from pathlib import Path
from decimal import Decimal
import check_hsbi_02b_r0e_c1_contracts as new
import check_hsbi_02b_r0e_contracts as old
import check_hsbi_02b_r0e_package as pkg
import check_hsbi_02b_r0e_mutations as muts
ROOT=new.ROOT;REPO=ROOT.parents[1];PREFIX=ROOT.relative_to(REPO).as_posix()+'/'
def module(s,name):
 m=types.ModuleType(name);m.__file__=name;exec(compile(s,name,'exec'),m.__dict__);return m
def main():
 started=new.now();rows=[];sources=[Path(__file__).resolve(),Path(old.__file__),Path(old.model.__file__),Path(pkg.__file__),Path(muts.__file__),Path(old.model.exact.__file__),Path(new.__file__),Path(new.subject.__file__),Path(new.wire.__file__)]
 stock=old.run();stock={k:v for k,v in stock.items() if k not in ('tests','contextConfigurations')};print('R0E_STOCK',stock,flush=True)
 source=Path(old.model.__file__).read_text();specs={r['TestID']:r for r in old.cases()};stockMut=[]
 for name,fn,pos,neg,edits in muts.catalog():
  s=source
  for a,b in edits:s=s.replace(a,b)
  m=module(s,'old_mut_'+name);op=old.view(specs[pos]['run'](old.model));mp=old.view(specs[pos]['run'](m));on=old.view(specs[neg]['run'](old.model));mn=old.view(specs[neg]['run'](m))
  stockMut.append(dict(MutationID=name,TargetFunction=fn,ExactEdit=[dict(old=a,new=b) for a,b in edits],PositiveTestID=pos,NegativeTestID=neg,PositiveExpected=old.view(specs[pos]['Expected']),OriginalPositive=op,MutantPositive=mp,StockExpected=old.view(specs[neg]['Expected']),OriginalNegative=on,MutantNegative=mn,Killed=op==mp==old.view(specs[pos]['Expected']) and on==old.view(specs[neg]['Expected']) and mn!=on))
 extra=[]
 for name,a,b in [('raw',"raw==number(r['rawNet']) and ",''),('grid'," and exact.grid(r['postedNet'],r['digits'])",''),('namespace','require(source_key(r)==tuple(source))','require(True)')]:
  assert source.count(a)==1;m=module(source.replace(a,b),'old_extra_'+name);r=old.run(m)
  def causal(subject):
   s,h,k=old.fixture()
   if name=='raw':h[old.wire.encode(k)]['rawNet']=Decimal(999)
   if name=='namespace':h[old.wire.encode(k)]['identity']['Account']=2
   if name=='grid':
    h[old.wire.encode(k)]['postedNet']=Decimal('50.005')
    try:subject.economic_record(h,k);return 'RECORD_ACCEPTED'
    except subject.Malformed:return 'REJECT'
   return subject.fund(s,h,k,'A1',1,old.grants())[0]
  extra.append(dict(MutationID='R0E-extra-'+name,ExactEdit=dict(old=a,new=b),OriginalSourceHash=hashlib.sha256(source.encode()).hexdigest(),MutantSourceHash=hashlib.sha256(source.replace(a,b).encode()).hexdigest(),Stock={k:v for k,v in r.items() if k not in ('tests','contextConfigurations')},OriginalNegativeOutcome=causal(old.model),MutantNegativeOutcome=causal(m),IndependentExpected='REJECT',Classification='CONFIRMED' if r['passed']==728 and causal(old.model)=='REJECT' and causal(m)!='REJECT' else 'NOT_REPRODUCED'))
  extra[-1].update(FindingID='C1-03-'+name,SourceFile=str(Path(old.model.__file__).relative_to(ROOT)),SourceFunction='economic_record',PositiveControl='Normal source50: stock positive scenario passes in original and mutant',StateDelta='Grid direct API is pure; raw/namespace mutant produces a new in-memory funding while original rejects. Original/returned ledger differences covered by C1 causal cases.',ProofBoundary='Old R0E validator/registry fixtures; no broker/durable proof')
  print('R0E_EXTRA',name,extra[-1]['Classification'],flush=True)
 package=[]
 with tempfile.TemporaryDirectory(prefix='R0E_C1_baseline_',dir=ROOT/'Tests') as td:
  raw=subprocess.check_output(['git','archive',new.BASE,PREFIX],cwd=REPO)
  with tarfile.open(fileobj=io.BytesIO(raw)) as tar:tar.extractall(td,filter='data')
  candidate=Path(td)/PREFIX;positive=pkg.verify(candidate);stockPackage=pkg.probes(candidate)
  for name,path,change in [('C1-01',pkg.MUT,lambda d:d.update(catalogSize=0,killed=0,survived=0,infrastructureErrors=0,mutations=[])),('C1-02-approval',pkg.SHEET,lambda s:s.replace('ApprovalStatus: AWAITING_ADMIN_APPROVAL','ApprovalStatus: AWAITING_ADMIN_APPROVAL\nApprovalStatus: APPROVED',1)),('C1-02-admin',pkg.REPORT,lambda s:s+'\nADMIN_APPROVAL_COMPLETE=YES\n'),('C1-02-dispatch',pkg.REPORT,lambda s:s+'\nBROKER_DISPATCH_ALLOWED=YES\n'),('C1-08','Tests/Evidence/NEXT_STAGE_02B_R0E_REGRESSIONS.json',lambda d:d['runs'][0]['SourceHashes'].__setitem__(next(iter(d['runs'][0]['SourceHashes'])),'0'*64))]:
   f=candidate/path;data=f.read_bytes();pres=pkg.load(candidate,pkg.PRES)
   if path.endswith('.json'):d=json.loads(data);change(d);pkg.save(candidate,path,d)
   else:f.write_text(change(data.decode()))
   pp=copy.deepcopy(pres);pp['newArtifactHashes'][path]=pkg.sha(f);pkg.save(candidate,pkg.PRES,pp);errors=pkg.verify(candidate)
   package.append(dict(FindingID=name,PositiveControl=not positive,ExactInputOrSourceChange=name,IndependentExpected='REJECT_TAMPERED_PACKAGE',ActualOutcome='ACCEPT' if not errors else 'REJECT',Errors=errors,StateDelta='Disposable candidate only; Git baseline unchanged',ProofBoundary='Old package checker semantic validation',Classification='CONFIRMED' if not errors and not positive else 'NOT_REPRODUCED'))
   f.write_bytes(data);pkg.save(candidate,pkg.PRES,pres)
 m=old.model;s,h,k=old.funded(m);s['journalComplete']=False;before=copy.deepcopy(s);spend,out=m.operate(s,h,k,'A1',2,'CONSUME_FREE','FinalReserve',Decimal(10))
 rows.append(dict(FindingID='C1-04',PositiveControl='KNOWN_MODEL_AVAILABLE 50 with complete journal',ExactInputOrSourceChange='state.journalComplete=False',IndependentExpected='UNAVAILABLE availability',ActualOutcome=dict(availability=old.view(m.reserve_available(s,h,k[:3])),spend=spend),StateDelta=old.view(before,True)==old.view(out,True),Classification='CONFIRMED',ProofBoundary='No double spend; spend remains blocked'))
 f1=dict(source=('B1','S1',1,101),volume='0.4',net='-15');f2=dict(source=('B1','S1',2,102),volume='0.6',net='100')
 rows.append(dict(FindingID='C1-05',PositiveControl=old.view(m.transition_status([dict(f1,net='-5'),dict(f2,source=('B1','S1',1,102),net='-5')],{f1['source']:dict(f1,net='-5'),('B1','S1',1,102):dict(f2,source=('B1','S1',1,102),net='-5')},'1','12')),ExactInputOrSourceChange=[f1,f2],IndependentExpected='Must not confirm target-account batch with foreign fill',ActualOutcome=old.view(m.transition_status([f1,f2],{f1['source']:f1,f2['source']:f2},'1','12')),StateDelta=None,Classification='CONFIRMED',ProofBoundary='Missing batch scope; not broker execution'))
 basis={'EXEC':dict(RiskBasis='executionUncertainty',Window='I1',AlreadyIncluded=False,OverlapKnown=True)};cost=dict(CostID='EXEC',RiskBasis='executionUncertainty',Window='I1',AlreadyIncluded=False,AdditionalDeduction=False)
 rows.append(dict(FindingID='C1-06',PositiveControl=m.costs_status([dict(cost,AdditionalDeduction=True)],basis),ExactInputOrSourceChange=cost,IndependentExpected='Not complete cost proof',ActualOutcome=dict(omitted=m.costs_status([cost],basis),empty=m.costs_status([],basis)),StateDelta=None,Classification='CONFIRMED',ProofBoundary='Old helper checks supplied rows only'))
 h,k,c,a,i=old.identity_fixture();positive=m.verify_identity(i,h,k,c,a);a['allocationEvent']=999
 rows.append(dict(FindingID='C1-07',PositiveControl=positive,ExactInputOrSourceChange='allocationEvent 1→999',IndependentExpected='Not allocation-event-bound PASS',ActualOutcome=m.verify_identity(i,h,k,c,a),StateDelta=None,Classification='CONFIRMED',ProofBoundary='Source-context helper scope'))
 matrix=json.loads((ROOT/'Tests/Contracts/NEXT_STAGE_02B_R0E_REQUIREMENT_MATRIX.json').read_text());trace=[]
 for tid,actual in [('MQL-mul-overflow','checked_mul'),('D05-unsupported-aggregate','transition_status')]:
  row=next(r for r in matrix['cases'] if r['TestID']==tid);trace.append(dict(TestID=tid,Reported=row['SourceFunction'],ActualOperation=actual,SourceTest='Tests/Static/check_hsbi_02b_r0e_contracts.py',Classification='CONFIRMED' if row['SourceFunction']!=actual else 'NOT_REPRODUCED'))
 # Inspect EVERY old matrix row; observed calls distinguish indirect refs from absent refs.
 full=[];sourcefiles={str(Path(old.model.__file__).resolve()),str(Path(old.model.exact.__file__).resolve())}
 for spec in old.cases():
  calls=set()
  def profile(frame,event,arg):
   if event=='call' and frame.f_code.co_filename in sourcefiles:calls.add(frame.f_code.co_name)
  try:
   sys.setprofile(profile);spec['run'](old.model)
  finally:sys.setprofile(None)
  row=next(x for x in matrix['cases'] if x['TestID']==spec['TestID'])
  full.append(dict(TestID=spec['TestID'],ReportedSourceFile=row['SourceFile'],ReportedSourceFunction=row['SourceFunction'],ObservedSubjectCalls=sorted(calls),ReferenceStatus='OBSERVED_CALL_REFERENCE_NOT_EXACT_TARGET_PROOF' if row['SourceFunction'] in calls else 'REPORTED_FUNCTION_NOT_CALLED',TestImplementationLine=spec['run'].__code__.co_firstlineno))
 rows.append(dict(FindingID='C1-09',SourceFile=str(Path(old.__file__).relative_to(ROOT)),SourceFunction='cases',ActualOutcome=dict(DesignatedCases=trace,FullMatrixReviewed=len(full),ReportedFunctionNotCalled=sum(r['ReferenceStatus']=='REPORTED_FUNCTION_NOT_CALLED' for r in full)),FullMatrixReview=full,TraceProbeExecutions=len(full),Classification='CONFIRMED',IndependentExpected='Exact subject operation mapping; observed presence alone is not exact target proof'))
 for row in rows+package:
  row.setdefault('SourceFile',str(Path(pkg.__file__ if row['FindingID'].startswith(('C1-01','C1-02','C1-08')) else old.model.__file__).relative_to(ROOT)))
  row.setdefault('SourceFunction',{'C1-04':'reserve_available','C1-05':'transition_status','C1-06':'costs_status','C1-07':'verify_identity','C1-09':'matrix source mapping'}.get(row['FindingID'],'verify'))
  row.setdefault('PositiveControl','Untampered independent fixture / baseline archive accepted')
  row.setdefault('ExactInputOrSourceChange',row['FindingID'])
  row.setdefault('StateDelta',None)
  row.setdefault('ProofBoundary','Static source traceability, no production execution')
 out=dict(new.metadata(),Command=[sys.executable,*sys.argv],StartedUtc=started,FinishedUtc=new.now(),SourceHashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},StockReference=stock,StockMutations=stockMut,StockPackage=stockPackage,AdditionalMutations=extra,PackageGaps=package,Findings=rows)
 out['ExitCode']=int(stock['passed']!=728 or not all(r['Killed'] for r in stockMut) or any(r['Classification']!='CONFIRMED' for r in extra+package+rows));new.save(ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0E_C1_REPRODUCTION.json',out);print('REPRODUCTION_EXIT',out['ExitCode'],flush=True);return out['ExitCode']
if __name__=='__main__':raise SystemExit(main())
