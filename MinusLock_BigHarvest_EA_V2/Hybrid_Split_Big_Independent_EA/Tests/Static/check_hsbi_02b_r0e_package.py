#!/usr/bin/env python3
"""R0E independent Git inventory + semantic package validation; no production writes."""
import argparse,ast,copy,hashlib,json,re,shutil,subprocess,tempfile
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parents[1]
PREFIX=ROOT.relative_to(REPO).as_posix()+'/'
BASE='2d34c3378edc5f2df064282fa067bb4af2a1e3b0'
PRES='Tests/Evidence/NEXT_STAGE_02B_R0E_PRESERVATION.json'
RESULT='Tests/Evidence/NEXT_STAGE_02B_R0E_PACKAGE_RESULTS.json'
TESTS='Tests/Evidence/NEXT_STAGE_02B_R0E_VERIFICATION_SUMMARY.json'
MUT='Tests/Evidence/NEXT_STAGE_02B_R0E_MUTATION_RESULTS.json'
MATRIX='Tests/Contracts/NEXT_STAGE_02B_R0E_REQUIREMENT_MATRIX.json'
SHEET='Reports/NEXT_STAGE_02B_R0E_ADMIN_APPROVAL_SHEET_RU.md'
REPORT='Reports/NEXT_STAGE_02B_R0E_FINAL_VERDICT_RU.md'
SUBJECT='Tests/Reference/hsbi_02b_r0e_contract_model.py'
DECISIONS=[f'D-{i:02}' for i in range(1,9)]+['CR-09','NUM-EXACT-1','NUM-DOMAIN-1','NUM-CODEC','SNAP-FIXTURE-1','FUNDING-GLOBAL-ATTRIBUTION','MQL-DOMAIN','BALANCE-SCHEMA-MAPPING']
MANDATORY=[f'Docs/NEXT_STAGE_02B_R0E_{s}_RU.md' for s in ('CONTRACT_FREEZE_CANDIDATE','NUMERIC_ARCHITECTURE','PRODUCTION_REMEDIATION_PLAN')]+[f'Reports/NEXT_STAGE_02B_R0E_{s}_RU.md' for s in ('CONFLICT_REGISTER','ADMIN_APPROVAL_SHEET','TEST_RESULTS','FINAL_VERDICT','R0D_PROVENANCE_ERRATA')]+[SUBJECT,TESTS,MUT,MATRIX,PRES,RESULT]+[f'Tests/Static/{s}.py' for s in ('check_hsbi_02b_r0e_contracts','check_hsbi_02b_r0e_mutations','check_hsbi_02b_r0e_package','run_hsbi_02b_r0e_regressions')]+['Tests/Evidence/NEXT_STAGE_02B_R0E_REGRESSIONS.json']
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def inventory(repo=REPO):
 out={}
 for row in subprocess.check_output(['git','ls-tree','-rz',BASE,'--',PREFIX],cwd=repo).split(b'\0'):
  if row:
   meta,name=row.split(b'\t');mode,kind,oid=meta.decode().split()
   if kind!='blob' or mode not in ('100644','100755'):raise ValueError('unsupported Git baseline entry')
   out[name.decode()[len(PREFIX):]]=oid
 return out
def load(root,p):return json.loads((root/p).read_text())
def save(root,p,d):(root/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def allfiles(root):return {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
def scan(root):
 files=list((root/'Include').rglob('*.mqh'))+list(root.glob('*.mq5'))
 pattern=re.compile(r'\b(?:OrderSend(?:Async)?|CTrade\s*\.\s*(?:Buy|Sell)|(?:trade|m_trade)\s*\.\s*(?:Buy|Sell))\s*\(')
 controls=bool(pattern.search('OrderSend(request,result);')) and bool(pattern.search('trade.Buy(1);')) and not pattern.search('HSBI_IsBrokerDispatchAllowed(mode);')
 bad=[str(p.relative_to(root)) for p in files if pattern.search(p.read_text())]
 policy=(root/'Include/Core/HSBI_RuntimePolicy.mqh').read_text()
 return dict(files=len(files),forbidden=bad,controls=controls,guard=bool(re.search(r'HSBI_IsBrokerDispatchAllowed\([^)]*\)\s*\{return false;\}',policy)))
def seal(root=ROOT):
 inv=inventory();actual=allfiles(root);new=actual-set(inv)
 proof=dict(BaseSHA=BASE,UTC=datetime.now(timezone.utc).isoformat(),existingFiles={p:dict(gitBlob=o,sha256=sha(root/p)) for p,o in inv.items()},productionHashes={p:sha(root/p) for p in inv if p.startswith('Include/') and p.endswith('.mqh') or '/' not in p and p.endswith('.mq5')},newFiles=sorted(new),newArtifactHashes={p:sha(root/p) for p in sorted(new) if p not in (PRES,RESULT)},SelfHashExclusions={PRES:'self-reference',RESULT:'mutable package run results; semantically validated separately'},NoTrade=scan(root),NativeTools={name:shutil.which(name) for name in ('metaeditor','metaeditor64','terminal64','wine')},NativeToolStatus='NOT_RUN')
 save(root,PRES,proof)
def verify(root=ROOT,repo=REPO,check_result=True):
 errors=[]
 def fail(code,path=''):errors.append(dict(code=code,path=path))
 try:
  inv=inventory(repo);p=load(root,PRES)
  if root.resolve()==ROOT.resolve():
   tracked=subprocess.check_output(['git','diff','--name-only',BASE],cwd=repo,text=True).splitlines()
   untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=repo,text=True).splitlines()
   if any(not f.startswith(PREFIX) for f in tracked+untracked):fail('REPOSITORY_SCOPE')
  if p.get('BaseSHA')!=BASE:fail('BASELINE')
  if set(p.get('existingFiles',{}))!=set(inv):fail('BASELINE_INVENTORY')
  production={x for x in inv if x.startswith('Include/') and x.endswith('.mqh') or '/' not in x and x.endswith('.mq5')}
  if len(production)!=74 or set(p.get('productionHashes',{}))!=production:fail('PRODUCTION_INVENTORY')
  for f,oid in inv.items():
   file=root/f
   if not file.is_file() or file.is_symlink():fail('HISTORICAL_MISSING',f);continue
   b=file.read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();row=p['existingFiles'].get(f,{})
   if blob!=oid or row.get('gitBlob')!=oid or row.get('sha256')!=sha(file):fail('HISTORICAL_BYTES',f)
   if f in production and p['productionHashes'].get(f)!=sha(file):fail('PRODUCTION_HASH',f)
  additions=allfiles(root)-set(inv)
  if additions!=set(p.get('newFiles',[])) or len(p['newFiles'])!=len(additions):fail('NEW_INVENTORY')
  if any(f.split('/')[0] not in ('Docs','Reports','Tests') or 'r0e' not in f.lower() or (root/f).is_symlink() for f in additions):fail('OUTSIDE_SCOPE')
  for f in MANDATORY:
   if f not in additions or not (root/f).is_file() or not (root/f).stat().st_size:fail('MANDATORY_ARTIFACT',f)
  if set(p['newArtifactHashes'])!=additions-{PRES,RESULT}:fail('NEW_HASH_INVENTORY')
  for f,h in p['newArtifactHashes'].items():
   if not (root/f).is_file() or sha(root/f)!=h:fail('NEW_HASH',f)
  if scan(root)!=p['NoTrade'] or scan(root)!=dict(files=74,forbidden=[],controls=True,guard=True):fail('NO_TRADE')
  for f in additions:
   if f.endswith('.md'):
    fields=re.findall(r'^BASE_SHA=(\S+)$',(root/f).read_text(),re.M)
    if fields!=[BASE]:fail('REPORT_BASELINE',f)
  historical_base='ec7ae40fe22e1d6e5bed035450750502a1162ab5'
  errata=(root/'Reports/NEXT_STAGE_02B_R0E_R0D_PROVENANCE_ERRATA_RU.md').read_text()
  if subprocess.check_output(['git','rev-parse',BASE+'^'],cwd=repo,text=True).strip()!=historical_base or 'CorrectHistoricalR0DBase: '+historical_base not in errata or 'HistoricalR0DCommit: '+BASE not in errata:fail('PROVENANCE_ROLE')
  t=load(root,TESTS);m=load(root,MATRIX);mu=load(root,MUT);reg=load(root,'Tests/Evidence/NEXT_STAGE_02B_R0E_REGRESSIONS.json')
  for d in (t,m,mu,reg):
   if d.get('BaseSHA')!=BASE:fail('EVIDENCE_BASELINE')
  rows=t['tests'];ids={r['TestID'] for r in rows};contexts=t['contextConfigurations'];n=len(contexts)
  # Compare declared configurations to independently frozen context fixture definition.
  import sys
  sys.path.insert(0,str(ROOT/'Tests/Static'))
  import check_hsbi_02b_r0d_contracts as wire
  expected_configs=wire.view([wire.context_state(c) for c in wire.contexts()])
  if contexts!=expected_configs or n!=8:fail('CONTEXT_METADATA')
  pairs=[(r['TestID'],r['context']) for r in rows]
  if any(type(r['context']) is not int for r in rows) or set(pairs)!={(i,c) for i in ids for c in range(n)} or len(set(pairs))!=len(pairs):fail('CONTEXT_CARTESIAN')
  if len(rows)!=t['executions'] or len(ids)!=t['scenarios'] or t['predicates']!=sum(r['predicates'] for r in rows):fail('TEST_TOTALS')
  if any(r['predicates']!=2 for r in rows):fail('COMPARISON_SCOPE')
  for label,value in [('passed','PASS'),('failed','FAIL'),('infrastructureErrors','INFRASTRUCTURE_ERROR')]:
   if t[label]!=sum(r['Result']==value for r in rows):fail('TEST_TOTALS')
  if t['ExitCode']!=0 or t['failed'] or t['infrastructureErrors'] or any(r['Result']!='PASS' or r['Actual']!=r['Expected'] or r['IndependentExpected']!=r['Expected'] or not r['ContextUnchanged'] for r in rows):fail('TEST_ROW_VERDICT')
  cases=m['cases'];caseids=[r['TestID'] for r in cases]
  if set(caseids)!=ids or len(caseids)!=len(ids) or set(m['scenarioIDs'])!=ids or len(m['scenarioIDs'])!=len(ids):fail('MATRIX_BIJECTION')
  for r in cases:
   f=root/r['SourceFile'];functions={node.name:node.lineno for node in ast.walk(ast.parse(f.read_text())) if isinstance(node,ast.FunctionDef)}
   if functions.get(r['SourceFunction'])!=r['SourceLine']:fail('MATRIX_SOURCE',r['TestID'])
   if r['TestID'] not in ids or r['RequirementID'] not in {q['RequirementID'] for q in m['requirements']}:fail('MATRIX_REFERENCE')
   matching=next((x for x in rows if x['TestID']==r['TestID']),None)
   if matching and (r['IndependentExpected']!=matching['Expected'] or any(x['Expected']!=r['IndependentExpected'] for x in rows if x['TestID']==r['TestID'])):fail('MATRIX_EXPECTED')
  if len(m['requirements'])!=20 or len({x['RequirementID'] for x in m['requirements']})!=20:fail('REQUIREMENT_INVENTORY')
  if mu['catalogSize']!=len(mu['mutations']) or len({r['MutationID'] for r in mu['mutations']})!=len(mu['mutations']):fail('MUTATION_TOTALS')
  if mu['killed']!=sum(r['Verdict']=='MUTATION_KILLED' for r in mu['mutations']) or mu['survived'] or mu['infrastructureErrors']:fail('MUTATION_VERDICT')
  for r in mu['mutations']:
   source=(root/r['TargetFile']).read_text()
   if r['OriginalSourceHash']!=hashlib.sha256(source.encode()).hexdigest():fail('ORIGINAL_SOURCE_HASH',r['MutationID'])
   funcs={node.name for node in ast.walk(ast.parse(source)) if isinstance(node,ast.FunctionDef)}
   if r['TargetFunction'] not in funcs:fail('MUTATION_FUNCTION')
   for e in r['ExactEdit']:
    if e['count']<1 or source.count(e['old'])!=e['count']:fail('EXACT_EDIT',r['MutationID'])
    source=source.replace(e['old'],e['new'])
   try:ast.parse(source)
   except SyntaxError:fail('MUTANT_PARSE')
   if hashlib.sha256(source.encode()).hexdigest()!=r['MutantSourceHash']:fail('MUTANT_SOURCE_HASH',r['MutationID'])
   if r['CausalTestID'] not in ids or r['PositiveTestID'] not in ids or r['PositiveControl']!=r['PositiveExpected'] or r['MutantPositiveControl']!=r['PositiveExpected'] or r['OriginalNegativeOutcome']!=r['IndependentExpected'] or r['MutantNegativeOutcome']==r['IndependentExpected'] or r['Verdict']!='MUTATION_KILLED':fail('MUTATION_CAUSALITY')
  for r in mu['mutations']:
   negative=next((x for x in rows if x['TestID']==r['CausalTestID']),None);positive=next((x for x in rows if x['TestID']==r['PositiveTestID']),None)
   if negative is None or positive is None or r['IndependentExpected']!=negative['IndependentExpected'] or r['PositiveExpected']!=positive['IndependentExpected']:fail('MUTATION_EXPECTED_BINDING')
  for obj in (t,mu):
   for f,h in obj['SourceHashes'].items():
    if sha(root/f)!=h:fail('SOURCE_HASH',f)
  if not reg['BaselineMatch'] or reg['RegressionStatus']!='FAIL' or any(r['ExitCode']!=r['ExpectedBaselineExit'] for r in reg['runs'] if 'ExpectedBaselineExit' in r):fail('REGRESSION_BASELINE')
  text=(root/SHEET).read_text();sections=re.split(r'^## Contract: (.+)$',text,flags=re.M);found=[]
  for i in range(1,len(sections),2):
   contract,body=sections[i:i+2];found.append(contract)
   if 'ApprovalStatus: AWAITING_ADMIN_APPROVAL' not in body:fail('APPROVAL_STATUS',contract)
   for label in ('AdministratorDecision','ApprovalDate','ApprovalIdentifier'):
    if len(re.findall(r'^'+label+r':',body,re.M))!=1:fail('APPROVAL_DUPLICATE',contract+':'+label)
    match=re.search(r'^'+label+r':([^\n]*)(?:\n(.*?))?(?=^[A-Za-z][A-Za-z]+:|\Z)',body,re.M|re.S)
    if not match or any(part.strip() for part in match.groups() if part is not None):fail('APPROVAL_NONEMPTY',contract+':'+label)
  if sorted(found)!=sorted(DECISIONS):fail('APPROVAL_INVENTORY')
  if check_result:
   pr=load(root,RESULT);negative=pr.get('negative',[])
   if pr.get('BaseSHA')!=BASE or pr.get('positive')!='PASS' or pr.get('errors') or pr.get('SourceHash')!=sha(root/'Tests/Static/check_hsbi_02b_r0e_package.py'):fail('PACKAGE_RESULT_METADATA')
   if len(negative)!=23 or len({x['ProbeID'] for x in negative})!=23 or pr.get('negativePassed')!=23 or pr.get('negativeFailed')!=0 or any(x.get('Result')!='PASS' or x.get('ExpectedCode') not in {e['code'] for e in x.get('ActualErrors',[])} for x in negative):fail('PACKAGE_RESULT_TOTALS')
  verdict=(root/REPORT).read_text()
  for field in ('ADMIN_APPROVAL_COMPLETE','PRODUCTION_REMEDIATION_ALLOWED','TRADING_LOGIC_START_ALLOWED','BROKER_DISPATCH_ALLOWED','REAL_TRADING_ALLOWED'):
   if not re.search(r'^'+field+r'=NO$',verdict,re.M):fail('VERDICT_POLICY',field)
  if 'CONTRACT_FREEZE_CANDIDATE_READY=YES' not in verdict:fail('VERDICT_CANDIDATE')
 except (OSError,ValueError,KeyError,TypeError,StopIteration) as e:fail('MALFORMED_PACKAGE',str(e))
 return errors

def probes(root=ROOT):
 baseline=verify(root,check_result=False);results=[]
 if baseline:return dict(positive='FAIL',positiveErrors=baseline,negative=[])
 inv=inventory();files=allfiles(root)
 def edit_json(copyroot,path,edit):
  d=load(copyroot,path);edit(d);save(copyroot,path,d)
 def probe(name,expected,edit):
  with tempfile.TemporaryDirectory(prefix='R0E_package_',dir=root/'Tests') as td:
   candidate=Path(td)/'candidate'
   for f in files:
    dest=candidate/f;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/f,dest)
   edit(candidate)
   # Refresh only disposable new-artifact hashes to isolate semantic guards.
   p=load(candidate,PRES)
   for f in p['newArtifactHashes']:
    if (candidate/f).is_file():p['newArtifactHashes'][f]=sha(candidate/f)
   save(candidate,PRES,p);errors=verify(candidate,check_result=False)
   results.append(dict(ProbeID=name,ExpectedCode=expected,ActualErrors=errors,Result='PASS' if expected in {x['code'] for x in errors} else 'FAIL',Boundary='Disposable copy only; historical real bytes untouched'))
 def j(path,fn):return lambda r:edit_json(r,path,fn)
 historical=next(iter(inv))
 probe('inventory-omission','BASELINE_INVENTORY',j(PRES,lambda d:d['existingFiles'].pop(historical)))
 probe('historical-content','HISTORICAL_BYTES',lambda r:(r/historical).write_bytes((r/historical).read_bytes()+b'\nsynthetic'))
 probe('outside-scope','OUTSIDE_SCOPE',lambda r:(r/'bad_r0e.txt').write_text('synthetic'))
 probe('source-hash','SOURCE_HASH',j(TESTS,lambda d:d['SourceHashes'].__setitem__(SUBJECT,'0'*64)))
 probe('test-total','TEST_TOTALS',j(TESTS,lambda d:d.__setitem__('executions',0)))
 probe('fail-with-pass-total','TEST_ROW_VERDICT',j(TESTS,lambda d:d['tests'][0].__setitem__('Result','FAIL')))
 probe('mandatory-missing','MANDATORY_ARTIFACT',lambda r:(r/'Docs/NEXT_STAGE_02B_R0E_NUMERIC_ARCHITECTURE_RU.md').unlink())
 probe('report-baseline','REPORT_BASELINE',lambda r:(r/REPORT).write_text((r/REPORT).read_text().replace('BASE_SHA='+BASE,'BASE_SHA='+'0'*40)))
 probe('empty-cases','MATRIX_BIJECTION',j(MATRIX,lambda d:d.__setitem__('cases',[])))
 probe('missing-case','MATRIX_BIJECTION',j(MATRIX,lambda d:d['cases'].pop()))
 probe('duplicate-case','MATRIX_BIJECTION',j(MATRIX,lambda d:d['cases'].append(copy.deepcopy(d['cases'][0]))))
 probe('context-999','CONTEXT_CARTESIAN',j(TESTS,lambda d:d['tests'][0].__setitem__('context',999)))
 probe('context-bool','CONTEXT_CARTESIAN',j(TESTS,lambda d:d['tests'][0].__setitem__('context',False)))
 probe('context-missing','CONTEXT_CARTESIAN',j(TESTS,lambda d:d['tests'].pop()))
 probe('context-duplicate','CONTEXT_CARTESIAN',j(TESTS,lambda d:d['tests'].append(copy.deepcopy(d['tests'][0]))))
 probe('context-metadata','CONTEXT_METADATA',j(TESTS,lambda d:d['contextConfigurations'][0].__setitem__('precision',999)))
 probe('original-hash','ORIGINAL_SOURCE_HASH',j(MUT,lambda d:d['mutations'][0].__setitem__('OriginalSourceHash','0'*64)))
 probe('mutant-hash','MUTANT_SOURCE_HASH',j(MUT,lambda d:d['mutations'][0].__setitem__('MutantSourceHash','0'*64)))
 probe('exact-edit','EXACT_EDIT',j(MUT,lambda d:d['mutations'][0]['ExactEdit'][0].__setitem__('old','absent synthetic target')))
 probe('approval-inline','APPROVAL_NONEMPTY',lambda r:(r/SHEET).write_text((r/SHEET).read_text().replace('AdministratorDecision:\n','AdministratorDecision: APPROVED\n',1)))
 probe('approval-newline','APPROVAL_NONEMPTY',lambda r:(r/SHEET).write_text((r/SHEET).read_text().replace('AdministratorDecision:\n','AdministratorDecision:\n\nAPPROVED\n',1)))
 probe('approval-duplicate','APPROVAL_DUPLICATE',lambda r:(r/SHEET).write_text((r/SHEET).read_text().replace('AdministratorDecision:\n','AdministratorDecision:\n\nAdministratorDecision: APPROVED\n',1)))
 probe('verdict-policy','VERDICT_POLICY',lambda r:(r/REPORT).write_text((r/REPORT).read_text().replace('ADMIN_APPROVAL_COMPLETE=NO','ADMIN_APPROVAL_COMPLETE=YES')))
 return dict(positive='PASS',negative=results,negativePassed=sum(r['Result']=='PASS' for r in results),negativeFailed=sum(r['Result']!='PASS' for r in results))
def main():
 p=argparse.ArgumentParser();p.add_argument('--seal',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args()
 if a.seal:seal()
 start=datetime.now(timezone.utc).isoformat();errors=verify(check_result=not a.self_test);out=dict(BaseSHA=BASE,Command=['python',str(Path(__file__).relative_to(ROOT)),*(__import__('sys').argv[1:])],StartedUtc=start,FinishedUtc=datetime.now(timezone.utc).isoformat(),positive='PASS' if not errors else 'FAIL',errors=errors,SourceHash=sha(Path(__file__)))
 if a.self_test and not errors:out.update(probes())
 if a.self_test:
  out['FinishedUtc']=datetime.now(timezone.utc).isoformat();save(ROOT,RESULT,out)
 print(json.dumps(out,ensure_ascii=False));return int(bool(errors) or out.get('negativeFailed',0)>0)
if __name__=='__main__':raise SystemExit(main())
