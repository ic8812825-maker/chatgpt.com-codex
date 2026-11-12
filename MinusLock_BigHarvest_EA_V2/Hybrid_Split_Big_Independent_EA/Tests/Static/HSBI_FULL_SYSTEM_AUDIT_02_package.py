"""Read-only default audit02 integrity checker. --seal and --probes only write new audit02 evidence.
Hardcoded required inventory and IDs independent of checked aggregate totals.
"""
import sys,json,copy,hashlib,tempfile,subprocess,re
from pathlib import Path
import HSBI_FULL_SYSTEM_AUDIT_02_verify as a
REQUIRED_REPORTS=['FINAL_VERDICT','P0_REVERIFICATION','P1_P2_REVIEW','MATH_PROOF_GAPS','NATIVE_READINESS','R1_1_READINESS']
REQUIRED_CONTRACTS=['DEFECT_MATRIX','DECISION_MATRIX','R1_1_ACCEPTANCE','FORMULA_REVIEW','FSM_MATRIX']
REQUIRED_EVIDENCE=['TEST_RESULTS','REGRESSIONS','PRESERVATION','VERIFICATION','SOURCE_TESTS_FRESH','SOURCE_TESTS_EXTENDED','MATH_TESTS_FRESH','LEDGER_TESTS','FAIL_CLASSIFICATION','RECOVERY_INVENTORY','RECOVERY_ARCHIVE','NATIVE_ENVIRONMENT_FRESH']
TESTS=['ECON_REPLAY','FSA001_COMPONENTS','PRICE_CONFLICT','VOLUME_CONFLICT','MAGIC_SAME_PHYSICAL_SOURCE','ALLOC_REPLAY','FSA002_VECTOR','OTHER_ALLOC_EVENT_NEW','ALLOC_DOMAIN_POSITIVE','FSA007_NEGATIVE_BUCKET','RESERVE_BOUND','FSA003_FOREIGN_ALLOCATION','FSA004_EXHAUSTED','FSA010_INDEPENDENT_EXPECTED','FSA010_COPIED_EXPECTED_OBSERVATION','RISK_VALID','FSA005_NAN','RISK_NEGATIVE_MARGIN','TX_VALID','FOREIGN_OWNERSHIP','OTHER_ACTION','FSA006_NAN','TX_PARTIAL','MONEY_VALID','NEGATIVE_MONEY','FSA008_INVALID_FLAG','MONEY_INF','CONTEXT_ONE_FAR','FSA009_INITIAL_SLOT','NO_DUAL_ALL_SLOTS']
MUTS=['ECON_PRICE','ECON_VOLUME','ALLOC_EVENT','TX_OWNERSHIP','TX_ACTION','MONEY_NEGATIVE']
def ep(n):return 'Tests/Evidence/'+a.TAG+n+'.json'
def check(root,baseline=True):
 errors=[]
 def req(ok,msg):
  if not ok:errors.append(msg)
 try:
  for n in REQUIRED_REPORTS:req((root/'Reports'/(a.TAG+n+'_RU.md')).is_file(),'missing report '+n)
  for n in ['FSM_COMPARISON','ECONOMIC_CONSERVATION']:req((root/'Docs'/(a.TAG+n+'_RU.md')).is_file(),'missing doc '+n)
  for n in REQUIRED_CONTRACTS:req((root/'Tests/Contracts'/(a.TAG+n+'.json')).is_file(),'missing contract '+n)
  for n in REQUIRED_EVIDENCE:req((root/ep(n)).is_file(),'missing evidence '+n)
  if errors:return errors
  # Every obligatory graph JSON uses one strict loader, including manifest and catalogs.
  graph={str(p.relative_to(root)):a.strict(p) for p in root.rglob(a.TAG+'*.json') if p.is_file()}
  manifest=graph[ep('VERIFICATION')]
  for row in manifest['Artifacts']:
   req(a.sha(root/row['File'])==row['SHA256'],'artifact hash '+row['File'])
  actual={str(p.relative_to(root)) for p in root.rglob(a.TAG+'*') if p.is_file() and '__pycache__' not in str(p) and p.name not in (a.TAG+'VERIFICATION.json',a.TAG+'PACKAGE_RESULTS.json')}
  req({x['File'] for x in manifest['Artifacts']}==actual,'artifact inventory')
  d=graph['Tests/Contracts/'+a.TAG+'DEFECT_MATRIX.json']['Rows'];req({x['ID'] for x in d}=={'FSA-%03d'%i for i in range(1,30)} and len(d)==29,'defect IDs')
  f=graph['Tests/Contracts/'+a.TAG+'FORMULA_REVIEW.json']['Rows'];req({x['FormulaID'] for x in f}=={'F%02d'%i for i in range(1,50)} and len(f)==49,'formula IDs')
  dec=graph['Tests/Contracts/'+a.TAG+'DECISION_MATRIX.json']['Rows'];req({x['DecisionID'] for x in dec}=={'D-%02d'%i for i in range(1,9)}|{'CR-09','NUM-EXACT-1','NUM-DOMAIN-1','NUM-CODEC','SNAP-FIXTURE-1','FUNDING-GLOBAL-ATTRIBUTION','MQL-DOMAIN','BALANCE-SCHEMA-MAPPING'} and len(dec)==16,'decision IDs')
  req(all(x['ApprovalStatus']=='AWAITING_ADMIN_APPROVAL' and x['AdministratorDecision']=='' for x in dec),'unauthorized approval')
  for name,expected_count in [('SOURCE_TESTS_FRESH',30),('SOURCE_TESTS_EXTENDED',38)]:
   z=graph[ep(name)];req(len(z['Rows'])==expected_count,'test count '+name)
   req(len({x['TestID'] for x in z['Rows']})==expected_count and set(TESTS)<=set(x['TestID'] for x in z['Rows']),'test IDs '+name)
   req(z['Pass']==sum(x['Result']=='PASS' for x in z['Rows']) and z['Fail']==sum(x['Result']=='FAIL' for x in z['Rows']),'test totals '+name)
   req(all(x['Result']==('PASS' if x['Actual']==x['Expected'] else 'FAIL') for x in z['Rows']),'row consistency '+name)
   req(a.sha(root/'Tests/Static'/(a.TAG+'verify.py'))==z['ExecutionMetadata']['RunnerSHA256'],'source runner provenance '+name)
   for x in z['Sources']:req(a.sha(root/x['File'])==x['SHA256'],'subject source hash '+x['File'])
   req(a.sha(root/'Tests/Reference'/(a.TAG+'source_cases.cpp'))==z['FixtureSHA256'],'fixture provenance '+name)
   req(set(x['MutationID'] for x in z['Mutations'])==set(MUTS) and len(z['Mutations'])==6,'mutation catalog '+name)
   for m in z['Mutations']:
    req(m['OriginalNegative']['Result']=='PASS' and m['MutantPositive'][0]==m['MutantPositive'][1] and m['MutantNegative'][0]!=m['MutantNegative'][1] and m['Verdict']=='MUTATION_KILLED','mutation causality '+m['MutationID'])
  req(graph[ep('SOURCE_TESTS_EXTENDED')]['ExtensionSHA256']==a.sha(root/'Tests/Reference'/(a.TAG+'extension.cpp')),'extension provenance')
  fail=graph[ep('FAIL_CLASSIFICATION')]['Rows'];req(len(fail)==13 and {x['FailureID'] for x in fail}=={'A02-FAIL-%02d'%i for i in range(1,14)},'fail classification completeness')
  req({x['TestID'] for x in fail}=={x['TestID'] for x in graph[ep('SOURCE_TESTS_FRESH')]['Rows'] if x['Result']=='FAIL'},'failure traceability')
  for n in ['MATH_TESTS_FRESH','LEDGER_TESTS']:
   z=graph[ep(n)];req(z['Pass']==sum(x['Result']=='PASS' for x in z['Rows']) and z['Fail']==sum(x['Result']=='FAIL' for x in z['Rows']),'math/ledger totals')
  # Known scoped counts required independently, no empty evidence accepted.
  req(len(graph[ep('MATH_TESTS_FRESH')]['Rows'])==23,'rational inventory');req(len(graph[ep('LEDGER_TESTS')]['Rows'])==22,'ledger inventory')
  req(a.sha(root/'Tests/Reference'/(a.TAG+'ledger.py'))==graph[ep('LEDGER_TESTS')]['SubjectSHA256'],'ledger subject hash')
  regress=graph[ep('REGRESSIONS')];req(regress['Completed'] is True and len(regress['Runs'])==9,'regression completion')
  for x in regress['Runs']:
   req(type(x['ExitCode']) is int,'exit code type')
   for file,h in x['SubjectSourceHashes'].items():req(a.sha(root/file)==h,'regression source hash '+file)
  recovered=graph[ep('RECOVERY_INVENTORY')]['Files'];archive=graph[ep('RECOVERY_ARCHIVE')];import base64
  for row in recovered:
   if row['Path'] in archive:req(hashlib.sha256(base64.b64decode(archive[row['Path']]['Base64'])).hexdigest()==row['SHA256'],'recovered original hash '+row['Path'])
  final=(root/'Reports'/(a.TAG+'FINAL_VERDICT_RU.md')).read_text()
  for key,value in [('AUDIT_COMPLETENESS','PARTIAL'),('ADMIN_APPROVAL_COMPLETE','NO'),('R1_1_START_ALLOWED','NO'),('BROKER_DISPATCH_ALLOWED','NO'),('REAL_TRADING_ALLOWED','NO')]:req(re.findall(r'^'+key+r'=(.*)$',final,re.M)==[value],'status uniqueness '+key)
  if baseline:
   req(graph[ep('PRESERVATION')]['Files']==a.inv(),'baseline bytes/modes/inventory')
   paths=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=a.REPO,text=True).splitlines()
   for p in paths:
    fpath=Path(p);req(fpath.name.startswith(a.TAG) and fpath.parts[:2]==a.ROOT.relative_to(a.REPO).parts,'untracked scope '+p)

   for line in subprocess.check_output(['git','diff','--name-status',a.BASE],cwd=a.REPO,text=True).splitlines():
    status,path=line.split('\t',1);req(status=='A' and Path(path).name.startswith(a.TAG) and Path(path).parts[:2]==a.ROOT.relative_to(a.REPO).parts,'tracked unauthorized diff '+line)
 except Exception as e:errors.append('PACKAGE_ERROR '+type(e).__name__+': '+str(e))
 return errors

def seal():
 rows=[]
 for p in sorted(a.ROOT.rglob(a.TAG+'*')):
  if p.is_file() and '__pycache__' not in str(p) and p.name not in (a.TAG+'VERIFICATION.json',a.TAG+'PACKAGE_RESULTS.json'):rows.append(dict(File=str(p.relative_to(a.ROOT)),SHA256=a.sha(p),Bytes=p.stat().st_size))
 a.save('VERIFICATION',dict(BaseSHA=a.BASE,UTC=a.utc(),Artifacts=rows,Exclusions=['VERIFICATION itself: no self-referential hash','PACKAGE_RESULTS: independently re-executed positive/negative probes'],Scope='Integrity of partial audit package, not system correctness',ApprovalStatus='AWAITING_ADMIN_APPROVAL'))
def probes():
 import shutil
 rows=[]
 specs=[('EMPTY_MUTATIONS','SOURCE_TESTS_FRESH',lambda z:z.update(Mutations=[])),('FALSE_TOTAL','SOURCE_TESTS_FRESH',lambda z:z.update(Pass=999)),('FALSE_SOURCE_HASH','REGRESSIONS',lambda z:z['Runs'][0]['SubjectSourceHashes'].update({next(iter(z['Runs'][0]['SubjectSourceHashes'])):'0'*64})),('DELETE_FAILURE','FAIL_CLASSIFICATION',lambda z:z['Rows'].pop())]
 with tempfile.TemporaryDirectory(prefix='hsbi-audit02-package-') as td:
  root=Path(td)/'project';shutil.copytree(a.ROOT,root,ignore=shutil.ignore_patterns('__pycache__','.bin'))
  original=(root/ep('VERIFICATION')).read_bytes()
  for name,n,edit in specs:
   p=root/ep(n);data=p.read_bytes();obj=a.strict(p);edit(obj);p.write_text(json.dumps(obj))
   manifest=a.strict(root/ep('VERIFICATION'))
   for row in manifest['Artifacts']:
    if row['File']==ep(n):row['SHA256']=a.sha(p)
   (root/ep('VERIFICATION')).write_text(json.dumps(manifest));errors=check(root,False);rows.append(dict(ProbeID=name,Errors=errors,Result='PASS' if errors else 'FAIL',ArtifactHashUpdated=True));p.write_bytes(data);(root/ep('VERIFICATION')).write_bytes(original)
  for name,text in [('DUPLICATE_KEY','{"Result":"FAIL","Result":"PASS"}'),('NAN','{"v":NaN}')]:
   p=root/ep('BAD_PROBE');p.write_text(text);errors=check(root,False);rows.append(dict(ProbeID=name,Errors=errors,Result='PASS' if any('ValueError' in e for e in errors) else 'FAIL'));p.unlink()
  p=root/'Reports'/(a.TAG+'FINAL_VERDICT_RU.md');old=p.read_bytes();p.write_text(p.read_text()+'\nBROKER_DISPATCH_ALLOWED=YES\n');m=a.strict(root/ep('VERIFICATION'))
  for row in m['Artifacts']:
   if row['File']==str(p.relative_to(root)):row['SHA256']=a.sha(p)
  (root/ep('VERIFICATION')).write_text(json.dumps(m));errors=check(root,False);rows.append(dict(ProbeID='CONTRADICTORY_POLICY',Errors=errors,Result='PASS' if 'status uniqueness BROKER_DISPATCH_ALLOWED' in errors else 'FAIL'));p.write_bytes(old);(root/ep('VERIFICATION')).write_bytes(original)
  p=root/'Tests/Contracts'/(a.TAG+'R1_1_ACCEPTANCE.json');p.unlink();errors=check(root,False);rows.append(dict(ProbeID='MISSING_REQUIRED',Errors=errors,Result='PASS' if errors else 'FAIL'))
 a.save('PACKAGE_RESULTS',dict(UTC=a.utc(),RunnerSHA256=a.sha(__file__),PositiveErrors=check(a.ROOT),NegativeProbes=rows,Pass=sum(x['Result']=='PASS' for x in rows),Fail=sum(x['Result']=='FAIL' for x in rows),Boundary='8 explicit probes only; no exhaustive package-checker correctness proof'))
 print('PACKAGE_PROBES',len(rows),sum(x['Result']=='PASS' for x in rows));return int(any(x['Result']!='PASS' for x in rows))
if __name__=='__main__':
 if '--seal' in sys.argv:seal()
 if '--probes' in sys.argv:raise SystemExit(probes())
 e=check(a.ROOT);print('PACKAGE',e);raise SystemExit(bool(e))
