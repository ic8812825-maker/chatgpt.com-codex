#!/usr/bin/env python3
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import run_hsb_2e_r4_r9_r4a_r10_regressions as r10
import verify_hsb_2e_r4_r9_r4a_r10 as v10
import run_hsb_2e_r4_r9_r4a_r11_first_block as block
import run_hsb_2e_r4_r9_r4a_r11_revision_pairs as pairs
OUT=ROOT/'Tests/Evidence/R4A_R11/acceptance.json';BASE='2141806cf32c5c9155f2fd7d7e3600b6bc234681'
def run(include_mutations=True):
 findings=[];old=r10.run();b=block.run();p=pairs.run()
 if old['required']!=67 or old['wrongFailures'] or old['unexpectedInfrastructureErrors']:findings.append({'check':'R10_REGRESSION_PRESERVATION'})
 try:v10.execute()
 except Exception as ex:findings.append({'check':'R10_POSITIVE_PRESERVATION','detail':str(ex)})
 if b['fixtures']!=15 or b['failed'] or b['result']!='PASS':findings.append({'check':'FIRST_BLOCK_TRACES'})
 ind=block.independence();sens=block.evaluator_sensitivity()
 if not all(ind.values()) or not all(x['caught'] for x in sens):findings.append({'check':'EVALUATOR_INDEPENDENCE_OR_SENSITIVITY'})
 if p['failed']:findings.append({'check':'REVISION_CAUSAL_PAIRS'})
 mutation=None
 if include_mutations:
  cp=subprocess.run([sys.executable,'-B','Tests/Static/run_hsb_2e_r4_r9_r4a_r11_causal_mutations.py'],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  if cp.returncode!=0:findings.append({'check':'CAUSAL_MUTATIONS','stderr':cp.stderr})
  else:
   mutation=json.loads(cp.stdout)
   if mutation['result']!='PASS':findings.append({'check':'CAUSAL_MUTATIONS_RESULT'})
 reg=json.loads((ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R11_PROTECTED_FILES.json').read_text())['files'];bad=[x['path'] for x in reg if hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()!=x['sha256']]
 if bad:findings.append({'check':'PROTECTED_FILES','paths':bad})
 changed=subprocess.run(['git','diff','--name-only',f'{BASE}..HEAD'],cwd=ROOT,text=True,check=True,stdout=subprocess.PIPE).stdout.splitlines();prefix='MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/';scope=[x for x in changed if not x.startswith(prefix) or x.endswith(('.mq5','.mqh'))]
 if scope:findings.append({'check':'SCOPE','paths':scope})
 return {'r10Cases':old['executed'],'causalFixtures':b['fixtures'],'predicateCount':7,'revisionPairs':p['required'],'independence':ind,'evaluatorSensitivity':sens,'mutationResult':mutation['result'] if mutation else 'NOT_RUN','findings':findings,'result':'PASS' if not findings else 'FAIL'}
def main():
 p=argparse.ArgumentParser();p.add_argument('--publish-evidence',action='store_true');p.add_argument('--skip-mutations',action='store_true');a=p.parse_args();o=run(not a.skip_mutations)
 if a.publish_evidence:OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
 print(f"RESULT={o['result']} R10={o['r10Cases']} FIXTURES={o['causalFixtures']} PREDICATES={o['predicateCount']} MUTATIONS={o['mutationResult']} FINDINGS={len(o['findings'])}");return 0 if o['result']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
