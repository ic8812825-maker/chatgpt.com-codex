#!/usr/bin/env python3
"""Autonomous C1 reproduction. Never writes C1 artifacts; archived package probes only."""
import copy,io,tarfile,tempfile,types,json,sys,subprocess
from pathlib import Path
import check_hsbi_02b_r0e_c2_contracts as t
import check_hsbi_02b_r0e_c1_contracts as old
import check_hsbi_02b_r0e_c1_mutations as mu
import check_hsbi_02b_r0e_c1_package as pkg

def mutated(source,a,b,name):
 assert source.count(a)==1,(name,source.count(a));m=types.ModuleType(name);m.__file__=name;exec(compile(source.replace(a,b),name,'exec'),m.__dict__);return m
SIX=[('receipt-digest',"receipt['digest']==digest(q) and ",''),('receipt-equation',"require(number(receipt['AdditionalRisk'])>=0 and number(receipt['DebitAmount'])==number(q['PrincipalAmount']) and number(receipt['RequiredBalance'])==number(receipt['DebitAmount'])+number(receipt['AdditionalRisk']) and number(e['amount'])==number(receipt['DebitAmount']))",'require(True)'),('planned-purpose',"for k in ('bucket','purpose','intent')","for k in ('bucket','intent')"),('planned-intent',"for k in ('bucket','purpose','intent')","for k in ('bucket','purpose')"),('ledger-event'," and ledger['allocationEvent']==record['allocationEvent']",''),('ledger-policy'," and ledger['policyVersion']==record['PolicyVersion']",'')]
def causal(name,m):
 if name=='receipt-digest':return t.receipt_case(m,'digest','0'*64)
 if name=='receipt-equation':return t.receipt_case(m,'RequiredBalance',t.Decimal(999))
 if name.startswith('planned'):return t.apply_edit(m,lambda q,s,a:q.__setitem__('purpose' if name.endswith('purpose') else 'intent','FinalClose' if name.endswith('purpose') else 'FOREIGN_INTENT'))
 return t.apply_edit(m,t.allocation_edit('allocationEvent' if name.endswith('event') else 'PolicyVersion'))
def main():
 started=t.now();source=Path(old.subject.__file__).read_text();stock=old.run();stock={k:v for k,v in stock.items() if k not in ('Rows','ContextConfigurations')};sm=mu.run();six=[]
 for name,a,b in SIX:
  m=mutated(source,a,b,'C1_extra_'+name);r=old.run(m);six.append(dict(FindingID='C2-03-'+name,ExactEdit=dict(old=a,new=b),OriginalSourceHash=t.sha(Path(old.subject.__file__)),MutantSourceHash=__import__('hashlib').sha256(source.replace(a,b).encode()).hexdigest(),Stock={k:v for k,v in r.items() if k not in ('Rows','ContextConfigurations')},OriginalNegative=t.view(causal(name,old.subject)),MutantNegative=t.view(causal(name,m)),Classification='CONFIRMED' if r['Pass']==840 and r['Fail']==r['InfrastructureErrors']==0 else 'NOT_REPRODUCED'))
 probes=[]
 q,s,a=t.fixture(old.subject);t.bool_policy(q,s,a);before=copy.deepcopy(s);result,out=old.subject.apply_for_test(q,s,a);probes.append(dict(FindingID='C2-01',PositiveControl='normal50/10/.5',ExactInputOrSourceChange='nested fact+claim PolicyVersion=True, root1',IndependentExpected='REJECT zero deltas',Actual=t.view(dict(coverage=old.subject.cost_coverage(q['costClaims'],a['costSets']['COST1']),authorization=old.subject.authorize(q,s,a),apply=result)),StateBefore=old.state_summary(before),StateAfter=old.state_summary(out),Classification='CONFIRMED' if result['status']=='COMMITTED_IN_MEMORY' else 'NOT_REPRODUCED',ProofBoundary='test-only type contract, no money creation'))
 for label,edit in [('batch-null',lambda q,s,a:a['batches']['T1'].__setitem__('expected',None)),('batch-empty',lambda q,s,a:a['batches']['T1'].__setitem__('expected',{})),('batch-bool',lambda q,s,a:a['batches']['T1'].__setitem__('expected',True)),('history-empty',lambda q,s,a:a['history'].__setitem__(t.wire.encode(('B1','S1',1,99)),{}))]:
  q,s,a=t.fixture(old.subject);edit(q,s,a);before=copy.deepcopy((q,s,a));row=dict(FindingID='C2-02-'+label,IndependentExpected='typed rejection/unavailability',ExactInputOrSourceChange=label,ProofBoundary='malformed DTO, no durable claim')
  try:row['Actual']=old.subject.apply_for_test(q,s,a)[0];row['Classification']='NOT_REPRODUCED'
  except (TypeError,KeyError) as e:row.update(Exception=type(e).__name__,Message=str(e),Classification='CONFIRMED')
  row['InputsUnchanged']=t.same((q,s,a),before);probes.append(row)
 try:old.subject.recover_store(dict(schema='HSBI-C1-STORE-SNAPSHOT-1',checksum='0'*64),None,t.fixture(old.subject)[2]);snapshot='NOT_REPRODUCED'
 except KeyError:snapshot='CONFIRMED'
 # Exact baseline archive for strict stock C1 package checker; do not reseal real history.
 prefix=t.ROOT.relative_to(t.REPO).as_posix()+'/'
 with tempfile.TemporaryDirectory(prefix='R0E_C2_archive_',dir=t.ROOT/'Tests') as td:
  raw=subprocess.check_output(['git','archive',t.BASE,prefix],cwd=t.REPO)
  with tarfile.open(fileobj=io.BytesIO(raw)) as tar:tar.extractall(td,filter='data')
  candidate=Path(td)/prefix
  clone=types.ModuleType('archived_c1_package');clone.__file__=pkg.__file__;exec(compile(Path(pkg.__file__).read_text().replace('str(Path(mu.__file__).relative_to(ROOT))','str(Path(mu.__file__).relative_to(t.ROOT))'),pkg.__file__,'exec'),clone.__dict__)
  clone.ROOT=candidate;clone.REPO=t.REPO;clone.verify.__defaults__=(candidate,t.REPO,True);clone.git_tree.__defaults__=(t.REPO,)
  stockpackage=clone.probes();duplicates=[]
  for label,path,needle,replacement in [('result',pkg.TEST,'"Result": "PASS"','"Result": "FAIL", "Result": "PASS"'),('result-reverse',pkg.TEST,'"Result": "PASS"','"Result": "PASS", "Result": "FAIL"'),('exit',pkg.REG,'"ExitCode": 0','"ExitCode": 1, "ExitCode": 0'),('exit-reverse',pkg.REG,'"ExitCode": 0','"ExitCode": 0, "ExitCode": 1')]:
   f=candidate/path;data=f.read_bytes();proof=clone.load(candidate,pkg.PRES);assert needle in data.decode();f.write_text(data.decode().replace(needle,replacement,1));proof2=copy.deepcopy(proof);proof2['ArtifactHashes'][path]=clone.sha(f);clone.save(candidate,pkg.PRES,proof2);errors=clone.verify();duplicates.append(dict(ID=label,Accepted=not errors,Errors=errors));f.write_bytes(data);clone.save(candidate,pkg.PRES,proof)
 out=dict(t.metadata(),Command=[sys.executable,*sys.argv],StartedUtc=started,FinishedUtc=t.now(),SourceHashes={**t.hashes(),str(Path(__file__).relative_to(t.ROOT)):t.sha(Path(__file__)),**{str(Path(x.__file__).relative_to(t.ROOT)):t.sha(Path(x.__file__)) for x in (old,old.subject,mu,pkg)}},StockReference=stock,StockMutations=sm,StockPackage=stockpackage,SixAdditionalMutations=six,Findings=probes,SnapshotMissingPayload=snapshot,DuplicateJSON=duplicates,RecoveryScope=t.recovery_scope(old.subject))
 out['ExitCode']=int(stock['Pass']!=840 or sm['Killed']!=54 or sm['RedundantSurvivors']!=1 or stockpackage['NegativePassed']!=46 or any(x['Classification']!='CONFIRMED' for x in six+probes) or snapshot!='CONFIRMED');t.save(t.ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0E_C2_REPRODUCTION.json',out);print('REPRODUCTION',out['ExitCode']);return out['ExitCode']
if __name__=='__main__':raise SystemExit(main())
