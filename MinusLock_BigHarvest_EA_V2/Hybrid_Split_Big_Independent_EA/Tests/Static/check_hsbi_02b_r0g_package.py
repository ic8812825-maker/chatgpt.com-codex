#!/usr/bin/env python3
"""R0G independent baseline/approval preservation verifier, no historical writes.
--build-evidence runs R0G tests and read-only frozen R0F check, captures real processes.
--seal writes R0G preservation only; default verifies read-only.
"""
import sys,json,subprocess,hashlib,copy,os
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parents[1];BASE='bcaa766568b9fe7eec0781a8c6efbb288cf16dae';PREFIX=ROOT.relative_to(REPO).as_posix()+'/'
sys.path[:0]=[str(ROOT/'Tests/Static'),str(ROOT/'Tests/Reference')]
import check_hsbi_02b_r0g_contracts as tests

def strict(text):
 def pairs(items):
  d={}
  for k,v in items:
   if k in d:raise ValueError('duplicate key '+k)
   d[k]=v
  return d
 return json.loads(text,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def path(name,folder='Tests/Evidence'):return ROOT/folder/f'NEXT_STAGE_02B_R0G_{name}.json'
def save(name,obj):path(name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def inventory():
 data={}
 for row in subprocess.check_output(['git','ls-tree','-rz',BASE,'--',PREFIX],cwd=REPO).split(b'\0'):
  if not row:continue
  modeblob,name=row.split(b'\t');mode,kind,blob=modeblob.decode().split();rel=name.decode()[len(PREFIX):];p=ROOT/rel;b=p.read_bytes();actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
  if actual!=blob or bool(p.stat().st_mode&0o111)!=(mode=='100755'):raise ValueError('historical change '+rel)
  data[rel]=dict(Mode=mode,GitBlob=blob,SHA256=sha(p))
 return data

def process(label,runner,args=()):
 cmd=[sys.executable,str(ROOT/runner),*args];start=now();p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
 return dict(ID=label,Command=cmd,StartedUtc=start,FinishedUtc=now(),TestedSHA=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),RunnerSourceHash=sha(ROOT/runner),RunnerPath=runner,ExitCode=p.returncode,Stdout=p.stdout,Stderr=p.stderr)

def assess(override=None):
 errors=[]
 def check(ok,msg):
  if not ok:errors.append(msg)
 try:
  pres=override if override is not None else strict(path('PRESERVATION').read_text());actual=inventory();check(actual==pres['Existing'],'baseline inventory');prod={p:v for p,v in actual.items() if p.startswith('Include/') and p.endswith('.mqh') or '/' not in p and p.endswith('.mq5')};check(prod==pres['Production'] and len(prod)==74,'production inventory')
  newfiles=set()
  for row in subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','--',PREFIX],cwd=REPO,text=True).splitlines():
   rel=row[len(PREFIX):]
   if rel in actual:continue
   f=ROOT/rel
   if not f.is_file():continue
   if rel.startswith(('Docs/','Reports/','Tests/Contracts/','Tests/Evidence/')):allowed=f.name.startswith('NEXT_STAGE_02B_R0G_')
   elif rel.startswith('Tests/Reference/'):allowed=f.name.startswith('hsbi_02b_r0g_')
   elif rel.startswith('Tests/Static/'):allowed=f.name.startswith('check_hsbi_02b_r0g_')
   else:allowed=False
   check(allowed,'out of scope '+rel);newfiles.add(rel)
  excluded={'Tests/Evidence/NEXT_STAGE_02B_R0G_PRESERVATION.json','Tests/Evidence/NEXT_STAGE_02B_R0G_PACKAGE_RESULTS.json'}
  check(set(pres['ArtifactHashes'])==newfiles-excluded,'artifact inventory')
  for p,h in pres['ArtifactHashes'].items():check(sha(ROOT/p)==h,'artifact hash '+p)
  load=lambda n,f='Tests/Evidence':strict(path(n,f).read_text())
  a=load('APPROVAL_MATRIX','Tests/Contracts');i=load('IDENTITY_MATRIX','Tests/Contracts');t=load('TEST_RESULTS');e=load('EXECUTIONS')
  check(a['ApprovalStatus']=='AWAITING_ADMIN_APPROVAL' and a['AdministratorDecision']=='' and a['R1_1_START_ALLOWED'] is False,'approval status')
  check(a['ProductionBaseline']==BASE and a['ProductionAllowlist']==['Include/Money/HSBI_EconomicLedgerTypes.mqh'],'allowlist/baseline')
  check(len(a['RequiredDecisions'])==16 and len({r['DecisionID'] for r in a['RequiredDecisions']})==16 and all(r['ApprovalStatus']=='AWAITING_ADMIN_APPROVAL' for r in a['RequiredDecisions']),'16 pending decisions')
  check(a['CodecCandidate']=='HSBI-F64Z-1' and a['CandidateNotAdministratorSelection'] is True,'codec candidate scope')
  check(len(i['Fields'])==29 and tuple(r['Field'] for r in i['Fields'])==tests.fixture.ORDER and all(r['RequiredForMinimalR1'] for r in i['Fields']),'immutable schema')
  check(i['SourceKey']==['Broker','Server','AccountLogin','DealTicket'] and i['NoFundingPermission'] is True,'source scope')
  expected=tests.execute();check(len(expected)==128,'required test count');check(t['Rows']==expected,'independent reproducibility')
  check(type(t['Pass']) is int and t['Pass']==128 and t['Fail']==t['InfrastructureErrors']==t['ExitCode']==0,'test totals')
  check(t['MQL5_NATIVE_TESTS']==t['MQL5_COMPILE']=='NOT_RUN','native scope')
  for p,h in t['SourceHashes'].items():check(sha(ROOT/p)==h,'execution source hash '+p)
  for r in e['Runs']:check(r['ExitCode']==0 and sha(ROOT/r['RunnerPath'])==r['RunnerSourceHash'],'process '+r['ID'])
  check(len(e['Runs'])==2 and e['StaticNoTrade']=={'files':74,'forbidden':[],'controls':True,'guard':True},'read-only R0F/no trade')
  for p,h in e['SourceHashes'].items():check(sha(ROOT/p)==h,'process dependency '+p)
  for name in ('APPROVAL_BALLOT','FINAL_VERDICT'):
   doc=(ROOT/f'Reports/NEXT_STAGE_02B_R0G_{name}_RU.md').read_text()
   for field in ('ADMIN_APPROVAL_COMPLETE','R1_1_START_ALLOWED','PRODUCTION_REMEDIATION_ALLOWED','TRADING_LOGIC_START_ALLOWED','BROKER_DISPATCH_ALLOWED','REAL_TRADING_ALLOWED'):
    check(doc.count('\n'+field+'=NO\n')==1 and doc.count('\n'+field+'=')==1,'unique policy '+name+' '+field)
 except (ValueError,KeyError,TypeError,OSError) as err:errors.append(type(err).__name__+': '+str(err))
 return errors

def main():
 if '--build-evidence' in sys.argv:
  start=now();runs=[process('R0G_REFERENCE','Tests/Static/check_hsbi_02b_r0g_contracts.py'),process('R0F_READ_ONLY_PACKAGE','Tests/Static/check_hsbi_02b_r0f_package.py')]
  import check_hsbi_02b_r0e_package as old
  scan=old.scan(ROOT);save('EXECUTIONS',dict(BaseSHA=BASE,StartedUtc=start,FinishedUtc=now(),SourceHashes={str(Path(p).relative_to(ROOT)):sha(p) for p in [__file__,old.__file__]},Runs=runs,StaticNoTrade=scan,MQL5Native='NOT_RUN',HistoricalRegressionR7R0='NOT_RERUN; frozen R0F failures retained',ExitCode=int(any(r['ExitCode'] for r in runs))))
 if '--seal' in sys.argv:
  old=inventory();files=[p for p in ROOT.rglob('*') if p.is_file() and ('NEXT_STAGE_02B_R0G_' in p.name or p.name.startswith(('hsbi_02b_r0g_','check_hsbi_02b_r0g_'))) and '__pycache__' not in str(p)]
  excluded={path('PRESERVATION'),path('PACKAGE_RESULTS')};save('PRESERVATION',dict(BaseSHA=BASE,UTC=now(),Existing=old,Production={p:v for p,v in old.items() if p.startswith('Include/') and p.endswith('.mqh') or '/' not in p and p.endswith('.mq5')},ArtifactHashes={str(p.relative_to(ROOT)):sha(p) for p in files if p not in excluded},SelfHashExcluded=['PRESERVATION','PACKAGE_RESULTS']))
 errors=assess();print('R0G PACKAGE',errors)
 if '--seal' in sys.argv:
  probes=[];manifest=strict(path('PRESERVATION').read_text())
  for kind in ['omitted-baseline','altered-baseline-hash','missing-production','altered-artifact-hash']:
   candidate=copy.deepcopy(manifest)
   if kind=='omitted-baseline':candidate['Existing'].pop(next(iter(candidate['Existing'])))
   if kind=='altered-baseline-hash':candidate['Existing'][next(iter(candidate['Existing']))]['SHA256']='0'*64
   if kind=='missing-production':candidate['Production'].pop(next(iter(candidate['Production'])))
   if kind=='altered-artifact-hash':candidate['ArtifactHashes'][next(iter(candidate['ArtifactHashes']))]='0'*64
   found=assess(candidate);probes.append(dict(ProbeID=kind,Errors=found,Result='PASS' if found else 'FAIL'))
  for label,text in [('duplicate-root','{"a":0,"a":1}'),('duplicate-nested','{"a":{"x":1,"x":1}}'),('nan','{"a":NaN}'),('infinity','{"a":Infinity}')]:
   try:strict(text);found=False
   except ValueError:found=True
   probes.append(dict(ProbeID=label,Result='PASS' if found else 'FAIL'))
  save('PACKAGE_RESULTS',dict(BaseSHA=BASE,UTC=now(),VerifierHash=sha(__file__),Errors=errors,Positive='PASS' if not errors else 'FAIL',NegativeProbes=probes,ExitCode=int(bool(errors) or any(p['Result']!='PASS' for p in probes)),Scope='Read-only identity ballot/registry binding; no broker/native/durable evidence'))
 return int(bool(errors))
if __name__=='__main__':raise SystemExit(main())
