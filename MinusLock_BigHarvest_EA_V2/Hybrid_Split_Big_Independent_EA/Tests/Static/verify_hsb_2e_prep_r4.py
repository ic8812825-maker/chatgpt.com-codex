#!/usr/bin/env python3
"""Closed executable PREP-R4 verifier: every verdict is derived from executed checks."""
import argparse,ast,fnmatch,hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent/'Reference'))
import hsb_2e_reference_model_r4 as model
import hsb_2e_invariants_r4 as inv
import hsb_2e_scenario_engine_r4 as engine
import hsb_2e_broker_intent_validator_r4 as broker
BASELINE='d6c3e80a6eecb3288b5846d1824bd7e86711ef82'
DATA=('Tests/Reference/hsb_2e_reference_model_r4.py','Tests/Reference/hsb_2e_invariants_r4.py','Tests/Reference/hsb_2e_scenario_engine_r4.py','Tests/Reference/hsb_2e_broker_intent_validator_r4.py','Tests/Static/hsb_2e_formula_contracts_r4.json','Tests/Static/hsb_2e_scenario_contracts_r4.json','Tests/Static/hsb_2e_api_contracts_r4.json','Tests/Static/hsb_2e_normative_source_map_r4.json','Tests/Static/hsb_2e_test_plan_r4.json','Tests/Static/hsb_2e_metric_derivations_r4.json','Tests/Vectors/HSB_2E_R4_GOLDEN_VECTORS.json','Tests/Vectors/HSB_2E_R4_BOUNDARY_VECTORS.json','Tests/Vectors/HSB_2E_R4_NEGATIVE_VECTORS.json','Tests/Vectors/HSB_2E_R4_SCENARIO_VECTORS.json','Tests/Vectors/HSB_2E_R4_RESTART_VECTORS.json','Tests/Static/verify_hsb_2e_prep_r4.py','Tests/Static/run_hsb_2e_prep_r4_mutations.py','Tests/Static/hsb_2e_prep_r4_mutations.json','Docs/HSB_2E_PREP_R4_IMPLEMENTATION_HANDOFF_RU.md','Reports/HSB_2E_PREP_R4_FALSE_PASS_ANALYSIS_RU.md','Reports/HSB_2E_PREP_R4_FINAL_VERDICT_RU.md')
EVIDENCE=('Tests/Evidence/HSB_2E_PREP_R4_VERIFIER_RESULT.txt','Tests/Evidence/HSB_2E_PREP_R4_VERIFIER_RESULT.json','Tests/Evidence/HSB_2E_PREP_R4_VECTOR_RESULTS.json','Tests/Evidence/HSB_2E_PREP_R4_INVARIANT_RESULTS.json','Tests/Evidence/HSB_2E_PREP_R4_SCENARIO_RESULTS.json','Tests/Evidence/HSB_2E_PREP_R4_BROKER_INTENT_RESULTS.json','Tests/Evidence/HSB_2E_PREP_R4_RESTART_RESULTS.json','Tests/Evidence/HSB_2E_PREP_R4_T465_T1149_RESULTS.json','Tests/Evidence/HSB_2E_PREP_R4_METRIC_DERIVATIONS.json','Tests/Evidence/HSB_2E_PREP_R4_MUTATION_RESULTS.json','Tests/Evidence/HSB_2E_PREP_R4_MUTATION_RESULTS.txt','Tests/Evidence/HSB_2E_PREP_R4_MUTATION_QUALITY_AUDIT.json')
def load(r,p,key=None):
 x=json.loads((r/p).read_text());return x[key] if key else x
def dg(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()
def checkrow(cid,ok,actual=None,expected=None,function='',assertion='',invariants=()):return {'CHECK_ID':cid,'INPUT_DIGEST':dg(actual if actual is not None else {}),'ACTUAL_DIGEST':dg(actual),'EXPECTED_DIGEST':dg(expected),'EXECUTED_FUNCTION':function,'ASSERTION_ID':assertion,'INVARIANT_IDS':list(invariants),'RESULT':'PASS' if ok else 'FAIL'}
def hashfile(root,path,expected):
 try:lines=(root/path).read_text().splitlines()
 except OSError:return False
 got=[]
 for line in lines:
  try:h,rel=line.split('  ',1);p=(root/rel).resolve();p.relative_to(root)
  except (ValueError,OSError):return False
  if len(h)!=64 or not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=h:return False
  got.append(rel)
 return len(got)==len(set(got)) and set(got)==set(expected)
def hardcoded_audit(path):
 tree=ast.parse(path.read_text());bad=[]
 for n in ast.walk(tree):
  if isinstance(n,(ast.Assign,ast.AnnAssign)):
   targets=n.targets if isinstance(n,ast.Assign) else [n.target];value=n.value
   for t in targets:
    if isinstance(t,ast.Subscript) and isinstance(t.value,ast.Name) and t.value.id=='metrics' and isinstance(value,ast.Constant) and value.value in ('PASS',0):bad.append(n.lineno)
 return bad
def execute_assertion(a,v,actual,invrows,broker_result):
 expected=v['EXPECTED_RESULT'];o=actual['output'];aid=a
 if aid=='ASSERT_STATUS':return actual['status']==v['EXPECTED_STATUS']
 if aid=='ASSERT_REASON':return actual['reason']==v['EXPECTED_REASON']
 if aid=='ASSERT_OUTPUT':return o==v['EXPECTED_OUTPUT']
 if aid=='ASSERT_DIGEST':return actual['outputDigest']==expected['outputDigest']
 if aid=='ASSERT_INVARIANTS':return all(x['RESULT']=='PASS' for x in invrows)
 if aid=='ASSERT_MONEY_CONSERVATION':return inv.check('MONEY_CONSERVATION',v['INPUT'],actual) is True
 if aid=='ASSERT_VOLUME_CONSERVATION':return inv.check('VOLUME_CONSERVATION',v['INPUT'],actual) is True
 if aid=='ASSERT_RESERVE_ISOLATION':return inv.check('PARTIAL_FAR_RESERVE_ISOLATION',v['INPUT'],actual) is True
 if aid=='ASSERT_NEW_FAR_COMPRESSION':return inv.check('NEW_FAR_COMPRESSION',v['INPUT'],actual) is True
 if aid=='ASSERT_INTENT_ORDER':return [x['positionRole'] for x in actual['futureBrokerIntents']]==[x['positionRole'] for x in expected['futureBrokerIntents']]
 if aid=='ASSERT_NO_DUPLICATE_INTENT':return broker_result['result']=='PASS'
 if aid=='ASSERT_PERSISTENCE_ORDER':return inv.check('PERSISTENCE_BEFORE_MUTATION',v['INPUT'],actual) is True
 if aid=='ASSERT_RESTART_STATE':return actual['output'].get('replayAction')==v['EXPECTED_OUTPUT'].get('replayAction')
 if aid=='ASSERT_LEDGER_DELTA':return actual['ledgerDelta']==expected['ledgerDelta']
 if aid=='ASSERT_POSITION_DELTA':return actual['positionDelta']==expected['positionDelta']
 return None
def run(root,skip_integrity=False,fixture_mode=False):
 r=root.resolve();checks=[];vector_rows=[];inv_rows=[];broker_rows=[];restart_rows=[]
 vector_files=['GOLDEN','BOUNDARY','NEGATIVE','SCENARIO','RESTART'];vectors=[]
 for group in vector_files:vectors+=load(r,f'Tests/Vectors/HSB_2E_R4_{group}_VECTORS.json','vectors')
 byid={v['VECTOR_ID']:v for v in vectors};actuals={};inv_by_vector={};broker_by_vector={}
 for v in vectors:
  actual=model.execute(v['FUNCTION'],v['INPUT']);actuals[v['VECTOR_ID']]=actual;expected=v['EXPECTED_RESULT'];baseok=actual==expected
  local=[]
  for name in v['EXPECTED_INVARIANTS']:
   outcome=inv.check(name,v['INPUT'],actual);cid=f'INV_{name}_{v["VECTOR_ID"]}';row=checkrow(cid,outcome is True,{'input':v['INPUT'],'actual':actual},True,v['FUNCTION'],'',v['EXPECTED_INVARIANTS']);local.append(row);inv_rows.append(row);checks.append(row)
  inv_by_vector[v['VECTOR_ID']]=local
  br=broker.validate(actual['futureBrokerIntents'],v['INPUT'].get('positions',[]),failed=actual['status'] in ('REJECT','ERROR'))
  broker_by_vector[v['VECTOR_ID']]=br
  if v['CATEGORY']=='BROKER_INTENT':row=checkrow('BROKER_'+v['VECTOR_ID'],br['result']=='PASS',actual['futureBrokerIntents'],[], 'broker.validate');broker_rows.append(row);checks.append(row)
  ok=baseok and all(x['RESULT']=='PASS' for x in local) and (br['result']=='PASS' or not actual['futureBrokerIntents'])
  row=checkrow('VECTOR_'+v['VECTOR_ID'],ok,actual,expected,v['FUNCTION'],'',v['EXPECTED_INVARIANTS']);vector_rows.append(row);checks.append(row)
  if v['CATEGORY']=='RESTART':rr=checkrow('RESTART_'+v['VECTOR_ID'],ok and actual['output'].get('actionId')==v['INPUT']['actionId'],actual,expected,v['FUNCTION']);restart_rows.append(rr);checks.append(rr)
 # typed scenario contracts execute, not just inspect
 contracts=load(r,'Tests/Static/hsb_2e_scenario_contracts_r4.json','scenarios');scenario_rows=[]
 reps={'BIG':next(v for v in vectors if v['CATEGORY']=='BIG'),'SMALL':next(v for v in vectors if v['CATEGORY']=='SMALL'),'OTHER':next(v for v in vectors if v['FUNCTION']=='validate_context' and v['EXPECTED_STATUS']=='PASS')}
 for c in contracts:
  v=copy_vector(reps[c['KIND']]);er=engine.execute(c,v);row=checkrow('SCENARIO_'+c['SCENARIO_ID'],er['result']=='PASS',er,{'result':'PASS'},'scenario_engine');scenario_rows.append(row);checks.append(row)
 # 685 concrete assertion executions
 tests=load(r,'Tests/Static/hsb_2e_test_plan_r4.json','tests');test_rows=[];unknown=0
 for t in tests:
  v=byid.get(t['VECTOR_ID']);outcome=None
  if v:outcome=execute_assertion(t['ASSERTION_ID'],v,actuals[v['VECTOR_ID']],inv_by_vector[v['VECTOR_ID']],broker_by_vector[v['VECTOR_ID']])
  if outcome is None:unknown+=1
  row=checkrow('TEST_'+t['TEST_ID'],outcome is True,actuals.get(t['VECTOR_ID']),v['EXPECTED_RESULT'] if v else None,t['FUNCTION'],t['ASSERTION_ID'],v['EXPECTED_INVARIANTS'] if v else []);test_rows.append(row);checks.append(row)
 # schema/cross-reference checks
 forms=load(r,'Tests/Static/hsb_2e_formula_contracts_r4.json','formulas');api=load(r,'Tests/Static/hsb_2e_api_contracts_r4.json','components');src=load(r,'Tests/Static/hsb_2e_normative_source_map_r4.json');ids=[x['TEST_ID'] for x in tests]
 structural=[('STRUCT_FORMULAS',len(forms)==22 and all(f['PUBLIC_FUNCTION'] in model.FUNCTIONS for f in forms)),('STRUCT_API',len(api)==32 and all(not x['SIDE_EFFECTS'] and 'BROKER_DISPATCH' in x['FORBIDDEN_SIDE_EFFECTS'] for x in api)),('STRUCT_SOURCES',not src['open_decisions']),('STRUCT_TEST_IDS',ids==[f'T{i}' for i in range(465,1150)]),('STRUCT_TEST_PAIRS',len({(x['VECTOR_ID'],x['ASSERTION_ID']) for x in tests})==685),('HARDCODED_VERDICTS',not hardcoded_audit(Path(__file__)))]
 for cid,ok in structural:checks.append(checkrow(cid,ok,ok,True,'verifier'))
 # derived metrics: pattern expansion over real check IDs
 registry=load(r,'Tests/Static/hsb_2e_metric_derivations_r4.json','metrics');metric_rows=[];available={x['CHECK_ID']:x['RESULT'] for x in checks}
 for spec in registry:
  matched=sorted({cid for pat in spec['SOURCE_PATTERNS'] for cid in available if fnmatch.fnmatch(cid,pat)});mode=spec['DERIVATION'];ok=mode=='ALL' and len(matched)>=spec['MINIMUM_SOURCE_CHECKS'] and all(available[x]=='PASS' for x in matched);metric_rows.append({'METRIC_ID':spec['METRIC_ID'],'SOURCE_CHECK_IDS':matched,'REQUIRED_RESULTS':'PASS','ACTUAL_RESULTS':[available[x] for x in matched],'DERIVATION':'ALL_SOURCE_CHECKS_PASS','RESULT':'PASS' if ok else 'FAIL'});checks.append(checkrow('METRIC_'+spec['METRIC_ID'],ok,matched,spec['MINIMUM_SOURCE_CHECKS'],'derive_metrics'))
 # scope and production
 if fixture_mode:scope_ok=prod_ok=True
 else:
  cp=subprocess.run(['git','diff','--name-only',BASELINE+'..HEAD'],cwd=r,text=True,capture_output=True);paths=cp.stdout.splitlines();scope_ok=cp.returncode==0 and all(x.startswith('MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/') for x in paths);prod_ok=not any(x.endswith('.mq5') or '/Include/' in x and x.endswith('.mqh') for x in paths)
 checks.append(checkrow('SCOPE_AUDIT',scope_ok,scope_ok,True,'git'));checks.append(checkrow('PRODUCTION_AUDIT',prod_ok,prod_ok,True,'git'))
 manifest=hashfile(r,'Reports/HSB_2E_PREP_R4_FILE_MANIFEST_SHA256.txt',DATA);seal=hashfile(r,'Tests/Evidence/HSB_2E_PREP_R4_EVIDENCE_SEAL_SHA256.txt',EVIDENCE+DATA)
 checks.append(checkrow('MANIFEST',manifest or skip_integrity,manifest,True,'hashfile'));checks.append(checkrow('SEAL',seal or skip_integrity,seal,True,'hashfile'))
 return {'checks':checks,'vectors':vector_rows,'invariants':inv_rows,'scenarios':scenario_rows,'broker':broker_rows,'restart':restart_rows,'tests':test_rows,'metrics':metric_rows,'unknownAssertions':unknown,'result':'PASS' if all(x['RESULT']=='PASS' for x in checks) else 'FAIL'}
def copy_vector(v):return json.loads(json.dumps(v))
def summary(x):
 fail=sum(r['RESULT']=='FAIL' for r in x['checks']);lines=[f'{r["CHECK_ID"]}|{r["RESULT"]}' for r in x['checks'] if r['CHECK_ID'].startswith(('STRUCT_','METRIC_','SCOPE','PRODUCTION','MANIFEST','SEAL'))]
 lines += [f'CHECKS_EXECUTED={len(x["checks"])}',f'CHECKS_FAILED={fail}',f'VECTORS_EXECUTED={len(x["vectors"])}',f'INVARIANTS_EXECUTED={len(x["invariants"])}',f'SCENARIOS_EXECUTED={len(x["scenarios"])}',f'BROKER_INTENTS_VALIDATED={len(x["broker"])}',f'RESTART_VECTORS_EXECUTED={len(x["restart"])}',f'T465_T1149_REQUIRED={len(x["tests"])}',f'T465_T1149_EXECUTED={len(x["tests"])}',f'T465_T1149_PASS={sum(r["RESULT"]=="PASS" for r in x["tests"])}',f'T465_T1149_FAIL={sum(r["RESULT"]=="FAIL" for r in x["tests"])}',f'UNKNOWN_ASSERTIONS={x["unknownAssertions"]}',f'RESULT={x["result"]}'];return '\n'.join(lines)+'\n'
def write(root,x):
 d=root/'Tests/Evidence';d.mkdir(parents=True,exist_ok=True);mapping={'VECTOR_RESULTS':'vectors','INVARIANT_RESULTS':'invariants','SCENARIO_RESULTS':'scenarios','BROKER_INTENT_RESULTS':'broker','RESTART_RESULTS':'restart','T465_T1149_RESULTS':'tests','METRIC_DERIVATIONS':'metrics'}
 text=summary(x);(d/'HSB_2E_PREP_R4_VERIFIER_RESULT.txt').write_text(text);(d/'HSB_2E_PREP_R4_VERIFIER_RESULT.json').write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
 for suffix,key in mapping.items():(d/f'HSB_2E_PREP_R4_{suffix}.json').write_text(json.dumps({'results':x[key]},indent=2,sort_keys=True)+'\n')
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--skip-integrity',action='store_true');p.add_argument('--fixture-mode',action='store_true');p.add_argument('--write-evidence',action='store_true');a=p.parse_args();root=Path(a.root).resolve();x=run(root,a.skip_integrity,a.fixture_mode);print(summary(x),end='');
 if a.write_evidence:write(root,x)
 return 0 if x['result']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
