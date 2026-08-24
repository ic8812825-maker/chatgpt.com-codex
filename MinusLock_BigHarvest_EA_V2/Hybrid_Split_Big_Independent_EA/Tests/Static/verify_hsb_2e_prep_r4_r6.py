#!/usr/bin/env python3
"""Independent R4-R6 verifier: recomputes counts, hashes and critical properties."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
BASE='6c5093a53a8d1701ebcdfa351de1b7c5d534f52a'
def command(args,cwd):return subprocess.run(args,cwd=cwd,capture_output=True,text=True)
def main(root,mutation_fixture=False):
 root=Path(root).resolve();repo=root.parents[1];sys.path.insert(0,str(root/'Tests/Reference'));checks={}
 try:
  from hsb_2e_invariants_r4_r6 import run_checks,CHECK_IDS
  checks.update(run_checks())
  vector_files=('HSB_2E_R4_R2_VECTORS.json','HSB_2E_R4_R3_VECTORS.json','HSB_2E_R4_R4_VECTORS.json');counts=[len(json.loads((root/'Tests/Vectors'/f).read_text())['vectors']) for f in vector_files];checks['R6_HISTORICAL_VECTOR_COUNT']=counts==[30,48,26]
  cv=command([sys.executable,str(root/'Tests/Static/run_hsb_2e_r4_r6_cross_version.py'),'--root',str(root)],root);cvd=json.loads(cv.stdout);checks['R6_CROSS_VERSION_TARGET']=cv.returncode==0 and cvd['HISTORICAL_VECTORS_EXECUTED_ON_R6']==104 and cvd['HISTORICAL_MODELS_USED_AS_TEST_TARGET']==0 and all(r.get('targetModel')=='hsb_2e_reference_model_r4_r6' for r in cvd['rows'])
  exact=json.loads((root/'Tests/Vectors/HSB_2E_R4_R6_EXACT_R5_FALSE_PASSES.json').read_text());from hsb_2e_provenance_model_r4_r6 import digest
  checks['R6_EXACT_FIXTURE_HASHES']=len(exact['cases'])==10 and all(digest(c['exactInput'])==c['EXACT_INPUT_SHA256'] for c in exact['cases'])
  ex=command([sys.executable,str(root/'Tests/Static/run_hsb_2e_r4_r6_exact_false_passes.py'),'--root',str(root)],root);exd=json.loads(ex.stdout);checks['R6_EXACT_FALSE_PASS_REPLAY']=ex.returncode==0 and exd['HEURISTIC_FALSE_PASS_RECONSTRUCTION']==0 and exd['R5_FALSE_PASSES_BLOCKED_BY_R6']==10
  coverage=json.loads((root/'Tests/Contracts/HSB_2E_R4_R6_INVARIANT_COVERAGE.json').read_text())['requirements'];checks['R6_INVARIANT_BINDINGS']=len(coverage)==30 and {r['CHECK_ID'] for r in coverage}==set(CHECK_IDS) and len({r['positiveVector'] for r in coverage})==30 and len({r['negativeVector'] for r in coverage})==30
  for runner,check in (('run_hsb_2e_r4_r6_provenance.py','R6_PROVENANCE_RUNNER'),('run_hsb_2e_r4_r6_economic.py','R6_ECONOMIC_RUNNER'),('run_hsb_2e_r4_r6_scenarios.py','R6_SCENARIO_RUNNER')):checks[check]=command([sys.executable,str(root/'Tests/Static'/runner),'--root',str(root)],root).returncode==0
  if not mutation_fixture:
   branch=command(['git','branch','--show-current'],repo);anc=command(['git','merge-base','--is-ancestor',BASE,'HEAD'],repo);changed=command(['git','diff','--name-only',BASE+'..HEAD'],repo).stdout.splitlines();prefix='MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/';checks['R6_BASELINE_ANCESTRY']=branch.stdout.strip()=='work' and anc.returncode==0;checks['R6_SCOPE_AUDIT']=all(p.startswith(prefix) for p in changed);checks['R6_PRODUCTION_DIFF']=not any(p.endswith('.mq5') or p.startswith(prefix+'Include/') and p.endswith('.mqh') for p in changed)
  failed=[k for k,v in checks.items() if not v]
  for k,v in checks.items():print(f'{k}|{"PASS" if v else "FAIL"}')
  print(f'CHECKS_EXECUTED={len(checks)}\nCHECKS_FAILED={len(failed)}\nFAILURE_IDS={",".join(failed)}\nINFRASTRUCTURE_FAILURE=0\nRESULT={"PASS" if not failed else "FAIL"}')
  return not failed
 except Exception as e:print(f'INFRASTRUCTURE_FAILURE=1\nERROR={type(e).__name__}:{e}\nRESULT=FAIL');return False
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--mutation-fixture',action='store_true');a=p.parse_args();raise SystemExit(0 if main(a.root,a.mutation_fixture) else 1)
