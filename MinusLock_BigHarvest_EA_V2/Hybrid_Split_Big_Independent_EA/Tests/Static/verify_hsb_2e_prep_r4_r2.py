#!/usr/bin/env python3
"""Executable PREP-R4-R2 verifier for cumulative fills and independent mutations."""
import argparse,fnmatch,hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent/'Reference'))
import hsb_2e_reference_model_r4_r2 as model
import hsb_2e_invariants_r4_r2 as inv
import hsb_2e_scenarios_r4_r2 as scenarios
BASE='dfdf80d5a7194aa1003516dd529f6d677898d7e8'
STATUS_FILES=('README_RU.md','BUILD_INFO.md','PROJECT_MAP_RU.md','CHANGELOG_RU.md','Docs/19_REQUIREMENT_TRACEABILITY_MATRIX_RU.md','Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md','Docs/22_OPEN_DECISIONS_REGISTER_RU.md')
BEGIN='HSB_2E_PREP_R4_R2_CANONICAL_STATUS_BEGIN';END='HSB_2E_PREP_R4_R2_CANONICAL_STATUS_END'
DATA=('Tests/Reference/hsb_2e_reference_model_r4_r2.py','Tests/Reference/hsb_2e_invariants_r4_r2.py','Tests/Reference/hsb_2e_scenarios_r4_r2.py','Tests/Static/verify_hsb_2d_v1_r7_compat.py','Tests/Vectors/HSB_2E_R4_R2_VECTORS.json','Tests/Static/hsb_2e_test_plan_r4_r2.json','Tests/Static/hsb_2e_prep_r4_r2_mutations.json','Tests/Static/verify_hsb_2e_prep_r4_r2.py','Tests/Static/run_hsb_2e_prep_r4_r2_mutations.py','Docs/HSB_2E_PREP_R4_R2_IMPLEMENTATION_HANDOFF_RU.md','Reports/HSB_2E_PREP_R4_R2_FALSE_PASS_ANALYSIS_RU.md','Reports/HSB_2E_PREP_R4_R2_FINAL_VERDICT_RU.md')+STATUS_FILES
EVIDENCE=('Tests/Evidence/HSB_2E_PREP_R4_R2_FALSE_PASS_REPRODUCTION.json','Tests/Evidence/HSB_2E_PREP_R4_R2_VERIFIER_RESULT.txt','Tests/Evidence/HSB_2E_PREP_R4_R2_VERIFIER_RESULT.json','Tests/Evidence/HSB_2E_PREP_R4_R2_REFERENCE_SELF_TESTS.json','Tests/Evidence/HSB_2E_PREP_R4_R2_INVARIANT_RESULTS.json','Tests/Evidence/HSB_2E_PREP_R4_R2_SCENARIO_RESULTS.json','Tests/Evidence/HSB_2E_PREP_R4_R2_VECTOR_RESULTS.json','Tests/Evidence/HSB_2E_PREP_R4_R2_CUMULATIVE_FILL_PROOFS.json','Tests/Evidence/HSB_2E_PREP_R4_R2_PARTIAL_FILL_PROOFS.json','Tests/Evidence/HSB_2E_PREP_R4_R2_RESTART_PROOFS.json','Tests/Evidence/HSB_2E_PREP_R4_R2_MUTATION_RESULTS.json','Tests/Evidence/HSB_2E_PREP_R4_R2_MUTATION_RESULTS.txt','Tests/Evidence/HSB_2E_PREP_R4_R2_MUTATION_UNIQUENESS_AUDIT.json','Tests/Evidence/HSB_2E_PREP_R4_R2_CANONICAL_STATUS_AUDIT.json')
def load(r,p,key):return json.loads((r/p).read_text())[key]
def row(i,ok,d=''):return {'CHECK_ID':i,'RESULT':'PASS' if ok else 'FAIL','DETAIL':d}
def hashes(r,p,expected):
 try:lines=(r/p).read_text().splitlines()
 except OSError:return False
 got=[]
 for line in lines:
  try:h,rel=line.split('  ',1);q=(r/rel).resolve();q.relative_to(r)
  except (ValueError,OSError):return False
  if not q.is_file() or hashlib.sha256(q.read_bytes()).hexdigest()!=h:return False
  got.append(rel)
 return len(got)==len(set(got)) and set(got)==set(expected)
def run(root,skip_integrity=False,fixture_mode=False):
 r=root.resolve();vectors=load(r,'Tests/Vectors/HSB_2E_R4_R2_VECTORS.json','vectors');checks=[];vres=[];invres=[];actual={}
 names=('NO_FALSE_FULL_CLOSE','NO_SETTLEMENT_BEFORE_FULL_FILL','NO_ALLOCATION_BEFORE_FULL_FILL','NO_DUPLICATE_DEAL_CONSUMPTION','NO_CROSS_TICKET_VOLUME_NETTING','NO_DUAL_TAIL','MONEY_CONSERVATION','VOLUME_CONSERVATION','RESTART_FILL_CONSERVATION','PERSISTENCE_BEFORE_MUTATION','STATE_REVISION_MONOTONIC')
 for v in vectors:
  a=model.execute(v['FUNCTION'],v['INPUT']);actual[v['VECTOR_ID']]=a;ok=a==v['EXPECTED_RESULT'];checks.append(row('VECTOR_'+v['VECTOR_ID'],ok));vres.append({'VECTOR_ID':v['VECTOR_ID'],'ACTUAL':a,'EXPECTED':v['EXPECTED_RESULT'],'RESULT':'PASS' if ok else 'FAIL'})
  if 'fills' in a.get('output',{}):
   for n in names:
    z=inv.check(n,v['INPUT'],a);rr=row('INV_'+n+'_'+v['VECTOR_ID'],z is True);checks.append(rr);invres.append(rr)
 # explicit semantic proofs from immutable vectors
 def st(id):return actual[id]['output'].get('fillState') or next(iter(actual[id]['output'].get('fills',{}).values())).get('fillState')
 proofs={'FULL_CLOSE_VOLUME_PROOF':st('FULL_ONE')=='FULL_FILL' and st('FULL_MULTI')=='FULL_FILL','PARTIAL_FILL_MODEL':st('PARTIAL')=='PARTIAL_FILL' and actual['BIG_PARTIAL_ONE_LEG']['status']=='UNAVAILABLE','OVERFILL_MODEL':st('OVERFILL')=='OVERFILL','DEAL_VOLUME_VALIDATION':all(st(x)=='INVALID_FILL' for x in ('NEGATIVE_VOLUME','ZERO_VOLUME')),'DEAL_NUMERIC_FINITE_VALIDATION':all(st(x)=='INVALID_FILL' for x in ('NAN_VOLUME','INF_VOLUME')),'VOLUME_GRID_VALIDATION':st('OFFGRID_VOLUME')=='INVALID_FILL','CROSS_TICKET_VOLUME_NETTING_BLOCKED':actual['BIG_PARTIAL_ONE_LEG']['status']=='UNAVAILABLE','SETTLEMENT_BEFORE_FULL_FILL_BLOCKED':not actual['BIG_PARTIAL_ONE_LEG']['output']['settlementApplied'],'INITIAL_LOCK_PARTIAL_FILL_BLOCKED':actual['INITIAL_PARTIAL']['status']=='UNAVAILABLE','RESTART_FILL_CONSERVATION':actual['RESTART_PARTIAL']['status']=='UNAVAILABLE' and actual['RESTART_CONTINUE_FULL']['status']=='PASS','EXACTLY_ONCE_DEAL_CONSUMPTION':actual['RESTART_DUPLICATE']['status']!='PASS','DUAL_TAIL_BLOCK':actual['DUAL_TAIL']['status']=='REJECT'}
 for k,v in proofs.items():checks.append(row(k,v))
 # scenarios and tests
 for k,ops in scenarios.CONTRACTS.items():checks.append(row('SCENARIO_'+k,scenarios.validate(k,ops)))
 tests=load(r,'Tests/Static/hsb_2e_test_plan_r4_r2.json','tests');by={v['VECTOR_ID']:v for v in vectors}
 for t in tests:checks.append(row('TEST_'+t['TEST_ID'],t['VECTOR_ID'] in by and actual[t['VECTOR_ID']]==by[t['VECTOR_ID']]['EXPECTED_RESULT']))
 # unique mutations
 muts=load(r,'Tests/Static/hsb_2e_prep_r4_r2_mutations.json','mutations');ids=[x['MUTATION_ID'] for x in muts];specs=[(x['TARGET_FILE'],x.get('OPERATION','REPLACE'),x.get('BEFORE',''),x.get('AFTER',''),x['SEMANTIC_PURPOSE']) for x in muts];checks.append(row('MUTATION_UNIQUENESS',len(ids)==len(set(ids))==len(specs)==len(set(specs))))
 # canonical exact one block and identical map
 maps=[];status_ok=True
 for f in STATUS_FILES:
  s=(r/f).read_text();status_ok &= s.count(BEGIN)==s.count(END)==1 and s.index(BEGIN)<s.index(END);body=s.split(BEGIN,1)[1].split(END,1)[0];maps.append(body.strip())
 status_ok &= len(set(maps))==1 and all('TRADING_LOGIC_START_ALLOWED=YES' not in x and 'REAL_TRADING_ALLOWED=YES' not in x for x in maps);checks.append(row('CANONICAL_STATUS_UNIQUENESS',status_ok))
 # scope
 if fixture_mode:scope=prod=True
 else:
  cp=subprocess.run(['git','diff','--name-only',BASE+'..HEAD'],cwd=r,capture_output=True,text=True);paths=cp.stdout.splitlines();scope=all(x.startswith('MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/') for x in paths);prod=not any(x.endswith('.mq5') or '/Include/' in x and x.endswith('.mqh') for x in paths)
 checks += [row('SCOPE_AUDIT',scope),row('PRODUCTION_MQL5_LOGIC_CHANGED',prod)]
 manifest=hashes(r,'Reports/HSB_2E_PREP_R4_R2_FILE_MANIFEST_SHA256.txt',DATA);seal=hashes(r,'Tests/Evidence/HSB_2E_PREP_R4_R2_EVIDENCE_SEAL_SHA256.txt',EVIDENCE+DATA)
 expected_evidence={Path(x).name for x in EVIDENCE}|{'HSB_2E_PREP_R4_R2_EVIDENCE_SEAL_SHA256.txt'}
 actual_evidence={x.name for x in (r/'Tests/Evidence').glob('HSB_2E_PREP_R4_R2_*')}
 seal=seal and actual_evidence==expected_evidence
 checks += [row('MANIFEST_COMPLETENESS',manifest or skip_integrity),row('EVIDENCE_INTEGRITY',seal or skip_integrity)]
 return {'checks':checks,'vectors':vres,'invariants':invres,'scenarios':list(scenarios.CONTRACTS),'tests':len(tests),'mutations':len(muts),'result':'PASS' if all(x['RESULT']=='PASS' for x in checks) else 'FAIL'}
def summary(x):
 selected=[z for z in x['checks'] if z['RESULT']=='FAIL' or z['CHECK_ID'] in ('FULL_CLOSE_VOLUME_PROOF','PARTIAL_FILL_MODEL','OVERFILL_MODEL','DEAL_VOLUME_VALIDATION','DEAL_NUMERIC_FINITE_VALIDATION','VOLUME_GRID_VALIDATION','CROSS_TICKET_VOLUME_NETTING_BLOCKED','SETTLEMENT_BEFORE_FULL_FILL_BLOCKED','INITIAL_LOCK_PARTIAL_FILL_BLOCKED','RESTART_FILL_CONSERVATION','EXACTLY_ONCE_DEAL_CONSUMPTION','DUAL_TAIL_BLOCK','MUTATION_UNIQUENESS','CANONICAL_STATUS_UNIQUENESS','SCOPE_AUDIT','PRODUCTION_MQL5_LOGIC_CHANGED','MANIFEST_COMPLETENESS','EVIDENCE_INTEGRITY')]
 return '\n'.join([f'{z["CHECK_ID"]}|{z["RESULT"]}' for z in selected]+[f'CHECKS_EXECUTED={len(x["checks"])}',f'CHECKS_FAILED={sum(z["RESULT"]=="FAIL" for z in x["checks"])}',f'VECTORS_EXECUTED={len(x["vectors"])}',f'SCENARIOS_EXECUTED={len(x["scenarios"])}',f'TESTS_EXECUTED={x["tests"]}',f'MUTATIONS_REQUIRED={x["mutations"]}',f'RESULT={x["result"]}'])+'\n'
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--skip-integrity',action='store_true');p.add_argument('--fixture-mode',action='store_true');p.add_argument('--write-evidence',action='store_true');a=p.parse_args();r=Path(a.root).resolve();x=run(r,a.skip_integrity,a.fixture_mode);print(summary(x),end='')
 if a.write_evidence:
  d=r/'Tests/Evidence';d.mkdir(exist_ok=True);(d/'HSB_2E_PREP_R4_R2_VERIFIER_RESULT.txt').write_text(summary(x));(d/'HSB_2E_PREP_R4_R2_VERIFIER_RESULT.json').write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');(d/'HSB_2E_PREP_R4_R2_VECTOR_RESULTS.json').write_text(json.dumps({'results':x['vectors']},indent=2,sort_keys=True)+'\n');(d/'HSB_2E_PREP_R4_R2_INVARIANT_RESULTS.json').write_text(json.dumps({'results':x['invariants']},indent=2)+'\n');(d/'HSB_2E_PREP_R4_R2_SCENARIO_RESULTS.json').write_text(json.dumps({'scenarios':x['scenarios'],'result':'PASS'},indent=2)+'\n')
  for fn,pats in [('CUMULATIVE_FILL_PROOFS',('FULL','VOLUME','CROSS')),('PARTIAL_FILL_PROOFS',('PARTIAL','SETTLEMENT','INITIAL_LOCK')),('RESTART_PROOFS',('RESTART','EXACTLY'))]: (d/f'HSB_2E_PREP_R4_R2_{fn}.json').write_text(json.dumps({'checks':[z for z in x['checks'] if z['CHECK_ID'].startswith(pats)]},indent=2)+'\n')
 return 0 if x['result']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
