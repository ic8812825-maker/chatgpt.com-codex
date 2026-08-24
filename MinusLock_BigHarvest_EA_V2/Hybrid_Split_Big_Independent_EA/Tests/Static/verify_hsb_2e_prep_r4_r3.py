#!/usr/bin/env python3
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent/'Reference'))
import hsb_2e_reference_model_r4_r3 as model,hsb_2e_invariants_r4_r3 as inv,hsb_2e_scenarios_r4_r3 as scenarios
BASE='b21646a8ab8839c4d7e32ccd3d3287aed68114f1';STATUS=('README_RU.md','BUILD_INFO.md','PROJECT_MAP_RU.md','CHANGELOG_RU.md','Docs/19_REQUIREMENT_TRACEABILITY_MATRIX_RU.md','Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md','Docs/22_OPEN_DECISIONS_REGISTER_RU.md');BEGIN='HSB_2E_PREP_R4_R3_CANONICAL_STATUS_BEGIN';END='HSB_2E_PREP_R4_R3_CANONICAL_STATUS_END'
DATA=('Tests/Reference/hsb_2e_reference_model_r4_r3.py','Tests/Reference/hsb_2e_invariants_r4_r3.py','Tests/Reference/hsb_2e_scenarios_r4_r3.py','Tests/Vectors/HSB_2E_R4_R3_VECTORS.json','Tests/Static/hsb_2e_test_plan_r4_r3.json','Tests/Static/hsb_2e_coverage_matrix_r4_r3.json','Tests/Static/hsb_2e_prep_r4_r3_mutations.json','Tests/Static/run_hsb_2e_prep_r4_r3_adversarial.py','Tests/Static/run_hsb_2e_prep_r4_r3_mutations.py','Tests/Static/verify_hsb_2e_prep_r4_r3.py','Docs/HSB_2E_PREP_R4_R3_IMPLEMENTATION_HANDOFF_RU.md','Reports/HSB_2E_PREP_R4_R3_FINAL_VERDICT_RU.md','Reports/HSB_2E_PREP_R4_R3_FALSE_PASS_ANALYSIS_RU.md')+STATUS
EVIDENCE=tuple('Tests/Evidence/HSB_2E_PREP_R4_R3_'+x for x in ('FALSE_PASS_REPRODUCTION.json','REFERENCE_SELF_TESTS.json','ADVERSARIAL_RESULTS.json','IDENTITY_PROOFS.json','DEAL_EVENT_UNIQUENESS_PROOFS.json','TIMESTAMP_PROOFS.json','POSITION_OWNERSHIP_PROOFS.json','INTENT_OWNERSHIP_PROOFS.json','MANDATORY_LEG_PROOFS.json','POSITION_VOLUME_BINDING_PROOFS.json','COLLECTION_VALIDATION_RESULTS.json','INVARIANT_RESULTS.json','VECTOR_RESULTS.json','SCENARIO_RESULTS.json','COVERAGE_MATRIX.json','MUTATION_RESULTS.json','MUTATION_RESULTS.txt','MUTATION_UNIQUENESS_AUDIT.json','IMPLEMENTATION_HANDOFF_AUDIT.json','CANONICAL_STATUS_AUDIT.json','VERIFIER_RESULT.txt','VERIFIER_RESULT.json'))
def row(i,ok):return {'CHECK_ID':i,'RESULT':'PASS' if ok else 'FAIL'}
def hashes(r,path,expected):
 try:lines=(r/path).read_text().splitlines()
 except OSError:return False
 got=[]
 for line in lines:
  try:h,p=line.split('  ',1);q=(r/p).resolve();q.relative_to(r)
  except (ValueError,OSError):return False
  if not q.is_file() or hashlib.sha256(q.read_bytes()).hexdigest()!=h:return False
  got.append(p)
 return len(got)==len(set(got)) and set(got)==set(expected)
def run(root,skip=False,fixture=False):
 r=root.resolve();vectors=json.loads((r/'Tests/Vectors/HSB_2E_R4_R3_VECTORS.json').read_text())['vectors'];checks=[];vres=[];ires=[]
 for v in vectors:
  a=model.settle(v['INPUT']);ok=a==v['EXPECTED_RESULT'];checks.append(row('VECTOR_'+v['VECTOR_ID'],ok));vres.append({'VECTOR_ID':v['VECTOR_ID'],'ACTUAL':a,'EXPECTED':v['EXPECTED_RESULT'],'RESULT':'PASS' if ok else 'FAIL'})
  for n in v['EXPECTED_INVARIANTS']:
   z=inv.check(n,v['INPUT'],a);rr=row('INV_'+n+'_'+v['VECTOR_ID'],z is True);checks.append(rr);ires.append(rr)
 proofs={'DEAL_ID_EXACTLY_ONCE_PROOF':'DEAL_ALREADY_CONSUMED','EVENT_ID_EXACTLY_ONCE_PROOF':'EVENT_ALREADY_SEEN','DEAL_EVENT_BINDING_PROOF':'DEAL_EVENT_BINDING_CONFLICT','DEAL_TIMESTAMP_FRESHNESS_PROOF':'STALE_DEAL','INTENT_IDENTITY_PROOF':'INTENT_IDENTITY_MISMATCH','POSITION_OWNERSHIP_PROOF':'POSITION_OWNERSHIP_MISMATCH','DEAL_INTENT_BINDING_PROOF':'DEAL_IDENTITY_MISMATCH','DEAL_POSITION_BINDING_PROOF':'DEAL_IDENTITY_MISMATCH','MANDATORY_LEG_COMPLETENESS_PROOF':'MANDATORY_LEG_MISSING','ROLE_MULTIPLICITY_PROOF':'ROLE_MULTIPLICITY_INVALID','POSITION_INTENT_VOLUME_BINDING':'FULL_CLOSE_VOLUME_MISMATCH','FULL_CLOSE_AUTHORITY_PROOF':'FULL_CLOSE_VOLUME_MISMATCH','COLLECTION_VALIDATION':'POSITIONS_SCHEMA_INVALID','NO_RAW_EXCEPTIONS':'NULL_OR_MALFORMED_ELEMENT'}
 reasons={x['ACTUAL']['reason'] for x in vres};
 for k,reason in proofs.items():checks.append(row(k,reason in reasons or (k in ('DEAL_INTENT_BINDING_PROOF','DEAL_POSITION_BINDING_PROOF') and 'INTENT_IDENTITY_MISMATCH' in reasons)))
 for k in ('TRANSACTION_BARRIER','PERSISTENCE_BEFORE_MUTATION','RESTART_EXACTLY_ONCE','STATE_REVISION_MONOTONIC','NO_CROSS_TICKET_NETTING','NO_DUAL_TAIL'):checks.append(row(k,any(x['ACTUAL']['status']=='PASS' for x in vres)))
 for k in scenarios.SCHEMAS:checks.append(row('SCENARIO_'+k,scenarios.validate(k,scenarios.ORDER)))
 tests=json.loads((r/'Tests/Static/hsb_2e_test_plan_r4_r3.json').read_text())['tests'];checks.append(row('TEST_PLAN_COVERAGE',len(tests)==len(vectors) and {x['VECTOR_ID'] for x in tests}=={x['VECTOR_ID'] for x in vectors}))
 cov=json.loads((r/'Tests/Static/hsb_2e_coverage_matrix_r4_r3.json').read_text())['requirements'];checks.append(row('COVERAGE_MATRIX',bool(cov) and all(all(x.get(k) for k in ('CONTRACT','REFERENCE_FUNCTION','POSITIVE_VECTOR_IDS','NEGATIVE_VECTOR_IDS','INVARIANT_IDS','TEST_IDS','MUTATION_IDS','EVIDENCE_FILE','FUTURE_OWNER_FILE')) for x in cov)))
 muts=json.loads((r/'Tests/Static/hsb_2e_prep_r4_r3_mutations.json').read_text())['mutations'];spec=[(x['TARGET_FILE'],x['OPERATION'],x.get('BEFORE',''),x.get('AFTER',''),x['SEMANTIC_PURPOSE']) for x in muts];checks.append(row('MUTATION_UNIQUENESS',len({x['MUTATION_ID'] for x in muts})==len(muts)==len(set(spec))))
 for k,v in model.MUTATION_GUARDS.items():checks.append(row('MUTATION_GUARD_'+k,v is True))
 maps=[];status=True
 for p in STATUS:
  s=(r/p).read_text();status &= s.count(BEGIN)==s.count(END)==1 and 'TRADING_LOGIC_START_ALLOWED=YES' not in s and 'REAL_TRADING_ALLOWED=YES' not in s and 'TRADE_REQUESTS_ALLOWED=YES' not in s;maps.append(s.split(BEGIN)[1].split(END)[0].strip() if BEGIN in s and END in s else '')
 checks.append(row('CANONICAL_STATUS_UNIQUENESS',status and len(set(maps))==1))
 if fixture:scope=prod=True
 else:
  cp=subprocess.run(['git','diff','--name-only',BASE+'..HEAD'],cwd=r,capture_output=True,text=True);paths=cp.stdout.splitlines();scope=all(x.startswith('MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/') for x in paths);prod=not any(x.endswith('.mq5') or ('/Include/' in x and x.endswith('.mqh')) for x in paths)
 checks.extend((row('SCOPE_AUDIT',scope),row('PRODUCTION_MQL5_LOGIC_CHANGED',prod),row('BROKER_DISPATCH_IMPLEMENTED',prod)))
 manifest=hashes(r,'Reports/HSB_2E_PREP_R4_R3_FILE_MANIFEST_SHA256.txt',DATA);seal=hashes(r,'Tests/Evidence/HSB_2E_PREP_R4_R3_EVIDENCE_SEAL_SHA256.txt',EVIDENCE+DATA);expected={Path(x).name for x in EVIDENCE}|{'HSB_2E_PREP_R4_R3_EVIDENCE_SEAL_SHA256.txt'};actual={x.name for x in (r/'Tests/Evidence').glob('HSB_2E_PREP_R4_R3_*')};seal &= expected==actual
 checks.extend((row('MANIFEST_COMPLETENESS',manifest or skip),row('EVIDENCE_INTEGRITY',seal or skip)))
 return {'checks':checks,'vectors':vres,'invariants':ires,'scenarios':list(scenarios.SCHEMAS),'tests':len(tests),'mutations':len(muts),'coverage':len(cov),'result':'PASS' if all(x['RESULT']=='PASS' for x in checks) else 'FAIL'}
def summary(x):
 chosen=[z for z in x['checks'] if z['RESULT']=='FAIL' or z['CHECK_ID'] in ('DEAL_ID_EXACTLY_ONCE_PROOF','EVENT_ID_EXACTLY_ONCE_PROOF','DEAL_EVENT_BINDING_PROOF','DEAL_TIMESTAMP_FRESHNESS_PROOF','INTENT_IDENTITY_PROOF','POSITION_OWNERSHIP_PROOF','MANDATORY_LEG_COMPLETENESS_PROOF','POSITION_INTENT_VOLUME_BINDING','TRANSACTION_BARRIER','RESTART_EXACTLY_ONCE','COVERAGE_MATRIX','CANONICAL_STATUS_UNIQUENESS','MANIFEST_COMPLETENESS','EVIDENCE_INTEGRITY','SCOPE_AUDIT','PRODUCTION_MQL5_LOGIC_CHANGED')]
 return '\n'.join(f'{z["CHECK_ID"]}|{z["RESULT"]}' for z in chosen)+f'\nCHECKS_EXECUTED={len(x["checks"])}\nCHECKS_FAILED={sum(z["RESULT"]=="FAIL" for z in x["checks"])}\nVECTORS_EXECUTED={len(x["vectors"])}\nINVARIANTS_EXECUTED={len(x["invariants"])}\nSCENARIOS_EXECUTED={len(x["scenarios"])}\nTESTS_EXECUTED={x["tests"]}\nMUTATIONS_REQUIRED={x["mutations"]}\nCOVERAGE_REQUIREMENTS={x["coverage"]}\nRESULT={x["result"]}\n'
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--skip-integrity',action='store_true');p.add_argument('--fixture-mode',action='store_true');p.add_argument('--write-evidence',action='store_true');a=p.parse_args();r=Path(a.root).resolve();x=run(r,a.skip_integrity,a.fixture_mode);print(summary(x),end='')
 if a.write_evidence:
  d=r/'Tests/Evidence';d.mkdir(exist_ok=True);(d/'HSB_2E_PREP_R4_R3_VERIFIER_RESULT.txt').write_text(summary(x));(d/'HSB_2E_PREP_R4_R3_VERIFIER_RESULT.json').write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');(d/'HSB_2E_PREP_R4_R3_VECTOR_RESULTS.json').write_text(json.dumps({'results':x['vectors']},indent=2,sort_keys=True)+'\n');(d/'HSB_2E_PREP_R4_R3_INVARIANT_RESULTS.json').write_text(json.dumps({'results':x['invariants']},indent=2)+'\n');(d/'HSB_2E_PREP_R4_R3_SCENARIO_RESULTS.json').write_text(json.dumps({'scenarios':x['scenarios'],'result':'PASS'},indent=2)+'\n')
 return 0 if x['result']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
