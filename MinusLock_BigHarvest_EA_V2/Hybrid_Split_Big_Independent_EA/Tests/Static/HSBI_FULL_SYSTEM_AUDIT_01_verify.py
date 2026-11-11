"""Build/capture selected audit evidence and verify package; default read-only.
Package PASS means scope/hash/report consistency, NOT audit complete/system safe.
"""
import sys,subprocess,os,json,re,copy
from pathlib import Path
import HSBI_FULL_SYSTEM_AUDIT_01_common as a
import HSBI_FULL_SYSTEM_AUDIT_01_knowledge as knowledge

def strict(text):
 def pairs(items):
  d={}
  for k,v in items:
   if k in d:raise ValueError('duplicate JSON key '+k)
   d[k]=v
  return d
 return json.loads(text,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))

def static_evidence():
 inv=a.load('INVENTORY');source=(a.ROOT/'Include/Planning/HSBI_NewFarSolver.mqh').read_text()
 rows=[dict(TestID='STATIC-CALL-GRAPH',Actual=dict(MainIncludes=len(inv['MainIncludeClosure']),ProjectFunctions=len(inv['ConservativeReachable']),HasOnTradeTransaction=inv['MainOnTradeTransactionPresent']),Expected=dict(MainIncludes=16,ProjectFunctions=13,HasOnTradeTransaction=False),Scope='Conservative lexical graph plus entrysource, not native runtime'),dict(TestID='STATIC-BOUNDS-DIGEST',Actual='for(int i=0;i<f.maximumDepth;i++)' in source,Expected=True,Scope='Confirmed unguarded loop before downstream FutureSmall validation; OOB execution NOT_RUN'),dict(TestID='STATIC-DOCUMENTATION-MAP',Actual='OPEN_P0=0' in (a.ROOT/'Docs/03_FULL_SYSTEM_MANUAL_RU.md').read_text(),Expected=True,Scope='Historical documentary claim located, not current financial acceptance')]
 for r in rows:r['Result']='PASS' if r['Actual']==r['Expected'] else 'FAIL'
 a.save('STATIC_RESULTS',dict(a.meta(__file__),Rows=rows,StaticEvidenceOnly=True))

def seal():
 old=a.inventory();files=[p for p in a.ROOT.rglob('*') if p.is_file() and p.name.startswith(a.TAG) and '__pycache__' not in str(p)]
 exclude={a.TAG+'PRESERVATION.json',a.TAG+'VERIFICATION.json'}
 production={p:v for p,v in old.items() if p.startswith('Include/') and p.endswith('.mqh') or '/' not in p and p.endswith('.mq5')};assert len(production)==74
 a.save('PRESERVATION',dict(a.meta(__file__),Existing=old,Production=production,HistoricalEvidence={p:v for p,v in old.items() if p.startswith('Tests/Evidence/')},ArtifactHashes={str(p.relative_to(a.ROOT)):a.sha(p) for p in files if p.name not in exclude},SelfHashExcluded=sorted(exclude)))

def verify(override=None):
 errors=[]
 def ck(ok,message):
  if not ok:errors.append(message)
 try:
  pres=override if override is not None else a.load('PRESERVATION');old=a.inventory();ck(pres['Existing']==old,'baseline independent Git inventory/bytes/blob/mode')
  prod={p:v for p,v in old.items() if p.startswith('Include/') and p.endswith('.mqh') or '/' not in p and p.endswith('.mq5')};ck(pres['Production']==prod and len(prod)==74,'production74');ck(pres['HistoricalEvidence']=={p:v for p,v in old.items() if p.startswith('Tests/Evidence/')},'historical evidence')
  new=set()
  for full in subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','--',a.PREFIX],cwd=a.REPO,text=True).splitlines():
   rel=full[len(a.PREFIX):]
   if rel in old:continue
   p=a.ROOT/rel
   if not p.is_file():continue
   ck(p.name.startswith(a.TAG) and rel.startswith(('Docs/','Reports/','Tests/Contracts/','Tests/Reference/','Tests/Static/','Tests/Evidence/')) and p.resolve().is_relative_to(a.ROOT),'scope '+rel);new.add(rel)
  excludes={'Tests/Evidence/'+a.TAG+'PRESERVATION.json','Tests/Evidence/'+a.TAG+'VERIFICATION.json'};ck(new-excludes==set(pres['ArtifactHashes']),'full new-file inventory')
  for p,h in pres['ArtifactHashes'].items():ck(a.sha(a.ROOT/p)==h,'artifact hash '+p)
  required_reports=['PROJECT_INVENTORY','DOCUMENTATION_MAP','ARCHITECTURE','MATHEMATICS','ECONOMIC_MODEL','TRADING_CYCLE','RISK_ANALYSIS','CODE_REVIEW','HISTORICAL_DEFECTS','TEST_COVERAGE','DEFECT_REGISTER','REMEDIATION_ROADMAP','FINAL_VERDICT']
  for s in required_reports:ck((a.ROOT/'Reports'/(a.TAG+s+'_RU.md')).is_file(),'required report '+s)
  for s in ['REQUIREMENT_MATRIX','FORMULA_MATRIX','INVARIANT_MATRIX','STATE_MATRIX']:ck((a.ROOT/'Tests/Contracts'/(a.TAG+s+'.json')).is_file(),'required matrix '+s)
  for s in ['TEST_RESULTS','EXECUTIONS','PRESERVATION','COVERAGE','DEFECTS']:ck((a.ROOT/'Tests/Evidence'/(a.TAG+s+'.json')).is_file(),'required evidence '+s)
  summary=a.load('TEST_RESULTS');coverage=a.load('COVERAGE');ds=a.load('DEFECTS');fm=a.load('FORMULA_MATRIX','Tests/Contracts');iv=a.load('INVARIANT_MATRIX','Tests/Contracts');state=a.load('STATE_MATRIX','Tests/Contracts');ex=a.load('EXTRACTED');ref=a.load('REFERENCE');math=a.load('MATH_TESTS');reg=a.load('REGRESSIONS');execution=a.load('EXECUTIONS')
  ck(summary['AuditCompleteness']=='PARTIAL' and summary['StageComplete'] is False,'honest partial completion');ck(summary['FinalSystemVerdict']=='SYSTEM_CRITICAL_CONTRADICTIONS_FOUND','negative verdict');ck(summary['DefectCounts']==ds['SeverityCounts'] and ds['Rows']==knowledge.defects(),'defect registry consistent')
  ck(fm['Rows']==knowledge.formulas() and len(fm['Rows'])==49 and len(fm['RawSourceExpressionSites'])==137,'formula inventory/scopes');ck(summary['FormulaCounts']==fm['StatusCounts'],'formula counts')
  ck(len(iv['Rows'])==15 and all(x['ModelStatus']=='REFERENCE_EXECUTED_PASS' and x['ProductionSystemStatus']!='VERIFIED' for x in iv['Rows']),'15 abstract invariants not productionPASS')
  ck(len(state['States'])==33 and len(state['Edges'])==1089 and state['ActualEAStates']==['HSBI_STATE_DISABLED'],'state observations')
  ck(ref['ScenarioCount']==ref['ScenarioPass']==20 and ref['ScenarioFail']==0,'20 analytical scenarios');ck(ref['PropertySamplePairs']==ref['PropertyPass']==245 and ref['PropertyFail']==0 and ref['MutationsKilled']==15,'distinct property/mutation counts')
  ck(all(x['OriginalActual']==[True,False] and x['MutantActual']==[True,True] and x['Verdict']=='MUTATION_KILLED' for x in ref['Mutations']),'causal mutation controls')
  ck(math['Pass']==20 and math['Fail']==0,'20 exact spec vectors');ck(len(ex['Rows'])==54 and ex['Pass']==27 and ex['Fail']==27 and ex['InfrastructureError'] is None,'source normative FAIL retained');ck(ex['MQL5_COMPILE']=='NOT_RUN','Cpp not nativeMQL')
  ck(coverage['ProductionModulesIndexedAndStaticallyReviewed']==74 and coverage['ProductionDeclaredFunctions']==199,'source/static review count');ck(reg['Completed'] is True,'regressions completed')
  runs={x['ID']:x for x in reg['Runs']};ck((runs['R7_FROZEN']['ExitCode'],runs['R7_FROZEN']['PassCount'],runs['R7_FROZEN']['FailCount'])==(1,57,5),'R7 FAIL preserved');ck((runs['R0']['ExitCode'],runs['R0']['PassCount'],runs['R0']['FailCount'])==(1,35,46),'R0 FAIL preserved');ck(runs['R8']['ExitCode']==runs['R10']['ExitCode']==1 and runs['R12']['ExitCode']==runs['R12A']['ExitCode']==0,'actual regression exits')
  for name in ('R8','R10'):
   detail=strict(runs[name]['AcceptanceDetail']['Stdout']);ck([f['check'] for f in detail['findings']]==['SCOPE'],'scope-only historical conflict '+name)
  ck(all(r['ActualExitCode']==0 for r in execution['Runs']),'audit process exits')
  for r in execution['Runs']:
   ck(a.sha(a.ROOT/r['Runner'])==r['RunnerHash'],'executed runner hash '+r['Runner'])
  for name in ('REFERENCE','MATH_TESTS','EXTRACTED','REGRESSIONS','R0F_FRESH','NATIVE_ENVIRONMENT'):
   d=a.load(name);runner={'REFERENCE':'reference','MATH_TESTS':'math','EXTRACTED':'extracted','REGRESSIONS':'regressions','R0F_FRESH':'followup','NATIVE_ENVIRONMENT':'followup'}[name];ck(d['RunnerSourceHash']==a.sha(a.ROOT/'Tests/Static'/(a.TAG+runner+'.py')),'artifact runnerhash '+name)
  native=a.load('NATIVE_ENVIRONMENT');ck(native['MQL5_COMPILE']==native['MQL5_NATIVE_TESTS']=='NOT_RUN' and native['CompilerAvailable'] is False,'native NOT_RUN retained')
  import check_hsbi_02b_r0e_package as originalscan
  ck(originalscan.scan(a.ROOT)=={'files':74,'forbidden':[],'controls':True,'guard':True},'static no-trade')
  text=(a.ROOT/'Reports'/(a.TAG+'FINAL_VERDICT_RU.md')).read_text()
  for field in ('ADMIN_APPROVAL_COMPLETE','PRODUCTION_REMEDIATION_ALLOWED','TRADING_LOGIC_START_ALLOWED','BROKER_DISPATCH_ALLOWED','REAL_TRADING_ALLOWED'):
   ck(text.count('\n'+field+'=NO\n')==1 and text.count('\n'+field+'=')==1,'unique NO approval '+field)
  for rel in new:
   p=a.ROOT/rel
   if p.suffix=='.json':strict(p.read_text())
  # Current source/code citations: every registered file exists; line within actual file.
  for d in ds['Rows']:ck((a.ROOT/d['SourceFile']).is_file() and 1<=d['SourceLine']<=len((a.ROOT/d['SourceFile']).read_text().splitlines()),'defect locator '+d['DefectID'])
 except (ValueError,KeyError,TypeError,OSError) as e:errors.append(type(e).__name__+': '+str(e))
 return errors

def all_work():
 started=a.now();runs=[]
 for task in ['common','extracted','reference','math','regressions','followup','build']:
  runner='Tests/Static/'+a.TAG+task+'.py';cmd=[sys.executable,str(a.ROOT/runner)];start=a.now();p=subprocess.run(cmd,cwd=a.ROOT,text=True,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
  runs.append(dict(Runner=runner,RunnerHash=a.sha(a.ROOT/runner),Command=cmd,StartedUtc=start,FinishedUtc=a.now(),TestedSHA=a.BASE,ActualExitCode=p.returncode,Stdout=p.stdout,Stderr=p.stderr));print(task,p.returncode,p.stdout.strip()[:180],flush=True)
  a.save('EXECUTIONS',dict(a.meta(__file__),StartedUtc=started,FinishedUtc=a.now(),Runs=runs,Completed=False,Interpretation='C++/regression orchestrator success does not convert normative/historical failures toPASS; inspect nested results.'))
  if p.returncode:return p.returncode
 static_evidence();a.save('EXECUTIONS',dict(a.meta(__file__),StartedUtc=started,FinishedUtc=a.now(),Runs=runs,Completed=True,Interpretation='Package preparation succeeded, audit remains PARTIAL;54sourcechecks27PASS27FAIL, R7/R0/R8/R10 historicalFAIL retained.'))
 seal();errors=verify();pres=a.load('PRESERVATION');probes=[]
 for kind in ['omitted-baseline','altered-production-hash','altered-artifact-hash','omitted-new-artifact']:
  d=copy.deepcopy(pres)
  if kind=='omitted-baseline':d['Existing'].pop(next(iter(d['Existing'])))
  if kind=='altered-production-hash':d['Production'][next(iter(d['Production']))]['SHA256']='0'*64
  if kind=='altered-artifact-hash':d['ArtifactHashes'][next(iter(d['ArtifactHashes']))]='0'*64
  if kind=='omitted-new-artifact':d['ArtifactHashes'].pop(next(iter(d['ArtifactHashes'])))
  found=verify(d);probes.append(dict(ProbeID=kind,Errors=found,Result='PASS' if found else 'FAIL'))
 for label,text in [('rootduplicate','{"x":0,"x":1}'),('nestedduplicate','{"x":{"a":1,"a":1}}'),('nan','{"x":NaN}'),('infinity','{"x":Infinity}')]:
  try:strict(text);bad=False
  except ValueError:bad=True
  probes.append(dict(ProbeID=label,Result='PASS' if bad else 'FAIL'))
 result=dict(a.meta(__file__),PackagePositive='PASS' if not errors else 'FAIL',Errors=errors,NegativeProbes=probes,PackageExitCode=int(bool(errors) or any(x['Result']!='PASS' for x in probes)),AuditCompleteness='PARTIAL',StageComplete=False,SystemSafetyPass=False,ProductionFilesUnchanged=True,HistoricalEvidenceUnchanged=True,Scope='Integrity/consistency PASS is NOT audit completeness/native/system/trading PASS')
 a.save('VERIFICATION',result);print('PACKAGE',result['PackageExitCode'],errors,flush=True);return result['PackageExitCode']
if __name__=='__main__':
 if '--all' in sys.argv:raise SystemExit(all_work())
 errors=verify();print('PACKAGE',errors);raise SystemExit(int(bool(errors)))
