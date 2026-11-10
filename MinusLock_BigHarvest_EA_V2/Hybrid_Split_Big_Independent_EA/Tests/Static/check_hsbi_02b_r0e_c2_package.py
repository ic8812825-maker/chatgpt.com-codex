#!/usr/bin/env python3
"""Trusted C2 verifier: independent Git baseline + executable required inventory + strict evidence."""
import argparse,ast,copy,hashlib,json,re,shutil,stat,subprocess,sys,tempfile
from pathlib import Path
import check_hsbi_02b_r0e_c2_contracts as t
import check_hsbi_02b_r0e_c2_mutations as mu
import build_hsbi_02b_r0e_c2_catalog as catalog
import check_hsbi_02b_r0e_package as historical
ROOT=t.ROOT;REPO=ROOT.parents[1];PREFIX=ROOT.relative_to(REPO).as_posix()+'/';BASE=t.BASE
VERIFIER_SOURCE_HASH=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
PRES='Tests/Evidence/NEXT_STAGE_02B_R0E_C2_PRESERVATION.json'
RESULT='Tests/Evidence/NEXT_STAGE_02B_R0E_C2_PACKAGE_RESULTS.json'
TEST='Tests/Evidence/NEXT_STAGE_02B_R0E_C2_TEST_RESULTS.json'
MUT='Tests/Evidence/NEXT_STAGE_02B_R0E_C2_MUTATION_RESULTS.json'
REG='Tests/Evidence/NEXT_STAGE_02B_R0E_C2_REGRESSIONS.json'
REPRO='Tests/Evidence/NEXT_STAGE_02B_R0E_C2_REPRODUCTION.json'
SHEET='Reports/NEXT_STAGE_02B_R0E_C2_ADMIN_ADDENDUM_RU.md'
VERDICT='Reports/NEXT_STAGE_02B_R0E_C2_FINAL_VERDICT_RU.md'
DECISIONS=historical.DECISIONS
POLICY={'ADMIN_APPROVAL_COMPLETE':'NO','PRODUCTION_REMEDIATION_ALLOWED':'NO','TRADING_LOGIC_START_ALLOWED':'NO','BROKER_DISPATCH_ALLOWED':'NO','REAL_TRADING_ALLOWED':'NO','STAGE_02B_R0E_C2_COMPLETE':'YES','CONTRACT_FREEZE_CANDIDATE_READY':'YES'}
MANDATORY=[catalog.SCHEMAS,'Tests/Reference/hsbi_02b_r0e_c2_schemas.py','Tests/Reference/hsbi_02b_r0e_c2_evidence.py',PRES,RESULT,TEST,MUT,REG,REPRO,catalog.CATALOG,catalog.MATRIX,SHEET,VERDICT,mu.TARGET]+[f'Docs/NEXT_STAGE_02B_R0E_C2_{s}_RU.md' for s in ('DTO_SCHEMA_CONTRACT','GUARD_COVERAGE_AND_RECOVERY_SCOPE')]+[f'Reports/NEXT_STAGE_02B_R0E_C2_{s}_RU.md' for s in ('REPRODUCTION','TEST_AND_MUTATION_RESULTS')]+[f'Tests/Static/{s}.py' for s in ('check_hsbi_02b_r0e_c2_contracts','check_hsbi_02b_r0e_c2_mutations','check_hsbi_02b_r0e_c2_package','run_hsbi_02b_r0e_c2_regressions','check_hsbi_02b_r0e_c2_reproduction','build_hsbi_02b_r0e_c2_catalog')]
LEGACY_PROBES=('inventory-omission','historical-content','outside-scope','source-hash','test-total','fail-with-pass-total','mandatory-missing','report-baseline','empty-cases','missing-case','duplicate-case','context-999','context-bool','context-missing','context-duplicate','context-metadata','original-hash','mutant-hash','exact-edit','approval-inline','approval-newline','approval-duplicate','verdict-policy')
NEW_PROBES=('empty-mutation-catalog','missing-mutation','unknown-mutation','duplicate-mutation','missing-test-coherent-totals','approval-status-contradiction','approval-status-duplicate','admin-policy-conflict','dispatch-policy-conflict','regression-source-hash','reproduction-source-hash','matrix-function','matrix-mutation-dangling','catalog-version','catalog-inventory','catalog-source-pin','mutation-wrong-function','test-missing-source-pin','status-wrong-section','historical-mode','status-field-case','verifier-source-identity','counter-type','json-root','json-nested','json-reverse','json-same','json-regression','json-manifest','json-hash-map','json-nan','json-infinity','json-counter-bool','schema-probe-missing','clause-mapping')
PROBE_IDS=LEGACY_PROBES+NEW_PROBES

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(root,p):return t.subject.evidence.loads((root/p).read_text())
def save(root,p,d):(root/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def files(root):return {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
def git_tree(repo=REPO):
 out={}
 for row in subprocess.check_output(['git','ls-tree','-rz',BASE,'--',PREFIX],cwd=repo).split(b'\0'):
  if row:
   meta,path=row.split(b'\t');mode,kind,oid=meta.decode().split()
   if kind!='blob' or mode not in ('100644','100755'):raise ValueError('unsupported Git entry')
   out[path.decode()[len(PREFIX):]]=dict(mode=mode,gitBlob=oid)
 return out

def seal():
 old=git_tree();actual=files(ROOT);additions=actual-set(old)
 proof=dict(BaseSHA=BASE,UTC=t.now(),Existing={p:dict(**v,sha256=sha(ROOT/p)) for p,v in old.items()},Production={p:sha(ROOT/p) for p in old if p.startswith('Include/') and p.endswith('.mqh') or '/' not in p and p.endswith('.mq5')},NewFiles=sorted(additions),ArtifactHashes={p:sha(ROOT/p) for p in sorted(additions) if p not in (PRES,RESULT)},SelfHashExclusions={PRES:'Self-reference; inventory and all baseline bytes independently validated',RESULT:'Own final run report semantically validated; no impossible self hash'},NoTrade=historical.scan(ROOT),NativeTools={n:shutil.which(n) for n in ('metaeditor64','terminal64','wine')},DevelopmentEvidence='Tests/Evidence/NEXT_STAGE_02B_R0E_C2_DEVELOPMENT.json is retained nonfinal prototype evidence; not consumed as current execution PASS')
 save(ROOT,PRES,proof)

def verify(root=ROOT,repo=REPO,check_results=True):
 errors=[]
 def fail(code,path=''):errors.append(dict(Code=code,Path=path))
 def safe(path):
  if type(path) is not str or Path(path).is_absolute() or '..' in Path(path).parts or not (root/path).resolve().is_relative_to(root.resolve()):fail('UNSAFE_PATH',str(path));return None
  return root/path
 def provenance(d,required,label):
  pins=d.get('SourceHashes')
  if type(pins) is not dict or not pins or not set(required)<=set(pins):fail('PROVENANCE_INVENTORY',label);return
  for path,h in pins.items():
   p=safe(path)
   if p is None:continue
   if type(h) is not str or not re.fullmatch('[0-9a-f]{64}',h) or not p.is_file() or p.is_symlink() or sha(p)!=h:fail('SOURCE_HASH',label+':'+path)
  if d.get('BaseSHA',BASE)!=BASE or d.get('TestedSHA')!=BASE:fail('EXECUTION_SHA',label)
  if not d.get('Command') or not d.get('StartedUtc') or not d.get('FinishedUtc'):fail('EXECUTION_METADATA',label)
 try:
  old=git_tree(repo);pres=load(root,PRES)
  if sha(root/'Tests/Static/check_hsbi_02b_r0e_c2_package.py')!=VERIFIER_SOURCE_HASH:fail('VERIFIER_SOURCE')
  if pres.get('BaseSHA')!=BASE or set(pres.get('Existing',{}))!=set(old):fail('BASELINE_INVENTORY')
  for path,entry in old.items():
   p=safe(path)
   if p is None:continue
   if not p.is_file() or p.is_symlink():fail('HISTORICAL_MISSING',path);continue
   b=p.read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();row=pres['Existing'].get(path,{})
   if blob!=entry['gitBlob'] or row.get('gitBlob')!=entry['gitBlob'] or row.get('mode')!=entry['mode'] or row.get('sha256')!=sha(p):fail('HISTORICAL_BYTES',path)
   if bool(p.stat().st_mode & 0o111)!=(entry['mode']=='100755'):fail('HISTORICAL_MODE',path)
  prod={p for p in old if p.startswith('Include/') and p.endswith('.mqh') or '/' not in p and p.endswith('.mq5')}
  if len(prod)!=74 or set(pres.get('Production',{}))!=prod or any(pres['Production'].get(p)!=sha(root/p) for p in prod):fail('PRODUCTION_HASHES')
  added=files(root)-set(old)
  if added!=set(pres.get('NewFiles',[])) or len(pres.get('NewFiles',[]))!=len(added):fail('NEW_INVENTORY')
  if any(p.split('/')[0] not in ('Docs','Reports','Tests') or 'r0e_c2' not in Path(p).name.lower() or (root/p).is_symlink() for p in added):fail('OUTSIDE_SCOPE')
  if set(pres.get('ArtifactHashes',{}))!=added-{PRES,RESULT}:fail('ARTIFACT_HASH_INVENTORY')
  for path,h in pres['ArtifactHashes'].items():
   p=safe(path)
   if p is not None and (not p.is_file() or sha(p)!=h):fail('ARTIFACT_HASH',path)
  for path in MANDATORY:
   if path not in added or not (root/path).is_file() or not (root/path).stat().st_size:fail('MANDATORY_ARTIFACT',path)
  if root.resolve()==ROOT.resolve():
   changed=subprocess.check_output(['git','diff','--name-only',BASE],cwd=repo,text=True).splitlines()+subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=repo,text=True).splitlines()
   if any(not p.startswith(PREFIX) for p in changed):fail('REPOSITORY_SCOPE')
  if historical.scan(root)!=dict(files=74,forbidden=[],controls=True,guard=True) or pres['NoTrade']!=historical.scan(root):fail('NO_TRADE')
  for path in added:
   if path.endswith('.json'):load(root,path)
   if path.endswith('.md') and re.findall(r'^BASE_SHA=(\S+)$',(root/path).read_text(),re.M)!=[BASE]:fail('REPORT_BASELINE',path)
  cat=load(root,catalog.CATALOG);expected=catalog.expected_catalog();matrix=load(root,catalog.MATRIX)
  if not t.equal(cat,expected):fail('REQUIRED_CATALOG')
  if not t.equal(matrix,catalog.expected_matrix(expected)):fail('MATRIX_TRACEABILITY')
  tests=load(root,TEST);mut=load(root,MUT);repro=load(root,REPRO);reg=load(root,REG)
  # All current executable evidence roles have their own nonempty hash inventory.
  provenance(tests,t.hashes(),'reference')
  provenance(mut,{**t.hashes(),str(Path(mu.__file__).relative_to(ROOT)):''},'mutations')
  provenance(repro,('Tests/Static/check_hsbi_02b_r0e_c2_reproduction.py','Tests/Static/check_hsbi_02b_r0e_c1_contracts.py','Tests/Reference/hsbi_02b_r0e_c1_contract_model.py','Tests/Static/check_hsbi_02b_r0e_c1_package.py','Tests/Static/check_hsbi_02b_r0e_c1_mutations.py'),'reproduction')
  provenance(reg,{**t.hashes(),'Tests/Static/run_hsbi_02b_r0e_c2_regressions.py':''},'regressions')
  if any(type(tests[k]) is not int or tests[k]<0 for k in ('Scenarios','Executions','Comparisons','Pass','Fail','InfrastructureErrors','ExitCode')):fail('TEST_TOTALS')
  if any(type(mut[k]) is not int or mut[k]<0 for k in ('CatalogSize','Killed','RedundantSurvivors','UnexplainedSurvivors','InfrastructureErrors','ExitCode')):fail('MUTATION_TOTALS')
  ids=expected['RequiredTestIDs'];rows=tests['Rows'];configs=tests['ContextConfigurations'];realconfigs=t.view([t.wire.context_state(c) for c in t.wire.contexts()])
  if not t.equal(configs,realconfigs):fail('CONTEXT_METADATA')
  pairs=[(r['TestID'],r['ContextID']) for r in rows]
  if any(type(r['ContextID']) is not int for r in rows) or set(pairs)!={(i,c) for i in ids for c in range(len(realconfigs))} or len(pairs)!=len(set(pairs)):fail('TEST_CONTEXT_INVENTORY')
  if tests['Scenarios']!=len(ids) or tests['Executions']!=len(rows) or tests['Comparisons']!=2*len(rows)+3*len(tests['SchemaRows']) or any(r['Comparisons']!=2 for r in rows):fail('TEST_TOTALS')
  for field,value in [('Pass','PASS'),('Fail','FAIL'),('InfrastructureErrors','INFRASTRUCTURE_ERROR')]:
   if tests[field]!=(sum(r['Result']==value for r in rows) + (sum(r['Result']==value for r in tests['SchemaRows']) if field!='Pass' else 0)):fail('TEST_TOTALS')
  schemarows=tests['SchemaRows'];sids=[r['TestID'] for r in schemarows]
  if sids!=expected['RequiredSchemaProbeIDs'] or tests['SchemaProbes']!=len(sids):fail('SCHEMA_INVENTORY')
  if load(root,catalog.SCHEMAS)!=t.schema.inventory():fail('SCHEMA_CONTRACT')
  for r,spec in zip(schemarows,t.schema_specs()):
   if r.get('Result')!='PASS' or r.get('Actual')!=spec['Expected'] or r.get('IndependentExpected')!=spec['Expected'] or r.get('ZeroDelta') is not True or r.get('InputsUnchanged') is not True or r.get('Path')!=list(spec['Path']) or r.get('Change')!=spec['Change']:fail('SCHEMA_RESULT')
  known={x['TestID']:x for x in expected['Tests']}
  for r in rows:
   spec=known.get(r['TestID'])
   if spec is None:fail('UNKNOWN_TEST');continue
   if r.get('Operation')!=spec['Operation'] or not t.equal(r.get('IndependentExpected'),spec['IndependentExpected']) or not t.equal(r.get('Actual'),spec['IndependentExpected']) or r.get('Result')!='PASS' or r.get('ContextUnchanged') is not True:fail('TEST_VERDICT',r['TestID'])
   if spec['Operation'] not in r.get('SubjectCalls',[]):fail('DYNAMIC_TRACEABILITY',r['TestID'])
   if r['ContextID']==0 and not r.get('Input',{}).get('Calls'):fail('INPUT_TRACE',r['TestID'])
  if tests['ExitCode']!=0 or tests['Fail'] or tests['InfrastructureErrors']:fail('TEST_VERDICT')
  mids=[r['MutationID'] for r in mut['Rows']]
  if set(mids)!=set(expected['RequiredMutationIDs']) or len(mids)!=len(set(mids)) or mut['CatalogSize']!=len(mids):fail('MUTATION_INVENTORY')
  defs={m['MutationID']:m for m in expected['Mutations']}
  for r in mut['Rows']:
   spec=defs.get(r['MutationID'])
   if spec is None:fail('UNKNOWN_MUTATION');continue
   for field in ('TargetFile','TargetFunction','PositiveTestID','NegativeTestID','ExactEdit'):
    if not t.equal(r.get(field),spec[field]):fail('MUTATION_SPEC',r['MutationID']+':'+field)
   source=(root/spec['TargetFile']).read_text()
   if r['OriginalSourceHash']!=hashlib.sha256(source.encode()).hexdigest():fail('ORIGINAL_SOURCE_HASH')
   for e in spec['ExactEdit']:
    if source.count(e['old'])!=1:fail('EXACT_EDIT')
    source=source.replace(e['old'],e['new'])
   ast.parse(source)
   if r['MutantSourceHash']!=hashlib.sha256(source.encode()).hexdigest():fail('MUTANT_SOURCE_HASH')
   pe=known[spec['PositiveTestID']]['IndependentExpected'];ne=known[spec['NegativeTestID']]['IndependentExpected']
   if not t.equal(r.get('PositiveExpected'),pe) or not t.equal(r.get('IndependentExpected'),ne) or not t.equal(r.get('OriginalPositive'),pe) or not t.equal(r.get('MutantPositive'),pe) or not t.equal(r.get('OriginalNegative'),ne) or r.get('ControlsPass') is not True:fail('MUTATION_CONTROLS')
   if r['Verdict'] not in (['UNSAFE_ACCEPTANCE_KILL','STATUS_CONTRACT_KILL'] if spec['ExpectedVerdict']=='KILL' else [spec['ExpectedVerdict']]):fail('MUTATION_VERDICT')
   if spec['ExpectedVerdict']=='REDUNDANT_GUARD_SURVIVOR':
    d=r.get('DomainRegression',{})
    if r.get('RedundancyProof')!=spec['RedundancyProof'] or not t.equal(r.get('MutantNegative'),ne) or d.get('Pass')!=len(ids)*8 or d.get('Fail') or d.get('InfrastructureErrors'):fail('REDUNDANCY_PROOF')
   elif t.equal(r.get('MutantNegative'),ne):fail('MUTATION_CAUSALITY')
  if mut['Killed']!=sum(r['Verdict'] in ('UNSAFE_ACCEPTANCE_KILL','STATUS_CONTRACT_KILL') for r in mut['Rows']) or mut['RedundantSurvivors']!=sum(r['Verdict']=='REDUNDANT_GUARD_SURVIVOR' for r in mut['Rows']) or mut['UnexplainedSurvivors'] or mut['InfrastructureErrors'] or mut['ExitCode']:fail('MUTATION_TOTALS')
  # Frozen C1 results remain a separate execution role, not merged into C2 totals.
  if repro['StockReference']['Pass']!=840 or repro['StockMutations']['Killed']!=54 or repro['StockMutations']['RedundantSurvivors']!=1 or repro['StockPackage']['NegativePassed']!=46 or len(repro['SixAdditionalMutations'])!=6 or any(r['Classification']!='CONFIRMED' for r in repro['SixAdditionalMutations']):fail('REPRODUCTION')
  baseline=load(root,'Tests/Evidence/NEXT_STAGE_02B_R0E_C1_REGRESSIONS.json');required={r['ID']:r for r in baseline['Runs'] if r.get('Command')}
  required.update(C1_reference=dict(ExitCode=0,PassCount=840,FailCount=0),C1_mutations=dict(ExitCode=0,PassCount=54,FailCount=0),C1_package_baseline=dict(ExitCode=0,PassCount=None,FailCount=None))
  runids=[r['ID'] for r in reg['Runs']]
  if set(runids)!=set(required) or len(runids)!=len(set(runids)):fail('REGRESSION_INVENTORY')
  for r in reg['Runs']:
   provenance(r,('Tests/Static/run_hsbi_02b_r0e_c2_regressions.py',),'regression:'+r['ID'])
   exp=required.get(r['ID'])
   if exp is None:fail('UNKNOWN_REGRESSION');continue
   if type(r['ExitCode']) is not int or r['ExitCode']!=exp['ExitCode'] or not r['BaselineMatch'] or exp['PassCount'] is not None and (r['PassCount'],r['FailCount'])!=(exp['PassCount'],exp['FailCount']):fail('REGRESSION_BASELINE',r['ID'])
   if r.get('RunnerSourceHash')!=sha(root/'Tests/Static/run_hsbi_02b_r0e_c2_regressions.py'):fail('RUNNER_HASH')
  if not reg['BaselineMatch'] or reg['RegressionStatus']!='FAIL' or reg['ExitCode']!=0:fail('REGRESSION_VERDICT')
  # Approval fields: exactly one structural value, never substring acceptance.
  sheet=(root/SHEET).read_text();parts=re.split(r'^## Contract: (.+)$',sheet,flags=re.M);names=[]
  for i in range(1,len(parts),2):
   name,body=parts[i:i+2];names.append(name)
   reserved={re.sub('[^a-z]','',f.lower()):f for f in ('ApprovalStatus','AdministratorDecision','ApprovalDate','ApprovalIdentifier')}
   for line in body.splitlines():
    if ':' in line:
     k=line.split(':',1)[0];normalized=re.sub('[^a-z]','',k.lower())
     if normalized in reserved and k!=reserved[normalized]:fail('STATUS_FIELD_NAME',name+':'+k)
   for field in ('ApprovalStatus','AdministratorDecision','ApprovalDate','ApprovalIdentifier'):
    found=re.findall(r'^'+field+r':([^\n]*)(?:\n(.*?))?(?=^[A-Za-z][A-Za-z]+:|\Z)',body,re.M|re.S)
    if len(found)!=1:fail('STATUS_UNIQUENESS',name+':'+field);continue
    values=[x.strip() for x in found[0] if x and x.strip()];wanted=['AWAITING_ADMIN_APPROVAL'] if field=='ApprovalStatus' else []
    if values!=wanted:fail('APPROVAL_VALUE',name+':'+field)
  if sorted(names)!=sorted(DECISIONS):fail('APPROVAL_INVENTORY')
  text=(root/VERDICT).read_text();sections=re.findall(r'^\[C2_FINAL_STATUS\]\n(.*?)^\[/C2_FINAL_STATUS\]$',text,re.M|re.S)
  if len(sections)!=1:fail('STATUS_SECTION')
  for line in text.splitlines():
   if '=' in line:
    k=line.split('=',1)[0];normalized=re.sub('[^a-z]','',k.lower())
    matched=[f for f in POLICY if re.sub('[^a-z]','',f.lower())==normalized]
    if matched and k!=matched[0]:fail('STATUS_FIELD_NAME',k)
  if len(sections)==1 and set(re.findall(r'^([A-Z_0-9]+)=',sections[0],re.M))!=set(POLICY):fail('STATUS_SECTION')
  for field,wanted in POLICY.items():
   full=re.findall(r'^'+field+r'=(.*)$',text,re.M);inside=re.findall(r'^'+field+r'=(.*)$',sections[0],re.M) if len(sections)==1 else []
   allowed=[wanted] if check_results or field not in ('STAGE_02B_R0E_C2_COMPLETE','CONTRACT_FREEZE_CANDIDATE_READY') else ['NO','YES']
   if len(full)!=1 or full!=inside or full[0] not in allowed:fail('STATUS_UNIQUENESS',field)
  if check_results:
   report=load(root,RESULT);provenance(report,('Tests/Static/check_hsbi_02b_r0e_c2_package.py',),'package')
   if report.get('ExitCode')!=0 or report.get('Positive')!='PASS' or report.get('Errors') or report.get('CatalogDigest')!=catalog.canonical_digest(expected):fail('PACKAGE_RESULT')
   probeids=[r['ProbeID'] for r in report.get('Negative',[])]
   if set(probeids)!=set(PROBE_IDS) or len(probeids)!=len(PROBE_IDS) or report.get('NegativePassed')!=len(PROBE_IDS) or report.get('NegativeFailed')!=0:fail('PACKAGE_PROBE_INVENTORY')
   if any(r['Result']!='PASS' or r['ExpectedCode'] not in {e['Code'] for e in r['ActualErrors']} for r in report.get('Negative',[])):fail('PACKAGE_RESULT')
 except (OSError,KeyError,ValueError,TypeError,SyntaxError) as e:fail('PACKAGE_SCHEMA',type(e).__name__+':'+str(e))
 return errors

def probes():
    baseline=verify(check_results=False)
    if baseline:return dict(Positive='FAIL',Errors=baseline,Negative=[],NegativePassed=0,NegativeFailed=0)
    paths=files(ROOT);old=git_tree();rows=[]
    def j(root,path,edit):
        d=load(root,path);edit(d);save(root,path,d)
    def text_edit(root,path,edit):(root/path).write_text(edit((root/path).read_text()))
    historical_file=next(iter(old))
    def coherent_test_removal(root):
        d=load(root,TEST);tid='C2-BASE-COST-not-applicable';d['Rows']=[r for r in d['Rows'] if r['TestID']!=tid];d['Scenarios']-=1;d['Executions']=len(d['Rows']);d['Comparisons']=2*len(d['Rows'])+3*len(d['SchemaRows']);d['Pass']=len(d['Rows']);save(root,TEST,d)
        m=load(root,catalog.MATRIX);m['Cases']=[r for r in m['Cases'] if r['TestID']!=tid];m['ScenarioIDs'].remove(tid);save(root,catalog.MATRIX,m)
    def missing_mutation(root):
        d=load(root,MUT);r=d['Rows'].pop(0);d['CatalogSize']-=1;d['Killed']-=1;save(root,MUT,d)
    def wrong_verifier(root):
        path='Tests/Static/check_hsbi_02b_r0e_c2_package.py';f=root/path;f.write_text(f.read_text()+'\n# synthetic verifier modification\n');d=load(root,RESULT);d.setdefault('SourceHashes',{})[path]=sha(f);save(root,RESULT,d)
    def raw(root,path,needle,replacement):
        f=root/path;text=f.read_text();assert needle in text;f.write_text(text.replace(needle,replacement,1))
    def hash_map_duplicate(root):
        d=load(root,PRES);path,h=next(iter(d['ArtifactHashes'].items()));needle=json.dumps(path)+': '+json.dumps(h);raw(root,PRES,needle,needle+', '+needle)
    specs=[
      ('inventory-omission','BASELINE_INVENTORY',lambda r:j(r,PRES,lambda d:d['Existing'].pop(historical_file))),
      ('historical-content','HISTORICAL_BYTES',lambda r:(r/historical_file).write_bytes((r/historical_file).read_bytes()+b'\nsynthetic')),
      ('outside-scope','OUTSIDE_SCOPE',lambda r:(r/'outside_r0e_c2.txt').write_text('synthetic')),
      ('source-hash','SOURCE_HASH',lambda r:j(r,TEST,lambda d:d['SourceHashes'].__setitem__(mu.TARGET,'0'*64))),
      ('test-total','TEST_TOTALS',lambda r:j(r,TEST,lambda d:d.__setitem__('Executions',0))),
      ('fail-with-pass-total','TEST_VERDICT',lambda r:j(r,TEST,lambda d:d['Rows'][0].__setitem__('Result','FAIL'))),
      ('mandatory-missing','MANDATORY_ARTIFACT',lambda r:(r/'Docs/NEXT_STAGE_02B_R0E_C2_DTO_SCHEMA_CONTRACT_RU.md').unlink()),
      ('report-baseline','REPORT_BASELINE',lambda r:text_edit(r,VERDICT,lambda s:s.replace('BASE_SHA='+BASE,'BASE_SHA='+'0'*40))),
      ('empty-cases','MATRIX_TRACEABILITY',lambda r:j(r,catalog.MATRIX,lambda d:d.__setitem__('Cases',[]))),
      ('missing-case','MATRIX_TRACEABILITY',lambda r:j(r,catalog.MATRIX,lambda d:d['Cases'].pop())),
      ('duplicate-case','MATRIX_TRACEABILITY',lambda r:j(r,catalog.MATRIX,lambda d:d['Cases'].append(copy.deepcopy(d['Cases'][0])))),
      ('context-999','TEST_CONTEXT_INVENTORY',lambda r:j(r,TEST,lambda d:d['Rows'][0].__setitem__('ContextID',999))),
      ('context-bool','PACKAGE_SCHEMA',lambda r:j(r,TEST,lambda d:d['Rows'][0].__setitem__('ContextID',False))),
      ('context-missing','TEST_CONTEXT_INVENTORY',lambda r:j(r,TEST,lambda d:d['Rows'].pop())),
      ('context-duplicate','TEST_CONTEXT_INVENTORY',lambda r:j(r,TEST,lambda d:d['Rows'].append(copy.deepcopy(d['Rows'][0])))),
      ('context-metadata','CONTEXT_METADATA',lambda r:j(r,TEST,lambda d:d['ContextConfigurations'][0].__setitem__('precision',999))),
      ('original-hash','ORIGINAL_SOURCE_HASH',lambda r:j(r,MUT,lambda d:d['Rows'][0].__setitem__('OriginalSourceHash','0'*64))),
      ('mutant-hash','MUTANT_SOURCE_HASH',lambda r:j(r,MUT,lambda d:d['Rows'][0].__setitem__('MutantSourceHash','0'*64))),
      ('exact-edit','MUTATION_SPEC',lambda r:j(r,MUT,lambda d:d['Rows'][0]['ExactEdit'][0].__setitem__('old','no such target'))),
      ('approval-inline','APPROVAL_VALUE',lambda r:text_edit(r,SHEET,lambda s:s.replace('AdministratorDecision:\n','AdministratorDecision: APPROVED\n',1))),
      ('approval-newline','APPROVAL_VALUE',lambda r:text_edit(r,SHEET,lambda s:s.replace('AdministratorDecision:\n','AdministratorDecision:\n\nAPPROVED\n',1))),
      ('approval-duplicate','STATUS_UNIQUENESS',lambda r:text_edit(r,SHEET,lambda s:s.replace('AdministratorDecision:\n','AdministratorDecision:\n\nAdministratorDecision: APPROVED\n',1))),
      ('verdict-policy','STATUS_UNIQUENESS',lambda r:text_edit(r,VERDICT,lambda s:s.replace('ADMIN_APPROVAL_COMPLETE=NO','ADMIN_APPROVAL_COMPLETE=YES'))),
      ('empty-mutation-catalog','MUTATION_INVENTORY',lambda r:j(r,MUT,lambda d:d.update(Rows=[],CatalogSize=0,Killed=0,RedundantSurvivors=0,UnexplainedSurvivors=0,InfrastructureErrors=0))),
      ('missing-mutation','MUTATION_INVENTORY',missing_mutation),
      ('unknown-mutation','UNKNOWN_MUTATION',lambda r:j(r,MUT,lambda d:d['Rows'][0].__setitem__('MutationID','UNKNOWN'))),
      ('duplicate-mutation','MUTATION_INVENTORY',lambda r:j(r,MUT,lambda d:d['Rows'].append(copy.deepcopy(d['Rows'][0])))),
      ('missing-test-coherent-totals','TEST_CONTEXT_INVENTORY',coherent_test_removal),
      ('approval-status-contradiction','STATUS_UNIQUENESS',lambda r:text_edit(r,SHEET,lambda s:s.replace('ApprovalStatus: AWAITING_ADMIN_APPROVAL','ApprovalStatus: AWAITING_ADMIN_APPROVAL\nApprovalStatus: APPROVED',1))),
      ('approval-status-duplicate','STATUS_UNIQUENESS',lambda r:text_edit(r,SHEET,lambda s:s.replace('ApprovalStatus: AWAITING_ADMIN_APPROVAL','ApprovalStatus: AWAITING_ADMIN_APPROVAL\nApprovalStatus: AWAITING_ADMIN_APPROVAL',1))),
      ('admin-policy-conflict','STATUS_UNIQUENESS',lambda r:text_edit(r,VERDICT,lambda s:s+'\nADMIN_APPROVAL_COMPLETE=YES\n')),
      ('dispatch-policy-conflict','STATUS_UNIQUENESS',lambda r:text_edit(r,VERDICT,lambda s:s+'\nBROKER_DISPATCH_ALLOWED=YES\n')),
      ('regression-source-hash','SOURCE_HASH',lambda r:j(r,REG,lambda d:d['Runs'][0]['SourceHashes'].__setitem__(next(iter(d['Runs'][0]['SourceHashes'])),'0'*64))),
      ('reproduction-source-hash','SOURCE_HASH',lambda r:j(r,REPRO,lambda d:d['SourceHashes'].__setitem__(next(iter(d['SourceHashes'])),'0'*64))),
      ('matrix-function','MATRIX_TRACEABILITY',lambda r:j(r,catalog.MATRIX,lambda d:d['Cases'][0].__setitem__('SourceFunction','checked_add'))),
      ('matrix-mutation-dangling','MATRIX_TRACEABILITY',lambda r:j(r,catalog.MATRIX,lambda d:d['Cases'][0]['MutationIDs'].append('UNKNOWN'))),
      ('catalog-version','REQUIRED_CATALOG',lambda r:j(r,catalog.CATALOG,lambda d:d.__setitem__('CatalogVersion','UNKNOWN'))),
      ('catalog-inventory','REQUIRED_CATALOG',lambda r:j(r,catalog.CATALOG,lambda d:d.__setitem__('RequiredMutationIDs',[]))),
      ('catalog-source-pin','REQUIRED_CATALOG',lambda r:j(r,catalog.CATALOG,lambda d:d['SourcePins'].__setitem__(mu.TARGET,'0'*64))),
      ('mutation-wrong-function','MUTATION_SPEC',lambda r:j(r,MUT,lambda d:d['Rows'][0].__setitem__('TargetFunction','checked_add'))),
      ('test-missing-source-pin','PROVENANCE_INVENTORY',lambda r:j(r,TEST,lambda d:d['SourceHashes'].pop(mu.TARGET))),
      ('status-wrong-section','STATUS_UNIQUENESS',lambda r:text_edit(r,VERDICT,lambda s:s.replace('BROKER_DISPATCH_ALLOWED=NO\n','')+'\nBROKER_DISPATCH_ALLOWED=NO\n')),
      ('historical-mode','HISTORICAL_MODE',lambda r:(r/historical_file).chmod((r/historical_file).stat().st_mode ^ 0o111)),
      ('status-field-case','STATUS_FIELD_NAME',lambda r:text_edit(r,VERDICT,lambda s:s+'\nbroker_dispatch_allowed=YES\n')),
      ('verifier-source-identity','VERIFIER_SOURCE',wrong_verifier),
      ('counter-type','PACKAGE_SCHEMA',lambda r:j(r,TEST,lambda d:d.__setitem__('Fail',False))),
    ]
    specs += [
     ('json-root','PACKAGE_SCHEMA',lambda r:raw(r,TEST,'"ExitCode": 0','"ExitCode": 1, "ExitCode": 0')),
     ('json-nested','PACKAGE_SCHEMA',lambda r:raw(r,TEST,'"Result": "PASS"','"Result": "FAIL", "Result": "PASS"')),
     ('json-reverse','PACKAGE_SCHEMA',lambda r:raw(r,TEST,'"Result": "PASS"','"Result": "PASS", "Result": "FAIL"')),
     ('json-same','PACKAGE_SCHEMA',lambda r:raw(r,TEST,'"Result": "PASS"','"Result": "PASS", "Result": "PASS"')),
     ('json-regression','PACKAGE_SCHEMA',lambda r:raw(r,REG,'"ExitCode": 0','"ExitCode": 1, "ExitCode": 0')),
     ('json-manifest','PACKAGE_SCHEMA',lambda r:raw(r,PRES,'"BaseSHA": "'+BASE+'"','"BaseSHA": "'+BASE+'", "BaseSHA": "'+BASE+'"')),
     ('json-hash-map','PACKAGE_SCHEMA',hash_map_duplicate),
     ('json-nan','PACKAGE_SCHEMA',lambda r:raw(r,TEST,'"ExitCode": 0','"ExitCode": NaN')),
     ('json-infinity','PACKAGE_SCHEMA',lambda r:raw(r,TEST,'"ExitCode": 0','"ExitCode": Infinity')),
     ('json-counter-bool','PACKAGE_SCHEMA',lambda r:raw(r,REG,'"ExitCode": 0','"ExitCode": false')),
     ('schema-probe-missing','SCHEMA_INVENTORY',lambda r:j(r,TEST,lambda d:d['SchemaRows'].pop())),
     ('clause-mapping','MATRIX_TRACEABILITY',lambda r:j(r,catalog.MATRIX,lambda d:d['Guards'][0].__setitem__('ClauseID','FOREIGN'))),
    ]
    assert [s[0] for s in specs]==list(PROBE_IDS)
    # Freeze one template BEFORE creating any nested disposable candidate.
    with tempfile.TemporaryDirectory(prefix='R0E_C2_pkg_',dir=ROOT/'Tests') as td:
        template=Path(td)/'template'
        for path in paths:
            dest=template/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/path,dest)
        for name,code,edit in specs:
            candidate=Path(td)/'candidate';shutil.copytree(template,candidate)
            edit(candidate)
            proof=load(template if name in ('json-manifest','json-hash-map') else candidate,PRES)
            for path in proof['ArtifactHashes']:
                p=candidate/path
                if p.is_file():proof['ArtifactHashes'][path]=sha(p)
            if name not in ('json-manifest','json-hash-map'):save(candidate,PRES,proof)
            errors=verify(candidate,check_results=False)
            ok=code in {e['Code'] for e in errors}
            rows.append(dict(ProbeID=name,Group='R0E_23_CLASS' if name in LEGACY_PROBES else 'C2_EXTENSION',PositiveControl='PASS_FROZEN_TEMPLATE',ExpectedCode=code,ActualErrors=errors,Result='PASS' if ok else 'FAIL',ProofBoundary='Disposable fixture; refreshed new-artifact hashes; real baseline untouched'))
            print(name,rows[-1]['Result'],flush=True);shutil.rmtree(candidate)
    return dict(Positive='PASS',Errors=[],Negative=rows,NegativePassed=sum(r['Result']=='PASS' for r in rows),NegativeFailed=sum(r['Result']!='PASS' for r in rows))

def main():
    p=argparse.ArgumentParser();p.add_argument('--seal',action='store_true');p.add_argument('--self-test',action='store_true');args=p.parse_args()
    if args.seal:seal()
    started=t.now();errors=verify(check_results=not args.self_test)
    result=dict(t.metadata(),Command=[sys.executable,*sys.argv],StartedUtc=started,FinishedUtc=t.now(),SourceHashes={str(Path(__file__).relative_to(ROOT)):sha(Path(__file__)),**catalog.expected_catalog()['SourcePins']},CatalogDigest=catalog.canonical_digest(catalog.expected_catalog()),Positive='PASS' if not errors else 'FAIL',Errors=errors)
    if args.self_test and not errors:result.update(probes())
    result['FinishedUtc']=t.now();result['ExitCode']=int(bool(errors) or result.get('NegativeFailed',0)>0 or result['Positive']!='PASS')
    if args.self_test:save(ROOT,RESULT,result)
    print(json.dumps({k:v for k,v in result.items() if k!='Negative'},ensure_ascii=False));return result['ExitCode']
if __name__=='__main__':raise SystemExit(main())
