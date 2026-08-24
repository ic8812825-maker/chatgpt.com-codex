#!/usr/bin/env python3
import argparse,hashlib,json
from pathlib import Path
NAMES=('BASELINE_RESULT','R6_FALSE_PASS_REPRODUCTION','EXACT_FALSE_PASS_FIXTURES','LOSSLESS_ADAPTER_MAPS','SEMANTIC_ORACLE','CROSS_VERSION_RESULTS','MIGRATION_DECISIONS','SNAPSHOT_CONTEXT_PROOF','CLOSE_SIDE_PROOF','NEW_FAR_PROVENANCE','CERTIFICATE_RECOMPUTATION','INVARIANT_RESULTS','SEMANTIC_MUTATION_CATALOG','MUTATION_RESULTS','SCOPE_AUDIT','PRODUCTION_DIFF','FINAL_VERDICT','IMPLEMENTATION_HANDOFF')
def run(root):
 root=Path(root).resolve();ev=root/'Tests/Evidence';entries=[]
 for n in NAMES:
  p=ev/f'HSB_2E_PREP_R4_R7_{n}.json';entries.append({'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 manifest={'schemaVersion':1,'entries':entries};mp=ev/'HSB_2E_PREP_R4_R7_MANIFEST.json';mp.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n');seal=hashlib.sha256(json.dumps(entries,sort_keys=True,separators=(',',':')).encode()).hexdigest();(ev/'HSB_2E_PREP_R4_R7_EVIDENCE_SEAL_SHA256.txt').write_text(seal+'\n');print('PUBLISH_RESULT=PASS');return True
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();raise SystemExit(0 if run(a.root) else 1)
