"""Independent inventory, strict JSON/schema, semantic and baseline checks. Read-only default."""
import sys,re,json,hashlib,subprocess,difflib,tempfile,shutil
from pathlib import Path
from jsonschema import Draft202012Validator
import HSBI_DG01_common as a
from HSBI_DG01_schemas import schemas
REQ_DOCS=['CONTRACT_RESOLUTION','P0_REMEDIATION_MATRIX','MINIMAL_R1_1_DIFF_PLAN','NATIVE_VERIFICATION_PLAN','DEPENDENCY_GRAPH']
REQ_REPORTS=['FINAL_VERDICT','ADMIN_DECISION_BALLOT','R1_1_APPROVAL_GATE','P0_REVERIFICATION_FORMATTED','P1_P2_REVIEW_FORMATTED','MATH_PROOF_GAPS_FORMATTED']
REQ_JSON=['BASELINE','PRESERVATION','TEST_RESULTS','NATIVE_RESULTS','PACKAGE_RESULTS','FINAL_INTEGRITY']
CANONICAL={'D-%02d'%i for i in range(1,9)}|{'CR-09','NUM-EXACT-1','NUM-DOMAIN-1','NUM-CODEC','SNAP-FIXTURE-1','FUNDING-GLOBAL-ATTRIBUTION','MQL-DOMAIN','BALANCE-SCHEMA-MAPPING'}
REQUIRED_MUTATIONS={'M-AUTH','M-VECTOR','M-SCOPE','M-REV','M-HISTORY','M-ACCOUNT'}
def ep(n):return 'Tests/Evidence/'+a.TAG+n+'.json'
def cp(n):return 'Tests/Contracts/'+a.TAG+n+'.json'
def required_ref_ids(root):
 source=(root/'Tests/Static/HSBI_DG01_reference_tests.py').read_text()
 names={v for v in re.findall(r"case\('([^']+)'",source) if not v.endswith('-')}
 return names|{'L18-SCOPE-'+str(i) for i in range(3)}|{'L26-EVENT-'+str(i) for i in range(8)}|{'L27-AMOUNT-'+str(i) for i in range(6)}
def check(root,baseline=True,manifest=True,package_result=True):
 errors=[]
 def req(ok,msg):
  if not ok:errors.append(msg)
 try:
  for n in REQ_DOCS:req((root/'Docs'/(a.TAG+n+'_RU.md')).is_file(),'missing doc '+n)
  for n in REQ_REPORTS:req((root/'Reports'/(a.TAG+n+'_RU.md')).is_file(),'missing report '+n)
  for n in ['DECISION_MATRIX','P0_REMEDIATION_MATRIX','ACCEPTANCE_MATRIX','JSON_SCHEMAS']:req((root/cp(n)).is_file(),'missing required contract '+n)
  for n in REQ_JSON:
   if not package_result and n=='PACKAGE_RESULTS' or not manifest and n=='FINAL_INTEGRITY':continue
   req((root/ep(n)).is_file(),'missing evidence '+n)
  if errors:return errors
  graph={str(p.relative_to(root)):a.strict(p) for p in root.rglob(a.TAG+'*.json') if p.is_file()}
  declared=graph[cp('JSON_SCHEMAS')]['Schemas'];expected=schemas();req(declared==expected,'independent schema catalog differs')
  for name,data in graph.items():
   req(name in expected,'unregistered JSON schema '+name)
   if name in expected:
    Draft202012Validator.check_schema(expected[name]);validation=list(Draft202012Validator(expected[name]).iter_errors(data));req(not validation,'schema '+name+': '+('; '.join(str(e.message) for e in validation[:2])))
  if errors:return errors
  if manifest:
   rows=graph[ep('FINAL_INTEGRITY')]['Artifacts'];expectedpaths={str(p.relative_to(root)) for p in root.rglob(a.TAG+'*') if p.is_file() and '__pycache__' not in str(p) and p.name not in (a.TAG+'FINAL_INTEGRITY.json',a.TAG+'PACKAGE_RESULTS.json')}
   req({x['Path'] for x in rows}==expectedpaths and len(rows)==len(expectedpaths),'artifact inventory')
   for x in rows:req(a.sha(root/x['Path'])==x['SHA256'] and (root/x['Path']).stat().st_size==x['Size'],'artifact hash '+x['Path'])
  d=graph[cp('DECISION_MATRIX')]['Rows'];req(len(d)==16 and {x['DecisionID'] for x in d}==CANONICAL,'16 canonical decisions')
  req({x['DisplayOrdinal'] for x in d}=={'D-%02d'%i for i in range(1,17)},'display mapping')
  plans=graph[cp('P0_REMEDIATION_MATRIX')]['Rows'];req(len(plans)==10 and {x['DefectID'] for x in plans}=={'FSA-%03d'%i for i in range(1,11)},'10 P0 plans')
  old=a.strict(root/'Tests/Contracts/HSBI_FULL_SYSTEM_AUDIT_02_DEFECT_MATRIX.json')['Rows'];issues=graph[cp('ACCEPTANCE_MATRIX')]['Rows'];req(len(issues)==29 and {x['DefectID'] for x in issues}=={x['ID'] for x in old},'29 defect inventory')
  for x in issues:
   orig=next(z for z in old if z['ID']==x['DefectID']);req(x['Classification']==orig['Classification'],'unauthorized classification change '+x['DefectID']);req(a.sha(root/x['Source']['File'])==x['Source']['SHA256'],'source hash '+x['DefectID'])
  formulas=a.strict(root/'Tests/Contracts/HSBI_FULL_SYSTEM_AUDIT_02_FORMULA_REVIEW.json')['Rows'];req(len(formulas)==49,'49 formula inventory')
  # Exact reverse transformation: no semantic rewording allowed in three requested representations.
  for x in graph[ep('FORMATTING_RESULTS')]['Rows']:
   src=(root/x['Source']).read_text();out=(root/x['Output']).read_text();req(out==src.replace('\\n','\n'),'formatted content '+x['Output']);back=out
   for pos in reversed(x['OutputCharacterOffsets']):back=back[:pos]+'\\n'+back[pos+1:]
   req(back==src and a.sha(root/x['Source'])==x['SourceSHA256'] and a.sha(root/x['Output'])==x['OutputSHA256'],'format provenance '+x['Output'])
  tests=graph[ep('TEST_RESULTS')];rows=tests['Rows'];req(len(rows)==62 and {x['TestID'] for x in rows}==required_ref_ids(root),'required reference cases')
  req(tests['Pass']==sum(x['Status']=='PASS' for x in rows) and tests['Fail']==sum(x['Status']=='FAIL' for x in rows) and tests['InfrastructureErrors']==sum(x['Status']=='INFRASTRUCTURE_ERROR' for x in rows),'reference totals')
  for x in rows:
   req(x['SubjectSHA256']==a.sha(root/'Tests/Reference/HSBI_DG01_ledger.py') and x['RunnerSHA256']==a.sha(root/'Tests/Static/HSBI_DG01_reference_tests.py'),'reference provenance '+x['TestID'])
   e=x['Expected'];v=x['Actual'];good=v['Status']==e['Status'] and (e['Balance'] is None or v['Balance']==e['Balance']) and (e['Revision'] is None or v['Revision']==e['Revision']) and (not e['ZeroDelta'] or v['StateUnchanged']) and v['InputUnchanged']
   req(x['Status']==('INFRASTRUCTURE_ERROR' if x['Error'] else 'PASS' if good else 'FAIL'),'reference verdict '+x['TestID'])
  req(tests['Fail']==tests['InfrastructureErrors']==0 and tests['FormattingPass']==3,'final reference failure')
  native=graph[ep('NATIVE_RESULTS')];ids=[x['TestID'] for x in native['Rows']];req(len(ids)==len(set(ids))==native['CaseCount'] and set(ids)==set(graph[cp('ACCEPTANCE_MATRIX')]['NativeRequiredIDs']),'native inventory')
  native_source='\n'.join(p.read_text() for p in (root/'Tests/Native').glob('HSBI_DG01_*.mq*'))
  source_ids={v for v in re.findall(r'DGCheck\("([^"\n]+)"',native_source) if v!='E1-FIELD-'}
  fields=['SchemaVersion','Broker','Server','AccountLogin','Symbol','Magic','CycleID','DealTicket','OrderTicket','PositionIdentifier','ActionID','EventID','Role','EntryType','DealType','TimestampMsc','Volume','Price','Profit','Swap','Commission','Fee','DealNet','Currency','Precision','SourcePlanApplicable','SourcePlan','SourcePolicyApplicable','SourcePolicyVersion']
  source_ids|={'E1-FIELD-'+name for name in fields}
  source_ids|={'E5-'+name+suffix for name in ['zero','negative-zero','one','negative-five','tenth','min-normal','min-subnormal','max-finite'] for suffix in ['-bits','-roundtrip','-T17-probe']}
  req(set(ids)==source_ids and len(ids)==113,'native source/case completeness')
  required_native={'E1-EXACT','E1-SAME-NET','E1-NONFINITE','E2-FOREIGN-ALLOCATION','E2-ALREADY-CONSUMED','E3-NAN-MARGIN','E3-NAN-FILL','E4-DISTINCT-FAR-SLOTS','E4-INDEPENDENT-EXPECTED','E4-COPIED-EXPECTED','E4-MISSING-PROVIDER','E5-GOLDEN-RECORD','E5-min-subnormal-bits','E5-max-finite-bits','E5-UTF8-LENGTH','E5-ULONG-NO-DOUBLE'}
  req(required_native<=set(ids),'native required groups')
  for x in native['Rows']:
   for file,h in x['SubjectSHA256'].items():req(a.sha(root/file)==h,'native source hash '+file)
   req(x['RunnerSHA256']==a.sha(root/'Tests/Native/HSBI_DG01_harness.mq5'),'native runner hash')
  mutations=graph[ep('MUTATION_RESULTS')];req(len(mutations['Rows'])==6 and {x['MutationID'] for x in mutations['Rows']}==REQUIRED_MUTATIONS,'mutation catalog')
  for x in mutations['Rows']:
   req(x['OriginalSourceSHA256']==a.sha(root/'Tests/Reference/HSBI_DG01_ledger.py') and x['RunnerSHA256']==a.sha(root/'Tests/Static/HSBI_DG01_mutations.py'),'mutation provenance '+x['MutationID'])
   req(x['OriginalPositive']==x['MutantPositive']=='FUNDED_IN_MEMORY' and x['OriginalCausal']['Status']==x['Expected'] and x['MutantCausal']['Status']!=x['Expected'] and x['Status'] in ('UNSAFE_ACCEPTANCE_KILL','STATUS_CONTRACT_KILL'),'mutation causality '+x['MutationID'])
  req(mutations['Killed']==6 and mutations['Survived']==mutations['InfrastructureErrors']==0,'mutation totals')
  for x in graph[ep('DEVELOPMENT_SOURCES')]['Files']:req(hashlib.sha256(x['Text'].encode()).hexdigest()==x['SHA256'],'development archived source hash')
  # Unapplied patch must be exactly append-only V2 body, not a hidden legacy rewrite.
  f='Include/Money/HSBI_EconomicLedgerTypes.mqh';oldtext=(root/f).read_text();candidate=(root/'Tests/Reference/HSBI_DG01_identity_candidate.mqh').read_text();body=candidate[candidate.index('enum HSBI_EconomicIdentityStatusV2'):candidate.rindex('#endif')]
  proposal=oldtext[:oldtext.rindex('#endif')]+'\n// PROPOSED DG01 additive V2; admin approval and native validation required.\n'+body+'#endif\n';full=(a.ROOT.relative_to(a.REPO)/f).as_posix();patch=''.join(difflib.unified_diff(oldtext.splitlines(True),proposal.splitlines(True),fromfile='a/'+full,tofile='b/'+full))
  req((root/'Tests/Reference/HSBI_DG01_MINIMAL_R1_1_CANDIDATE.patch').read_text()==patch,'one-file exact unapplied patch')
  req(graph[ep('DIFF_CHECK')]['ExitCode']==0 and graph[ep('DIFF_CHECK')]['BaseSHA256']==a.sha(root/f),'patch check provenance')
  for folder,names in [('Docs',REQ_DOCS),('Reports',REQ_REPORTS)]:
   for n in names:
    text=(root/folder/(a.TAG+n+'_RU.md')).read_text();req(text.startswith('# ') and text.count('```')%2==0,'markdown structure '+n)
  final=(root/'Reports/HSBI_DG01_FINAL_VERDICT_RU.md').read_text()
  for key in ['ADMIN_APPROVAL_COMPLETE','R1_1_START_ALLOWED','PRODUCTION_REMEDIATION_ALLOWED','TRADING_LOGIC_START_ALLOWED','BROKER_DISPATCH_ALLOWED','REAL_TRADING_ALLOWED']:req(re.findall(r'^'+key+'=(.*)$',final,re.M)==['NO'],'policy uniqueness '+key)
  ps=(root/'Tests/Native/HSBI_DG01_compile_isolated.ps1').read_text();req('-FilePath $MetaEditorPath' in ps and '-FilePath $TerminalPath' not in ps and '$created -and' in ps and 'NativeRuntimeStatus=\'NOT_RUN\'' in ps,'compile-only launcher static boundary')
  if baseline:
   req(graph[ep('PRESERVATION')]['Files']==a.inventory(),'baseline preservation')
   prefix=a.ROOT.relative_to(a.REPO).as_posix()+'/'
   for line in subprocess.check_output(['git','diff','--name-status',a.BASE],cwd=a.REPO,text=True).splitlines():
    status,path=line.split('\t',1);req(status=='A' and path.startswith(prefix) and Path(path).name.startswith(a.TAG),'tracked scope '+line);req(path[len(prefix):].startswith(('Docs/','Reports/','Tests/')),'tracked folder scope '+path)
   for path in subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=a.REPO,text=True).splitlines():
    req(path.startswith(prefix) and Path(path).name.startswith(a.TAG) and path[len(prefix):].startswith(('Docs/','Reports/','Tests/')),'untracked scope '+path)
    req(not (a.REPO/path).is_symlink(),'untracked symlink '+path)
 except Exception as e:errors.append('PACKAGE_ERROR '+type(e).__name__+': '+str(e))
 return errors

def seal():
 rows=[]
 for p in sorted(a.ROOT.rglob(a.TAG+'*')):
  if p.is_file() and '__pycache__' not in str(p) and p.name not in (a.TAG+'FINAL_INTEGRITY.json',a.TAG+'PACKAGE_RESULTS.json'):rows.append(dict(Path=str(p.relative_to(a.ROOT)),SHA256=a.sha(p),Size=p.stat().st_size))
 a.save('FINAL_INTEGRITY',dict(BaseSHA=a.BASE,UTC=a.now(),Artifacts=rows,IndependentInventoryVersion=1,Exclusions=['FINAL_INTEGRITY itself: no self-referential hash','PACKAGE_RESULTS: independently recomputed by checker/probes'],Scope='Preparation/native-pending package integrity only; no system/trading approval'))
def probes():
 rows=[]
 edits=[('COUNTER-BOOL','TEST_RESULTS',lambda x:x.update(Pass=True)),('COHERENT-TEST-DELETION','TEST_RESULTS',lambda x:(x['Rows'].pop(),x.update(Pass=x['Pass']-1))),('UNAUTHORIZED-APPROVAL','DECISION_MATRIX',lambda x:x['Rows'][0].update(ApprovalStatus='APPROVED')),('NATIVE-FALSE-PASS','NATIVE_RESULTS',lambda x:x['Rows'][0].update(Status='PASS',Actual=True)),('FALSE-SOURCE-HASH','TEST_RESULTS',lambda x:x['Rows'][0].update(SubjectSHA256='0'*64)),('EMPTY-MUTATIONS','MUTATION_RESULTS',lambda x:x.update(Rows=[],Killed=0))]
 with tempfile.TemporaryDirectory(prefix='HSBI_DG01_disposable_',dir=a.ROOT/'Tests') as td:
  root=Path(td)/'project';shutil.copytree(a.ROOT,root,ignore=shutil.ignore_patterns('__pycache__','.bin','HSBI_DG01_disposable_*'))
  original=(root/ep('FINAL_INTEGRITY')).read_bytes()
  def refresh(path):
   m=a.strict(root/ep('FINAL_INTEGRITY'))
   for row in m['Artifacts']:
    if row['Path']==str(path.relative_to(root)):row['SHA256']=a.sha(path);row['Size']=path.stat().st_size
   (root/ep('FINAL_INTEGRITY')).write_text(json.dumps(m))
  for name,target,edit in edits:
   path=root/(cp(target) if target=='DECISION_MATRIX' else ep(target));old=path.read_bytes();x=a.strict(path);edit(x);path.write_text(json.dumps(x));refresh(path);errors=check(root,False,package_result=False);rows.append(dict(ProbeID=name,Status='PASS' if errors else 'FAIL',Errors=errors));path.write_bytes(old);(root/ep('FINAL_INTEGRITY')).write_bytes(original)
  for name,text in [('DUPLICATE-JSON','{"x":0,"x":1}'),('NONFINITE-JSON','{"x":NaN}')]:
   p=root/ep('INVALID');p.write_text(text);errors=check(root,False,package_result=False);rows.append(dict(ProbeID=name,Status='PASS' if any('ValueError' in e for e in errors) else 'FAIL',Errors=errors));p.unlink()
  p=root/'Reports/HSBI_DG01_P0_REVERIFICATION_FORMATTED_RU.md';old=p.read_bytes();p.write_text(p.read_text().replace('FSA-001','FSA-999',1));refresh(p);errors=check(root,False,package_result=False);rows.append(dict(ProbeID='SEMANTIC-FORMAT-CHANGE',Status='PASS' if errors else 'FAIL',Errors=errors));p.write_bytes(old);(root/ep('FINAL_INTEGRITY')).write_bytes(original)
  p=root/'Reports/HSBI_DG01_FINAL_VERDICT_RU.md';old=p.read_bytes();p.write_text(p.read_text()+'\nBROKER_DISPATCH_ALLOWED=YES\n');refresh(p);errors=check(root,False,package_result=False);rows.append(dict(ProbeID='CONTRADICTORY-POLICY',Status='PASS' if errors else 'FAIL',Errors=errors));p.write_bytes(old);(root/ep('FINAL_INTEGRITY')).write_bytes(original)
  p=root/'Tests/Contracts/HSBI_DG01_P0_REMEDIATION_MATRIX.json';p.unlink();errors=check(root,False,package_result=False);rows.append(dict(ProbeID='MISSING-P0-MATRIX',Status='PASS' if errors else 'FAIL',Errors=errors))
 a.save('PACKAGE_RESULTS',dict(UTC=a.now(),PositiveErrors=check(a.ROOT,package_result=False),NegativeProbes=rows,Pass=sum(x['Status']=='PASS' for x in rows),Fail=sum(x['Status']=='FAIL' for x in rows),RunnerSHA256=a.sha(__file__),Boundary='11 disposable semantic/schema/integrity probes. No exhaustive checker proof; no native compilation.'))
 print('DG01 PACKAGE PROBES',len(rows),sum(x['Status']=='PASS' for x in rows));return int(any(x['Status']!='PASS' for x in rows) or bool(check(a.ROOT)))
if __name__=='__main__':
 if '--seal' in sys.argv:seal()
 if '--probes' in sys.argv:raise SystemExit(probes())
 e=check(a.ROOT,package_result='--seal' not in sys.argv);print('DG01 PACKAGE',e);raise SystemExit(bool(e))
