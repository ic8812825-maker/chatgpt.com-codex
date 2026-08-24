#!/usr/bin/env python3
"""Independent R4-R7 verifier: it loads sources/vectors and recomputes outcomes."""
import argparse,importlib,json,subprocess,sys
from pathlib import Path
BASE='78520488d53f3f19eebc254a9cc5a7338714ceb4';PREFIX='MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/'
def run(root):
 root=Path(root).resolve();sys.path.insert(0,str(root/'Tests/Reference'));checks={}
 def check(cid,value):checks[cid]=bool(value);print(f'{cid}|{"PASS" if value else "FAIL"}')
 from hsb_2e_r4_r7_adapter_common import sha
 oracle=json.loads((root/'Tests/Contracts/HSB_2E_R4_R7_SEMANTIC_ORACLE.json').read_text())['vectors'];check('R7_SEMANTIC_ORACLE',len(oracle)==104 and len({(x['version'],x['vectorId']) for x in oracle})==104 and all(x['classification']!='UNRESOLVED' for x in oracle))
 cv=subprocess.run(['python3',str(root/'Tests/Static/run_hsb_2e_r4_r7_cross_version.py'),'--root',str(root)],capture_output=True,text=True);check('R7_LOSSLESS_ADAPTER',cv.returncode==0 and '"HISTORICAL_VECTORS_SEMANTICALLY_COMPARED":104' in cv.stdout);check('R7_NO_SELF_HEALING','broker_fixture' not in (root/'Tests/Reference/hsb_2e_r4_r7_adapter_common.py').read_text() and 'zip(' not in (root/'Tests/Reference/hsb_2e_r4_r7_adapter_common.py').read_text())
 for cid,script in [('R7_SNAPSHOT_CONTEXT_BINDING','run_hsb_2e_r4_r7_price_adversarial.py'),('R7_NORMATIVE_CLOSE_SIDES','run_hsb_2e_r4_r7_price_adversarial.py'),('R7_OUTPUT_STATE_RECOMPUTATION','run_hsb_2e_r4_r7_certificate_adversarial.py'),('R7_CERTIFICATE_BROKER_RECOMPUTATION','run_hsb_2e_r4_r7_certificate_adversarial.py'),('R7_CERTIFICATE_ECONOMIC_RECOMPUTATION','run_hsb_2e_r4_r7_certificate_adversarial.py'),('R7_CERTIFICATE_ALLOCATION_RECOMPUTATION','run_hsb_2e_r4_r7_certificate_adversarial.py'),('R7_CERTIFICATE_PERSISTENCE_RECOMPUTATION','run_hsb_2e_r4_r7_certificate_adversarial.py'),('R7_BIG_RESIDUAL_PROVENANCE','run_hsb_2e_r4_r7_new_far_adversarial.py'),('R7_NEW_FAR_VOLUME_CONSERVATION','run_hsb_2e_r4_r7_new_far_adversarial.py')]:
  p=subprocess.run(['python3',str(root/'Tests/Static'/script),'--root',str(root)],capture_output=True,text=True);check(cid,p.returncode==0)
 changed=subprocess.check_output(['git','diff','--name-only',f'{BASE}..HEAD'],cwd=root,text=True).splitlines();check('R7_SCOPE_AUDIT',all(p.startswith(PREFIX) for p in changed));check('R7_PRODUCTION_DIFF',not any(p.endswith('.mq5') or ('/Include/' in p and p.endswith('.mqh')) for p in changed))
 forbidden=('OrderSend(','OrderSendAsync(','CTrade','MqlTradeRequest');added=subprocess.check_output(['git','diff','--unified=0',f'{BASE}..HEAD'],cwd=root,text=True);check('R7_BROKER_DISPATCH_DISABLED',not any(line.startswith('+') and any(x in line for x in forbidden) for line in added.splitlines()))
 check('R7_REAL_MODEL_MUTATION_SENSITIVITY',(root/'Tests/Static/run_hsb_2e_r4_r7_semantic_mutations.py').exists())
 failed=[k for k,v in checks.items() if not v];print(f'CHECKS_EXECUTED={len(checks)}');print('FAILURE_IDS='+','.join(failed));print('INFRASTRUCTURE_FAILURE=0');print('RESULT='+('PASS' if not failed else 'FAIL'));return not failed
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();
try:ok=run(a.root)
except Exception as e:print(f'INFRASTRUCTURE_FAILURE=1\nFAILURE_IDS=R7_UNHANDLED_{type(e).__name__}\nRESULT=FAIL');ok=False
raise SystemExit(0 if ok else 1)
